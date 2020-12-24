# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/state.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 4676 bytes
"""Basic listing module that treadmill_list and REST API can use"""
import fnmatch, logging
try:
    import pickle
except ImportError:
    import pickle

from enum import Enum
from . import zknamespace as z
_LOGGER = logging.getLogger(__name__)

class StateEnum(Enum):
    __doc__ = '\n    Enum for the different state names\n    '
    SCHEDULED = 'scheduled'
    RUNNING = 'running'
    PENDING = 'pending'
    STOPPED = 'stopped'
    BROKEN = 'broken'


STATE_NODE_MAP = {StateEnum.SCHEDULED.value: z.SCHEDULED, 
 StateEnum.RUNNING.value: z.RUNNING, 
 StateEnum.PENDING.value: None, 
 StateEnum.STOPPED.value: None}
GLOB_CHAR = '*'
HASH_CHAR = '#'

def strip_instance(name):
    """Strip #.+ suffix if exists."""
    if name.find('#') != -1:
        return name[:name.rfind('#')]
    return name


class State(object):
    __doc__ = 'Treadmill state class.\n\n    :param cell:\n        The cell to retrieve states from\n\n    :param zkclient:\n        Optional existing connection to zkclient, defaults creating a new\n        zkclient\n    '

    def __init__(self, cell, zkclient):
        self.cell = cell
        self.zkclient = zkclient
        self.scheduled = lambda : set(self.zkclient.get_children(STATE_NODE_MAP[StateEnum.SCHEDULED.value]))
        self.running = lambda : set(self.zkclient.get_children(STATE_NODE_MAP[StateEnum.RUNNING.value]))
        self.started = lambda : set([strip_instance(a) for a in self.scheduled()])

    def scheduler(self):
        """Returns scheduled state."""
        sched = None
        try:
            pickled, _metadata = self.zkclient.get('/scheduler')
            sched = pickle.loads(pickled.decode('zlib'))
        except pickle.UnpicklingError:
            _LOGGER.critical('%s - incompatible cell version.', self.cell)

        return sched

    def broken(self):
        """Returns all apps that are scheduled but not running."""
        sched = self.scheduler()
        if sched is None:
            return
        placed = set([app for app in sched.cell.apps if sched.cell.apps[app].node])
        broken_apps = {name:sched.cell.apps[name].node for name in sorted(placed - self.running())}
        broken_nodes = {}
        for app, node in broken_apps.items():
            broken_nodes.setdefault(node, []).append(app)

        return broken_nodes

    def list(self, state, pattern=None):
        """List various application states for the provided cell"""
        handlers = {StateEnum.SCHEDULED.value: lambda : sorted(self.scheduled()), 
         StateEnum.RUNNING.value: lambda : sorted(self.running()), 
         StateEnum.PENDING.value: lambda : sorted(self.scheduled() - self.running()), 
         StateEnum.STOPPED.value: lambda : sorted(self.configured() - self.started()), 
         StateEnum.BROKEN.value: self.broken}
        result = handlers.get(state, self.configured())()
        if isinstance(result, list):
            fully_qualified = ['/'.join([self.cell, name]) for name in result]
            if pattern:
                fully_qualified = ['/'.join([self.cell, name]) for name in result if fnmatch.fnmatch(name, pattern)]
            return fully_qualified
        if isinstance(result, dict) and result.keys():
            fully_qualified = {key:['/'.join([self.cell, app]) for app in result[key]] for key in result}
            if pattern:
                fully_qualified = {key:['/'.join([self.cell, app]) for app in result[key] if fnmatch.fnmatch(app, pattern)] for key in result}
            return fully_qualified

    def get_app_state(self, app, state):
        """Get application for a specific state"""
        pattern = app
        if not app.endswith(GLOB_CHAR):
            if HASH_CHAR not in app:
                pattern = app + GLOB_CHAR
        return self.list(state, pattern)

    def get_app_states(self, app):
        """Return full state for a specific application"""
        app_states = {}
        for state in STATE_NODE_MAP:
            app_states[state] = self.get_app_state(app, state)

        return app_states