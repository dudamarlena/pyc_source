# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/__main__.py
# Compiled at: 2020-02-26 23:34:27
# Size of source mod 2**32: 4145 bytes
import os, sys, traceback
from sqlalchemy import exc as sql_exceptions
from nicfit.console import ansi
from nicfit import Application, ConfigOpts
from eyed3.utils.prompt import PromptExit
from .config import DEFAULT_CONFIG, CONFIG_ENV_VAR, Config, MAIN_SECT, SA_KEY
from . import log
from .core import Command, CommandError
from .commands import *
_FORK_METHOD_SET = False

def _pErr(msg):
    print(ansi.Fg.red(str(msg) + ':'))
    tb = sys.exc_info()
    traceback.print_exception(tb[0], tb[1], tb[2])


def main(args):
    global _FORK_METHOD_SET
    import multiprocessing
    if not _FORK_METHOD_SET:
        try:
            multiprocessing.set_start_method('fork')
            _FORK_METHOD_SET = True
        except RuntimeError as ex:
            try:
                log.warning('multiprocessing.set_start_method: ' + str(ex))
            finally:
                ex = None
                del ex

        else:
            if not (hasattr(args, 'command_func') and args.command_func):
                args.app.arg_parser.print_help()
                return 1
            args.applyLoggingOpts(args.log_levels, args.log_files)
            if args.db_url:
                args.config.set(MAIN_SECT, SA_KEY, args.db_url)
                args.db_url = None
    else:
        if 'MISHMASH_DBURL' in os.environ:
            log.verbose('Using environment MISHMASH_DBURL over configuration: {}'.format(os.environ['MISHMASH_DBURL']))
            args.config.set(MAIN_SECT, SA_KEY, os.environ['MISHMASH_DBURL'])
        else:
            try:
                retval = args.command_func(args) or 0
            except (KeyboardInterrupt, PromptExit):
                retval = 0
            except (sql_exceptions.ArgumentError,):
                _pErr('Database error')
                retval = 1
            except (sql_exceptions.OperationalError,) as db_err:
                try:
                    print((str(db_err)), file=(sys.stderr))
                    retval = 1
                finally:
                    db_err = None
                    del db_err

            except CommandError as cmd_err:
                try:
                    print((str(cmd_err)), file=(sys.stderr))
                    retval = cmd_err.exit_status
                finally:
                    cmd_err = None
                    del cmd_err

            except Exception as ex:
                try:
                    log.exception(ex)
                    _pErr('General error')
                    retval = 2
                finally:
                    ex = None
                    del ex

        return retval


class MishMash(Application):

    def __init__(self, progname='mishmash', ConfigClass=None, config_obj=None):
        from . import version
        if ConfigClass:
            if config_obj:
                raise ValueError('ConfigClass and config_obj are not compatible together.')
        config_opts = ConfigOpts(required=False, default_config=DEFAULT_CONFIG,
          default_config_opt='--default-config',
          ConfigClass=(ConfigClass or Config),
          config_env_var=CONFIG_ENV_VAR,
          init_logging_fileConfig=True)
        super().__init__(main, name=progname, version=version, config_opts=config_opts,
          pdb_opt=False,
          gettext_domain='MishMash')
        ansi.init()
        desc = 'Database command line options (or config) are required by most sub commands.'
        subs = self.arg_parser.add_subparsers(title='Commands', dest='command', description=desc,
          required=False)
        Command.loadCommandMap(subparsers=subs)
        self.arg_subparsers = subs
        self._user_config = config_obj

    def _main(self, args):
        if self._user_config:
            args.config = self._user_config
        return super()._main(args)

    def _addArguments(self, parser):
        group = parser.add_argument_group(title='Settings and options')
        group.add_argument('-D', '--database', dest='db_url', metavar='url', default=None, help='Database URL. This will override the URL from the config file be it the default of one passed with -c/--config.')


app = MishMash()
if __name__ == '__main__':
    app.run()