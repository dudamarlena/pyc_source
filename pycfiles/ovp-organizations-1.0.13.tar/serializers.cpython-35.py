# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/serializers.py
# Compiled at: 2017-06-22 12:25:06
# Size of source mod 2**32: 4111 bytes
from django.core.exceptions import ValidationError
from ovp_uploads.serializers import UploadedImageSerializer
from ovp_users.models.user import User
from ovp_core.models import Cause
from ovp_core.helpers import get_address_serializers
from ovp_core.serializers.cause import CauseSerializer, CauseAssociationSerializer
from ovp_organizations import models
from ovp_organizations import validators
from ovp_organizations.decorators import hide_address
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import fields
from rest_framework.compat import set_many
from rest_framework.utils import model_meta
address_serializers = get_address_serializers()

class OrganizationCreateSerializer(serializers.ModelSerializer):
    address = address_serializers[0](required=False)
    causes = CauseAssociationSerializer(many=True, required=False)

    class Meta:
        model = models.Organization
        fields = ['id', 'slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type', 'image', 'cover', 'hidden_address', 'causes', 'contact_name', 'contact_email', 'contact_phone']

    def create(self, validated_data):
        causes = validated_data.pop('causes', [])
        address_data = validated_data.pop('address', None)
        if address_data:
            address_sr = address_serializers[0](data=address_data)
            address = address_sr.create(address_data)
            validated_data['address'] = address
        organization = models.Organization.objects.create(**validated_data)
        for cause in causes:
            c = Cause.objects.get(pk=cause['id'])
            organization.causes.add(c)

        return organization

    def update(self, instance, validated_data):
        causes = validated_data.pop('causes', [])
        address_data = validated_data.pop('address', None)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                set_many(instance, attr, value)
            else:
                setattr(instance, attr, value)

        if address_data:
            address_sr = address_serializers[0](data=address_data)
            address = address_sr.create(address_data)
            instance.address = address
        if causes:
            instance.causes.clear()
            for cause in causes:
                c = Cause.objects.get(pk=cause['id'])
                instance.causes.add(c)

        instance.save()
        return instance


class UserOrganizationRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'email', 'phone']


class OrganizationSearchSerializer(serializers.ModelSerializer):
    address = address_serializers[2]()
    image = UploadedImageSerializer()

    class Meta:
        model = models.Organization
        fields = ['id', 'slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type', 'image']


class OrganizationRetrieveSerializer(serializers.ModelSerializer):
    address = address_serializers[0]()
    image = UploadedImageSerializer()
    cover = UploadedImageSerializer()
    causes = CauseSerializer(many=True)
    owner = UserOrganizationRetrieveSerializer()

    class Meta:
        model = models.Organization
        fields = ['slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type', 'image', 'cover', 'published', 'hidden_address', 'causes', 'contact_name', 'contact_phone', 'contact_email']

    @hide_address
    def to_representation(self, instance):
        return super(OrganizationRetrieveSerializer, self).to_representation(instance)


class OrganizationInviteSerializer(serializers.Serializer):
    email = fields.EmailField(validators=[validators.invite_email_validator])

    class Meta:
        fields = [
         'email']


class MemberRemoveSerializer(serializers.Serializer):
    email = fields.EmailField(validators=[validators.invite_email_validator])

    class Meta:
        fields = [
         'email']