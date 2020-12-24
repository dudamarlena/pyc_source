# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/image_import.py
# Compiled at: 2014-09-10 23:49:44
"""
This module is the import command of bowl.

Created on 6 June 2014
@author: Charlie Lewis
"""
import os

class image_import(object):
    """
    This class is responsible for the import command of the cli.
    """

    @classmethod
    def main(self, args):
        directory = args.metadata_path
        directory = os.path.expanduser(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if args.uuid is None:
            args.uuid = ''
        if args.description is None:
            args.description = ''
        try:
            with open(os.path.join(directory, 'images'), 'a') as (f):
                f.write("{'title': '" + args.IMAGE_NAME + "'," + " 'command': '" + args.IMAGE_NAME + ',' + args.DOCKER_HOST + "'," + " 'host': '" + args.DOCKER_HOST + "'," + " 'uuid': '" + args.uuid + "'," + " 'description': '" + args.description + "'," + " 'type': 'image_choice_menu'" + '}\n')
        except:
            print 'unable to import image'
            return False

        return True