# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/tal/session.py
# Compiled at: 2012-06-20 10:07:04
__docformat__ = 'restructuredtext'
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.utils.tal.interfaces import ISessionDataTalesAPI
from zope.interface import implements
from ztfy.utils.session import getData

class SessionDataTalesAdapter(object):
    implements(ISessionDataTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def __getattr__(self, attr):
        app, key = attr.split(',')
        return getData(self.context, app, key)