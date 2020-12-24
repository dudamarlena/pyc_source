# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/hostingsvcs/githubenterprise.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.github import GitHub
from rbpowerpack.utils.extension import get_powerpack_extension

class GitHubEnterprisePublicForm(HostingServiceForm):
    github_enterprise_public_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the repository. This is the &lt;repo_name&gt; in http://&lt;hostname&gt;/&lt;username&gt;/&lt;repo_name&gt;/'))


class GitHubEnterprisePrivateForm(HostingServiceForm):
    github_enterprise_private_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the repository. This is the &lt;repo_name&gt; in http://&lt;hostname&gt;/&lt;username&gt;/&lt;repo_name&gt;/'))


class GitHubEnterprisePublicOrgForm(HostingServiceForm):
    github_enterprise_public_org_name = forms.CharField(label=_(b'Organization name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the organization. This is the &lt;org_name&gt; in http://&lt;hostname&gt;/&lt;org_name&gt;/&lt;repo_name&gt;/'))
    github_enterprise_public_org_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the repository. This is the &lt;repo_name&gt; in http://&lt;hostname&gt;/&lt;org_name&gt;/&lt;repo_name&gt;/'))


class GitHubEnterprisePrivateOrgForm(HostingServiceForm):
    github_enterprise_private_org_name = forms.CharField(label=_(b'Organization name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the organization. This is the &lt;org_name&gt; in http://&lt;hostname&gt;/&lt;org_name&gt;/&lt;repo_name&gt;/'))
    github_enterprise_private_org_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the repository. This is the &lt;repo_name&gt; in http://&lt;hostname&gt;/&lt;org_name&gt;/&lt;repo_name&gt;/'))


class GitHubEnterprise(GitHub):
    name = _(b'GitHub Enterprise')
    plans = [
     (
      b'public',
      {b'name': _(b'Public'), 
         b'form': GitHubEnterprisePublicForm, 
         b'repository_fields': {b'Git': {b'path': b'git@%(hosting_domain)s:%(hosting_account_username)s/%(github_enterprise_public_repo_name)s.git', 
                                         b'mirror_path': b''}}, 
         b'bug_tracker_field': b'%(hosting_url)s/%(hosting_account_username)s/%(github_enterprise_public_repo_name)s/issues#issue/%%s'}),
     (
      b'public-org',
      {b'name': _(b'Public Organization'), 
         b'form': GitHubEnterprisePublicOrgForm, 
         b'repository_fields': {b'Git': {b'path': b'git@%(hosting_domain)s:%(github_enterprise_public_org_name)s/%(github_enterprise_public_org_repo_name)s.git', 
                                         b'mirror_path': b''}}, 
         b'bug_tracker_field': b'%(hosting_url)s/%(github_enterprise_public_org_name)s/%(github_enterprise_public_org_repo_name)s/issues#issue/%%s'}),
     (
      b'private',
      {b'name': _(b'Private'), 
         b'form': GitHubEnterprisePrivateForm, 
         b'repository_fields': {b'Git': {b'path': b'git@%(hosting_domain)s:%(hosting_account_username)s/%(github_enterprise_private_repo_name)s.git', 
                                         b'mirror_path': b''}}, 
         b'bug_tracker_field': b'%(hosting_url)s/%(hosting_account_username)s/%(github_enterprise_private_repo_name)s/issues#issue/%%s'}),
     (
      b'private-org',
      {b'name': _(b'Private Organization'), 
         b'form': GitHubEnterprisePrivateOrgForm, 
         b'repository_fields': {b'Git': {b'path': b'git@%(hosting_domain)s:%(github_enterprise_private_org_name)s/%(github_enterprise_private_org_repo_name)s.git', 
                                         b'mirror_path': b''}}, 
         b'bug_tracker_field': b'%(hosting_url)s/%(github_enterprise_private_org_name)s/%(github_enterprise_private_org_repo_name)s/issues#issue/%%s'})]
    self_hosted = True
    plan_field_prefix = b'github_enterprise'

    def get_api_url(self, hosting_url):
        if hosting_url.endswith(b'/'):
            hosting_url = hosting_url[:-1]
        return b'%s/api/v3/' % hosting_url

    def can_user_post(self, user, repository):
        """Returns whether a user can post against the given repository.

        This will check the extension's policy to ensure that the user
        is permitted to post.
        """
        extension = get_powerpack_extension()
        return extension is not None and extension.policy.is_github_enterprise_enabled(user, repository)