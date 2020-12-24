# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/api/input_serializers.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 1518 bytes
import django.utils.translation as _
from rest_framework import serializers
from common.api.fields import JsonField
from common.api.serializers import BaseCustomSerializer

class ResolveUrlInputSerializer(BaseCustomSerializer):
    """ResolveUrlInputSerializer"""
    viewname = serializers.CharField()
    args = serializers.ListField(required=False)
    kwargs = serializers.JSONField(required=False)


class ResetPasswordSerializer(BaseCustomSerializer):
    """ResetPasswordSerializer"""
    username = serializers.CharField(max_length=30, required=False, label=(_("nom d'utilisateur")))
    email = serializers.EmailField(required=False, label=(_('e-mail')))


class ConfirmPasswordSerializer(BaseCustomSerializer):
    """ConfirmPasswordSerializer"""
    secret_key = serializers.CharField(label=(_('clé secrète')))
    uid = serializers.CharField(label=(_('identifiant')))
    token = serializers.CharField(label=(_('token')))
    password = serializers.CharField(label=(_('mot de passe')), write_only=True, style=dict(input_type='password'))


class MetaDataSerializer(BaseCustomSerializer):
    """MetaDataSerializer"""
    key = serializers.CharField(label=(_('clé')))
    value = JsonField(required=False, label=(_('valeur')))
    date = serializers.DateTimeField(required=False, label=(_('date péremption')))