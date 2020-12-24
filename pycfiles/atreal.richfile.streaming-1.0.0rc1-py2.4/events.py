# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/streaming/events.py
# Compiled at: 2009-09-14 10:15:09
from zope.interface.interfaces import IInterface
from zope.component import queryUtility
from atreal.richfile.streaming.interfaces import IStreamable

def is_richfilestreaming_installed():
    """
    """
    return queryUtility(IInterface, name='atreal.richfile.streaming.IRichFileStreamingSite', default=False)


def buildAndStoreStreaming(obj, event):
    """
    """
    if not is_richfilestreaming_installed():
        return
    print 'atreal.richfile.streaming: build and store streaming for %s' % ('/').join(obj.getPhysicalPath())
    IStreamable(obj).process()


def cleanStreamingData(obj, event):
    """
    """
    if not is_richfilestreaming_installed():
        return
    print 'atreal.richfile.streaming: clean data for %s' % ('/').join(obj.getPhysicalPath())
    IStreamable(obj).cleanUp()