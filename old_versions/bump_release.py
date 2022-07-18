#!/bin/python3

##
## bump_release.py
##
## v01
## 
## Read the app.conf of the application.
## Show the current version and ask for new version.
## Do a git commit with the new version
## Build tar file with new version (appname_x.y.z.tar.gz)
##


import configparser
import os
import sys
import stat


def ensure_dir(dir):
    ##
    ## Make sure the directory is created.
    ##
    ## dir: Must end with a slash, otherwise this is not seen as a directory.
    ##        /var/log/name  = /var/log is the directory
    ##        /var/log/name/ = /var/log/name is the directory
    ##
    directory = os.path.dirname(dir)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_config_name():
    ##
    ## Get the config name (script.conf) for the current script.
    ##
    ## Returns a config name 
    ##
    script_name = os.path.realpath(__file__)
    #script_name = os.path.basename(sys.argv[0])
    config_name = script_name.replace('.py', '.conf')
    return config_name



def get_bash_script_name():
    ##
    ## Returns a Bash script name
    ##
    script_name = get_script_name()
    #return script_name.replace('.py', '.sh')
    return "do_bump_release.sh"


def get_script_name():
    ##
    ##
    ##
    return os.path.basename(sys.argv[0])


def update_default(fw):
    ##
    ## Copy all newer files from local/* to default/* using rsync.
    ##
    print('RSYNC:')
    fw.write('\n')
    fw.write('rsync --progress -r -u local/* default/')
    fw.write('\n')


def git_actions(fw, path, version):
    #print('git_action(): add "' + path + '" to git and commit a new version: ' + version)
    print('GIT ACTIONS(): writing git actions to bash script.')
    fw.write('\n')
    fw.write('git add ' + path + '\n')
    fw.write('git commit -m "v' + version + '"\n')
    fw.write('git push\n')
    

def tar_actions(fw, path, version):
    try:
        dir_releases = config.get(app_name, 'DirReleases')
    except configparser.NoSectionError:
        print(f'ERROR: No config section found in bump_release.conf for {app_name}!')
        exit()


    #app_name= config.get('Settings', 'NameApp')

    #dir_app = path.replace('default/app.conf', '')
    cd_to = current_working_directory.replace(app_name, '')

    path_tar = dir_releases + '/' + app_name + '.' + version + '.tar.gz'
    print('TAR ACTIONS:')
    #print(path_tar)
    #tar cvzf /tmp/UMBRIO_SA_scmdb_1.0.x.tar.gz  --exclude=.git --exclude=local --exclude=DEV --exclude=do_bump_release.sh --exclude=.gitignore UMBRIO_SA_scmdb/
    fw.write('cd ' + cd_to + '\n')
    
    command_line = 'tar cvzf ' + path_tar + ' --exclude=.git --exclude=local --exclude=DEV --exclude=do_bump_release.sh --exclude=.gitignore ' + app_name + '/'
    print('\t' + command_line)

    fw.write(command_line + '\n')
    print()


def get_app_name(directory):
    ##
    ## From a directory name get the Splunk App name.
    ##
    ## From '/opt/splunk/etc/apps/UMBRIO_SA_scmdb/' get 'UMRBIO_SA_scmdb'.
    ##
    parts = directory.split('/')
    return parts[5]


def dir_add_slash(dir):
    ##
    ## Returns a directory name that ends with a slash (dir/)
    ## Adds a slash when it's missing. 
    ##
    ## Example:
    ## - dir1/name -> dir1/name/     Add back slash
    ## - dir2/name/ -> dir2/name/    No change
    ##
    ## Parameters:
    ## - dir: The directory name to check
    ##
    ## Returns:
    ## - A directory that ends with a slash
    ##
    if dir.endswith('/'):
        return dir
    else:
        return dir + '/'


def update_app_version(app_name):
    print()
    print('update_app_version(): ' + app_name)
    global new_version
    new_version = "0.0"

    path_app_conf_old = path_app_conf + '.old'
    print('path_app_conf_old: ' + path_app_conf_old)

    print(f'update_app_version(): {path_bash_script}')

    #if os.path.exists(path_bash_script):
    #    os.remove(path_bash_script)

    #f_bash = open(path_bash_script, 'w')
    #f_bash.write('#!/bin/bash\n')

    ## Check if the app.conf file exists; then continue
    if os.path.exists(path_app_conf):
        print(f'Found the {path_app_conf}')

        ## Rename the conf file to conf.old
        os.rename(path_app_conf, path_app_conf_old)

        ## Open the conf.old; walk thru and show current version.
        ## ask for new version and write to conf file.
   
        f_new = open(path_app_conf, 'w')

        f_old = open(path_app_conf_old, 'r')
        for line in f_old:
            line = line.strip()
            print(line)
            if 'version = ' in line:
                print('CURRENT VERSION:')
                print(line)
                new_version = input('Enter new version: ')
                f_new.write('version = ' + new_version + '\n')
            else:
                f_new.write(line + '\n')

        f_old.close()
        f_new.close()

        os.remove(path_app_conf_old)
    else:
        print('ERROR: Can''t find file "' + path_app_conf_old + '"')
    return new_version



def main():
    global config
    global current_working_directory
    global path_script
    global path_bash_script
    global path_app_conf
    global app_name

    #print(get_config_name())

    config = configparser.ConfigParser()
    config.read(get_config_name())

    current_working_directory = os.getcwd()

    print('Current working directory: ' + current_working_directory)

    app_name = get_app_name(current_working_directory)
    print('Splunk App name: ' + app_name)
    
    path_script = get_script_name()
    print('Path script: ' + path_script)
    

    bash_script_name = get_bash_script_name()
    print('Bash script: ' + bash_script_name)
    
    
    path_bash_script = dir_add_slash(current_working_directory) + 'DEV/' + bash_script_name
    ensure_dir(path_bash_script)
    print('Path Bash script: ' + path_bash_script)

    path_app_conf = dir_add_slash(current_working_directory) + 'default/app.conf'
    print('path_app_conf: ' + path_app_conf)
    
    new_version = update_app_version(app_name)

    f_bash_script = open(path_bash_script, 'w')
    f_bash_script.write('#!/bin/bash\n')
    
    update_default(f_bash_script)

    git_actions(f_bash_script, path_app_conf, new_version)

    tar_actions(f_bash_script, path_app_conf, new_version)

    f_bash_script.close()

    st = os.stat(path_bash_script)
    os.chmod(path_bash_script, st.st_mode | stat.S_IEXEC)

    print('Done writing to ' + path_bash_script)


if __name__ ==  "__main__":
    main()

## EOS