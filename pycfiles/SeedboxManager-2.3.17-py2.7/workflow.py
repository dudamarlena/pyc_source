# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/process/workflow.py
# Compiled at: 2015-06-14 13:30:57
"""Workflow implementation that handles automatic execution.

Continues to process each step until the workflow reaches completion.

::

    wf = Workflow(torrent)
    tasks = wf.next_tasks()
    # execute tasks in separate threads
    <<logic>>
    # now move the workflow to the next step
    wf.run()

"""
import logging
from seedbox.process import flow
LOG = logging.getLogger(__name__)

class Workflow(flow.BaseFlow):
    """Implementation that handles the orchestration of the process"""

    def run(self):
        """Orchestrate each step of the process based on current state"""
        if not self.is_done():
            next_step = getattr(self, self.phase)
            LOG.debug('next_step: %s', next_step)
            try:
                next_step()
            except (flow.WorkflowError, flow.AbortTransition, flow.InvalidTransitionError,
             flow.ForbiddenTransition) as wferr:
                LOG.exception('workflow error:')
                self.torrent = self.dbapi.get_torrent(self.torrent.torrent_id)
                self.torrent.error_msg = str(wferr)
                self.torrent.failed = True
                self.torrent = self.dbapi.save_torrent(self.torrent)
                return True

        return self.is_done()