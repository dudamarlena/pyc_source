# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/commander/commands/generate_config.py
# Compiled at: 2016-06-30 06:13:10
from __future__ import print_function
import os
from tingyun.logistics.exceptions import CommandlineParametersException

class Command(object):
    """
    """

    def __init__(self):
        """
        """
        self.name = 'generate-config'
        self.options = '[license_key] filename'
        self.description = 'Generate the config file with license(optional) with filename'

    def execute(self, args):
        """generate default configuration to specified path.
        :param args:
        :return:
        """
        if len(args) < 1:
            raise CommandlineParametersException()
        from tingyun import __file__ as package_root
        package_root = os.path.dirname(package_root)
        config_file = os.path.join(package_root, 'tingyun.ini')
        default_config = open(config_file, 'r')
        content = default_config.read()
        if 2 == len(args):
            output_file = open(args[1], 'w')
        else:
            output_file = open(args[0], 'w')
        if 2 == len(args):
            content = content.replace('** YOUR-LICENSE-KEY **', args[0])
            print('\n                        ================ Messages ==============\n                  You use license key: %s, to generate config file: %s\n                  ' % (args[0], args[1]))
        elif 1 == len(args):
            print('\n                        ================ Messages ==============\n                  You use license key: , to generate config file: %s.\n                  Before you use the python agent, you should type the license key into config file\n                  ' % args[0])
        output_file.write(content)
        output_file.close()
        default_config.close()