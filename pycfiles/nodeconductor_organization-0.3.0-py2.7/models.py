# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/models.py
# Compiled at: 2016-09-25 10:50:25
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from model_utils import FieldTracker
from nodeconductor.core import models as core_models
from nodeconductor.structure.models import Customer, CustomerRole

@python_2_unicode_compatible
class Organization(core_models.UuidMixin, core_models.NameMixin, models.Model):
    abbreviation = models.CharField(unique=True, max_length=8)
    native_name = models.CharField(max_length=160, blank=True, null=True)
    customer = models.OneToOneField(Customer, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return b'%(name)s (%(abbreviation)s)' % {b'name': self.name, 
           b'abbreviation': self.abbreviation}


@python_2_unicode_compatible
class OrganizationUser(core_models.UuidMixin, models.Model):
    user = models.OneToOneField(core_models.User)
    is_approved = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization)
    tracker = FieldTracker()

    def __str__(self):
        return b'%(username)s | %(abbreviation)s' % {b'username': self.user.username, 
           b'abbreviation': self.organization.abbreviation}

    def can_be_managed_by(self, user):
        customer = self.organization.customer
        if customer and customer.has_user(user, role_type=CustomerRole.OWNER):
            return True
        return user.is_staff