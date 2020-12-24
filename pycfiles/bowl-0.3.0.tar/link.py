# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/link.py
# Compiled at: 2014-09-21 04:14:07
"""
This module is the link command of bowl.

Created on 14 July 2014
@author: Charlie Lewis
"""
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