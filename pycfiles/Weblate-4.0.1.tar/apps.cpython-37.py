# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nijel/weblate/weblate/weblate/fonts/apps.py
# Compiled at: 2020-03-12 04:44:12
# Size of source mod 2**32: 1061 bytes
from django.apps import AppConfig
from django.core.checks import register
from weblate.fonts.utils import check_fonts

class FontsConfig(AppConfig):
    name = 'weblate.fonts'
    label = 'fonts'
    verbose_name = 'Fonts'

    def ready(self):
        super().ready()
        register(check_fonts)