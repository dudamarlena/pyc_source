# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/nielsen/__init__.py
# Compiled at: 2020-05-04 01:00:37
# Size of source mod 2**32: 369 bytes
"""
chown, chmod, rename, and organize TV show files.
"""
from nielsen.api import filter_series, get_file_info, organize_file, process_file, sanitize_filename
from nielsen.config import CONFIG, load_config, update_series_ids
__all__ = [
 'api', 'config', 'files', 'tv']