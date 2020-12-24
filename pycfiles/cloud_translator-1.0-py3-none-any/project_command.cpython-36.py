# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\cloud_training\project_command.py
# Compiled at: 2017-10-29 21:39:23
# Size of source mod 2**32: 2328 bytes
import json, os
from argparse import Namespace
from cloud_training import configure
from cloud_training.abstract_command import AbstractCommand
from cloud_training.aws import Aws

class ProjectCommand(AbstractCommand):

    def __init__(self, args):
        """Abstract class to implement a command that interacts with a project"""
        super().__init__(args)
        for key in self._settings:
            if self._settings[key] is None:
                raise ValueError('Use the "cloud-training configure" command to configure the tool.')

        self._project_dir = self._args.project_dir
        if not os.path.isabs(self._project_dir):
            self._project_dir = os.path.abspath(os.path.join(os.getcwd(), self._project_dir))
        self._project_config = self._get_project_config()
        if not self._project_config:
            raise ValueError('"cloud_training.json" was not found in the project directory.')
        self._project_config = {**{'project_name':None, 
         'package_name':None}, **(self._project_config)}
        if not self._project_config['project_name']:
            raise ValueError('"project_name" is not defined in the config file.')
        if not self._project_config['package_name']:
            raise ValueError('"package_name" is not defined in the config file.')
        self._s3_project_dir = 's3://' + self._settings['s3_bucket'] + '/projects/' + self._project_config['project_name']
        if self._args.model is None:
            raise ValueError('The model is not specified.')
        self._model = self._args.model
        self._aws = Aws(configure.get_aws_profile_name(self._args.profile))

    def _get_project_config(self):
        """Returns a project configuration"""
        config = None
        config_file = os.path.join(self._project_dir, 'cloud_training.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as (f):
                config = json.load(f)
        return config