# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/logout.py
# Compiled at: 2014-05-30 02:26:32
__doc__ = '\nThis module is the logout command of bowl.\n\nCreated on 29 May 2014\n@author: Charlie Lewis\n'

class logout(object):
    """
    This class is responsible for the logout command of the cli.
    """

    @classmethod
    def main(self, args):
        print args