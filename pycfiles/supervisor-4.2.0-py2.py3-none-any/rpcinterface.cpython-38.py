# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/rpcinterface.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 37333 bytes
import os, time, datetime, errno, types
from supervisor.compat import as_string
from supervisor.compat import as_bytes
from supervisor.compat import unicode
from supervisor.datatypes import Automatic, signal_number
from supervisor.options import readFile
from supervisor.options import tailFile
from supervisor.options import NotExecutable
from supervisor.options import NotFound
from supervisor.options import NoPermission
from supervisor.options import make_namespec
from supervisor.options import split_namespec
from supervisor.options import VERSION
from supervisor.events import notify
from supervisor.events import RemoteCommunicationEvent
from supervisor.http import NOT_DONE_YET
from supervisor.xmlrpc import capped_int, Faults, RPCError
from supervisor.states import SupervisorStates
from supervisor.states import getSupervisorStateDescription
from supervisor.states import ProcessStates
from supervisor.states import getProcessStateDescription
from supervisor.states import RUNNING_STATES, STOPPED_STATES
API_VERSION = '3.0'

class SupervisorNamespaceRPCInterface:

    def __init__(self, supervisord):
        self.supervisord = supervisord

    def _update(self, text):
        self.update_text = text
        if isinstance(self.supervisord.options.mood, int):
            if self.supervisord.options.mood < SupervisorStates.RUNNING:
                raise RPCError(Faults.SHUTDOWN_STATE)

    def getAPIVersion(self):
        """ Return the version of the RPC API used by supervisord

        @return string version version id
        """
        self._update('getAPIVersion')
        return API_VERSION

    getVersion = getAPIVersion

    def getSupervisorVersion(self):
        """ Return the version of the supervisor package in use by supervisord

        @return string version version id
        """
        self._update('getSupervisorVersion')
        return VERSION

    def getIdentification(self):
        """ Return identifying string of supervisord

        @return string identifier identifying string
        """
        self._update('getIdentification')
        return self.supervisord.options.identifier

    def getState(self):
        """ Return current state of supervisord as a struct

        @return struct A struct with keys int statecode, string statename
        """
        self._update('getState')
        state = self.supervisord.options.mood
        statename = getSupervisorStateDescription(state)
        data = {'statecode':state, 
         'statename':statename}
        return data

    def getPID(self):
        """ Return the PID of supervisord

        @return int PID
        """
        self._update('getPID')
        return self.supervisord.options.get_pid()

    def readLog(self, offset, length):
        """ Read length bytes from the main log starting at offset

        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        """
        self._update('readLog')
        logfile = self.supervisord.options.logfile
        if not (logfile is None or os.path.exists(logfile)):
            raise RPCError(Faults.NO_FILE, logfile)
        try:
            return as_string(readFile(logfile, int(offset), int(length)))
            except ValueError as inst:
            try:
                why = inst.args[0]
                raise RPCError(getattr(Faults, why))
            finally:
                inst = None
                del inst

    readMainLog = readLog

    def clearLog(self):
        """ Clear the main log.

        @return boolean result always returns True unless error
        """
        self._update('clearLog')
        logfile = self.supervisord.options.logfile
        if not (logfile is None or self.supervisord.options.exists(logfile)):
            raise RPCError(Faults.NO_FILE)
        try:
            self.supervisord.options.remove(logfile)
        except (OSError, IOError):
            raise RPCError(Faults.FAILED)
        else:
            for handler in self.supervisord.options.logger.handlers:
                if hasattr(handler, 'reopen'):
                    self.supervisord.options.logger.info('reopening log file')
                    handler.reopen()
                return True

    def shutdown(self):
        """ Shut down the supervisor process

        @return boolean result always returns True unless error
        """
        self._update('shutdown')
        self.supervisord.options.mood = SupervisorStates.SHUTDOWN
        return True

    def restart(self):
        """ Restart the supervisor process

        @return boolean result  always return True unless error
        """
        self._update('restart')
        self.supervisord.options.mood = SupervisorStates.RESTARTING
        return True

    def reloadConfig(self):
        """
        Reload the configuration.

        The result contains three arrays containing names of process
        groups:

        * `added` gives the process groups that have been added
        * `changed` gives the process groups whose contents have
          changed
        * `removed` gives the process groups that are no longer
          in the configuration

        @return array result  [[added, changed, removed]]

        """
        self._update('reloadConfig')
        try:
            self.supervisord.options.process_config(do_usage=False)
        except ValueError as msg:
            try:
                raise RPCError(Faults.CANT_REREAD, msg)
            finally:
                msg = None
                del msg

        else:
            added, changed, removed = self.supervisord.diff_to_active()
            added = [group.name for group in added]
            changed = [group.name for group in changed]
            removed = [group.name for group in removed]
            return [[added, changed, removed]]

    def addProcessGroup(self, name):
        """ Update the config for a running process from config file.

        @param string name         name of process group to add
        @return boolean result     true if successful
        """
        self._update('addProcessGroup')
        for config in self.supervisord.options.process_group_configs:
            if config.name == name:
                result = self.supervisord.add_process_group(config)
                if not result:
                    raise RPCError(Faults.ALREADY_ADDED, name)
                return True
        else:
            raise RPCError(Faults.BAD_NAME, name)

    def removeProcessGroup(self, name):
        """ Remove a stopped process from the active configuration.

        @param string name         name of process group to remove
        @return boolean result     Indicates whether the removal was successful
        """
        self._update('removeProcessGroup')
        if name not in self.supervisord.process_groups:
            raise RPCError(Faults.BAD_NAME, name)
        result = self.supervisord.remove_process_group(name)
        if not result:
            raise RPCError(Faults.STILL_RUNNING, name)
        return True

    def _getAllProcesses(self, lexical=False):
        all_processes = []
        if lexical:
            group_names = list(self.supervisord.process_groups.keys())
            group_names.sort()
            for group_name in group_names:
                group = self.supervisord.process_groups[group_name]
                process_names = list(group.processes.keys())
                process_names.sort()
                for process_name in process_names:
                    process = group.processes[process_name]
                    all_processes.append((group, process))

        else:
            groups = list(self.supervisord.process_groups.values())
            groups.sort()
            for group in groups:
                processes = list(group.processes.values())
                processes.sort()
                for process in processes:
                    all_processes.append((group, process))
                else:
                    return all_processes

    def _getGroupAndProcess(self, name):
        group_name, process_name = split_namespec(name)
        group = self.supervisord.process_groups.get(group_name)
        if group is None:
            raise RPCError(Faults.BAD_NAME, name)
        if process_name is None:
            return (
             group, None)
        process = group.processes.get(process_name)
        if process is None:
            raise RPCError(Faults.BAD_NAME, name)
        return (group, process)

    def startProcess(self, name, wait=True):
        """ Start a process

        @param string name Process name (or ``group:name``, or ``group:*``)
        @param boolean wait Wait for process to be fully started
        @return boolean result     Always true unless error

        """
        self._update('startProcess')
        group, process = self._getGroupAndProcess(name)
        if process is None:
            group_name, process_name = split_namespec(name)
            return self.startProcessGroup(group_name, wait)
        try:
            filename, argv = process.get_execv_args()
        except NotFound as why:
            try:
                raise RPCError(Faults.NO_FILE, why.args[0])
            finally:
                why = None
                del why

        except (NotExecutable, NoPermission) as why:
            try:
                raise RPCError(Faults.NOT_EXECUTABLE, why.args[0])
            finally:
                why = None
                del why

        else:
            if process.get_state() in RUNNING_STATES:
                raise RPCError(Faults.ALREADY_STARTED, name)
            else:
                process.spawn()
                self.supervisord.reap()
                if process.spawnerr:
                    raise RPCError(Faults.SPAWN_ERROR, name)
                process.transition()
                if wait and process.get_state() != ProcessStates.RUNNING:

                    def onwait():
                        if process.spawnerr:
                            raise RPCError(Faults.SPAWN_ERROR, name)
                        state = process.get_state()
                        if state not in (ProcessStates.STARTING, ProcessStates.RUNNING):
                            raise RPCError(Faults.ABNORMAL_TERMINATION, name)
                        if state == ProcessStates.RUNNING:
                            return True
                        return NOT_DONE_YET

                    onwait.delay = 0.05
                    onwait.rpcinterface = self
                    return onwait
            return True

    def startProcessGroup(self, name, wait=True):
        """ Start all processes in the group named 'name'

        @param string name     The group name
        @param boolean wait    Wait for each process to be fully started
        @return array result   An array of process status info structs
        """
        self._update('startProcessGroup')
        group = self.supervisord.process_groups.get(name)
        if group is None:
            raise RPCError(Faults.BAD_NAME, name)
        processes = list(group.processes.values())
        processes.sort()
        processes = [(group, process) for process in processes]
        startall = make_allfunc(processes, isNotRunning, (self.startProcess), wait=wait)
        startall.delay = 0.05
        startall.rpcinterface = self
        return startall

    def startAllProcesses(self, wait=True):
        """ Start all processes listed in the configuration file

        @param boolean wait    Wait for each process to be fully started
        @return array result   An array of process status info structs
        """
        self._update('startAllProcesses')
        processes = self._getAllProcesses()
        startall = make_allfunc(processes, isNotRunning, (self.startProcess), wait=wait)
        startall.delay = 0.05
        startall.rpcinterface = self
        return startall

    def stopProcess(self, name, wait=True):
        """ Stop a process named by name

        @param string name  The name of the process to stop (or 'group:name')
        @param boolean wait        Wait for the process to be fully stopped
        @return boolean result     Always return True unless error
        """
        self._update('stopProcess')
        group, process = self._getGroupAndProcess(name)
        if process is None:
            group_name, process_name = split_namespec(name)
            return self.stopProcessGroup(group_name, wait)
        if process.get_state() not in RUNNING_STATES:
            raise RPCError(Faults.NOT_RUNNING, name)
        msg = process.stop()
        if msg is not None:
            raise RPCError(Faults.FAILED, msg)
        self.supervisord.reap()
        if wait:
            if process.get_state() not in STOPPED_STATES:

                def onwait():
                    process.stop_report()
                    if process.get_state() not in STOPPED_STATES:
                        return NOT_DONE_YET
                    return True

                onwait.delay = 0
                onwait.rpcinterface = self
                return onwait
        return True

    def stopProcessGroup(self, name, wait=True):
        """ Stop all processes in the process group named 'name'

        @param string name     The group name
        @param boolean wait    Wait for each process to be fully stopped
        @return array result   An array of process status info structs
        """
        self._update('stopProcessGroup')
        group = self.supervisord.process_groups.get(name)
        if group is None:
            raise RPCError(Faults.BAD_NAME, name)
        processes = list(group.processes.values())
        processes.sort()
        processes = [(group, process) for process in processes]
        killall = make_allfunc(processes, isRunning, (self.stopProcess), wait=wait)
        killall.delay = 0.05
        killall.rpcinterface = self
        return killall

    def stopAllProcesses(self, wait=True):
        """ Stop all processes in the process list

        @param  boolean wait   Wait for each process to be fully stopped
        @return array result   An array of process status info structs
        """
        self._update('stopAllProcesses')
        processes = self._getAllProcesses()
        killall = make_allfunc(processes, isRunning, (self.stopProcess), wait=wait)
        killall.delay = 0.05
        killall.rpcinterface = self
        return killall

    def signalProcess(self, name, signal):
        """ Send an arbitrary UNIX signal to the process named by name

        @param string name    Name of the process to signal (or 'group:name')
        @param string signal  Signal to send, as name ('HUP') or number ('1')
        @return boolean
        """
        self._update('signalProcess')
        group, process = self._getGroupAndProcess(name)
        if process is None:
            group_name, process_name = split_namespec(name)
            return self.signalProcessGroup(group_name, signal=signal)
        try:
            sig = signal_number(signal)
        except ValueError:
            raise RPCError(Faults.BAD_SIGNAL, signal)
        else:
            if process.get_state() not in RUNNING_STATES:
                raise RPCError(Faults.NOT_RUNNING, name)
            msg = process.signal(sig)
            if msg is not None:
                raise RPCError(Faults.FAILED, msg)
            return True

    def signalProcessGroup(self, name, signal):
        """ Send a signal to all processes in the group named 'name'

        @param string name    The group name
        @param string signal  Signal to send, as name ('HUP') or number ('1')
        @return array
        """
        group = self.supervisord.process_groups.get(name)
        self._update('signalProcessGroup')
        if group is None:
            raise RPCError(Faults.BAD_NAME, name)
        processes = list(group.processes.values())
        processes.sort()
        processes = [(group, process) for process in processes]
        sendall = make_allfunc(processes, isRunning, (self.signalProcess), signal=signal)
        result = sendall()
        self._update('signalProcessGroup')
        return result

    def signalAllProcesses(self, signal):
        """ Send a signal to all processes in the process list

        @param string signal  Signal to send, as name ('HUP') or number ('1')
        @return array         An array of process status info structs
        """
        processes = self._getAllProcesses()
        signalall = make_allfunc(processes, isRunning, (self.signalProcess), signal=signal)
        result = signalall()
        self._update('signalAllProcesses')
        return result

    def getAllConfigInfo(self):
        """ Get info about all available process configurations. Each struct
        represents a single process (i.e. groups get flattened).

        @return array result  An array of process config info structs
        """
        self._update('getAllConfigInfo')
        configinfo = []
        for gconfig in self.supervisord.options.process_group_configs:
            inuse = gconfig.name in self.supervisord.process_groups
            for pconfig in gconfig.process_configs:
                d = {'autostart':pconfig.autostart, 
                 'command':pconfig.command, 
                 'exitcodes':pconfig.exitcodes, 
                 'group':gconfig.name, 
                 'group_prio':gconfig.priority, 
                 'inuse':inuse, 
                 'killasgroup':pconfig.killasgroup, 
                 'name':pconfig.name, 
                 'process_prio':pconfig.priority, 
                 'redirect_stderr':pconfig.redirect_stderr, 
                 'startretries':pconfig.startretries, 
                 'startsecs':pconfig.startsecs, 
                 'stdout_capture_maxbytes':pconfig.stdout_capture_maxbytes, 
                 'stdout_events_enabled':pconfig.stdout_events_enabled, 
                 'stdout_logfile':pconfig.stdout_logfile, 
                 'stdout_logfile_backups':pconfig.stdout_logfile_backups, 
                 'stdout_logfile_maxbytes':pconfig.stdout_logfile_maxbytes, 
                 'stdout_syslog':pconfig.stdout_syslog, 
                 'stopsignal':int(pconfig.stopsignal), 
                 'stopwaitsecs':pconfig.stopwaitsecs, 
                 'stderr_capture_maxbytes':pconfig.stderr_capture_maxbytes, 
                 'stderr_events_enabled':pconfig.stderr_events_enabled, 
                 'stderr_logfile':pconfig.stderr_logfile, 
                 'stderr_logfile_backups':pconfig.stderr_logfile_backups, 
                 'stderr_logfile_maxbytes':pconfig.stderr_logfile_maxbytes, 
                 'stderr_syslog':pconfig.stderr_syslog}
                d.update(((k, 'auto') for k, v in d.items() if v is Automatic))
                d.update(((k, 'none') for k, v in d.items() if v is None))
                configinfo.append(d)
            else:
                configinfo.sort(key=(lambda r: r['name']))
                return configinfo

    def _interpretProcessInfo(self, info):
        state = info['state']
        if state == ProcessStates.RUNNING:
            start = info['start']
            now = info['now']
            start_dt = (datetime.datetime)(*time.gmtime(start)[:6])
            now_dt = (datetime.datetime)(*time.gmtime(now)[:6])
            uptime = now_dt - start_dt
            if _total_seconds(uptime) < 0:
                uptime = datetime.timedelta(0)
            desc = 'pid %s, uptime %s' % (info['pid'], uptime)
        else:
            if state in (ProcessStates.FATAL, ProcessStates.BACKOFF):
                desc = info['spawnerr']
                desc = desc or 'unknown error (try "tail %s")' % info['name']
            else:
                if state in (ProcessStates.STOPPED, ProcessStates.EXITED):
                    if info['start']:
                        stop = info['stop']
                        stop_dt = (datetime.datetime)(*time.localtime(stop)[:7])
                        desc = stop_dt.strftime('%b %d %I:%M %p')
                    else:
                        desc = 'Not started'
                else:
                    desc = ''
        return desc

    def getProcessInfo(self, name):
        """ Get info about a process named name

        @param string name The name of the process (or 'group:name')
        @return struct result     A structure containing data about the process
        """
        self._update('getProcessInfo')
        group, process = self._getGroupAndProcess(name)
        if process is None:
            raise RPCError(Faults.BAD_NAME, name)
        start = capped_int(process.laststart)
        stop = capped_int(process.laststop)
        now = capped_int(self._now())
        state = process.get_state()
        spawnerr = process.spawnerr or ''
        exitstatus = process.exitstatus or 0
        stdout_logfile = process.config.stdout_logfile or ''
        stderr_logfile = process.config.stderr_logfile or ''
        info = {'name':process.config.name, 
         'group':group.config.name, 
         'start':start, 
         'stop':stop, 
         'now':now, 
         'state':state, 
         'statename':getProcessStateDescription(state), 
         'spawnerr':spawnerr, 
         'exitstatus':exitstatus, 
         'logfile':stdout_logfile, 
         'stdout_logfile':stdout_logfile, 
         'stderr_logfile':stderr_logfile, 
         'pid':process.pid}
        description = self._interpretProcessInfo(info)
        info['description'] = description
        return info

    def _now(self):
        return time.time()

    def getAllProcessInfo(self):
        """ Get info about all processes

        @return array result  An array of process status results
        """
        self._update('getAllProcessInfo')
        all_processes = self._getAllProcesses(lexical=True)
        output = []
        for group, process in all_processes:
            name = make_namespec(group.config.name, process.config.name)
            output.append(self.getProcessInfo(name))
        else:
            return output

    def _readProcessLog(self, name, offset, length, channel):
        group, process = self._getGroupAndProcess(name)
        if process is None:
            raise RPCError(Faults.BAD_NAME, name)
        logfile = getattr(process.config, '%s_logfile' % channel)
        if not (logfile is None or os.path.exists(logfile)):
            raise RPCError(Faults.NO_FILE, logfile)
        try:
            return as_string(readFile(logfile, int(offset), int(length)))
            except ValueError as inst:
            try:
                why = inst.args[0]
                raise RPCError(getattr(Faults, why))
            finally:
                inst = None
                del inst

    def readProcessStdoutLog(self, name, offset, length):
        """ Read length bytes from name's stdout log starting at offset

        @param string name        the name of the process (or 'group:name')
        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        """
        self._update('readProcessStdoutLog')
        return self._readProcessLog(name, offset, length, 'stdout')

    readProcessLog = readProcessStdoutLog

    def readProcessStderrLog(self, name, offset, length):
        """ Read length bytes from name's stderr log starting at offset

        @param string name        the name of the process (or 'group:name')
        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        """
        self._update('readProcessStderrLog')
        return self._readProcessLog(name, offset, length, 'stderr')

    def _tailProcessLog(self, name, offset, length, channel):
        group, process = self._getGroupAndProcess(name)
        if process is None:
            raise RPCError(Faults.BAD_NAME, name)
        else:
            logfile = getattr(process.config, '%s_logfile' % channel)
            return logfile is None or os.path.exists(logfile) or [
             '', 0, False]
        return tailFile(logfile, int(offset), int(length))

    def tailProcessStdoutLog(self, name, offset, length):
        """
        Provides a more efficient way to tail the (stdout) log than
        readProcessStdoutLog().  Use readProcessStdoutLog() to read
        chunks and tailProcessStdoutLog() to tail.

        Requests (length) bytes from the (name)'s log, starting at
        (offset).  If the total log size is greater than (offset +
        length), the overflow flag is set and the (offset) is
        automatically increased to position the buffer at the end of
        the log.  If less than (length) bytes are available, the
        maximum number of available bytes will be returned.  (offset)
        returned is always the last offset in the log +1.

        @param string name         the name of the process (or 'group:name')
        @param int offset          offset to start reading from
        @param int length          maximum number of bytes to return
        @return array result       [string bytes, int offset, bool overflow]
        """
        self._update('tailProcessStdoutLog')
        return self._tailProcessLog(name, offset, length, 'stdout')

    tailProcessLog = tailProcessStdoutLog

    def tailProcessStderrLog(self, name, offset, length):
        """
        Provides a more efficient way to tail the (stderr) log than
        readProcessStderrLog().  Use readProcessStderrLog() to read
        chunks and tailProcessStderrLog() to tail.

        Requests (length) bytes from the (name)'s log, starting at
        (offset).  If the total log size is greater than (offset +
        length), the overflow flag is set and the (offset) is
        automatically increased to position the buffer at the end of
        the log.  If less than (length) bytes are available, the
        maximum number of available bytes will be returned.  (offset)
        returned is always the last offset in the log +1.

        @param string name         the name of the process (or 'group:name')
        @param int offset          offset to start reading from
        @param int length          maximum number of bytes to return
        @return array result       [string bytes, int offset, bool overflow]
        """
        self._update('tailProcessStderrLog')
        return self._tailProcessLog(name, offset, length, 'stderr')

    def clearProcessLogs(self, name):
        """ Clear the stdout and stderr logs for the named process and
        reopen them.

        @param string name   The name of the process (or 'group:name')
        @return boolean result      Always True unless error
        """
        self._update('clearProcessLogs')
        group, process = self._getGroupAndProcess(name)
        if process is None:
            raise RPCError(Faults.BAD_NAME, name)
        try:
            process.removelogs()
        except (IOError, OSError):
            raise RPCError(Faults.FAILED, name)
        else:
            return True

    clearProcessLog = clearProcessLogs

    def clearAllProcessLogs(self):
        """ Clear all process log files

        @return array result   An array of process status info structs
        """
        self._update('clearAllProcessLogs')
        results = []
        callbacks = []
        all_processes = self._getAllProcesses()
        for group, process in all_processes:
            callbacks.append((group, process, self.clearProcessLog))
        else:

            def clearall():
                if not callbacks:
                    return results
                group, process, callback = callbacks.pop(0)
                name = make_namespec(group.config.name, process.config.name)
                try:
                    callback(name)
                except RPCError as e:
                    try:
                        results.append({'name':process.config.name, 
                         'group':group.config.name, 
                         'status':e.code, 
                         'description':e.text})
                    finally:
                        e = None
                        del e

                else:
                    results.append({'name':process.config.name, 
                     'group':group.config.name, 
                     'status':Faults.SUCCESS, 
                     'description':'OK'})
                if callbacks:
                    return NOT_DONE_YET
                return results

            clearall.delay = 0.05
            clearall.rpcinterface = self
            return clearall

    def sendProcessStdin(self, name, chars):
        """ Send a string of chars to the stdin of the process name.
        If non-7-bit data is sent (unicode), it is encoded to utf-8
        before being sent to the process' stdin.  If chars is not a
        string or is not unicode, raise INCORRECT_PARAMETERS.  If the
        process is not running, raise NOT_RUNNING.  If the process'
        stdin cannot accept input (e.g. it was closed by the child
        process), raise NO_FILE.

        @param string name        The process name to send to (or 'group:name')
        @param string chars       The character data to send to the process
        @return boolean result    Always return True unless error
        """
        self._update('sendProcessStdin')
        if not isinstance(chars, (str, bytes, unicode)):
            raise RPCError(Faults.INCORRECT_PARAMETERS, chars)
        chars = as_bytes(chars)
        group, process = self._getGroupAndProcess(name)
        if process is None:
            raise RPCError(Faults.BAD_NAME, name)
        if not process.pid or process.killing:
            raise RPCError(Faults.NOT_RUNNING, name)
        try:
            process.write(chars)
        except OSError as why:
            try:
                if why.args[0] == errno.EPIPE:
                    raise RPCError(Faults.NO_FILE, name)
                else:
                    raise
            finally:
                why = None
                del why

        else:
            return True

    def sendRemoteCommEvent(self, type, data):
        """ Send an event that will be received by event listener
        subprocesses subscribing to the RemoteCommunicationEvent.

        @param  string  type  String for the "type" key in the event header
        @param  string  data  Data for the event body
        @return boolean       Always return True unless error
        """
        if isinstance(type, unicode):
            type = type.encode('utf-8')
        if isinstance(data, unicode):
            data = data.encode('utf-8')
        notify(RemoteCommunicationEvent(type, data))
        return True


