# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yuji/Projects/Stimson/stimson_project/env/lib/python2.7/site-packages/cleditor/widgets.py
# Compiled at: 2012-01-25 21:01:14
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils import simplejson
from django.middleware.csrf import get_token
from django.core.exceptions import ImproperlyConfigured
from django.forms.util import flatatt

class CLEditorWidget(forms.Textarea):
    """
    Widget providing CLEditor for Rich Text Editing.
    Supports direct image uploads and embed.
    """

    class Media:
        js = [
         'cleditor/jquery.cookie.js',
         'cleditor/jquery.cleditor.min.js']
        css = {'all': ('cleditor/jquery.cleditor.css', )}

    def __init__(self, config_name='default', upload=False, *args, **kwargs):
        self.upload = upload
        super(CLEditorWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(('<textarea{flat_attrs}>{value}</textarea>\n        <script type="text/javascript">\n            django.jQuery("#{id}").cleditor();\n        </script>').format(flat_attrs=flatatt(final_attrs), value=value, id=final_attrs.get('id')))


class CLEditorUploadWidget(CLEditorWidget):

    class Media:
        js = [
         'cleditor/jquery.cookie.js',
         'cleditor/jquery.cleditor.min.js',
         'cleditor/jquery.cleditor.extimage.js']
        css = {'all': ('cleditor/jquery.cleditor.css', )}