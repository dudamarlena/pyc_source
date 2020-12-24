# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/gensim.py
# Compiled at: 2009-12-08 17:43:28
"""
Parse output of Pegasus 'gensim' parser.

THIS PARSER IS EXPERIMENTAL

You can get the gensim parser from  svn at 
 https://smarty.isi.edu/svn/repo1/pegasus/trunk/contrib/showlog
The file is called gensim.

The only way this currently runs is with BOTH the 'out' and 'jobs' files
of the gensim output, in that order, e.g.:

    cat out logs | nl_parser -m gensim > parsed.out
"""
from netlogger.parsers.base import BaseParser

class Parser(BaseParser):
    """Parse the 'job' + 'out' file output by Pegasus 'gensim' parser. 
       Note: EXPERIMENTAL.
    """

    def __init__(self, fileobj, **kw):
        BaseParser.__init__(self, fileobj, **kw)
        self._ts_offs = None
        self._ts = {}
        self._parsing_out = True
        return

    def process(self, line):
        if line.startswith('#Job'):
            self._parsing_out = False
            return ()
        else:
            if self._parsing_out:
                self._parseOut(line)
                return ()
            return self._parseJob(line)

    def _parseOut(self, line):
        fields = line.split()
        relts = int(fields[0])
        job = fields[1]
        if job == 'INTERNAL' and self._ts_offs is None:
            self._ts_offs = relts
        else:
            try:
                (j_action, j_type, j_id) = self._splitJob(job)
                self._ts[j_id] = relts
            except ValueError:
                pass

            return

    def _parseJob(self, line):
        fields = line.split()
        job = fields[0]
        (j_action, j_type, j_id) = self._splitJob(job)
        ts = self._ts[j_id] + self._ts_offs
        e = {'ts': ts, 'event': j_type, 'job.id': j_id, 'action': j_action, 
           'site.id': fields[1], 'kickstart': fields[2], 
           'post': fields[3], 'dagman': fields[4], 
           'condor': fields[5], 'resource': fields[6], 
           'runtime': fields[7], 'condor.queue': fields[8]}
        return (e,)

    def _splitJob(self, job):
        p_id = job.find('_ID')
        if p_id < 0:
            raise ValueError('no ID')
        j_id = job[p_id + 3:]
        p_action = job.find('_', 0, p_id - 1)
        if p_action < 0:
            j_action = 'run'
            j_type = job[:p_id]
        else:
            j_action = job[:p_action]
            j_type = job[p_action + 1:p_id]
        return (
         j_action, j_type, j_id)