# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/tinymce/models.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 915 bytes
from django.db import models
import django.contrib.admin as admin_widgets
import tendenci.libs.tinymce as tinymce_widgets
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^tinymce\\.models\\.HTMLField'])
except ImportError:
    pass

class HTMLField(models.TextField):
    __doc__ = '\n    A large string field for HTML content. It uses the TinyMCE widget in\n    forms.\n    '

    def formfield(self, **kwargs):
        defaults = {'widget': tinymce_widgets.TinyMCE}
        defaults.update(kwargs)
        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = tinymce_widgets.AdminTinyMCE
        return (super(HTMLField, self).formfield)(**defaults)