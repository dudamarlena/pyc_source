# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/config/salveconfig.py
# Compiled at: 2015-11-06 23:45:35
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import logging, os, string, salve, salve.log
from salve import ugo
from salve.context import FileContext, ExecutionContext
from salve.exceptions import SALVEException
from .parser import SALVEConfigParser
SALVE_ENV_PREFIX = 'SALVE_'

class SALVEConfig(object):
    """
    SALVE's configuration is stored statefully as
    an object. In this way, configuration can be modified
    if we support an interactive mode in the future.
    SALVE will also load special values from the environment
    so that users can make ephemeral changes to configuration
    without modifying the config files. They also offer a way
    of guaranteeing that the configuration values are as desired
    without inspecting the files.
    """

    def __init__(self, filename=None):
        """
        SALVEConfig constructor.

        KWArgs:
            @filename
            The specific config file to create Config from. Defaults to
            None, which indicates that the defaults and ~/.salverc
            should be used without any supplement.
        """
        user = os.environ['USER']
        if 'SUDO_USER' in os.environ:
            user = os.environ['SUDO_USER']
        userhome = os.path.expanduser('~' + user)
        self.env = {}
        for k in os.environ:
            self.env[k] = os.environ[k]

        self.env['USER'] = user
        self.env['HOME'] = userhome
        self.env['SALVE_USER_PRIMARY_GROUP'] = ugo.get_group_from_username(user)
        self.filename = filename
        try:
            conf = SALVEConfigParser(userhome, filename)
        except configparser.Error as e:
            raise SALVEException('Encountered an error while parsing your ' + 'configuration file(s).\n%s' % e.message, FileContext(filename))

        sections = conf.sections()
        self.attributes = dict((s.lower(), dict((k.lower(), v) for k, v in conf.items(s))) for s in sections)
        self._apply_environment_overrides()
        self._set_context_globals()

    def _apply_environment_overrides(self):
        salve_env = dict((k, self.env[k]) for k in self.env if k.startswith(SALVE_ENV_PREFIX) and k.isupper())
        prefixes = dict((SALVE_ENV_PREFIX + s.upper(), s) for s in self.attributes)
        for key in salve_env:
            for p in prefixes:
                if key.startswith(p):
                    subdict = self.attributes[prefixes[p]]
                    subkey = key[len(p) + 1:].lower()
                    subdict[subkey] = salve_env[key]

    def _set_context_globals(self):
        for key in self.attributes['global']:
            val = self.template(self.attributes['global'][key])
            if key == 'run_log':
                salve.log.add_logfile(salve.logger, logging.NOTSET, val)
            if key == 'log_level':
                val = salve.log.str_to_level(val)
                salve.logger.setLevel(val)
            ExecutionContext()[key] = val

    def template(self, template_string):
        """
        Given a @template_string, takes the environment stored in the
        SALVE configuration object and uses it to replace placeholders

        Returns a new string in which placeholders have been replaced,
        or raises a KeyError if they are not found.

        Args:
            @template_string
            A string containing variables meant to be replaced with
            environment variables, as represented or overridden in the
            Config.
        """
        temp = string.Template(template_string)
        return temp.substitute(self.env)

    def apply_to_block(self, block):
        """
        Given a @block produced by the parser, takes any settings which
        describe defaults and uses them to populate any missing attrs
        of the block.

        Args:
            @block
            The block to which Config attributes should be applied. The
            general policy is to only apply attributes that are not
            already specified.
        """
        ty = block.block_type.lower()
        relevant_attrs = self.attributes[ty]
        for key in relevant_attrs:
            if key not in block.attrs:
                block[key] = relevant_attrs[key]

        for key in self.attributes['default']:
            if key not in block.attrs:
                block[key] = self.attributes['default'][key]

        for key in block.attrs:
            block[key] = self.template(block[key])