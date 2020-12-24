# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/trim/interior/plain/estimating.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 11399 bytes
"""estimating.py estimator deed module

"""
import math, time, struct
from collections import deque
import inspect
from ....aid.sixing import *
from ....aid.odicting import odict
from ....base.globaling import *
from ....aid import aiding, navigating, blending
from ....aid.navigating import DEGTORAD, RADTODEG
from ....base import doing
from ....aid.consoling import getConsole
console = getConsole()

class EstimatorPositionNfl(doing.DoerLapse):
    __doc__ = 'Estimator Position NonlinearFusion class\n    '
    Ioinits = odict(group='estimator.position.nlf',
      position='nlf.position',
      drPosition='dr.position',
      drBias='dr.bias',
      speed='state.speed',
      heading='heading.output',
      current='dvl.current',
      dvlVelocity='dvl.velocity',
      gpsPosition='gps.position',
      gpsVelocity='gps.velocity',
      parms=dict(upsilon=5.0, scale=2.0, gain=0.01, dvlStamp=0.0,
      stale=1.0,
      gpsPosStamp=0.0,
      gpsVelStamp=0.0))

    def __init__(self, **kw):
        (super(EstimatorPositionNfl, self).__init__)(**kw)

    def _initio(self, ioinits):
        """
        Initialize Actor data store interface from ioinits odict

        Wrapper for backwards compatibility to new _initio signature
        """
        (self._prepio)(**ioinits)
        return odict()

    def _prepio(self, group, position, drPosition, drBias, speed, heading, current, dvlVelocity, gpsPosition, gpsVelocity, parms=None, **kw):
        """ Override since uses legacy interface
            group is path name of group in store, group has following subgroups or shares:
              group.parm = share for data structure of fixed parameters or coefficients
                 parm has the following fields:
                    upsilon = fusion parameter related to uncertainty
                    scale = fusion scale factor
                    gain = bias filter gain
                    dvlStamp = time stamp last dvl update
                    stale = time delay for stale pos estimate
                    gpsPosStamp = time stamp last gps position update
                    gpsVelStamp = time stamp last gps velocity update

              group.elapsed = share copy of time lapse for logging

           position = share path name output fused position north east m
           drPosition = share path name output dead reckoned position
           drBias = share path name output dead reckoned forward starboard bias (drift rate m/s)

           speed = share path name input speed m/s
           heading = share path name input heading deg north =0 positive clock wise
           current = share path name input current vector (north, east) m wrt origin on plane
           dvlVelocity = share path name input dvl velocity forward starboard
           gpsPosition = share path name input gps position north sourth
           gpsVelocity = share path name input gps velocity

           parms = dictionary to initialize group.parm fields

           instance attributes

           .group = copy of group name
           .parm = reference to input parameter share

           .position = ref to output position share
           .drPosition = ref to output dr position share
           .drBias = ref to output dr bias share

           .speed = ref to speed share
           .heading = ref to heading share
           .current = ref to input current north east share
           .dvlVelocity = ref to input dvl velocity
           .gpsPosition = ref to input gps position
           .gpsVelocity = ref to input gps velocity

        """
        self.group = group
        self.parm = self.store.create(group + '.parm')
        if not parms:
            parms = dict(upsilon=5.0, scale=2.0, gain=0.01, dvlStamp=0.0,
              stale=1.0,
              gpsPosStamp=0.0,
              gpsVelStamp=0.0)
        (self.parm.create)(**parms)
        self.parm.data.upsilon = abs(self.parm.data.upsilon)
        self.parm.data.scale = abs(self.parm.data.scale)
        self.parm.data.gain = abs(self.parm.data.gain)
        self.parm.data.stale = abs(self.parm.data.stale)
        self.elapsed = self.store.create(group + '.elapsed').create(value=0.0)
        self.position = self.store.create(position)
        self.position.create(north=0.0).update(north=0.0)
        self.position.create(east=0.0).update(east=0.0)
        self.drPosition = self.store.create(drPosition)
        self.drPosition.update(north=0.0)
        self.drPosition.update(east=0.0)
        self.drBias = self.store.create(drBias)
        self.drBias.update(forward=0.0)
        self.drBias.update(starboard=0.0)
        self.speed = self.store.create(speed).create(value=0.0)
        self.heading = self.store.create(heading).create(value=0.0)
        self.current = self.store.create(current)
        self.current.create(north=0.0)
        self.current.create(east=0.0)
        self.dvlVelocity = self.store.create(dvlVelocity)
        self.dvlVelocity.create(forward=0.0)
        self.dvlVelocity.create(starboard=0.0)
        self.gpsPosition = self.store.create(gpsPosition)
        self.gpsPosition.create(north=0.0)
        self.gpsPosition.create(east=0.0)
        self.gpsVelocity = self.store.create(gpsVelocity)
        self.gpsVelocity.create(north=0.0)
        self.gpsVelocity.create(east=0.0)

    def restart(self):
        """Restart

        """
        self.stamp = self.store.stamp
        self.lapse = 0.0
        self.parm.data.dvlStamp = self.dvlVelocity.stamp
        self.parm.data.gpsPosStamp = self.gpsPosition.stamp
        self.parm.data.gpsVelStamp = self.gpsVelocity.stamp

    def action(self, **kw):
        (super(EstimatorPositionNfl, self).action)(**kw)
        self.elapsed.value = self.lapse
        if self.lapse <= 0.0:
            return
        staleNLF = False
        newDVL = False
        newGPS = False
        newHSC = False
        if self.dvlVelocity.stamp > self.parm.data.dvlStamp:
            newDVL = True
        if self.gpsPosition.stamp > self.parm.data.gpsPosStamp:
            newGPS = True
        dvlAge = self.stamp - self.parm.data.dvlStamp
        gpsAge = self.stamp - self.parm.data.gpsPosStamp
        if min(dvlAge, gpsAge) >= self.parm.data.stale:
            staleNLF = True
        if not newDVL:
            if newGPS or staleNLF:
                newHSC = True
        if not (newDVL or newGPS or newHSC):
            return
        heading = self.heading.value
        nlfLapse = self.stamp - self.position.stamp
        if newDVL:
            dvlForward = self.dvlVelocity.data.forward * nlfLapse
            dvlStarboard = self.dvlVelocity.data.starboard * nlfLapse
            nDisp, eDisp = navigating.RotateFSToNE(heading, dvlForward, dvlStarboard)
            self.parm.data.dvlStamp = self.stamp
        else:
            speed = self.speed.value
            cn = self.current.data.north
            ce = self.current.data.east
            nDisp = (speed * math.cos(DEGTORAD * heading) + cn) * nlfLapse
            eDisp = (speed * math.sin(DEGTORAD * heading) + ce) * nlfLapse
        north = self.position.data.north
        east = self.position.data.east
        north += nDisp
        east += eDisp
        drNorth = self.drPosition.data.north
        drEast = self.drPosition.data.east
        drNorth += nDisp
        drEast += eDisp
        self.drPosition.update(north=drNorth, east=drEast)
        if newGPS:
            gpsNorth = self.gpsPosition.data.north
            gpsEast = self.gpsPosition.data.east
            nError = gpsNorth - north
            eError = gpsEast - east
            upsilon = self.parm.data.upsilon
            scale = self.parm.data.scale
            nDelta = nError * blending.blend1(nError, upsilon, scale)
            eDelta = eError * blending.blend1(eError, upsilon, scale)
            north += nDelta
            east += eDelta
            fBias = self.drBias.data.forward
            sBias = self.drBias.data.starboard
            gpsLapse = self.stamp - self.parm.data.gpsPosStamp
            fDelta, sDelta = navigating.RotateNEToFS(heading, nDelta, eDelta)
            gain = self.parm.data.gain
            fBias = (1.0 - gain) * fBias + gain * fDelta / gpsLapse
            sBias = (1.0 - gain) * sBias + gain * sDelta / gpsLapse
            self.drBias.update(forward=fBias, starboard=sBias)
            self.parm.data.gpsPosStamp = self.stamp
        self.position.update(north=north, east=east)

    def _expose(self):
        """
           prints out sensor state

        """
        print('Estimator %s stamp = %s  lapse = %0.3f' % (self.name, self.stamp, self.lapse))
        format = 'north = %0.3f east = %0.3f'
        print(format % (
         self.position.data.north, self.position.data.east))