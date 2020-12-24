# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/profile/tal/api.py
# Compiled at: 2013-05-13 03:36:01
__docformat__ = 'restructuredtext'
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.sendit.profile.interfaces import IProfile
from ztfy.sendit.profile.tal.interfaces import IPrincipalProfileTalesAPI
from zope.interface import implements

class PrincipalProfileTalesAPI(object):
    implements(IPrincipalProfileTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def external(self):
        profile = IProfile(self.context)
        return profile.isExternal()

    def documents_count(self):
        profile = IProfile(self.context)
        return profile.getMaxDocuments(profile)