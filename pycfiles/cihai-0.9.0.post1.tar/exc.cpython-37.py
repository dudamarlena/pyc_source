# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/t/work/cihai/cihai/cihai/exc.py
# Compiled at: 2019-08-17 05:41:51
# Size of source mod 2**32: 2209 bytes
"""Exceptions raised from the Cihai library."""
from __future__ import absolute_import, unicode_literals

class CihaiException(Exception):
    __doc__ = 'Base Cihai Exception class.'


class ImportStringError(ImportError, CihaiException):
    __doc__ = '\n    Provides information about a failed :func:`import_string` attempt.\n\n    Notes\n    -----\n    This is from werkzeug.utils c769200 on May 23, LICENSE BSD.\n    https://github.com/pallets/werkzeug\n\n    Changes:\n    - Deferred load import import_string from cihai.util\n    - Format with black\n    '
    import_name = None
    exception = None

    def __init__(self, import_name, exception):
        from .utils import import_string
        self.import_name = import_name
        self.exception = exception
        msg = 'import_string() failed for %r. Possible reasons are:\n\n- missing __init__.py in a package;\n- package or module path not included in sys.path;\n- duplicated package or module name taking precedence in sys.path;\n- missing module, class, function or variable;\n\nDebugged import:\n\n%s\n\nOriginal exception:\n\n%s: %s'
        name = ''
        tracked = []
        for part in import_name.replace(':', '.').split('.'):
            name += (name and '.') + part
            imported = import_string(name, silent=True)
            if imported:
                tracked.append((name, getattr(imported, '__file__', None)))
            else:
                track = ['- %r found in %r.' % (n, i) for n, i in tracked]
                track.append('- %r not found.' % name)
                msg = msg % (
                 import_name,
                 '\n'.join(track),
                 exception.__class__.__name__,
                 str(exception))
                break

        ImportError.__init__(self, msg)

    def __repr__(self):
        return '<%s(%r, %r)>' % (
         self.__class__.__name__,
         self.import_name,
         self.exception)