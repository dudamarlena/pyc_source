# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/tui.py
# Compiled at: 2015-01-08 02:58:40
from sparts.vtask import VTask
import npyscreen

class UITask(VTask):
    SHUTDOWN_ON_FORM_CLOSE = True

    def initTask(self):
        self._first_run = True
        self.app = npyscreen.NPSAppManaged()
        self.app.onStart = self.appStart
        self.app.onInMainLoop = self.__appInMainLoop
        self.app.onCleanExit = self.appCleanExit
        super(UITask, self).initTask()

    def _runloop(self):
        self.app.run()
        self.service.shutdown()

    def appStart(self):
        """Override this method to initialize the app.

        This should generally consist of calls to something like:

            self.app.registerForm('main', self.make_form())
            self.app.setNextForm('main')
        """
        raise NotImplementedError()

    def appInMainLoop(self):
        """Called between each screen while the application is running.

        Not called before the first screen. Override at will"""
        pass

    def appCleanExit(self):
        """Override to perform cleanup when application exits without error."""
        self.service.shutdown()

    def __appInMainLoop(self):
        """Internal onMainLoop that configures shutdown on first form close."""
        if self._first_run:
            self._first_run = False
            self.app.setNextForm(None)
        self.appInMainLoop()
        return

    def stop(self):
        """npycurses magic to shutdown the app."""
        super(UITask, self).stop()
        if self.app is not None:
            self.app.switchForm(None)
        return