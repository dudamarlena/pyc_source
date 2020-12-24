# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/pidbaseagent.py
# Compiled at: 2011-11-29 11:50:35
import os
from signal import SIGTERM, SIGINT, SIGHUP, SIGKILL
from time import sleep
from os.path import exists
from inqbus.ocf.generic.agent import Agent
from inqbus.ocf.generic.handlers import Handler
from inqbus.ocf.generic import exits

class PIDBaseAgent(Agent):
    """
    Abstract base class for PID controlled executables.
    It implements the Action Handlers start, stop, Monitor
    """

    def config(self):
        """
        The main configuration registers the action handlers.
        The OCF parameters will be configured in descendant classes.
        """
        self.handlers['start'] = Handler(PIDBaseAgent.do_start, 10)
        self.handlers['stop'] = Handler(PIDBaseAgent.do_stop, 10)
        self.handlers['monitor'] = Handler(PIDBaseAgent.do_monitor, 10)

    def init(self):
        """
        Main initialisation. Set members pid_file and executable. 
        """
        self.pid_file = self.get_pid_file()
        self.executable = self.get_executable()
        self.get_pid()

    def get_pid_file(self):
        """
        Abstract method that return the path of the PIDfile. 
        
        >>> a = PIDBaseAgent()
        >>> a.get_pid_file()
        Traceback (most recent call last):
            ...
        NotImplementedError: To use PIDAgent you have to implement a get_pid_file() routine that returns the PID-File
        """
        raise NotImplementedError('To use PIDAgent you have to implement a get_pid_file() routine that returns the PID-File')

    def get_executable(self):
        """
        Abstract method that return the path of the executable. 
        """
        raise NotImplementedError('To use PIDAgent you have to implement a get_executable() routine that return the executable location')

    def get_pid(self):
        """
        Read the PID from the pid_file.
        """
        if exists(self.pid_file):
            try:
                pid_file = open(self.pid_file)
            except:
                raise exits.OCF_ERR_PERM('cannot open pid file: %s' % self.pid_file)
            else:
                try:
                    pid_str = pid_file.read()
                except:
                    raise exits.OCF_ERR_PERM('cannot read pid file : %s' % self.pid_file)
                else:
                    try:
                        self.pid = int(pid_str)
                    except:
                        raise exits.OCF_ERR_PERM('no pid in file : %s' % self.pid_file)

        else:
            self.pid = None
        return self.pid

    def validate_dir(self, parameter):
        """
        Validates the a directory parameter for existence and accessibility.
        """
        dir_name = parameter.value
        if not os.path.exists(dir_name):
            raise exits.OCF_ERR_PERM('directory "%s" does not exist' % dir_name)
        if not os.access(dir_name, os.R_OK):
            raise exits.OCF_ERR_PERM('insufficient read permission for directory "%s"' % dir_name)

    def validate_file(self, parameter):
        """
        Validates the a file parameter for an existing file.
        Do not use for a PID-File!
        """
        file_name = parameter.value
        if not os.path.exists(file_name):
            raise exits.OCF_ERR_PERM('file "%s" does not exist' % file_name)
        if not os.access(file_name, os.R_OK):
            raise exits.OCF_ERR_PERM('insufficient read permission for file "%s"' % file_name)

    def validate_executable(self, parameter):
        """
        Validates the executable parameter.
        """
        self.validate_file(parameter)
        file_name = parameter.value
        if not os.access(file_name, os.X_OK):
            raise exits.OCF_ERR_PERM('not an executable: file "%s"' % file_name)

    def rm_pid_file(self):
        """
        Remove the pid_file if it exists
        """
        if exists(self.pid_file):
            os.remove(self.pid_file)

    def kill_pid(self, signal=0):
        """sends a signal to a process
        returns True if the pid is dead
        with no signal argument, sends no signal"""
        try:
            return os.kill(self.pid, signal)
        except OSError, e:
            if e.errno == 3:
                return True
            if e.errno == 1:
                return False
            raise

    def dead(self):
        """
        Checks if the process is dead.
        """
        if self.kill_pid():
            return True
        try:
            dead = os.waitpid(self.pid, os.WNOHANG)[0]
        except OSError, e:
            if e.errno == 10:
                return False
            raise

        return dead

    def running(self):
        """
        Checks if the process is running.
        """
        return not self.dead()

    def goodkill(self, interval=1, timeout=2):
        """let the process die gracefully, gradually send harsher signals if necessary"""
        for signal in [SIGTERM, SIGINT, SIGHUP]:
            if self.kill_pid(signal):
                return True
            if self.dead():
                return True
            sleep(interval)

        time = 0
        while True:
            if time < timeout:
                time += 1
            else:
                return False
            if self.kill_pid(SIGKILL):
                return True
            if self.dead():
                return True
            sleep(interval)

    def wait_pid(self, interval=1, timeout=2):
        """
        Wait infinitly for a PID in the  pid_file to come up.
        This process will be terminated by Pacemaker after the timeout
        specified for the start handler.
        Independent of that external termination, we stop our waiting for 
        the PID after the same timeout. This is crucial for self testing of 
        the Agent with no possibility of an external termination.  
        """
        sleep(2)
        time = 0
        while True:
            if time < timeout:
                time += 1
            else:
                return False
            self.get_pid()
            if self.pid and self.running():
                return True
            sleep(interval)

    def stop_process(self):
        """
        Stop the process with good_kill.
        """
        return self.goodkill()

    def start_process(self):
        """
        abstract: start the process. To be implemented from the inheriting class.
        """
        raise NotImplementedError('To use PIDBaseAgent you have to implement start_process() method')

    def do_start(self):
        """
        Buisiness logic for starting the process.
        """
        if self.pid == None or self.dead():
            self.start_process()
            if not self.wait_pid(timeout=self.handlers['start'].timeout):
                raise exits.OCF_NOT_RUNNING('start: Process cannot be started, PID does not come up')
        return

    def do_stop(self):
        """
        Buisiness logic for stopping the process.
        """
        if self.pid:
            if not self.dead():
                if self.stop_process():
                    self.rm_pid_file()
            else:
                self.rm_pid_file()

    def do_monitor(self):
        """
        Buisiness logic for monitoring the process.
        """
        if not self.pid:
            raise exits.OCF_NOT_RUNNING('monitor: Process not running')
        if self.dead():
            raise exits.OCF_NOT_RUNNING('monitor: Process not running')