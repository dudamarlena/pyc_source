# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shimul/Projects/django-hyper-editor/hypereditor/apps.py
# Compiled at: 2019-04-07 12:41:03
# Size of source mod 2**32: 260 bytes
from django.apps import AppConfig
from hypereditor.utils import load_hyper_blocks

class HyperEditorConfig(AppConfig):
    name = 'hypereditor'

    def ready(self):
        super().ready()
        list(load_hyper_blocks())