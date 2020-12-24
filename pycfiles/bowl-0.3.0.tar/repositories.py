# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/repositories.py
# Compiled at: 2014-09-20 15:49:32
"""
This module is the repositories command of bowl.

Created on 19 July 2014
@author: Charlie Lewis
"""
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