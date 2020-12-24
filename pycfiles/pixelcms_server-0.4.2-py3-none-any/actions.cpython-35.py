# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/admin_addons/actions.py
# Compiled at: 2016-08-04 10:10:57
# Size of source mod 2**32: 456 bytes
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

def duplicate(self, request, queryset):
    for q in queryset:
        try:
            q.pk = None
            q.save()
        except:
            self.message_user(request, _('Failed to duplicate "{}".').format(q), level=messages.ERROR)


duplicate.short_description = _('Duplicate selected items')