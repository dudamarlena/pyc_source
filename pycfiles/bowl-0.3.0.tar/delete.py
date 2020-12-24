# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/delete.py
# Compiled at: 2014-07-27 23:45:38
"""
This module is the delete command of bowl.

Created on 22 June 2014
@author: Charlie Lewis
"""
import ast, fileinput, os

class delete(object):
    """
    This class is responsible for the delete command of the cli.
    """

    @classmethod
    def main(self, args):
        try:
            directory = args.metadata_path
            directory = os.path.expanduser(directory)
            for line in fileinput.input(os.path.join(directory, 'images'), inplace=True):
                image = ast.literal_eval(line.rstrip('\n'))
                if args.IMAGE_NAME != image['title']:
                    print '%s' % line,

        except:
            print 'unable to delete image'
            return False

        return True