# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/models/observation_timing_functions.py
# Compiled at: 2014-08-27 19:26:12
from datetime import datetime, timedelta

def observations_due_in_window(start=None, end=None):
    """Get the list of Observations which are ready to send now."""
    from observation import Observation
    start = start or datetime.now() - timedelta(weeks=4)
    end = end or datetime.now()
    lookaboutright = Observation.objects.filter(status=0, created_by_script__isnull=False, due__range=(
     start, end))
    actuallyready = [ i for i in lookaboutright if i.ready_to_send() ]
    return actuallyready


def is_pending(observation):
    """Check the Observation is waiting to be 'done' -> Boolean.

    For example, that it hasn't previously been sent, or isn't in progress.
    """
    return bool(observation.status < 1 and observation.status > -99)


def wait_period_expired(observation):
    """Check the last time this Observation was tried was not too recently -> Boolean."""
    redial_delay = timedelta(minutes=observation.dyad.study.redial_delay)
    if observation.last_attempted:
        last = observation.last_attempted
        return bool(datetime.now() > last + redial_delay)
    else:
        return True


def less_than_max_attempts(observation):
    """Check the maximum number of attempts for an Observation has not been met -> Boolean."""
    return bool(observation.attempt_count < observation.dyad.study.max_redial_attempts)