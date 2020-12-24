# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/load_custom_dataset.py
# Compiled at: 2019-09-12 15:29:52
# Size of source mod 2**32: 992 bytes
"""
This module descibes how to load a custom dataset from a single file.

As a custom dataset we will actually use the movielens-100k dataset, but act as
if it were not built-in.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os
from surprise import BaselineOnly
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
file_path = os.path.expanduser('~/.surprise_data/ml-100k/ml-100k/u.data')
reader = Reader(line_format='user item rating timestamp', sep='\t')
data = Dataset.load_from_file(file_path, reader=reader)
cross_validate((BaselineOnly()), data, verbose=True)