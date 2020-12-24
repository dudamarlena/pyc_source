# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/hakan/Desktop/project/unimport/unimport/config.py
# Compiled at: 2020-04-09 19:08:42
# Size of source mod 2**32: 2489 bytes
import configparser
try:
    import toml
    HAS_TOML = True
except ImportError:
    HAS_TOML = False

CONFIG_FILES = {'setup.cfg': 'unimport'}
if HAS_TOML is True:
    CONFIG_FILES.update({'pyproject.toml': 'tool.unimport'})
DEFAULT_EXCLUDES = {
 '**/*.git**',
 '**/*.github**',
 '**/*build**',
 '**/*__pycache__**',
 '**/*develop-eggs**',
 '**/*dist**',
 '**/*downloads**',
 '**/*eggs**',
 '**/*lib**',
 '**/*lib64**',
 '**/*parts**',
 '**/*sdist**',
 '**/*var**',
 '**/*wheels**',
 '**/*.egg-info**',
 '**/*MANIFEST**',
 '**/*htmlcov**',
 '**/*.tox**',
 '**/*.hypothesis**',
 '**/*.pytest_cache**',
 '**/*instance**',
 '**/*docs**',
 '**/*target**',
 '**/*celerybeat-schedul**',
 '**/*.venv**',
 '**/*env**',
 '**/*venv**',
 '**/*site**',
 '**/*.mypy_cache**',
 '**/*.sage.py',
 '**/*local_settings.py',
 '**/*__init__.py'}

class Config:

    def __init__(self, config_file=None):
        self.exclude = DEFAULT_EXCLUDES.copy()
        self.config_file = config_file
        self.config_path, self.section = self.find_config()
        if self.config_path is not None:
            self.parse()

    @staticmethod
    def is_available_to_parse(config_path):
        if config_path.suffix == '.toml':
            if HAS_TOML is False:
                return False
        return config_path.exists()

    def find_config(self):
        config_files = dict(CONFIG_FILES)
        if self.config_file is not None:
            if self.config_file.name in config_files:
                return (
                 self.config_file, config_files[self.config_file.name])
        if self.config_file:
            for file_name, section in config_files.items():
                config_path = self.config_file / file_name
                if self.is_available_to_parse(config_path):
                    return (
                     config_path, section)

        return (None, None)

    def parse(self):
        getattr(self, f"parse_{self.config_path.suffix.strip('.')}")()

    def parse_cfg(self):
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_path)
        if parser.has_section(self.section):
            self.exclude.update(parser.get(self.section, 'exclude').split())

    def parse_toml(self):
        parsed_toml = toml.loads(self.config_path.read_text())
        config = parsed_toml.get('tool', {}).get('unimport', {})
        self.exclude.update(set(config.get('exclude', [])))