# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/uptime.py
# Compiled at: 2019-05-16 13:41:33
"""
Uptime - command ``/usr/bin/uptime``
====================================

Parse the output of the ``uptime`` command into six attributes:

* ``currtime``: the time on the system as a string.
* ``loadavg``: a three element array of strings for the one, five and
  fifteen minute load averages.
* ``updays``: a string of the number of days the system has been up, or ''
  if the system has been running for less than a day.
* ``uphhmm``: a string of the fraction of a day in hours and minutes that the
  system has been running.  Times reported by ``uptime`` as e.g. '30 mins' are
  converted in to hh:mm format.
* ``users``: a string containing the number of users ``uptime`` reports as
  using the system.
* ``uptime``: a ``datetime.timedelta`` object of the total duration of uptime.

These can also be queried as named keys in the ``data`` attribute.

Sample output::

     11:51:06 up  3:17,  1 user,  load average: 0.12, 0.20, 0.28

Examples:
    >>> uptime = shared[Uptime]
    >>> from datetime import timedelta
    >>> uptime.uptime > timedelta(days=1)
    False
    >>> uptime.updays
    ''
    >>> uptime.users
    '1'
    >>> uptime.loadavg[1]
    '0.20'
    >>> uptime.data['currtime']
    '11:51:06'
"""
import re, datetime
from .. import parser, CommandParser
from insights.parsers import ParseException
from insights.specs import Specs

@parser(Specs.uptime)
class Uptime(CommandParser):
    """Parser class to parse the output of ``uptime``."""

    def parse_content(self, content):
        self.currtime = None
        self.loadavg = None
        self.updays = None
        self.uphhmm = None
        self.users = None
        self.uptime = None
        uptime_info = {}
        self.data = uptime_info
        line = content[0].strip()
        curr_time_re = '(?P<currtime>\\d\\d:\\d\\d:\\d\\d)'
        duration_re = ' up  ?(?:(?P<days>\\d+) days?)?(?:, )?' + '(?:(?:(?P<mins>\\d+) mins?)?|(?: ?(?P<hhmm>\\d?\\d:\\d\\d)))'
        users_re = ',  ?(?P<users>\\d+) users?'
        load_re = ',  ?load average: (?P<load1>\\d+.\\d\\d), (?P<load5>\\d+.\\d\\d), (?P<load15>\\d+.\\d\\d)'
        line_rex = re.compile(curr_time_re + duration_re + users_re + load_re)
        match = line_rex.search(line)
        if not match:
            raise ParseException(("No uptime data found on '{line}'").format(line=line))
        uptime_info['updays'] = match.group('days') if match.group('days') else ''
        uptime_info['currtime'] = match.group('currtime')
        uptime_info['uphhmm'] = match.group('hhmm') if match.group('hhmm') else ''
        uptime_info['users'] = match.group('users')
        uptime_info['loadavg'] = [match.group('load1'), match.group('load5'), match.group('load15')]
        uptime_info['uptime'] = datetime.timedelta()
        if not match.group('hhmm') and match.group('mins'):
            uptime_info['uphhmm'] = ('00:{m:02}').format(m=int(match.group('mins')))
        if uptime_info['uphhmm']:
            hours, mins = uptime_info['uphhmm'].split(':')
            uptime_info['uptime'] += datetime.timedelta(hours=int(hours), minutes=int(mins))
        if uptime_info['updays']:
            uptime_info['uptime'] += datetime.timedelta(days=int(uptime_info['updays']))
        for k, v in uptime_info.items():
            setattr(self, k, v)

        self.data = uptime_info
        return