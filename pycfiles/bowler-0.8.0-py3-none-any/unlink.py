# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/unlink.py
# Compiled at: 2014-09-21 01:44:43
__doc__ = '\nThis module is the unlink command of bowl.\n\nCreated on 14 July 2014\n@author: Charlie Lewis\n'
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