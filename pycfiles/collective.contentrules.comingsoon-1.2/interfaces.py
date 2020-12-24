# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentmigrationui/interfaces.py
# Compiled at: 2010-08-17 07:07:37
from zope.interface import Interface
from zope.interface import Attribute

class IContentMigrator(Interface):
    """Interface for migrator registration"""
    __module__ = __name__
    title = Attribute('The migration title')
    src_meta_type = Attribute('source content meta type')
    src_portal_type = Attribute('source content portal type')
    dst_meta_type = Attribute('destination content meta type')
    dst_portal_type = Attribute('destination content portal type')