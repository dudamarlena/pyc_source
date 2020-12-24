# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/xadmin/adminx.py
# Compiled at: 2018-01-28 08:42:20
# Size of source mod 2**32: 1059 bytes
from __future__ import absolute_import
import xadmin
from .models import UserSettings, Log
from xadmin.layout import *
from django.utils.translation import ugettext_lazy as _, ugettext

class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True


xadmin.site.register(UserSettings, UserSettingsAdmin)

class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url('%s_%s_change' % (instance.content_type.app_label, instance.content_type.model), instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''

    link.short_description = ''
    link.allow_tags = True
    link.is_column = False
    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'


xadmin.site.register(Log, LogAdmin)