# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tigorc/repo/django-redactorjs/redactor/widgets.py
# Compiled at: 2018-10-30 10:19:47
import json
from django.forms import widgets
from django.utils.safestring import mark_safe
try:
    from django.core.urlresolvers import reverse
except ModuleNotFoundError:
    from django.urls import reverse

from django.conf import settings
GLOBAL_OPTIONS = getattr(settings, 'REDACTOR_OPTIONS', {})
REDACTOR_CSS = getattr(settings, 'REDACTOR_CSS', {})
REDACTOR_JS = getattr(settings, 'REDACTOR_JS', [])
INIT_JS = '<script type="text/javascript">\n    (function($){\n        $("#%s").redactor(%s);\n    })(jQuery || django.jQuery);\n    </script>\n    '

class RedactorEditor(widgets.Textarea):

    class Media:
        js = REDACTOR_JS
        css = REDACTOR_CSS

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.custom_options = kwargs.pop('redactor_options', {})
        self.Media.css['all'] = self.Media.css.get('all', ()) + ('redactor/css/django_admin.css', )
        super(RedactorEditor, self).__init__(*args, **kwargs)

    def get_upload_params(self):
        kwargs = {'upload_to': self.upload_to}
        return {'imageUpload': reverse('redactor_upload_image', kwargs=kwargs), 
           'fileUpload': reverse('redactor_upload_file', kwargs=kwargs)}

    def get_options(self):
        options = GLOBAL_OPTIONS.copy()
        options.update(self.get_upload_params())
        options.update(self.custom_options)
        return json.dumps(options)

    def render(self, name, value, renderer=None, attrs=None):
        html = super(RedactorEditor, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        html += INIT_JS % (id_, self.get_options())
        return mark_safe(html)