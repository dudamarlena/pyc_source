# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/hep_spt/stats/setup.py
# Compiled at: 2019-11-15 13:21:53
"""
Configuration file for the modules in the "stats" subpackage.
"""
__author__ = 'Miguel Ramos Pernas'
__email__ = 'miguel.ramos.pernas@cern.ch'

def configuration(parent_package='', top_path=''):
    """
    Function to do the configuration.
    """
    from numpy.distutils.misc_util import Configuration
    config = Configuration('stats', parent_package, top_path)
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)