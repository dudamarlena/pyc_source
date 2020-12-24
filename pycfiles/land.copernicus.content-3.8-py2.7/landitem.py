# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/content/landitem.py
# Compiled at: 2018-02-05 08:31:50
""" Land content-types
"""
from zope.interface import implements
from Products.ATContentTypes.content.folder import ATFolder
from land.copernicus.content.content import schema
from land.copernicus.content.content.interfaces import ILandItem
from land.copernicus.content.content.landfile import LandFileStore

class LandItem(ATFolder):
    """ Land Item
    """
    implements(ILandItem)
    meta_type = 'LandItem'
    portal_type = 'LandItem'
    archetype_name = 'LandItem'
    schema = schema.ITEM_SCHEMA
    _landfiles = None

    @property
    def landfiles(self):
        """ BTree land file storage for faster operation.
            Title and shortnames need to be unique, as they are used as keys!
        """
        if self._landfiles is None:
            self._landfiles = LandFileStore()
        return self._landfiles