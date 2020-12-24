# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tdd/io.py
# Compiled at: 2019-06-08 11:53:32
# Size of source mod 2**32: 607 bytes
"""
Class for io :
    - Should have methods to take data and transform to a photometry table and light curves
    - Should have methods to transform to light curves
"""
from __future__ import absolute_import, print_function, division
from future.utils import with_metaclass
__all__ = [
 'read_plasticc_data']
import numpy as np, pandas as pd

def read_plasticc_data(metadata_fname, photometry_fname):
    """
    function to read the plasticc data from a single csv file
    """
    metadata = pd.read_csv(metadata_fname)
    photometry = pd.read_csv(photometry_fname)
    return (metadata, photometry)