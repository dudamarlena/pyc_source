# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/extension.py
# Compiled at: 2016-09-25 10:50:25
from nodeconductor.core import NodeConductorExtension

class OrganizationExtension(NodeConductorExtension):

    @staticmethod
    def django_app():
        return 'nodeconductor_organization'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in