# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/config_test.py
# Compiled at: 2017-05-17 13:39:44
# Size of source mod 2**32: 186 bytes
import tensorflow as tf
from . import test
from . import config

def test_def_config():
    test.append_argv()
    assert isinstance(config.def_config()(), tf.contrib.learn.RunConfig)