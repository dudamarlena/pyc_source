# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/config.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import pprint, radical.utils.config as ruc, radical.utils.singleton as rus

class Configuration(ruc.Configurable):
    __metaclass__ = rus.Singleton

    def __init__(self):
        ruc.Configurable.__init__(self, 'troy')
        _general_section = [
         {'category': 'general', 
            'name': 'output_directory', 
            'type': str, 
            'default': '', 
            'valid_options': '', 
            'documentation': 'Troy working directory', 
            'env_variable': ''},
         {'category': 'general', 
            'name': 'log_level', 
            'type': str, 
            'default': '0', 
            'valid_options': [
                            '0', '1', '2', '3'], 
            'documentation': 'Verbosity mode', 
            'env_variable': ''}]
        ruc.Configurable.config_options(self, 'general', _general_section)
        _bundle_section = [
         {'category': 'bundle', 
            'name': 'mode', 
            'type': str, 
            'default': 'local', 
            'valid_options': [
                            'local', 'remote'], 
            'documentation': 'Mode of operation for bundles.', 
            'env_variable': ''},
         {'category': 'bundle', 
            'name': 'finished_job_trace', 
            'type': str, 
            'default': '', 
            'valid_options': '', 
            'documentation': 'Storage of finished job traces for bundles', 
            'env_variable': ''}]
        ruc.Configurable.config_options(self, 'bundle', _bundle_section)
        cd = self.get_config_as_dict()
        all_sections = cd.keys()
        self.compute_sections = filter(lambda x: x.startswith('compute:'), all_sections)
        for section_name in self.compute_sections:
            _compute_section_template = [
             {'category': section_name, 
                'name': 'endpoint', 
                'type': str, 
                'default': '', 
                'valid_options': '', 
                'documentation': 'This option specifies the endpoint address of the resource', 
                'env_variable': ''},
             {'category': section_name, 
                'name': 'type', 
                'type': str, 
                'default': 'moab', 
                'valid_options': [
                                'moab', 'pbs'], 
                'documentation': 'This option specifies the type endpoint address of the resource', 
                'env_variable': ''},
             {'category': section_name, 
                'name': 'port', 
                'type': str, 
                'default': '22', 
                'valid_options': '', 
                'documentation': 'Port to use at endpoint address of the resource', 
                'env_variable': ''},
             {'category': section_name, 
                'name': 'username', 
                'type': str, 
                'default': '', 
                'valid_options': '', 
                'documentation': 'This option specifies the endpoint address of the resource', 
                'env_variable': ''},
             {'category': section_name, 
                'name': 'ssh_key', 
                'type': str, 
                'default': '', 
                'valid_options': '', 
                'documentation': 'This option specifies the ssh key to use with the resource', 
                'env_variable': ''},
             {'category': section_name, 
                'name': 'password', 
                'type': str, 
                'default': '', 
                'valid_options': '', 
                'documentation': 'Specifies the password to use with the resource', 
                'env_variable': ''},
             {'category': section_name, 
                'name': 'h_flag', 
                'type': bool, 
                'default': True, 
                'valid_options': '', 
                'documentation': 'Heterogenerous resource type', 
                'env_variable': ''}]
            ruc.Configurable.config_options(self, section_name, _compute_section_template)
            c = ruc.Configurable.get_config(self, section_name)
            endpoint = c['endpoint'].get_value()