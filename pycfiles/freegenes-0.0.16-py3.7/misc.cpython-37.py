# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/freegenes/utils/misc.py
# Compiled at: 2019-08-18 10:01:58
# Size of source mod 2**32: 1262 bytes
import os

def setEnvVar(name, value):
    """Set or unset an environment variable

    name -- Name of the variable to set
    value -- Value to use or None to clear
    """
    if value is None:
        if name in os.environ:
            del os.environ[name]
    else:
        os.environ[name] = value


class ScopedEnvVar(object):
    __doc__ = 'Temporarly change an environment variable\n\n    Usage:\n        with ScopedEnvVar("FOO", "bar"):\n            print(os.environ["FOO"]) # "bar"\n        print(os.environ["FOO"]) # <oldvalue>\n    '

    def __init__(self, name, value):
        """Create the scoped environment variable object

        name -- Name of the variable to set
        value -- Value to use or None to clear
        """
        self.name = name
        self.value = value
        self.oldValue = None

    def __enter__(self):
        self.oldValue = os.environ.get(self.name)
        setEnvVar(self.name, self.value)
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        setEnvVar(self.name, self.oldValue)