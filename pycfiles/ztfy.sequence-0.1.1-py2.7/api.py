# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sequence/tal/api.py
# Compiled at: 2012-09-19 17:23:16
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.sequence.tal.interfaces import ISequentialIdTalesAPI
from zope.interface import implements
from ztfy.sequence.interfaces import ISequentialIdInfo

class SequentialIdTalesAPI(object):
    """Sequential ID TALES API"""
    implements(ISequentialIdTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def oid(self):
        return ISequentialIdInfo(self.context).oid