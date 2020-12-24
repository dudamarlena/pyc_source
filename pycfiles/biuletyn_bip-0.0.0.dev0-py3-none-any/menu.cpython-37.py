# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/utils/menu.py
# Compiled at: 2019-09-27 14:05:29
# Size of source mod 2**32: 202 bytes
import collections
VisibilityOptions = collections.namedtuple('VisibilityOptions', ['authenticated', 'anonymous'])
MenuItem = collections.namedtuple('MenuItem', ['title', 'url', 'hide'])