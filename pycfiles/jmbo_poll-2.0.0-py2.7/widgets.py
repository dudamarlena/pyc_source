# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/poll/widgets.py
# Compiled at: 2015-04-21 15:32:20
from django.forms.widgets import RadioFieldRenderer as BaseRadioFieldRenderer
from django.forms.widgets import RadioSelect as BaseRadioSelect
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class RadioFieldRenderer(BaseRadioFieldRenderer):
    """Use div tags instad of a ul tag for rendering"""

    def render(self):
        return mark_safe(('\n').join([ '<div>%s</div>' % force_unicode(w) for w in self
                                     ]))


class RadioSelect(BaseRadioSelect):
    renderer = RadioFieldRenderer