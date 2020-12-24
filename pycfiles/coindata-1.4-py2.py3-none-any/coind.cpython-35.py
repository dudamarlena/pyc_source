# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /app/coind/coind.py
# Compiled at: 2018-05-18 15:51:57
# Size of source mod 2**32: 3390 bytes
import os
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime

class Coind:
    TYPE_D = 1
    TYPE_CLI = 2

    def __init__(self, name, type, path='', debug=False):
        """
        Constructor

        :param name: cryptocurrency name. Ex: bitcoin
        :type name: string

        :param type: script execution type
        :type type: int

        :param path: coind executable path if its not recognizable
        :type path: string

        :param debug: enable debug logs during execution
        :type debug: bool
        """
        self._Coind__name = name
        self._Coind__type = type
        self._Coind__path = path
        self._Coind__debug = debug

    def run(self, action):
        """
        Run coind commands

        :param action: coind command
        :type action: string
        """
        cmd = self._Coind__form_cmd(action)
        if '-daemon' in cmd:
            return self._Coind__run_daemon(cmd)
        else:
            return self._Coind__run(cmd)

    def has_cli(self):
        """
        Check if has cli

        :returns: bool
        """
        cmd = 'find / -iname ' + self._Coind__name + '-cli'
        result = self._Coind__run(cmd)
        return result != ''

    def is_running(self):
        """
        Check if coind is running
        """
        result = self._Coind__run('pidof ' + self._Coind__name + 'd')
        return result != ''

    def __getattr__(self, name):
        """
        Call command dynamically
        """
        if name.startswith('_') is False:

            def wrapper(*args):
                cmd = name
                if len(args) > 0 and args[0]:
                    cmd += ' ' + args[0]
                return self.run(cmd)

            return wrapper

    def __form_cmd(self, action):
        """
        Mount full command

        :param action: coind command
        :type action: string
        """
        cmd = ''
        if self._Coind__path:
            cmd += self._Coind__path + '/'
        cmd += self._Coind__name
        if self._Coind__type is self.TYPE_D or '-daemon' in action:
            cmd += 'd'
        else:
            if self._Coind__type is self.TYPE_CLI:
                cmd += '-cli'
            else:
                raise Exception('Invalid coind type')
        cmd += ' ' + action
        self._Coind__log('Mounting command: ' + cmd)
        return cmd

    def __run(self, cmd):
        """
        Run command

        :param cmd: coind command
        :type cmd: string
        """
        self._Coind__log('Running command')
        out = Popen(cmd, stderr=STDOUT, stdout=PIPE, shell=True)
        result = out.stdout.read()
        out.communicate()
        out.terminate()
        self._Coind__log('Finished running command')
        return str(result, 'utf-8').strip()

    def __run_daemon(self, cmd):
        self._Coind__log('Running command')
        os.system(cmd + ' 2>&1')
        self._Coind__log('is_running: %s' % self.is_running())
        result = self._Coind__name.capitalize() + ' server starting' if self.is_running() else ''
        self._Coind__log('Finished running command')
        return result.strip()

    def __log(self, text):
        if self._Coind__debug:
            print('[' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '] ' + text)