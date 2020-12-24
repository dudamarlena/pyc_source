# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-form-renderers/form_renderers/__init__.py
# Compiled at: 2017-01-04 10:04:06
from django.conf import settings
SETTINGS = {'enable-bem-classes': False, 'replace-as-p': False, 'replace-as-table': False}
try:
    SETTINGS.update(settings.FORM_RENDERERS)
except AttributeError:
    pass

def as_div(form):
    """This formatter arranges label, widget, help text and error messages by
    using divs."""
    form.error_css_class = 'Field-message--error'
    if SETTINGS['enable-bem-classes']:
        return form._html_output(normal_row='<div%(html_class_attr)s>%(label)s<div class="Field-item">%(errors)s %(field)s</div><div class="Field-message">%(help_text)s</div></div>', error_row='%s', row_ender='</div>', help_text_html='%s', errors_on_separate_row=False)
    else:
        return form._html_output(normal_row='<div class="field"><div %(html_class_attr)s>%(label)s %(errors)s %(field)s</div><div class="helptext">%(help_text)s</div></div>', error_row='%s', row_ender='</div>', help_text_html='%s', errors_on_separate_row=False)