# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gabriel.faleiro/.virtualenvs/test_save/saveall/saveall/tests/test_models.py
# Compiled at: 2016-03-14 10:28:06
from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command
from models import Table01, Table02, Table03

class ModelsIntegrityTest(TestCase):

    def setUp(self):
        self.out = StringIO()
        p1 = Table01.objects.create(nome='row01tb01')
        r1 = Table02.objects.create(nome='row01tb02')
        Table03.objects.create(nome='row01tb03', dono=p1, raca=r1)

    def test_integrity_saveall_command_create_update_datetime(self):
        created = Table01.objects.filter(pk=1).values('created')[0]['created']
        old_updated = Table01.objects.filter(pk=1).values('updated')[0]['updated']
        call_command('saveall', 'saveall.Table01', stdout=self.out)
        new_created = Table01.objects.filter(pk=1).values('created')[0]['created']
        new_updated = Table01.objects.filter(pk=1).values('updated')[0]['updated']
        self.assertNotEqual(old_updated, new_updated)
        self.assertEqual(created, new_created)