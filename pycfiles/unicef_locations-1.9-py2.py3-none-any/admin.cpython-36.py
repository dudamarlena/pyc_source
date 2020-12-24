# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/admin.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 2581 bytes
from celery import chain
from django import forms
from django.contrib import admin as basic_admin
from django.contrib.gis import admin
from django.forms import Textarea
from leaflet.admin import LeafletGeoAdmin
from mptt.admin import MPTTModelAdmin
from .forms import CartoDBTableForm
from .models import CartoDBTable, GatewayType, Location
from .tasks import update_sites_from_cartodb

class AutoSizeTextForm(forms.ModelForm):
    __doc__ = '\n    Use textarea for name and description fields\n    '

    class Meta:
        widgets = {'name':Textarea(), 
         'description':Textarea()}


class ActiveLocationsFilter(basic_admin.SimpleListFilter):
    title = 'Active Status'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return [
         (True, 'Active'),
         (False, 'Archived')]

    def queryset(self, request, queryset):
        return (queryset.filter)(**self.used_parameters)


class LocationAdmin(LeafletGeoAdmin, MPTTModelAdmin):
    save_as = True
    form = AutoSizeTextForm
    fields = [
     'name',
     'gateway',
     'p_code',
     'geom',
     'point']
    list_display = ('name', 'gateway', 'p_code', 'is_active')
    list_filter = (
     'gateway',
     ActiveLocationsFilter,
     'parent')
    search_fields = ('name', 'p_code')

    def get_queryset(self, request):
        qs = Location.objects.all_locations()
        ordering = self.get_ordering(request)
        if ordering:
            qs = (qs.order_by)(*ordering)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = [] if request.user.is_superuser else ['p_code', 'geom', 'point', 'gateway']
        return (super(LocationAdmin, self).get_form)(request, obj, **kwargs)


class CartoDBTableAdmin(admin.ModelAdmin):
    form = CartoDBTableForm
    save_as = True
    list_display = ('table_name', 'location_type', 'name_col', 'pcode_col', 'parent_code_col')
    actions = ('import_sites', )

    def import_sites(self, request, queryset):
        queryset = sorted(queryset, key=(lambda l: (l.tree_id, l.lft, l.pk)))
        chain([update_sites_from_cartodb.si(table.pk) for table in queryset]).delay()


admin.site.register(Location, LocationAdmin)
admin.site.register(GatewayType)
admin.site.register(CartoDBTable, CartoDBTableAdmin)