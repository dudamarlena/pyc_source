# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_forms/djinn_forms/widgets/image.py
# Compiled at: 2014-03-04 08:09:49
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

class ImageWidget(forms.widgets.Widget):
    """ Image upload widget """
    template_name = 'djinn_forms/snippets/imagewidget.html'

    def render(self, name, value, attrs=None):
        try:
            value = self.model.objects.get(pk=value)
        except:
            pass

        context = {'name': name, 
           'widget': self, 
           'show_progress': True, 
           'multiple': False, 
           'value': value}
        context.update(self.attrs)
        if value:
            accessor = 'get_%s_url' % self.attrs.get('size', 'thumbnail')
            try:
                context['image_url'] = getattr(value, accessor)()
            except:
                pass

        if attrs:
            context.update(attrs)
        return mark_safe(render_to_string(self.template_name, context))