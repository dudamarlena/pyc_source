# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Andrea/Dropbox/Projects/django-custom-tools/django-countable-field/countable_field/widgets.py
# Compiled at: 2017-06-25 19:56:02
# Size of source mod 2**32: 1626 bytes
from django import VERSION
from django.forms import widgets
from django.utils.safestring import mark_safe

class CountableWidget(widgets.Textarea):

    class Media:
        js = ('countable_field/js/scripts.js', )
        css = {'all': ('countable_field/css/styles.css', )}

    def render(self, name, value, attrs=None, **kwargs):
        if VERSION[:2] >= (1, 11):
            final_attrs = self.build_attrs(self.attrs, attrs)
        else:
            final_attrs = self.build_attrs(attrs)
        if not isinstance(final_attrs.get('data-min-count'), int):
            final_attrs['data-min-count'] = 'false'
        if not isinstance(final_attrs.get('data-max-count'), int):
            final_attrs['data-max-count'] = 'false'
        if VERSION[:2] >= (1, 11):
            output = super(CountableWidget, self).render(name, value, final_attrs, **kwargs)
        else:
            output = super(CountableWidget, self).render(name, value, final_attrs)
        output += self.get_word_count_template(final_attrs)
        return mark_safe(output)

    @staticmethod
    def get_word_count_template(attrs):
        return '<span class="text-count" id="%(id)s_counter">Word count: <span class="text-count-current">0</span></span>\r\n<script type="text/javascript">var countableField = new CountableField("%(id)s")</script>\n' % {'id': attrs.get('id')}