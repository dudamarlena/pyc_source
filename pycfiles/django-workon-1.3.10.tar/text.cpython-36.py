# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/VALDYS/MANAGER/app/fields/forms/text.py
# Compiled at: 2017-11-07 12:27:53
# Size of source mod 2**32: 627 bytes
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt
from .html import HtmlInput, HtmlField

class TextField(HtmlField):

    def __init__(self, *args, **kwargs):
        (super(TextField, self).__init__)(*args, **kwargs)


class TextInput(HtmlInput):

    def __init__(self, *args, **kwargs):
        kwargs['inline'] = True
        (super(TextInput, self).__init__)(*args, **kwargs)

    def get_tinymce_config(self, name, attrs):
        config = super(TextInput, self).get_tinymce_config(name, attrs)
        config['toolbar'] = 'undo redo'
        return config