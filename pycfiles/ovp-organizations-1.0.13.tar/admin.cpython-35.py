# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/admin.py
# Compiled at: 2017-04-06 16:03:08
# Size of source mod 2**32: 2182 bytes
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from ovp_organizations.models import Organization
from ovp_core.mixins import CountryFilterMixin

class OrganizationAdmin(admin.ModelAdmin, CountryFilterMixin):
    fields = [
     ('id', 'highlighted'), ('name', 'slug'),
     'owner',
     ('published', 'deleted'),
     ('published_date', 'deleted_date'),
     'address',
     'image', 'cover',
     'facebook_page', 'website',
     'description', 'details',
     'causes', 'members',
     ('created_date', 'modified_date')]
    list_display = [
     'id', 'created_date', 'name', 'owner__email', 'owner__phone', 'address', 'highlighted', 'published', 'deleted', 'modified_date']
    list_filter = [
     'created_date', 'modified_date', 'highlighted', 'published', 'deleted']
    list_editable = [
     'highlighted', 'published']
    search_fields = [
     'name', 'owner__email', 'address__typed_address', 'description']
    readonly_fields = [
     'id', 'created_date', 'modified_date', 'published_date', 'deleted_date']
    filter_horizontal = ('causes', 'members')

    def owner__name(self, obj):
        if obj.owner:
            return obj.owner.name
        else:
            return _('None')

    owner__name.short_description = _("Owner's Name")
    owner__name.admin_order_field = 'owner__name'

    def owner__email(self, obj):
        if obj.owner:
            return obj.owner.email
        else:
            return _('None')

    owner__email.short_description = _("Owner's E-mail")
    owner__email.admin_order_field = 'owner__email'

    def owner__phone(self, obj):
        if obj.owner:
            return obj.owner.phone
        else:
            return _('None')

    owner__phone.short_description = _("Owner's Phone")
    owner__phone.admin_order_field = 'owner__phone'

    def get_queryset(self, request):
        qs = super(OrganizationAdmin, self).get_queryset(request)
        return self.filter_by_country(request, qs, 'address')


admin.site.register(Organization, OrganizationAdmin)