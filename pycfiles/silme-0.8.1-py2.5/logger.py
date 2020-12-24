# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/silme/core/logger.py
# Compiled at: 2009-11-24 18:17:29
import silme.core

class Logger:

    @classmethod
    def log(cls, type, message, path=None):
        """
        adds a new log to the object.
        """
        if hasattr(cls, 'logs'):
            cls.logs.append((type, message, path))
        else:
            cls.logs = [
             (
              type, message, path)]
        return True

    @classmethod
    def get_logs(cls):
        """
        returns list of logs for Logger
        """
        if hasattr(cls, 'logs'):
            return cls.logs
        return []


def log(self, type, message, path=None):
    """
    adds a new log to the object. If self.logs list does not exist its being added
    """
    if hasattr(self, 'logs'):
        self.logs.append((type, message, path))
    else:
        self.logs = [
         (
          type, message, path)]
    return True


def get_logs(self):
    """
    returns list of logs for the object
    """
    if hasattr(self, 'logs'):
        return self.logs
    return []


def get_all_logs(self, recursive=False):
    """
    returns list of logs for the package, optionally can also load
    all logs from its objects and sub-packages.
    """
    if hasattr(self, 'logs'):
        logs = self.logs
    else:
        logs = []
    if not recursive:
        return logs
    for object in self.structures():
        logs.extend(object.get_logs())

    for package in self.packages():
        logs.extend(package.get_logs(recursive=True))

    return logs


silme.core.EntityList.log = log
silme.core.EntityList.get_logs = get_logs
silme.core.Structure.log = log
silme.core.Structure.get_logs = get_logs
silme.core.Package.log = log
silme.core.Package.get_logs = get_all_logs