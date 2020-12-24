# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/eventcalendar/base/wagtail_eventcalendar/wagtail_eventcalendar/wagtail_hooks.py
# Compiled at: 2018-10-04 03:13:57
# Size of source mod 2**32: 1343 bytes
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from .models import EventCalPage, Category

class EventCalPageModelAdmin(ModelAdmin):
    __doc__ = '\n    ModelAdmin required for pulling the calender functionality out of the pages hierarchy for easier accessibility.\n    '
    model = EventCalPage
    menu_label = _('Calendar Events')
    menu_icon = 'date'
    list_display = ('title', 'start_dt', 'description', 'categories')
    list_filter = ('start_dt', 'categories')
    search_fields = ('title', 'description', 'start_dt', 'categories')


class EventCalPageCategoryAdmin(ModelAdmin):
    __doc__ = '\n    Model Admin required for making the calendar categories available in the special calendar tab\n    '
    model = Category
    menu_label = _('Categories')
    menu_icon = 'group'
    list_display = ('name', )
    search_fields = ('name', )


class EventCalendarModelAdminGroup(ModelAdminGroup):
    __doc__ = '\n    ModelAdminGroup that allows one to add Events/Calendar Entries via a tab on the sidebar rather than digging through the page hierarchy.\n    '
    menu_label = _('Calendar')
    menu_icon = 'date'
    menu_order = 300
    items = (EventCalPageModelAdmin, EventCalPageCategoryAdmin)


modeladmin_register(EventCalendarModelAdminGroup)