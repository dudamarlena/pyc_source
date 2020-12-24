# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/widgets.py
# Compiled at: 2016-04-01 12:16:58
# Size of source mod 2**32: 2457 bytes
from __future__ import unicode_literals, absolute_import
from pkg_resources import parse_version
from django import forms, get_version
from django.contrib.admin.widgets import AdminTextareaWidget
from django.contrib.admin.templatetags.admin_static import static
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.conf import settings
__all__ = [
 'AdminHStoreWidget']

class BaseAdminHStoreWidget(AdminTextareaWidget):
    __doc__ = '\n    Base admin widget class for default-admin and grappelli-admin widgets\n    '
    admin_style = 'default'

    @property
    def media(self):
        internal_js = [
         'django_hstore/underscore-min.js',
         'django_hstore/hstore-widget.js']
        js = [static('admin/js/%s' % path) for path in internal_js]
        return forms.Media(js=js)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'hstore-original-textarea'
        html = super(BaseAdminHStoreWidget, self).render(name, value, attrs)
        template_context = Context({'field_name': name, 
         'STATIC_URL': settings.STATIC_URL, 
         'use_svg': parse_version(get_version()) >= parse_version('1.9')})
        template = get_template('hstore_%s_widget.html' % self.admin_style)
        additional_html = template.render(template_context)
        html = html + additional_html
        html = mark_safe(html)
        return html


class DefaultAdminHStoreWidget(BaseAdminHStoreWidget):
    __doc__ = '\n    Widget that displays the HStore contents\n    in the default django-admin with a nice interactive UI\n    '
    admin_style = 'default'


class GrappelliAdminHStoreWidget(BaseAdminHStoreWidget):
    __doc__ = '\n    Widget that displays the HStore contents\n    in the django-admin with a nice interactive UI\n    designed for django-grappelli\n    '
    admin_style = 'grappelli'


if 'grappelli' in settings.INSTALLED_APPS:
    AdminHStoreWidget = GrappelliAdminHStoreWidget
else:
    AdminHStoreWidget = DefaultAdminHStoreWidget