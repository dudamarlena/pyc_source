# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/common.py
# Compiled at: 2019-07-19 11:14:44
# Size of source mod 2**32: 377 bytes
import os

def is_valid_path(parser, p_file):
    p_file = os.path.abspath(p_file)
    if not os.path.exists(p_file):
        parser.error('The path %s does not exist!' % p_file)
    else:
        return p_file


def is_valid_file(parser, n_file):
    if not os.path.isfile(n_file):
        parser.error('The file %s does not exist!' % n_file)
    else:
        return n_file