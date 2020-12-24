# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/api/input_serializers.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 1518 bytes
import django.utils.translation as _
from rest_framework import serializers
from common.api.fields import JsonField
from common.api.serializers import BaseCustomSerializer

class ResolveUrlInputSerializer(BaseCustomSerializer):
    __doc__ = "\n    Serializer pour la résolution d'URLs\n    "
    viewname = serializers.CharField()
    args = serializers.ListField(required=False)
    kwargs = serializers.JSONField(required=False)


class ResetPasswordSerializer(BaseCustomSerializer):
    __doc__ = '\n    Serializer pour la réinitialisation du mot de passe utilisateur\n    '
    username = serializers.CharField(max_length=30, required=False, label=(_("nom d'utilisateur")))
    email = serializers.EmailField(required=False, label=(_('e-mail')))


class ConfirmPasswordSerializer(BaseCustomSerializer):
    __doc__ = '\n    Serializer pour la confirmation de réinitialisation du mot de passe\n    '
    secret_key = serializers.CharField(label=(_('clé secrète')))
    uid = serializers.CharField(label=(_('identifiant')))
    token = serializers.CharField(label=(_('token')))
    password = serializers.CharField(label=(_('mot de passe')), write_only=True, style=dict(input_type='password'))


class MetaDataSerializer(BaseCustomSerializer):
    __doc__ = "\n    Serializer pour l'ajout de métadonnées sur une entité\n    "
    key = serializers.CharField(label=(_('clé')))
    value = JsonField(required=False, label=(_('valeur')))
    date = serializers.DateTimeField(required=False, label=(_('date péremption')))