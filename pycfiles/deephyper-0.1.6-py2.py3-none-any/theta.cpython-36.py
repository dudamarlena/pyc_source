# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/contrib/perf/theta.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 993 bytes
import os, tensorflow as tf
from tensorflow.keras import backend as K

def get_session_conf():
    """Set env variables for better performance on Theta.

        Return:
                A tf.ConfigProto object with specific settings.
    """
    os.environ['KMP_BLOCKTIME'] = '0'
    os.environ['KMP_AFFINITY'] = 'granularity=fine,compact,1,0'
    if os.environ.get('OMP_NUM_THREADS') is not None:
        session_conf = tf.ConfigProto(intra_op_parallelism_threads=(int(os.environ.get('OMP_NUM_THREADS'))))
    return session_conf


def set_perf_settings_for_keras():
    """Set a session with performance setting for keras backend.
    """
    if os.environ.get('HOST') is not None:
        if 'theta' in os.environ.get('HOST'):
            session_conf = get_session_conf()
            session = tf.Session(config=session_conf)
            K.set_session(session)