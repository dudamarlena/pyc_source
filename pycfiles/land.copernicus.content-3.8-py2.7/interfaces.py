# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/content/interfaces.py
# Compiled at: 2018-01-23 05:41:50
""" Content interfaces
"""
from zope import schema
from zope.interface import Interface

class ILandContent(Interface):
    """ Abstract
    """
    pass


class ILandSection(ILandContent):
    """ Folderish sections
    """
    pass


class ILandItem(ILandContent):
    """ Bottom items
    """
    pass


class ILandProduct(Interface):
    """ LandProducts are similar to a Dataset from eea.dataservice
    """
    pass


class ILandFile(Interface):
    """ LandFile are links to files on FTP
    """
    pass


class IPLandFile(Interface):
    """ Lightweight implementation of LandFile,
        inheriting only from persistent.Persistent,
        the bare-minimum requirement for ZODB storage.
    """
    title = schema.TextLine(title='Title', required=True)
    shortname = schema.TextLine(title='Short name', required=True)
    description = schema.Text(title='Description', required=False)
    remoteUrl = schema.URI(title='URL', required=True)
    fileSize = schema.TextLine(title='Download file size', description='Leave this field empty. It is automatically extracted.', default='N/A', required=False)
    fileCategories = schema.Tuple(title='Categorization of this file', description='Enter, for each category, its value', required=False)