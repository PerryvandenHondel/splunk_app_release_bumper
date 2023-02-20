How to bump the release/version of a Splunk app using this script 


SPLUNK_APP_BUM_RELEASE.PY

# CONFIGUREATION
The configuration of the script is done through a .conf file.

Options
- DirSplunkApps: Directory where Splunk Apps are located
- DirReleases: Directory where to store the created archives of Splunk Apps
- DirTemp: A Directory to store the files in for the run of the script 

Example configuration splunk_app_bum_release.conf

```
[settings]
## Directory where Splunk Apps are located.
DirSplunkApps=/opt/splunk/etc/apps/

## Directory where to store the created archives of Splunk Apps.
DirReleases=/home/perry/dev/Splunk_Apps_Releases

DirTemp=/tmp

```

# GITIGNORE
Add all files and directories to the .gitignore file that do not need to be in the repo.

# USAGE

1) Configure the .conf file with your settings.

2) Run the script splunk_app_bum_release.py with the name of the Splunk app that needs it's release/version number increased.

```
splunk_app_bump_release.py [Splunk App Name]
```

Example:

```
> splunk_app_bump_release.py UMBRIO_SA_toexitnodes
```

# ACTIONS
The script will perform the following actions:

1. Update the version number in the apps.conf file
2. Updates the repo if the app is under source controle. Commit messag with "Release vX.X.X"
3. Makes a copy of the whole app to the temp dir.
4. Renames local/ to default/ directory
5. Create a compressed archive .tar.gz of the new file in the releases dir.

On the Splunk instance where the app is developed do a Debug Refresh to use the configs that are in the default dir.

http://voyager:8000/en-GB/debug/refresh
