# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/views/password_recovery.py
# Compiled at: 2017-05-23 13:28:27
# Size of source mod 2**32: 3402 bytes
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from dateutil.relativedelta import relativedelta
from ovp_users import serializers
from ovp_users import models
from rest_framework import response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters

class RecoveryTokenFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset

    def get_fields(self, view):
        return [
         'email']


class RecoveryTokenViewSet(viewsets.GenericViewSet):
    __doc__ = '\n  RecoveryToken resource endpoint\n  '
    queryset = models.User.objects.all()
    filter_backends = (RecoveryTokenFilter,)
    serializer_class = serializers.RecoveryTokenSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        try:
            user = self.get_queryset().get(email=email)
        except:
            user = None

        if user:
            limit = 5
            now = timezone.now()
            to_check = (now - relativedelta(hours=1)).replace(tzinfo=timezone.utc)
            tokens = models.PasswordRecoveryToken.objects.filter(user=user, created_date__gte=to_check)
            if tokens.count() >= limit:
                will_release = tokens.order_by('-created_date')[(limit - 1)].created_date + relativedelta(hours=1)
                seconds = abs((will_release - now).seconds)
                return response.Response({'success': False, 'message': 'Five tokens generated last hour.', 'try_again_in': seconds}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            token = models.PasswordRecoveryToken(user=user)
            token.save()
        return response.Response({'success': True, 'message': 'Token requested successfully(if user exists).'})


class RecoverPasswordFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset

    def get_fields(self, view):
        return [
         'email']


class RecoverPasswordViewSet(viewsets.GenericViewSet):
    __doc__ = '\n  RecoverPassword resource endpoint\n  '
    queryset = models.PasswordRecoveryToken.objects.all()
    filter_backends = (RecoverPasswordFilter,)
    serializer_class = serializers.RecoverPasswordSerializer

    def create(self, request, *args, **kwargs):
        token = request.data.get('token', None)
        new_password = request.data.get('new_password', None)
        day_ago = (timezone.now() - relativedelta(hours=24)).replace(tzinfo=timezone.utc)
        try:
            rt = self.get_queryset().get(token=token)
        except:
            rt = None

        if not rt or rt.used_date or rt.created_date < day_ago:
            return response.Response({'message': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return new_password or response.Response({'message': 'Empty password not allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(new_password, user=rt.user)
        except ValidationError as e:
            return response.Response({'message': 'Invalid password.', 'errors': e}, status=status.HTTP_400_BAD_REQUEST)

        serializers.RecoverPasswordSerializer(data=request.data, context=self.get_serializer_context()).is_valid(raise_exception=True)
        rt.used_date = timezone.now()
        rt.save()
        rt.user.password = new_password
        rt.user.save()
        return response.Response({'message': 'Password updated.'})