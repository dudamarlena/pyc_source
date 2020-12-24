# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/TestCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
import os
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import banner
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand

class TestCommand(PluginCommand, CloudPluginCommand):
    topics = {'test': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command test')

    @command
    def do_test(self, args, arguments):
        """
        ::

          Usage:
             test list
             test [TEST] [NUMBER] [--test=TESTER]

          This is an internal command and is ment for developers. If executed, in the source directory,
          it will execute the specified series of tests in the tests directory.
          managing the admins test test test test

          Arguments:
            TEST     the name of the test directory
            NUMBER   the number of a specific test

          Options:
            --test=TESTER   nosetests or py.test. [default: nosetests -v --nocapture]

          Examples:
              cm test var
                  finds the first test that contains var and than executes all tests in it

              cm test var 4
                  finds the first test that contains var and than executes the test with number 004

        """
        data = dotdict({'test': arguments['TEST'], 
           'number': arguments['NUMBER'], 
           'tester': arguments['--test']})

        def get_file():
            data.file = None
            for file in files:
                if data.test in file:
                    break

            data.file = file
            return

        def run(command):
            command = command.format(**data)
            banner(command, c='-')
            parameter = command.split(' ')
            os.system(command)

        files = []
        dirs = []
        for root, dirnames, filenames in os.walk('tests'):
            for filename in filenames:
                if '.pyc' in filename:
                    continue
                if '.py' not in filename:
                    dirs.append(os.path.join(root, filename))
                elif filename not in ('__init__.py', ):
                    files.append(os.path.join(root, filename))

        if arguments['list']:
            print(('\n').join(files))
            return ''
        else:
            if data.test is None:
                command = '{tester}'
            elif data.test in dirs:
                command = '{tester} {test}'
            elif data.number is None:
                get_file()
                command = '{tester} {file}'
            else:
                get_file()
                data.basename = os.path.basename(data.file).replace('.py', '')
                data.basename = data.basename.replace('test_', '')
                data.number = data.number.zfill(3)
                command = '{tester} {file}:Test_{basename}.test_{number}'
            run(command)
            return ''