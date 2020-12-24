# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_vendor/cachecontrol/filewrapper.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 2533 bytes
from io import BytesIO

class CallbackFileWrapper(object):
    __doc__ = '\n    Small wrapper around a fp object which will tee everything read into a\n    buffer, and when that file is closed it will execute a callback with the\n    contents of that buffer.\n\n    All attributes are proxied to the underlying file object.\n\n    This class uses members with a double underscore (__) leading prefix so as\n    not to accidentally shadow an attribute.\n    '

    def __init__(self, fp, callback):
        self._CallbackFileWrapper__buf = BytesIO()
        self._CallbackFileWrapper__fp = fp
        self._CallbackFileWrapper__callback = callback

    def __getattr__(self, name):
        fp = self.__getattribute__('_CallbackFileWrapper__fp')
        return getattr(fp, name)

    def __is_fp_closed(self):
        try:
            return self._CallbackFileWrapper__fp.fp is None
        except AttributeError:
            pass

        try:
            return self._CallbackFileWrapper__fp.closed
        except AttributeError:
            pass

        return False

    def _close(self):
        if self._CallbackFileWrapper__callback:
            self._CallbackFileWrapper__callback(self._CallbackFileWrapper__buf.getvalue())
        self._CallbackFileWrapper__callback = None

    def read(self, amt=None):
        data = self._CallbackFileWrapper__fp.read(amt)
        self._CallbackFileWrapper__buf.write(data)
        if self._CallbackFileWrapper__is_fp_closed():
            self._close()
        return data

    def _safe_read(self, amt):
        data = self._CallbackFileWrapper__fp._safe_read(amt)
        if amt == 2:
            if data == b'\r\n':
                return data
        self._CallbackFileWrapper__buf.write(data)
        if self._CallbackFileWrapper__is_fp_closed():
            self._close()
        return data