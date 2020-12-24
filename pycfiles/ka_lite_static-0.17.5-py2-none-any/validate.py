# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/validate.py
# Compiled at: 2018-07-11 18:15:30
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = 'Validates all installed models.'
    requires_model_validation = False

    def handle_noargs(self, **options):
        self.validate(display_num_errors=True)