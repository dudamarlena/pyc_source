# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilDebugJob.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 2595 bytes
"""Debug tool for running a toil job locally.
"""
from __future__ import absolute_import
import logging
from toil.lib.bioio import getBasicOptionParser
from toil.lib.bioio import parseBasicOptions
from toil.common import jobStoreLocatorHelp, Config, Toil
from toil.version import version
from toil.worker import workerScript
from toil.utils.toilDebugFile import printContentsOfJobStore
logger = logging.getLogger(__name__)

def print_successor_jobs():
    pass


def main():
    parser = getBasicOptionParser()
    parser.add_argument('jobStore', type=str, help=('The location of the job store used by the workflow.' + jobStoreLocatorHelp))
    parser.add_argument('jobID', nargs=1, help='The job store id of a job within the provided jobstore to run by itself.')
    parser.add_argument('--printJobInfo', nargs=1, help='Return information about this job to the user including preceding jobs, inputs, outputs, and runtime from the last known run.')
    parser.add_argument('--version', action='version', version=version)
    options = parseBasicOptions(parser)
    config = Config()
    config.setOptions(options)
    jobStore = Toil.resumeJobStore(config.jobStore)
    if options.printJobInfo:
        printContentsOfJobStore(jobStorePath=(options.jobStore), nameOfJob=(options.printJobInfo))
    jobID = options.jobID[0]
    logger.debug('Going to run the following job locally: %s', jobID)
    workerScript(jobStore, config, jobID, jobID, redirectOutputToLogFile=False)
    logger.debug('Ran the following job locally: %s', jobID)