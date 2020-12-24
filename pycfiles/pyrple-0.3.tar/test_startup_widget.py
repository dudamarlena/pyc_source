# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_widgets/test_startup_widget.py
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

class TestStartupWidgets(TestPyrpl):

    def teardown(self):
        pass

    def test_startup_widget(self):
        for hide_password in [True, False]:
            HostnameSelectorWidget._HIDE_PASSWORDS = hide_password
            self.widget = HostnameSelectorWidget()

        self.widget.show()
        self.widget.password = 'dummy_password'
        self.widget.user = 'dummy_user'
        self.widget.sshport = 12
        sleep(0.1)
        self.widget.item_double_clicked(self.widget.items[0], 0)
        self.widget.remove_device(self.widget.items[0])
        self.widget.countdown_start(2)
        sleep(3)
        self.widget.ok()