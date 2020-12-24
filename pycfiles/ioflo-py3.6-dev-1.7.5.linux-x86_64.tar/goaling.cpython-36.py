# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/goaling.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 3570 bytes
"""goaling.py goal action module

"""
import time, struct
from collections import deque
try:
    from itertools import izip
except ImportError:
    izip = zip

import inspect
from ..aid.sixing import *
from ..aid.odicting import odict
from ..aid import aiding
from . import excepting
from . import registering
from . import storing
from . import acting
from ..aid.consoling import getConsole
console = getConsole()

class Goal(acting.Actor):
    __doc__ = 'Goal Class for setting configuration or command value in data share '
    Registry = odict()


class GoalDirect(Goal):
    __doc__ = 'GoalDirect Goal '

    def __init__(self, **kw):
        (super(GoalDirect, self).__init__)(**kw)

    def _resolve(self, destination, destinationFields, sourceData, **kwa):
        parms = (super(GoalDirect, self)._resolve)(**kwa)
        destination = self._resolvePath(ipath=destination, warn=True)
        sourceFields = sourceData.keys()
        destinationFields = self._prepareDstFields(sourceFields, destination, destinationFields)
        dstData = odict()
        for dstField, srcField in izip(destinationFields, sourceFields):
            dstData[dstField] = sourceData[srcField]

        parms['destination'] = destination
        parms['data'] = dstData
        return parms

    def action(self, destination, data, **kw):
        """
        Set destination goal to data dictionary
        parameters:
              destination = share of goal
              data = dict of data fields to assign to goal share
        """
        console.profuse('Set {0} to {1}\n'.format(destination.name, data))
        destination.update(data)


class GoalIndirect(Goal):
    __doc__ = 'GoalIndirect Goal '

    def __init__(self, **kw):
        (super(GoalIndirect, self).__init__)(**kw)

    def _resolve(self, destination, destinationFields, source, sourceFields, **kwa):
        parms = (super(GoalIndirect, self)._resolve)(**kwa)
        destination = self._resolvePath(ipath=destination, warn=True)
        source = self._resolvePath(ipath=source, warn=True)
        sourceFields, destinationFields = self._prepareSrcDstFields(source, sourceFields, destination, destinationFields)
        parms['destination'] = destination
        parms['destinationFields'] = destinationFields
        parms['source'] = source
        parms['sourceFields'] = sourceFields
        return parms

    def action(self, destination, destinationFields, source, sourceFields, **kw):
        """
        Set destinationFields in destination goal from sourceFields in source

        parameters:
              destination = share of goal
              source = share of source to get data from
              fields = fields to use to update goal
        """
        console.profuse('Set {0} in {1} from {2} in {3}\n'.format(destination.name, destinationFields, source.name, sourceFields))
        data = odict()
        for gf, sf in izip(destinationFields, sourceFields):
            data[gf] = source[sf]

        destination.update(data)