# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rvaziri/django_mobile_push/sns_notification/client.py
# Compiled at: 2018-04-29 12:36:11
# Size of source mod 2**32: 4738 bytes
"""
AWS SNS Client
"""
from django.conf import settings
import boto3, json

class Client(object):
    __doc__ = ' Class representing an AWS SNS client that supports mobile push notifications.\n\n    Design Pattern:\n\n    It follows Borg design pattern.\n    https://github.com/faif/python-patterns/blob/master/creational/borg.py\n    '
    _Client__shared_state = {}

    def __init__(self):
        """
        Constructor method.
        """
        self.__dict__ = self._Client__shared_state
        self.connection = self.connect()
        self.ios_arn = getattr(settings, 'IOS_PLATFORM_APPLICATION_ARN')
        self.android_arn = getattr(settings, 'ANDROID_PLATFORM_APPLICATION_ARN')

    @staticmethod
    def connect():
        """
        Method that creates a connection to AWS SNS
        :return: AWS boto3 connection object
        """
        session = boto3.Session()
        if getattr(settings, 'AWS_SNS_REGION_NAME', None) and getattr(settings, 'AWS_ACCESS_KEY_ID', None):
            return session.client('sns', region_name=getattr(settings, 'AWS_SNS_REGION_NAME'), aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID'), aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY'))
        else:
            return session.client('sns', region_name=getattr(settings, 'AWS_SNS_REGION_NAME'))

    def retrieve_platform_endpoint_attributs(self, arn):
        """
        Method that retrieves a platform endpoint for an IOS device.
        :param arn: ARN(Amazon resource name)
        :return: attributes of the endpoint
        """
        response = self.connection.get_endpoint_attributes(EndpointArn=arn)
        return response['Attributes']

    def delete_platform_endpoint(self, arn):
        self.connection.delete_endpoint(EndpointArn=arn)

    def create_ios_platform_endpoint(self, token):
        """
        Method that creates a platform endpoint for an IOS device.
        :param token: device token
        :return: response from SNS
        """
        response = self.connection.create_platform_endpoint(PlatformApplicationArn=self.ios_arn, Token=token)
        return response

    def create_android_platform_endpoint(self, token):
        """
        Method that creates a platform endpoint for an Android device.
        :param token: device token
        :return: response from SNS
        """
        response = self.connection.create_platform_endpoint(PlatformApplicationArn=self.android_arn, Token=token)
        return response

    def publish_to_android(self, arn, title, text, notification_type, data, id):
        """
        Method that sends a mobile push notification to an android device.
        :param arn: ARN(Amazon resource name)
        :param title: message title
        :param text: message body
        :param notification_type: type of notification
        :param data: data to be used for deep-linking
        :param id: notification ID
        :return: response from SNS
        """
        message = {'GCM': '{ "notification": { "title": "%s", "text": "%s", "body": "%s", "sound": "default" }, "data": { "id": "%s", "type": "%s", "serializer": "%s" } }' % (title, text, text, id, notification_type, json.dumps(data).replace('"', "'"))}
        response = self.connection.publish(TargetArn=arn, Message=json.dumps(message), MessageStructure='json')
        return (
         message, response)

    def publish_to_ios(self, arn, title, text, notification_type, data, id):
        """
        Method that sends a mobile push notification to an IOS device.
        :param arn: ARN(Amazon resource name)
        :param title: message title
        :param text: message body
        :param notification_type: type of notification
        :param data: data to be used for deep-linking
        :param id: notification ID
        :return: response from SNS
        """
        message = {'APNS': '{ "aps": { "alert": { "title": "%s", "body": "%s" }, "sound": "default" }, "id": "%s",  "type": "%s", "serializer": "%s" }' % (title, text, id, notification_type, json.dumps(data).replace('"', "'"))}
        response = self.connection.publish(TargetArn=arn, Message=json.dumps(message), MessageStructure='json')
        return (
         message, response)