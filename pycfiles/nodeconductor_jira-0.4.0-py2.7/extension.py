# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/extension.py
# Compiled at: 2016-09-16 10:02:59
from __future__ import unicode_literals
from nodeconductor.core import NodeConductorExtension

class JiraExtension(NodeConductorExtension):

    class Settings:
        JIRA_COMMENT_TEMPLATE = b'{body}\n\n_(added by {user.full_name} [{user.username}] via G-Cloud Portal)_'
        JIRA_PRIORITY_MAPPING = {b'Minor': b'3 - Minor', 
           b'Major': b'2 - Major', 
           b'Critical': b'1 - Critical'}

    @staticmethod
    def django_app():
        return b'nodeconductor_jira'

    @staticmethod
    def django_urls():
        from .urls import urlpatterns
        return urlpatterns

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in