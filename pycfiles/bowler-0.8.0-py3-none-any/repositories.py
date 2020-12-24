# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/repositories.py
# Compiled at: 2014-09-20 15:49:32
__doc__ = '\nThis module is the repositories command of bowl.\n\nCreated on 19 July 2014\n@author: Charlie Lewis\n'
import ast, os

class repositories(object):
    """
    This class is responsible for the repositories command of the cli.
    """

    @classmethod
    def main(self, args):
        repositories = []
        try:
            directory = args.metadata_path
            directory = os.path.expanduser(directory)
            with open(os.path.join(directory, 'repositories'), 'r') as (f):
                for line in f:
                    repository = ast.literal_eval(line.rstrip('\n'))
                    repositories.append(repository['name'] + ', ' + repository['title'] + ', ' + repository['path'])

        except:
            pass

        if not args.z:
            for repository in repositories:
                print repository

        return repositories