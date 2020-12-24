# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/envs/dfuzz/project/dfuzz/dfuzz/core/exceptions.py
# Compiled at: 2011-04-25 11:13:45


class SyscallException(Exception):

    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr
        self.line = '--------------------'
        self.str_stdout = ('stdout').center(20, '-')
        self.str_stderr = ('stderr').center(20, '-')

    def __str__(self):
        fmt = '\n%s\n\n%s\n%s\n'
        return fmt % (self.str_stdout, self.stdout, self.line) + fmt % (self.str_stderr, self.stderr, self.line)