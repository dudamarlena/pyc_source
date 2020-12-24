# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/pwm.py
# Compiled at: 2017-08-29 09:44:06
from . import DspModule

class Pwm(DspModule):
    """Auxiliary outputs. PWM0-3 correspond to pins 17-20 on E2 connector.

    See  http://wiki.redpitaya.com/index.php?title=Extension_connectors
    to find out where to connect your output device to the board.
    Outputs are 0-1.8V, but we will map this to -1 to 1 V internally to
    guarantee compatibility with other modules. So setting a pwm voltage
    to '-1V' means you'll measure 0V, setting it to '+1V' you'll find 1.8V.

    Usage:
    pwm0 = AuxOutput(output='pwm0')
    pwm0.input = 'pid0'
    Pid(client, module='pid0').ival = 0 # -> outputs 0.9V on PWM0

    Make sure you have an analog low-pass with cutoff of at most 1 kHz
    behind the output pin, and possibly an output buffer for proper
    performance. Only recommended for temperature control or other
    slow actuators. Big noise peaks are expected around 480 kHz.

    Currently, only pwm1 and pwm2 are available.
    """

    def __init__(self, rp, name=None):
        super(Pwm, self).__init__(rp, name=dict(pwm0='in1', pwm1='in2')[name])
        self.name = name
        with self.do_setup:
            self.input = 'off'

    output_direct = None
    output_directs = None
    _output_directs = None