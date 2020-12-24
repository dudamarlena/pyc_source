# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/django-manifest/manifest/serializers.py
# Compiled at: 2019-10-15 15:40:16
# Size of source mod 2**32: 13382 bytes
""" Manifest REST API Serializers
"""
import datetime
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.utils.encoding import force_text
import django.utils.http as uid_decoder
import django.utils.translation as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from manifest import defaults
from manifest.messages import EMAIL_IN_USE_MESSAGE
from manifest.utils import validate_picture
USER_MODEL = get_user_model()

class JWTSerializer(serializers.Serializer):
    __doc__ = '\n    Serializer for JWT authentication.\n    '
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        return UserSerializer((obj['user']), context=(self.context)).data


class LoginSerializer(serializers.Serializer):
    identification = serializers.CharField(error_messages={'required': _('Please enter your username or email address.')})
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        identification = attrs.get('identification')
        password = attrs.get('password')
        user = None
        if identification:
            if password:
                user = authenticate(identification=identification,
                  password=password)
                if user is None:
                    raise serializers.ValidationError(_('Please check your identification and password.'))
                if not user.is_active:
                    raise serializers.ValidationError(_('User account is not activated.'))
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    __doc__ = '\n    Serializer for creating a new user account.\n\n    Validates that the requested username and email is not already in use.\n    Also requires the password to be entered twice.\n\n    '
    username = serializers.RegexField(regex='^\\w+$',
      max_length=24,
      min_length=4,
      required=True,
      error_messages={'invalid': _('Username must contain only letters, numbers and underscores.')})
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, value):
        """
        Validate that the username is unique and not listed
        in ``defaults.MANIFEST_FORBIDDEN_USERNAMES`` list.

        """
        try:
            get_user_model().objects.get(username=value)
        except get_user_model().DoesNotExist:
            pass
        else:
            raise serializers.ValidationError(_('A user with that username already exists.'))
        if value.lower() in defaults.MANIFEST_FORBIDDEN_USERNAMES:
            raise serializers.ValidationError(_('This username is not allowed.'))
        return value

    def validate_email(self, value):
        """
        Validate that the email address is unique.

        """
        if get_user_model().objects.filter(Q(email__iexact=value) | Q(email_unconfirmed__iexact=value)):
            raise serializers.ValidationError(EMAIL_IN_USE_MESSAGE)
        return value

    def validate_password1(self, value):
        password1 = self.initial_data['password1']
        password2 = self.initial_data['password2']
        if password1:
            if password2:
                if password1 != password2:
                    raise serializers.ValidationError(_('The two password fields didn’t match.'))
        return value

    def save(self, **kwargs):
        """
        Creates a new user and account. Returns the newly created user.

        """
        user = get_user_model().objects.create_user(self.validated_data['username'], self.validated_data['email'], self.validated_data['password1'], not defaults.MANIFEST_ACTIVATION_REQUIRED)
        return user


class ActivateSerializer(serializers.Serializer):
    username = serializers.CharField()
    token = serializers.CharField()
    _errors = {}

    def validate(self, attrs):
        user = USER_MODEL.objects.activate_user(attrs['username'], attrs['token'])
        if not user:
            raise ValidationError('Token validation failed.')
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    __doc__ = '\n    Serializer for requesting a password reset e-mail.\n    '
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=(self.initial_data))
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        return value


