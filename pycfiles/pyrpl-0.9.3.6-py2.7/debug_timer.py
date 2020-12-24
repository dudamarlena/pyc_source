# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/debug_timer.py
# Compiled at: 2017-08-29 09:44:06
from qtpy import QtCore, QtWidgets
import time
from pyrpl.async_utils import sleep as async_sleep
if False:
    from pyrpl import Pyrpl
    pyrpl = Pyrpl(config='nosetests_source.yml', source='nosetests_config.yml')
    async_sleep(0.5)

    class ToPasteInNotebook(object):

        def coucou(self):
            self.count += 1
            if self.count < 1000:
                self.timer.start()

        def test_stupid_timer(self):
            self.timer = QtCore.QTimer()
            self.timer.setInterval(1)
            self.timer.setSingleShot(True)
            self.count = 0
            self.timer.timeout.connect(self.coucou)
            tic = time.time()
            self.timer.start()
            while self.count < 10:
                async_sleep(0.01)

            duration = time.time() - tic
            assert duration < 1, duration


    t = ToPasteInNotebook()
    t.test_stupid_timer()