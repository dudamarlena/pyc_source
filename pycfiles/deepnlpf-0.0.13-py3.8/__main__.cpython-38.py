# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/__main__.py
# Compiled at: 2020-04-28 08:21:17
# Size of source mod 2**32: 2771 bytes
import argparse, re, json
from os import path
from codecs import open
import deepnlpf._version as v
HERE = path.abspath(path.dirname(__file__))

def install(args):
    if args:
        from deepnlpf.core.plugin_manager import PluginManager
        PluginManager().install(args)
    else:
        print('Wrong command!')
        print('Try the command: deepnlpf --install <name_plugin>')


def uninstall(args):
    if args:
        from deepnlpf.core.plugin_manager import PluginManager
        PluginManager().uninstall(args)
    else:
        print('Wrong command!')
        print('Try the command: deepnlpf --uninstall <name_plugin>')


def listplugins(args):
    if args:
        from deepnlpf.core.plugin_manager import PluginManager
        PluginManager().listplugins(args)
    else:
        print('Wrong command!')
        print('Try the command: deepnlpf --listplugins all')


def api(args):
    if args:
        from deepnlpf.api import app
        if args == 'start':
            app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print('Wrong command!')
        print('Try the command: deepnlpf --api start')


def main():
    my_parser = argparse.ArgumentParser(prog='deepnlpf',
      description='DeepNLPF Command Line Interface - CLI',
      epilog='🐙 Enjoy the program! :)')
    my_parser.version = '🐙 DeepNLPF V-' + v.__version__
    my_parser.add_argument('-v', '--version', help='show version.',
      action='version')
    my_parser.add_argument('-install', '--install', help='Command for install plugin.',
      type=install,
      action='store')
    my_parser.add_argument('-uninstall', '--uninstall', help='Command for uninstall plugin.',
      type=install,
      action='store')
    my_parser.add_argument('-listplugins', '--listplugins', help='Command for listplugins plugin.',
      type=listplugins,
      action='store')
    my_parser.add_argument('-api', '--api', help='Command run api.',
      type=api,
      action='store')
    args = my_parser.parse_args()


if __name__ == '__main__':
    main()