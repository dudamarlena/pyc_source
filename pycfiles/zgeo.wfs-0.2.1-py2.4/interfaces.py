# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zgeo/wfs/interfaces.py
# Compiled at: 2008-10-27 05:35:22
from zope.interface import Interface, Attribute
from zope.schema import Field, Text, URI, Dict
from zgeo.geographer.interfaces import IGeoCollection, IWriteGeoreferenced

class IWebFeatureServiceable(Interface):
    """Marks classes which can expose a WFS service
        """
    __module__ = __name__


class IWebFeatureService(IGeoCollection):
    """An OGC Web Feature Service
        """
    __module__ = __name__
    name = Field(title='Name', description='WFS service name', required=False)
    title = Field(title='Title', description='WFS service title', required=False)
    abstract = Text(title='Abstract', description='WFS service abstract', required=False)
    onlineresource = URI(title='OnlineResource', description='Uniform Resource Identifier', required=False)
    featuretypes = Dict(title='Feature types', description='Dictionary which provides the feature types names and their elements list')
    srs = Field(title='SRS', description='Spatial reference system', required=False)


class IWFSGeoItem(IWriteGeoreferenced):
    """A georeferenced object exposable through WFS
        """
    __module__ = __name__


class IWFSGeoreferencedEvent(Interface):
    """An event fired when georeferenced.
    """
    __module__ = __name__
    context = Attribute('The content object that was saved.')