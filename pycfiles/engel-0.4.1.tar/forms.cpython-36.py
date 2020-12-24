# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wduss/src/github.com/dalloriam/engel/engel/widgets/forms.py
# Compiled at: 2017-01-06 15:18:40
# Size of source mod 2**32: 1376 bytes
import html
from .base import BaseElement
from ..utils import html_property

class Button(BaseElement):
    __doc__ = '\n    A simple button.\n    '
    html_tag = 'button'

    def build(self, text):
        super(Button, self).build()
        self.content = text


class TextBox(BaseElement):
    __doc__ = '\n    A simple textbox.\n    '
    html_tag = 'input'

    @property
    def text(self):
        """
        Text content of the TextBox
        """
        return self._text

    @text.setter
    def text(self, value):
        self._text = html.escape(value)
        if self.view:
            if self.view.is_loaded:
                self.view.dispatch({'name':'text',  'selector':'#' + self.id,  'text':value})

    input_type = html_property('type')
    name = html_property('name')

    def build(self, name=None):
        super(TextBox, self).build()
        self._text = ''
        self.input_type = 'text'
        if name:
            self.name = name

    def on_view_attached(self):
        super(TextBox, self).on_view_attached()

        def text_changed_callback(event, interface):
            self._text = html.escape(event['event_object']['target']['value'])

        self.view.on('change', text_changed_callback, '#' + self.id)