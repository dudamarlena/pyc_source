# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vini/Bio/abacat/abacat/data/__init__.py
# Compiled at: 2020-03-26 16:30:35
# Size of source mod 2**32: 281 bytes
__doc__ = '\nDirectory for data files. Contains the pathways json file and\nalso files for the test runs.\n'
from os import path
data_dir = path.dirname(__file__)
genomes_dir = path.join(data_dir, 'genomes')
local_db_dir = path.join(data_dir, 'db')