# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyramid/setup.py
# Compiled at: 2018-11-02 11:39:14
from __future__ import absolute_import
import os
from pyramid._build_utils import maybe_cythonize_extensions

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    libs = []
    if os.name == 'posix':
        libs.append('m')
    config = Configuration('pyramid', parent_package, top_path)
    config.add_subpackage('__check_build')
    config.add_subpackage('__check_build/tests')
    config.add_subpackage('_build_utils')
    config.add_subpackage('_build_utils/tests')
    config.add_subpackage('compat')
    config.add_subpackage('compat/tests')
    config.add_subpackage('datasets')
    config.add_subpackage('datasets/tests')
    config.add_subpackage('utils')
    config.add_subpackage('utils/tests')
    config.add_subpackage('arima')
    config.add_subpackage('arima/tests')
    maybe_cythonize_extensions(top_path, config)
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())