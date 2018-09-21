# Jive Group Name Changer
Jive offers two types of places: groups and spaces. Spaces are easily modified and the permission system is extremely granular and robust. For most groupings they are overkill. Enter Groups.

Groups are meant to be quickly and easily implemented and managed by folks that may not have the technical acuity to set up complex permission systems. The downside of this is that these groups also have far fewer administrative controls. The most problematic missing feature is the ability to change the URL for the group.

The purpose of this project is to script these changes through the use of the Jive APIs. The alternative is a paid consulting engagment, which we do not have budget for.

## About this script
This script is written in Python and built with Python3. To run, simply install Python3, ensure it is in your environment PATH, and run from the commandline:

> python changeGroupUrl.py -j <Jive-site-domain\> -u <username\> -p <password\> -g <old-group-name\> -n <new-group-name\>

If you like, you can add the -d flag to turn on debug mode and follow the script more closely through print statements.

## License
This project is licensed under the MIT license

## Additional Help
As an open source project, feel free to issue pull requests to make improvements or offer additional functionality. If you have questions, use the tools available via github and I will respond as soon as possible.
