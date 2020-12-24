# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_newsletter/admin.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 2061 bytes
from django.contrib import admin
from .models import MailingList, Subscriber, SubscribeTask

@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_service', 'external_id')
    list_filter = ('external_service', )
    search_fields = ('name', 'external_id')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('mailing_list', 'email', 'first_name', 'last_name', 'external_id')
    list_filter = ('mailing_list__external_service', 'mailing_list')
    search_fields = ('email', 'first_name', 'last_name', 'external_id')
    fields = ('mailing_list', 'email', ('first_name', 'last_name'), 'external_id')
    actions = [
     'delete_selected_and_unsubscribe']

    def get_actions(self, request):
        actions = super(SubscriberAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_selected_and_unsubscribe(self, request, queryset):
        for obj in queryset:
            obj.unsubscribe()

        queryset.delete()


@admin.register(SubscribeTask)
class SubscribeTaskAdmin(admin.ModelAdmin):
    list_display = ('type', 'created', 'attempts', 'mailing_list', 'email', 'external_id')
    list_filter = ('type', 'created', 'attempts')
    search_fields = ('email', 'external_id', 'last_error')
    readonly_fields = list_display + ('last_error', 'first_name', 'last_name')
    fieldsets = (
     (
      None,
      {'fields': ('type', 'created', 'attempts', 'last_error')}),
     (
      'Data',
      {'fields': ('mailing_list', 'email', ('first_name', 'last_name'), 'external_id')}))

    def has_add_permission(self, request):
        return False