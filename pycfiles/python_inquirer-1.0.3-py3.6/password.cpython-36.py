# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/prompts/password.py
# Compiled at: 2019-08-16 00:14:27
# Size of source mod 2**32: 282 bytes
"""
`password` type question
"""
from __future__ import print_function, unicode_literals
from . import input

def question(message, **kwargs):
    kwargs['is_password'] = True
    return (input.question)(message, **kwargs)