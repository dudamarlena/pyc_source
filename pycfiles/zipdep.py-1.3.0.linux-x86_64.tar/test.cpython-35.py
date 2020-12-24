# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/test.py
# Compiled at: 2016-02-02 11:40:41
# Size of source mod 2**32: 761 bytes
import yaml, base64
from tornado import auth
try:
    from test2 import other_function
except ImportError as e:
    __test2_e = e
else:
    __test2_e = "this doesn't work in the test environment."
__zipdep_zipmodules = ['yaml', 'base64', 'tornado']

def test():
    pass


if __name__ == '__main__':
    print('Loaded YAML from {}'.format(yaml.__path__))
    print("base64, however, is a built-in, so it's loaded from {}".format(base64.__file__))
    print("We only imported a function from tornado, not the module. However, that's checked too! Tornado's auth module is", auth)
    print("However, since other_function is a project file, it won't import successfully outside of the test environment.")
    print('See:', __test2_e)