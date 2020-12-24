# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alex/projects/showmore/venv3/lib/python3.4/site-packages/semantic_ui/patch.py
# Compiled at: 2015-08-08 14:59:20
# Size of source mod 2**32: 384 bytes
from django.conf import settings
from crispy_forms import layout

def patch_all():
    if settings.CRISPY_TEMPLATE_PACK != 'semantic-ui':
        return
    layout.Submit.field_classes = 'ui primary button'
    layout.Button.field_classes = 'ui button'
    layout.Reset.field_classes = 'ui button'
    layout.Column.field_classes = 'column'
    layout.Field.field_classes = 'field'