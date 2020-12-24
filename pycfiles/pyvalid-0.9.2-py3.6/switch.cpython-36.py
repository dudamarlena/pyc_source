# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pyvalid/switch.py
# Compiled at: 2018-06-02 14:20:59
# Size of source mod 2**32: 272 bytes


def turn_on():
    globals()['pyvalid_enabled'] = True


def turn_off():
    globals()['pyvalid_enabled'] = False


def is_enabled():
    if 'pyvalid_enabled' in globals():
        enabled = globals()['pyvalid_enabled']
    else:
        enabled = True
    return enabled