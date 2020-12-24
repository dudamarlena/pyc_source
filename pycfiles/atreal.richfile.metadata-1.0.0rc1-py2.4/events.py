# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/metadata/events.py
# Compiled at: 2009-09-04 10:38:20
from zope.interface.interfaces import IInterface
from zope.component import queryUtility
from atreal.richfile.metadata.interfaces import IMetadataExtractor

def is_richfilemetadata_installed():
    """
    """
    return queryUtility(IInterface, name='atreal.richfile.metadata.IRichFileMetadataSite', default=False)


def extractMetadata(obj, event):
    """
    """
    if not is_richfilemetadata_installed():
        return
    print 'Extracting metadatas for %s' % ('/').join(obj.getPhysicalPath())
    IMetadataExtractor(obj).process()


def cleanMetadata(obj, event):
    """
    """
    if not is_richfilemetadata_installed():
        return
    print 'Clean metadata %s' % ('/').join(obj.getPhysicalPath())
    IMetadataExtractor(obj).cleanUp()