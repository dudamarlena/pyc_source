# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/source/lyrics/lyrics/settings.py
# Compiled at: 2013-01-30 10:28:49
"""Some settings for the lyrics library"""
use_database = True
import os
config_directory = os.path.join(os.getenv('HOME'), '.lyrics')
try:
    os.makedirs(config_directory)
except OSError:
    pass

database_path = os.path.join(config_directory, 'lyrics.db')
save_not_found_lyrics = True