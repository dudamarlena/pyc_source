# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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