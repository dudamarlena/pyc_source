# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mikhail/.virtualenvs/django-robokassa/lib/python3.5/site-packages/robokassa/models.py
# Compiled at: 2018-04-26 06:48:34
# Size of source mod 2**32: 785 bytes
from __future__ import unicode_literals
from django.db import models
from django.utils.six import python_2_unicode_compatible

@python_2_unicode_compatible
class SuccessNotification(models.Model):
    InvId = models.IntegerField('Номер заказа', db_index=True)
    OutSum = models.CharField('Сумма', max_length=15)
    created_at = models.DateTimeField('Дата и время получения уведомления', auto_now_add=True)

    class Meta:
        verbose_name = 'Уведомление об успешном платеже'
        verbose_name_plural = 'Уведомления об успешных платежах (ROBOKASSA)'

    def __str__(self):
        return '#{}: {} ({})'.format(self.InvId, self.OutSum, self.created_at)