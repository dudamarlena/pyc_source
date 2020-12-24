# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/refresher/refresher_application.py
# Compiled at: 2013-04-04 15:36:36
from time import sleep
from threading import Thread
from muntjac.application import Application
from muntjac.ui.window import Window
from muntjac.ui.label import Label
from muntjac.addon.refresher.refresher import Refresher, RefreshListener

class RefresherApplication(Application):

    def __init__(self):
        super(RefresherApplication, self).__init__()
        self._databaseResult = None
        self._content = None
        return

    def init(self):
        mainWindow = Window('Refresher Database Example')
        self.setMainWindow(mainWindow)
        self._content = Label('please wait while the database is queried')
        mainWindow.addComponent(self._content)
        refresher = Refresher()
        refresher.addListener(DatabaseListener(self))
        mainWindow.addComponent(refresher)
        DatabaseQueryProcess(self).start()


class DatabaseListener(RefreshListener):

    def __init__(self, app):
        self._app = app

    def refresh(self, source):
        if self._app._databaseResult is not None:
            source.setEnabled(False)
            self._app._content.setValue('Database result was: ' + self._app._databaseResult)
        return


class DatabaseQueryProcess(Thread):

    def __init__(self, app):
        super(DatabaseQueryProcess, self).__init__()
        self._app = app

    def run(self):
        self._app._databaseResult = self.veryHugeDatabaseCalculation()

    def veryHugeDatabaseCalculation(self):
        try:
            sleep(2000)
        except KeyboardInterrupt:
            pass

        return 'huge!'


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(RefresherApplication, nogui=True, debug=True, contextRoot='.')