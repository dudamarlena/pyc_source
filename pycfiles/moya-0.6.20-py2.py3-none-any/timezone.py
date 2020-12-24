# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/timezone.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
import pytz
from .context.expressiontime import ExpressionDateTime
from .compat import implements_to_string, text_type, string_types
from tzlocal import get_localzone
common_timezones = pytz.common_timezones

def _make_choice(t):
    return (
     t, t.replace(b'_', b' ').replace(b'/', b' / '))


common_timezones_choices = [ _make_choice(t) for t in common_timezones ]

def get_common_timezones_groups():
    regions = []
    region_map = {}
    for tz in common_timezones:
        if b'/' in tz:
            region, label = tz.split(b'/', 1)
        else:
            region = b''
            label = tz
        if region not in region_map:
            regions.append(region)
            region_map[region] = []
        region_map[region].append((tz, label.replace(b'_', b' ').replace(b'/', b' / ')))

    regions.sort()
    return [ (r, region_map[r]) for r in regions ]


def write_common_timezones(path):
    from json import dump
    import io
    with io.open(path, b'wb') as (f):
        dump(get_common_timezones_groups(), f)


@implements_to_string
class Timezone(object):

    def __init__(self, tz=b'UTC'):
        if isinstance(tz, Timezone):
            self.tz = tz.tz
        elif tz == b'auto':
            self.tz = get_localzone()
        else:
            self.tz = pytz.timezone(tz or b'UTC')

    def __str__(self):
        return text_type(self.tz.zone)

    def __repr__(self):
        return (b'<timezone "{}">').format(self.tz.zone)

    def __moyafilter__(self, context, app, dt, params):
        if isinstance(dt, string_types):
            dt = ExpressionDateTime.from_isoformat(dt)
        return self(dt)

    def __call__(self, dt):
        if dt.tzinfo is None:
            dt = pytz.UTC.localize(dt)
        return dt.astimezone(self.tz)


if __name__ == b'__main__':
    from datetime import datetime
    t = datetime.utcnow()
    tz = Timezone(b'Asia/Seoul')
    print(repr(tz))
    print(text_type(tz))
    print(tz(t))