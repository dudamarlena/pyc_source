# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/metadata/browser/views.py
# Compiled at: 2009-09-04 10:38:20
from zope.interface import implements
from Products.Five import BrowserView
from zope.interface import implements
from kss.core import KSSView, kssaction
from Products.Archetypes.BaseObject import Wrapper
from atreal.richfile.metadata import RichFileMetadataMessageFactory as _
from atreal.richfile.metadata.interfaces import IMetadataExtractor
from atreal.richfile.qualifier.common import RFView
from atreal.richfile.qualifier.interfaces import IRFView

class RFMetadataView(RFView):
    __module__ = __name__
    plugin_interface = IMetadataExtractor
    kss_id = 'metadata'
    viewlet_name = 'atreal.richfile.metadata.viewlet'
    update_message = _('The metadatas have been updated.')
    active_message = _('Metadatas activated.')
    unactive_message = _('Metadatas un-activated.')