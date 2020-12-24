# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/django-manifest/manifest/api_views.py
# Compiled at: 2019-10-15 15:40:16
# Size of source mod 2**32: 14458 bytes
""" REST API Views
"""
from django.conf import settings
from django.contrib.auth import get_user_model, login as django_login, logout as django_logout
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from manifest import defaults, messages, serializers
from manifest.mixins import EmailChangeMixin, SendActivationMailMixin
from manifest.signals import REGISTRATION_COMPLETE
from manifest.utils import jwt_encode

@method_decorator((sensitive_post_parameters('password')), name='dispatch')
class AuthLoginAPIView(GenericAPIView):
    __doc__ = 'Check credentials, authenticate and return JWT Token\n    if credentials are valid.\n    '
    permission_classes = (
     AllowAny,)
    serializer_class = serializers.LoginSerializer
    token_serializer = serializers.JWTSerializer
    success_message = messages.AUTH_LOGIN_SUCCESS
    user = token = request = serializer = None

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token = jwt_encode(self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_login(self.request, self.user)

    def get_response(self):
        serializer_class = self.token_serializer
        data = {'detail':self.success_message, 
         'user':self.user, 
         'token':self.token}
        serializer = serializer_class(instance=data,
          context={'request': self.request})
        response = Response((serializer.data), status=(status.HTTP_200_OK))
        return response

    def post(self, request):
        self.request = request
        self.serializer = self.get_serializer(data=(self.request.data),
          context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class AuthLogoutAPIView(APIView):
    __doc__ = 'Calls Django logout method and delete the Token object\n    assigned to the current User object.\n\n    Accepts/Returns nothing.\n    '
    permission_classes = (
     AllowAny,)
    success_message = messages.AUTH_LOGOUT_SUCCESS

    def get(self, request, *args, **kwargs):
        if getattr(defaults, 'MANIFEST_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            raise (self.http_method_not_allowed)(request, *args, **kwargs)
        return (self.finalize_response)(request, response, *args, **kwargs)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)
        response = Response({'detail': self.success_message},
          status=(status.HTTP_200_OK))
        return response


@method_decorator((sensitive_post_parameters('password1', 'password2')),
  name='dispatch')
class AuthRegisterAPIView(CreateAPIView, SendActivationMailMixin):
    serializer_class = serializers.RegisterSerializer
    permission_classes = (AllowAny,)
    success_message = messages.AUTH_REGISTER_SUCCESS
    email_subject_template_name = 'manifest/emails/activation_email_subject.txt'
    email_message_template_name = 'manifest/emails/activation_email_message_api.txt'

    def get_response_data(self, user, token):
        data = {'detail':self.success_message, 
         'user':user,  'token':token}
        return serializers.JWTSerializer(data).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=(request.data))
        if request.user.is_authenticated:
            return Response({'detail': messages.AUTH_REGISTER_FORBIDDEN},
              status=(status.HTTP_403_FORBIDDEN))
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        REGISTRATION_COMPLETE.send(sender=None,
          user=user,
          request=(self.request))
        if defaults.MANIFEST_ACTIVATION_REQUIRED:
            self.send_activation_mail(user)
        headers = self.get_success_headers(serializer.data)
        return Response((self.get_response_data(user, jwt_encode(user))),
          status=(status.HTTP_201_CREATED),
          headers=headers)


class AuthActivateAPIView(GenericAPIView):
    __doc__ = 'Confirm the email address with username and confirmation key.\n\n    Confirms the new email address by running\n    ``get_user_model().objects.confirm_email`` method.\n\n    User will be redirected to ``email_change_complete`` view\n    if ``success_url`` is not defined.\n\n    If no ``User`` object returned the user will be shown the\n    ``template_name`` template displaying a fail message.\n    '
    serializer_class = serializers.ActivateSerializer
    permission_classes = (AllowAny,)
    success_message = messages.AUTH_ACTIVATE_SUCCESS
    error_message = messages.AUTH_ACTIVATE_ERROR

    def post(self, request):
        serializer = self.get_serializer(data=(request.data))
        serializer.is_valid(raise_exception=True)
        return Response({'detail': self.success_message})


class PasswordResetAPIView(GenericAPIView):
    __doc__ = 'Calls Django Auth PasswordResetForm save method.\n\n    Accepts the following POST parameters: email\n    Returns the success/fail message.\n    '
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)
    success_message = messages.PASSWORD_RESET_SUCCESS
    email_subject_template_name = 'manifest/emails/password_reset_subject.txt'
    email_body_template_name = 'manifest/emails/password_reset_message_api.txt'
    email_html_template_name = None

    def get_email_kwargs(self, request):
        return {'request':request, 
         'use_https':request.is_secure(), 
         'token_generator':default_token_generator, 
         'from_email':None, 
         'subject_template_name':self.email_subject_template_name, 
         'email_template_name':self.email_body_template_name, 
         'html_email_template_name':self.email_html_template_name, 
         'extra_email_context':None}

    def post(self, request):
        serializer = self.get_serializer(data=(request.data))
        serializer.is_valid(raise_exception=True)
        email_kwargs = self.get_email_kwargs(request)
        (serializer.reset_form.save)(**email_kwargs)
        return Response({'detail': self.success_message},
          status=(status.HTTP_200_OK))


class PasswordResetVerifyAPIView(GenericAPIView):
    __doc__ = "Password reset e-mail link is confirmed, therefore\n    this resets the user's password.\n\n    Accepts the following POST parameters:\n    token, uid, new_password1, new_password2\n    Returns the success/fail message.\n    "
    serializer_class = serializers.PasswordResetVerifySerializer
    permission_classes = (AllowAny,)
    success_message = messages.PASSWORD_RESET_VERIFY_SUCCESS

    def post(self, request):
        serializer = self.get_serializer(data=(request.data))
        serializer.is_valid(raise_exception=True)
        return Response({'detail': self.success_message})


