# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/extensions/management/commands/list-extensions.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.models import RegisteredExtension

class Command(BaseCommand):
    help = _(b'Lists available Review Board extensions.')
    option_list = BaseCommand.option_list + (
     make_option(b'--enabled', action=b'store_true', default=False, dest=b'list_enabled', help=_(b'List only enabled extensions')),)

    def handle(self, *args, **options):
        extensions = RegisteredExtension.objects.all()
        if options[b'list_enabled']:
            extensions = extensions.filter(enabled=True)
        for extension in extensions:
            self.stdout.write(_(b'* Name: %s\n') % extension.name)
            if extension.enabled:
                self.stdout.write(_(b'  Status: enabled\n'))
            else:
                self.stdout.write(_(b'  Status: disabled\n'))
            self.stdout.write(_(b'  ID: %s\n') % extension.class_name)
            self.stdout.write(b'\n')