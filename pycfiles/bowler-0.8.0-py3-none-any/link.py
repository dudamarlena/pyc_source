# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/link.py
# Compiled at: 2014-09-21 04:14:07
__doc__ = '\nThis module is the link command of bowl.\n\nCreated on 14 July 2014\n@author: Charlie Lewis\n'
import ast, os

class link(object):
    """
    This class is responsible for the link command of the cli.
    """

    @classmethod
    def main(self, args):
        directory = args.metadata_path
        directory = os.path.expanduser(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = os.path.join(os.path.expanduser(args.path), 'services')
        exists = False
        try:
            if os.path.exists(os.path.join(directory, 'repositories')):
                with open(os.path.join(directory, 'repositories'), 'r') as (f):
                    for line in f:
                        repo = ast.literal_eval(line.strip())
                        if repo['title'] == args.SERVICE_HOST and repo['path'] == path:
                            exists = True

            if not exists:
                with open(os.path.join(directory, 'repositories'), 'a') as (f):
                    f.write("{'title': '" + args.SERVICE_HOST + "'," + " 'type': 'choice_menu'," + " 'name': '" + args.NAME + "'," + " 'path': '" + path + "'" + '}\n')
            elif not args.z:
                print 'repository has already been linked'
        except:
            if not args.z:
                print 'unable to link service host'
            return False

        return True