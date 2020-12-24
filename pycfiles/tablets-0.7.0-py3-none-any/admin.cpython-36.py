# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./../tablets/admin.py
# Compiled at: 2019-01-24 09:14:36
# Size of source mod 2**32: 2507 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_ace import AceWidget
from mptt.admin import MPTTModelAdmin
from .models import Template

class AceWidgetMixin(object):

    def formfield_for_dbfield(self, db_field, **kwargs):
        if getattr(settings, 'USE_ACE_WIDGET', True):
            if db_field.name == 'content':
                kwargs['widget'] = AceWidget(mode=(getattr(settings, 'ACE_MODE', 'twig')), theme=(getattr(settings, 'ACE_THEME', 'chrome')),
                  width=(getattr(settings, 'ACE_WIDTH', '100%')),
                  height=(getattr(settings, 'ACE_HEIGHT', '300px')))
        return (super(AceWidgetMixin, self).formfield_for_dbfield)(db_field, **kwargs)


class ChildInline(admin.TabularInline):
    model = Template
    verbose_name = 'Extending Template'
    verbose_name_plural = 'Extending Templates'
    extra = 1
    readonly_fields = [
     'admin_id', 'admin_name']
    fields = ['admin_id', 'admin_name']

    def has_add_permission(self, request):
        return False

    def admin_id(self, obj):
        return obj.pk

    admin_id.short_description = 'Id'

    def admin_name(self, obj):
        try:
            url = reverse('admin:tablets_template_change', args=(obj.pk,))
            return '<a href="{0}">{1}</a>'.format(url, obj.name)
        except Exception:
            return obj.name

    admin_name.short_description = 'Name'
    admin_name.allow_tags = True


class TemplateAdmin(AceWidgetMixin, MPTTModelAdmin):
    inlines = [
     ChildInline]
    list_display = ['name', 'parent', 'template_engine']
    raw_id_fields = ['parent']
    mptt_level_indent = 20

    @property
    def admin_view_info(self):
        return '%s_%s' % (self.model._meta.app_label, self.model._meta.model_name)

    def get_urls(self):
        urls = super(TemplateAdmin, self).get_urls()
        my_urls = [
         url('^(.+)/render/', (self.render), name=('%s_render' % self.admin_view_info))]
        return my_urls + urls

    def render(self, request, obj_id):
        template = get_object_or_404(Template, pk=obj_id)
        return HttpResponse(template.render(template.get_default_context()))


admin.site.register(Template, TemplateAdmin)