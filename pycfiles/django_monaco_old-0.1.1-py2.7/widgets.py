# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/monaco/widgets.py
# Compiled at: 2020-03-12 10:19:44
from __future__ import absolute_import, unicode_literals
from django import forms

class MonacoEditorWidget(forms.Textarea):

    def render(self, name, value, attrs=None):
        monaco_attrs = {b'monaco-editor': b'true', 
           b'data-language': b'json', 
           b'data-wordwrap': b'on', 
           b'data-minimap': b'false'}
        monaco_attrs.update(attrs)
        output = super(MonacoEditorWidget, self).render(name, value, monaco_attrs)
        return output

    class Media:
        css = {b'all': ('monaco.custom.css', )}
        js = ('monaco/loader.js', 'monaco.config.js')