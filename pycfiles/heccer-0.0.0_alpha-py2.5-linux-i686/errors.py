# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/heccer/errors.py
# Compiled at: 2011-09-09 23:43:09
from exceptions import Exception

class HeccerAddressError(Exception):
    """

    """

    def __init__(self, serial, field, msg=''):
        self.msg = 'Cannot find the address of ' + str(serial) + ' -> ' + field
        if msg != '':
            self.msg += ', %s' % msg

    def __str__(self):
        return self.msg


class HeccerNotAllocatedError(Exception):
    """

    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        error_msg = 'The Heccer core data struct is not allocated\n %s : %s' % (self.msg, self.value)
        return error_msg


class HeccerOptionsError(Exception):
    """

    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        error_msg = 'Error in the Heccer options\n %s : %s' % (self.msg, self.value)
        return error_msg


class HeccerCompileError(Exception):
    """

    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        error_msg = 'Error compiling Heccer: %s' % self.msg
        return error_msg