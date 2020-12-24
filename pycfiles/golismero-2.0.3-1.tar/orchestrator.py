# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/main/orchestrator.py
# Compiled at: 2014-01-07 11:03:17
"""
Orchestrator, the manager of everything, core of GoLismero.

All messages go through here before being dispatched to their destinations.
Most other tasks are delegated from here to other managers.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'Orchestrator']
from .console import Console
from .scope import DummyScope
from ..api.config import Config
from ..api.logger import Logger
from ..database.cachedb import PersistentNetworkCache, VolatileNetworkCache
from ..managers.auditmanager import AuditManager
from ..managers.pluginmanager import PluginManager
from ..managers.uimanager import UIManager
from ..managers.rpcmanager import RPCManager
from ..managers.processmanager import ProcessManager, PluginContext
from ..managers.networkmanager import NetworkManager
from ..messaging.codes import MessageType, MessageCode, MessagePriority
from ..messaging.message import Message
from os import getpid
from thread import get_ident
from traceback import format_exc, print_exc
from signal import signal, SIGINT, SIG_DFL
from multiprocessing import Manager

class Orchestrator(object):
    """
    Orchestrator, the manager of everything, core of GoLismero.

    All messages go through here before being dispatched to
    their destinations. Most other tasks are delegated from
    here to other managers.
    """

    def __init__(self, config):
        """
        Start the Orchestrator.

        :param config: configuration of orchestrator.
        :type config: OrchestratorConfig
        """
        self.__config = config
        if getattr(config, 'max_concurrent', 0) <= 0:
            from Queue import Queue
            self.__queue = Queue(maxsize=0)
        else:
            self.__queue_manager = Manager()
            self.__queue = self.__queue_manager.Queue()
        self.__context = PluginContext(orchestrator_pid=getpid(), orchestrator_tid=get_ident(), msg_queue=self.__queue, audit_config=self.__config)
        Config._context = self.__context
        PluginContext._orchestrator = self
        self.__pluginManager = PluginManager(self)
        Console.level = self.config.verbose
        Console.use_colors = self.config.color
        success, failure = self.pluginManager.find_plugins(self.config)
        if not success:
            raise RuntimeError('Failed to find any plugins!')
        ui_plugin_id = 'ui/%s' % self.config.ui_mode
        try:
            self.pluginManager.get_plugin_by_id(ui_plugin_id)
        except KeyError:
            raise ValueError('No plugin found for UI mode: %r' % self.config.ui_mode)

        self.pluginManager.load_plugin_by_id(ui_plugin_id)
        for plugin_id, plugin_args in self.config.plugin_args.iteritems():
            self.pluginManager.set_plugin_args(plugin_id, plugin_args)

        self.__ui = UIManager(self)
        self.__netManager = NetworkManager(self.__config)
        if self.__config.use_cache_db or self.__config.use_cache_db is None:
            self.__cache = PersistentNetworkCache()
        else:
            self.__cache = VolatileNetworkCache()
        self.__rpcManager = RPCManager(self)
        self.__processManager = ProcessManager(self)
        self.__processManager.start()
        self.__auditManager = AuditManager(self)
        return

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    @property
    def config(self):
        """
        :returns: Orchestrator config.
        :rtype: Orchestratorconfig
        """
        return self.__config

    @property
    def pluginManager(self):
        """
        :returns: Plugin manager.
        :rtype: PluginManager
        """
        return self.__pluginManager

    @property
    def netManager(self):
        """
        :returns: Network manager.
        :rtype: NetworkManager
        """
        return self.__netManager

    @property
    def cacheManager(self):
        """
        :returns: Cache manager.
        :rtype: AbstractNetworkCache
        """
        return self.__cache

    @property
    def rpcManager(self):
        """
        :returns: RPC manager.
        :rtype: RPCManager
        """
        return self.__rpcManager

    @property
    def processManager(self):
        """
        :returns: Process manager.
        :rtype: ProcessManager
        """
        return self.__processManager

    @property
    def auditManager(self):
        """
        :returns: Audit manager.
        :rtype: AuditManager
        """
        return self.__auditManager

    @property
    def uiManager(self):
        """
        :returns: UI manager.
        :rtype: UIManager
        """
        return self.__ui

    def __control_c_handler(self, signum, frame):
        """
        Signal handler to catch Control-C interrupts.
        """
        try:
            Console.display('User cancel requested, stopping all audits...')
            message = Message(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_STOP, message_info=False, priority=MessagePriority.MSG_PRIORITY_HIGH)
            try:
                self.__queue.put_nowait(message)
            except:
                exit(1)

        finally:
            signal(SIGINT, self.__panic_control_c_handler)

    def __panic_control_c_handler(self, signum, frame):
        """
        Emergency signal handler to catch Control-C interrupts.
        """
        try:
            try:
                self.processManager.stop()
            except Exception:
                exit(1)

        finally:
            try:
                action, self.__old_signal_action = self.__old_signal_action, SIG_DFL
            except AttributeError:
                action = SIG_DFL

            signal(SIGINT, action)

    def dispatch_msg(self, message):
        """
        Process messages from audits or from the message queue, and send them
        forward to the plugins through the Message Manager when appropriate.

        :param message: Incoming message.
        :type message: Message
        """
        if not isinstance(message, Message):
            raise TypeError('Expected Message, got %r instead' % type(message))
        try:
            if message.audit_name and not self.auditManager.has_audit(message.audit_name):
                print 'Internal error: dropped message for audit %r: %r' % (
                 message.audit_name, message)
                return
            if message.message_type == MessageType.MSG_TYPE_RPC:
                self.__rpcManager.execute_rpc(message.audit_name, message.message_code, *message.message_info)
            elif message.message_type == MessageType.MSG_TYPE_CONTROL and message.message_code == MessageCode.MSG_CONTROL_STOP_AUDIT:
                self.uiManager.dispatch_msg(message)
                self.auditManager.dispatch_msg(message)
                Logger.log_verbose('Audit finished: %s' % message.audit_name)
            else:
                self.auditManager.dispatch_msg(message)
                self.uiManager.dispatch_msg(message)
        finally:
            if message.message_type == MessageType.MSG_TYPE_CONTROL and message.message_code == MessageCode.MSG_CONTROL_STOP:
                if message.message_info:
                    exit(0)
                else:
                    raise KeyboardInterrupt()

    def enqueue_msg(self, message):
        """
        Put messages into the message queue.

        :param message: incoming message
        :type message: Message
        """
        if not isinstance(message, Message):
            raise TypeError('Expected Message, got %r instead' % type(message))
        if message.priority == MessagePriority.MSG_PRIORITY_HIGH and Config._has_context and getpid() == Config._context._orchestrator_pid:
            self.dispatch_msg(message)
        else:
            try:
                self.__queue.put_nowait(message)
            except Exception:
                exit(1)

    def build_plugin_context(self, audit_name, plugin, ack_identity):
        """
        Prepare a PluginContext object to pass to the plugins.

        :param audit_name: Name of the audit.
        :type audit_name: str

        :param plugin: Plugin instance.
        :type plugin: Plugin

        :param ack_identity: Identity hash of the current input data.
        :type ack_identity: str

        :returns: OOP plugin execution context.
        :rtype: PluginContext
        """
        if audit_name:
            audit = self.auditManager.get_audit(audit_name)
            audit_config = audit.config
            audit_scope = audit.scope
            pluginManager = audit.pluginManager
        else:
            audit_config = self.config
            audit_scope = DummyScope()
            pluginManager = self.pluginManager
        info = pluginManager.get_plugin_info_from_instance(plugin)[1]
        return PluginContext(orchestrator_pid=self.__context._orchestrator_pid, orchestrator_tid=self.__context._orchestrator_tid, msg_queue=self.__queue, ack_identity=ack_identity, plugin_info=info, audit_name=audit_name, audit_config=audit_config, audit_scope=audit_scope)

    def run(self, *audits):
        """
        Message loop.

        Optionally start new audits passed as positional arguments.
        """
        try:
            self.uiManager.start()
            for audit_config in audits:
                message = Message(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_START_AUDIT, message_info=audit_config, priority=MessagePriority.MSG_PRIORITY_HIGH)
                self.enqueue_msg(message)

            self.__old_signal_action = signal(SIGINT, self.__control_c_handler)
            while True:
                try:
                    try:
                        message = self.__queue.get()
                    except Exception:
                        exit(1)

                    self.dispatch_msg(message)
                except Exception:
                    Logger.log_error('Error processing message!\n%s' % format_exc())

        finally:
            try:
                self.uiManager.stop()
            except Exception:
                print_exc()

    def close(self):
        """
        Release all resources held by the Orchestrator.
        """
        try:
            try:
                try:
                    try:
                        try:
                            try:
                                self.processManager.stop()
                            finally:
                                pass

                        finally:
                            self.auditManager.close()

                    finally:
                        self.cacheManager.compact()

                finally:
                    self.cacheManager.close()

            finally:
                self.pluginManager.close()

        finally:
            Config._context = None
            self.__auditManager = None
            self.__cache = None
            self.__config = None
            self.__netManager = None
            self.__pluginManager = None
            self.__processManager = None
            self.__rpcManager = None
            self.__queue = None
            self.__queue_manager = None
            self.__ui = None

        return