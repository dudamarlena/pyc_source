# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/whotracksme/website/utils.py
# Compiled at: 2018-05-17 05:30:15
# Size of source mod 2**32: 149 bytes


def print_progress(text, default_space=40):
    print('{} {:{}} done'.format(text, '.' * (default_space - len(text)), default_space - len(text)))