@method_decorator((sensitive_post_parameters()), name='dispatch')
class PasswordResetConfirmAPIView(GenericAPIView):
    __doc__ = "Password reset e-mail link is confirmed, therefore\n    this resets the user's password.\n\n    Accepts the following POST parameters:\n    token, uid, new_password1, new_password2\n    Returns the success/fail message.\n    "
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    success_message = messages.PASSWORD_RESET_CONFIRM_SUCCESS

    def post(self, request):
        serializer = self.get_serializer(data=(request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': self.success_message})


class AuthProfileAPIView(RetrieveUpdateAPIView):
    __doc__ = 'Update profile of current user.\n\n    Updates profile information for ``request.user``. User will be\n    redirected to ``user`` view in ``success_url`` is not\n    defined.\n    '
    permission_classes = (
     IsAuthenticated,)
    serializer_class = serializers.AuthProfileSerializer
    success_message = messages.PROFILE_UPDATE_SUCCESS

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer((request.user), data=(request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': self.success_message})


class ProfileOptionsAPIView(APIView):
    __doc__ = 'Responses list of options for choicefields.\n    '
    permission_classes = (
     AllowAny,)
    serializer_class = serializers.ProfileUpdateSerializer

    def get(self, request, *args, **kwargs):
        genders = get_user_model()._meta.get_field('gender').choices
        timezones = get_user_model()._meta.get_field('timezone').choices
        locales = get_user_model()._meta.get_field('locale').choices
        choices = {'gender':dict(genders), 
         'timezone':dict(timezones), 
         'locale':dict(locales)}
        return Response(choices)


class EmailChangeAPIView(GenericAPIView, EmailChangeMixin):
    __doc__ = 'Change email of current user.\n\n    Changes email for ``request.user``. Change will not be applied\n    until user confirm their new email.\n    '
    serializer_class = serializers.EmailChangeSerializer
    permission_classes = (IsAuthenticated,)
    success_message = messages.EMAIL_CHANGE_SUCCESS
    email_message_template_name_new = 'manifest/emails/confirmation_email_message_new_api.txt'

    def post(self, request):
        serializer = self.get_serializer(user=(request.user), data=(request.data))
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_confirmation_mail(user)
        return Response({'detail': self.success_message})


class EmailChangeConfirmAPIView(GenericAPIView):
    __doc__ = 'Confirm the email address with username and confirmation key.\n\n    Confirms the new email address by running\n    ``get_user_model().objects.confirm_email`` method.\n\n    User will be redirected to ``email_change_complete`` view\n    if ``success_url`` is not defined.\n\n    If no ``User`` object returned the user will be shown the\n    ``template_name`` template displaying a fail message.\n    '
    serializer_class = serializers.EmailChangeConfirmSerializer
    permission_classes = (AllowAny,)
    success_message = messages.EMAIL_CHANGE_CONFIRM_SUCCESS
    error_message = messages.EMAIL_CHANGE_CONFIRM_ERROR

    def post(self, request):
        serializer = self.get_serializer(data=(request.data))
        serializer.is_valid(raise_exception=True)
        return Response({'detail': self.success_message})


class PictureUploadAPIView(GenericAPIView):
    __doc__ = 'Upload profile picture.\n    '
    serializer_class = serializers.PictureUploadSerializer
    permission_classes = (IsAuthenticated,)
    success_message = messages.PICTURE_UPLOAD_SUCCESS
    parser_class = (FormParser,)

    def post(self, request):
        serializer = self.get_serializer((request.user), data=(request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': self.success_message})


@method_decorator((sensitive_post_parameters()), name='dispatch')
class PasswordChangeAPIView(GenericAPIView):
    __doc__ = 'Calls Django Auth SetPasswordForm save method.\n\n    Accepts the following POST parameters: new_password1, new_password2\n    Returns the success/fail message.\n    '
    serializer_class = serializers.PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    success_message = messages.PASSWORD_CHANGE_SUCCESS

    def patch(self, request):
        serializer = self.get_serializer(user=(request.user), data=(request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': self.success_message})


class UserListAPIView(ListAPIView):
    __doc__ = 'Lists active user profiles, accepts ``GET``.\n\n    List view that lists active user profiles\n    if ``MANIFEST_DISABLE_PROFILE_LIST`` setting is ``False``,\n    else raises Http404.\n    '
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.get_visible_profiles()

    def get(self, request, *args, **kwargs):
        if defaults.MANIFEST_DISABLE_PROFILE_LIST:
            if not request.user.is_superuser:
                return Response(status=(status.HTTP_404_NOT_FOUND))
        return (super().get)(request, *args, **kwargs)


class UserDetailAPIView(RetrieveAPIView):
    __doc__ = 'Reads an active user profile by username, accepts ``GET``.\n\n    Detail view that reads an active user profile by username,\n    if ``MANIFEST_DISABLE_PROFILE_LIST`` setting is ``False``,\n    else raises Http404.\n    '
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.get_visible_profiles()
    lookup_field = 'username'
    lookup_url_kwarg = 'username'

    def get(self, request, *args, **kwargs):
        if defaults.MANIFEST_DISABLE_PROFILE_LIST:
            if not request.user.is_superuser:
                return Response(status=(status.HTTP_404_NOT_FOUND))
        return (super().get)(request, *args, **kwargs)