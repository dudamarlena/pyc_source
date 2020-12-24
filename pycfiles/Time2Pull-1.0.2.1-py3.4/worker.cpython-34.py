# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/time2pull/worker.py
# Compiled at: 2014-06-16 15:45:18
# Size of source mod 2**32: 2867 bytes
"""
This module contains the worker thread implementation.
"""
import locale
from PyQt5 import QtCore
from time2pull.constants import RemoteStatus

class WorkerThread(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    status_available = QtCore.pyqtSignal(str, bool, object)

    def __init__(self):
        super().__init__()
        self._repositories = []
        self._sleep = True
        self._mutex = QtCore.QMutex()

    def set_repositories_to_refresh(self, repositories):
        _ = QtCore.QMutexLocker(self._mutex)
        self._repositories = repositories

    def get_repositories(self):
        _ = QtCore.QMutexLocker(self._mutex)
        return list(self._repositories)

    def wake_up(self, wake_up=True):
        """
        Wake up the thread and performs a status refresh for all repositories
        in the repositories list.
        """
        _ = QtCore.QMutexLocker(self._mutex)
        self._sleep = not wake_up

    def is_sleeping(self):
        """
        Checks if the thread is sleeping (waiting for wake up/refresh requests)
        :return:
        """
        _ = QtCore.QMutexLocker(self._mutex)
        return self._sleep

    def run(self):
        while True:
            if self.is_sleeping():
                self.sleep(1)
            else:
                self._refresh_all_status()

    def _refresh_all_status(self):
        repositories = self.get_repositories()
        for repo in repositories:
            self._refresh_repo(repo)

        self._sleep = True
        self.finished.emit()

    def _refresh_repo(self, repo):
        process = QtCore.QProcess()
        process.setWorkingDirectory(repo)
        process.start('git', ['remote', 'update'])
        process.waitForFinished()
        process = QtCore.QProcess()
        process.setWorkingDirectory(repo)
        process.start('git', ['status', '-uno'])
        process.waitForFinished()
        output = process.readAllStandardOutput().data().decode(locale.getpreferredencoding())
        if 'behind' in output:
            status = RemoteStatus.behind
        else:
            if 'ahead' in output:
                status = RemoteStatus.ahead
            else:
                if 'diverged' in output:
                    status = RemoteStatus.diverged
                else:
                    status = RemoteStatus.up_to_date
        dirty = 'Changes not staged' in output or 'Changes to be committed' in output
        self.status_available.emit(repo, dirty, status)