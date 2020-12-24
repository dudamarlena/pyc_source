# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/service.py
# Compiled at: 2016-04-04 17:18:11
from __future__ import unicode_literals
from ..tags.context import ContextElementBase
from ..elements.elementbase import ReturnContainer
from ..compat import text_type, raw_input
import subprocess, weakref

class ServiceCallElement(ContextElementBase):
    """A psuedo element that proxies a Python callable"""
    xmlns = b'http://moyaproject.com/db'
    _element_class = b'logic'

    class Meta:
        is_call = True
        app_first_arg = True

    def __init__(self, archive, element_name, service_callable, document):
        self.libname = element_name
        self.service = service_callable
        self._document = weakref.ref(document)
        self.parent_docid = None
        self._tag_name = b'ServiceCall'
        self._children = ()
        self._attributes = {}
        self._code = b''
        self._libid = None
        self.source_line = 0
        self._element_type = ('http://moyaproject.com', '')
        self._location = text_type(service_callable.__code__)
        return

    def __iter__(self):
        yield self

    def check(self, context):
        return True

    def close(self):
        pass

    def logic(self, context):
        try:
            call = context[b'.call']
            args = call.pop(b'args', ())
            if context.get(b'._winpdb_debug', False):
                password = context.get(b'._winpdb_password', b'password')
                del context[b'._winpdb_debug']
                del context[b'._winpdb_password']
                try:
                    import rpdb2
                except ImportError:
                    context[b'.console'].text(b'rpdb2 is required to debug with WinPDB', fg=b'red', bold=True)
                else:
                    context[b'.console'].text((b"Reading to launch winpdb... Click File -> Attach and enter password '{}'").format(password), fg=b'green', bold=True)
                    raw_input(b'Hit <RETURN> to continue ')
                    subprocess.Popen([b'winpdb'])
                    rpdb2.start_embedded_debugger(password)

            if getattr(self.service, b'call_with_context', False):
                ret = self.service(context, *args, **call)
            else:
                ret = self.service(*args, **call)
            context[b'_return'] = ReturnContainer(ret)
        except Exception as e:
            raise