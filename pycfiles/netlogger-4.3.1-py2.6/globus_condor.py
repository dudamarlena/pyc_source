# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/globus_condor.py
# Compiled at: 2009-12-08 17:43:28
"""
Parse logs from the log file currently called
globus-condor.log. These record Condor-G jobs.

Input Format
============
These consist of XML stanzas
<c>
  <a n="NAME1"><s|i|r>VALUE1</s|i|r>
  <a n="NAME1"><s|i|r>VALUE1</s|i|r>
  ...
</c>

Names/values in all stanzas:
---------------------------
 MyType: Name of event type
 EventTypeNumber: Number of event type
 Cluster: Cluster number
 Proc: Processor number
 Subproc: Sub-processor number

** Note **
----------
  Condor jobid = "%03d.%03d.%03d" % (Cluster, Proc, Subproc)

Sample:
------
<c>
<a n="MyType"><s>JobTerminatedEvent</s></a>
<a n="EventTypeNumber"><i>5</i></a>
<a n="MyType"><s>JobTerminatedEvent</s></a>
<a n="EventTime"><s>2008-02-06T16:45:10</s></a>
<a n="Cluster"><i>5</i></a>
<a n="Proc"><i>0</i></a>
<a n="Subproc"><i>0</i></a>
<a n="TerminatedNormally"><b v="t"/></a>
<a n="ReturnValue"><i>0</i></a>
<a n="RunLocalUsage"><s>Usr 0 00:00:00, Sys 0 00:00:00</s></a>
<a n="RunRemoteUsage"><s>Usr 0 00:00:00, Sys 0 00:00:00</s></a>
<a n="TotalLocalUsage"><s>Usr 0 00:00:00, Sys 0 00:00:00</s></a>
<a n="TotalRemoteUsage"><s>Usr 0 00:00:00, Sys 0 00:00:00</s></a>
<a n="SentBytes"><r>0.000000000000000E+00</r></a>
<a n="ReceivedBytes"><r>0.000000000000000E+00</r></a>
<a n="TotalSentBytes"><r>0.000000000000000E+00</r></a>
<a n="TotalReceivedBytes"><r>0.000000000000000E+00</r></a>
</c>
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: globus_condor.py 23616 2009-03-26 18:58:47Z dang $'
import re, time
from netlogger import nldate
from netlogger.parsers.base import BaseParser

class Parser(BaseParser):
    """Parse logs from the log file currently called
    globus-condor.log. These record Condor-G jobs.

    The logs are a series of XML fragments whose outer element is '<c>'.
    The information in each fragment includes an event type and name,
    and the Condor job id (split into constituent parts of 
    cluster.processor.jobid, plus (on the JobTerminated event) 
    other job statistics such as the return value, resource usage stats, 
    and bytes sent and received.
    """
    CE_PARAM = 'current_event'
    TZ_PARAM = 'timezone'
    FIELD_RE = re.compile('<a n="(\\w+)"><([a-z])>?([^<]*)</[a-z]>')
    HOST_RE = re.compile('(?:&lt;)?([0-9\\.]+)(?::(\\d+))?')
    DATE_FIELD_NAME = 'EventTime'
    EVENT_FIELD_NAME = 'MyType'
    IGNORE_FIELDS = ('EventTypeNumber', )
    IGNORE_FIELDS_DICT = dict.fromkeys(IGNORE_FIELDS)
    NAMESPACE = 'globus.condor'

    def __init__(self, f, **kwargs):
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)
        self._cur = None
        self._tzstr = None
        return

    def getParameters(self):
        """Get current values to persist.
        """
        return {self.CE_PARAM: self._cur, self.TZ_PARAM: self._tzstr}

    def setParameters(self, param):
        """Set parameters from persistent values.
        """
        self._cur = param[self.CE_PARAM]
        self._tzstr = param[self.TZ_PARAM]

    def _setTimestamp(self, value):
        """Set the 'ts' field in the current event to the
        timezone-appended value in 'value'.
        """
        if self._tzstr is None:
            self._tzstr = nldate.getLocaltimeISO(value)
        self._cur['ts'] = value + self._tzstr
        return

    def process(self, line):
        if not line:
            return ()
        else:
            result = ()
            tag_start = line[:2]
            if tag_start == '<c':
                if self._cur is None:
                    self._cur = {}
                else:
                    self._cur = {}
                    raise ValueError('premature start of record')
            elif tag_start == '</':
                if self._cur is None:
                    raise ValueError('unexpected end of record')
                elif self._cur == {}:
                    self._cur = None
                    raise ValueError('empty record')
                else:
                    if not self._cur.has_key('ts'):
                        self._cur = None
                        raise KeyError('missing event time')
                    try:
                        cluster, proc, subproc = self._cur['cluster'], self._cur['proc'], self._cur['subproc']
                    except (KeyError, ValueError):
                        self._cur = None
                        raise KeyError('Missing one or more of cluster, proc and subproc in: %s' % self._cur)
                    else:
                        jobid = '%03d.%03d.%03d' % (cluster, proc, subproc)
                        self._cur['job.id'] = jobid
                        del self._cur['cluster']
                        del self._cur['proc']
                        del self._cur['subproc']
                        result, self._cur = (
                         self._cur,), None
            elif tag_start == '<a':
                if self._cur is None:
                    raise ValueError('orphaned field: %s' % line)
                m = self.FIELD_RE.match(line)
                if m is None:
                    raise ValueError('unrecognized format for field: %s' % line)
                (key, type, value) = m.groups()
                ckey = _camel(key)
                if self.IGNORE_FIELDS_DICT.has_key(key):
                    pass
                elif key == self.EVENT_FIELD_NAME:
                    self._cur['event'] = self.NAMESPACE + '.' + _camel(value[:-5])
                elif key == self.DATE_FIELD_NAME:
                    self._setTimestamp(value)
                elif key.endswith('Host'):
                    m = self.HOST_RE.match(value)
                    if m is None:
                        raise ValueError('Bad Host field: %s' % line)
                    (host, port) = m.groups()
                    self._cur['host'] = host
                    if port:
                        self._cur['port'] = port
                elif key.endswith('Usage'):
                    for part in value.split(', '):
                        (name, idx, raw_time) = part.split()
                        (h, m, s) = raw_time.split(':')
                        sec = int(h) * 3600 + int(m) * 60 + int(s)
                        self._cur[ckey + '.' + name.lower() + '.' + idx] = sec

                elif type == 'b':
                    self._cur[ckey] = value[3] == 't'
                elif type == 'i':
                    self._cur[ckey] = int(value)
                elif type == 'r':
                    self._cur[ckey] = float(value)
                else:
                    self._cur[ckey] = value
            else:
                raise ValueError('line does not start with XML tag: %s' % line)
            return result


def _camel(key):
    return key[0].lower() + key[1:]