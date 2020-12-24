# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/image_import.py
# Compiled at: 2014-09-10 23:49:44
__doc__ = '\nThis module is the import command of bowl.\n\nCreated on 6 June 2014\n@author: Charlie Lewis\n'
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