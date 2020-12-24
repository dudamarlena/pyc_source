# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/scikits/ann/setup.py
# Compiled at: 2008-01-29 21:41:27
"""
setup.py

Created by Barry Wark on 2007-11-07.
Copyright (c) 2007 Barry Wark. All rights reserved.
"""
import os, os.path
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration

def configuration(parent_package='', top_path=None):
    config = Configuration('ann', parent_package, top_path)
    assert 'ANN_LIB' in os.environ
    assert 'ANN_INCLUDE' in os.environ
    ann_library_dir = os.environ['ANN_LIB']
    ann_include_dir = os.environ['ANN_INCLUDE']
    config.add_extension('_ANN', sources=[
     'ANN.i'], include_dirs=[
     '.', ann_include_dir], library_dirs=[
     ann_library_dir], libraries=[
     'ANN'], language='c++', swig_opts='-c++')
    config.add_subpackage('tests')
    return config


if __name__ == '__main__':
    setup(configuration=configuration)