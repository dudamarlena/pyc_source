# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/siteconfig/management/commands/list-siteconfig.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import json
from django.core.management.base import BaseCommand
from djblets.siteconfig.models import SiteConfiguration

class Command(BaseCommand):
    """Lists the site configuration."""

    def handle(self, *args, **options):
        siteconfig = SiteConfiguration.objects.get_current()
        self.stdout.write(json.dumps(siteconfig.settings, indent=2))