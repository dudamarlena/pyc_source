# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/tal/api.py
# Compiled at: 2012-06-20 11:31:01
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.file.tal.interfaces import IImageDisplayTalesAPI
from ztfy.file.interfaces import IImageDisplay
from zope.interface import implements

class ImageDisplayTalesAPI(object):
    implements(IImageDisplayTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def adapter(self):
        return IImageDisplay(self.context)