# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\A_MSU_NASA\VS\pyiomica\pyiomica\globalVariables.py
# Compiled at: 2020-04-14 15:05:28
# Size of source mod 2**32: 1819 bytes
"""This module contains global constants used in PyIOmica.
Some of the modules, classes and functions are imported in this module."""
import io, os, types, appdirs, gzip, copy, shutil, zipfile, numpy as np
np.random.seed(0)
import pandas as pd, networkx as nx, scipy, scipy.stats, scipy.fftpack
import scipy.cluster.hierarchy as hierarchy
import sklearn
printPackageGlobalDefaults = False
PackageDirectory = os.path.dirname(__file__)
UserDataDirectory = os.path.join(PackageDirectory, 'data')
if not os.path.exists(UserDataDirectory):
    print('Cannot access default site package directory, will instead use ', UserDataDirectory)
    UserDataDirectory = appdirs.user_data_dir('pyiomica', 'gmiaslab')
ConstantPyIOmicaDataDirectory = UserDataDirectory
ConstantPyIOmicaExamplesDirectory = os.path.join(UserDataDirectory, 'ExampleData')
ConstantPyIOmicaExampleVideosDirectory = os.path.join(UserDataDirectory, 'ExampleVideos')
for path in [ConstantPyIOmicaDataDirectory, ConstantPyIOmicaExamplesDirectory, ConstantPyIOmicaExampleVideosDirectory]:
    if not os.path.exists(path):
        os.makedirs(path)

del path
ConstantGeneDictionary = None