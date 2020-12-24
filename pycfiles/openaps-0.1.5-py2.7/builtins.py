# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/builtins.py
# Compiled at: 2016-03-06 16:21:44
import init, alias, shlex, cli
from subprocess import call

class BuiltinApp(cli.ConfigApp):
    name = 'builtin'


builtins = {'init': init.init}

def get_builtins():
    app = BuiltinApp([])
    app.read_config()
    out = alias.get_alias_map(app.config)
    out.update(**builtins)
    return out


class RunnableAlias(object):

    def __init__(self, spec, parent):
        self.spec = spec
        self.parent = parent

    def __call__(self, args):
        if self.spec is None:
            return
        else:
            spec_command = shlex.split(self.spec.fields.get('command'))
            cmd = [
             'openaps-%s' % spec_command[0]] + spec_command[1:]
            if spec_command[0].startswith('!'):
                prog = shlex.split(spec_command[0][1:])
                cmd = prog + spec_command[1:]
            exit(call(cmd + args.args))
            return


def get_alias(command, app):
    spec = alias.get_alias_map(app.config).get(command, None)
    runnable = RunnableAlias(spec, app)
    return runnable


def dispatch(args, back):
    app = None
    command = builtins.get(args.command, None)
    if command:
        command(args)
    else:
        app = BuiltinApp(args)
        app.read_config()
        get_alias(args.command, app)(args)
    return


def is_builtin(command):
    if command in builtins:
        return True
    app = BuiltinApp([])
    app.read_config()
    if command in alias.get_alias_map(app.config):
        return True
    return False