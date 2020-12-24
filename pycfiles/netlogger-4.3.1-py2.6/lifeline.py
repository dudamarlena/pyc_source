# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/lifeline.py
# Compiled at: 2010-06-10 19:40:52
"""
Produce a batch file for plotting a lifeline from a netlogger log.
Supported output formats are R (eventually!) and gnuplot.
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__rcsid__ = '$Id: lifeline.py 23923 2009-09-18 22:42:26Z ksb $'
from netlogger.parsers.base import TS_FIELD, EVENT_FIELD, NLFastParser
from netlogger.nllog import DoesLogging

class LifelineSet(DoesLogging):
    """Set of lifelines with different identifiers.
    """

    def __init__(self, events=None, lineids=None, groupids=None, prefix=''):
        DoesLogging.__init__(self)
        self.events = dict.fromkeys(events)
        self.event_pos = events
        self.lineids, self.groupids = lineids, groupids
        self.event_prefix, self.event_prefix_len = prefix, len(prefix)
        self.lifelines = []
        self._count = 0

    def process(self, record):
        """Process a record (dictionary) and, potentially, return a lifeline
        """
        self._count += 1
        r = None
        try:
            r = self._process(record)
        except KeyError, E:
            self.log.warn('process.record.missing_attribute', n=self._count, attr__name=E)
        except ValueError, E:
            self.log.warn('process.error.bad_value', n=self._count, msg=E)

        return r

    def _process(self, record):
        result = None
        event = record[EVENT_FIELD]
        if self.event_prefix:
            if event.startswith(self.event_prefix):
                event = event[self.event_prefix_len:]
            if self.events.has_key(event):
                pos = self.event_pos.index(event)
                tmp = []
                for key in self.lineids:
                    if not record.has_key(key):
                        raise ValueError("missing line-id key '%s'" % key)
                    tmp.append(record[key])

                record_lineid = tuple(tmp)
                tmp = []
                for key in self.groupids:
                    if not record.has_key(key):
                        raise ValueError("missing group-id key '%s'" % key)
                    tmp.append(record[key])

                record_groupid = tuple(tmp)
                matched = False
                for (i, lifeline) in enumerate(self.lifelines):
                    if lifeline.lineid == record_lineid:
                        if lifeline.groupid != record_groupid:
                            raise ValueError('same lineid, different group')
                        if lifeline.times[pos] is None:
                            lifeline.setTime(pos, float(record[TS_FIELD]))
                        else:
                            result = lifeline
                            lifeline = Lifeline(record_lineid, record_groupid, len(self.events))
                            lifeline.setTime(pos, float(record[TS_FIELD]))
                            self.lifelines.append(lifeline)
                            self.lifelines = self.lifelines[:i] + self.lifelines[i + 1:]
                        matched = True
                        break

                lifeline = matched or Lifeline(record_lineid, record_groupid, len(self.events))
                lifeline.setTime(pos, float(record[TS_FIELD]))
                self.lifelines.append(lifeline)
        return result


class Lifeline:

    def __init__(self, lineid, groupid, n):
        self.lineid = lineid
        self.groupid = groupid
        self.times = []
        for i in xrange(n):
            self.times.append(None)

        return

    def setTime(self, pos, t):
        self.times[pos] = t