# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/exception.py
# Compiled at: 2008-09-11 19:48:09
from AccessControl import ModuleSecurityInfo
modulesec = ModuleSecurityInfo('Products.Relations.exception')
modulesec.declarePublic('ValidationException')

class ValidationException(Exception):
    __module__ = __name__
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, message, reference=None, chain=None):
        self.message = message
        self.reference = reference
        self.chain = chain
        self.args = (
         self.message, self.reference)