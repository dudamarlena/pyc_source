# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /elicit/env.py
# Compiled at: 2018-08-13 00:06:39
# Size of source mod 2**32: 3066 bytes
"""An dictionary that supports environment-style operations.
"""
__all__ = [
 'Environ']
import os, re
_var_re = re.compile('\\$([a-zA-Z0-9_\\?]+|\\{[^}]*\\})')
del re

class Environ(dict):
    __doc__ = "Environ is a dictionary-like object that does automatic variable\n    expansion when setting new elements.\n\n    It supports an extra method called 'export' that takes strings of the form\n    'name=value' that may be used to set assign variable names.  The 'expand'\n    method will return a string with variables expanded from the values\n    contained in this object.\n    "

    @classmethod
    def from_system(cls, **kwargs):
        """Constructor that returns Environ instance pre-populated with values
        from the process environment.
        """
        env = cls(**kwargs)
        env.inherit()
        return env

    def inherit(self, env=None):
        """Works like the 'update' method, but defaults to updating from the
        system environment (os.environ).
        """
        if env is None:
            env = os.environ
        self.update(env)

    def set(self, name, val):
        self.__setitem__(name, self.expand(str(val)))

    def export(self, nameval):
        """Similar to the _export_ command in the bash shell.

        It assigns the name on the left of the equals sign to the value on the
        right, performing variable expansion if necessary.
        """
        name, val = nameval.split('=', 1)
        self.__setitem__(name, self.expand(str(val)))
        return name

    def __str__(self):
        s = ['%s=%s' % (nv[0], nv[1]) for nv in self.items()]
        s.sort()
        return '\n'.join(s)

    def expand(self, value):
        """Pass in a string that might have variable expansion to be performed
        (e.g. a section that has $NAME embedded), and return the expanded
        string.
        """
        i = 0
        while 1:
            m = _var_re.search(value, i)
            if not m:
                return value
                i, j = m.span(0)
                vname = m.group(1)
                if vname[0] == '{':
                    vname = vname[1:-1]
                else:
                    tail = value[j:]
                    tv = self.get(vname)
                    if tv is not None:
                        value = value[:i] + str(tv)
                    else:
                        value = value[:i]
                i = len(value)
                value = value + tail

    def copy(self):
        return Environ(self)