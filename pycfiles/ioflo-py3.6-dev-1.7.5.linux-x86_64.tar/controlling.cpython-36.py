# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/trim/interior/plain/controlling.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 9154 bytes
"""controlling.py controller deed module

"""
import math, time, struct
from collections import deque
import inspect
from ....aid.sixing import *
from ....aid.odicting import odict
from ....aid import aiding, navigating, blending
from ....base import storing
from ....base import doing
from ....aid.consoling import getConsole
console = getConsole()

class ControllerBase(doing.DoerLapse):
    __doc__ = '\n    Base class to provide backwards compatible ._initio interface\n    '

    def _initio(self, ioinits):
        """
        Initialize Actor data store interface from ioinits odict
        Wrapper for backwards compatibility to new ._initio signature
        """
        (self._prepio)(**ioinits)
        return odict()


class ControllerPid(ControllerBase):
    __doc__ = 'PIDController DeedLapse Deed Class\n       PID Controller Class\n\n    '

    def __init__(self, **kw):
        (super(ControllerPid, self).__init__)(**kw)
        self.lapse = 0.0

    def _prepio(self, group, output, input, rate, rsp, parms=None, **kw):
        """ Override default since legacy deed interface

            group is path name of group in store, group has following subgroups or shares:
              group.parm = share for data structure of fixed parameters or coefficients
                 parm has the following fields:
                    wrap = where setpoint wraps around must be positive
                    drsp = delta rsp needed to indicate change in rsp avoids rounding error
                    calcRate = True rate is time difference, False rate is rate sensor input
                    ger = error rate to rate conversion gain
                    gff = feedforward reference to controller gain
                    gpe = proportional error gain
                    gde = derivative error gain
                    gie = integral error gain
                    esmax = maximum error sum
                    esmin = minimum error sum
                    ovmax = maximum controller output value
                    ovmin = minimum controller output value

              group.elapsed = share copy of lapse for logging
              group.prsp = share of prior reference set point needed to compute if changed
              group.e = share of error between rsp and input value appropriately scaled
              group.er = share of rate of change of error
              group.es = share of summation of error

           output is path name of share for output/truth of arbiter

           input = path name of input controlled variable
           rate = path name to input sensed rate of change of controlled variable
           rsp = path name of reference set point for controlled variable
           parms is optional dictionary of initial values for group.parm fields

           instance attributes

           .output = reference to output share
           .group = copy of group name
           .parm = reference to input parameter share
           .elapsed = referenceto lapse share
           .prsp = reference to prior ref set point share
           .e = reference to error share
           .er = reference to error rate share
           .es = reference to error sum share

           .input = reference to input share
           .rate = reference to input rate share
           .rsp = reference to input reference set point

        """
        self.group = group
        self.parm = self.store.create(group + '.parm')
        if not parms:
            parms = dict(wrap=0.0, drsp=0.01, calcRate=True, ger=1.0,
              gff=0.0,
              gpe=0.0,
              gde=0.0,
              gie=0.0,
              esmax=0.0,
              esmin=0.0,
              ovmax=0.0,
              ovmin=0.0)
        (self.parm.create)(**parms)
        self.elapsed = self.store.create(group + '.elapsed').create(value=0.0)
        self.prsp = self.store.create(group + '.prsp').create(value=0.0)
        self.e = self.store.create(group + '.error').create(value=0.0)
        self.er = self.store.create(group + '.errorRate').create(value=0.0)
        self.es = self.store.create(group + '.errorSum').create(value=0.0)
        self.output = self.store.create(output).update(value=0.0)
        self.input = self.store.create(input).create(value=0.0)
        self.rate = self.store.create(rate).create(value=0.0)
        self.rsp = self.store.create(rsp).create(value=0.0)

    def restart(self):
        """Restart controller   """
        self.es.value = 0.0

    def action(self, **kw):
        (super(ControllerPid, self).action)(**kw)
        self.elapsed.value = self.lapse
        if self.lapse <= 0.0:
            return
        else:
            input = self.input.value
            rate = self.rate.value
            rsp = self.rsp.value
            prsp = self.prsp.value
            if abs(rsp - prsp) > self.parm.data.drsp:
                self.prsp.value = rsp
                self.es.value = 0.0
            else:
                rsp = prsp
            pe = self.e.value
            e = navigating.wrap2(angle=(input - rsp), wrap=(self.parm.data.wrap))
            self.e.value = e
            if self.parm.data.calcRate:
                er = (e - pe) / self.lapse
            else:
                er = self.parm.data.ger * rate
        self.er.value = er
        es = self.es.value
        ae = self.lapse * (e + pe) / 2.0
        es += ae * blending.blend0(ae, 0.0, 3.0) * blending.blend0(er, 0.0, 0.1)
        es = min(self.parm.data.esmax, max(self.parm.data.esmin, es))
        self.es.value = es
        out = self.parm.data.gff * rsp + self.parm.data.gpe * e + self.parm.data.gde * er + self.parm.data.gie * es
        out = min(self.parm.data.ovmax, max(self.parm.data.ovmin, out))
        self.output.value = out

    def _expose(self):
        """
           prints out controller state

        """
        print('Controller PID %s stamp = %s lapse = %0.3f input = %0.3f set point = %0.3f ' % (
         self.name, self.stamp, self.lapse, self.input.value, self.rsp.value))
        print('    error = %0.3f errorRate = %0.3f errorSum = %0.3f output = %0.3f truth = %s' % (
         self.e.value, self.er.value, self.es.value, self.output.value, self.output.truth))


ControllerPid.__register__('ControllerPidSpeed', ioinits=odict(group='controller.pid.speed',
  output='goal.rpm',
  input='state.speed',
  rate='state.speedRate',
  rsp='goal.speed',
  parms=dict(wrap=0.0, drsp=0.01, calcRate=True, ger=1.0,
  gff=400.0,
  gpe=0.0,
  gde=0.0,
  gie=0.0,
  esmax=0.0,
  esmin=0.0,
  ovmax=1500.0,
  ovmin=0.0)))
ControllerPid.__register__('ControllerPidHeading', ioinits=odict(group='controller.pid.heading',
  output='goal.rudder',
  input='state.heading',
  rate='state.headingRate',
  rsp='goal.heading',
  parms=dict(wrap=180.0, drsp=0.01, calcRate=True, ger=1.0,
  gff=0.0,
  gpe=3.0,
  gde=0.0,
  gie=0.0,
  esmax=0.0,
  esmin=0.0,
  ovmax=20.0,
  ovmin=(-20.0))))
ControllerPid.__register__('ControllerPidDepth', ioinits=odict(group='controller.pid.depth',
  output='goal.pitch',
  input='state.depth',
  rate='state.depthRate',
  rsp='goal.depth',
  parms=dict(wrap=0.0, drsp=0.01, calcRate=True, ger=1.0,
  gff=0.0,
  gpe=8.0,
  gde=0.0,
  gie=1.0,
  esmax=5.0,
  esmin=(-5.0),
  ovmax=10.0,
  ovmin=(-10.0))))
ControllerPid.__register__('ControllerPidPitch', ioinits=odict(group='controller.pid.pitch',
  output='goal.stern',
  input='state.pitch',
  rate='state.pitchRate',
  rsp='goal.pitch',
  parms=dict(wrap=180.0, drsp=0.01, calcRate=True, ger=1.0,
  gff=0.0,
  gpe=2.0,
  gde=0.0,
  gie=0.0,
  esmax=0.0,
  esmin=0.0,
  ovmax=20.0,
  ovmin=(-20.0))))