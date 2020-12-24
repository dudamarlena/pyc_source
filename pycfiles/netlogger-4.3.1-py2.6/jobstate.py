# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/jobstate.py
# Compiled at: 2010-04-29 16:01:18
"""
A pegasus/dagman/condor jobstate log parser.
"""
__author__ = '$Author: dang $'
__rcsid__ = '$Id: jobstate.py 24755 2010-04-29 20:01:18Z dang $'
import re, time
from netlogger.nllog import TRACE
from netlogger.parsers.base import BaseParser, getGuid
from netlogger.pegasus.kickstart_hdr import lineHasHeader, getHeaderLabel
EVENT_PREFIX = 'pegasus.jobstate.'

class Parser(BaseParser):
    """Pegasus/dagman/condor jobstate parser.

    Parameters:
        - add_guid {yes,no,no*}: Add a unique identifer, using the guid= attribute,
          to each line of the output. The same identifier is used for all output from
          one instance (i.e. one run of the nl_parser).
    """
    INTERNAL = 'internal'
    POSTSCRIPT = 'post_script'
    POSTSCRIPT_START = POSTSCRIPT + '_started'
    (POSTSCRIPT_TERM, POSTSCRIPT_OK, POSTSCRIPT_FAIL) = [ POSTSCRIPT + '_' + s for s in ('terminated',
                                                                                         'success',
                                                                                         'failure')
                                                        ]
    COMP_ID = 'comp.id'
    SITE_ID = 'site.id'
    CONDOR_ID = 'condor.id'
    (PS_START, PS_END) = ('postscript.start', 'postscript.end')
    WORKFLOW_LABEL = 'workflow.id'

    def __init__(self, f, add_guid=False, **kwargs):
        """Construct and initialize class vars.
        """
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)
        self.add_guid = add_guid
        if self.add_guid:
            self.guid = getGuid(repr(time.time()))
        self._ps_term, self._ps_start_time, self._ps_dur = {}, {}, {}
        self._wf_label = None
        return

    def getParameters(self):
        """Get state."""
        return {'wf_label': self._wf_label, 'term': self._ps_term, 
           'start_time': self._ps_start_time, 
           'dur': self._ps_dur}

    def setParameters(self, param):
        """Restore state."""
        self._wf_label = param['wf_label']
        self._ps_term = param['term']
        self._ps_start_time = param['start_time']
        self._ps_dur = param['dur']

    def process(self, line):
        """Process a pegasus/dagman/condor jobstate line.
        """
        if self.log.isEnabledFor(TRACE):
            self.log.trace('process.start')
        if lineHasHeader(line):
            self._wf_label = getHeaderLabel(line)
            return ()
        parts = line.split()
        if len(parts) < 5 or len(parts) > 6:
            raise ValueError, 'Invalid line: expected either 5 or 6 whitespace separated fields'
        try:
            ts = float(parts[0])
        except ValueError:
            raise ValueError, 'Invalid line: expected float as 1st field'

        comp_id = parts[1]
        ename = parts[2].lower()
        condor_id = parts[3]
        site_id = parts[4]
        event = {'ts': float(parts[0])}
        if self.add_guid:
            event['guid'] = self.guid
        if ename == self.INTERNAL:
            if parts[3] == 'TAILSTATD_STARTED':
                event['event'] = EVENT_PREFIX + 'tailstatd.start'
            elif parts[3] == 'DAGMAN_STARTED':
                event['event'] = EVENT_PREFIX + 'dagman.start'
            elif parts[3] == 'DAGMAN_FINISHED':
                event['event'] = EVENT_PREFIX + 'dagman.end'
            elif parts[3] == 'TAILSTATD_FINISHED':
                event['event'] = EVENT_PREFIX + 'tailstatd.end'
                event['status'] = parts[4]
            if self.log.isEnabledFor(TRACE):
                self.log.trace('process.end', status=0, num=1)
            return [event]
        if ename == 'un_ready':
            if self.log.isEnabledFor(TRACE):
                self.log.trace('process.end', status=0, num=0, msg='skip UN_READY')
            return []
        if ename[0] == '*':
            if self.log.isEnabledFor(TRACE):
                self.log.trace('process.end', status=0, num=0, msg='skip header')
            return []
        if ename.startswith(self.POSTSCRIPT):
            if ename == self.POSTSCRIPT_START:
                ename = self.PS_START
                self._ps_start_time[comp_id] = ts
            else:
                if ename == self.POSTSCRIPT_TERM:
                    self._ps_term[comp_id] = condor_id
                    if self._ps_start_time.has_key(comp_id):
                        dur = ts = self._ps_start_time[comp_id]
                    else:
                        stripped_id = comp_id.split('.')[0]
                        if self._ps_start_time.has_key(stripped_id):
                            dur = ts - self._ps_start_time[stripped_id]
                        else:
                            raise ValueError('Cannot find START for %s' % ename)
                    self._ps_dur[comp_id] = dur
                    return ()
                if ename in (self.POSTSCRIPT_OK, self.POSTSCRIPT_FAIL):
                    if not self._ps_term.has_key(comp_id):
                        raise ValueError("Unexpected '%s' for component '%s'" % ename, comp_id)
                    condor_id = self._ps_term[comp_id]
                    event['status'] = (0, -1)[(ename == self.POSTSCRIPT_FAIL)]
                    event['dur'] = self._ps_dur[comp_id]
                    ename = self.PS_END
                    del self._ps_term[comp_id]
                    del self._ps_dur[comp_id]
        event['event'] = EVENT_PREFIX + ename
        event[self.COMP_ID] = comp_id
        event[self.CONDOR_ID] = condor_id
        event[self.SITE_ID] = site_id
        if self._wf_label:
            event[self.WORKFLOW_LABEL] = self._wf_label
        if self.log.isEnabledFor(TRACE):
            self.log.trace('process.end', status=0, num=1)
        return [
         event]