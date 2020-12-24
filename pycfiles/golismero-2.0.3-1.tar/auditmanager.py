# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/managers/auditmanager.py
# Compiled at: 2014-02-10 15:24:09
"""
Manager for audits.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'AuditManager', 'Audit', 'AuditException']
from .importmanager import ImportManager
from .processmanager import PluginContext
from .reportmanager import ReportManager
from .rpcmanager import implementor
from ..api.data import Data
from ..api.data.resource import Resource
from ..api.config import Config
from ..api.logger import Logger
from ..api.plugin import STAGES
from ..common import AuditConfig
from ..database.auditdb import AuditDB
from ..main.scope import AuditScope, DummyScope
from ..messaging.codes import MessageType, MessageCode, MessagePriority
from ..messaging.message import Message
from ..messaging.notifier import AuditNotifier
from collections import defaultdict
from warnings import catch_warnings, warn
from time import time
from traceback import format_exc

@implementor(MessageCode.MSG_RPC_AUDIT_COUNT)
def rpc_audit_get_count(orchestrator, current_audit_name):
    return orchestrator.auditManager.get_audit_count()


@implementor(MessageCode.MSG_RPC_AUDIT_NAMES)
def rpc_audit_get_names(orchestrator, current_audit_name):
    return orchestrator.auditManager.get_audit_names()


@implementor(MessageCode.MSG_RPC_AUDIT_CONFIG)
def rpc_audit_get_config(orchestrator, current_audit_name, audit_name=None):
    if audit_name:
        return orchestrator.auditManager.get_audit(audit_name).config
    return orchestrator.config


@implementor(MessageCode.MSG_RPC_AUDIT_TIMES)
def rpc_audit_get_times(orchestrator, current_audit_name, audit_name=None):
    if not audit_name:
        audit_name = current_audit_name
    return orchestrator.auditManager.get_audit(audit_name).database.get_audit_times()


@implementor(MessageCode.MSG_RPC_AUDIT_STATS)
def rpc_audit_get_stats(orchestrator, current_audit_name, audit_name=None):
    if not audit_name:
        audit_name = current_audit_name
    return orchestrator.auditManager.get_audit(audit_name).get_runtime_stats()


@implementor(MessageCode.MSG_RPC_AUDIT_SCOPE)
def rpc_audit_get_scope(orchestrator, current_audit_name, audit_name=None):
    if audit_name:
        return orchestrator.auditManager.get_audit(audit_name).scope
    return DummyScope()


class AuditException(Exception):
    """Exception for audits"""
    pass


class AuditManager(object):
    """
    Manage and control audits.
    """

    def __init__(self, orchestrator):
        """
        :param orchestrator: Core to send messages to.
        :type orchestrator: Orchestrator
        """
        self.__audits = dict()
        self.__orchestrator = orchestrator

    @property
    def orchestrator(self):
        """
        :returns: Orchestrator instance.
        :rtype: Orchestrator
        """
        return self.__orchestrator

    def new_audit(self, audit_config):
        """
        Creates a new audit.

        :param audit_config: Parameters of the audit.
        :type audit_config: AuditConfig

        :returns: Newly created audit.
        :rtype: Audit
        """
        if not isinstance(audit_config, AuditConfig):
            raise TypeError('Expected AuditConfig, got %r instead' % type(audit_config))
        self.orchestrator.uiManager.check_params(audit_config)
        audit = Audit(audit_config, self.orchestrator)
        self.__audits[audit.name] = audit
        if audit.is_new:
            Logger.log('Audit name: %s' % audit.name)
        else:
            Logger.log_verbose('Audit name: %s' % audit.name)
        if hasattr(audit.database, 'filename') and audit.database.filename != ':memory:':
            Logger.log_verbose('Audit database: %s' % audit.database.filename)
        try:
            audit.run()
            return audit
        except Exception as e:
            tb = format_exc()
            try:
                self.remove_audit(audit.name)
            except Exception:
                pass

            Logger.log_error(str(e))
            Logger.log_error_more_verbose(tb)
            raise AuditException('Failed to add new audit, reason: %s' % e)

    def get_audit_count(self):
        """
        Get the number of currently running audits.

        :returns: Number of currently running audits.
        :rtype: int
        """
        return len(self.__audits)

    def get_audit_names(self):
        """
        Get the names of the currently running audits.

        :returns: Audit names.
        :rtype: set(str)
        """
        return {audit.name for audit in self.__audits}

    def get_all_audits(self):
        """
        Get the currently running audits.

        :returns: Mapping of audit names to instances.
        :rtype: dict(str -> Audit)
        """
        return self.__audits

    def has_audit(self, name):
        """
        Check if there's an audit with the given name.

        :param name: Audit name.
        :type name: str

        :returns: True if the audit exists, False otherwise.
        :rtype: bool
        """
        return name in self.__audits

    def get_audit(self, name):
        """
        Get an instance of an audit by its name.

        :param name: Audit name.
        :type name: str

        :returns: Audit instance.
        :rtype: Audit

        :raises KeyError: No audit exists with that name.
        """
        return self.__audits[name]

    def remove_audit(self, name):
        """
        Delete an instance of an audit by its name.

        :param name: Audit name.
        :type name: str

        :raises KeyError: No audit exists with that name.
        """
        try:
            self.orchestrator.netManager.release_all_slots(name)
        finally:
            try:
                audit = self.__audits[name]
                try:
                    audit.close()
                finally:
                    del self.__audits[name]

            finally:
                self.orchestrator.cacheManager.clean(name)

    def dispatch_msg(self, message):
        """
        Process an incoming message from the Orchestrator.

        :param message: Incoming message.
        :type message: Message
        """
        if not isinstance(message, Message):
            raise TypeError('Expected Message, got %r instead' % type(message))
        if message.message_type == MessageType.MSG_TYPE_DATA:
            if not message.audit_name:
                raise ValueError('Data message with no target audit!')
            self.get_audit(message.audit_name).dispatch_msg(message)
        elif message.message_type == MessageType.MSG_TYPE_CONTROL:
            if message.message_code == MessageCode.MSG_CONTROL_ACK:
                if message.audit_name:
                    self.get_audit(message.audit_name).acknowledge(message)
            elif message.message_code == MessageCode.MSG_CONTROL_START_AUDIT:
                try:
                    self.new_audit(message.message_info)
                except AuditException as e:
                    tb = format_exc()
                    message = Message(message_type=MessageType.MSG_TYPE_STATUS, message_code=MessageCode.MSG_STATUS_AUDIT_ABORTED, message_info=(
                     message.message_info.audit_name,
                     str(e), tb), priority=MessagePriority.MSG_PRIORITY_HIGH, audit_name=None)
                    self.orchestrator.enqueue_msg(message)

            elif message.message_code == MessageCode.MSG_CONTROL_STOP_AUDIT:
                if not message.audit_name:
                    raise ValueError("I don't know which audit to stop...")
                self.get_audit(message.audit_name).close()
                self.remove_audit(message.audit_name)
            elif message.message_code == MessageCode.MSG_CONTROL_LOG:
                if message.audit_name:
                    self.get_audit(message.audit_name).dispatch_msg(message)
        return

    def close(self):
        """
        Release all resources held by all audits.
        """
        self.__orchestrator = None
        for name in self.__audits.keys():
            try:
                self.remove_audit(name)
            except:
                pass

        return


class Audit(object):
    """
    Instance of an audit, with its custom parameters,
    scope, target, plugins, etc.
    """

    def __init__(self, audit_config, orchestrator):
        """
        :param audit_config: Audit configuration.
        :type audit_config: AuditConfig

        :param orchestrator: Orchestrator instance that will receive messages
            sent by this audit.
        :type orchestrator: Orchestrator
        """
        if not isinstance(audit_config, AuditConfig):
            raise TypeError('Expected AuditConfig, got %r instead' % type(audit_config))
        self.__audit_config = audit_config
        self.__orchestrator = orchestrator
        self.__current_stage = orchestrator.pluginManager.min_stage
        self.__is_report_started = False
        self.__must_update_stop_time = True
        self.__followed_links = 0
        self.__show_max_links_warning = True
        self.__expecting_ack = 0
        self.__stage_cycles = defaultdict(int)
        self.__processed_count = 0
        self.__total_count = 0
        self.__stages_enabled = tuple()
        self.__notifier = None
        self.__plugin_manager = None
        self.__import_manager = None
        self.__report_manager = None
        self.__is_new = not audit_config.audit_name or audit_config.audit_db == ':auto:'
        self.__database = AuditDB(audit_config)
        self.__name = self.__database.audit_name
        return

    @property
    def name(self):
        """
        :returns: Name of the audit.
        :rtype: str
        """
        return self.__name

    @property
    def is_new(self):
        """
        :returns: True if the audit is new, False if it's a reopened audit.
        :rtype: bool
        """
        return self.__is_new

    @property
    def orchestrator(self):
        """
        :returns: Orchestrator instance that will receive messages
            sent by this audit.
        :rtype: Orchestrator
        """
        return self.__orchestrator

    @property
    def config(self):
        """
        :returns: Audit configuration.
        :rtype: AuditConfig
        """
        return self.__audit_config

    @property
    def scope(self):
        """
        :returns: Audit scope.
        :rtype: AuditScope
        """
        return self.__audit_scope

    @property
    def database(self):
        """
        :returns: Audit database.
        :rtype: AuditDB
        """
        return self.__database

    @property
    def pluginManager(self):
        """
        :returns: Audit plugin manager.
        :rtype: AuditPluginManager
        """
        return self.__plugin_manager

    @property
    def importManager(self):
        """
        :returns: Import manager.
        :rtype: ImportManager
        """
        return self.__import_manager

    @property
    def reportManager(self):
        """
        :returns: Report manager.
        :rtype: ReportManager
        """
        return self.__report_manager

    @property
    def expecting_ack(self):
        """
        :returns: Number of ACKs expected by this audit.
        :rtype: int
        """
        return self.__expecting_ack

    @property
    def current_stage(self):
        """
        :returns: Current execution stage.
        :rtype: int
        """
        return self.__current_stage

    @property
    def is_report_started(self):
        """
        :returns: True if report generation has started, False otherwise.
        :rtype: bool
        """
        return self.__is_report_started

    def get_runtime_stats(self):
        r"""
        Returns a dictionary with runtime statistics with at least the
        following keys:

         - "current_stage": [int]
           Current stage number.
         - "total_count": [int]
           Total number of data objects to process in this stage.
         - "processed_count": [int]
           Number of data objects already processed in this stage.
         - "stage_cycles": [dict(int -> int)]
           Map of stage numbers and times each stage ran.
         - "stages_enabled": [tuple(int)]
           Stages enabled for this audit.

        Future versions of GoLismero may include more keys.

        :returns: Runtime statistics.
        :rtype: dict(str -> \*)
        """
        return {'current_stage': self.__current_stage, 
           'total_count': self.__total_count, 
           'processed_count': self.__processed_count, 
           'stage_cycles': dict(self.__stage_cycles), 
           'stages_enabled': self.__stages_enabled}

    def run(self):
        """
        Start execution of an audit.
        """
        start_time = time()
        self.__expecting_ack = 0
        old_context = Config._context
        try:
            self.__audit_scope = DummyScope()
            Config._context = PluginContext(msg_queue=old_context.msg_queue, audit_name=self.name, audit_config=self.config, audit_scope=self.scope, orchestrator_pid=old_context._orchestrator_pid, orchestrator_tid=old_context._orchestrator_tid)
            self.__plugin_manager = self.orchestrator.pluginManager.get_plugin_manager_for_audit(self)
            self.__plugin_manager.initialize(self.config)
            testing_plugins = self.pluginManager.load_plugins('testing')
            self.__notifier = AuditNotifier(self)
            self.__notifier.add_multiple_plugins(testing_plugins)
            self.__stages_enabled = sorted(stage_num for stage, stage_num in STAGES.iteritems() if self.pluginManager.get_plugins(stage))
            self.__import_manager = ImportManager(self.orchestrator, self)
            self.__report_manager = ReportManager(self.orchestrator, self)
            audit_scope = self.database.get_audit_scope()
            if audit_scope is None:
                if self.config.targets:
                    audit_scope = AuditScope(self.config)
            else:
                audit_scope.add_targets(self.config)
            if audit_scope is not None:
                self.__audit_scope = audit_scope
                self.database.save_audit_scope(self.scope)
                Config._context = PluginContext(msg_queue=old_context.msg_queue, audit_name=self.name, audit_config=self.config, audit_scope=self.scope, orchestrator_pid=old_context._orchestrator_pid, orchestrator_tid=old_context._orchestrator_tid)
            if not self.database.get_audit_times()[0]:
                self.database.set_audit_start_time(start_time)
            count = self.database.get_data_count()
            if count:
                Logger.log_verbose('Found %d objects in database' % count)
            target_data = self.scope.get_targets()
            targets_added_count = 0
            for data in target_data:
                if not self.database.has_data_key(data.identity, data.data_type):
                    self.database.add_data(data)
                    targets_added_count += 1

            if targets_added_count:
                Logger.log_verbose('Added %d new targets to the database.' % targets_added_count)
            self.database.clear_all_stage_marks()
            imported_count = 0
            if self.importManager.is_enabled:
                self.send_msg(message_type=MessageType.MSG_TYPE_STATUS, message_code=MessageCode.MSG_STATUS_STAGE_UPDATE, message_info='import', priority=MessagePriority.MSG_PRIORITY_HIGH)
                if not target_data:
                    target_types = (Resource.RESOURCE_BASE_URL,
                     Resource.RESOURCE_FOLDER_URL,
                     Resource.RESOURCE_URL,
                     Resource.RESOURCE_IP,
                     Resource.RESOURCE_DOMAIN)
                    old_data = set()
                    for data_subtype in target_types:
                        old_data.update(self.database.get_data_keys(Data.TYPE_RESOURCE, data_subtype))

                imported_count = self.importManager.import_results()
                if not target_data:
                    new_data = set()
                    for data_subtype in target_types:
                        new_data.update(self.database.get_data_keys(Data.TYPE_RESOURCE, data_subtype))

                    new_data.difference_update(old_data)
                    old_data.clear()
                    self.config.targets = [ str(self.database.get_data(identity)) for identity in new_data
                                          ]
                    new_data.clear()
                    self.__audit_scope = AuditScope(self.config)
                    self.database.save_audit_scope(self.scope)
                    Config._context = PluginContext(msg_queue=old_context.msg_queue, audit_name=self.name, audit_config=self.config, audit_scope=self.scope, orchestrator_pid=old_context._orchestrator_pid, orchestrator_tid=old_context._orchestrator_tid)
                    target_data = self.scope.get_targets()
                    targets_added_count = 0
                    for data in target_data:
                        if not self.database.has_data_key(data.identity):
                            self.database.add_data(data)
                            targets_added_count += 1

                    if targets_added_count:
                        Logger.log_verbose('Added %d new targets to the database.' % targets_added_count)
            Logger.log_more_verbose(str(self.scope))
            if not not isinstance(self.scope, DummyScope):
                raise AssertionError('Internal error!')
                raise (self.scope.targets or ValueError)('No targets selected for audit, aborting execution.')
            existing = self.database.get_data_keys()
            stack = list(existing)
            visited = set()
            while stack:
                identity = stack.pop()
                if identity not in visited:
                    visited.add(identity)
                    data = self.database.get_data(identity)
                    if data.is_in_scope():
                        for data in data.discovered:
                            identity = data.identity
                            if identity not in existing and data.is_in_scope():
                                self.database.add_data(data)
                                existing.add(identity)
                                stack.append(identity)

            del existing
            del visited
        finally:
            Config._context = old_context

        self.__must_update_stop_time = imported_count or targets_added_count
        if testing_plugins:
            Logger.log_verbose('Launching tests...')
            self.update_stage()
        else:
            self.__current_stage = self.__plugin_manager.max_stage + 1
            self.generate_reports()
        return

    def send_msg(self, message_type=MessageType.MSG_TYPE_DATA, message_code=MessageCode.MSG_DATA_REQUEST, message_info=None, priority=MessagePriority.MSG_PRIORITY_MEDIUM):
        """
        Send messages to the Orchestrator.

        :param message_type: Message type.
            Must be one of the constants from MessageType.
        :type mesage_type: int

        :param message_code: Message code.
            Must be one of the constants from MessageCode.
        :type message_code: int

        :param message_info: The payload of the message.
            Its type depends on the message type and code.
        :type message_info: *

        :param priority: Priority level.
            Must be one of the constants from MessagePriority.
        :type priority: int
        """
        m = Message(message_type=message_type, message_code=message_code, message_info=message_info, audit_name=self.name, priority=priority)
        self.orchestrator.enqueue_msg(m)

    def acknowledge(self, message):
        """
        Got an ACK for a message sent from this audit to the plugins.

        :param message: The message with the ACK.
        :type message: Message
        """
        try:
            self.__expecting_ack -= 1
            self.__notifier.acknowledge(message)
        finally:
            if not self.expecting_ack:
                self.update_stage()

    def update_stage(self):
        """
        Sets the current stage to the minimum needed to process pending data.
        When the last stage is completed, sends the audit stop message.
        """
        database = self.database
        pluginManager = self.pluginManager
        if self.__is_report_started:
            self.__report_manager.generate_screen_report(self.orchestrator.uiManager.notifier)
            self.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_STOP_AUDIT, message_info=True)
        else:
            for stage in xrange(pluginManager.min_stage, pluginManager.max_stage + 1):
                self.__current_stage = stage
                pending = database.get_pending_data(stage)
                if not pending:
                    continue
                if not pluginManager.stages[stage]:
                    database.mark_stage_finished_many(pending, stage)
                    continue
                candidates = list(pending)
                pending.clear()
                for i in xrange(0, len(candidates), 10):
                    batch_ids = set(candidates[i:i + 10])
                    batch = database.get_many_data(batch_ids)
                    if not batch:
                        database.mark_stage_finished_many(batch_ids, stage)
                        continue
                    data_ok = []
                    ids_ok = set()
                    ids_not_ok = set()
                    for data in batch:
                        if data.is_in_scope(self.scope):
                            ids_ok.add(data.identity)
                            data_ok.append(data)
                        else:
                            ids_not_ok.add(data.identity)

                    if ids_not_ok:
                        database.mark_stage_finished_many(ids_not_ok, stage)
                    batch_ids = ids_ok
                    batch = data_ok
                    if not batch:
                        continue
                    if not self.__notifier.is_runnable_stage(batch, stage):
                        database.mark_stage_finished_many(batch_ids, stage)
                        continue
                    pending.update(batch_ids)
                    batch = []

                if not pending:
                    continue
                self.__stage_cycles[self.__current_stage] += 1
                self.__processed_count = 0
                self.__total_count = len(pending)
                self.__must_update_stop_time = True
                stage_name = pluginManager.get_stage_name_from_value(stage)
                self.send_msg(message_type=MessageType.MSG_TYPE_STATUS, message_code=MessageCode.MSG_STATUS_STAGE_UPDATE, message_info=stage_name)
                to_send = list(pending)
                for i in xrange(0, len(to_send), 10):
                    datalist = database.get_many_data(to_send[i:i + 10])
                    self.send_msg(message_type=MessageType.MSG_TYPE_DATA, message_code=MessageCode.MSG_DATA_REQUEST, message_info=datalist)

                return

            self.__current_stage = pluginManager.max_stage + 1
            self.generate_reports()

    def dispatch_msg(self, message):
        """
        Send messages to the plugins of this audit.

        :param message: The message to send.
        :type message: Message
        """
        if not isinstance(message, Message):
            raise TypeError('Expected Message, got %r instead' % type(message))
        old_context = Config._context
        try:
            Config._context = PluginContext(msg_queue=old_context.msg_queue, audit_name=self.name, audit_config=self.config, audit_scope=self.scope, ack_identity=message.ack_identity, orchestrator_pid=old_context._orchestrator_pid, orchestrator_tid=old_context._orchestrator_tid)
            self.__dispatch_msg(message)
        finally:
            Config._context = old_context

    def __dispatch_msg(self, message):
        database = self.database
        pluginManager = self.pluginManager
        if message.message_type == MessageType.MSG_TYPE_CONTROL and message.message_code == MessageCode.MSG_CONTROL_LOG:
            text, level, is_error = message.message_info
            plugin_id = message.plugin_id
            ack_id = message.ack_identity
            timestamp = message.timestamp
            database.append_log_line(text, level, is_error, plugin_id, ack_id, timestamp)
            return
        if message.message_type == MessageType.MSG_TYPE_DATA:
            if isinstance(message.message_info, Data):
                message.message_info = [
                 message.message_info]
            if message.message_code == MessageCode.MSG_DATA_REQUEST:
                launched = self.__notifier.notify(message)
                if launched:
                    self.__expecting_ack += launched
                else:
                    self.__expecting_ack += 1
                    self.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_ACK, priority=MessagePriority.MSG_PRIORITY_LOW)
                self.__processed_count += len(message.message_info)
                return
            if message.message_code == MessageCode.MSG_DATA_RESPONSE:
                data_for_plugins = []
                for data in message.message_info:
                    if not isinstance(data, Data):
                        warn('TypeError: Expected Data, got %r instead' % type(data), RuntimeWarning, stacklevel=3)
                        continue
                    if not database.has_data_key(data.identity):
                        if data.data_type == Data.TYPE_RESOURCE and data.resource_type == Resource.RESOURCE_URL:
                            self.__followed_links += 1
                            if self.config.max_links > 0 and self.__followed_links >= self.config.max_links:
                                if self.__show_max_links_warning:
                                    self.__show_max_links_warning = False
                                    w = 'Maximum number of links (%d) reached! Audit: %s'
                                    w = w % (self.config.max_links, self.name)
                                    with catch_warnings(record=True) as (wlist):
                                        warn(w, RuntimeWarning)
                                    self.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_WARNING, message_info=wlist, priority=MessagePriority.MSG_PRIORITY_HIGH)
                                continue
                    database.add_data(data)
                    if data.is_in_scope():
                        plugin_id = message.plugin_id
                        if plugin_id:
                            plugin_info = pluginManager.get_plugin_by_id(plugin_id)
                            if not plugin_info.recursive:
                                database.mark_plugin_finished(data.identity, plugin_id)
                        data_for_plugins.append(data)
                    else:
                        database.mark_stage_finished(data.identity, pluginManager.max_stage)

                visited = {data.identity for data in data_for_plugins}
                for data in list(data_for_plugins):
                    links = set(data.links)
                    queue = list(data.discovered)
                    links = set(data.links).difference(links)
                    while queue:
                        data = queue.pop(0)
                        if data.identity not in visited and not database.has_data_key(data.identity):
                            database.add_data(data)
                            visited.add(data.identity)
                            queue.extend(data.discovered)
                            if data.is_in_scope():
                                data_for_plugins.append(data)
                            else:
                                database.mark_stage_finished(data.identity, pluginManager.max_stage)

                    if links:
                        database.add_data(data)

                if data_for_plugins and self.current_stage == self.pluginManager.min_stage:
                    self.__total_count += len(data_for_plugins)
                    self.send_msg(message_type=MessageType.MSG_TYPE_DATA, message_code=MessageCode.MSG_DATA_REQUEST, message_info=data_for_plugins)

    def generate_reports(self):
        """
        Start the generation of reports for the audit.
        """
        if self.__is_report_started:
            raise RuntimeError('Why are you asking for the report twice?')
        self.__expecting_ack += 1
        try:
            self.__is_report_started = True
            if self.__must_update_stop_time:
                self.database.set_audit_stop_time(time())
            launched = 0
            if self.__report_manager.plugin_count > 0:
                self.send_msg(message_type=MessageType.MSG_TYPE_STATUS, message_code=MessageCode.MSG_STATUS_STAGE_UPDATE, message_info='report')
                launched = self.__report_manager.generate_reports(self.__notifier)
            if launched:
                self.__expecting_ack += launched
            else:
                self.__expecting_ack += 1
                self.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_ACK, priority=MessagePriority.MSG_PRIORITY_LOW)
        finally:
            self.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_ACK, priority=MessagePriority.MSG_PRIORITY_LOW)

    def close(self):
        """
        Release all resources held by this audit.
        """
        try:
            try:
                try:
                    try:
                        try:
                            if self.database is not None:
                                try:
                                    self.database.compact()
                                finally:
                                    self.database.close()

                        finally:
                            if self.__notifier is not None:
                                self.__notifier.close()

                    finally:
                        if self.__plugin_manager is not None:
                            self.__plugin_manager.close()

                finally:
                    if self.__import_manager is not None:
                        self.__import_manager.close()

            finally:
                if self.__report_manager is not None:
                    self.__report_manager.close()

        finally:
            self.__database = None
            self.__orchestrator = None
            self.__notifier = None
            self.__audit_config = None
            self.__audit_scope = None
            self.__plugin_manager = None
            self.__import_manager = None
            self.__report_manager = None

        return