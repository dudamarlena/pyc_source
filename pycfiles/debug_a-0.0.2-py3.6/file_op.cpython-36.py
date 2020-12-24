# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\debug_a\tools\file_op.py
# Compiled at: 2018-06-02 23:42:01
# Size of source mod 2**32: 1145 bytes
"""
file operation
==========================================================================
"""
import os

def ensure_file_exist(file):
    if not os.path.exists(file):
        create_file(file)


def create_file(file, content=None, mode='a', encoding='utf-8'):
    with open(file, mode, encoding=encoding) as (f):
        if isinstance(content, str):
            content += '\n'
            f.write(content)
        else:
            if isinstance(content, list):
                content = [i.strip('\n') + '\n' for i in content]
                f.writelines(content)
            else:
                if content is None:
                    return
                raise ValueError('If content is not None, it must be list or str!')


def write_file(file, content, mode='a', encoding='utf-8'):
    create_file(file, content=content, mode=mode, encoding=encoding)


def read_file(file, encoding='utf-8'):
    with open(file, 'r', encoding=encoding) as (f):
        lines = f.readlines()
        lines = [line.strip('\n') for line in lines]
    if len(lines) > 0:
        return lines
    raise ValueError('file is empty!')