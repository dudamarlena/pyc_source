# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/action.py
# Compiled at: 2016-02-23 09:10:32
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
from collections import OrderedDict
import path, introspection, ConfigParser

def action_factory(config_section_items):
    actions = OrderedDict()
    for a in config_section_items:
        d = dict(config_section_items[a])
        if 'type' in d:
            actions[a] = introspection.get_class_one_arg(d['type'], d)

    return actions


class CopyFile(object):

    def __init__(self, param_dict):
        self.source = path.path(param_dict['source'])
        self.target = path.path(param_dict['target'])

    def execute(self, input_values):
        self.source.copy(self.target)


class CopyINIFileAddParam(object):

    def __init__(self, param_dict):
        self.source = path.path(param_dict['source'])
        self.target = path.path(param_dict['target'])
        self.param_section = param_dict['param_section']
        self.param_name = param_dict['param_name']
        self.param_value_ref = param_dict['param_value_ref']

    def execute(self, input_values):
        self.source.copy(self.target)
        config = ConfigParser.ConfigParser(allow_no_value=True)
        fp = self.target.open()
        config.readfp(fp)
        fp.close()
        config.set(self.param_section, self.param_name, input_values[self.param_value_ref])
        with self.target.open('wb') as (configfile):
            config.write(configfile)