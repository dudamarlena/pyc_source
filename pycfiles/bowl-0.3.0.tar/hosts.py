# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/hosts.py
# Compiled at: 2014-07-27 23:46:32
"""
This module is the hosts command of bowl.

Created on 14 March 2014
@author: Charlie Lewis
"""
import ast, os

class hosts(object):
    """
    This class is responsible for the hosts command of the cli.
    """

    @classmethod
    def main(self, args):
        hosts = []
        try:
            directory = args.metadata_path
            directory = os.path.expanduser(directory)
            with open(os.path.join(directory, 'hosts'), 'r') as (f):
                for line in f:
                    host = ast.literal_eval(line.rstrip('\n'))
                    hosts.append(host['title'])

        except:
            pass

        if not args.z:
            for host in hosts:
                print host

        return hosts