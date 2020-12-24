# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/content/landsection.py
# Compiled at: 2017-09-19 09:07:49
""" Land content-types
"""
from zope.interface import implements
from Products.ATContentTypes.content.folder import ATFolder
from land.copernicus.content.content.interfaces import ILandSection
from land.copernicus.content.content import schema

class LandSection(ATFolder):
    """ Section
    """
    implements(ILandSection)
    meta_type = 'LandSection'
    portal_type = 'LandSection'
    archetype_name = 'LandSection'
    schema = schema.SECTION_SCHEMA