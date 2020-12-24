# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/epitome/__init__.py
# Compiled at: 2020-01-22 08:45:51
# Size of source mod 2**32: 957 bytes
"""
==============
epitome Module
==============
.. currentmodule:: epitome

epitome is a computational model for predicting ChIP-seq peaks in a new cell type
from chromatin accessibility and known ChIP-seq peaks from ENCODE. This module
also includes scripts for processing ENCODE peaks.

.. automodule:: epitome.models
.. automodule:: epitome.functions
.. automodule:: epitome.viz
.. automodule:: epitome.constants

"""
import os
from os.path import expanduser
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
S3_DATA_PATH = 'https://epitome-data.s3-us-west-1.amazonaws.com/data.zip'

def GET_EPITOME_USER_PATH():
    return os.path.join(os.path.expanduser('~'), '.epitome')


def GET_DATA_PATH():
    return os.path.join(GET_EPITOME_USER_PATH(), 'data')


POSITIONS_FILE = 'all.pos.bed.gz'
FEATURE_NAME_FILE = 'feature_name'
REQUIRED_FILES = [POSITIONS_FILE, 'train.npz', 'valid.npz', FEATURE_NAME_FILE, 'test.npz']