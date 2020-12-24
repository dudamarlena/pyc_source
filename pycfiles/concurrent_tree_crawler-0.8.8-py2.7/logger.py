# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/logger.py
# Compiled at: 2011-09-28 13:50:09
import logging, sys

class Logger:
    __default_root_log_level = logging.WARNING
    __console_h = None
    __file_h = None

    @staticmethod
    def start(stream=sys.stderr, file_path=None, logging_level=logging.WARNING, format_='%(asctime)s %(levelname)s %(message)s'):
        """@param stream: output stream where logs are written. If C{None}, 
                        logs are not written to any stream.
                        @param file_path: if it is not C{None}, logging messages are written
                        not only to the stream, but to the specified file as well.
                        @param logging_level: logging level accepted by logging devices"""
        formatter = logging.Formatter(format_)
        root_logger = logging.getLogger('')
        root_logger.setLevel(logging_level)
        if stream is not None:
            Logger.__console_h = logging.StreamHandler(stream)
            Logger.__console_h.setLevel(logging_level)
            Logger.__console_h.setFormatter(formatter)
            root_logger.addHandler(Logger.__console_h)
        if file_path is not None:
            Logger.__file_h = logging.FileHandler(file_path)
            Logger.__file_h.setLevel(logging_level)
            Logger.__file_h.setFormatter(formatter)
            root_logger.addHandler(Logger.__file_h)
        return

    @staticmethod
    def stop():
        """Set the default values in the logging system"""
        root_logger = logging.getLogger()
        if Logger.__console_h is not None:
            root_logger.removeHandler(Logger.__console_h)
            Logger.__console_h.close()
        if Logger.__file_h is not None:
            root_logger.removeHandler(Logger.__file_h)
            Logger.__file_h.close()
        root_logger.setLevel(Logger.__default_root_log_level)
        return