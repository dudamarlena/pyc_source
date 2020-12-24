# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/connect.py
# Compiled at: 2014-08-03 14:19:30
__doc__ = '\nThis module is the connect command of bowl.\n\nCreated on 15 March 2014\n@author: Charlie Lewis\n'
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