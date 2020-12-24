# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/managers/processmanager.py
# Compiled at: 2014-01-07 11:03:17
"""
Process manager.

Here's where the process pool is prepared and plugins are launched.
The bootstrapping code for plugins is also here.

Lots of black magic going on, beware of dragons! :)
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'ProcessManager', 'PluginContext']
from ..api.config import Config
from ..api.data import LocalDataCache
from ..api.localfile import LocalFile
from ..api.logger import Logger
from ..api.net.cache import NetworkCache
from ..api.net.http import HTTP
from ..messaging.codes import MessageType, MessageCode, MessagePriority
from ..messaging.message import Message
from imp import load_source
from multiprocessing import Manager
from os import getpid
from thread import get_ident
from threading import Timer
from traceback import format_exc, print_exc, format_exception_only, format_list
from warnings import catch_warnings, simplefilter
import socket, sys
from ..patches import mp
from multiprocessing import Process as _Original_Process
from multiprocessing.pool import Pool as _Original_Pool

class Process(_Original_Process):
    """
    A customized process that forces the 'daemon' property to False.

    This means we have to take care of killing our own subprocesses.
    """

    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass

    @daemon.deleter
    def daemon(self, value):
        pass


class Pool(_Original_Pool):
    """
    A customized process pool that forces the 'daemon' property to False.

    This means we have to take care of killing our own subprocesses.
    """
    Process = Process


plugin_class_cache = dict()

def do_nothing(*args, **kwargs):
    pass


def launcher(queue, max_concurrent, refresh_after_tasks):
    return _launcher(queue, max_concurrent, refresh_after_tasks)


def _launcher(queue, max_concurrent, refresh_after_tasks):
    _init_worker()
    pool = PluginPoolManager(max_concurrent, refresh_after_tasks)
    wait = True
    pool.start()
    try:
        while True:
            try:
                item = queue.get()
            except:
                wait = False
                exit(1)

            if item is True or item is False:
                wait = item
                return
            pool.run_plugin(*item)

    finally:
        try:
            pool.stop(wait)
        except:
            exit(1)


def bootstrap(context, func, args, kwargs):
    return _bootstrap(context, func, args, kwargs)


_do_notify_end = False

def _bootstrap(context, func, args, kwargs):
    global _do_notify_end
    try:
        _do_notify_end = False
        try:
            try:
                plugin_warnings = []
                try:
                    with catch_warnings(record=True) as (plugin_warnings):
                        simplefilter('always')
                        Config._context = context
                        kill_timer = None
                        if Config.audit_config.plugin_timeout:
                            kill_timer = Timer(Config.audit_config.plugin_timeout, _plugin_killer, (context,))
                            kill_timer.start()
                        try:
                            _bootstrap_inner(context, func, args, kwargs)
                        finally:
                            if kill_timer is not None:
                                kill_timer.cancel()

                finally:
                    if plugin_warnings:
                        try:
                            context.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_WARNING, message_info=plugin_warnings, priority=MessagePriority.MSG_PRIORITY_HIGH)
                        except Exception as e:
                            context.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_ERROR, message_info=(
                             str(e), format_exc()), priority=MessagePriority.MSG_PRIORITY_HIGH)

            except Exception as e:
                context.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_ERROR, message_info=(
                 str(e), format_exc()), priority=MessagePriority.MSG_PRIORITY_HIGH)

        finally:
            context.send_ack(_do_notify_end)
            context._depth = -1

    except:
        try:
            context.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_STOP, message_info=False)
        except SystemExit:
            raise
        except:
            try:
                print_exc()
            except:
                pass

        exit(1)

    return


def _bootstrap_inner(context, func, args, kwargs):
    global _do_notify_end
    if func == 'recv_info':
        try:
            input_data = kwargs['info']
        except KeyError:
            input_data = args[0]

        if not input_data.is_in_scope():
            return
        if hasattr(input_data, 'depth'):
            context._depth = input_data.depth
            max_depth = context.audit_config.depth
            if max_depth is not None and max_depth < context._depth:
                Logger.log_error_more_verbose('Maximum crawling depth exceeded! Skipped: %s' % input_data.identity)
                return
    if sys.version_info[:3] >= (2, 7, 5):
        socket.setdefaulttimeout(5.0)
    LocalFile._update_plugin_path()
    HTTP._initialize()
    NetworkCache._clear_local_cache()
    LocalDataCache.on_run()
    if func == 'recv_info':
        LocalDataCache.on_create(input_data)
    cache_key = (
     context.plugin_module, context.plugin_class)
    try:
        cls = plugin_class_cache[cache_key]
    except KeyError:
        mod = load_source('_plugin_tmp_' + context.plugin_class.replace('.', '_'), context.plugin_module)
        cls = getattr(mod, context.plugin_class)
        plugin_class_cache[cache_key] = cls

    instance = cls()
    context.send_msg(message_type=MessageType.MSG_TYPE_STATUS, message_code=MessageCode.MSG_STATUS_PLUGIN_BEGIN)
    _do_notify_end = True
    result = None
    try:
        result = getattr(instance, func)(*args, **kwargs)
    finally:
        if func == 'recv_info':
            result = LocalDataCache.on_finish(result, input_data)
            if result:
                try:
                    context.send_msg(message_type=MessageType.MSG_TYPE_DATA, message_code=MessageCode.MSG_DATA_RESPONSE, message_info=result)
                except Exception as e:
                    context.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_ERROR, message_info=(
                     str(e), format_exc()), priority=MessagePriority.MSG_PRIORITY_HIGH)

    return


def _plugin_killer(context):
    """
    Internally used function that kills a plugin
    when the execution timeout has been reached.

    :param context: Plugin execution context.
    :type context: PluginContext
    """
    try:
        try:
            context.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_ERROR, message_info=('Execution timeout reached.',
                                                                                                                                  ''), priority=MessagePriority.MSG_PRIORITY_HIGH)
        finally:
            context.send_ack(_do_notify_end)
            context._depth = -1

    finally:
        exit(1)


def _init_worker():
    """
    Initializer for pooled processes.
    """
    try:
        import posix
        posix.nice(99)
    except Exception:
        pass


class PluginContext(object):
    """
    Serializable execution context for the plugins.
    """
    _depth = -1

    def __init__(self, msg_queue, ack_identity=None, plugin_info=None, audit_name=None, audit_config=None, audit_scope=None, orchestrator_pid=None, orchestrator_tid=None):
        """
        Serializable execution context for the plugins.

        :param msg_queue: Message queue where to send the responses.
            This argument is mandatory.
        :type msg_queue: Queue

        :param ack_identity: Identity hash of the current input data,
            or None if not running a plugin.
        :type ack_identity: str | None

        :param plugin_info: Plugin information,
            or None if not running a plugin.
        :type plugin_info: PluginInfo | None

        :param audit_name: Name of the audit,
            or None if not running an audit.
        :type audit_name: str | None

        :param audit_config: Parameters of the audit,
            or None if not running an audit.
        :type audit_config: AuditConfig | None

        :param audit_scope: Scope of the audit,
            or None if not running an audit.
        :type audit_scope: AuditScope | None

        :param orchestrator_pid: Process ID of the Orchestrator.
        :type orchestrator_pid: int | None

        :param orchestrator_tid: Main thread ID of the Orchestrator.
        :type orchestrator_tid: int | None
        """
        self.__msg_queue = msg_queue
        self.__ack_identity = ack_identity
        self.__plugin_info = plugin_info
        self.__audit_name = audit_name
        self.__audit_config = audit_config
        self.__audit_scope = audit_scope
        self.__orchestrator_pid = orchestrator_pid
        self.__orchestrator_tid = orchestrator_tid

    @property
    def msg_queue(self):
        """"
        :returns: Message queue where to send the responses.
        :rtype: str
        """
        return self.__msg_queue

    @property
    def audit_name(self):
        """"
        :returns: Name of the audit, or None if not running an audit.
        :rtype: str | None
        """
        return self.__audit_name

    @property
    def audit_config(self):
        """"
        :returns: Parameters of the audit, or None if not running an audit.
        :rtype: AuditConfig | None
        """
        return self.__audit_config

    @property
    def audit_scope(self):
        """"
        :returns: Scope of the audit, or None if not running an audit.
        :rtype: AuditScope | None
        """
        return self.__audit_scope

    @property
    def ack_identity(self):
        """"
        :returns: Identity hash of the current input data, or None if not running a plugin.
        :rtype: str | None
        """
        return self.__ack_identity

    @property
    def plugin_info(self):
        """"
        :returns: Plugin information, or None if not running a plugin.
        :rtype: str | None
        """
        return self.__plugin_info

    @property
    def plugin_id(self):
        """"
        :returns: Plugin ID, or None if not running a plugin.
        :rtype: str | None
        """
        if self.__plugin_info:
            return self.__plugin_info.plugin_id

    @property
    def plugin_module(self):
        """"
        :returns: Module where the plugin is to be loaded from, or None if not running a plugin.
        :rtype: str | None
        """
        if self.__plugin_info:
            return self.__plugin_info.plugin_module

    @property
    def plugin_class(self):
        """"
        :returns: Class name of the plugin, or None if not running a plugin.
        :rtype: str | None
        """
        if self.__plugin_info:
            return self.__plugin_info.plugin_class

    @property
    def plugin_config(self):
        """"
        :returns: Plugin configuration, or None if not running a plugin.
        :rtype: str | None
        """
        if self.__plugin_info:
            return self.__plugin_info.plugin_config

    @property
    def depth(self):
        """"
        :returns: Current analysis depth.
        :rtype: int
        """
        return self._depth

    @property
    def _orchestrator_pid(self):
        """"
        .. warning: This property is internally used by GoLismero.

        :returns: Process ID of the Orchestrator.
        :rtype: int | None
        """
        return self.__orchestrator_pid

    @property
    def _orchestrator_tid(self):
        """"
        .. warning: This property is internally used by GoLismero.

        :returns: Main thread ID of the Orchestrator.
        :rtype: int | None
        """
        return self.__orchestrator_tid

    def is_local(self):
        """
        :returns: True if we're running inside the Orchestrator's
                  main thread, False otherwise.
        :rtype: bool
        """
        return self.__orchestrator_pid == getpid() and self.__orchestrator_tid == get_ident()

    def send_ack(self, do_notify_end):
        """
        Send ACK messages from the plugins to the Orchestrator.

        :param do_notify_end: True to send the plugin end notification to
            the UI plugin, False otherwise.
        :type do_notify_end: bool
        """
        self.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_ACK, message_info=do_notify_end, priority=MessagePriority.MSG_PRIORITY_LOW)

    def send_status(self, progress=None):
        """
        Send status updates from the plugins to the Orchestrator.

        :param text: Optional status text.
        :type text: str | None

        :param progress: Progress percentage [0, 100] as a float,
                         or None to indicate progress can't be measured.
        :type progress: float | None
        """
        if progress is not None:
            if type(progress) in (int, long):
                progress = float(progress)
            elif type(progress) is not float:
                raise TypeError('Expected float, got %r instead', type(progress))
            if progress < 0.0:
                progress = 0.0
            elif progress > 100.0:
                progress = 100.0
        self.send_msg(message_type=MessageType.MSG_TYPE_STATUS, message_code=MessageCode.MSG_STATUS_PLUGIN_STEP, message_info=progress, priority=MessagePriority.MSG_PRIORITY_MEDIUM)
        return

    def send_msg(self, message_type=0, message_code=0, message_info=None, priority=MessagePriority.MSG_PRIORITY_MEDIUM):
        r"""
        Send messages from the plugins to the Orchestrator.

        :param message_type: Message type.
            Must be one of the constants from MessageType.
        :type mesage_type: int

        :param message_code: Message code.
            Must be one of the constants from MessageCode.
        :type message_code: int

        :param message_info: The payload of the message.
            Its type depends on the message type and code.
        :type message_info: \*

        :param priority: Priority level.
            Must be one of the constants from MessagePriority.
        :type priority: int
        """
        if message_type == MessageType.MSG_TYPE_RPC and self.is_local():
            self._orchestrator.rpcManager.execute_rpc(self.audit_name, message_code, *message_info)
            return
        message = Message(message_type=message_type, message_code=message_code, message_info=message_info, audit_name=self.audit_name, plugin_id=self.plugin_id, ack_identity=self.ack_identity, priority=priority)
        self.send_raw_msg(message)

    def send_raw_msg(self, message):
        """
        Send raw messages from the plugins to the Orchestrator.

        :param message: Message to send.
        :type message: Message
        """
        if message.priority >= MessagePriority.MSG_PRIORITY_HIGH and self.is_local():
            self._orchestrator.dispatch_msg(message)
            return
        try:
            self.msg_queue.put_nowait(message)
        except:
            exit(1)

    def remote_call(self, rpc_code, *args, **kwargs):
        r"""
        Make synchronous remote procedure calls on the Orchestrator.

        :param rpc_code: RPC code.
        :type rpc_code: int

        :returns: Depends on the call.
        :rtype: \*
        """
        try:
            response_queue = Manager().Queue()
        except:
            exit(1)

        self.send_msg(message_type=MessageType.MSG_TYPE_RPC, message_code=rpc_code, message_info=(
         response_queue, args, kwargs), priority=MessagePriority.MSG_PRIORITY_HIGH)
        try:
            raw_response = response_queue.get()
        except:
            exit(1)

        success, response = raw_response
        if not success:
            exc_type, exc_value, tb_list = response
            try:
                sys.stderr.writelines(format_exception_only(exc_type, exc_value))
                sys.stderr.writelines(format_list(tb_list))
            except Exception:
                pass

            raise response[0], response[1]
        return response

    def async_remote_call(self, rpc_code, *args, **kwargs):
        """
        Make asynchronous remote procedure calls on the Orchestrator.

        There's no return value, since we're not waiting for a response.

        :param rpc_code: RPC code.
        :type rpc_code: int
        """
        self.send_msg(message_type=MessageType.MSG_TYPE_RPC, message_code=rpc_code, message_info=(
         None, args, kwargs), priority=MessagePriority.MSG_PRIORITY_HIGH)
        return

    def bulk_remote_call(self, rpc_code, *arguments):
        """
        Make synchronous bulk remote procedure calls on the Orchestrator.

        The interface and behavior mimics that of the built-in map() function.
        For more details see:
        http://docs.python.org/2/library/functions.html#map

        :param rpc_code: RPC code.
        :type rpc_code: int

        :returns: List contents depend on the call.
        :rtype: list
        """
        arguments = tuple(tuple(x) for x in arguments)
        return self.remote_call(MessageCode.MSG_RPC_BULK, rpc_code, *arguments)

    def async_bulk_remote_call(self, rpc_code, *arguments):
        """
        Make asynchronous bulk remote procedure calls on the Orchestrator.

        The interface and behavior mimics that of the built-in map() function.
        For more details see:
        http://docs.python.org/2/library/functions.html#map

        There's no return value, since we're not waiting for a response.

        :param rpc_code: RPC code.
        :type rpc_code: int
        """
        arguments = tuple(tuple(x) for x in arguments)
        self.async_remote_call(MessageCode.MSG_RPC_BULK, rpc_code, *arguments)


class PluginPoolManager(object):
    """
    Manages a pool of subprocesses to run plugins in them.
    """

    def __init__(self, max_process, refresh_after_tasks):
        """
        :param max_process: Maximum number of processes to create.
        :type max_process: int

        :param refresh_after_tasks:
            Maximum number of function calls to make
            before refreshing a subprocess.
        :type refresh_after_tasks: int
        """
        self.__max_processes = max_process
        self.__refresh_after_tasks = refresh_after_tasks
        self.__pool = None
        return

    def run_plugin(self, context, func, args, kwargs):
        """
        Run a plugin in a pooled process.

        :param context: Context for the OOP plugin execution.
        :type context: PluginContext

        :param func: Name of the method to execute.
        :type func: str

        :param args: Positional arguments to the function call.
        :type args: tuple

        :param kwargs: Keyword arguments to the function call.
        :type kwargs: dict
        """
        if self.__pool is not None:
            self.__pool.apply_async(bootstrap, (
             context, func, args, kwargs))
            return
        else:
            old_context = Config._context
            try:
                return bootstrap(context, func, args, kwargs)
            finally:
                Config._context = old_context

            return

    def start(self):
        """
        Start the process manager.
        """
        if self.__pool is None:
            if self.__max_processes is not None and self.__max_processes > 0:
                self.__pool = Pool(initializer=_init_worker, processes=self.__max_processes, maxtasksperchild=self.__refresh_after_tasks)
                self.__pool.map_async(do_nothing, 'A' * self.__max_processes)
            else:
                self.__pool = None
        return

    def stop(self, wait=True):
        """
        Stop the process manager.

        :param wait: True to wait for the subprocesses to finish,
            False to kill them.
        :type wait: bool
        """
        if self.__pool is not None:
            if wait:
                self.__pool.close()
            else:
                self.__pool.terminate()
            self.__pool.join()
            self.__pool = None
        plugin_class_cache.clear()
        return


class PluginLauncher(object):
    """
    Manages a pool of subprocesses to run plugins in them.
    """

    def __init__(self, max_process, refresh_after_tasks):
        """
        :param max_process: Maximum number of processes to create.
        :type max_process: int

        :param refresh_after_tasks:
                Maximum number of function calls to make
                before refreshing a subprocess.
        :type refresh_after_tasks: int
        """
        try:
            self.__manager = Manager()
            self.__queue = self.__manager.Queue()
        except:
            exit(1)

        self.__process = Process(target=launcher, args=(
         self.__queue, max_process, refresh_after_tasks))
        self.__alive = True

    def run_plugin(self, context, func, args, kwargs):
        """
        Run a plugin in a pooled process.

        :param context: Context for the OOP plugin execution.
        :type context: PluginContext

        :param func: Name of the method to execute.
        :type func: str

        :param args: Positional arguments to the function call.
        :type args: tuple

        :param kwargs: Keyword arguments to the function call.
        :type kwargs: dict
        """
        if not self.__alive:
            raise RuntimeError('Plugin launcher was stopped')
        try:
            self.__queue.put_nowait((context, func, args, kwargs))
        except:
            try:
                self.stop(wait=False)
            except:
                pass

            exit(1)

    def start(self):
        """
        Start the plugin launcher.
        """
        if not self.__alive:
            raise RuntimeError('Plugin launcher was stopped')
        self.__process.start()

    def stop(self, wait=True):
        """
        Stop the plugin launcher.

        :param wait: True to wait for the subprocesses to finish,
            False to kill them.
        :type wait: bool
        """
        if not self.__alive:
            return
        else:
            try:
                self.__queue.put_nowait(wait)
                if wait:
                    self.__process.join()
                else:
                    self.__process.join(3)
                    try:
                        self.__process.terminate()
                    except Exception:
                        pass

            except:
                self.__process.terminate()

            self.__alive = False
            self.__process = None
            self.__queue = None
            self.__manager = None
            return


class ProcessManager(object):
    """
    Manages a pool of subprocesses to run plugins in them.
    """

    def __init__(self, orchestrator):
        """
        :param orchestrator: Orchestrator to send messages to.
        :type orchestrator: Orchestrator
        """
        self.__launcher = None
        config = orchestrator.config
        self.__max_processes = getattr(config, 'max_concurrent', None)
        self.__refresh_after_tasks = getattr(config, 'refresh_after_tasks', None)
        return

    def run_plugin(self, context, func, args, kwargs):
        """
        Run a plugin in a pooled process.

        :param context: Context for the OOP plugin execution.
        :type context: PluginContext

        :param func: Name of the method to execute.
        :type func: str

        :param args: Positional arguments to the function call.
        :type args: tuple

        :param kwargs: Keyword arguments to the function call.
        :type kwargs: dict
        """
        if self.__launcher is not None:
            return self.__launcher.run_plugin(context, func, args, kwargs)
        else:
            old_context = Config._context
            try:
                return bootstrap(context, func, args, kwargs)
            finally:
                Config._context = old_context

            return

    def start(self):
        """
        Start the process manager.
        """
        if self.__launcher is None:
            if self.__max_processes is not None and self.__max_processes > 0:
                launcher_class = PluginLauncher
                self.__launcher = launcher_class(self.__max_processes, self.__refresh_after_tasks)
                self.__launcher.start()
            else:
                self.__launcher = None
        return

    def stop(self, wait=True):
        """
        Stop the process manager.

        :param wait: True to wait for the subprocesses to finish,
            False to kill them.
        :type wait: bool
        """
        if self.__launcher is not None:
            self.__launcher.stop(wait)
            self.__launcher = None
        return