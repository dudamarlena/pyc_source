# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/locations.py
# Compiled at: 2017-04-23 10:30:41
import os
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.util import path_expand
__config_dir_prefix__ = os.path.join('~', '.cloudmesh')
__config_dir__ = path_expand(__config_dir_prefix__)

def config_file(filename):
    """
    The location of the config file: ~/.cloudmesh/filename. ~ will be expanded
    :param filename: the filename
    """
    return os.path.join(__config_dir__, filename)


def config_file_raw(filename):
    """
    The location of the config file: ~/.cloudmesh/filename. ~ will NOT be expanded
    :param filename: the filename
    """
    return os.path.join(__config_dir_prefix__, filename)


def config_file_prefix():
    """
    The prefix of the configuration file location
    """
    return __config_dir_prefix__


def config_dir_setup(filename):
    path = os.path.dirname(filename)
    if not os.path.isdir(path):
        Shell.mkdir(path)