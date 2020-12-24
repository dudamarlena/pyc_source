# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/command.py
# Compiled at: 2016-11-15 14:40:44
import os, signal, subprocess, threading, time

class Command:
    """Class to handle the interface between Python scripts and executables"""

    def __init__(self, command, output_callback, timeout=10):
        """Constructor for the command class that sets up generic
        timed out execution

        Params:
        command- the command to run in the form of a list of strings
            (per subprocess input

        output_callback(self, line, kill_switch)- the callback to
            process what the program prints to stdout and stderr where
            line is the latest line (all output is also logged to
            self.notifications) This function should also set the state
            variables self.started, self.error, and self.stopped
            correctly. The function may assume that these are
            initialized to False, but must appropriately change the
            variables depending on input. On an error, the function
            must also set self.error to True and self.error_msg to the
            error message

        """
        self.command = command
        self.output_callback = output_callback
        self.timeout = timeout
        self.started = False
        self.stopped = False
        self.exception = None
        self.error = False
        self.notifications = ''
        self.thread = threading.Thread(target=self._invoke_cmd)
        self.thread.setDaemon(1)
        return

    def start(self, timeout=None):
        """Start running the command"""
        self.thread.start()
        start_time = time.time()
        if not timeout:
            timeout = self.timeout
        while start_time + timeout > time.time():
            self.thread.join(1)
            if self.started:
                return True
            if self.error:
                return False

        return False

    def stop(self, timeout=None):
        """Stop the given command"""
        if not timeout:
            timeout = self.timeout
        self.kill_switch()
        self.process.kill()
        self.thread.join(timeout)
        try:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        except:
            pass

        if self.stopped:
            return True
        else:
            return False

    def _invoke_cmd(self):
        try:
            self.process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        except Exception as exp:
            self.exception = exp
            self.started = False
            self.error = False
            return

        self.kill_switch = self.process.terminate
        self.starting = True
        while True:
            line = self.process.stdout.readline().strip()
            if not line:
                break
            self.output_callback(self, line, self.process.terminate)
            self.notifications += line + '\n'