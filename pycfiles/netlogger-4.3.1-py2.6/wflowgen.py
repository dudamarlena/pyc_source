# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/wflowgen.py
# Compiled at: 2009-12-08 17:43:28
"""
Classes to generate random 'workflow' logs in BP (NetLogger)
format.
"""
__rcsid__ = '$Id$'
__author__ = 'Dan Gunter (dkgunter (at) lbl.gov)'
import optparse, random, time
from netlogger import nlapi

class RandomWorkflow:
    EVENT_NAMES = ('tinkywinky', 'dipsy', 'lala', 'po')

    def __init__(self, ofile, num=None, min_depth=None, max_depth=None, fail=None, nest=None, **kw):
        self.log = nlapi.Log(ofile)
        self.log.setLevel(nlapi.Level.DEBUG)
        self.max_count, self.min_depth, self.max_depth = num, min_depth, max_depth
        self.failure_rate = fail
        self.nest_rate = nest
        self.event_const = kw

    def generate(self):
        self._generate(0, 0, self._random_depth(), None)
        return

    def _generate(self, count, depth, target_depth, parent_id):
        while count < self.max_count:
            event_base = self._random_event()
            guid = self._random_guid()
            if parent_id:
                kw = self.event_const.copy()
                kw['p.guid'] = parent_id
            else:
                kw = self.event_const
            self.log.write((event_base + '.start'), guid=guid, **kw)
            count += 2
            if depth < target_depth and random.random() <= self.nest_rate:
                count = self._generate(count, depth + 1, target_depth, guid)
            status = (0, -1)[(random.random() < self.failure_rate)]
            self.log.write((event_base + '.end'), guid=guid, status=status, **self.event_const)

        return count

    def _random_depth(self):
        return random.randint(self.min_depth, self.max_depth)

    def _random_event(self):
        prefix = random.choice(self.EVENT_NAMES)
        return '%s.%d' % (prefix, random.randint(1, self.max_count))

    def _random_guid(self):
        s = ''
        for i in xrange(36):
            if i in (8, 13, 18, 23):
                s += '-'
            else:
                s += '%X' % random.randint(0, 15)

        return s


class GlobusWorkflow:

    def __init__(self, file=None, num=None):
        self.n = num
        self.log = nlapi.Log(logfile=file)

    def generate(self):
        """Produce fake Globus MDS4 logs
        
        Workflows can overlap significantly, as the processing time
        is only a few milliseconds whereas the submission time is
        up to one second long.
        """
        g = self.log
        efmt = 'org.globus.execution.job.%s'
        timestamp = time.time()
        for i in xrange(self.n):
            submit_id = nlapi.getGuid()
            resource_id = nlapi.getGuid()
            job_id = nlapi.getGuid()
            g.info(efmt % 'creation.start', ts=timestamp, __id=submit_id, service='ManagedJobFactoryService')
            timestamp += 0.001
            g.info(efmt % 'creation.end', ts=timestamp, __id=submit_id, related__id=resource_id, service='ManagedJobFactoryService')
            timestamp += 0.001
            g.info(efmt % 'processing.start', ts=timestamp, __id=resource_id)
            timestamp += 0.001
            g.info(efmt % 'processing.submission.start', ts=timestamp, __id=resource_id)
            status = random.randint(-1, 0)
            timestamp2 = timestamp + random.randrange(10, 1000) / 1000.0
            g.info(efmt % 'processing.submission.end', ts=timestamp2, status=status, __id=resource_id, job__id=job_id)
            timestamp2 += 0.003
            g.info(efmt % 'processing.end', ts=timestamp2, __id=resource_id, status=status)