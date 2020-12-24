# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/arguments/general_functionalities.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 68 bytes


def argument_string(name):
    return f"--{name.replace('_', '-')}"