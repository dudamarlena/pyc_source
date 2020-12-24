# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/progressindicator/ProgressIndicatorsExample.py
# Compiled at: 2013-04-04 15:36:38
import time, threading
from muntjac.api import VerticalLayout, Label, ProgressIndicator, HorizontalLayout, Alignment, Button
from muntjac.ui import button

class ProgressIndicatorsExample(VerticalLayout):

    def __init__(self):
        super(ProgressIndicatorsExample, self).__init__()
        self.setSpacing(True)
        self.addComponent(Label('<strong>Normal mode</strong> Runs for 20 seconds', Label.CONTENT_XHTML))
        hl = HorizontalLayout()
        hl.setSpacing(True)
        self.addComponent(hl)
        self._pi1 = ProgressIndicator()
        self._pi1.setIndeterminate(False)
        self._pi1.setEnabled(False)
        hl.addComponent(self._pi1)
        hl.setComponentAlignment(self._pi1, Alignment.MIDDLE_LEFT)
        self._startButton1 = Button('Start normal', NormalListener(self))
        self._startButton1.setStyleName('small')
        hl.addComponent(self._startButton1)
        self.addComponent(Label('<strong>Indeterminate mode</strong> Runs for 10 seconds', Label.CONTENT_XHTML))
        hl = HorizontalLayout()
        hl.setSpacing(True)
        self.addComponent(hl)
        self._pi2 = ProgressIndicator()
        self._pi2.setIndeterminate(True)
        self._pi2.setPollingInterval(5000)
        self._pi2.setEnabled(False)
        hl.addComponent(self._pi2)
        l = IndeterminateListener(self)
        self._startButton2 = Button('Start indeterminate', l)
        self._startButton2.setStyleName('small')
        hl.addComponent(self._startButton2)

    def prosessed(self):
        i = self._worker1.getCurrent()
        if i == Worker1.MAX:
            self._pi1.setEnabled(False)
            self._startButton1.setEnabled(True)
            self._pi1.setValue(1.0)
        else:
            self._pi1.setValue(i / self.Worker1.MAX)

    def prosessed2(self):
        self._pi2.setEnabled(False)
        self._startButton2.setEnabled(True)


class NormalListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c._worker1 = Worker1(self)
        self._c._worker1.start()
        self._c._pi1.setEnabled(True)
        self._c._pi1.setValue(0.0)
        self._c._startButton1.setEnabled(False)


class IndeterminateListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c._worker2 = Worker2(self)
        self._c._worker2.start()
        self._c._pi2.setEnabled(True)
        self._c._pi2.setVisible(True)
        self._c._startButton2.setEnabled(False)


class Worker1(threading.Thread):
    MAX = 20

    def __init__(self, c):
        super(Worker1, self).__init__()
        self._c = c
        self._current = 1

    def run(self):
        while self._current <= self.MAX:
            try:
                time.sleep(1000)
            except self.InterruptedException as e:
                print str(e)

            self._c.prosessed()
            self._current += 1

    def getCurrent(self):
        return self._current


class Worker2(threading.Thread):

    def __init__(self, c):
        super(Worker2, self).__init__()
        self._c = c

    def run(self):
        try:
            time.sleep(10000)
        except self.InterruptedException as e:
            print str(e)

        self._c.prosessed2()