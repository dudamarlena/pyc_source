# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/dsp.py
# Compiled at: 2017-08-29 09:44:06
from collections import OrderedDict
from ..attributes import BoolRegister, SelectProperty, SelectProperty, SelectRegister
from ..modules import HardwareModule, SignalModule
from ..pyrpl_utils import sorted_dict, recursive_getattr, recursive_setattr
DSP_INPUTS = OrderedDict([
 ('in1', 10),
 ('in2', 11),
 ('out1', 12),
 ('out2', 13),
 ('iq0', 5),
 ('iq1', 6),
 ('iq2', 7),
 ('iq2_2', 14),
 ('pid0', 0),
 ('pid1', 1),
 ('pid2', 2),
 ('asg0', 8),
 ('asg1', 9),
 ('trig', 3),
 ('iir', 4),
 ('off', 15)])

def all_inputs_keys(instance):
    """ collects all available logical inputs, composed of all
    dsp inputs and all submodule inputs, such as lockbox signals etc."""
    signals = list(DSP_INPUTS.keys())
    if instance is not None:
        try:
            pyrpl = instance.pyrpl
        except AttributeError:
            pass
        else:
            if hasattr(pyrpl, 'software_modules'):
                for module in pyrpl.software_modules:
                    try:
                        module_signals = module.signals
                    except AttributeError:
                        if isinstance(module, SignalModule):
                            module_signals = {module.name: module}
                        else:
                            continue

                    for name, signal in module_signals.items():
                        signals.append(signal.name)
                        signal = signal.parent
                        while signal != pyrpl:
                            signals[-1] = signal.name + '.' + signals[(-1)]
                            signal = signal.parent

    return signals


def all_inputs(instance):
    """ collects all available logical inputs, composed of all
    dsp inputs and all submodule inputs, such as lockbox signals etc."""
    signals = OrderedDict()
    for k in all_inputs_keys(instance):
        if k in DSP_INPUTS:
            signals[k] = DSP_INPUTS[k]
        elif instance is not None:
            try:
                signals[k] = recursive_getattr(instance.pyrpl, k + '.signal')()
            except AttributeError:
                pass

    for i in range(4):
        for signal in signals:
            if signals[signal] not in signals:
                pass
            elif signals[signal] == signal:
                signals[signal] = 'off'
            else:
                signals[signal] = signals[signals[signal]]

    return signals


class InputSelectProperty(SelectProperty):
    """ a select register that stores logical signals if possible,
    otherwise the underlying dsp signals"""

    def __init__(self, options=all_inputs_keys, **kwargs):
        SelectProperty.__init__(self, options=options, **kwargs)

    def validate_and_normalize(self, obj, value):
        if isinstance(value, SignalModule):
            pyrpl, rp = value.pyrpl, value.pyrpl.rp
            name = value.name
            fullname = name
            module = value.parent
            while module != pyrpl and module != rp:
                fullname = module.name + '.' + fullname
                module = module.parent

            if fullname in self.options(obj):
                value = fullname
            elif name in self.options(obj):
                value = name
            else:
                value = value.signal()
        else:
            options = self.options(obj)
            if value not in options:
                options = [ o for o in self.options(obj) if o.endswith(value) ]
                if len(options) > 0:
                    value, oldvalue = options[0], value
                    if len(options) > 1:
                        obj._logger.warning('%s.%s was ambiguously assigned the input %s from %s. Possible values were %s.', obj.name, self.name, value, oldvalue, options)
        return super(InputSelectProperty, self).validate_and_normalize(obj, value)


class InputSelectRegister(InputSelectProperty, SelectRegister):

    def __init__(self, address, options=all_inputs, **kwargs):
        SelectRegister.__init__(self, address, options=options, **kwargs)


def all_output_directs(instance):
    return sorted_dict(off=0, out1=1, out2=2, both=3, sort_by_values=True)


def dsp_addr_base(name):
    number = DSP_INPUTS[name]
    return 1076887552 + number * 65536


class DspModule(HardwareModule, SignalModule):

    def __init__(self, rp, name):
        self._number = DSP_INPUTS[name]
        self.addr_base = dsp_addr_base(name)
        super(DspModule, self).__init__(rp, name)

    _delay = 0

    @property
    def inputs(self):
        return all_inputs(self).keys()

    input = InputSelectRegister(0, options=all_inputs, doc='selects the input signal of the module')

    @property
    def output_directs(self):
        return all_output_directs(self).keys()

    output_direct = SelectRegister(4, options=all_output_directs, doc='selects to which analog output the module signal is sent directly')
    out1_saturated = BoolRegister(8, 0, doc='True if out1 is saturated')
    out2_saturated = BoolRegister(8, 1, doc='True if out2 is saturated')