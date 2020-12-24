# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/login.py
# Compiled at: 2014-05-27 15:20:53
"""
This module is the login command of bowl.

Created on 14 March 2014
@author: Charlie Lewis
"""

class login(object):
    """
    This class is responsible for the login command of the cli.
    """

    @classmethod
    def main(self, args):
        print args