# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/notifications/admin.py
# Compiled at: 2020-02-28 16:21:56
# Size of source mod 2**32: 2947 bytes
from __future__ import unicode_literals
from datetime import datetime
from django import forms
from django.contrib import admin
from .models import Notification, UserNotification

@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    actions = [
     'really_delete_selected']
    list_display = ('user', 'notification')
    search_fields = ('user__username', 'notification__name')

    def get_actions(self, request):
        actions = super(UserNotificationAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
        else:
            if queryset.count() == 1:
                message_bit = '1 UserNotification entry was'
            else:
                message_bit = '%s usernotification entries were' % queryset.count()
            self.message_user(request, '%s successfully deleted.' % message_bit)

    really_delete_selected.short_description = 'Delete selected entries'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ('management', )
    fields = ('name', 'message', 'expires', 'needs_approval', 'snooze_time', 'groups',
              'look', 'image', 'management')

    def management(self, instance):
        EXCLUDED_FIELDS = [
         'groups',
         'id',
         'recipients',
         'attachment',
         'active_from',
         'snooze_lock',
         'recipients',
         'send_email']
        params = ''
        for field in instance.__class__._meta.get_fields():
            if field.name in EXCLUDED_FIELDS:
                pass
            else:
                attr = getattr(instance, field.name, None)
                if not attr is None:
                    if attr == '':
                        pass
                    else:
                        if isinstance(attr, datetime):
                            attr = attr.isoformat()
                        if field.name == 'message':
                            attr = ''.join(attr.split('\n'))
                            attr = ''.join(attr.split('\r'))
                        params += " --{}='{}'".format(field.name, attr)
                groups = ','.join(instance.groups.values_list('id', flat=True))
                if groups:
                    params += ' --groups={}'.format(groups)
                return 'python manage.py import_notification{}'.format(params)

    management.short_description = 'Management'

    def save_model(self, request, obj, form, change):
        super(NotificationAdmin, self).save_model(request, obj, form, change)
        for group in form.cleaned_data['groups']:
            for user in group.user_set.all():
                UserNotification.objects.get_or_create(notification=obj, user=user)