# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/trim/interior/plain/detecting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 8613 bytes
"""detecting.py detector deed module

"""
import math, time, struct
from collections import deque
import inspect
from ....aid.sixing import *
from ....aid.odicting import odict
from ....base.globaling import *
from ....aid import aiding, navigating
from ....base import doing
from ....aid.consoling import getConsole
console = getConsole()

class DetectorBase(doing.Doer):
    __doc__ = '\n    Base class to provide backwards compatible ._initio interface\n    '

    def _initio(self, ioinits):
        """
        Initialize Actor data store interface from ioinits odict
        Wrapper for backwards compatibility to new ._initio signature
        """
        (self._prepio)(**ioinits)
        return odict()


class DetectorPositionBox(DetectorBase):
    __doc__ = '\n    Detects if vehicle position is in box or out\n    output share indicates which side in or out\n    '
    Ioinits = odict(group='detector.position.box',
      output='box',
      input='state.position',
      parms=dict(track=0.0, north=0.0, east=0.0, length=10000,
      width=2000,
      turn=45.0))

    def __init__(self, **kw):
        (super(DetectorPositionBox, self).__init__)(**kw)

    def _prepio(self, group, output, input, parms=None, **kw):
        """ Override since uses legacy interface

            output
              inside   = vehicle is inside box (Booleans True (False))
              outtop  = vehicle is outside box above top highest priority
              outbottom = vehicle is outside box below bottom next priority
              outleft  = vehicle is outside to the left
              outright  = vehicle is outside to the right
              turnleft = heading for left turn
              turnright = heading for right turn

           inputs
           input = share path name to input vehicle position (north, east)

           parms = dictionary to initialize group.parm fields
              parm.track  = azimuth of track in (degrees)
              parm.width  = width of box  (meters)
              parm.length = length of box (meters)
              parm.north  = north value for center bottom of box (meters)
              parm.east  = east value for center bottom of box (meters)
              parm.turn = degrees to left or right of track for zig zags (0 - 90)

           instance attributes

           .group = copy of group name

           .output = ref to output
              side state with boolean data fields
              .inside, .outtop, .outbottom, .outleft, .outright
              turn headings with data fields
              .turnleft
              .turnright

           .input = ref to vehicle position external input

           .parm = ref to input parameter share group.parm

        """
        self.group = group
        self.output = self.store.create(output)
        fields = odict(inside=False)
        fields['outtop'] = False
        fields['outbottom'] = False
        fields['outleft'] = False
        fields['outright'] = False
        fields['turnleft'] = 0.0
        fields['turnright'] = 0.0
        self.output.update(fields)
        self.input = self.store.create(input)
        self.input.create(north=0.0)
        self.input.create(east=0.0)
        self.parm = self.store.create(group + '.parm')
        if not parms:
            parms = dict(track=0.0, width=1000, length=10000, north=0.0,
              east=0.0,
              turn=45.0)
        parms['turn'] = abs(navigating.wrap2(parms['turn']))
        (self.parm.create)(**parms)
        turnleft = self.parm.data.track - self.parm.data.turn
        turnright = self.parm.data.track + self.parm.data.turn
        self.output.update(turnleft=turnleft, turnright=turnright)

    def action(self, **kw):
        """computes box detector output

           treat center bottom as origin
           inside outside as delta position relative to center bottom
           and rotated about center bottom by -track
        """
        turnleft = navigating.wrap2(self.parm.data.track - self.parm.data.turn)
        turnright = navigating.wrap2(self.parm.data.track + self.parm.data.turn)
        self.output.update(turnleft=turnleft, turnright=turnright)
        pn = self.input.data.north
        pe = self.input.data.east
        cbn = self.parm.data.north
        cbe = self.parm.data.east
        track = self.parm.data.track
        length = self.parm.data.length
        width = self.parm.data.width
        pn = pn - cbn
        pe = pe - cbe
        pn, pe = navigating.RotateFSToNE(heading=(-track), forward=pn, starboard=pe)
        self.output.update(inside=True)
        cn = length
        ce = -width / 2.0
        sn = 0.0
        se = width
        rn = pn - cn
        re = pe - ce
        side = se * rn - sn * re
        if side >= 0.0:
            self.output.update(outtop=True, inside=False)
        else:
            self.output.update(outtop=False)
        cn = 0.0
        ce = width / 2.0
        sn = 0.0
        se = -width
        rn = pn - cn
        re = pe - ce
        side = se * rn - sn * re
        if side >= 0.0:
            self.output.update(outbottom=True, inside=False)
        else:
            self.output.update(outbottom=False)
        cn = 0.0
        ce = -width / 2.0
        sn = length
        se = 0.0
        rn = pn - cn
        re = pe - ce
        side = se * rn - sn * re
        if side >= 0.0:
            self.output.update(outleft=True, inside=False)
        else:
            self.output.update(outleft=False)
        cn = length
        ce = width / 2.0
        sn = -length
        se = 0.0
        rn = pn - cn
        re = pe - ce
        side = se * rn - sn * re
        if side >= 0.0:
            self.output.update(outright=True, inside=False)
        else:
            self.output.update(outright=False)
        if console._verbosity >= console.Wordage.profuse:
            self._expose()
            console.profuse('doing {0} with output (itblf) = {1}\n'.format(self.name, self.output))

    def _expose(self):
        """
           prints out detector state

        """
        print('Detector %s' % self.name)
        format = 'box center bottom north = %0.3f east = %0.3f'
        print(format % (self.parm.data.north, self.parm.data.east))
        format = 'box track = %0.3f length = %0.3f width = %0.3f turn = %0.3f'
        print(format % (self.parm.data.track, self.parm.data.length,
         self.parm.data.width, self.parm.data.turn))
        format = 'turn left = %0.3f turn right  = %0.3f '
        print(format % (self.output.data.turnleft, self.output.data.turnright))
        format = 'position north = %0.3f east = %0.3f'
        print(format % (self.input.data.north, self.input.data.east))
        format = 'box inside = %s outside top = %s bottom = %s left = %s right = %s'
        print(format % (self.output.data.inside,
         self.output.data.outtop, self.output.data.outbottom,
         self.output.data.outleft, self.output.data.outright))