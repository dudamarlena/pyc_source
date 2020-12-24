# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/images.py
# Compiled at: 2014-09-10 23:51:25
__doc__ = '\nThis module is the images command of bowl.\n\nCreated on 22 June 2014\n@author: Charlie Lewis\n'
import ast, os

class images(object):
    """
    This class is responsible for the images command of the cli.
    """

    @classmethod
    def main(self, args):
        images = []
        try:
            directory = args.metadata_path
            directory = os.path.expanduser(directory)
            with open(os.path.join(directory, 'images'), 'r') as (f):
                for line in f:
                    image = ast.literal_eval(line.rstrip('\n'))
                    images.append(image['title'] + ' | ' + image['host'])

        except:
            pass

        if not args.z:
            for image in images:
                print image

        return images