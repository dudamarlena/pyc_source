# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: yac/lib/paths.py
# Compiled at: 2017-11-16 20:28:41
import os

def get_config_path():
    config_path = os.path.join(os.path.dirname(__file__), '../', 'config')
    return config_path


def get_root_path():
    root_path = os.path.join(os.path.dirname(__file__), '../')
    return root_path


def get_yac_path():
    yac_path = os.path.join(os.path.dirname(__file__), '../../')
    return yac_path


def get_lib_path():
    lib_path = os.path.join(os.path.dirname(__file__))
    return lib_path