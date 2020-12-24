# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/mk/mktable.py
# Compiled at: 2003-08-02 18:46:25
from pytable import dbtable
from basicproperty import common

class MkTable(dbtable.DBTable):
    """Metakit table"""
    __module__ = __name__
    propertyClass = common.ClassByNameProperty('propertyClass', 'The class used for creating property objects', defaultValue='pytable.metakit.mkdescriptor.MkDescriptor')