# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/tests_permission_api.py
# Compiled at: 2017-09-14 10:59:08
# Size of source mod 2**32: 8053 bytes
from django.urls import reverse
from rest_framework import status
from billjobs.tests.generics import GenericAPITest
import collections

class AnonymousPermissionAPITest(GenericAPITest):
    __doc__ = '\n    Test /permissions endpoint status code and response data for anonymous user\n    '

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-api')
        self.expected_status = {'GET':401, 
         'POST':401, 
         'PUT':401, 
         'DELETE':401, 
         'HEAD':401, 
         'OPTIONS':401, 
         'PATCH':401}
        self.expected_content = {'GET':self.error_message['401'], 
         'POST':self.error_message['401'], 
         'PUT':self.error_message['401'], 
         'DELETE':self.error_message['401'], 
         'HEAD':self.error_message['401'], 
         'OPTIONS':self.error_message['401'], 
         'PATCH':self.error_message['401']}

    def tearDown(self):
        super().tearDown()

    def test_permission_api_status_code(self):
        self.status_code_is()

    def test_permission_api_content(self):
        self.content_is()


class AnonymousPermissionDetailAPITest(GenericAPITest):
    __doc__ = '\n    Test /permissions/pk endpoint status code and response data for anonymous\n    user\n    '

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-detail-api', args=(1, ))
        self.expected_status = {'GET':401, 
         'POST':401, 
         'PUT':401, 
         'DELETE':401, 
         'HEAD':401, 
         'OPTIONS':401, 
         'PATCH':401}
        self.expected_content = {'GET':self.error_message['401'], 
         'POST':self.error_message['401'], 
         'PUT':self.error_message['401'], 
         'DELETE':self.error_message['401'], 
         'HEAD':self.error_message['401'], 
         'OPTIONS':self.error_message['401'], 
         'PATCH':self.error_message['401']}

    def tearDown(self):
        super().tearDown()

    def test_permission_detail_api_status_code(self):
        self.status_code_is()

    def test_permission_detail_api_content(self):
        self.content_is()


class UserPermissionAPITest(GenericAPITest):
    __doc__ = '\n    Test /permissions endpoint status code and response data for authenticated\n    user\n    '

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-api')
        self.force_authenticate(user=(self.bill))
        self.expected_status = {'GET':403, 
         'POST':403, 
         'PUT':403, 
         'DELETE':403, 
         'HEAD':403, 
         'OPTIONS':403, 
         'PATCH':403}
        self.expected_content = {'GET':self.error_message['403'], 
         'POST':self.error_message['403'], 
         'PUT':self.error_message['403'], 
         'DELETE':self.error_message['403'], 
         'HEAD':self.error_message['403'], 
         'OPTIONS':self.error_message['403'], 
         'PATCH':self.error_message['403']}

    def tearDown(self):
        super().tearDown()

    def test_permission_api_status_code(self):
        self.status_code_is()

    def test_permission_api_content(self):
        self.content_is()


class UserPermissionDetailAPITest(GenericAPITest):
    __doc__ = '\n    Test /permissions/pk endpoint status code and response data for\n    authenticated user\n    '

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-detail-api', args=(1, ))
        self.force_authenticate(user=(self.bill))
        self.expected_status = {'GET':403, 
         'POST':403, 
         'PUT':403, 
         'DELETE':403, 
         'HEAD':403, 
         'OPTIONS':403, 
         'PATCH':403}
        self.expected_content = {'GET':self.error_message['403'], 
         'POST':self.error_message['403'], 
         'PUT':self.error_message['403'], 
         'DELETE':self.error_message['403'], 
         'HEAD':self.error_message['403'], 
         'OPTIONS':self.error_message['403'], 
         'PATCH':self.error_message['403']}

    def tearDown(self):
        super().tearDown()

    def test_permission_detail_api_status_code(self):
        self.status_code_is()

    def test_permission_detail_api_content(self):
        self.content_is()


class AdminPermissionAPITest(GenericAPITest):
    __doc__ = '\n    Test /permissions endpoint status code and response data for authenticated\n    admin\n    '

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-api')
        self.force_authenticate(user=(self.admin))
        self.expected_status = {'GET':200, 
         'PUT':405, 
         'DELETE':405, 
         'HEAD':200, 
         'OPTIONS':200, 
         'PATCH':405}
        self.expected_content = {'GET':[
          collections.OrderedDict({'url':'http://testserver/billjobs/api/1.0/permissions/1/', 
           'name':'Can add log entry', 
           'codename':'add_logentry'}),
          collections.OrderedDict({'url':'http://testserver/billjobs/api/1.0/permissions/18/', 
           'name':'Can delete session', 
           'codename':'delete_session'})], 
         'PUT':self.error_message['405_PUT'], 
         'DELETE':self.error_message['405_DELETE'], 
         'PATCH':self.error_message['405_PATCH']}

    def tearDown(self):
        super().tearDown()

    def test_permission_api_status_code(self):
        self.status_code_is()

    def test_permission_api_content(self):
        self.content_is()


class AdminPermissionDetailAPITest(GenericAPITest):
    __doc__ = '\n    Test /permissions/pk endpoint status code and response data for\n    authenticated admin\n    '

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-detail-api', args=(1, ))
        self.force_authenticate(user=(self.admin))
        self.expected_status = {'GET':200, 
         'POST':405}
        self.expected_content = {'GET':{'url':'http://testserver/billjobs/api/1.0/permissions/1/', 
          'name':'Can add log entry', 
          'codename':'add_logentry'}, 
         'POST':self.error_message['405_POST']}

    def tearDown(self):
        super().tearDown()

    def test_permission_api_status_code(self):
        self.status_code_is()

    def test_permission_api_content(self):
        self.content_is()