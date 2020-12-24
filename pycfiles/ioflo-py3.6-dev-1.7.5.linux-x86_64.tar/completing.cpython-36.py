# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/completing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 1862 bytes
"""completing.py  done action module

"""
import time, struct
from collections import deque
import inspect
from ..aid.sixing import *
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

class Complete(acting.Actor):
    __doc__ = 'Complete Class for indicating tasker done state\n\n    '
    Registry = odict()

    def _resolve(self, taskers, **kwa):
        parms = (super(Complete, self)._resolve)(**kwa)
        links = oset()
        for tasker in taskers:
            if tasker == 'me':
                tasker = self._act.frame.framer
                links.add(tasker)
            else:
                tasker = tasking.resolveTasker(tasker, who=(self.name),
                  desc='tasker',
                  contexts=[
                 AUX, SLAVE],
                  human=(self._act.human),
                  count=(self._act.count))
                links.add(tasker)

        parms['taskers'] = links
        return parms


class CompleteDone(Complete):
    __doc__ = 'CompleteDone Complete\n\n    '

    def action(self, taskers, **kw):
        """set done state to True for aux or slave framer

        """
        for tasker in taskers:
            tasker.done = True
            console.profuse('    Done {0}\n'.format(tasker.name))