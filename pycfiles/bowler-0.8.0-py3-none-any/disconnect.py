# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/disconnect.py
# Compiled at: 2014-07-27 23:46:01
__doc__ = '\nThis module is the disconnect command of bowl.\n\nCreated on 15 March 2014\n@author: Charlie Lewis\n'
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