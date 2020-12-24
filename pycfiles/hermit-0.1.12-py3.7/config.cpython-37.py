# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/config.py
# Compiled at: 2020-01-08 10:49:47
# Size of source mod 2**32: 2696 bytes
import yaml
from os import path, environ
from typing import Dict

class HermitConfig:
    __doc__ = 'Object to hold Hermit configuration\n\n    Hermit reads its configuration from a YAML file on disk at\n    `/etc/hermit.yaml` (by default).\n\n    The following settings are supported:\n\n    * `shards_file` -- path to store shards\n    * `plugin_dir` -- directory containing plugins\n    * `commands` -- a dictionary of command lines used to manipulate storage, see :attribute:`hermit.HermitConfig.DefaultCommands`.\n\n    '
    DefaultCommands = {'persistShards':'cat {0} | gzip -c - > {0}.persisted', 
     'backupShards':'cp {0}.persisted {0}.backup', 
     'restoreBackup':'zcat {0}.backup > {0}', 
     'getPersistedShards':'zcat {0}.persisted > {0}'}
    DefaultPaths = {'config_file':'/etc/hermit.yaml', 
     'shards_file':'/tmp/shard_words.bson', 
     'plugin_dir':'/var/lib/hermit'}

    def __init__(self, config_file: str):
        """
        Initialize Hermit configuration

        :param config_file: the path to the YAML configuration file
        """
        self.config_file = config_file
        self.shards_file = self.DefaultPaths['shards_file']
        self.plugin_dir = self.DefaultPaths['plugin_dir']
        self.config = {}
        self.commands = {}
        if path.exists(config_file):
            self.config = yaml.safe_load(open(config_file))
        if 'shards_file' in self.config:
            self.shards_file = self.config['shards_file']
        if 'plugin_dir' in self.config:
            self.plugin_dir = self.config['plugin_dir']
        if 'commands' in self.config:
            self.commands = self.config['commands']
        defaults = self.DefaultCommands.copy()
        for key in defaults:
            if key not in self.commands:
                self.commands[key] = defaults[key]

        for key in self.commands:
            formatted_key = self.commands[key].format(self.shards_file)
            self.commands[key] = formatted_key

    @classmethod
    def load(cls):
        return HermitConfig(environ.get('HERMIT_CONFIG', cls.DefaultPaths['config_file']))