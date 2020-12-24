# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/types/int_name.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 347 bytes
from ...util import int_names
USAGE = "\nAn int_name is either an integer, a string representing an integer, or a\nfanciful name that's either a day of week, a month, a planet, or a chemical\nelement.\n"

def make(c):
    try:
        return int_names.to_index(c)
    except:
        raise ValueError('Don\'t understand "%s"\n%s' % (c, USAGE))