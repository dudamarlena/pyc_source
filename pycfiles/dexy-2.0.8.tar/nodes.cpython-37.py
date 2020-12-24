# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/nodes.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1173 bytes
from dexy.node import Node
from dexy.commands.utils import dummy_wrapper
import inspect

def nodes_command(alias=False):
    """
    Prints available node types and their settings.
    """
    if not alias:
        for alias in sorted(Node.plugins):
            print(alias)

        print('For info on a particular node type run `dexy nodes -alias doc`')
    else:
        print_node_info(alias)


def print_node_info(alias):
    print(alias)
    _, settings = Node.plugins[alias]
    instance = Node.create_instance(alias, 'dummy', dummy_wrapper())
    instance.update_settings(settings)
    print('')
    print(instance.setting('help'))
    print('')
    if len(instance._instance_settings) > 2:
        print('Settings:')
    for k in sorted(instance._instance_settings):
        if k in ('aliases', 'help'):
            continue
        tup = instance._instance_settings[k]
        print('    %s' % k)
        for line in inspect.cleandoc(tup[0]).splitlines():
            print('        %s' % line)

        print('        default value: %s' % tup[1])
        print('')