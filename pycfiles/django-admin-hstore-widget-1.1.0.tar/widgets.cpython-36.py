# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adufour/Projets/django-admin-hstore/django_admin_hstore_widget/widgets.py
# Compiled at: 2018-03-05 07:50:48
# Size of source mod 2**32: 1504 bytes
from django.conf import settings
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.widgets import AdminTextareaWidget
from django.contrib.postgres.forms import forms
from django.template.loader import get_template
from django.utils.safestring import mark_safe

class HStoreFormWidget(AdminTextareaWidget):

    @property
    def media(self):
        internal_js = [
         'django_admin_hstore_widget/underscore-min.js',
         'django_admin_hstore_widget/django_admin_hstore_widget.js']
        js = [static('admin/js/%s' % path) for path in internal_js]
        return forms.Media(js=js)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'hstore-original-textarea'
        html = super(HStoreFormWidget, self).render(name, value, attrs)
        template_context = {'field_name':name, 
         'STATIC_URL':settings.STATIC_URL}
        template = get_template('django_admin_hstore_widget.html')
        additional_html = template.render(template_context)
        html = html + additional_html
        html = mark_safe(html)
        return html