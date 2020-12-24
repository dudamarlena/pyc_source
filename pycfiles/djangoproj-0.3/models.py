# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\FilePkl\latihan_django\11agustus\djangoproj\form\models.py
# Compiled at: 2014-08-18 00:42:35
from django.db import models
import datetime

class ContactForm(models.Model):
    Nama = models.CharField(max_length=50)
    Email = models.EmailField(max_length=100)
    Tanggal = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)

    def __unicode__(self):
        return self.Email


class Meta:
    ordering = [
     '-Tanggal']