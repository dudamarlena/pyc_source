# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/views/healthcheck.py
# Compiled at: 2018-04-27 06:39:21
from ocs.api import healthchecks
from . import MetadataAPIBaseView

class HealthCheck(MetadataAPIBaseView):

    def index(self):
        return healthchecks.format_response({'Compute privileged API token permissions': healthchecks.token_has_perm(self.privileged_account_api, self.privileged_compute_api.auth_token, service='compute', name='servers:read', resource='*'), 
           'Account privileged API token permissions': healthchecks.token_has_perm(self.privileged_account_api, self.privileged_account_api.auth_token, service='account', name='organization:read', resource='*')})