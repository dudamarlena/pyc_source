# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/sloop/tests.py
# Compiled at: 2019-06-28 06:41:03
# Size of source mod 2**32: 9086 bytes
import time
from botocore.exceptions import ClientError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mock import Mock
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from sloop.handlers import SNSHandler
from sloop.models import AbstractSNSDevice
from sloop.serializers import DeviceSerializer
from sloop.settings import SLOOP_SETTINGS
User = get_user_model()
TEST_SNS_ENDPOINT_ARN = 'test_sns_endpoint_arn'
TEST_IOS_PUSH_TOKEN = 'test_ios_push_token'
TEST_ANDROID_PUSH_TOKEN = 'test_android_push_token'

class Device(AbstractSNSDevice):
    pass


class SNSHandlerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('username', 'username@test.com', 'test123')
        self.ios_device = Device.objects.create(user=self.user, push_token=TEST_IOS_PUSH_TOKEN, platform=Device.PLATFORM_IOS)
        self.android_device = Device.objects.create(user=self.user, push_token=TEST_ANDROID_PUSH_TOKEN, platform=Device.PLATFORM_ANDROID)

    def test_get_ios_application_arn(self):
        sns_client = Mock()
        SNSHandler.client = sns_client
        handler = SNSHandler(self.ios_device)
        self.assertEqual(handler.application_arn, SLOOP_SETTINGS['SNS_IOS_APPLICATION_ARN'])

    def test_get_android_application_arn(self):
        sns_client = Mock()
        SNSHandler.client = sns_client
        handler = SNSHandler(self.android_device)
        self.assertEqual(handler.application_arn, SLOOP_SETTINGS['SNS_ANDROID_APPLICATION_ARN'])

    def test_create_platform_endpoint(self):
        sns_client = Mock()
        sns_client.create_platform_endpoint.return_value = {'EndpointArn': TEST_SNS_ENDPOINT_ARN}
        sns_client.publish.return_value = 'published'
        SNSHandler.client = sns_client
        handler = SNSHandler(self.ios_device)
        self.assertEqual(handler.get_or_create_platform_endpoint_arn(), TEST_SNS_ENDPOINT_ARN)
        sns_client.create_platform_endpoint.assert_called_once_with(PlatformApplicationArn=SLOOP_SETTINGS['SNS_IOS_APPLICATION_ARN'], Token=self.ios_device.push_token)
        self.assertEqual(self.ios_device.sns_platform_endpoint_arn, TEST_SNS_ENDPOINT_ARN)

    def test_get_platform_endpoint(self):
        sns_client = Mock()
        sns_client.create_platform_endpoint.return_value = {'EndpointArn': TEST_SNS_ENDPOINT_ARN}
        SNSHandler.client = sns_client
        self.ios_device.sns_platform_endpoint_arn = 'test_arn'
        self.ios_device.save()
        handler = SNSHandler(self.ios_device)
        self.assertEqual(handler.get_or_create_platform_endpoint_arn(), 'test_arn')
        self.assertFalse(sns_client.create_platform_endpoint.called)


class DeviceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('username', 'username@test.com', 'test123')
        self.ios_device = Device.objects.create(user=self.user, push_token=TEST_IOS_PUSH_TOKEN, platform=Device.PLATFORM_IOS)
        self.android_device = Device.objects.create(user=self.user, push_token=TEST_ANDROID_PUSH_TOKEN, platform=Device.PLATFORM_ANDROID)

    def test_send_ios_push_notification(self):
        sns_client = Mock()
        sns_client.publish.return_value = 'published'
        SNSHandler.client = sns_client
        self.ios_device.sns_platform_endpoint_arn = 'test_ios_arn'
        self.ios_device.save()
        self.ios_device.send_push_notification(message='test_message', url='test_url', badge_count=3, sound='test_sound', extra={'foo': 'bar'}, category='test_category', foo='bar')
        sns_client.publish.assert_called_once_with(TargetArn=self.ios_device.sns_platform_endpoint_arn, Message='{"APNS": "{\\"aps\\": {\\"sound\\": \\"test_sound\\", \\"category\\": \\"test_category\\", \\"foo\\": \\"bar\\", \\"alert\\": \\"test_message\\", \\"badge\\": 3, \\"custom\\": {\\"url\\": \\"test_url\\", \\"foo\\": \\"bar\\"}}}"}', MessageStructure='json')

    def test_send_android_push_notification(self):
        sns_client = Mock()
        sns_client.publish.return_value = 'published'
        SNSHandler.client = sns_client
        self.android_device.sns_platform_endpoint_arn = 'test_android_arn'
        self.android_device.save()
        self.android_device.send_push_notification(message='test_message', url='test_url', badge_count=3, sound='test_sound', extra={'foo': 'bar'}, category='test_category', foo='bar')
        sns_client.publish.assert_called_once_with(TargetArn=self.android_device.sns_platform_endpoint_arn, Message='{"GCM": "{\\"data\\": {\\"sound\\": \\"test_sound\\", \\"category\\": \\"test_category\\", \\"foo\\": \\"bar\\", \\"alert\\": \\"test_message\\", \\"badge\\": 3, \\"custom\\": {\\"url\\": \\"test_url\\", \\"foo\\": \\"bar\\"}}}"}', MessageStructure='json')

    def test_send_ios_silent_push_notification(self):
        sns_client = Mock()
        sns_client.publish.return_value = 'published'
        SNSHandler.client = sns_client
        self.ios_device.sns_platform_endpoint_arn = 'test_ios_arn'
        self.ios_device.save()
        self.ios_device.send_silent_push_notification(badge_count=0, extra={'foo': 'bar'}, content_available=True, foo='bar')
        sns_client.publish.assert_called_once_with(TargetArn=self.ios_device.sns_platform_endpoint_arn, Message='{"APNS": "{\\"aps\\": {\\"content-available\\": true, \\"sound\\": \\"\\", \\"foo\\": \\"bar\\", \\"badge\\": 0, \\"custom\\": {\\"foo\\": \\"bar\\"}}}"}', MessageStructure='json')

    def test_send_android_silent_push_notification(self):
        sns_client = Mock()
        sns_client.publish.return_value = 'published'
        SNSHandler.client = sns_client
        self.android_device.sns_platform_endpoint_arn = 'test_android_arn'
        self.android_device.save()
        self.android_device.send_silent_push_notification(badge_count=0, extra={'foo': 'bar'}, content_available=True, foo='bar')
        sns_client.publish.assert_called_once_with(TargetArn=self.android_device.sns_platform_endpoint_arn, Message='{"GCM": "{\\"data\\": {\\"content-available\\": true, \\"sound\\": \\"\\", \\"foo\\": \\"bar\\", \\"badge\\": 0, \\"custom\\": {\\"foo\\": \\"bar\\"}}}"}', MessageStructure='json')

    def test_invalidate_device_if_push_message_fails(self):
        sns_client = Mock()
        SNSHandler.client = sns_client
        sns_client.publish.side_effect = ClientError(error_response={'Error': {'Code': 'EndpointDisabled'}}, operation_name='test')
        self.ios_device.sns_platform_endpoint_arn = 'test_ios_arn'
        self.ios_device.save()
        self.ios_device.send_push_notification(message='test')
        self.assertFalse(Device.objects.filter(id=self.ios_device.id).exists())


class DeviceAPITests(TestCase):

    def setUp(self):
        self.client, self.user = self.create_test_user_client()
        self.ios_device = Device.objects.create(user=self.user, push_token=TEST_IOS_PUSH_TOKEN, platform=Device.PLATFORM_IOS)
        self.android_device = Device.objects.create(user=self.user, push_token=TEST_ANDROID_PUSH_TOKEN, platform=Device.PLATFORM_ANDROID)
        self.create_delete_url = reverse('sloop:create-delete-device')

    def create_test_user_client(self, **user_data):
        millis = int(round(time.time() * 1000))
        user = User.objects.create_user('username' + str(millis), 'username@test.com', 'test123')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.default_format = 'json'
        client.force_authenticate(user=user, token=token.key)
        return (
         client, user)

    def test_api_create_device(self):
        data = {'push_token': 'test_ios_push_token2', 
         'platform': Device.PLATFORM_IOS}
        response = self.client.post(self.create_delete_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device = self.user.devices.get(**data)
        self.assertEqual(response.data, DeviceSerializer(device).data)

    def test_api_delete_device(self):
        non_device_owner_client, non_device_owner = self.create_test_user_client()
        data = {'push_token': self.ios_device.push_token}
        response = non_device_owner_client.delete(self.create_delete_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(self.create_delete_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Device.objects.filter(id=self.ios_device.id).exists())