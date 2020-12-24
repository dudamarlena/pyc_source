# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/commonutils/getpackagepath.py
# Compiled at: 2016-10-07 10:50:01
__doc__ = '\n*Get common file and folder paths for the host package*\n\n:Author:\n    David Young\n\n:Date Created:\n    October  4, 2016\n'
import os

def getpackagepath():
    """
     *Get the root path for this python package*

    *Used in unit testing code*
    """
    moduleDirectory = os.path.dirname(__file__)
    packagePath = os.path.dirname(__file__) + '/../'
    return packagePath