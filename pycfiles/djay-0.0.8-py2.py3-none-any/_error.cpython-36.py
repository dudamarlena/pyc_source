# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/py/py/_error.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 2917 bytes
"""
create errno-specific classes for IO or os calls.

"""
from types import ModuleType
import sys, os, errno

class Error(EnvironmentError):

    def __repr__(self):
        return '%s.%s %r: %s ' % (self.__class__.__module__,
         self.__class__.__name__,
         self.__class__.__doc__,
         ' '.join(map(str, self.args)))

    def __str__(self):
        s = '[%s]: %s' % (self.__class__.__doc__,
         ' '.join(map(str, self.args)))
        return s


_winerrnomap = {2:errno.ENOENT, 
 3:errno.ENOENT, 
 17:errno.EEXIST, 
 18:errno.EXDEV, 
 13:errno.EBUSY, 
 22:errno.ENOTDIR, 
 20:errno.ENOTDIR, 
 267:errno.ENOTDIR, 
 5:errno.EACCES}

class ErrorMaker(ModuleType):
    __doc__ = " lazily provides Exception classes for each possible POSIX errno\n        (as defined per the 'errno' module).  All such instances\n        subclass EnvironmentError.\n    "
    Error = Error
    _errno2class = {}

    def __getattr__(self, name):
        if name[0] == '_':
            raise AttributeError(name)
        eno = getattr(errno, name)
        cls = self._geterrnoclass(eno)
        setattr(self, name, cls)
        return cls

    def _geterrnoclass(self, eno):
        try:
            return self._errno2class[eno]
        except KeyError:
            clsname = errno.errorcode.get(eno, 'UnknownErrno%d' % (eno,))
            errorcls = type(Error)(clsname, (Error,), {'__module__':'py.error', 
             '__doc__':os.strerror(eno)})
            self._errno2class[eno] = errorcls
            return errorcls

    def checked_call(self, func, *args, **kwargs):
        """ call a function and raise an errno-exception if applicable. """
        __tracebackhide__ = True
        try:
            return func(*args, **kwargs)
        except self.Error:
            raise
        except (OSError, EnvironmentError):
            cls, value, tb = sys.exc_info()
            if not hasattr(value, 'errno'):
                raise
            __tracebackhide__ = False
            errno = value.errno
            try:
                if not isinstance(value, WindowsError):
                    raise NameError
            except NameError:
                cls = self._geterrnoclass(errno)
            else:
                try:
                    cls = self._geterrnoclass(_winerrnomap[errno])
                except KeyError:
                    raise value

                raise cls('%s%r' % (func.__name__, args))
            __tracebackhide__ = True


error = ErrorMaker('py.error')
sys.modules[error.__name__] = error