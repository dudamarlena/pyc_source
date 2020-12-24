# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alex/projects/showmore/venv3/lib/python3.4/site-packages/semantic_ui/apps.py
# Compiled at: 2015-08-08 14:59:20
# Size of source mod 2**32: 262 bytes
from django.apps import AppConfig

class SemanticUIConfig(AppConfig):
    name = 'semantic_ui'
    verbose_name = 'semantic_ui'

    def ready(self):
        super(SemanticUIConfig, self).ready()
        from semantic_ui import patch
        patch.patch_all()