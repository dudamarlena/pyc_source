# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/path_utils.py
# Compiled at: 2018-09-14 11:23:44
import os

def has_hidden_component(path):
    head, tail = os.path.split(path)
    if tail.startswith('.'):
        return True
    if not head or head == path:
        return False
    return has_hidden_component(head)


def ensure_directory(directory):
    if not os.path.exists(directory):
        print 'Creating directory ' + os.path.relpath(directory)
        os.makedirs(directory)