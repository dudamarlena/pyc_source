# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gabriel.faleiro/.virtualenvs/test_save/saveall/saveall/tests/test_command.py
# Compiled at: 2016-03-11 14:42:32
from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command
from saveall.models import Table01, Table02, Table03

class CommandsTest(TestCase):

    def setUp(self):
        self.out = StringIO()
        p1 = Table01.objects.create(nome='row01tb01')
        r1 = Table02.objects.create(nome='row01tb02')
        Table03.objects.create(nome='row01tb03', dono=p1, raca=r1)

    def test_saveall_command(self):
        call_command('saveall', 'saveall.Table01', stdout=self.out)
        self.assertIn('All instances saved.', self.out.getvalue())

    def test_saveall_command_all_option(self):
        call_command('saveall', all=True, stdout=self.out)
        self.assertIn('All instances from all models saved.', self.out.getvalue())

    def test_saveall_command_app_option(self):
        call_command('saveall', app=['saveall'], stdout=self.out)
        self.assertIn('All instances from all models in "saveall" saved.', self.out.getvalue())

    def test_saveall_command_app_option_doesnt_exist(self):
        call_command('saveall', app=['aeho'], stdout=self.out)
        self.assertIn("Can't find 'aeho' app.", self.out.getvalue())

    def test_saveall_command_multiple_models(self):
        call_command('saveall', 'saveall.Table01', 'saveall.Table02', stdout=self.out)
        self.assertIn('All instances saved.', self.out.getvalue())

    def test_saveall_command_table_doesnt_exist(self):
        call_command('saveall', 'saveall.wrongtable', stdout=self.out)
        self.assertIn("Can't find 'saveall.wrongtable' model.", self.out.getvalue())