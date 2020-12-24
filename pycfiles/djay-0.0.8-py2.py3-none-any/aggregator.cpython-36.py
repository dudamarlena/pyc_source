# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/flake8/flake8/options/aggregator.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 3225 bytes
"""Aggregation function for CLI specified options and config file options.

This holds the logic that uses the collected and merged config files and
applies the user-specified command-line configuration on top of it.
"""
import logging
from flake8.options import config
LOG = logging.getLogger(__name__)

def aggregate_options(manager, config_finder, arglist=None, values=None):
    """Aggregate and merge CLI and config file options.

    :param flake8.options.manager.OptionManager manager:
        The instance of the OptionManager that we're presently using.
    :param flake8.options.config.ConfigFileFinder config_finder:
        The config file finder to use.
    :param list arglist:
        The list of arguments to pass to ``manager.parse_args``. In most cases
        this will be None so ``parse_args`` uses ``sys.argv``. This is mostly
        available to make testing easier.
    :param optparse.Values values:
        Previously parsed set of parsed options.
    :returns:
        Tuple of the parsed options and extra arguments returned by
        ``manager.parse_args``.
    :rtype:
        tuple(optparse.Values, list)
    """
    default_values, _ = manager.parse_args([], values=values)
    original_values, _ = manager.parse_args(arglist)
    config_parser = config.MergedConfigParser(option_manager=manager,
      config_finder=config_finder)
    parsed_config = config_parser.parse(original_values.config, original_values.isolated)
    extended_default_ignore = manager.extended_default_ignore.copy()
    LOG.debug('Extended default ignore list: %s', list(extended_default_ignore))
    extended_default_ignore.update(default_values.ignore)
    default_values.ignore = list(extended_default_ignore)
    LOG.debug('Merged default ignore list: %s', default_values.ignore)
    extended_default_select = manager.extended_default_select.copy()
    LOG.debug('Extended default select list: %s', list(extended_default_select))
    default_values.extended_default_select = extended_default_select
    for config_name, value in parsed_config.items():
        dest_name = config_name
        if not hasattr(default_values, config_name):
            dest_name = config_parser.config_options[config_name].dest
        LOG.debug('Overriding default value of (%s) for "%s" with (%s)', getattr(default_values, dest_name, None), dest_name, value)
        setattr(default_values, dest_name, value)

    return manager.parse_args(arglist, default_values)