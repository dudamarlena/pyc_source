# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/unlink.py
# Compiled at: 2014-09-21 01:44:43
"""
This module is the unlink command of bowl.

Created on 14 July 2014
@author: Charlie Lewis
"""
import ast, fileinput, os

class unlink(object):
    """
    This class is responsible for the unlink command of the cli.
    """

    @classmethod
    def main(self, args):
        try:
            directory = args.metadata_path
            directory = os.path.expanduser(directory)
            for line in fileinput.input(os.path.join(directory, 'repositories'), inplace=True):
                host = ast.literal_eval(line.rstrip('\n'))
                if args.NAME != host['name'] and directory != host['path']:
                    print '%s' % line,

        except:
            return False

        return True