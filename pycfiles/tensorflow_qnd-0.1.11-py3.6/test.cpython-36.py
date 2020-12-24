# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/test.py
# Compiled at: 2017-05-17 13:34:19
# Size of source mod 2**32: 344 bytes
import sys, tensorflow as tf

def oracle_model(x, y):
    return (
     y, 0.0, tf.no_op())


def user_input_fn(filename_queue):
    x = filename_queue.dequeue()
    return ({'x': x}, {'y': x})


def append_argv(*args):
    command = 'THIS_SHOULD_NEVER_MATCH'
    if sys.argv[0] != command:
        sys.argv = [
         command]
    sys.argv += [*args]