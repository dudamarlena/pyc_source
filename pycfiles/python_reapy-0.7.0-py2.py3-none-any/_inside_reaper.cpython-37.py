# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\_inside_reaper.py
# Compiled at: 2020-03-18 12:13:39
# Size of source mod 2**32: 3457 bytes
import contextlib, functools, importlib, reapy, reapy.config
from reapy.errors import DisabledDistAPIError, DisabledDistAPIWarning
from .network import machines

def dist_api_is_enabled():
    """Return whether reapy can reach REAPER from the outside."""
    return machines.get_selected_client() is not None


class inside_reaper(contextlib.ContextDecorator):
    __doc__ = '\n    Context manager for efficient calls from outside REAPER.\n\n    It can also be used as a function decorator.\n\n    Examples\n    --------\n    Instead of running:\n\n    >>> project = reapy.Project()\n    >>> l = [project.bpm for i in range(1000)\n\n    which takes around 30 seconds, run:\n\n    >>> project = reapy.Project()\n    >>> with reapy.inside_reaper():\n    ...     l = [project.bpm for i in range(1000)\n    ...\n\n    which takes 0.1 seconds!\n\n    Example usage as decorator:\n\n    >>> @reapy.inside_reaper()\n    ... def add_n_tracks(n):\n    ...     for x in range(n):\n    ...         reapy.Project().add_track()\n\n    '

    def __call__(self, func, encoded_func=None):
        if reapy.is_inside_reaper():
            return func
        if isinstance(func, property):
            return DistProperty.from_property(func)
        module_name = func.__module__
        if module_name == 'reapy' or module_name.startswith('reapy.'):

            @functools.wraps(func)
            def wrap(*args, **kwargs):
                f = func if encoded_func is None else encoded_func
                client = machines.get_selected_client()
                return client.request(f, {'args':args,  'kwargs':kwargs})

            return wrap
        return super().__call__(func)

    def __enter__(self):
        if not reapy.is_inside_reaper():
            machines.get_selected_client().request('HOLD')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not reapy.is_inside_reaper():
            machines.get_selected_client().request('RELEASE')
        return False


class DistProperty(property):
    _inside_reaper = inside_reaper()

    @classmethod
    def from_property(cls, p):
        return cls().getter(p.fget).setter(p.fset).deleter(p.fdel)

    @staticmethod
    def _encode(f, method_name):
        return {'__callable__':True, 
         'module_name':f.__module__, 
         'name':'{}.f{}'.format(f.__qualname__, method_name)}

    def getter(self, fget):
        if fget is not None:
            fget = self._inside_reaper(fget, self._encode(fget, 'get'))
        return super().getter(fget)

    def setter(self, fset):
        if fset is not None:
            fset = self._inside_reaper(fset, self._encode(fset, 'set'))
        return super().setter(fset)

    def deleter(self, fdel):
        if fdel is not None:
            fdel = self._inside_reaper(fdel, self._encode(fdel, 'del'))
        return super().deleter(fdel)