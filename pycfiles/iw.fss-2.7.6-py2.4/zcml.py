# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/zcml.py
# Compiled at: 2008-10-23 05:55:17
"""
ZCML fss namespace handling, see meta.zcml
"""
__author__ = 'glenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import logging
from zope.interface import Interface
from zope.configuration.fields import GlobalObject, Tokens, PythonIdentifier
import config
from FileSystemStorage import FileSystemStorage

class ITypeWithFSSDirective(Interface):
    """Schema for fss:typeWithFSS directive"""
    __module__ = __name__
    class_ = GlobalObject(title='Class', description='Dotted name of class of AT based content type using FSS', required=True)
    fields = Tokens(title='Fields', description='Field name or space(s) separated field names', value_type=PythonIdentifier(), required=True)


def typeWithFSS(_context, class_, fields):
    """Register our monkey patch"""
    _context.action(discriminator=(class_.__module__, class_.__name__), callable=patchATType, args=(class_, fields))


logger = logging.getLogger(config.PROJECTNAME)
LOG = logger.info

def patchATType(class_, fields):
    """Processing the type patch"""
    global patchedTypesRegistry
    for fieldname in fields:
        field = class_.schema[fieldname]
        former_storage = field.storage
        field.storage = FileSystemStorage()
        field.registerLayer('storage', field.storage)
        if patchedTypesRegistry.has_key(class_):
            patchedTypesRegistry[class_][fieldname] = former_storage
        else:
            patchedTypesRegistry[class_] = {fieldname: former_storage}
        LOG("Field '%s' of %s is stored in file system.", fieldname, class_.meta_type)


patchedTypesRegistry = {}