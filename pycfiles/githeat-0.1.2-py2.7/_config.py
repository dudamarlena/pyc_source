# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/githeat/core/_config.py
# Compiled at: 2016-07-07 01:11:03
""" Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

"""
from __future__ import absolute_import
from re import compile
from yaml import load
from ._logger import logger
__all__ = ('config', )

class _AttrDict(dict):
    """ A dict with attribute access.

    """

    def __getattr__(self, name):
        """ Access a dict value as an attribute.

        """
        value = self[name]
        if isinstance(value, dict):
            value = _AttrDict(value)
        return value


class _Config(_AttrDict):
    """ Store configuration data.

    Data can be accessed as dict values or object attributes.

    """

    def __init__(self, paths=None, params=None):
        """ Initialize this object.

        """
        super(_Config, self).__init__()
        if paths:
            self.load(paths)

    def load(self, paths, params=None):
        """ Load data from configuration files.

        Configuration values are read from a sequence of one or more YAML
        files. Files are read in the given order, and a duplicate value will
        overwrite the existing value.

        The optional 'params' argument is a dict-like object to use for
        parameter substitution in the config files. Any text matching "%key;"
        will be replaced with the value for 'key' in params.

        """

        def replace(match):
            """ Callback for re.sub to do parameter replacement. """
            return params[match.group(0)]

        self.clear()
        params = {('%{:s};').format(key):val for key, val in params.iteritems()} if params else {}
        regex = compile(('|').join(params) or '^(?!)')
        for path in paths:
            try:
                with open(path, 'r') as (stream):
                    logger.info(('reading config data from {:s}').format(path))
                    yaml = regex.sub(replace, stream.read())
                    self.update(load(yaml))
            except TypeError:
                logger.warn(("config file '{:s}' is empty").format(yaml))
            except IOError:
                logger.warn(("config file '{:s}' does not exist").format(path))


config = _Config()