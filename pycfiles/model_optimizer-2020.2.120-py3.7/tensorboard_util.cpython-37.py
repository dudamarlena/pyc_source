# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/utils/tensorboard_util.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 1433 bytes
"""
 Copyright (C) 2018-2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
try:
    import tensorflow.compat.v1 as tf_v1
except ImportError:
    import tensorflow as tf_v1

try:
    import tensorflow.contrib
except:
    pass

from mo.utils.error import Error
from mo.utils.utils import refer_to_faq_msg

def dump_for_tensorboard(graph_def: tf_v1.GraphDef, logdir: str):
    try:
        print('Writing an event file for the tensorboard...')
        with tf_v1.summary.FileWriter(logdir=logdir, graph_def=graph_def) as (writer):
            writer.flush()
        print('Done writing an event file.')
    except Exception as err:
        try:
            raise Error('Cannot write an event file for the tensorboard to directory "{}". ' + refer_to_faq_msg(36), logdir) from err
        finally:
            err = None
            del err