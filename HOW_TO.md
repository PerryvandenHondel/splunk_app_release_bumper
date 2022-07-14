Hot to bump the release of a Splunk app using this script bump_release.py

[__TOC__]

Go to the directory of the app under the Splunk directory:

> cd /opt/splunk/etc/apps/theapptobump

# Update .gitignore file
Add
'''
**/DEV/*
'''
to the Git ignore file. '.gitignore'


# Run Python script
Run the Python script:

'''
> /home/perry/dev/python/bump_release/bump_release.py
'''

# Update the version number
Script reads the current version; you are asked to enter a new version number:

CURRENT VERSION:
version = 1.5.0
Enter new version: 1.6.0

# Build the new package
Run the shell script to do a git update and create an archive

'''
> ./DEV/do_bump_release.sh
'''
