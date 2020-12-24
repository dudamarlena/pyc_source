# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_log/__init__.py
# Compiled at: 2019-12-29 02:40:55
# Size of source mod 2**32: 8176 bytes
import time, logging, logging.config, os
from logging.handlers import TimedRotatingFileHandler
import portalocker.constants as porta_lock_const
import portalocker.utils as PortaLock

class ConcurrentLogFileLock(PortaLock):

    def __init__(self, filename, *args, **kwargs):
        (PortaLock.__init__)(self, self.get_lock_filename(filename), *args, **kwargs)

    def get_lock_filename(self, log_file_name):
        """
        定义日志文件锁名称，类似于 `.__file.lock`，其中file与日志文件baseFilename一致
        :return: 锁文件名称
        """
        if log_file_name.endswith('.log'):
            lock_file = log_file_name[:-4]
        else:
            lock_file = log_file_name
        lock_file += '.lock'
        lock_path, lock_name = os.path.split(lock_file)
        lock_name = '.__' + lock_name
        return os.path.join(lock_path, lock_name)


class ConcurrentTimedRotatingFileHandler(TimedRotatingFileHandler):
    before_rollover_at = -1

    def __init__(self, filename, *args, **kwargs):
        (TimedRotatingFileHandler.__init__)(self, filename, *args, **kwargs)
        file_path = os.path.split(filename)[0]
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        self.concurrent_lock = ConcurrentLogFileLock(filename, flags=(porta_lock_const.LOCK_EX))

    def emit(self, record) -> None:
        """
        本方法继承Python标准库,修改的部分已在下方使用注释标记出
        本次改动主要是对日志文件进行加锁，并且保证在多进程环境下日志内容切割正确
        """
        with self.concurrent_lock:
            try:
                if self.shouldRollover(record):
                    self.doRollover()
                elif record.created <= ConcurrentTimedRotatingFileHandler.before_rollover_at:
                    currentTime = int(record.created)
                    dstNow = time.localtime(currentTime)[(-1)]
                    t = self.computeRollover(currentTime) - self.interval
                    if self.utc:
                        timeTuple = time.gmtime(t)
                    else:
                        timeTuple = time.localtime(t)
                        dstThen = timeTuple[(-1)]
                        if dstNow != dstThen:
                            if dstNow:
                                addend = 3600
                            else:
                                addend = -3600
                            timeTuple = time.localtime(t + addend)
                    dfn = self.rotation_filename(self.baseFilename + '.' + time.strftime(self.suffix, timeTuple))
                    self._do_write_record(dfn, record)
                else:
                    logging.FileHandler.emit(self, record)
            except Exception:
                self.handleError(record)

    def doRollover(self):
        """
        本方法继承Python标准库,修改的部分已在下方使用注释标记出
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        else:
            currentTime = int(time.time())
            dstNow = time.localtime(currentTime)[(-1)]
            t = self.rolloverAt - self.interval
            if self.utc:
                timeTuple = time.gmtime(t)
            else:
                timeTuple = time.localtime(t)
            dstThen = timeTuple[(-1)]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
            else:
                dfn = self.rotation_filename(self.baseFilename + '.' + time.strftime(self.suffix, timeTuple))
                ConcurrentTimedRotatingFileHandler.before_rollover_at = self.rolloverAt
                if os.path.exists(dfn):
                    pass
                else:
                    self.rotate(self.baseFilename, dfn)
            if self.backupCount > 0:
                for s in self.getFilesToDelete():
                    os.remove(s)

            else:
                if not self.delay:
                    self.stream = self._open()
                newRolloverAt = self.computeRollover(currentTime)
                while newRolloverAt <= currentTime:
                    newRolloverAt = newRolloverAt + self.interval

                if self.when == 'MIDNIGHT' or self.when.startswith('W'):
                    if not self.utc:
                        dstAtRollover = time.localtime(newRolloverAt)[(-1)]
                        if dstNow != dstAtRollover:
                            if not dstNow:
                                addend = -3600
                            else:
                                addend = 3600
                            newRolloverAt += addend
        self.rolloverAt = newRolloverAt

    def _do_write_record(self, dfn, record):
        """
        将日志内容写入指定文件
        :param dfn: 指定日志文件
        :param record: 日志内容
        """
        with open(dfn, mode='a', encoding=(self.encoding)) as (file):
            file.write(self.format(record) + self.terminator)


import logging.handlers
logging.handlers.ConcurrentTimedRotatingFileHandler = ConcurrentTimedRotatingFileHandler