# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/JSApiExample.py
# Compiled at: 2013-04-04 15:36:38
import time, threading
from time import gmtime, strftime
from muntjac.api import Button, VerticalLayout, Label, TextArea
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.ui.button import IClickListener

class JSApiExample(VerticalLayout):

    def __init__(self):
        super(JSApiExample, self).__init__()
        self._toBeUpdatedFromThread = None
        self._startThread = None
        self._running = Label('')
        self.setSpacing(True)
        javascript = Label('<h3>Run Native JavaScript</h3>', Label.CONTENT_XHTML)
        self.addComponent(javascript)
        script = TextArea()
        script.setWidth('100%')
        script.setRows(3)
        script.setValue('alert("Hello Muntjac");')
        self.addComponent(script)
        self.addComponent(Button('Run script', RunListener(self, script)))
        return


class RunListener(IClickListener):

    def __init__(self, component, script):
        self._component = component
        self._script = script

    def buttonClick(self, event):
        self._component.getWindow().executeJavaScript(str(self._script.getValue()))


class StartListener(IClickListener):

    def __init__(self, component):
        self._component = component

    def buttonClick(self, event):
        self._component._startThread.getParent().replaceComponent(self._component._startThread, self._component._running)
        BackgroundProcess(self._component).start()


class BackgroundProcess(threading.Thread):

    def __init__(self, component):
        super(BackgroundProcess, self).__init__()
        self._component = component

    def run(self):
        try:
            i = 0
            while i < 10:
                time.sleep(1000)
                self._component._toBeUpdatedFromThread.setValue('<strong>Server time is ' + strftime('%H:%M:%S', gmtime()) + '</strong>')
                i += 1

            self._component._toBeUpdatedFromThread.setValue('Background process finished')
            self._component._running.getParent().replaceComponent(self._component._running, self._component._startThread)
        except self.InterruptedException as e:
            e.printStackTrace()