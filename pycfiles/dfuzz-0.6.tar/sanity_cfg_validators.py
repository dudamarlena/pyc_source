# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/envs/dfuzz/project/dfuzz/dfuzz/tests/dummy/sanity_cfg_validators.py
# Compiled at: 2011-04-28 10:56:20


class empty(object):
    pass


class invalid(object):
    binary = ''
    args = ''


class valid(object):
    binary = 'bin'
    args = 'args'