# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/views/healthcheck.py
# Compiled at: 2018-04-27 06:39:21
from ocs.api import healthchecks
from . import MetadataAPIBaseView

class HealthCheck(MetadataAPIBaseView):

    def index(self):
        return healthchecks.format_response({'Compute privileged API token permissions': healthchecks.token_has_perm(self.privileged_account_api, self.privileged_compute_api.auth_token, service='compute', name='servers:read', resource='*'), 
           'Account privileged API token permissions': healthchecks.token_has_perm(self.privileged_account_api, self.privileged_account_api.auth_token, service='account', name='organization:read', resource='*')})