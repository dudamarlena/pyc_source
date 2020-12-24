# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/serializers/apply_user.py
# Compiled at: 2017-06-20 14:03:48
# Size of source mod 2**32: 1255 bytes
from ovp_projects import models
from rest_framework import serializers
from ovp_core.helpers import get_address_serializers
from ovp_uploads.serializers import UploadedImageSerializer
from ovp_organizations.serializers import OrganizationSearchSerializer
address_serializers = get_address_serializers()

class ProjectApplyRetrieveSerializer(serializers.ModelSerializer):
    image = UploadedImageSerializer()
    address = address_serializers[1]()
    organization = OrganizationSearchSerializer()

    class Meta:
        model = models.Project
        fields = ['slug', 'image', 'name', 'description', 'highlighted', 'published_date', 'address', 'details', 'created_date', 'organization', 'minimum_age', 'applied_count', 'max_applies', 'max_applies_from_roles', 'closed', 'closed_date', 'published', 'hidden_address', 'crowdfunding', 'public_project']

    def to_representation(self, instance):
        return super(ProjectApplyRetrieveSerializer, self).to_representation(instance)


class ApplyUserRetrieveSerializer(serializers.ModelSerializer):
    project = ProjectApplyRetrieveSerializer()

    class Meta:
        model = models.Apply
        fields = ['id', 'email', 'username', 'phone', 'date', 'canceled', 'canceled_date', 'project']