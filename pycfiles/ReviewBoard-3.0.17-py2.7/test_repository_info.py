# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_repository_info.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import repository_info_item_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_repository_info_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceTests(BaseWebAPITestCase):
    """Testing the RepositoryInfoResource APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'repositories/<id>/info/'
    resource = resources.repository_info

    def setup_http_not_allowed_list_test(self, user):
        repository = self.create_repository(tool_name=b'Test')
        return get_repository_info_url(repository)

    def setup_http_not_allowed_item_test(self, user):
        repository = self.create_repository(tool_name=b'Test')
        return get_repository_info_url(repository)

    def compare_item(self, item_rsp, info):
        self.assertEqual(item_rsp, info)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        repository = self.create_repository(tool_name=b'Test', with_local_site=with_local_site)
        return (
         get_repository_info_url(repository, local_site_name),
         repository_info_item_mimetype,
         repository.get_scmtool().get_repository_info())