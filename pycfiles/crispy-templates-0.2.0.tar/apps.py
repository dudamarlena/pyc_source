# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alex/projects/vk-board/src/semantic_ui/apps.py
# Compiled at: 2015-05-23 18:35:42
from django.conf import settings
from django.apps import AppConfig

class SemanticUIConfig(AppConfig):
    name = 'semantic_ui'
    verbose_name = 'semantic_ui'

    def ready(self):
        super(SemanticUIConfig, self).ready()
        from semantic_ui import patch
        patch.patch_all()