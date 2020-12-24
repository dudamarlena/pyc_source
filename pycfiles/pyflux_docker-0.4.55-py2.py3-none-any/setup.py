# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/var/setup.py
# Compiled at: 2018-02-01 11:59:15
import os

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('var', parent_package, top_path)
    config.add_extension('var_recursions', sources=[
     'var_recursions.c'])
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())