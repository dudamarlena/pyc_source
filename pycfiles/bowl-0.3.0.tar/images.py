# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/images.py
# Compiled at: 2014-09-10 23:51:25
"""
This module is the images command of bowl.

Created on 22 June 2014
@author: Charlie Lewis
"""
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