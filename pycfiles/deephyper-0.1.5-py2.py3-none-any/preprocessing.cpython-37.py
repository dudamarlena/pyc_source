# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/preprocessing.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 550 bytes
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def stdscaler():
    """Use StandardScaler.

    Returns:
        preprocessor:
    """
    preprocessor = Pipeline([
     (
      'stdscaler', StandardScaler())])
    return preprocessor


def minmaxstdscaler():
    """Use MinMaxScaler then StandardScaler.

    Returns:
        preprocessor:
    """
    preprocessor = Pipeline([
     (
      'minmaxscaler', MinMaxScaler()),
     (
      'stdscaler', StandardScaler())])
    return preprocessor