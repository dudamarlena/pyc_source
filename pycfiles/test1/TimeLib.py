# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\TimeLib.py
# Compiled at: 2005-11-07 15:02:05
import re
try:
    from datetime import time, datetime
except:
    pass

DATETIME_PAT = re.compile('\n    (?P<year>\\d{4,4})\n    (?:\n        -\n        (?P<month>\\d{1,2})\n        (?:\n            -\n            (?P<day>\\d{1,2})\n            (?:\n                T\n                (?P<hour>\\d{1,2})\n                :\n                (?P<minute>\\d{1,2})\n                (?:\n                    :\n                    (?P<second>\\d{1,2})\n                    (?:\n                        \\.\n                        (?P<fract_second>\\d+)?\n                    )?\n                )?\n                (?:\n                    Z\n                    |\n                    (?:\n                        (?P<tz_sign>[+-])\n                        (?P<tz_hour>\\d{1,2})\n                        :\n                        (?P<tz_min>\\d{2,2})\n                    )\n                )\n            )?\n        )?\n    )?\n$', re.VERBOSE)
TIME_PAT = re.compile('\n                (?P<hour>\\d{1,2})\n                :\n                (?P<minute>\\d{1,2})\n                (?:\n                    :\n                    (?P<second>\\d{1,2})\n                    (?:\n                        \\.\n                        (?P<fract_second>\\d+)?\n                    )?\n                )?\n                (?:\n                    Z\n                    |\n                    (?:\n                        (?P<tz_sign>[+-])\n                        (?P<tz_hour>\\d{1,2})\n                        :\n                        (?P<tz_min>\\d{2,2})\n                    )\n                )\n$', re.VERBOSE)

def parse_isodate(st):
    """
    st - string or Unicode with ISO 8601 date
    """
    m = DATETIME_PAT.match(st)
    if not m:
        return None
    gd = m.groupdict('0')
    dt = datetime(int(gd['year']), int(gd['month']) or 1, int(gd['day']) or 1, int(gd['hour']), int(gd['minute']), int(gd['second']), int(float('.' + gd['fract_second']) * 1000000))
    return dt
    return


def parse_isotime(st):
    """
    st - string or Unicode with ISO 8601 time
    """
    m = TIME_PAT.match(st)
    if not m:
        return None
    gd = m.groupdict('0')
    t = time(int(gd['hour']), int(gd['minute']), int(gd['second']), int(float('.' + gd['fract_second']) * 1000000))
    return t
    return