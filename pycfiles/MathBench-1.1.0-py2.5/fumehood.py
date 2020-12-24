# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathbench/lab/fumehood.py
# Compiled at: 2008-03-15 12:42:07
"""
Define a nice way to show the messages sent to be logged.

NOTE: not used yet
"""
import wx, logging, logging.handlers
from mathbench.basement.logging_utils import CreateLogger

class FumeHoodLogHandler(logging.StreamHandler):
    """
        A log handler that will display the logged messages (above a
        certain priprity level) in GUI windows.
        """

    def __init__(self):
        """
                Initialisation
                """
        logging.StreamHandler.__init__(self)
        self.handle_mapping = {logging.CRITICAL: self.TriggerCritical, 
           logging.ERROR: self.TriggerError, 
           logging.WARNING: self.TriggerWarning, 
           logging.INFO: self.TriggerInfo}

    def handle(self, record):
        """
                React to the record according to its priority level.
                """
        if self.handle_mapping.has_key(record.levelno):
            self.handle_mapping[record.levelno](record)
        logging.StreamHandler.handle(self, record)

    def TriggerWarning(self, record):
        """
                mouf
                """
        dialog = wx.MessageBox(record.getMessage(), caption='Warning', style=wx.OK | wx.ICON_WARNING)

    def TriggerError(self, record):
        """
                Trigger the info contained in a record of level ERROR.
                """
        dialog = wx.MessageBox(record.getMessage(), caption='Error !', style=wx.OK | wx.ICON_ERROR)

    def TriggerInfo(self, record):
        """
                Trigger the info contained in a record of level INFO.
                """
        dialog = wx.MessageBox(record.getMessage(), caption='Information...', style=wx.OK | wx.ICON_INFORMATION)

    def TriggerCritical(self, record):
        """
                Trigger the info contained in a record of level CRITICAL.
                """
        dialog = wx.MessageBox(record.getMessage(), caption='Critical Error !', style=wx.OK | wx.ICON_STOP)


if 'fumehood' in __name__ or __name__ == '__main__':
    __log_handler = FumeHoodLogHandler()
    __MB_LOGGER = CreateLogger(__log_handler)

    def debug(text):
        return __MB_LOGGER.debug(text)


    def info(text):
        return __MB_LOGGER.info(text)


    def warn(text):
        return __MB_LOGGER.warn(text)


    def critical(text):
        return __MB_LOGGER.critical(text)


    def log(text):
        return __MB_LOGGER.log(text)


    def error(text):
        return __MB_LOGGER.error(text)


def log_function_call(func):
    """
        Send a message each time the decorated function is called.

        This nifty decorator is very usefull to trace the function calls
        """

    def wrapper(*args, **kwargs):
        debug('Called func.: %s (defined in %s)' % (func.__name__, func.code.co_filename))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__dict__.update(func.__dict__)
    return wrapper


if __name__ == '__main__':
    app = wx.PySimpleApp()
    debug('debug message')
    info('info message')
    warn('warn message')
    error('error message')
    critical('critical message')
    app.MainLoop()