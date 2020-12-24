# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/connect.py
# Compiled at: 2014-08-03 14:19:30
"""
This module is the connect command of bowl.

Created on 15 March 2014
@author: Charlie Lewis
"""
import ast, os

class connect(object):
    """
    This class is responsible for the connect command of the cli.
    """

    @classmethod
    def main(self, args):
        directory = args.metadata_path
        directory = os.path.expanduser(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        exists = False
        try:
            if os.path.exists(os.path.join(directory, 'hosts')):
                with open(os.path.join(directory, 'hosts'), 'r') as (f):
                    for line in f:
                        repo = ast.literal_eval(line.strip())
                        if repo['title'] == args.DOCKER_HOST:
                            exists = True

            if not exists:
                with open(os.path.join(directory, 'hosts'), 'a') as (f):
                    f.write("{'title': '" + args.DOCKER_HOST + "'," + " 'type': 'choice_menu'" + '}\n')
            else:
                print 'host has already been connected'
        except:
            print 'unable to add docker host'
            return False

        return True