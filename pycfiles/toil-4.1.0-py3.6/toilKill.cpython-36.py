# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilKill.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 2680 bytes
"""Kills rogue toil processes."""
from __future__ import absolute_import
import logging, os, signal
from toil.lib.bioio import getBasicOptionParser
from toil.lib.bioio import parseBasicOptions
from toil.common import Toil, jobStoreLocatorHelp, Config
from toil.version import version
logger = logging.getLogger(__name__)

def main():
    parser = getBasicOptionParser()
    parser.add_argument('jobStore', type=str, help=('The location of the job store used by the workflow whose jobs should be killed.' + jobStoreLocatorHelp))
    parser.add_argument('--version', action='version', version=version)
    options = parseBasicOptions(parser)
    config = Config()
    config.setOptions(options)
    config.jobStore = config.jobStore[5:] if config.jobStore.startswith('file:') else config.jobStore
    if ':' in config.jobStore:
        jobStore = Toil.resumeJobStore(config.jobStore)
        logger.info('Starting routine to kill running jobs in the toil workflow: %s', config.jobStore)
        batchSystem = Toil.createBatchSystem(jobStore.config)
        for jobID in batchSystem.getIssuedBatchJobIDs():
            batchSystem.killBatchJobs(jobID)

        logger.info('All jobs SHOULD have been killed')
    else:
        pid_log = os.path.join(os.path.abspath(config.jobStore), 'pid.log')
        with open(pid_log, 'r') as (f):
            pid2kill = f.read().strip()
    try:
        os.kill(int(pid2kill), signal.SIGKILL)
        logger.info('Toil process %s successfully terminated.' % str(pid2kill))
    except OSError:
        logger.error('Toil process %s could not be terminated.' % str(pid2kill))
        raise