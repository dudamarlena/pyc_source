# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: package/errors.py
# Compiled at: 2010-05-16 23:47:58
__doc__ = 'This module provides package management support stuff.\n'
import sys
ENONAME = "\nThe 'name' entry is required in your `info.yaml` file.\n\n"
ENOSETUP = "\nFor some bizarre reason, I cannot locate your Python 'setuptools' or\n'distutils' packages. Paint me pathetic, but I just cannot go on at this\npoint.\n\n"
ENOINFO = "\nI can't find the 'package.info' module. If you are the author of this package,\nplease run this command:\n\n    make package-info\n\nIf you are simply some dude installing this Python package, please contact the\nauthor about the missing 'package.info' module.\n\n"
ENOYAML = '\nYou need to install pyyaml to use the package-py framework as a package author.\n\n'
ENOHOMEINFO = '\nYou need to have a file called $HOME/.package-py/info.yaml. This is where you\nput the default info that applies to all your packages.\n\nJust copy ./package/info.yaml to that name and edit it.\n\n'
ENOLOCALINFO = "\nStrange. I can't find the file called ./package/info.yaml. Did you delete it?\n\n"
ELOCALINFONOTSET = "\nIt seems like you haven't edited the ./package/info.yaml file yet. You need to\nput all the pertinent information in there in order to proceed.\n\n"
ENOSETUPTOOLS = "\nThe package you are trying to install depends on an installation feature that\nrequires the 'setuptools' Python module, but you do not have that module\ninstalled. You will need to install 'setuptools' before proceeding with this\ninstall.\n\nYou can find setuptools here:\n\n    http://pypi.python.org/pypi/setuptools/\n\n"

def die(msg):
    sys.stderr.write(msg)
    sys.exit(1)