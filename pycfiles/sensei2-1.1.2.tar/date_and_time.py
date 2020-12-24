# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/xacce/addit/Projects/inventory/venv/src/sensei2/sensei2/sensei/handlers/date_and_time.py
# Compiled at: 2015-10-16 10:22:04
from random import randint
from django.db import models
from django.utils.timezone import utc
from django.utils.datetime_safe import datetime
from sensei2.sensei.handlers.base import BaseHandler

class DateTimeFieldHandler(BaseHandler):

    def __init__(self):
        super(DateTimeFieldHandler, self).__init__()
        self.handled_class = models.DateTimeField

    def prepare_value(self, obj, field, sensei):
        return datetime.today().replace(tzinfo=utc, year=randint(2000, 2015), month=randint(1, 12), day=randint(1, 28), hour=randint(0, 23), minute=randint(1, 59))


class DateFieldHandler(BaseHandler):

    def __init__(self):
        super(DateFieldHandler, self).__init__()
        self.handled_class = models.DateField

    def prepare_value(self, obj, field, sensei):
        return datetime.today().replace(tzinfo=utc, year=randint(2000, 2015), month=randint(1, 12), day=randint(1, 28), hour=randint(0, 23), minute=randint(1, 59))


class TimeFieldHandler(BaseHandler):

    def __init__(self):
        super(TimeFieldHandler, self).__init__()
        self.handled_class = models.TimeField

    def prepare_value(self, obj, field, sensei):
        return datetime.today().replace(tzinfo=utc, hour=randint(1, 23), minute=randint(1, 59)).time()