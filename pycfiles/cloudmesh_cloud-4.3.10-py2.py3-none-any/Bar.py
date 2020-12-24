# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/Bar.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command

class BarCommand(object):
    topics = {'bar': 'example'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init Bar')

    @command
    def do_bar(self, args, arguments):
        """
        ::

          Usage:
                bar -f FILE
                bar FILE
                bar list

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        print(arguments)