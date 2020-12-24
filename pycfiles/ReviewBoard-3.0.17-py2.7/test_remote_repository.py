# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_remote_repository.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import json
from django.utils import six
from kgb import SpyAgency
from reviewboard.hostingsvcs.github import GitHub
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.repository import RemoteRepository
from reviewboard.hostingsvcs.utils.paginator import APIPaginator
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import remote_repository_item_mimetype, remote_repository_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_remote_repository_item_url, get_remote_repository_list_url

def _compare_item(self, item_rsp, remote_repository):
    self.assertEqual(item_rsp[b'id'], remote_repository.id)
    self.assertEqual(item_rsp[b'name'], remote_repository.name)
    self.assertEqual(item_rsp[b'owner'], remote_repository.owner)
    self.assertEqual(item_rsp[b'scm_type'], remote_repository.scm_type)
    self.assertEqual(item_rsp[b'path'], remote_repository.path)
    self.assertEqual(item_rsp[b'mirror_path'], remote_repository.mirror_path)


class RemoteRepositoryTestPaginator(APIPaginator):

    def __init__(self, results):
        self.results = results
        super(RemoteRepositoryTestPaginator, self).__init__(client=None, url=b'')
        return

    def fetch_url(self, url):
        return {b'data': self.results}


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(SpyAgency, BaseWebAPITestCase):
    """Testing the RemoteRepositoryResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'hosting-service-accounts/<id>/remote-repositories/'
    resource = resources.remote_repository
    basic_get_use_admin = True
    compare_item = _compare_item

    def setup_http_not_allowed_list_test(self, user):
        account = HostingServiceAccount.objects.create(service_name=b'github', username=b'bob')
        return get_remote_repository_list_url(account)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        account = HostingServiceAccount.objects.create(service_name=b'github', username=b'bob', local_site=self.get_local_site_or_none(name=local_site_name), data=json.dumps({b'authorization': {b'token': b'123'}}))
        service = account.service
        remote_repositories = [
         RemoteRepository(service, repository_id=b'123', name=b'repo1', owner=b'bob', scm_type=b'Git', path=b'ssh://example.com/repo1', mirror_path=b'https://example.com/repo1'),
         RemoteRepository(service, repository_id=b'456', name=b'repo2', owner=b'bob', scm_type=b'Git', path=b'ssh://example.com/repo2', mirror_path=b'https://example.com/repo2')]
        paginator = RemoteRepositoryTestPaginator(remote_repositories)
        self.spy_on(GitHub.get_remote_repositories, call_fake=lambda *args, **kwargs: paginator)
        return (
         get_remote_repository_list_url(account, local_site_name),
         remote_repository_list_mimetype,
         remote_repositories)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(SpyAgency, BaseWebAPITestCase):
    """Testing the RemoteRepositoryResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'hosting-service-accounts/<id>/remote-repositories/<id>/'
    resource = resources.remote_repository
    basic_get_use_admin = True
    compare_item = _compare_item

    def setup_http_not_allowed_item_test(self, user):
        account = HostingServiceAccount.objects.create(service_name=b'github', username=b'bob')
        remote_repository = RemoteRepository(account.service, repository_id=b'123', name=b'repo1', owner=b'bob', scm_type=b'Git', path=b'ssh://example.com/repo1')
        return get_remote_repository_item_url(remote_repository)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        account = HostingServiceAccount.objects.create(service_name=b'github', username=b'bob', local_site=self.get_local_site_or_none(name=local_site_name), data=json.dumps({b'authorization': {b'token': b'123'}}))
        remote_repository = RemoteRepository(account.service, repository_id=b'123', name=b'repo1', owner=b'bob', scm_type=b'Git', path=b'ssh://example.com/repo1', mirror_path=b'https://example.com/repo1')
        self.spy_on(GitHub.get_remote_repository, call_fake=lambda *args, **kwargs: remote_repository)
        return (
         get_remote_repository_item_url(remote_repository, local_site_name),
         remote_repository_item_mimetype,
         remote_repository)