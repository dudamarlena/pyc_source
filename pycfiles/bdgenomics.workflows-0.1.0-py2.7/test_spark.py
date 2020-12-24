# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/bdgenomics/workflows/test/test_spark.py
# Compiled at: 2017-09-18 01:42:06
from __future__ import absolute_import
import os
from subprocess import check_output
import tempfile
from unittest import TestCase, skip
from toil.common import Toil
from toil.job import Job
from bdgenomics.workflows.spark import spawn_spark_cluster
from toil_lib.test import needs_spark

def _count(job, workers):
    ip = None
    if os.uname()[0] == 'Darwin':
        machines = check_output(['docker-machine', 'ls']).strip().rstrip().split('\n')
        if len(machines) != 2:
            raise RuntimeError('Expected a single docker-machine to be running.Got %d:\n%r.' % (
             len(machines) - 1, machines))
        machine = machines[1].split()[0]
        ip = check_output(['docker-machine', 'ip', machine]).strip().rstrip()
    masterHostname = spawn_spark_cluster(job, workers, cores=1, overrideLeaderIP=ip)
    job.addChildJobFn(_count_child, masterHostname)
    return


def _count_child(job, masterHostname):
    from pyspark import SparkContext
    sc = SparkContext(master='spark://%s:7077' % masterHostname, appName='count_test')
    rdd = sc.parallelize(xrange(10000), 10)
    assert rdd.count() == 10000


repeats = 10
failureRate = 0.1

class SparkTest(TestCase):

    def wordCount(self, badWorker=0.0, badWorkerFailInterval=0.05, checkpoint=True):
        workDir = tempfile.mkdtemp()
        os.rmdir(workDir)
        countJob = Job.wrapJobFn(_count, 1, checkpoint=checkpoint)
        options = Job.Runner.getDefaultOptions(workDir)
        options.batchSystem = 'singleMachine'
        options.badWorker = badWorker
        options.badWorkerFailInterval = badWorkerFailInterval
        options.clean = 'never'
        Job.Runner.startToil(countJob, options)

    @needs_spark
    def testSparkLocal(self):
        self.wordCount()

    @skip('fails due to docker container shutdown issue, see #987')
    def testSparkLocalWithBadWorkerAndCheckpoint(self):
        for i in xrange(repeats):
            self.wordCount(badWorker=failureRate)

    @skip('fails due to docker container shutdown issue, see #987')
    def testSparkLocalWithBadWorkerNoCheckpoint(self):
        failed = False
        try:
            for i in xrange(repeats):
                self.wordCount(badWorker=failureRate, checkpoint=False)

        except:
            failed = True

        assert failed