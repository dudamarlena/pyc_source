# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/json.py
# Compiled at: 2015-02-05 18:27:28
import datetime, decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import is_aware
try:
    from moneyed import Money
except ImportError:
    Money = None

try:
    from money.Money import Money as OldMoney
except ImportError:
    OldMoney = None

class JSONEncoder(DjangoJSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        if isinstance(o, datetime.date):
            return o.isoformat()
        else:
            if isinstance(o, datetime.time):
                if is_aware(o):
                    raise ValueError("JSON can't represent timezone-aware times.")
                r = o.isoformat()
                if o.microsecond:
                    r = r[:12]
                return r
            if isinstance(o, decimal.Decimal):
                return str(o)
            if isinstance(o, datetime.timedelta):
                value = abs(o)
                return value.days * 24 * 3600 * 1000000 + value.seconds * 1000000 + value.microseconds
            if Money is not None and isinstance(o, Money) or OldMoney is not None and isinstance(o, OldMoney):
                return '%s' % o
            return super(DjangoJSONEncoder, self).default(o)
            return