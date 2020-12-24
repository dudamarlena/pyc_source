# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/events/download.py
# Compiled at: 2017-11-01 05:34:47
from zope.interface import implementer
from zope.component.interfaces import IObjectEvent

class IDownloadReady(IObjectEvent):
    """ Land download package is ready.
    """
    pass


@implementer(IDownloadReady)
class DownloadReady(object):

    def __init__(self, context, **kwargs):
        self.object = context