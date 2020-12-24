# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/_argparse.py
# Compiled at: 2019-09-28 20:42:58
# Size of source mod 2**32: 3234 bytes
import sys, argparse, gettext
_ = gettext.gettext

class ArgumentParser(argparse.ArgumentParser):
    __doc__ = 'ArgumentParser with optional logging, config, and sub-command support.'

    def __init__(self, add_log_args=False, config_opts=None, **kwargs):
        (super().__init__)(**kwargs)
        if add_log_args:
            from . import logger
            logger.addCommandLineArgs(self)
        self._add_log_args = add_log_args
        if config_opts:
            from . import config
            config.addCommandLineArgs(self, config_opts)
        self._config_opts = config_opts
        self._subcmd_required = None

    def parse_known_args(self, args=None, namespace=None):
        from . import logger
        parsed, remaining = super().parse_known_args(args=args, namespace=namespace)
        if self._subcmd_required is not None:
            req, dest = self._subcmd_required
            if req:
                if dest:
                    hasattr(parsed, dest) and getattr(parsed, dest) or self.error(_('the following arguments are required: %s') % dest)
        if 'config' in parsed:
            if 'config_overrides' in parsed:
                config = parsed.config
                overrides = parsed.config_overrides or []
                for sect, subst in overrides:
                    key, val = subst
                    if not config.has_section(sect):
                        config.add_section(sect)
                    config.set(sect, key, val)

        if 'config_show_default' in parsed:
            if parsed.config_show_default:
                print(self._config_opts.default_config)
                self.exit(0)
        if self._add_log_args:
            parsed.applyLoggingOpts = logger.applyLoggingOpts
        return (parsed, remaining)

    def add_subparsers(self, add_help_subcmd=False, required=True, dest='subcmd', **kwargs):
        if 'parser_class' not in kwargs:
            kwargs['parser_class'] = ArgumentParser
        elif sys.version_info[:2] >= (3, 7):
            subparser = (super().add_subparsers)(required=required, dest=dest, **kwargs)
        else:
            self._subcmd_required = (
             required, dest)
            subparser = (super().add_subparsers)(dest=dest, **kwargs)
        if add_help_subcmd:

            def _help(args):
                if args.command:
                    self.parse_args([args.command, '--help'])
                else:
                    self.print_help()
                self.exit(0)

            help = subparser.add_parser('help', help='Show help for a sub command')
            help.set_defaults(command_func=_help)
            help.add_argument('command', nargs='?', default=None)
        return subparser