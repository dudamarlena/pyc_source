# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/preflight.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ..elements.elementbase import Attribute
from ..tags.context import ContextElementBase
from .. import namespaces
from .. import logic

class Check(ContextElementBase):
    """A pre-flight check"""
    xmlns = namespaces.preflight

    class Help:
        synopsis = b'define a pre-flight test'


class Result(ContextElementBase):
    xmlns = namespaces.preflight
    exit = Attribute(b'Also exit the check', type=b'boolean', default=False)
    status = None

    class Help:
        undocumented = True

    def logic(self, context):
        check = self.get_ancestor((self.xmlns, b'check'))
        text = context.sub(self.text)
        context[b'.preflight'].append((check, self.status, text))
        if self.exit(context):
            raise logic.Unwind()


class Pass(Result):
    status = b'pass'

    class Help:
        synopsis = b'pass a preflight check'


class Fail(Result):
    status = b'fail'

    class Help:
        synopsis = b'fail a preflight check'


class Warning(Result):
    status = b'warning'

    class Help:
        synopsis = b'add a warning result to a preflight check'