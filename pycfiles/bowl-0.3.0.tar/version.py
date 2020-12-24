# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/version.py
# Compiled at: 2014-08-18 19:26:14
"""
This module is the version command of bowl.

Created on 14 March 2014
@author: Charlie Lewis
"""
import pkg_resources

class version(object):
    """
    This class is responsible for the version command of the cli.
    """

    @classmethod
    def main(self, args):
        if not args.z:
            print pkg_resources.get_distribution('bowl').version
        return pkg_resources.get_distribution('bowl').version