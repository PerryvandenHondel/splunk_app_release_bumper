#!/bin/python3

##
## BUMPER.PY
##
## Script to bump the release of a Splunk App to a new version
##
## Actions to perform:
## 1) Update the version number in the apps.conf file
## 2) Copy all files from local/ to default/ for newer files that are changed.
## 3) Update the git repo with all changes in this new version of the app.
## 4) Create a compressed archive .tar.gz of the new file in a releases dir. 
##



from icecream import ic
import configparser
import os
import stat
import sys



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



def get_script_name():
    ##
    ## From a directory name get the Splunk App name.
    ##
    ## From '/opt/splunk/etc/apps/UMBRIO_SA_scmdb/' get 'UMRBIO_SA_scmdb'.
    ##

    # TODO: change this so that the script name without the extention is returned
    # ~/dev/python/bumber/bumper.py should return: bumper
    return('bumper')



def dir_add_slash(dir):
    ic()
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



def show_title():
    print(sys.argv[0].upper())
    print()
    print('Bump the release version of a Splunk App')
    print()



def show_usage():
    print('Usage:')
    print('\t' + sys.argv[0] + ' [Splunk App Name]')
    print()
    exit()



def update_version_in_app_conf(dir_splunk_app_name):
    ic()
    ic(dir_splunk_app_name)
    path_app_conf = dir_add_slash(dir_splunk_app_name) + 'default/app.conf'
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



def copy_files_from_local_to_default(dir_splunk_app_name):
    ##
    ## Copy the files from the local directory to the default directory.
    ## But only when the 'local/' version of the file is newer then the
    ## 'default/' version of the same file.
    ##
    ## Input:
    ##      dir_splunk_app_name:    Then directory that holds the default and local directories
    ##                              /opt/splunk/etc/apps/appname
    ic()
    
    dir_local = dir_add_slash(dir_splunk_app_name) + 'local/'
    dir_default = dir_add_slash(dir_splunk_app_name) + 'default/'

    ## Rsync options used:
    ##      --progress      show progress during transfer  
    ##      --recursive     recurse into directories
    ##      --update        skip files that are newer on the receiver
    cmd = 'rsync --progress --recursive --update "' + dir_local + '" "' + dir_default + '"'
    print(cmd)
    ic(cmd)
    


def update_git_repo():
    ic()



def create_archive_file():
    ic()



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

    ic(splunk_app)

    config = configparser.ConfigParser()
    config.read(get_config_name())

    script_name = get_script_name()
    dir_splunk_apps = config.get(script_name, 'SplunkAppsDir')
    ic(dir_splunk_apps)

    dir_splunk_app_name = dir_add_slash(dir_splunk_apps) + splunk_app
    ic(dir_splunk_app_name)

    ## 1) Update the version number in the apps.conf file; return new version number.
    new_version = update_version_in_app_conf(dir_splunk_app_name)
    ic(f'New version set in app.conf file {new_version}')

    ## 2) Copy all files from local/ to default/ for newer files that are changed.
    copy_files_from_local_to_default(dir_splunk_app_name)

    ## 3) Update the git repo with all changes in this new version of the app.
    update_git_repo()

    ## 4) Create a compressed archive .tar.gz of the new file in a releases dir.
    create_archive_file() 
    
    print(f'End of script!')



if __name__ == "__main__":
    main()



# EOS