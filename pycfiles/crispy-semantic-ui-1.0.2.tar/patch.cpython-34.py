# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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