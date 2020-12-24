# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/parsers/environment.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1073 bytes
from dexy.parser import Parser
from dexy.utils import parse_json

class Environment(Parser):
    __doc__ = '\n    Parent class for environment parsers.\n    '

    @classmethod
    def parse_environment_from_text(klass, text):
        pass

    def parse(self, parent_dir, config_text):
        config = self.parse_environment_from_text(config_text)
        self.ast.environment_for_directory.append((parent_dir, config))


class JsonEnvironment(Environment):
    __doc__ = '\n    Loads environment variables from a JSON file.\n    '
    aliases = ['dexy-env.json']

    @classmethod
    def parse_environment_from_text(klass, text):
        return parse_json(text)


class PythonEnvironment(Environment):
    __doc__ = '\n    Loads environment variables from a python script.\n    '
    aliases = ['dexy-env.py']

    @classmethod
    def parse_environment_from_text(klass, text):
        env = {}
        skip = ('env', 'skip', 'self', 'parent_dir', 'env_text')
        exec(text)
        for k, v in locals().items():
            if k not in skip:
                env[k] = v

        return env