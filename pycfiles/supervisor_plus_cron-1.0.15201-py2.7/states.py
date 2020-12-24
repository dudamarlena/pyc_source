# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\states.py
# Compiled at: 2015-07-18 10:13:56


class ProcessStates:
    STOPPED = 0
    STARTING = 10
    RUNNING = 20
    BACKOFF = 30
    STOPPING = 40
    EXITED = 100
    FATAL = 200
    UNKNOWN = 1000


STOPPED_STATES = (
 ProcessStates.STOPPED,
 ProcessStates.EXITED,
 ProcessStates.FATAL,
 ProcessStates.UNKNOWN)
RUNNING_STATES = (
 ProcessStates.RUNNING,
 ProcessStates.BACKOFF,
 ProcessStates.STARTING)

def getProcessStateDescription(code):
    return _process_states_by_code.get(code)


class SupervisorStates:
    FATAL = 2
    RUNNING = 1
    RESTARTING = 0
    SHUTDOWN = -1


def getSupervisorStateDescription(code):
    return _supervisor_states_by_code.get(code)


class EventListenerStates:
    READY = 10
    BUSY = 20
    ACKNOWLEDGED = 30
    UNKNOWN = 40


def getEventListenerStateDescription(code):
    return _eventlistener_states_by_code.get(code)


def _names_by_code(states):
    d = {}
    for name in states.__dict__:
        if not name.startswith('__'):
            code = getattr(states, name)
            d[code] = name

    return d


_process_states_by_code = _names_by_code(ProcessStates)
_supervisor_states_by_code = _names_by_code(SupervisorStates)
_eventlistener_states_by_code = _names_by_code(EventListenerStates)