# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: microdrop\logger.py
# Compiled at: 2016-08-22 17:19:26
import logging, logging.handlers
from plugin_manager import ILoggingPlugin
import plugin_manager

class CustomHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        if record.levelname == 'DEBUG':
            plugin_manager.emit_signal('on_debug', [record], interface=ILoggingPlugin)
        elif record.levelname == 'INFO':
            plugin_manager.emit_signal('on_info', [record], interface=ILoggingPlugin)
        elif record.levelname == 'WARNING':
            plugin_manager.emit_signal('on_warning', [record], interface=ILoggingPlugin)
        elif record.levelname == 'ERROR':
            plugin_manager.emit_signal('on_error', [record], interface=ILoggingPlugin)
        elif record.levelname == 'CRITICAL':
            plugin_manager.emit_signal('on_critical', [record], interface=ILoggingPlugin)


logger = logging.getLogger()