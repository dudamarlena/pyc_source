# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jace/Dropbox/projects/hasgeek/baseframe/baseframe/_version.py
# Compiled at: 2017-03-08 22:26:47
__all__ = [
 '__version__', '__version_info__']
__version__ = '0.3.1'
__version_info__ = tuple([ int(num) if num.isdigit() else num for num in __version__.replace('-', '.', 1).split('.') ])