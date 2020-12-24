# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_ownership.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
from qtpy import QtWidgets
from pyrpl.test.test_base import TestPyrpl
from pyrpl.software_modules.module_managers import ModuleManager

class TestOwnership(TestPyrpl):

    def test_ownership_restored(self):
        if self.r is None:
            return
        else:
            self.pyrpl.networkanalyzer.iq.free()
            for module in self.pyrpl.modules:
                if isinstance(module, ModuleManager):
                    with module.pop('foo') as (mod):
                        assert mod.owner == 'foo'
                    assert mod.owner == None

            return