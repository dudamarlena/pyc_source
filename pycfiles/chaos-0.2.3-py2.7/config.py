# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chaos/config.py
# Compiled at: 2014-04-03 12:01:42
"""
Helper functions for loading ConfigObj configuration files.

Care must be taken to catch any ParseErrors that the underlying ConfigObj code may raise,
these functions explicitely do not catch them.
"""
from __future__ import absolute_import
import logging, os, inspect
from configobj import ConfigObj, ConfigObjError
from validate import Validator
from .globber import Globber

def get_config(config_base, custom_file=None, configspec=None):
    """
        Loads a configuration file from multiple locations, and merge the results into one.

        This function will load configuration files from a number of locations in sequence,
        and will overwrite values in the previous level if they are redefined in the current.

        The levels are in sequence:

        1. Distribution level configuration in the program directory called $config_base.config.
        2. System-wide level configuration in /etc/$config_base.config
        3. User level configuration in ~/.$config_base.config
        4. An optionally specified $custom_file

        Parameters
        ----------
        config_base: string
                Basename of the configuration file, typically the same as the name of the program.
        custom_file: string
                Absolute path to a custom configuration file.
        configspec: ConfigObj
                Used to sanitize the values in the resulting ConfigObj. Validation errors are currently
                not exposed to the caller.
        """
    logger = logging.getLogger(__name__)
    logger.debug('Expanding variables')
    home = os.path.expanduser('~')
    loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    logger.debug('Create empty config')
    config = ConfigObj()
    if os.path.isfile(os.path.join(loc, '%s.config' % config_base)):
        logger.debug('Loading config from workingdir')
        cfg = ConfigObj(os.path.join(loc, '%s.config' % config_base), configspec=configspec)
        if configspec:
            cfg.validate(Validator())
        config.merge(cfg)
    if os.path.isfile('/etc/%s.config' % config_base):
        logger.debug('Loading config from /etc')
        cfg = ConfigObj('/etc/%s.config' % config_base, configspec=configspec)
        if configspec:
            cfg.validate(Validator())
        config.merge(cfg)
    if os.path.isfile(os.path.join(home, '.%s.config' % config_base)):
        logger.debug('Loading config from homedir')
        cfg = ConfigObj(os.path.join(home, '.%s.config' % config_base), configspec=configspec)
        if configspec:
            cfg.validate(Validator())
        config.merge(cfg)
    if custom_file:
        logger.debug('Loading custom config file')
        cfg = ConfigObj(custom_file, configspec=configspec)
        if configspec:
            cfg.validate(Validator())
        config.merge(cfg)
    return config


def get_config_dir(path, pattern='*.config', configspec=None, allow_errors=False):
    """
        Load an entire directory of configuration files, merging them into one.

        This function will load multiple configuration files matching the given pattern,
        in the given path, and merge them. The found files are first sorted alphabetically,
        and then loaded and merged. A good practice is to use ConfigObj sections, for easy
        loading of information like per-host configuration.

        Parameters
        ----------
        path: string
                Absolute path to a directory of ConfigObj files
        pattern: string
                Globbing pattern used to find files. Defaults to *.config.
        configspec: ConfigObj
                Used to sanitize the values in the resulting ConfigObj. Validation errors are currently
                not exposed to the caller.
        allow_errors: boolean
                If False, errors raised by ConfigObj are not caught.
                If True, errors raise by ConfigObj are caught, and an error is logged using logger.
        """
    logger = logging.getLogger(__name__)
    logger.debug(('Loading all files matching {0} in {1}').format(pattern, path))
    files = Globber(path, include=[pattern], recursive=False).glob()
    files = sorted(files)
    config = ConfigObj()
    for filename in files:
        logger.debug(('- Loading config for {0}').format(filename))
        try:
            conf = ConfigObj(filename, configspec=configspec)
        except ConfigObjError as coe:
            logger.error(('An error occurred while parsing {0}: {1}').format(filename, str(coe)))
            continue

        if configspec:
            conf.validate(Validator())
        config.merge(conf)

    return config