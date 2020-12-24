# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vivek/Projects/djingles/src/djingles/apps.py
# Compiled at: 2018-04-18 13:19:32
# Size of source mod 2**32: 346 bytes
from django.apps import AppConfig

class DjinglesConfig(AppConfig):
    name = 'djingles'

    def ready(self):
        self.scan_jinja_tags()

    def scan_jinja_tags(self):
        from djingles import utils
        from djingles.jinja2 import filters, functions
        for module in utils.iter_app_modules('jinja2globals'):
            pass