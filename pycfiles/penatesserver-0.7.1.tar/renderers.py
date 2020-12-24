# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/renderers.py
# Compiled at: 2015-10-19 03:33:47
from __future__ import unicode_literals
from django.template import Context, loader
from django.utils import six
from rest_framework import serializers
from rest_framework.renderers import AdminRenderer, HTMLFormRenderer
__author__ = b'Matthieu Gallet'
default_styles = HTMLFormRenderer.default_style
default_styles[serializers.ListField] = {b'base_template': b'list_field.html'}

class HTMLListFormRenderer(HTMLFormRenderer):

    def render_field(self, field, parent_style):
        if isinstance(field._field, serializers.HiddenField):
            return b''
        style = dict(self.default_style[field])
        style.update(field.style)
        if b'template_pack' not in style:
            style[b'template_pack'] = parent_style.get(b'template_pack', self.template_pack)
        style[b'renderer'] = self
        original_field = field
        field = field.as_form_field()
        if style.get(b'input_type') == b'datetime-local' and isinstance(field.value, six.text_type):
            field.value = field.value.rstrip(b'Z')
        if b'template' in style:
            template_name = style[b'template']
        else:
            template_name = style[b'template_pack'].strip(b'/') + b'/' + style[b'base_template']
        template = loader.get_template(template_name)
        context = Context({b'field': field, b'style': style, b'original_field': original_field})
        return template.render(context)


class ListAdminRenderer(AdminRenderer):
    form_renderer_class = HTMLListFormRenderer