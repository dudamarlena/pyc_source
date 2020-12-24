# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/user_authenticator_enroll.py
# Compiled at: 2019-08-23 05:13:18
from __future__ import absolute_import
from rest_framework import serializers, status
from rest_framework.fields import SkipField
from rest_framework.response import Response
import logging, petname
from sentry.api.bases.user import UserEndpoint
from sentry.api.decorators import sudo_required
from sentry.api.serializers import serialize
from sentry.models import Authenticator, OrganizationMember
from sentry.security import capture_security_activity
from sentry.api.invite_helper import ApiInviteHelper
logger = logging.getLogger(__name__)
ALREADY_ENROLLED_ERR = {'details': 'Already enrolled'}
INVALID_OTP_ERR = ({'details': 'Invalid OTP'},)
SEND_SMS_ERR = {'details': 'Error sending SMS'}

class BaseRestSerializer(serializers.Serializer):
    memberId = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    token = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class TotpRestSerializer(BaseRestSerializer):
    otp = serializers.CharField(label='Authenticator code', help_text='Code from authenticator', required=True, max_length=20)


class SmsRestSerializer(BaseRestSerializer):
    phone = serializers.CharField(label='Phone number', help_text='Phone number to send SMS code', required=True, max_length=20)
    otp = serializers.CharField(label='Authenticator code', help_text='Code from authenticator', required=False, allow_null=True, allow_blank=True, max_length=20)


class U2fRestSerializer(BaseRestSerializer):
    deviceName = serializers.CharField(label='Device name', required=False, allow_null=True, allow_blank=True, max_length=60, default=lambda : petname.Generate(2, ' ', letters=10).title())
    challenge = serializers.CharField(required=True)
    response = serializers.CharField(required=True)


hidden_fields = [
 'memberId', 'token']
serializer_map = {'totp': TotpRestSerializer, 'sms': SmsRestSerializer, 'u2f': U2fRestSerializer}

def get_serializer_field_metadata(serializer, fields=None):
    """Returns field metadata for serializer"""
    meta = []
    for field_name, field in serializer.fields.items():
        if (fields is None or field_name in fields) and field_name not in hidden_fields:
            try:
                default = field.get_default()
            except SkipField:
                default = None

            serialized_field = {'name': field_name, 'defaultValue': default, 
               'read_only': field.read_only, 
               'required': field.required, 
               'type': 'string'}
            if hasattr(field, 'max_length') and field.max_length:
                serialized_field['max_length'] = field.max_length
            if field.label:
                serialized_field['label'] = field.label
            meta.append(serialized_field)

    return meta


class UserAuthenticatorEnrollEndpoint(UserEndpoint):

    @sudo_required
    def get(self, request, user, interface_id):
        """
        Get Authenticator Interface
        ```````````````````````````

        Retrieves authenticator interface details for user depending on user enrollment status

        :pparam string user_id: user id or "me" for current user
        :pparam string interface_id: interface id

        :auth: required
        """
        interface = Authenticator.objects.get_interface(user, interface_id)
        if interface.is_enrolled and not interface.allow_multi_enrollment:
            return Response(ALREADY_ENROLLED_ERR, status=status.HTTP_400_BAD_REQUEST)
        response = serialize(interface)
        response['form'] = get_serializer_field_metadata(serializer_map[interface_id]())
        try:
            response['secret'] = interface.secret
        except AttributeError:
            pass

        if interface_id == 'totp':
            response['qrcode'] = interface.get_provision_qrcode(user.email)
        if interface_id == 'u2f':
            response['challenge'] = interface.start_enrollment()
            app_id = response['challenge']['appId']
            for register_request in response['challenge']['registerRequests']:
                register_request['appId'] = app_id

        return Response(response)

    @sudo_required
    def post(self, request, user, interface_id):
        """
        Enroll in authenticator interface
        `````````````````````````````````

        :pparam string user_id: user id or "me" for current user
        :pparam string interface_id: interface id

        :auth: required
        """
        serializer_cls = serializer_map.get(interface_id, None)
        if serializer_cls is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = serializer_cls(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            interface = Authenticator.objects.get_interface(request.user, interface_id)
            if interface.is_enrolled and not interface.allow_multi_enrollment:
                return Response(ALREADY_ENROLLED_ERR, status=status.HTTP_400_BAD_REQUEST)
            try:
                interface.secret = request.data['secret']
            except KeyError:
                pass

            context = {}
            if 'phone' in request.data:
                interface.phone_number = serializer.data['phone']
                if 'otp' not in request.data:
                    if interface.send_text(for_enrollment=True, request=request._request):
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response(SEND_SMS_ERR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if 'otp' in request.data and not interface.validate_otp(serializer.data['otp']):
                return Response(INVALID_OTP_ERR, status=status.HTTP_400_BAD_REQUEST)
            if interface_id == 'u2f':
                interface.try_enroll(serializer.data['challenge'], serializer.data['response'], serializer.data['deviceName'])
                context.update({'device_name': serializer.data['deviceName']})
            try:
                interface.enroll(request.user)
            except Authenticator.AlreadyEnrolled:
                return Response(ALREADY_ENROLLED_ERR, status=status.HTTP_400_BAD_REQUEST)

            context.update({'authenticator': interface.authenticator})
            capture_security_activity(account=request.user, type='mfa-added', actor=request.user, ip_address=request.META['REMOTE_ADDR'], context=context, send_email=True)
            request.user.clear_lost_passwords()
            request.user.refresh_session_nonce(self.request)
            request.user.save()
            Authenticator.objects.auto_add_recovery_codes(request.user)
            member_id = serializer.data.get('memberId')
            token = serializer.data.get('token')
            if member_id and token:
                try:
                    helper = ApiInviteHelper(instance=self, request=request, member_id=member_id, token=token, logger=logger)
                except OrganizationMember.DoesNotExist:
                    logger.error('Failed to accept pending org invite', exc_info=True)
                else:
                    if helper.valid_request:
                        helper.accept_invite()
                        response = Response(status=status.HTTP_204_NO_CONTENT)
                        helper.remove_invite_cookie(response)
                        return response

            return Response(status=status.HTTP_204_NO_CONTENT)
            return