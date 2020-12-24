# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/configuration/schema.py
# Compiled at: 2008-10-23 05:55:16
"""
FSS configuration schema factory
$Id: schema.py 63747 2008-04-27 13:46:09Z glenfant $
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import os
from ZConfig.datatypes import Registry
from ZConfig.loader import SchemaLoader
import datatypes
_this_dir = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE = os.path.join(_this_dir, 'schema.xml')
fssRegistry = Registry(stock=None)
fssRegistry.register('existing-storage-path', datatypes.existingStoragePath)
fssRegistry.register('existing-backup-path', datatypes.existingBackupPath)
fssRegistry.register('default-strategy', datatypes.default_strategy)
fssRegistry.register('strategy', datatypes.strategy)
fssSchema = None

def loadSchema(filepath, registry=fssRegistry, overwrite=False):
    """Sets up fssSchema
    @param filepath: path to schema xml file
    @param registry: ZConfig.datatypes.Registry
    @param overwrite: True to change fss
    """
    global fssSchema
    if fssSchema is not None and not overwrite:
        raise RuntimeError, 'Schema already loaded'
    schemaLoader = SchemaLoader(registry=registry)
    fssSchema = schemaLoader.loadURL(filepath)
    return fssSchema


loadSchema(SCHEMA_FILE)
__all__ = 'fssSchema'