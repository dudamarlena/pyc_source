# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Bucket/projects/tinymce/gu-django-tinymce/tinymce/models.py
# Compiled at: 2016-04-21 01:35:09
from django.db import models
from django.contrib.admin import widgets as admin_widgets
from tinymce import widgets as tinymce_widgets
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^tinymce\\.models\\.HTMLField'])
except ImportError:
    pass

class HTMLField(models.TextField):
    """
    A large string field for HTML content. It uses the TinyMCE widget in
    forms.
    """

    def formfield(self, **kwargs):
        defaults = {'widget': tinymce_widgets.TinyMCE}
        defaults.update(kwargs)
        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = tinymce_widgets.AdminTinyMCE
        return super(HTMLField, self).formfield(**defaults)