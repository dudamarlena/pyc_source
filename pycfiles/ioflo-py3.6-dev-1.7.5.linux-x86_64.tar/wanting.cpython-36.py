# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/wanting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 5165 bytes
"""wanting.py goal action module

"""
import time, struct
from collections import deque
import inspect
from ..aid.sixing import *
from .globaling import STOP, START, RUN, ABORT, READY, ControlNames
from .globaling import INACTIVE, ACTIVE, AUX, SLAVE, MOOT, ScheduleNames, ScheduleValues
from ..aid import odict, oset
from ..aid import aiding
from . import excepting
from . import registering
from . import storing
from . import acting
from . import tasking
from . import framing
from ..aid.consoling import getConsole
console = getConsole()

class Want(acting.Actor):
    __doc__ = '\n    Class for requesting control via skedder using .desire attribute\n       of explicit peer tasker generators\n\n    '
    Registry = odict()

    def _resolve(self, taskers, period, source, sourceField, **kwa):
        parms = (super(Want, self)._resolve)(**kwa)
        links = oset()
        for tasker in taskers:
            if tasker == 'all':
                for tasker in self.store.house.taskables:
                    links.add(tasker)

            elif tasker == 'me':
                tasker = self._act.frame.framer
                links.add(tasker)
            else:
                tasker = tasking.resolveTasker(tasker, who=(self.name),
                  desc='tasker',
                  contexts=[
                 ACTIVE, INACTIVE],
                  human=(self._act.human),
                  count=(self._act.count))
                links.add(tasker)

        if period is None:
            if source is not None:
                parms['source'] = source = self._resolvePath(ipath=source, warn=True)
                if not sourceField:
                    sourceField = 'value'
                if sourceField not in source:
                    console.profuse("     Warning: Non-existent field '{0}' in source {1} ... creating anyway".format(sourceField, source.name))
                    source[sourceField] = 0.0
                parms['sourceField'] = sourceField
        else:
            parms['source'] = None
            parms['sourceField'] = None
        parms['taskers'] = links
        parms['period'] = period
        return parms


class WantStop(Want):
    __doc__ = 'WantStop Want\n       bid stop tasker [tasker ...]\n       bid stop all\n       bid stop [me]\n    '

    def action(self, taskers, **kw):
        """stop taskers """
        for tasker in taskers:
            tasker.desire = STOP
            console.profuse('Bid stop {0}\n'.format(tasker.name))


class WantStart(Want):
    __doc__ = "WantStart Want\n       bid start tasker [taskers ...]\n       bid start all\n       bid start [me] #won't cahnge anything since must be already started\n    "

    def action(self, taskers, period, source, sourceField, **kw):
        """start taskers  """
        if source is not None:
            period = source[sourceField]
        for tasker in taskers:
            if period is not None:
                tasker.period = max(0.0, period)
            tasker.desire = START
            console.profuse('Bid start {0} at {1}\n'.format(tasker.name, tasker.period))


class WantRun(Want):
    __doc__ = "WantRun Want\n       bid run tasker [taskers ...]\n       bid run all\n       bid run [me] #won't cahnge anything since must be already running\n    "

    def action(self, taskers, period, source, sourceField, **kw):
        """run taskers """
        if source is not None:
            period = source[sourceField]
        for tasker in taskers:
            if period is not None:
                tasker.period = max(0.0, period)
            tasker.desire = RUN
            console.profuse('Bid run {0} at (1)\n'.format(tasker.name, tasker.period))


class WantAbort(Want):
    __doc__ = 'WantAbort Want\n       bid abort tasker [taskers ...]\n       bid abort all\n       bid abort [me]\n    '

    def action(self, taskers, **kw):
        """abort taskers """
        for tasker in taskers:
            tasker.desire = ABORT
            console.profuse('Bid abort {0}\n'.format(tasker.name))


class WantReady(Want):
    __doc__ = "WantReady Want\n       bid ready tasker [taskers ...]\n       bid ready all\n       bid ready [me]  # won't change anything since must be already ready\n    "

    def action(self, taskers, period, source, sourceField, **kw):
        """readty taskers """
        if source is not None:
            period = source[sourceField]
        for tasker in taskers:
            if period is not None:
                tasker.period = max(0.0, period)
            tasker.desire = READY
            console.profuse('Bid ready {0} at {1}\n'.format(tasker.name, tasker.period))