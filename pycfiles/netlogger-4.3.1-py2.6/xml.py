# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/modules/xml.py
# Compiled at: 2011-08-17 23:42:54
"""
'Load' input as XML records to a file.
"""
__author__ = 'Dan Gunter'
__rcsid__ = '$Id: xml.py 28287 2011-08-18 03:42:53Z dang $'
import sys
from netlogger.analysis.modules._base import Analyzer as BaseAnalyzer
from netlogger.nlapi import TS_FIELD, EVENT_FIELD
from netlogger import util
LINE_SEP = '\n'
ATTR_INDENT = '    '
STREAM_OPEN_TAG = "<events xmlns='http://stampede-project.nsf.gov'>"
STREAM_CLOSE_TAG = '</events>'
NC_STREAM_OPEN_TAG = "<nc:data xmlns:nc='urn:ietf:params:xml:ns:netconf:base:1.0'>"
NC_STREAM_CLOSE_TAG = '</nc:data>'

class Analyzer(BaseAnalyzer):
    """Write XML version of records to a file.

    ts=99999 event=foo.bar level=Info value=1234
    =>
    <event-stream xmlns='http://stampede-project.nsf.gov'><events>
    <foo.bar>
       <ts>99999</ts>
       <level>Info</level>
       <value>1234</value>
    </foo.bar>
    </events></event-stream>
    
    Parameters:
      - ostrm {filename,standard output*}: Output stream
      - pretty {True,False*}: If true, make output more readable
      - netconf {True,False*}: If true, make XML compatible with NETCONF
    """

    def __init__(self, ostrm=sys.stdout, pretty='no', netconf='no', **kw):
        """Initialize
        """
        BaseAnalyzer.__init__(self, **kw)
        self.ostrm = ostrm
        self._first = True
        self._pretty = util.as_bool(pretty)
        if self._pretty:
            self._sep, self._indent = LINE_SEP, ATTR_INDENT
        else:
            (self._sep, self._indent) = ('', '')
        self._nc = util.as_bool(netconf)

    def process(self, data):
        if self._dbg:
            self.log.debug('process_data.start')
        if self._first:
            if self._nc:
                self.ostrm.write(NC_STREAM_OPEN_TAG + self._sep)
            self.ostrm.write(STREAM_OPEN_TAG + self._sep)
            self._first = False
        event = data[EVENT_FIELD]
        self.ostrm.write('<event><%s>%s' % (event, self._sep))
        for (key, value) in data.iteritems():
            if key != EVENT_FIELD:
                self.ostrm.write('%s<%s>%s</%s>%s' % (self._indent, key, util.stringize(value), key, self._sep))

        self.ostrm.write('</%s></event>%s' % (event, self._sep))

    def finish(self):
        self.ostrm.write(STREAM_CLOSE_TAG + self._sep)
        if self._nc:
            self.ostrm.write(NC_STREAM_CLOSE_TAG + self._sep)