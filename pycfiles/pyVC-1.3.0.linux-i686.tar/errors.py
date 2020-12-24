# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/errors.py
# Compiled at: 2007-08-31 18:49:27
__revision__ = '$Revision: 245 $'

class pyVCError(Exception):
    __revision__ = '$Revision: 245 $'

    def __init__(self, value, errid, hostname):
        Exception.__init__(self)
        self.value = value
        self.errid = errid
        self.hostname = hostname

    def __str__(self):
        return repr(self.value)


class MachineError(pyVCError):
    __revision__ = '$Revision: 245 $'

    def __init__(self, value, errid, hostname):
        pyVCError.__init__(self, value, errid, hostname)


class NetworkError(pyVCError):
    __revision__ = '$Revision: 245 $'

    def __init__(self, value, errid, hostname, networkname):
        pyVCError.__init__(self, value, errid, hostname)
        self.networkname = networkname


class DiskError(pyVCError):
    __revision__ = '$Revision: 245 $'

    def __init__(self, value, errid, hostname):
        pyVCError.__init__(self, value, errid, hostname)


class VMError(pyVCError):
    __revision__ = '$Revision: 245 $'

    def __init__(self, value, errid, hostname, vmname):
        pyVCError.__init__(self, value, errid, hostname)
        self.vmname = vmname


class SpecificationError(pyVCError):
    __revision__ = '$Revision: 245 $'

    def __init__(self, value, errid):
        pyVCError.__init__(self, value, errid, 'Specification')


class VCMLError(pyVCError):
    __revision__ = '$Revision: 245 $'

    def __init__(self, value, errid, error_log):
        pyVCError.__init__(self, value, errid, 'VCML')
        self.error_log = error_log


class pyVCdError(pyVCError):
    __revision__ = '$Revision: 245 $'

    def __init__(self, value, errid):
        pyVCError.__init__(self, value, errid, 'pyVCd')