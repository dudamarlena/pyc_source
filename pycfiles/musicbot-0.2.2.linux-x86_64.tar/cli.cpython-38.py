# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/cli.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 2897 bytes
import sys, os, logging, click, requests, spotipy, click_completion, click_completion.core
from click.formatting import HelpFormatter
from attrdict import AttrDict
from musicbot import lib, helpers, config, exceptions
from musicbot import __version__
HelpFormatter.write_dl.__defaults__ = (50, 2)
bin_folder = os.path.dirname(__file__)
commands_folder = 'commands'
plugin_folder = os.path.join(bin_folder, commands_folder)
CONTEXT_SETTINGS = {'max_content_width':140,  'terminal_width':140,  'auto_envvar_prefix':'MB',  'help_option_names':['-h', '--help']}
logger = logging.getLogger('musicbot')

def custom_startswith(string, incomplete):
    """A custom completion matching that supports case insensitive matching"""
    if os.environ.get('_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE'):
        string = string.lower()
        incomplete = incomplete.lower()
    return string.startswith(incomplete)


click_completion.core.startswith = custom_startswith
click_completion.init()
prog_name = 'musicbot'

class SubCommandLineInterface(helpers.GroupWithHelp):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and '__init__' not in filename:
                rv.append(filename[:-3])
            all_commands = rv + super().list_commands(ctx)
            all_commands.sort()
            return all_commands

    def get_command(self, ctx, cmd_name):
        ns = {}
        fn = os.path.join(plugin_folder, cmd_name + '.py')
        try:
            with open(fn) as (f):
                code = compile(f.read(), fn, 'exec')
                ns['__name__'] = f"{commands_folder}.{cmd_name}"
                ns['__file__'] = fn
                eval(code, ns, ns)
        except FileNotFoundError:
            return super().get_command(ctx, cmd_name)
        else:
            return ns['cli']


@click.group(cls=SubCommandLineInterface, context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(__version__, '--version', '-V', prog_name=prog_name)
@helpers.add_options(config.options)
@click.pass_context
def cli(ctx, **kwargs):
    """Music swiss knife, new gen."""
    ctx.obj = AttrDict
    ctx.obj.folder = bin_folder
    (config.config.set)(**kwargs)
    ctx.obj.config = config.config


@cli.command(short_help='Print version')
def version():
    """Print version

       Equivalent : -V
    """
    print(f"{prog_name}, version {__version__}")


def main(**kwargs):
    try:
        return (cli.main)(prog_name=prog_name, **kwargs)
    except (exceptions.MusicbotError, spotipy.client.SpotifyException, requests.exceptions.ConnectionError) as e:
        try:
            logger.error(e)
            sys.exit(1)
        finally:
            e = None
            del e


if __name__ == '__main__':
    lib.raise_limits()
    main()