# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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