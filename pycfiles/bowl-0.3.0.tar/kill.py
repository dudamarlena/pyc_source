# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/kill.py
# Compiled at: 2014-09-28 15:41:09
"""
This module is the kill command of bowl.

Created on 15 March 2014
@author: Charlie Lewis
"""
import ast, docker, os

class kill(object):
    """
    This class is responsible for the kill command of the cli.
    """

    @classmethod
    def main(self, args):
        try:
            directory = args.metadata_path
            directory = os.path.expanduser(directory)
            with open(os.path.join(directory, 'containers'), 'r') as (f):
                for line in f:
                    container = ast.literal_eval(line.rstrip('\n'))
                    if container['container_id'] == args.CONTAINER:
                        c = docker.Client(base_url='tcp://' + container['host'] + ':2375', version='1.12', timeout=10)
                        c.kill(args.CONTAINER)
                        if not args.z:
                            print 'killed ' + container['container_id'] + ' on ' + container['host']

        except:
            if not args.z:
                print 'unable to kill ', args.CONTAINER
            return False

        return True