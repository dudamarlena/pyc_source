# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/siyuan/projects/django-simplemde/testproject/simplemde/fields.py
# Compiled at: 2018-01-17 09:49:38
# Size of source mod 2**32: 912 bytes
from django.db.models import TextField
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from .widgets import SimpleMDEEditor

class SimpleMDEField(TextField):

    def __init__(self, *args, **kwargs):
        options = kwargs.pop('simplemde_options', {})
        self.widget = SimpleMDEEditor(simplemde_options=options)
        (super(SimpleMDEField, self).__init__)(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = self.widget
        return (super(SimpleMDEField, self).formfield)(**defaults)


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^simplemde\\.fields\\.SimpleMDEField'])