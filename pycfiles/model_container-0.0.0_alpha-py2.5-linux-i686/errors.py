# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/model_container/errors.py
# Compiled at: 2011-09-09 23:42:50
"""!
@file errors.py

This file contains custom exception error objects
for use in reporting errors in nmc.
"""

class NoOutputFilenameError(Exception):

    def __init__(self, errormsg):
        self.errormsg = errormsg

    def __str__(self):
        return self.errormsg


class ParameterError(Exception):

    def __init__(self, errormsg):
        self.errormsg = errormsg

    def __str__(self):
        return self.errormsg


class ImportChildError(Exception):

    def __init__(self, errormsg):
        self.errormsg = 'Symbol Import Child Error: %s' % errormsg

    def __str__(self):
        return self.errormsg


class SymbolError(Exception):

    def __init__(self, errormsg):
        self.errormsg = 'Symbol Error: %s' % errormsg

    def __str__(self):
        return self.errormsg


class LibraryPathError(Exception):

    def __init__(self, errormsg=''):
        self.errormsg = "Can't find a suitable model library path, please set one\n        of the following variables to point to the appropriate directory (absolute path)\n        that contains your ndf library: NEUROSPACES_NMC_USER_MODELS, NEUROSPACES_NMC_PROJECT_MODELS,\n        NEUROSPACES_NMC_SYSTEM_MODELS or NEUROSPACES_NMC_MODELS\n        "

    def __str__(self):
        return self.errormsg