# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/2to3_fixes/fix_unicode.py
# Compiled at: 2018-07-11 18:15:30
"""Fixer for __unicode__ methods.

Uses the django.utils.encoding.python_2_unicode_compatible decorator.
"""
from __future__ import unicode_literals
from lib2to3 import fixer_base
from lib2to3.fixer_util import find_indentation, Name, syms, touch_import
from lib2to3.pgen2 import token
from lib2to3.pytree import Leaf, Node

class FixUnicode(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = b"\n    classdef< 'class' any+ ':'\n              suite< any*\n                     funcdef< 'def' unifunc='__unicode__'\n                              parameters< '(' NAME ')' > any+ >\n                     any* > >\n    "

    def transform(self, node, results):
        unifunc = results[b'unifunc']
        strfunc = Name(b'__str__', prefix=unifunc.prefix)
        unifunc.replace(strfunc)
        klass = node.clone()
        klass.prefix = b'\n' + find_indentation(node)
        decorator = Node(syms.decorator, [Leaf(token.AT, b'@'), Name(b'python_2_unicode_compatible')])
        decorated = Node(syms.decorated, [decorator, klass], prefix=node.prefix)
        node.replace(decorated)
        touch_import(b'django.utils.encoding', b'python_2_unicode_compatible', decorated)