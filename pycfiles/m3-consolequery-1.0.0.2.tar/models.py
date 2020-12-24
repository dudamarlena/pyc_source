# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/khalikov/projects/processing/src/processing/../env/m3_consolequery/models.py
# Compiled at: 2013-09-30 07:59:05
"""
Модуль содержит общие модели справочников и перечисления для всех подсистем МИС.
"""
from django.db import models

class CustomQueries(models.Model):
    """
    Справочник "Пользовательские запросы"
    """
    code = models.CharField(max_length=20, db_index=True, null=True, blank=True)
    name = models.CharField(max_length=200, db_index=True)
    query = models.TextField()

    class Meta:
        db_table = 'm3_conquery_customqueries'