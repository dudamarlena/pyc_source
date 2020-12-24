# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ruamel/yaml/configobjwalker.py
# Compiled at: 2017-07-27 07:36:53
import warnings
from ruamel.yaml.util import configobj_walker as new_configobj_walker

def configobj_walker(cfg):
    warnings.warn('configobj_walker has move to ruamel.yaml.util, please update your code')
    return new_configobj_walker(cfg)