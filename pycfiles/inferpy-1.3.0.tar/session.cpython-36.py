# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/util/session.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 1457 bytes
import tensorflow as tf, warnings
__session = None

def new_session(gpu_memory_fraction=0.0):
    if gpu_memory_fraction <= 0.0:
        set_session(tf.Session())
    else:
        config = tf.ConfigProto(log_device_placement=True)
        config.gpu_options.per_process_gpu_memory_fraction = gpu_memory_fraction
        set_session(tf.Session(config=config))


def get_session():
    global __session
    if not __session:
        __session = tf.Session()
    return __session


def set_session(session):
    global __session
    if __session:
        warnings.warn('Running session closed to use the provided session instead')
        __session.close()
    __session = session


def swap_session(new_session):
    global __session
    old_session = __session
    __session = new_session
    return old_session


def clear_session():
    global __session
    if __session:
        __session.close()
    __session = tf.Session()


def init_uninit_vars():
    uninit_vars = set(get_session().run(tf.report_uninitialized_variables()))
    if len(uninit_vars) > 0:
        get_session().run(tf.variables_initializer([v for v in tf.global_variables() if v.name.split(':')[0].encode('UTF-8') in uninit_vars]))