def _total_seconds(timedelta):
    return ((timedelta.days * 86400 + timedelta.seconds) * 1000000 + timedelta.microseconds) / 1000000


def make_allfunc(processes, predicate, func, **extra_kwargs):
    """ Return a closure representing a function that calls a
    function for every process, and returns a result """
    callbacks = []
    results = []

    def allfunc--- This code section failed: ---

 L. 941         0  LOAD_FAST                'callbacks'
                2  POP_JUMP_IF_TRUE    196  'to 196'

 L. 943         4  LOAD_FAST                'processes'
                6  GET_ITER         
              8_0  COME_FROM            40  '40'
                8  FOR_ITER            196  'to 196'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'group'
               14  STORE_FAST               'process'

 L. 944        16  LOAD_GLOBAL              make_namespec
               18  LOAD_FAST                'group'
               20  LOAD_ATTR                config
               22  LOAD_ATTR                name
               24  LOAD_FAST                'process'
               26  LOAD_ATTR                config
               28  LOAD_ATTR                name
               30  CALL_FUNCTION_2       2  ''
               32  STORE_FAST               'name'

 L. 945        34  LOAD_FAST                'predicate'
               36  LOAD_FAST                'process'
               38  CALL_FUNCTION_1       1  ''
               40  POP_JUMP_IF_FALSE     8  'to 8'

 L. 946        42  SETUP_FINALLY        60  'to 60'

 L. 947        44  LOAD_FAST                'func'
               46  LOAD_FAST                'name'
               48  BUILD_TUPLE_1         1 
               50  LOAD_FAST                'extra_kwargs'
               52  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               54  STORE_FAST               'callback'
               56  POP_BLOCK        
               58  JUMP_FORWARD        134  'to 134'
             60_0  COME_FROM_FINALLY    42  '42'

 L. 948        60  DUP_TOP          
               62  LOAD_GLOBAL              RPCError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE   132  'to 132'
               68  POP_TOP          
               70  STORE_FAST               'e'
               72  POP_TOP          
               74  SETUP_FINALLY       120  'to 120'

 L. 949        76  LOAD_FAST                'results'
               78  LOAD_METHOD              append
               80  LOAD_FAST                'process'
               82  LOAD_ATTR                config
               84  LOAD_ATTR                name

 L. 950        86  LOAD_FAST                'group'
               88  LOAD_ATTR                config
               90  LOAD_ATTR                name

 L. 951        92  LOAD_FAST                'e'
               94  LOAD_ATTR                code

 L. 952        96  LOAD_FAST                'e'
               98  LOAD_ATTR                text

 L. 949       100  LOAD_CONST               ('name', 'group', 'status', 'description')
              102  BUILD_CONST_KEY_MAP_4     4 
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          

 L. 953       108  POP_BLOCK        
              110  POP_EXCEPT       
              112  CALL_FINALLY        120  'to 120'
              114  JUMP_BACK             8  'to 8'
              116  POP_BLOCK        
              118  BEGIN_FINALLY    
            120_0  COME_FROM           112  '112'
            120_1  COME_FROM_FINALLY    74  '74'
              120  LOAD_CONST               None
              122  STORE_FAST               'e'
              124  DELETE_FAST              'e'
              126  END_FINALLY      
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
            132_0  COME_FROM            66  '66'
              132  END_FINALLY      
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM            58  '58'

 L. 954       134  LOAD_GLOBAL              isinstance
              136  LOAD_FAST                'callback'
              138  LOAD_GLOBAL              types
              140  LOAD_ATTR                FunctionType
              142  CALL_FUNCTION_2       2  ''
              144  POP_JUMP_IF_FALSE   164  'to 164'

 L. 955       146  LOAD_FAST                'callbacks'
              148  LOAD_METHOD              append
              150  LOAD_FAST                'group'
              152  LOAD_FAST                'process'
              154  LOAD_FAST                'callback'
              156  BUILD_TUPLE_3         3 
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          
              162  JUMP_BACK             8  'to 8'
            164_0  COME_FROM           144  '144'

 L. 957       164  LOAD_FAST                'results'
              166  LOAD_METHOD              append

 L. 958       168  LOAD_FAST                'process'
              170  LOAD_ATTR                config
              172  LOAD_ATTR                name

 L. 959       174  LOAD_FAST                'group'
              176  LOAD_ATTR                config
              178  LOAD_ATTR                name

 L. 960       180  LOAD_GLOBAL              Faults
              182  LOAD_ATTR                SUCCESS

 L. 961       184  LOAD_STR                 'OK'

 L. 958       186  LOAD_CONST               ('name', 'group', 'status', 'description')
              188  BUILD_CONST_KEY_MAP_4     4 

 L. 957       190  CALL_METHOD_1         1  ''
              192  POP_TOP          
              194  JUMP_BACK             8  'to 8'
            196_0  COME_FROM             2  '2'

 L. 964       196  LOAD_FAST                'callbacks'
              198  POP_JUMP_IF_TRUE    204  'to 204'

 L. 965       200  LOAD_FAST                'results'
              202  RETURN_VALUE     
            204_0  COME_FROM           198  '198'

 L. 967       204  LOAD_FAST                'callbacks'
              206  LOAD_CONST               None
              208  LOAD_CONST               None
              210  BUILD_SLICE_2         2 
              212  BINARY_SUBSCR    
              214  GET_ITER         
            216_0  COME_FROM           326  '326'
              216  FOR_ITER            370  'to 370'
              218  STORE_FAST               'struct'

 L. 969       220  LOAD_FAST                'struct'
              222  UNPACK_SEQUENCE_3     3 
              224  STORE_FAST               'group'
              226  STORE_FAST               'process'
              228  STORE_FAST               'cb'

 L. 971       230  SETUP_FINALLY       242  'to 242'

 L. 972       232  LOAD_FAST                'cb'
              234  CALL_FUNCTION_0       0  ''
              236  STORE_FAST               'value'
              238  POP_BLOCK        
              240  JUMP_FORWARD        320  'to 320'
            242_0  COME_FROM_FINALLY   230  '230'

 L. 973       242  DUP_TOP          
              244  LOAD_GLOBAL              RPCError
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   318  'to 318'
              252  POP_TOP          
              254  STORE_FAST               'e'
              256  POP_TOP          
              258  SETUP_FINALLY       306  'to 306'

 L. 974       260  LOAD_FAST                'results'
              262  LOAD_METHOD              append

 L. 975       264  LOAD_FAST                'process'
              266  LOAD_ATTR                config
              268  LOAD_ATTR                name

 L. 976       270  LOAD_FAST                'group'
              272  LOAD_ATTR                config
              274  LOAD_ATTR                name

 L. 977       276  LOAD_FAST                'e'
              278  LOAD_ATTR                code

 L. 978       280  LOAD_FAST                'e'
              282  LOAD_ATTR                text

 L. 975       284  LOAD_CONST               ('name', 'group', 'status', 'description')
              286  BUILD_CONST_KEY_MAP_4     4 

 L. 974       288  CALL_METHOD_1         1  ''
              290  POP_TOP          

 L. 979       292  LOAD_FAST                'callbacks'
              294  LOAD_METHOD              remove
              296  LOAD_FAST                'struct'
              298  CALL_METHOD_1         1  ''
              300  POP_TOP          
              302  POP_BLOCK        
              304  BEGIN_FINALLY    
            306_0  COME_FROM_FINALLY   258  '258'
              306  LOAD_CONST               None
              308  STORE_FAST               'e'
              310  DELETE_FAST              'e'
              312  END_FINALLY      
              314  POP_EXCEPT       
              316  JUMP_BACK           216  'to 216'
            318_0  COME_FROM           248  '248'
              318  END_FINALLY      
            320_0  COME_FROM           240  '240'

 L. 981       320  LOAD_FAST                'value'
              322  LOAD_GLOBAL              NOT_DONE_YET
              324  COMPARE_OP               is-not
              326  POP_JUMP_IF_FALSE   216  'to 216'

 L. 982       328  LOAD_FAST                'results'
              330  LOAD_METHOD              append

 L. 983       332  LOAD_FAST                'process'
              334  LOAD_ATTR                config
              336  LOAD_ATTR                name

 L. 984       338  LOAD_FAST                'group'
              340  LOAD_ATTR                config
              342  LOAD_ATTR                name

 L. 985       344  LOAD_GLOBAL              Faults
              346  LOAD_ATTR                SUCCESS

 L. 986       348  LOAD_STR                 'OK'

 L. 983       350  LOAD_CONST               ('name', 'group', 'status', 'description')
              352  BUILD_CONST_KEY_MAP_4     4 

 L. 982       354  CALL_METHOD_1         1  ''
              356  POP_TOP          

 L. 988       358  LOAD_FAST                'callbacks'
              360  LOAD_METHOD              remove
              362  LOAD_FAST                'struct'
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          
              368  JUMP_BACK           216  'to 216'

 L. 990       370  LOAD_FAST                'callbacks'
          372_374  POP_JUMP_IF_FALSE   380  'to 380'

 L. 991       376  LOAD_GLOBAL              NOT_DONE_YET
              378  RETURN_VALUE     
            380_0  COME_FROM           372  '372'

 L. 993       380  LOAD_FAST                'results'
              382  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 112

    return allfunc


def isRunning(process):
    return process.get_state() in RUNNING_STATES


def isNotRunning(process):
    return not isRunning(process)


def make_main_rpcinterface(supervisord):
    return SupervisorNamespaceRPCInterface(supervisord)