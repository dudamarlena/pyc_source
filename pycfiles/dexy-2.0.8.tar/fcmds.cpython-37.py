# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/fcmds.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 2158 bytes
import dexy.filter, inspect

def fcmds_command(alias=False):
    """
    Prints a list of available filter commands.
    """
    if alias:
        filter_instances = [
         dexy.filter.Filter.create_instance(alias)]
    else:
        filter_instances = dexy.filter.Filter
    for filter_instance in filter_instances:
        cmds = filter_instance.filter_commands()
        if cmds:
            print('filter alias:', filter_instance.alias)
            for command_name in sorted(cmds):
                docs = inspect.getdoc(cmds[command_name])
                if docs:
                    doc = docs.splitlines()[0]
                    print('    %s   # %s' % (command_name, doc))
                else:
                    print('    %s' % command_name)

            print('')


def fcmd_command(alias=None, cmd=None, **kwargs):
    """
    Run a filter command.
    """
    filter_instance = dexy.filter.Filter.create_instance(alias)
    cmd_name = 'docmd_%s' % cmd
    if cmd_name not in dir(filter_instance):
        msg = '%s is not a valid command. There is no method %s defined in %s'
        msgargs = (cmd, cmd_name, filter_instance.__class__.__name__)
        raise dexy.exceptions.UserFeedback(msg % msgargs)
    else:
        instance_method = getattr(filter_instance, cmd_name)
        if inspect.ismethod(instance_method):
            try:
                (instance_method.__func__)(filter_instance, **kwargs)
            except TypeError as e:
                try:
                    print(e.message)
                    print(inspect.getargspec(instance_method.__func__))
                    print(inspect.getdoc(instance_method.__func__))
                    raise
                finally:
                    e = None
                    del e

        else:
            msg = 'expected %s to be an instance method of %s'
            msgargs = (cmd_name, filter_instance.__class__.__name__)
            raise dexy.exceptions.InternalDexyProblem(msg % msgargs)