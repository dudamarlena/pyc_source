# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/managers/logs.py
# Compiled at: 2020-05-13 19:27:59
# Size of source mod 2**32: 1319 bytes
"""
Module that contains implementation to handle DCC logs themes
"""
import os, logging, tpDcc
from tpDcc import register
from tpDcc.libs.python import decorators

class LogsManager(object):

    def __init__(self):
        super(LogsManager, self).__init__()

    def get_logger(self, tool_id=None):
        """
        Returns logger associated with given tool
        :param tool_id: str
        :return:
        """
        if not tool_id:
            return logging.getLogger('tpDcc')
        else:
            tool_data = tpDcc.ToolsMgr().get_plugin_data_from_id(tool_id)
            if not tool_data:
                return logging.getLogger('tpDcc')
            logging_file = tool_data.get('logging_file', None)
            if not logging_file:
                return logging.getLogger('tpDcc')
            logging.config.fileConfig(logging_file, disable_existing_loggers=False)
            return logging.getLogger(tool_id)


@decorators.Singleton
class LogsManagerSingleton(LogsManager, object):
    __doc__ = '\n    Singleton class that holds logs manager instance\n    '

    def __init__(self):
        LogsManager.__init__(self)


register.register_class('LogsMgr', LogsManagerSingleton)