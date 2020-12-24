# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lib/chimera_cli/yaml_config.py
# Compiled at: 2019-12-26 07:40:58
# Size of source mod 2**32: 954 bytes
from yaml import Loader, load
from glob import glob
from typing import Dict, List

class NoConfigurationFilesException(Exception):
    pass


class configuration_files:

    def __getitem__(self, key: str) -> List[Dict[(str, any)]]:
        return list(filter(lambda x: x['namespace'] == key, self.files))

    def get_from_type(self, key: str) -> List[Dict[(str, any)]]:
        return list(filter(lambda x: x['type'] == key), self.files)

    def __init__(self):
        print('Finding all configuration files...')
        files = glob('**/.chimera/**/*.yaml', recursive=True)
        if len(files) == 0:
            raise NoConfigurationFilesException("Review your configuration files inside the '.chimera' folder.")
        self.files = []
        for path in files:
            with open(path) as (f):
                teste = load(f, Loader=Loader)
                self.files += [teste]

        print('Configuration loaded!')