# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/sheldon/cli.py
# Compiled at: 2015-11-20 23:29:37
# Size of source mod 2**32: 881 bytes
import os

def new():
    project_name = ''
    while not project_name:
        project_name = input('Enter name for project: ')

    os.makedirs(project_name + '/adapters')
    os.mkdir(project_name + '/plugins')
    start_file = open(project_name + '/start.py', 'w')
    start_file.write("\nimport argparse\nfrom sheldon import Sheldon\n\nparser = argparse.ArgumentParser(description='Start bot')\nparser.add_argument('--config-prefix', type=str, default='SHELDON_',\n                    help='a str from which starting all config variables')\nparser.add_argument('--adapter', type=str, default='console',\n                    help='a str with name of adapter from adapters folder'\n                         'or PyPi')\nargs = parser.parse_args()\n\nbot = Sheldon({'config-prefix': args.config_prefix,\n               'adapter': args.adapter})\n\nbot.start()\n    ")
    start_file.close()