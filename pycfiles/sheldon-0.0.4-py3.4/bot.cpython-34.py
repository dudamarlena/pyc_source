# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/sheldon/bot.py
# Compiled at: 2015-11-23 23:13:27
# Size of source mod 2**32: 5077 bytes
"""
@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""
import time, _thread as thread, schedule
from sheldon import adapter
from sheldon import config
from sheldon import exceptions
from sheldon import manager
from sheldon import storage
from sheldon.utils import logger

class Sheldon:
    __doc__ = '\n    Main class of the bot.\n    Run script creating new instance of this class and run it.\n    '

    def __init__(self, command_line_arguments):
        """
        Function for loading bot.

        :param command_line_arguments: dict, arguments for start script
        :return:
        """
        self._load_config(command_line_arguments)
        self._load_storage()
        self._load_adapter(command_line_arguments)
        self._load_plugins()

    def _load_config(self, command_line_arguments):
        """
        Create and load bot config.

        :param command_line_arguments: dict, arguments for creating config:
                                       config-prefix - prefix of environment
                                                       variables.
                                                       Default - 'SHELDON_'
        :return:
        """
        self.config = config.Config(prefix=command_line_arguments['config-prefix'])
        if not self.config:
            logger.info_message('Quiting')
            exit()

    def _load_storage(self):
        """
        Connect to bot storage in Redis

        :return:
        """
        self.storage = storage.Storage(self)

    def _load_adapter(self, command_line_arguments):
        """
        Load adapter.

        :param command_line_arguments: dict, arguments for creating config:
                                       adapter - name of adapter.
                                                 May be local package in
                                                 adapters folder or package
                                                 from PyPi.
                                                 Default - 'console'.
        :return:
        """
        self.adapter = adapter.load_adapter(command_line_arguments['adapter'])
        if not self.adapter:
            logger.info_message('Quiting')
            exit()
        for variable in self.adapter.config.variables:
            if variable not in self.config.variables:
                self.config.variables[variable] = self.adapter.config.variables[variable]
                continue

    def _load_plugins(self):
        """
        Load plugins from plugins folder or PyPi using plugins manager.
        
        :return:
        """
        self.plugins_manager = manager.PluginsManager(self.config)
        self.plugins_manager.load_plugins()
        for plugin in self.plugins_manager.plugins:
            for variable in plugin.config.variables:
                if variable not in self.config.variables:
                    self.config.variables[variable] = plugin.config.variables[variable]
                    continue

    def start(self):
        """
        Start getting, parsing and answering messages

        :return:
        """
        thread.start_new_thread(self.start_interval_hooks, ())
        for message in self.adapter.module.get_messages(self):
            hook = self.parse_message(message)
            if hook:
                hook.call(message, self)
                continue

    def parse_message(self, message):
        """
        Check message for all hooks of plugins

        :param message: IncomingMessage object
        :return: Hook object or None
        """
        found_hooks = []
        for plugin in self.plugins_manager.plugins:
            hook = plugin.check_hooks(message)
            if hook is not None:
                found_hooks.append(hook)
                continue

        if found_hooks:
            found_hooks.sort(key=lambda h: h.priority, reverse=True)
            return found_hooks[0]
        else:
            return

    def start_interval_hooks(self):
        """
        Start all interval hooks in plugins using schedule module

        :return:
        """
        for plugin in self.plugins_manager.plugins:
            for hook in plugin.interval_hooks:
                hook.interval.do(lambda : hook.call(self))

        while True:
            schedule.run_pending()
            time.sleep(1)

    @exceptions.catch_module_errors
    def send_message(self, message):
        """
        Send outgoing message from plugin

        :param message: OutgoingMessage object
        :return:
        """
        self.adapter.module.send_message(message, self)