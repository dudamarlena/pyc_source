# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/VALDYS/MANAGER/app/fields/forms/content_type.py
# Compiled at: 2017-11-07 12:27:53
# Size of source mod 2**32: 1703 bytes
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms.widgets import Select
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe

def silent_reverse(url):
    try:
        return reverse(url)
    except NoReverseMatch:
        return ''


class GenericContentTypeSelect(Select):
    allow_multiple_selected = False

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        extra_attrs = {}
        if option_value:
            ct = ContentType.objects.get(pk=option_value)
            extra_attrs = {'data-generic-lookup-enabled':'yes', 
             'data-admin-url':silent_reverse('admin:{0.app_label}_{0.name}_changelist'.format(ct))}
        else:
            if option_value in selected_choices:
                selected_html = mark_safe(' selected="selected"')
                if not self.allow_multiple_selected:
                    selected_choices.remove(option_value)
            else:
                selected_html = ''
        return format_html('<option value="{0}"{1} {2}>{3}</option>', option_value, selected_html, mark_safe(' '.join(['{0}="{1}"'.format(k, v) for k, v in extra_attrs.items()])), force_text(option_label))

    class Media(object):
        js = ('admin/js/generic-lookup.js', )