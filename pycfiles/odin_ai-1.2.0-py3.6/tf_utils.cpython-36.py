# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/backend/tf_utils.py
# Compiled at: 2019-08-14 12:16:27
# Size of source mod 2**32: 369 bytes
from __future__ import absolute_import, division, print_function
from contextlib import contextmanager
import tensorflow as tf
from tensorflow.python.platform import tf_logging as logging

@contextmanager
def suppress_logging(level=logging.ERROR):
    curr_log = logging.get_verbosity()
    logging.set_verbosity(level)
    yield logging
    logging.set_verbosity(curr_log)