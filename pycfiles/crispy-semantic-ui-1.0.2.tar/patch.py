# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/projects/vk-board/src/semantic_ui/patch.py
# Compiled at: 2015-05-23 18:35:42
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