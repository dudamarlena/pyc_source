# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vini/Bio/abacat/abacat/data/__init__.py
# Compiled at: 2020-03-26 16:30:35
# Size of source mod 2**32: 281 bytes
"""
Directory for data files. Contains the pathways json file and
also files for the test runs.
"""
from os import path
data_dir = path.dirname(__file__)
genomes_dir = path.join(data_dir, 'genomes')
local_db_dir = path.join(data_dir, 'db')