# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/management/commands/backfill_api_keys.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import print_function
from __future__ import unicode_literals
from django.core.management.base import NoArgsCommand
from tastypie.compat import get_user_model
from tastypie.models import ApiKey

class Command(NoArgsCommand):
    help = b"Goes through all users and adds API keys for any that don't have one."

    def handle_noargs(self, **options):
        """Goes through all users and adds API keys for any that don't have one."""
        self.verbosity = int(options.get(b'verbosity', 1))
        User = get_user_model()
        for user in User.objects.all().iterator():
            try:
                api_key = ApiKey.objects.get(user=user)
                if not api_key.key:
                    api_key.save()
                    if self.verbosity >= 1:
                        print(b"Generated a new key for '%s'" % user.username)
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)
                if self.verbosity >= 1:
                    print(b"Created a new key for '%s'" % user.username)