# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/configuration/sources/envvars.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 1754 bytes
import os, sys, typing as tp
from satella.coding.recast_exceptions import rethrow_as
from satella.exceptions import ConfigurationError
from .base import BaseSource
from .format import JSONSource
__all__ = [
 'EnvVarsSource', 'EnvironmentSource']

class EnvironmentSource(BaseSource):
    __doc__ = "\n    This just returns a dictionary of { env_name => that env's value }\n    "
    __slots__ = ('env_name', 'config_name', 'cast_to')

    def __init__(self, env_name, config_name=None, cast_to=lambda v: v):
        """
        env_name -- name of the environment variable to check for
        config_name -- name of the env_name in the dictionary to return
        """
        super(EnvironmentSource, self).__init__()
        self.env_name = env_name
        self.config_name = config_name or env_name
        self.cast_to = cast_to

    @rethrow_as((ValueError, TypeError, KeyError), ConfigurationError)
    def provide(self) -> dict:
        v = self.cast_to(os.environ[self.env_name])
        return {self.config_name: v}


class EnvVarsSource(JSONSource):
    __doc__ = '\n    Return a dictionary that is the JSON encoded within a particular environment variable\n    '
    __slots__ = ('env_name', )

    def __init__(self, env_name):
        super(EnvVarsSource, self).__init__('', encoding=(sys.getfilesystemencoding()))
        self.env_name = env_name

    @rethrow_as(KeyError, ConfigurationError)
    def provide(self):
        self.root = os.environ[self.env_name]
        return super(EnvVarsSource, self).provide()