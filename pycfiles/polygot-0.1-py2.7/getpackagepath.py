# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/commonutils/getpackagepath.py
# Compiled at: 2016-10-07 10:50:01
"""
*Get common file and folder paths for the host package*

:Author:
    David Young

:Date Created:
    October  4, 2016
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