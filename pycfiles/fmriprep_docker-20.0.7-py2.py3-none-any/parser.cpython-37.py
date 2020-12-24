# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/cli/parser.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 9480 bytes
"""Base option parser setup"""
from __future__ import absolute_import
import logging, optparse, sys, textwrap
from distutils.util import strtobool
from pip._vendor.six import string_types
from pip._internal.cli.status_codes import UNKNOWN_ERROR
from pip._internal.configuration import Configuration, ConfigurationError
from pip._internal.utils.compat import get_terminal_size
logger = logging.getLogger(__name__)

class PrettyHelpFormatter(optparse.IndentedHelpFormatter):
    __doc__ = 'A prettier/less verbose help formatter for optparse.'

    def __init__(self, *args, **kwargs):
        kwargs['max_help_position'] = 30
        kwargs['indent_increment'] = 1
        kwargs['width'] = get_terminal_size()[0] - 2
        (optparse.IndentedHelpFormatter.__init__)(self, *args, **kwargs)

    def format_option_strings(self, option):
        return self._format_option_strings(option)

    def _format_option_strings(self, option, mvarfmt=' <{}>', optsep=', '):
        """
        Return a comma-separated list of option strings and metavars.

        :param option:  tuple of (short opt, long opt), e.g: ('-f', '--format')
        :param mvarfmt: metavar format string
        :param optsep:  separator
        """
        opts = []
        if option._short_opts:
            opts.append(option._short_opts[0])
        if option._long_opts:
            opts.append(option._long_opts[0])
        if len(opts) > 1:
            opts.insert(1, optsep)
        if option.takes_value():
            metavar = option.metavar or option.dest.lower()
            opts.append(mvarfmt.format(metavar.lower()))
        return ''.join(opts)

    def format_heading(self, heading):
        if heading == 'Options':
            return ''
        return heading + ':\n'

    def format_usage(self, usage):
        """
        Ensure there is only one newline between usage and the first heading
        if there is no description.
        """
        msg = '\nUsage: {}\n'.format(self.indent_lines(textwrap.dedent(usage), '  '))
        return msg

    def format_description(self, description):
        if description:
            if hasattr(self.parser, 'main'):
                label = 'Commands'
            else:
                label = 'Description'
            description = description.lstrip('\n')
            description = description.rstrip()
            description = self.indent_lines(textwrap.dedent(description), '  ')
            description = '{}:\n{}\n'.format(label, description)
            return description
        return ''

    def format_epilog(self, epilog):
        if epilog:
            return epilog
        return ''

    def indent_lines(self, text, indent):
        new_lines = [indent + line for line in text.split('\n')]
        return '\n'.join(new_lines)


class UpdatingDefaultsHelpFormatter(PrettyHelpFormatter):
    __doc__ = 'Custom help formatter for use in ConfigOptionParser.\n\n    This is updates the defaults before expanding them, allowing\n    them to show up correctly in the help listing.\n    '

    def expand_default(self, option):
        if self.parser is not None:
            self.parser._update_defaults(self.parser.defaults)
        return optparse.IndentedHelpFormatter.expand_default(self, option)


class CustomOptionParser(optparse.OptionParser):

    def insert_option_group(self, idx, *args, **kwargs):
        """Insert an OptionGroup at a given position."""
        group = (self.add_option_group)(*args, **kwargs)
        self.option_groups.pop()
        self.option_groups.insert(idx, group)
        return group

    @property
    def option_list_all(self):
        """Get a list of all options, including those in option groups."""
        res = self.option_list[:]
        for i in self.option_groups:
            res.extend(i.option_list)

        return res


class ConfigOptionParser(CustomOptionParser):
    __doc__ = 'Custom option parser which updates its defaults by checking the\n    configuration files and environmental variables'

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        isolated = kwargs.pop('isolated', False)
        self.config = Configuration(isolated)
        assert self.name
        (optparse.OptionParser.__init__)(self, *args, **kwargs)

    def check_default(self, option, key, val):
        try:
            return option.check_value(key, val)
        except optparse.OptionValueError as exc:
            try:
                print('An error occurred during configuration: {}'.format(exc))
                sys.exit(3)
            finally:
                exc = None
                del exc

    def _get_ordered_configuration_items(self):
        override_order = [
         'global', self.name, ':env:']
        section_items = {name:[] for name in override_order}
        for section_key, val in self.config.items():
            if not val:
                logger.debug("Ignoring configuration key '%s' as it's value is empty.", section_key)
                continue
            section, key = section_key.split('.', 1)
            if section in override_order:
                section_items[section].append((key, val))

        for section in override_order:
            for key, val in section_items[section]:
                yield (
                 key, val)

    def _update_defaults(self, defaults):
        """Updates the given defaults with values from the config files and
        the environ. Does a little special handling for certain types of
        options (lists)."""
        self.values = optparse.Values(self.defaults)
        late_eval = set()
        for key, val in self._get_ordered_configuration_items():
            option = self.get_option('--' + key)
            if option is None:
                continue
            elif option.action in ('store_true', 'store_false', 'count'):
                try:
                    val = strtobool(val)
                except ValueError:
                    error_msg = invalid_config_error_message(option.action, key, val)
                    self.error(error_msg)

            else:
                if option.action == 'append':
                    val = val.split()
                    val = [self.check_default(option, key, v) for v in val]
                else:
                    if option.action == 'callback':
                        late_eval.add(option.dest)
                        opt_str = option.get_opt_string()
                        val = option.convert_value(opt_str, val)
                        args = option.callback_args or ()
                        kwargs = option.callback_kwargs or {}
                        (option.callback)(option, opt_str, val, self, *args, **kwargs)
                    else:
                        val = self.check_default(option, key, val)
            defaults[option.dest] = val

        for key in late_eval:
            defaults[key] = getattr(self.values, key)

        self.values = None
        return defaults

    def get_default_values(self):
        """Overriding to make updating the defaults after instantiation of
        the option parser possible, _update_defaults() does the dirty work."""
        if not self.process_default_values:
            return optparse.Values(self.defaults)
        try:
            self.config.load()
        except ConfigurationError as err:
            try:
                self.exit(UNKNOWN_ERROR, str(err))
            finally:
                err = None
                del err

        defaults = self._update_defaults(self.defaults.copy())
        for option in self._get_all_options():
            default = defaults.get(option.dest)
            if isinstance(default, string_types):
                opt_str = option.get_opt_string()
                defaults[option.dest] = option.check_value(opt_str, default)

        return optparse.Values(defaults)

    def error(self, msg):
        self.print_usage(sys.stderr)
        self.exit(UNKNOWN_ERROR, '{}\n'.format(msg))


def invalid_config_error_message(action, key, val):
    """Returns a better error message when invalid configuration option
    is provided."""
    if action in ('store_true', 'store_false'):
        return '{0} is not a valid value for {1} option, please specify a boolean value like yes/no, true/false or 1/0 instead.'.format(val, key)
    return '{0} is not a valid value for {1} option, please specify a numerical value like 1/0 instead.'.format(val, key)