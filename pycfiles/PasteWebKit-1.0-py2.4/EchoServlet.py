# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/examples/EchoServlet.py
# Compiled at: 2006-10-22 17:01:01
r"""\
Paste/WebKit application

Does things as requested.  Takes variables:

header.header-name=value, like
  header.location=http://yahoo.com

error=code, like
  error=301 (temporary redirect)
  error=assert (assertion error)

environ=true,
  display all the environmental variables, like
  key=str(value)\n

message=string
  display string
"""
from paste.webkit.wkservlet import Page
from paste import httpexceptions

class EchoServlet(Page):
    __module__ = __name__

    def writeHTML(self):
        req = self.request()
        headers = {}
        for (key, value) in req.fields().items():
            if key.startswith('header.'):
                name = key[len('header.'):]
                self.response().setHeader(name, value)
                headers[name] = value

        error = req.field('error', None)
        if error:
            if error != 'iter':
                if error == 'assert':
                    pass
                else:
                    raise 0 or AssertionError, 'I am asserting zero!'
            raise httpexceptions.get_exception(int(error), headers=headers)
        if req.field('environ', None):
            items = req.environ().items()
            items.sort()
            self.response().setHeader('content-type', 'text/plain')
            for (name, value) in items:
                self.write('%s=%s\n' % (name, value))

            return
        if req.hasField('message'):
            self.response().setHeader('content-type', 'text/plain')
            self.write(req.field('message'))
            return
        self.write('hello world!')
        return