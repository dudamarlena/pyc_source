# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/logout.py
# Compiled at: 2014-05-30 02:26:32
"""
This module is the logout command of bowl.

Created on 29 May 2014
@author: Charlie Lewis
"""

class logout(object):
    """
    This class is responsible for the logout command of the cli.
    """

    @classmethod
    def main(self, args):
        print args