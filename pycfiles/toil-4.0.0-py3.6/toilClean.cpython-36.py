# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilClean.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 1569 bytes
"""
Delete the job store used by a previous Toil workflow invocation
"""
from __future__ import absolute_import
import logging
from toil.lib.bioio import getBasicOptionParser
from toil.lib.bioio import parseBasicOptions
from toil.common import Toil, jobStoreLocatorHelp, Config
from toil.version import version
logger = logging.getLogger(__name__)

def main():
    parser = getBasicOptionParser()
    parser.add_argument('jobStore', type=str, help=('The location of the job store to delete. ' + jobStoreLocatorHelp))
    parser.add_argument('--version', action='version', version=version)
    config = Config()
    config.setOptions(parseBasicOptions(parser))
    try:
        jobStore = Toil.getJobStore(config.jobStore)
        jobStore.destroy()
        logger.info('Successfully deleted the job store: %s' % config.jobStore)
    except:
        logger.info('Failed to delete the job store: %s' % config.jobStore)
        raise