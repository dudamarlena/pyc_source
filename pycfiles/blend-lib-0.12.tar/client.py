# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: blend/galaxy/libraries/client.py
# Compiled at: 2012-06-05 03:02:57
"""
Contains possible interactions with the Galaxy Data Libraries
"""

class LibraryClient(object):

    def __init__(self, galaxy_instance):
        self.gi = galaxy_instance