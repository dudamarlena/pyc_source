# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/manager.py
# Compiled at: 2015-11-08 18:31:47
"""Manages the processing of media files."""
import logging
from tvrenamer.core import episode
from tvrenamer.core import watcher
from tvrenamer import processors
LOG = logging.getLogger(__name__)

def _start(processor_mgr):
    LOG.debug('tvrenamer starting...')
    outputs = []
    for afile in watcher.retrieve_files():
        next_ep = episode.Episode(afile)
        outputs.append(next_ep())

    processor_mgr.map_method('process', outputs)
    LOG.debug('tvrenamer finished')


def run():
    """Entry point to start the processing."""
    _start(processors.load())