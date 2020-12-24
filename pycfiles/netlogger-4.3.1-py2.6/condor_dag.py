# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/condor_dag.py
# Compiled at: 2010-04-28 23:52:08
"""
Parse an output of Condor DAGMan
"""
import time
from netlogger.parsers.base import BaseParser
from netlogger.pegasus.kickstart_hdr import lineHasHeader, getHeaderLabel

class Parser(BaseParser):
    """Parse the 'dag' file output by Condor's DAGMan

    Parameters:
    - base_ts {TIMESTAMP}: Numeric or ISO8601 string timestamp 
               to use for all output events.
               If not given, use current time.
    """
    (PARENT, CHILD) = ('PARENT', 'CHILD')
    EVENT = 'condor.dag.edge'
    (PARENT_ID, CHILD_ID) = [ 'comp.' + s + '.id' for s in ('parent', 'child') ]
    WORKFLOW_LABEL = 'workflow.id'

    def __init__(self, fileobj, base_ts=None, **kw):
        BaseParser.__init__(self, fileobj, fullname='condor_dag', **kw)
        if base_ts is None:
            self._ts = time.time()
        else:
            self._ts = base_ts
        self._wf_label = None
        return

    def process(self, line):
        if lineHasHeader(line):
            self._wf_label = getHeaderLabel(line)
            return ()
        if not line.startswith(self.PARENT):
            return ()
        fields = line.split()
        if len(fields) != 4:
            raise ValueError('#fields (%d) does not match expected (4)' % len(fields))
        event = {'ts': self._ts, 'event': self.EVENT, self.PARENT_ID: fields[1], 
           self.CHILD_ID: fields[3]}
        if self._wf_label:
            event[self.WORKFLOW_LABEL] = self._wf_label
        return (
         event,)