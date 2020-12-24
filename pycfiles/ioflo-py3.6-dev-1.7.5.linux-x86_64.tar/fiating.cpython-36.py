# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/fiating.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 3419 bytes
"""fiating.py goal action module

"""
import time, struct
from collections import deque
import inspect
from ..aid.sixing import *
from .globaling import *
from ..aid.odicting import odict
from ..aid import aiding
from . import excepting
from . import registering
from . import storing
from . import acting
from . import tasking
from . import framing
from ..aid.consoling import getConsole
console = getConsole()

class Fiat(acting.Actor):
    __doc__ = 'Fiat Class for explicit control of slave framers\n       slave framer is not in framer.auxes list and is not actively run by scheduler\n\n    '
    Registry = odict()

    def _resolve(self, tasker, **kwa):
        parms = (super(Fiat, self)._resolve)(**kwa)
        parms['tasker'] = tasker = tasking.resolveTasker(tasker, who=(self.name),
          desc='fiat tasker',
          contexts=[
         SLAVE],
          human=(self._act.human),
          count=(self._act.count))
        return parms


class FiatReady(Fiat):
    __doc__ = 'FiatReady Fiat\n\n    '

    def __init__(self, **kw):
        (super(FiatReady, self).__init__)(**kw)

    def action(self, tasker, **kw):
        """ready control for explicit slave tasker"""
        console.profuse('Ready {0}\n'.format(tasker.name))
        status = tasker.runner.send(READY)
        return status == READIED


class FiatStart(Fiat):
    __doc__ = 'FiatStart Fiat\n\n    '

    def __init__(self, **kw):
        (super(FiatStart, self).__init__)(**kw)

    def action(self, tasker, **kw):
        """start control for explicit slave tasker"""
        console.profuse('Start {0}\n'.format(tasker.name))
        status = tasker.runner.send(START)
        return status == STARTED


class FiatStop(Fiat):
    __doc__ = 'FiatStop Fiat\n\n    '

    def __init__(self, **kw):
        (super(FiatStop, self).__init__)(**kw)

    def action(self, tasker, **kw):
        """stop control for explicit slave framer"""
        console.profuse('Stope {0}\n'.format(tasker.name))
        status = tasker.runner.send(STOP)
        return status == STOPPED


class FiatRun(Fiat):
    __doc__ = 'FiatRun Fiat\n\n    '

    def __init__(self, **kw):
        (super(FiatRun, self).__init__)(**kw)

    def action(self, tasker, **kw):
        """run control for explicit slave tasker"""
        console.profuse('Run {0}\n'.format(tasker.name))
        status = tasker.runner.send(RUN)
        return status == RUNNING


class FiatAbort(Fiat):
    __doc__ = 'FiatAbort Fiat\n\n    '

    def __init__(self, **kw):
        (super(FiatAbort, self).__init__)(**kw)

    def action(self, tasker, **kw):
        """abort control for explicit slave tasker"""
        console.profuse('Abort {0}\n'.format(tasker.name))
        status = tasker.runner.send(ABORT)
        return status == ABORTED