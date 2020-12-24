# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/hoerapi.py/venv/lib/python3.5/site-packages/hoerapi/util.py
# Compiled at: 2015-11-05 07:03:05
# Size of source mod 2**32: 797 bytes
from datetime import datetime
from iso8601 import parse_date as parse_isodate
from pytz import timezone
DefaultZone = timezone('Europe/Berlin')

def parse_date(val):
    val = parse_isodate(val, DefaultZone)
    if val.tzinfo != DefaultZone:
        return val
    val = datetime.combine(val.date(), val.time())
    return DefaultZone.localize(val)


def parse_bool(str):
    if str == '1':
        return True
    else:
        return False


class CommonEqualityMixin(object):

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)