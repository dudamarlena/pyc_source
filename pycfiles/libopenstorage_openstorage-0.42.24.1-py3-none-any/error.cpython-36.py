# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cffi/cffi/error.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 877 bytes


class FFIError(Exception):
    __module__ = 'cffi'


class CDefError(Exception):
    __module__ = 'cffi'

    def __str__(self):
        try:
            current_decl = self.args[1]
            filename = current_decl.coord.file
            linenum = current_decl.coord.line
            prefix = '%s:%d: ' % (filename, linenum)
        except (AttributeError, TypeError, IndexError):
            prefix = ''

        return '%s%s' % (prefix, self.args[0])


class VerificationError(Exception):
    __doc__ = ' An error raised when verification fails\n    '
    __module__ = 'cffi'


class VerificationMissing(Exception):
    __doc__ = ' An error raised when incomplete structures are passed into\n    cdef, but no verification has been done\n    '
    __module__ = 'cffi'


class PkgConfigError(Exception):
    __doc__ = ' An error raised for missing modules in pkg-config\n    '
    __module__ = 'cffi'