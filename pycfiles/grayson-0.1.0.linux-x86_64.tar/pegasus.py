# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/grayson/pegasus.py
# Compiled at: 2012-03-02 14:59:52
""" system """
import logging, traceback
from Pegasus.DAX3 import ADAG
from Pegasus.DAX3 import DAX
from Pegasus.DAX3 import Executable
from Pegasus.DAX3 import File
from Pegasus.DAX3 import Job
from Pegasus.DAX3 import Link
from Pegasus.DAX3 import PFN
from Pegasus.DAX3 import Profile
from Pegasus.DAX3 import Transformation
import Pegasus.DAX3

class WorkflowParser(object):

    def __init__(self, workflow):
        self.workflow = workflow
        logging.info('=================================================================')
        logging.info('== Analyzing DAX [%s] with Pegasus API', self.workflow)
        logging.info('=================================================================')
        self.dag = Pegasus.DAX3.parse(self.workflow)
        logging.info('dag-name: %s', self.dag.name)

    def getFiles(self):
        return self.dag.files

    def getJobs(self, includeRegularJobs=True, includeWorkflows=True):
        jobs = []
        for j in self.dag.jobs:
            if isinstance(job, DAX):
                if includeRegularJobs:
                    jobs.append(j)
            elif includeWorkflows:
                jobs.append(j)

        return jobs

    def getJobById(self, id):
        job = None
        for j in self.dag.jobs:
            if j.id == id:
                job = j
                break

        return job

    def getInputFiles(self, jobid):
        return self.getUsedFiles(jobid, Link.INPUT)

    def getOutputFiles(self, jobid):
        return self.getUsedFiles(jobid, Link.OUTPUT)

    def getUsedFiles(self, jobid, linkType=None):
        result = []
        job = self.getJobById(jobid)
        usedFiles = job.used_files
        for file in usedFiles:
            if linkType and file.link == linkType:
                item = {'type': 'file', 'name': file.name, 
                   'id': file.name}
                result.append(item)

        return result

    def getTansformations(self):
        return self.dag.transformations

    def getExecutables(self):
        return self.dag.executables

    def getDependencies(self):
        return self.dag.dependencies