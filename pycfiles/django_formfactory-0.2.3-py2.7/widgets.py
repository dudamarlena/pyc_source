# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/widgets.py
# Compiled at: 2017-11-28 02:59:59
import django
from django.forms.widgets import Widget
from django.utils.html import format_html

class ParagraphWidget(Widget):
    template_name = 'formfactory/forms/widgets/paragraph.html'

    def render(self, *args, **kwargs):
        if django.VERSION[1] >= 11 or django.VERSION[0] > 1:
            return super(ParagraphWidget, self).render(*args, **kwargs)
        else:
            return format_html(self.attrs['paragraph'])