class PasswordResetVerifySerializer(serializers.Serializer):
    __doc__ = '\n    Serializer for vaerifying a password token.\n    '
    uid = serializers.CharField()
    token = serializers.CharField()
    user = None
    _errors = {}

    def validate(self, attrs):
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = USER_MODEL.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, USER_MODEL.DoesNotExist):
            raise ValidationError({'uid': ['Invalid uid.']})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid token.']})
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    __doc__ = '\n    Serializer for requesting a password reset e-mail.\n    '
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()
    set_password_form_class = SetPasswordForm
    user = None
    _errors = {}
    set_password_form = None

    def validate(self, attrs):
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = USER_MODEL.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, USER_MODEL.DoesNotExist):
            raise ValidationError({'uid': ['Invalid uid.']})

        self.set_password_form = self.set_password_form_class(user=(self.user),
          data=attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid token.']})
        return attrs

    def save(self, **kwargs):
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    set_password_form_class = SetPasswordForm
    set_password_form = None

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        (super().__init__)(*args, **kwargs)

    def validate_old_password(self, value):
        invalid_password_conditions = (
         self.user,
         not self.user.check_password(value))
        if all(invalid_password_conditions):
            err_msg = _('Your old password was entered incorrectly. Please enter it again.')
            raise serializers.ValidationError(err_msg)
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(user=(self.user),
          data=attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self, **kwargs):
        self.set_password_form.save()


class EmailChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def __init__(self, *args, user=None, **kwargs):
        """
        The current ``user`` is needed for initialisation of this form so
        that we can check if the email address is still free and not always
        returning ``True`` for this query because it's the users own email
        address.

        """
        self.user = user
        (super().__init__)(*args, **kwargs)

    def validate_email(self, value):
        """
        Validate that the email is not already registered with another user.

        """
        if value.lower() == self.user.email:
            raise serializers.ValidationError(_("You're already known under this email address."))
        if get_user_model().objects.filter(email__iexact=value).exclude(email__iexact=(self.user.email)):
            raise serializers.ValidationError(EMAIL_IN_USE_MESSAGE)
        return value

    def save(self, **kwargs):
        """
        Save method calls :func:`user.change_email()` method which sends out
        an email with a verification key to verify and with it enable this
        new email address.

        """
        return self.user.change_email(self.validated_data['email'])


class EmailChangeConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    token = serializers.CharField()
    _errors = {}

    def validate(self, attrs):
        user = USER_MODEL.objects.confirm_email(attrs['username'], attrs['token'])
        if not user:
            raise ValidationError('Token validation failed.')
        return attrs


class DateField(serializers.DateField):
    __doc__ = ' Custom timezone serializer field to make it JSON serializable '

    def to_representation(self, value):
        return datetime.datetime.strftime(value, '%d/%m/%Y')

    def to_internal_value(self, value):
        return datetime.datetime.strptime(value, '%d/%m/%Y')


class AuthProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.ChoiceField(choices=(get_user_model()._meta.get_field('gender').choices))
    birth_date = DateField(required=True,
      input_formats=['%d/%m/%Y', '%d.%m.%Y'])
    avatar = serializers.SerializerMethodField('get_avatar')
    timezone = serializers.ChoiceField(choices=(get_user_model()._meta.get_field('timezone').choices))
    locale = serializers.ChoiceField(choices=(get_user_model()._meta.get_field('locale').choices))

    class Meta:
        model = USER_MODEL
        fields = ('first_name', 'last_name', 'gender', 'birth_date', 'timezone', 'locale',
                  'avatar')

    def get_avatar(self, obj):
        return self.context.get('request').build_absolute_uri(obj.avatar)


class ProfileUpdateSerializer(AuthProfileSerializer):
    __doc__ = ' Base serializer used for fields that are always required '

    class Meta:
        model = USER_MODEL
        fields = ('first_name', 'last_name', 'gender', 'birth_date')


class RegionUpdateSerializer(AuthProfileSerializer):
    __doc__ = ' Base form used for fields that are always required '

    class Meta:
        model = USER_MODEL
        fields = ('timezone', 'locale')


class PictureUploadSerializer(serializers.ModelSerializer):
    __doc__ = ' Base form used for fields that are always required '
    picture = serializers.ImageField()

    class Meta:
        model = USER_MODEL
        fields = ('picture', )

    def validate_picture(self, value):
        """
        Validates format and file size of uploaded profile picture.

        """
        return validate_picture(value, serializers)


class UserSerializer(serializers.ModelSerializer):
    __doc__ = '\n    User model w/o password\n    '

    class Meta:
        model = USER_MODEL
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email', )