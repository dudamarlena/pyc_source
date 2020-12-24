# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/bprc/variables.py
# Compiled at: 2016-08-20 13:14:45
# Size of source mod 2**32: 1111 bytes
__doc__ = '\nThis module implements all the class types required to variables in the YAML in memory.\n'
import os, sys
from itertools import chain
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import logging, collections
from bprc.utils import vlog, errlog, verboseprint

class Variables(collections.MutableMapping):
    """Variables"""

    def __init__(self, variables):
        self._variables = variables

    def __getitem__(self, key):
        return self._variables[key]

    def __setitem__(self, key, value):
        self._variables[key] = value

    def __delitem__(self, key):
        del self._variables[key]

    def __iter__(self):
        return iter(self._variables)

    def __len__(self):
        return len(self._variables)