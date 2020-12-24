# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_lib/test/test_jobs.py
# Compiled at: 2017-05-10 17:49:05
import tempfile, os
from toil.job import Job

def test_map_job():
    from toil_lib.jobs import map_job
    work_dir = tempfile.mkdtemp()
    options = Job.Runner.getDefaultOptions(os.path.join(work_dir, 'test_store'))
    options.workDir = work_dir
    samples = [ x for x in xrange(200) ]
    j = Job.wrapJobFn(map_job, _test_batch, samples, 'a', 'b', 'c', disk='1K')
    Job.Runner.startToil(j, options)


def _test_batch(job, sample, a, b, c):
    assert str(sample).isdigit()
    assert a == 'a'
    assert b == 'b'
    assert c == 'c'