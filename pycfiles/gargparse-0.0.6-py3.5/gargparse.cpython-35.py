# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gargparse.py
# Compiled at: 2016-12-24 06:36:44
# Size of source mod 2**32: 496 bytes
import argparse
_PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
_ARGS = None

class _Args:

    def __getattr__(self, name):
        global _ARGS
        if _ARGS == None:
            _ARGS = _PARSER.parse_args()
        return getattr(_ARGS, name)


ARGS = _Args()

def add_argument(*args, **kwargs):
    _PARSER.add_argument(*args, **kwargs)


def parse_args(*args, **kwargs):
    global _ARGS
    _ARGS = _PARSER.parse_args(*args, **kwargs)