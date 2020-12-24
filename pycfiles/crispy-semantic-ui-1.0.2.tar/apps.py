# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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