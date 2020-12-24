# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/git_repos/dryxDropboxCL/dryxDropboxCL/commonutils/getpackagepath.py
# Compiled at: 2016-06-17 04:40:49
"""
*Get common file and folder paths for the host package*

:Author:
    David Young

:Date Created:
    October 24, 2013

.. todo::
    
    - [ ] when complete pull all general functions and classes into dryxPython
"""
import sys, os
from docopt import docopt

def getpackagepath():
    """
    *getpackagepath*

    **Key Arguments:**
        - None

    **Return:**
        - ``packagePath`` -- path to the host package

    .. todo::

        - when complete, clean worker function and add comments
        - when complete add logging
    """
    moduleDirectory = os.path.dirname(__file__)
    packagePath = os.path.dirname(__file__) + '/../'
    return packagePath


if __name__ == '__main__':
    main()