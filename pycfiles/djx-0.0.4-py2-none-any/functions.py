# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/backends/oracle/functions.py
# Compiled at: 2019-02-14 00:35:17
from django.db.models import DecimalField, DurationField, Func

class IntervalToSeconds(Func):
    function = ''
    template = '\n    EXTRACT(day from %(expressions)s) * 86400 +\n    EXTRACT(hour from %(expressions)s) * 3600 +\n    EXTRACT(minute from %(expressions)s) * 60 +\n    EXTRACT(second from %(expressions)s)\n    '

    def __init__(self, expression, **extra):
        output_field = extra.pop('output_field', DecimalField())
        super(IntervalToSeconds, self).__init__(expression, output_field=output_field, **extra)


class SecondsToInterval(Func):
    function = 'NUMTODSINTERVAL'
    template = "%(function)s(%(expressions)s, 'SECOND')"

    def __init__(self, expression, **extra):
        output_field = extra.pop('output_field', DurationField())
        super(SecondsToInterval, self).__init__(expression, output_field=output_field, **extra)