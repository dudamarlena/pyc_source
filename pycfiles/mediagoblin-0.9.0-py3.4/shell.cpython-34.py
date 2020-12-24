# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/gmg_commands/shell.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2774 bytes
import code
from mediagoblin import mg_globals
from mediagoblin.gmg_commands import util as commands_util
from mediagoblin.tools.transition import DISABLE_GLOBALS

def shell_parser_setup(subparser):
    subparser.add_argument('--ipython', help='Use ipython', action='store_true')


if DISABLE_GLOBALS:
    SHELL_BANNER = 'GNU MediaGoblin shell!\n----------------------\nAvailable vars:\n - app: instantiated mediagoblin application\n - db: database session\n - ctx: context object\n'
else:
    SHELL_BANNER = 'GNU MediaGoblin shell!\n----------------------\nAvailable vars:\n - app: instantiated mediagoblin application\n - mg_globals: mediagoblin.globals\n - db: database instance\n - ctx: context object\n'

def py_shell(**user_namespace):
    """
    Run a shell using normal python shell.
    """
    code.interact(banner=SHELL_BANNER, local=user_namespace)


def ipython_shell(**user_namespace):
    """
    Run a shell for the user using ipython. Return False if there is no IPython
    """
    try:
        from IPython import embed
    except:
        return False

    embed(banner1=SHELL_BANNER, user_ns=user_namespace)
    return True


def shell(args):
    """
    Setup a shell for the user either a normal Python shell or an IPython one
    """
    app = commands_util.setup_app(args)

    def run_shell(db, ctx):
        user_namespace = {'mg_globals': mg_globals, 
         'app': app, 
         'db': db, 
         'ctx': ctx}
        if args.ipython:
            ipython_shell(**user_namespace)
        elif not ipython_shell(**user_namespace):
            py_shell(**user_namespace)

    with app.gen_context() as (ctx):
        db = ctx.db
        run_shell(db, ctx)