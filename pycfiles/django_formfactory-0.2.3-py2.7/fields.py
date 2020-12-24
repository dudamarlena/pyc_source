# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/fields.py
# Compiled at: 2017-11-28 02:59:59
import markdown
from django.forms.fields import Field
from django.utils.text import mark_safe
from django.utils.translation import ugettext as _
from formfactory import widgets

class ParagraphField(Field):
    widget = widgets.ParagraphWidget

    def __init__(self, paragraph='', *args, **kwargs):
        super(ParagraphField, self).__init__(*args, **kwargs)
        self.label = ''
        self.required = False
        self.widget.is_required = False
        if paragraph == '':
            paragraph = _('Please set a value for this field.')
        data = {'base_attrs': self.widget.attrs, 
           'extra_attrs': {'paragraph': markdown.markdown(paragraph)}}
        attrs = self.widget.build_attrs(**data)
        self.widget.attrs = attrs