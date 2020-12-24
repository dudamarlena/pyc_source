# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/generic/exits.py
# Compiled at: 2011-11-29 11:35:33
from __future__ import print_function
import sys, os, syslog

class OcfError(SystemExit):

    def __init__(self, code, message):
        message = self.__class__.__name__ + '\n' + str(message)
        if 'OCF_RESOURCE_INSTANCE' not in os.environ:
            print(message, file=sys.stderr)
        syslog.syslog(syslog.LOG_ERR, 'Agent exited with exitcode %s, %s' % (code, message))
        SystemExit.__init__(self, code)


class OCF_ERR_GENERIC(OcfError):

    def __init__(self, message):
        OcfError.__init__(self, 1, message)


class OCF_ERR_ARGS(OcfError):

    def __init__(self, message):
        OcfError.__init__(self, 2, message)


class OCF_ERR_UNIMPLEMENTED(OcfError):

    def __init__(self, message):
        OcfError.__init__(self, 3, message)


class OCF_ERR_PERM(OcfError):

    def __init__(self, message):
        OcfError.__init__(self, 4, message)


class OCF_ERR_INSTALLED(OcfError):

    def __init__(self, message):
        OcfError.__init__(self, 5, message)


class OCF_ERR_CONFIGURED(OcfError):

    def __init__(self, message):
        OcfError.__init__(self, 6, message)


class OCF_NOT_RUNNING(OcfError):

    def __init__(self, message=None):
        OcfError.__init__(self, 7, message)


class OCF_RUNNING_MASTER(OcfError):

    def __init__(self, message=None):
        OcfError.__init__(self, 8, message)


class OCF_FAILED_MASTER(OcfError):

    def __init__(self, message):
        OcfError.__init__(self, 9, message)