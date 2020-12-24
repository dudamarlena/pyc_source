# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/hosts.py
# Compiled at: 2014-07-27 23:46:32
__doc__ = '\nThis module is the hosts command of bowl.\n\nCreated on 14 March 2014\n@author: Charlie Lewis\n'
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