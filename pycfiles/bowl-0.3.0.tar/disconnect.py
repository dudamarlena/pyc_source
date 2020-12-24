# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/disconnect.py
# Compiled at: 2014-07-27 23:46:01
"""
This module is the disconnect command of bowl.

Created on 15 March 2014
@author: Charlie Lewis
"""
import ast, fileinput, os

class disconnect(object):
    """
    This class is responsible for the disconnect command of the cli.
    """

    @classmethod
    def main(self, args):
        try:
            directory = args.metadata_path
            directory = os.path.expanduser(directory)
            for line in fileinput.input(os.path.join(directory, 'hosts'), inplace=True):
                host = ast.literal_eval(line.rstrip('\n'))
                if args.DOCKER_HOST != host['title']:
                    print '%s' % line,

        except:
            print 'unable to remove docker host'
            return False

        return True