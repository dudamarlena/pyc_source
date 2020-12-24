# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/management/commands/jmbo_publish.py
# Compiled at: 2017-05-03 05:57:29
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from jmbo.models import ModelBase

class Command(BaseCommand):
    help = 'Publish or unpublish Jmbo objects.'

    @transaction.atomic
    def handle(self, *args, **options):
        now = timezone.now()
        q1 = Q(publish_on__lte=now, retract_on__isnull=True)
        q2 = Q(publish_on__lte=now, retract_on__gt=now)
        ModelBase.objects.filter(state='unpublished').filter(q1 | q2).update(state='published')
        ModelBase.objects.filter(state='published').filter(retract_on__lte=now).update(state='unpublished')