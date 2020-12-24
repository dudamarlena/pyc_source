# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/library.py
# Compiled at: 2016-03-01 16:55:54
"""
A module to manage a collection of git book repos
"""
import os
from . import config

class GitbergLibraryManager(object):
    """ A god object for managing a collection of Gitberg style books
    """

    def __init__(self, config=None):
        """ optionally takes an intialized and parsed ConfigFile instance
        """
        if not config.data:
            config.ConfigFile()

    def library_base_path(self):
        """ returns the path where library books are stored
        """
        return config.data['library_path']


def main():
    config.ConfigFile()
    library_dir = config.data['library_path']
    for folder in os.listdir(library_dir):
        print folder