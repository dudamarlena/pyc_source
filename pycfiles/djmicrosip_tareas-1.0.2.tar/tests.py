# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_tareas\djmicrosip_tareas\tests.py
# Compiled at: 2020-01-17 20:06:16
from django.test import TestCase
from microsip_api.comun.sic_db import first_or_none
from datetime import datetime, timedelta
from . import models

class ProgrammedTaskTests(TestCase):

    def setUp(self):
        models.ProgrammedTask.objects.all().delete()
        models.ProgrammedTask.objects.create(description='Mail Saldos Automaticos', command_type='http', command='http://127.0.0.1:8001/mail/saldos/todos_automatico/', period_start_datetime=datetime.now(), period_quantity=1, period_unit='dia')

    def test_progremmedtask_is_created(self):
        task = first_or_none(models.ProgrammedTask.objects.filter(description='Mail Saldos Automaticos'))
        self.assertIsNotNone(task, msg='No se encontro la tarea por crear')

    def test_next_execution_is_not_none(self):
        task = first_or_none(models.ProgrammedTask.objects.filter(description='Mail Saldos Automaticos'))
        self.assertIsNotNone(task.next_execution, msg='No se calcula la siguiente ejecucion al crear la tarea')