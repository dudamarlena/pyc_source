# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sloancone/commonutils/getpackagepath.py
# Compiled at: 2020-05-06 13:40:52
"""
*Get common file and folder paths for the host package*

:Author:
    David Young
"""
import sys, os
from docopt import docopt

def getpackagepath():
    """
    *getpackagepath*
    """
    moduleDirectory = os.path.dirname(__file__)
    packagePath = os.path.dirname(__file__) + '/../'
    return packagePath


if __name__ == '__main__':
    main()