# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/circleci/autohelm/autohelm/exception.py
# Compiled at: 2018-11-27 14:02:40


class AutoHelmException(Exception):
    pass


class MinimumVersionException(AutoHelmException):
    pass


class AutoHelmCommandException(Exception):

    def __init__(self, msg, stdout=None, stderr=None, exitcode=None):
        self.message = msg
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode

    def __str__(self):
        return self.message