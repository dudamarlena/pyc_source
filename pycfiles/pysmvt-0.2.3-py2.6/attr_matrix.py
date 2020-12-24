# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvttestapp/tasks/attr_matrix.py
# Compiled at: 2010-05-30 09:35:01
from pysmvt.tasks import attributes

def action_1noattr():
    pass


@attributes('xattr')
def action_2xattr():
    pass


@attributes('+xattr')
def action_3pxattr():
    pass


@attributes('-xattr')
def action_4mxattr():
    pass


@attributes('yattr')
def action_5yattr():
    pass


@attributes('+yattr')
def action_6pyattr():
    pass


@attributes('-yattr')
def action_7myattr():
    pass