# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_yaml.py
# Compiled at: 2020-01-06 16:40:45
from __future__ import absolute_import, division, print_function, unicode_literals
from six import StringIO
from unittest import TestCase
from yaml.constructor import ConstructorError
from octodns.yaml import safe_dump, safe_load

class TestYaml(TestCase):

    def test_stuff(self):
        self.assertEquals({1: b'a', 
           2: b'b', 
           b'3': b'c', 
           10: b'd', 
           b'11': b'e'}, safe_load(b"\n1: a\n2: b\n'3': c\n10: d\n'11': e\n"))
        self.assertEquals({b'*.1.2': b'a', 
           b'*.2.2': b'b', 
           b'*.10.1': b'c', 
           b'*.11.2': b'd'}, safe_load(b"\n'*.1.2': 'a'\n'*.2.2': 'b'\n'*.10.1': 'c'\n'*.11.2': 'd'\n"))
        with self.assertRaises(ConstructorError) as (ctx):
            safe_load(b"\n'*.2.2': 'b'\n'*.1.2': 'a'\n'*.11.2': 'd'\n'*.10.1': 'c'\n")
        self.assertTrue(b'keys out of order: expected *.1.2 got *.2.2 at' in ctx.exception.problem)
        buf = StringIO()
        safe_dump({b'*.1.1': 42, 
           b'*.11.1': 43, 
           b'*.2.1': 44}, buf)
        self.assertEquals(b"---\n'*.1.1': 42\n'*.2.1': 44\n'*.11.1': 43\n", buf.getvalue())
        buf = StringIO()
        safe_dump({b'45a03129': 42, 
           b'45a0392a': 43}, buf)
        self.assertEquals(b'---\n45a0392a: 43\n45a03129: 42\n', buf.getvalue())