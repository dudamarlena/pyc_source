# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/future_api.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 1367 bytes
"""Ensure compatibility with future tensorflow versions.

   This ensures that your code will be minimally impacted by future tensorflow
   API changes. Import the module to prevent accidental usage of stale APIs.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
delattr(tf, 'arg_max')
delattr(tf, 'arg_min')
delattr(tf, 'create_partitioned_variables')
delattr(tf, 'deserialize_many_sparse')
delattr(tf, 'lin_space')
delattr(tf, 'parse_single_sequence_example')
delattr(tf, 'serialize_many_sparse')
delattr(tf, 'serialize_sparse')
delattr(tf, 'sparse_matmul')