# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/base_models/widgets.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 319 bytes
from django import forms

class Markdown(forms.Textarea):

    class Media:
        css = {'all': ('editor/editor.css', 'editor/vendor/icomoon/style.css')}
        js = ('editor/editor.js', 'editor/marked.js')