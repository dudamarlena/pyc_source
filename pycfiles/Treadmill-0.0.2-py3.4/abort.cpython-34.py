# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/appmgr/abort.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 1104 bytes
"""Manages Treadmill applications lifecycle."""
import logging, os
from treadmill import appevents
from treadmill.apptrace import events
_LOGGER = logging.getLogger(__name__)

def abort(tm_env, event, exc=None, reason=None):
    """Abort a unconfigured application.

    Called when aborting after failed configure step.
    """
    instanceid = os.path.basename(event)
    _LOGGER.info('Aborting %s', instanceid)
    if reason is None:
        if exc:
            reason = type(exc).__name__
    appevents.post(tm_env.app_events_dir, events.AbortedTraceEvent(why=reason, instanceid=instanceid, payload=None))


def flag_aborted(_tm_env, container_dir, exc=None):
    """Flags container as aborted.

    Called when aborting in failed run step.
    Consumed by cleanup script.
    """
    with open(os.path.join(container_dir, 'aborted'), 'w+') as (f):
        if exc:
            f.write(str(exc))