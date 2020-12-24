# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_widgets/test_yml_editor.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import time, numpy as np
from pyrpl.async_utils import sleep as async_sleep
from qtpy import QtCore, QtWidgets
from pyrpl.test.test_base import TestPyrpl
from pyrpl import APP
from pyrpl.curvedb import CurveDB
from pyrpl.widgets.startup_widget import HostnameSelectorWidget
from pyrpl.async_utils import sleep
from pyrpl.widgets.yml_editor import YmlEditor
from pyrpl.software_modules.module_managers import ModuleManager

class TestYmlEditor(TestPyrpl):

    def teardown(self):
        pass

    def test_yml_editor(self):
        for mod in self.pyrpl.modules:
            if not isinstance(mod, ModuleManager):
                widg = YmlEditor(mod, None)
                widg.show()
                widg.load_all()
                widg.save()
                widg.cancel()

        return