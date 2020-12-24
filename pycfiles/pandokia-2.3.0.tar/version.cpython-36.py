# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/version.py
# Compiled at: 2018-06-11 11:14:16
# Size of source mod 2**32: 795 bytes
__all__ = [
 '__version__',
 '__version_short__',
 '__version_long__',
 '__version_post__',
 '__version_commit__',
 '__version_date__',
 '__version_dirty__',
 '__build_date__',
 '__build_time__',
 '__build_status__']
__version__ = '2.1.2.dev4+g21a2ac8a'
__version_short__ = '2.1.2'
__version_long__ = '2.1.2-4-g21a2ac8a'
__version_post__ = '4'
__version_commit__ = '21a2ac8a'
__version_date__ = '2018-06-08 16:24:03 -0400'
__version_dirty__ = False
__build_date__ = '2018-06-11'
__build_time__ = '11:14:16.825712'
__build_status__ = 'release' if (not int(__version_post__) > 0 and not __version_dirty__) else 'development'