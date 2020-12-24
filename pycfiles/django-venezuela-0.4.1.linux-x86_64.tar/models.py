# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/envs/programa_amigos/lib/python2.7/site-packages/venezuela/models.py
# Compiled at: 2014-01-23 11:32:07
from django.db import models

class Estado(models.Model):
    estado = models.CharField(max_length=50)
    iso_3166_2 = models.CharField(max_length=5)

    def __unicode__(self):
        return self.estado

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'


class Ciudad(models.Model):
    estado = models.ForeignKey('Estado')
    ciudad = models.CharField(max_length=100)
    capital = models.IntegerField(default=0)

    def __unicode__(self):
        return self.ciudad

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'


class Municipio(models.Model):
    estado = models.ForeignKey('Estado')
    municipio = models.CharField(max_length=100)

    def __unicode__(self):
        return self.municipio

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'


class Parroquia(models.Model):
    municipio = models.ForeignKey('Municipio')
    parroquia = models.CharField(max_length=100)

    def __unicode__(self):
        return self.parroquia

    class Meta:
        verbose_name = 'Parroquía'
        verbose_name_plural = 'Parroquías'