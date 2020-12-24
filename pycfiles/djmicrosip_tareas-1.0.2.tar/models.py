# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_tareas\djmicrosip_tareas\models.py
# Compiled at: 2020-01-17 20:06:16
from django.db import models
from datetime import datetime, timedelta
from monthdelta import monthdelta

class ProgrammedTask(models.Model):
    description = models.CharField('Descripción', max_length=400)
    TYPES = (('http', 'http'), ('cmd', 'cmd'))
    command_type = models.CharField('Tipo de comando', default='http', max_length=10, choices=TYPES)
    command = models.CharField('Comando', max_length=200)
    period_start_datetime = models.DateTimeField('Inicio')
    period_end_datetime = models.DateTimeField('Fin', blank=True, null=True)
    period_quantity = models.IntegerField('Cantidad')
    UNIT_CHOICES = (
     ('minutes', 'Minuto(s)'), ('hours', 'Hora(s)'), ('days', 'Día(s)'), ('weeks', 'Semana(s)'), ('months', 'Mes(es)'), ('years', 'Año(s)'))
    period_unit = models.CharField('Unidades', default='dia', max_length=10, choices=UNIT_CHOICES)
    STATES = (
     ('Activo', 'Activo'), ('En proceso', 'enproceso'), ('Inactivo', 'inactivo'))
    status = models.CharField(max_length=10, default='Activo', choices=STATES)
    next_execution = models.DateTimeField(blank=True, null=True)
    last_execution = models.DateTimeField(blank=True, null=True)

    def get_next_execution(self):
        """
        Calcula la siguiente ejecucion al guardar
        """
        _next_execution = self.period_start_datetime
        _now = datetime.now()
        _increment = self.period_quantity
        while _next_execution < _now and self.next_execution:
            if self.period_unit == 'minutes':
                _next_execution += timedelta(minutes=_increment)
            elif self.period_unit == 'hours':
                _next_execution += timedelta(hours=_increment)
            elif self.period_unit == 'days':
                _next_execution += timedelta(days=_increment)
            elif self.period_unit == 'weeks':
                _next_execution += timedelta(days=_increment * 7)
            elif self.period_unit == 'months':
                _next_execution += monthdelta(_increment)
            elif self.period_unit == 'years':
                _next_execution += timedelta(years=_increment)

        return _next_execution

    def save(self, *args, **kwargs):
        """
        Si no existe siguiente ejecucion o se cambia la fecha de inicio
        se calcula de nuevo.
        """
        if self.period_end_datetime == '':
            self.period_end_datetime = None
        self.next_execution = self.get_next_execution()
        super(ProgrammedTask, self).save(*args, **kwargs)
        return

    class Meta:
        db_table = 'SIC_PROGRAMMEDTASK'
        app_label = 'models_base'


class PendingTask(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30)
    APPS = (('sms', 'SMS'), ('correo', 'Correo'), ('Poliza', 'Poliza'))
    app = models.CharField(choices=APPS, max_length=30)
    parameters = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    intents = models.IntegerField(default=0)

    class Meta:
        db_table = 'SIC_PENDINGTASK'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.id