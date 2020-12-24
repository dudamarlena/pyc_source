# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tiziano/Development/StarterSquad/prudentia/prudentia/utils/bash.py
# Compiled at: 2019-02-10 12:34:50
# Size of source mod 2**32: 2159 bytes
import os
from subprocess import PIPE, Popen
from threading import Thread
import sys
from prudentia.utils import io

class BashCmd(object):

    def __init__(self, *cmd_args):
        self.cmd_args = cmd_args
        self.env = os.environ.copy()
        self.cwd = os.getcwd()
        self.show_output = True
        self.output_stdout = []
        self.output_stderr = []
        self.stdout = ''
        self.stderr = ''
        self.returncode = 1
        self.ON_POSIX = 'posix' in sys.builtin_module_names

    def set_env_var(self, var, value):
        if value:
            self.env[var] = value

    def set_cwd(self, cwd):
        self.cwd = cwd

    def set_show_output(self, b):
        self.show_output = b

    def print_output(self, out, err):
        try:
            for line in iter(out.readline, ''):
                if self.show_output:
                    print(line.strip())
                self.output_stdout.append(line.decode('utf-8'))

            for line in iter(err.readline, ''):
                print('ERR - ', line.strip())
                self.output_stderr.append(line.decode('utf-8'))

        finally:
            out.close()
            err.close()

    def execute(self):
        try:
            p = Popen(args=self.cmd_args, bufsize=1, stdout=PIPE, stderr=PIPE, close_fds=self.ON_POSIX, env=self.env, cwd=self.cwd)
            th = Thread(target=self.print_output, args=(p.stdout, p.stderr))
            th.daemon = True
            th.start()
            self.returncode = p.wait()
            th.join()
            self.stdout = ''.join(self.output_stdout)
            self.stderr = ''.join(self.output_stderr)
        except Exception as ex:
            io.track_error('cannot execute command {0}'.format(self.cmd_args), ex)

    def __repr__(self):
        return '{0}\nReturn code: {1}\nStd Output: {2}\nStd Error: {3}'.format(self.cmd_args, self.returncode, self.stdout, self.stderr)

    def is_ok(self):
        return bool(not self.returncode)

    def output(self):
        return self.stdout