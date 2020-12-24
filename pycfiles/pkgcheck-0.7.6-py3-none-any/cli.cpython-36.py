# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/cli.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 1768 bytes
"""Various command-line specific support."""
import configparser, os
from pkgcore.util import commandline
from snakeoil.cli import arghparse
from snakeoil.cli.exceptions import UserException
from snakeoil.contexts import patch
from snakeoil.klass import jit_attr
from snakeoil.log import suppress_logging

class Tool(commandline.Tool):
    __doc__ = 'Suppress log messages globally.'

    def main(self):
        with suppress_logging():
            return super().main()


class ConfigArgumentParser(arghparse.ArgumentParser):
    __doc__ = 'Argument parser that supports loading settings from specified config files.'

    def __init__(self, configs=(), **kwargs):
        (super().__init__)(**kwargs)
        self.configs = tuple(x for x in set(configs) if os.path.isfile(x))

    @jit_attr
    def config(self):
        """Config file object related to a given parser."""
        config = configparser.ConfigParser()
        try:
            for f in self.configs:
                config.read(f)

        except configparser.ParsingError as e:
            raise UserException(f"parsing config file failed: {e}")

        return config

    def parse_config_options(self, namespace, section='DEFAULT'):
        """Parse options from config if they exist."""
        config_args = [f"--{k}={v}" if v else f"--{k}" for k, v in self.config.items(section)]
        if config_args:
            with patch('snakeoil.cli.arghparse.ArgumentParser.error', self._config_error):
                namespace, _ = self.parse_known_optionals(config_args, namespace)
        return namespace

    def _config_error(self, message, status=2):
        """Stub to replace error method that notes config failure."""
        self.exit(status, f"{self.prog}: failed loading config: {message}\n")