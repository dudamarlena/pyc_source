# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus_search_cli/parsing/click_wrappers.py
# Compiled at: 2019-11-12 16:24:32
"""
Mostly copied from globus-cli

We want the niceties of parsing improvements worked out in that project.
In the future, if we integrate this CLI, it should lead to a smoother
transition.
"""
import logging.config, warnings, click
from globus_sdk import GlobusAPIError
from globus_search_cli.version import __version__

class HiddenOption(click.Option):
    """
    HiddenOption -- absent from Help text.

    Supported in latest and greatest version of Click, but not old versions, so
    use generic 'cls=HiddenOption' to get the desired behavior.
    """

    def get_help_record(self, ctx):
        """
        Has "None" as its help record. All that's needed.
        """
        pass


class CommandState(object):

    def __init__(self):
        self.debug = False


def setup_logging(level='DEBUG'):
    conf = {'version': 1, 
       'formatters': {'basic': {'format': '[%(levelname)s] %(name)s::%(funcName)s() %(message)s'}}, 'handlers': {'console': {'class': 'logging.StreamHandler', 
                                'level': level, 
                                'formatter': 'basic'}}, 
       'loggers': {'globus_sdk': {'level': level, 'handlers': ['console']}, 'globus_search_cli': {'level': level, 'handlers': ['console']}}}
    logging.config.dictConfig(conf)


def debug_option(f):

    def callback(ctx, param, value):
        if not value or ctx.resilient_parsing:
            warnings.simplefilter('ignore')
            return
        warnings.simplefilter('default')
        state = ctx.ensure_object(CommandState)
        state.debug = True
        setup_logging(level='DEBUG')

    return click.option('--debug', is_flag=True, cls=HiddenOption, expose_value=False, callback=callback, is_eager=True)(f)


def index_argument(f):
    f = click.argument('INDEX_ID')(f)
    return f


def common_options(f):
    """
    Global/shared options decorator.
    """
    f = click.help_option('-h', '--help')(f)
    f = click.version_option(__version__, '-v', '--version')(f)
    f = debug_option(f)
    return f


class GlobusCommandGroup(click.Group):
    """
    This is a click.Group with any customizations which we deem necessary
    *everywhere*.

    In particular, at present it provides a better form of handling for
    no_args_is_help. If that flag is set, helptext will be triggered not only
    off of cases where there are no arguments at all, but also cases where
    there are options, but no subcommand (positional arg) is given.
    """

    def invoke(self, ctx):
        if self.no_args_is_help and not ctx.protected_args:
            click.echo(ctx.get_help())
            ctx.exit()
        try:
            return super(GlobusCommandGroup, self).invoke(ctx)
        except GlobusAPIError as err:
            click.echo(err._underlying_response.text, err=True)
            click.get_current_context().exit(1)


def globus_group(*args, **kwargs):
    """
    Wrapper over click.group which sets GlobusCommandGroup as the Class
    """

    def inner_decorator(f):
        f = click.group(cls=GlobusCommandGroup, *args, **kwargs)(f)
        f = common_options(f)
        return f

    return inner_decorator


def globus_cmd(*args, **kwargs):
    """
    Wrapper over click.command which sets common opts
    """

    def inner_decorator(f):
        f = click.command(*args, **kwargs)(f)
        f = common_options(f)
        return f

    return inner_decorator