# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/commonutils/getpackagepath.py
# Compiled at: 2020-04-17 06:44:40
"""
*Get the root path for this python package*

:Author:
    David Young
"""
import os

def getpackagepath():
    """
    *Get the root path for this python package*

    *Used in unit testing code*
    """
    moduleDirectory = os.path.dirname(__file__)
    packagePath = os.path.dirname(__file__) + '/../'
    return packagePath