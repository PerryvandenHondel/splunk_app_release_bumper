#!/bin/python3

'''
SPLUNK_APP_BUMP_RELEASE.PY

Script to bump the release of a Splunk App to a new version

Steps:

1)  Update the version number in config /opt/splunk/etc/apps/app_name/local/app.conf
2)  Push to a Git repo when exists
3)  Copy the directory /opt/splunk/etc/apps/app_name to /tmp/app_name
4)  Rename the direcory /tmp/app_name/local to /tmp/app_name/default
5)  Compress the dir  /tmp/app_name to app_name.gz
'''

from icecream import ic
import configparser
import os
import shutil
import sys


def show_title():
    print(sys.argv[0].upper())
    print()
    print('Bump the release version of a Splunk App, do:')
    print('\tUpdate the version number in app.conf')
    print('\tCreate a archive file')
    print()


def show_usage():
    print('Usage:')
    print()
    print('\t' + sys.argv[0] + ' [Splunk App Name]')
    print()
    exit()


def get_config_name():
    '''
    Get the config name (script.conf) for the current script.
    
    Parameters:
        None
        
    Returns:
        Returns a config name 
    '''
    script_name = os.path.realpath(__file__)
    #script_name = os.path.basename(sys.argv[0])
    config_name = script_name.replace('.py', '.conf')
    return config_name


def ensure_dir(dir):
    '''
    Make sure the directory is created.
    
    Parameters:
        dir: Must end with a slash, otherwise this is not seen as a directory.
            /var/log/name  = /var/log is the directory
            /var/log/name/ = /var/log/name is the directory
    '''
    directory = os.path.dirname(dir)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            ic(e.errno)


def dir_add_slash(dir):
    '''
    Returns a directory name that ends with a slash (dir/)
    Adds a slash when it's missing. 
    
    Parameters:
        dir: The directory name to check
    
    
    Example:
        dir1/name -> dir1/name/     Add back slash
        dir2/name/ -> dir2/name/    No change
    
    Returns:
        A directory that ends with a slash
    '''
    if dir.endswith('/'):
        return dir
    else:
        return dir + '/'


def execute_cmd(command_line):
    '''
    Execute a command on the command line 
    
    Parameters:
        command_line: command to execute
    
    Returns:
        The return code of the executed command
    '''
    rc = os.system(command_line)
    #ic(f'command="execute_cmd" command_line="{command_line}" rc={rc}')
    return rc


def update_git_repo(dir_splunk_app_name, new_version):
    '''
    Add new files to local repo and push to remote repo.
    Use the new_version variable to mark the git commit.
    
    Parameters:
        dir_splunk_app_name: The directory to update
        new_version: The new version number to use a the commit text.
    
    Returns:
        None
    '''
    ic()
    ic(dir_splunk_app_name, new_version)

    #print('GIT ACTIONS(): writing git actions to bash script.')
    #fw.write('\n')
    #fw.write('git add ' + path + '\n')
    #fw.write('git commit -m "v' + version + '"\n')
    #fw.write('git push\n')

    ## Get the current working dir.
    current_working_dir = os.getcwd()
    ic(current_working_dir)

    ## Change to the directory where the app is located.
    os.chdir(dir_splunk_app_name)

    cmd = 'git add .'
    ic(cmd)
    rc = execute_cmd(cmd)

    cmd = 'git commit -m "Release v' + new_version + '"'
    ic(cmd)
    rc = execute_cmd(cmd)

    cmd = 'git push'
    ic(cmd)
    rc = execute_cmd(cmd)

    ## Change back to the working directory
    os.chdir(current_working_dir)


def update_version_in_app_conf(dir_splunk_app_name):
    ic()
    ic(dir_splunk_app_name)
    path_app_conf = dir_add_slash(dir_splunk_app_name) + 'local/app.conf'
    ic(path_app_conf)

    path_app_conf_tmp = path_app_conf + '.tmp'
    ic(path_app_conf_tmp)

    if os.path.exists(path_app_conf):
        ic(f'Found the app.conf file at {path_app_conf}')

        ## Rename the app.conf file to app.conf.tmp
        os.rename(path_app_conf, path_app_conf_tmp)

        ## Open the conf.tmp; walk thru and show current version.
        ## ask for new version and write to conf file.
   
        ## Write the the new app.conf
        f_app = open(path_app_conf, 'w')

        ## Read the app.conf.tmp from the original version.
        f_tmp = open(path_app_conf_tmp, 'r')
        for line in f_tmp:
            line = line.strip()
            print(line)
            if 'version = ' in line:
                print('CURRENT VERSION:')
                print(line)
                new_version = input('Enter new version: ')
                f_app.write('version = ' + new_version + '\n')
            else:
                f_app.write(line + '\n')

        f_tmp.close()
        f_app.close()

        ## Remove the app.conf.tmp file
        os.remove(path_app_conf_tmp)
    else:
        print(f'ERROR: Missing app.conf file {path_app_conf}')

    return new_version


