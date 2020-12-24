# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/testing/hosting_services.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django import forms
from reviewboard.hostingsvcs.errors import AuthorizationError, TwoFactorAuthCodeRequiredError
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService

class TestServiceForm(HostingServiceForm):
    test_repo_name = forms.CharField(label=b'Repository name', max_length=64, required=True)


class TestService(HostingService):
    hosting_service_id = b'test'
    name = b'Test Service'
    form = TestServiceForm
    needs_authorization = True
    supports_repositories = True
    supports_bug_trackers = True
    supports_two_factor_auth = True
    has_repository_hook_instructions = True
    supported_scmtools = [b'Git', b'Test', b'perforce']
    visible_scmtools = [b'git', b'test']
    bug_tracker_field = b'http://example.com/%(hosting_account_username)s/%(test_repo_name)s/issue/%%s'
    repository_fields = {b'Git': {b'path': b'http://example.com/%(test_repo_name)s/'}, 
       b'Perforce': {b'path': b'%(test_repo_name).p4.example.com:1666'}, 
       b'Test': {b'path': b'http://example.com/%(test_repo_name)s/'}}

    def authorize(self, username, password, hosting_url, local_site_name=None, two_factor_auth_code=None, *args, **kwargs):
        if username == b'baduser':
            raise AuthorizationError(b'The username is very very bad.')
        elif username == b'2fa-user' and two_factor_auth_code != b'123456':
            raise TwoFactorAuthCodeRequiredError(b'Enter your 2FA code.')
        self.account.data.update({b'username': username, 
           b'password': password, 
           b'hosting_url': hosting_url, 
           b'local_site_name': local_site_name})

    def is_authorized(self):
        return self.account.username != b'baduser' and b'password' in self.account.data

    def check_repository(self, *args, **kwargs):
        pass


class SelfHostedTestService(TestService):
    hosting_service_id = b'self_hosted_test'
    name = b'Self-Hosted Test'
    self_hosted = True
    bug_tracker_field = b'%(hosting_url)s/%(test_repo_name)s/issue/%%s'
    repository_fields = {b'Git': {b'path': b'%(hosting_url)s/%(test_repo_name)s/', 
                b'mirror_path': b'git@%(hosting_domain)s:%(test_repo_name)s/'}, 
       b'Test': {b'path': b'%(hosting_url)s/%(test_repo_name)s/', 
                 b'mirror_path': b'git@%(hosting_domain)s:%(test_repo_name)s/'}}