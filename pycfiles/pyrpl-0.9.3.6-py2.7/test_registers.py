# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_registers.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
from pyrpl.modules import Module
from pyrpl.attributes import *
from .test_redpitaya import TestRedpitaya

class TestRegisters(TestRedpitaya):
    """ This test verifies that all registers behave as expected.

    The test is not only useful to test the python interface,
    but also checks that the fpga is not behaving stragely,
    i.e. loosing data or writing the wrong data. Thus, it is the
    principal test to execute on new fpga designs. """

    def test_generator(self):
        assert self.r is None and False
        for modulekey, module in self.r.__dict__.items():
            if isinstance(module, Module):
                logger.info('Scanning module %s...', modulekey)
                for regkey, regclass in type(module).__dict__.items():
                    if isinstance(regclass, BaseRegister):
                        logger.info('Scanning register %s...', regkey)
                        yield (self.register_validation, module, modulekey,
                         regclass, regkey)

        return

    def register_validation(self, module, modulekey, reg, regkey):
        logger.debug('%s %s', modulekey, regkey)
        if type(reg) is BaseRegister:
            value = module.__getattribute__(regkey)
            assert isinstance(value, int) or False, 'wrong type: int != %s' % str(type(value))
        module.__setattr__(regkey, value)
        newvalue = module.__getattribute__(regkey)
        assert value == newvalue, 'Mismatch: value=' + str(value) + ' new value = ' + str(newvalue)
        if type(reg) is LongRegister:
            value = module.__getattribute__(regkey)
            assert not isinstance(value, int) and not isinstance(value, long) and False, 'wrong type: int/long != %s' % str(type(value))
        module.__setattr__(regkey, value)
        newvalue = module.__getattribute__(regkey)
        if regkey not in ('current_timestamp', ):
            if not value == newvalue:
                raise AssertionError('Mismatch: value=' + str(value) + ' new value = ' + str(newvalue))
        if type(reg) is BoolRegister or type(reg) is IORegister:
            value = module.__getattribute__(regkey)
            assert type(value) != bool and False
        if regkey in ('_reset_writestate_machine', '_trigger_armed', '_trigger_delay_running',
                      'pretrig_ok', 'armed'):
            return
        module.__setattr__(regkey, not value)
        if value == module.__getattribute__(regkey):
            assert False
            module.__setattr__(regkey, value)
            if value != module.__getattribute__(regkey):
                if not False:
                    raise AssertionError
            if type(reg) is FloatRegister:
                value = module.__getattribute__(regkey)
                assert isinstance(value, float) or False
            if regkey in ('pfd_integral', 'ch1_firstpoint', 'ch2_firstpoint', 'voltage_out1',
                          'voltage_out2', 'voltage_in1', 'voltage_in2', 'firstpoint',
                          'lastpoint') or modulekey == 'sampler':
                return
            if value == 0:
                write = 10000000000.0
            else:
                write = 0
            module.__setattr__(regkey, write)
            assert value == module.__getattribute__(regkey) and False
        write = -10000000000.0
        module.__setattr__(regkey, write)
        if module.__getattribute__(regkey) >= 0:
            if reg.signed:
                assert False
            elif module.__getattribute__(regkey) == 0:
                assert False
        module.__setattr__(regkey, value)
        if value != module.__getattribute__(regkey):
            if not False:
                raise AssertionError
        if type(reg) is PhaseRegister:
            value = module.__getattribute__(regkey)
            assert isinstance(value, float) or False
        if regkey not in ('scopetriggerphase', ):
            for phase in np.linspace(-1234, 5678, 90):
                module.__setattr__(regkey, phase)
                diff = abs(module.__getattribute__(regkey) - phase % 360)
                bits = getattr(module.__class__, regkey).bits
                thr = 360.0 / 2 ** bits / 2
                if diff > thr:
                    assert False, 'at phase ' + str(phase) + ': diff = ' + str(diff)

        module.__setattr__(regkey, value)
        if value != module.__getattribute__(regkey):
            if not False:
                raise AssertionError
        if type(reg) is FrequencyRegister:
            value = module.__getattribute__(regkey)
            assert isinstance(value, float) or False
        if regkey not in ():
            for freq in [0, 1, 10, 100.0, 1000.0, 10000.0, 100000.0, 1000000.0, 10000000.0, 125000000.0 / 2]:
                module.__setattr__(regkey, freq)
                diff = abs(module.__getattribute__(regkey) - freq)
                if diff > 0.1:
                    assert False, 'at freq ' + str(freq) + ': diff = ' + str(diff)

        module.__setattr__(regkey, value)
        if value != module.__getattribute__(regkey):
            if not False:
                raise AssertionError
        if type(reg) is SelectRegister:
            value = module.__getattribute__(regkey)
            assert isinstance(sorted(reg.options(module))[0], type(value)) or False
        if regkey in ('id', ):
            return
        for option in sorted(reg.options(module)):
            module.__setattr__(regkey, option)
            if option != module.__getattribute__(regkey):
                assert False

        module.__setattr__(regkey, value)
        if value != module.__getattribute__(regkey):
            if not False:
                raise AssertionError