def rename_directory(original_name, new_name):
    try:
        os.rename(original_name, new_name)
        print(f"Directory '{original_name}' renamed to '{new_name}'.")
    except OSError:
        print(f"Failed to rename directory '{original_name}' to '{new_name}'.")


def copy_directory_tree(original_path, new_path):

    ## Remove existing directory tree

    try:
        shutil.rmtree(new_path)
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")


    try:
        shutil.copytree(original_path, new_path)
        print(f"Directory tree copied from '{original_path}' to '{new_path}'.")
    except OSError:
        print(f"Failed to copy directory tree from '{original_path}' to '{new_path}'.")


def create_archive_file(config, dir_splunk_apps, splunk_app, new_version):
    '''
    Create an archive and compress the Splunk app dir into a 
    new archive named with the version number in the archive name.

    Parameters:
        config: Pointer to the config object
        dir_splunk_apps:
        splunk_app:
        new_version:

    Returns:
        None
    '''
    ic()
    ic(config, dir_splunk_apps, splunk_app, new_version)

    dir_releases = config.get('settings', 'DirReleases')
    ic(dir_releases)
    
    path_archive = dir_add_slash(dir_releases) + splunk_app + '_' + new_version + '.tar.gz'
    ic(path_archive)

    ensure_dir(path_archive)

    ## Get the current working dir.
    current_working_dir = os.getcwd()
   
    os.chdir(dir_splunk_apps)
  
    # 'tar cvzf ' + path_tar + ' --exclude=.git --exclude=local --exclude=DEV --exclude=do_bump_release.sh --exclude=.gitignore ' + app_name + '/'
    cmd =  'tar cvzf "' + path_archive + '" --exclude=.git --exclude=.gitignore --exclude=local --exclude=DEV "' + dir_add_slash(splunk_app) + '"'
    print(cmd)
    ic(cmd)
    execute_cmd(cmd)

    ## Change back to the working directory
    os.chdir(current_working_dir)



def main():
    show_title()

    num_args = len(sys.argv) - 1

    if num_args == 1:
        splunk_app = sys.argv[1]
        if len(splunk_app) == 0:
            print()
            print(f'**ERROR: Invalid Splunk App name ({splunk_app}) is not correct!')
            print()
            show_usage()
    else:
        show_usage()

    print(splunk_app)

    config = configparser.ConfigParser()
    config.read(get_config_name())

    dir_splunk_apps = config.get('settings', 'DirSplunkApps')
    ic(dir_splunk_apps)

    dir_splunk_app_name = dir_add_slash(dir_splunk_apps) + splunk_app
    ic(dir_splunk_app_name)

    dir_releases = config.get('settings', 'DirReleases')
    ic(dir_releases)

    dir_temp = config.get('settings', 'DirTemp')
    ic(dir_temp)

    ## Update the app.conf to reflect the new version
    new_version = update_version_in_app_conf(dir_splunk_app_name)

    ## Push this local repo to the remote repo. Use the version number as
    ## a commit message.
    if os.path.isdir(dir_add_slash(dir_splunk_app_name) + '.git') == True:
        update_git_repo(dir_splunk_app_name, new_version)
    
    ## Copy the current Splunk App /opt/splunk/etc/apps/app_name to
    ## /tmp/app_name including the complete tree of dirs and files.
    new_dir_splunk_app_name = dir_add_slash(dir_temp) + splunk_app
    ic(dir_splunk_app_name, new_dir_splunk_app_name)
    copy_directory_tree(dir_splunk_app_name, new_dir_splunk_app_name)

    ## Rename the local dir to the default dir.
    dir_local = dir_add_slash(new_dir_splunk_app_name) + 'local'
    dir_default = dir_local.replace('local', 'default')
    
    ic(dir_local)
    ic(dir_default)
    rename_directory(dir_local, dir_default)

    ## Create a compressed archive file splunk_app.version.tar.gz
    create_archive_file(config, dir_temp, splunk_app, new_version)


if __name__ == "__main__":
    main()


# EOS