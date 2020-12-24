# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thomas/Dev/Project/django-trusts/trusts/management/commands/create_trust_root.py
# Compiled at: 2016-04-16 22:35:57
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings

def create_root_trust(Trust, pk, settlor, title):
    kwargs = {b'id': pk, b'title': title}
    if settlor is not None:
        kwargs.update({b'settlor_id': settlor})
    trust = Trust(**kwargs)
    trust.trust = trust
    trust.save()
    return


class Command(BaseCommand):
    help = b'Create a self-referencing trust as the root of all trust.'

    def handle(self, **options):
        self.verbosity = int(options.get(b'verbosity', 1))
        pk = getattr(settings, b'TRUSTS_ROOT_PK', 1)
        settlor = getattr(settings, b'TRUSTS_ROOT_SETTLOR', None)
        title = getattr(settings, b'TRUSTS_ROOT_TITLE', b'In Trust We Trust')
        if b'apps' in options:
            apps = options[b'apps']
            Trust = apps.get_model(b'trusts', b'trust')
        else:
            from trusts.models import Trust
        create_root_trust(Trust, pk, settlor, title)
        return