# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/configuration.py
# Compiled at: 2020-01-13 19:20:43
# Size of source mod 2**32: 3002 bytes
import os, shutil
from pathlib import Path as P
import configparser
from cwl.specification import parse_schema
import logging
logger = logging.getLogger(__name__)
sbg_config_dir = P('sevenbridges', 'benten')
xdg_config_dir = {'env':'XDG_CONFIG_HOME', 
 'default':P(P.home(), '.config')}
xdg_data_home = {'env':'XDG_DATA_HOME', 
 'default':P(P.home(), '.local', 'share')}
default_config_data_dir = P(P(__file__).parent, '000.package.data')

class Configuration(configparser.ConfigParser):

    def __init__(self):
        super().__init__()
        self.cfg_path = P(os.getenv(xdg_config_dir['env'], xdg_config_dir['default']), sbg_config_dir)
        self.log_path = P(os.getenv(xdg_data_home['env'], xdg_data_home['default']), sbg_config_dir, 'logs')
        self.scratch_path = P(os.getenv(xdg_data_home['env'], xdg_data_home['default']), sbg_config_dir, 'scratch')
        if not self.cfg_path.exists():
            self.cfg_path.mkdir(parents=True)
        if not self.log_path.exists():
            self.log_path.mkdir(parents=True)
        if not self.scratch_path.exists():
            self.scratch_path.mkdir(parents=True)
        self.lang_models = {}

    def initialize(self):
        logging.info('Copying language schema files ...')
        self._copy_missing_language_files()
        logging.info('Loading language model ...')
        self._load_language_files()

    def optionxform(self, optionstr):
        return optionstr

    def getpath(self, section, option):
        return self._resolve_path(P(self.get(section, option)))

    def _resolve_path(self, path: P):
        """Paths in the config file can be absolute or relative. Absolute paths are left untouched
        relative paths are resolved relative to the configuration file location"""
        path = path.expanduser()
        if path.is_absolute():
            return path
        return P(self.cfg_path, path)

    def _copy_missing_language_files(self):
        for fn in ('schema-v1.0.json', 'schema-v1.1.json', 'schema-v1.2.0-dev1.json'):
            src_file = P(default_config_data_dir, fn)
            dst_file = P(self.cfg_path, fn)
            if not dst_file.exists():
                shutil.copy(src_file, dst_file)

    def _load_language_files(self):
        for fname in self.cfg_path.glob('schema-*.json'):
            version = fname.name[7:-5]
            self.lang_models[version] = parse_schema(fname)
            logger.info(f"Loaded language schema {version}")