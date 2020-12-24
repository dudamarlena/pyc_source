# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/serializers.py
# Compiled at: 2016-09-25 10:50:25
from __future__ import unicode_literals
from rest_framework import serializers
from rest_framework.permissions import SAFE_METHODS
from nodeconductor.core.models import User
from nodeconductor.structure.models import Customer
from nodeconductor_organization import models

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    customer = serializers.HyperlinkedRelatedField(view_name=b'customer-detail', lookup_field=b'uuid', queryset=Customer.objects.all(), allow_null=True)

    class Meta(object):
        model = models.Organization
        extra_kwargs = {b'url': {b'lookup_field': b'uuid'}}

    def validate(self, data):
        customer = data.get(b'customer')
        if customer is None:
            return super(OrganizationSerializer, self).validate(data)
        else:
            organizations = models.Organization.objects.filter(customer=customer)
            if organizations.exists():
                raise serializers.ValidationError(b'Organization for this customer already exist.')
            return super(OrganizationSerializer, self).validate(data)

    def get_fields(self):
        fields = super(OrganizationSerializer, self).get_fields()
        request = self.context[b'request']
        user = request.user
        if not user.is_staff:
            del fields[b'customer']
        return fields


class OrganizationUserSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name=b'user-detail', lookup_field=b'uuid', queryset=User.objects.all())
    username = serializers.ReadOnlyField(source=b'user.username')

    class Meta(object):
        model = models.OrganizationUser
        view_name = b'organization_user-detail'
        extra_kwargs = {b'organization': {b'lookup_field': b'uuid'}, b'url': {b'lookup_field': b'uuid'}}

    def validate(self, data):
        user = data.get(b'user')
        organization_users = models.OrganizationUser.objects.filter(user=user)
        if organization_users.exists():
            raise serializers.ValidationError(b'User can belong only to one organization.')
        return super(OrganizationUserSerializer, self).validate(data)

    def get_fields(self):
        fields = super(OrganizationUserSerializer, self).get_fields()
        request = self.context[b'request']
        if not request.user.is_staff:
            fields[b'user'].queryset = User.objects.filter(uuid=request.user.uuid)
        if request.method not in SAFE_METHODS:
            del fields[b'is_approved']
        return fields