# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/filters.py
# Compiled at: 2016-09-25 10:50:25
from __future__ import unicode_literals
import django_filters
from nodeconductor.core import filters as core_filters
from nodeconductor.core.filters import UUIDFilter
from nodeconductor_organization import models

class OrganizationFilter(django_filters.FilterSet):
    customer_uuid = UUIDFilter(name=b'customer__uuid')
    customer = core_filters.URLFilter(view_name=b'customer-detail', name=b'customer__uuid')

    class Meta(object):
        model = models.Organization
        fields = [
         b'name',
         b'native_name',
         b'abbreviation',
         b'customer',
         b'customer_uuid']
        order_by = [
         b'name',
         b'native_name',
         b'abbreviation-name',
         b'-native_name',
         b'-abbreviation']


class OrganizationUserFilter(django_filters.FilterSet):
    organization = core_filters.URLFilter(view_name=b'organization-detail', name=b'organization__uuid')
    organization_uuid = UUIDFilter(name=b'organization__uuid')
    user = core_filters.URLFilter(view_name=b'user-detail', name=b'user__uuid')
    user_uuid = UUIDFilter(name=b'user__uuid')

    class Meta(object):
        model = models.OrganizationUser
        fields = [
         b'organization',
         b'organization_uuid',
         b'user',
         b'user_uuid',
         b'is_approved']
        order_by = [
         b'is_approved',
         b'-is_approved']