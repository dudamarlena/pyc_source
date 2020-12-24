# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/umeboshi/admin.py
# Compiled at: 2015-12-31 08:37:33
from django.contrib import admin
from umeboshi.models import Event

def link_to_field(field_name, short_description=None, getter=None):
    """
    Generic field linking for to-one.
    """

    def fn(obj):
        field = getter(obj) if getter else getattr(obj, field_name)
        if field:
            return ('<a href="{}">{}</a>').format(field.get_admin_url(), field)
        return '(None)'

    fn.short_description = short_description or field_name.title()
    fn.admin_order_field = field_name
    fn.allow_tags = True
    return fn


class EventAdmin(admin.ModelAdmin):
    list_filter = [
     'trigger_name', 'status']
    date_hierarchy = 'datetime_processed'
    list_display = [
     'id',
     'trigger_name',
     'status',
     'datetime_created',
     'datetime_scheduled',
     'datetime_processed']
    readonly_fields = [
     'id', 'trigger_name', 'datetime_created',
     'datetime_processed', '_args']
    fieldsets = (
     (
      'Events',
      {'fields': ('id', 'trigger_name', '_args')}),
     (
      'Status',
      {'fields': ('status', 'datetime_created', 'datetime_scheduled', 'datetime_processed')}))

    def _args(self, obj):
        return (', ').join(str(a) for a in obj.args)


admin.site.register(Event, EventAdmin)