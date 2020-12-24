# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/commonruntime/RuntimeType.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 580 bytes
""" Class description goes here. """
from enum import Enum
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class RuntimeType(Enum):
    __doc__ = 'Running modes of Python source in dataClay.\n\n    Currently there exist the following modes:\n      - [client] For client-side execution --outside dataClay.\n      - [manage] The management mode for initialization/bootstraping the client.\n      - [exe_env] Execution Environment mode (inside dataClay infrastructure).\n    '
    client = 1
    manage = 2
    exe_env = 3