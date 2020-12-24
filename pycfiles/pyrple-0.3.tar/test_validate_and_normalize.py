# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_validate_and_normalize.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
from pyrpl.attributes import *
from pyrpl.test.test_base import TestPyrpl
from pyrpl.software_modules import *
from pyrpl.software_modules.module_managers import *
from pyrpl.hardware_modules import *
from pyrpl.modules import *
from pyrpl import APP
from pyrpl.async_utils import sleep as async_sleep
from qtpy import QtCore
from .test_load_save import scramble_values

class TestValidateAndNormalize(TestPyrpl):
    """
    ensures that the result of validate_and_normalize corresponds
    to the value the register actually contains for a number of random
    changes to all registers
    """

    def test_validate_and_normalize(self):
        for mod in self.pyrpl.modules:
            for exclude in [Lockbox]:
                if isinstance(mod, exclude):
                    break
            else:
                yield (
                 self.assert_validate_and_normalize, mod)
                try:
                    mod.stop()
                except:
                    pass

    def assert_validate_and_normalize(self, mod):
        self.results = []

        def check_fpga_value_equals_signal_value(attr_name, list_value):
            print 'check_fpga_value_equals_signal_value(%s.%s, %s) was called!' % (
             mod.name, attr_name, list_value)
            self.results.append(('%s.%s' % (mod.name, attr_name), list_value[0], getattr(mod, attr_name)))

        mod._signal_launcher.update_attribute_by_name.connect(check_fpga_value_equals_signal_value)
        attr_names, attr_vals = scramble_values(mod)
        APP.processEvents()
        mod._signal_launcher.update_attribute_by_name.disconnect(check_fpga_value_equals_signal_value)
        assert len(attr_names) <= len(self.results), '%d attr_names > %d results' % (len(attr_names), len(self.results))
        resultnames = [ name for name, _, __ in self.results ]
        for attr_name in attr_names:
            fullname = '%s.%s' % (mod.name, attr_name)
            assert fullname in resultnames, '%s not in resultnames' % fullname

        exceptions = ['scope._reset_writestate_machine',
         'asg0._offset_masked',
         'asg1._offset_masked',
         'asg0.offset',
         'asg1.offset']
        for name, list_value, attr_value in self.results:
            if name not in exceptions:
                assert list_value == attr_value, (name, list_value, attr_value)