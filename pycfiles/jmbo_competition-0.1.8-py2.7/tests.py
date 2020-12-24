# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/competition/tests.py
# Compiled at: 2013-09-27 03:42:43
from datetime import timedelta
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from foundry.models import Member
from competition.models import Competition, CompetitionEntry

class CompetitionTestCase(TestCase):

    def test_entry_export(self):
        comp = Competition.objects.create(title='Test Comp', start_date=timezone.now(), end_date=timezone.now() + timedelta(hours=1))
        member = Member(username='john123')
        member.first_name = member.username
        member.set_password('password')
        member.is_staff = True
        member.save()
        CompetitionEntry.objects.create(competition=comp, user=member)
        self.client.login(username=member.username, password='password')
        response = self.client.get(reverse('admin:competition-csv-export'))
        self.assertContains(response, member.username)
        self.assertNotContains(response, 'None')