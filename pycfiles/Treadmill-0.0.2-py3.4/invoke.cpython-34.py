# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/cli/admin/invoke.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 5112 bytes
"""Implementation of treadmill-admin CLI plugin."""
import pwd, importlib, os, decorator, click, jsonschema, yaml
from treadmill import authz
from treadmill import cli
from treadmill import context

class Context(object):
    __doc__ = 'CLI context.'

    def __init__(self):
        self.authorizer = authz.NullAuthorizer()

    def authorize(self, resource, action, args, kwargs):
        """Invoke internal authorizer."""
        self.authorizer.authorize(resource, action, args, kwargs)


def list_resource_types(api):
    """List available resource types."""
    apimod = importlib.import_module(api)
    resources = []
    for path in apimod.__path__:
        for filename in os.listdir(path):
            if filename == '__init__.py':
                continue
            if filename.endswith('.py'):
                resources.append(filename[:-3])
                continue

    resources.sort()
    return resources


def _import_resource_mod(resource_type, debug=False):
    """Safely import module for given resource type."""
    if resource_type.startswith('_'):
        return
    try:
        return importlib.import_module('treadmill.api.' + resource_type)
    except ImportError:
        if not debug:
            raise click.BadParameter(resource_type)
        else:
            raise


def make_command(parent, name, func):
    """Make a command using reflection on the function."""
    argspec = decorator.getargspec(func)
    args = list(argspec.args)
    defaults = argspec.defaults
    if defaults is None:
        defaults = []
    else:
        defaults = list(defaults)

    @parent.command(name=name, help=func.__doc__)
    def command(*args, **kwargs):
        """Constructs a command handler."""
        try:
            if 'rsrc' in kwargs:
                kwargs['rsrc'] = yaml.load(kwargs['rsrc'].read())
            formatter = cli.make_formatter(None)
            cli.out(formatter(func(*args, **kwargs)))
        except jsonschema.exceptions.ValidationError as input_err:
            click.echo(input_err, err=True)
        except jsonschema.exceptions.RefResolutionError as res_error:
            click.echo(res_error, err=True)
        except authz.AuthorizationError as auth_err:
            click.echo('Not authorized.', err=True)
            click.echo(auth_err, err=True)
        except TypeError as type_err:
            click.echo(type_err, err=True)

    while defaults:
        arg = args.pop()
        defarg = defaults.pop()
        if defarg is not None:
            argtype = type(defarg)
        else:
            argtype = str
        if defarg == ():
            argtype = cli.LIST
            defarg = None
        click.option('--' + arg, default=defarg, type=argtype)(command)

    if not args:
        return
    arg = args.pop(0)
    click.argument(arg)(command)
    while args:
        if len(args) == 1:
            arg = args.pop(0)
            click.argument(arg, type=click.File('rb'))(command)
        else:
            arg = args.pop(0)
            click.argument(arg)(command)

    if args:
        raise click.UsageError('Non-standard API: %s, %r' % (name, argspec))


def make_resource_group(ctx, parent, resource_type, api=None):
    """Make click group for a resource type."""
    if api is None:
        mod = _import_resource_mod(resource_type)
        if not mod:
            return
        api = getattr(mod, 'init')(ctx)

    @parent.group(name=resource_type, help=api.__doc__)
    def _rsrc_group():
        """Creates a CLI group for the given resource type."""
        pass

    for verb in dir(api):
        if verb.startswith('__'):
            continue
        func = getattr(api, verb)
        if hasattr(func, '__call__'):
            make_command(_rsrc_group, verb, func)
        elif hasattr(func, '__init__'):
            make_resource_group(ctx, _rsrc_group, verb, func)
            continue


def init():
    """Constructs parent level CLI group."""
    ctx = Context()

    @click.group()
    @click.option('--auth/--no-auth', is_flag=True, default=True)
    @click.option('--cell', required=True, envvar='TREADMILL_CELL', callback=cli.handle_context_opt, expose_value=False)
    def invoke(auth):
        """Directly invoke Treadmill API without REST."""
        if auth:
            user_clbk = lambda : pwd.getpwuid(os.getuid()).pw_name
            ctx.authorizer = authz.PluginAuthorizer(user_clbk)
        if cli.OUTPUT_FORMAT == 'pretty':
            raise click.BadParameter('must use --outfmt [json|yaml]')

    for resource in list_resource_types('treadmill.api'):
        try:
            make_resource_group(ctx, invoke, resource)
        except context.ContextError:
            pass

    return invoke