# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/delete.py
# Compiled at: 2014-07-27 23:45:38
__doc__ = '\nThis module is the delete command of bowl.\n\nCreated on 22 June 2014\n@author: Charlie Lewis\n'
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