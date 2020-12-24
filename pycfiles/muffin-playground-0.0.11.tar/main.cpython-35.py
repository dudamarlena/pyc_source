# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fhsu/work/python-examples/muffin/static/main.py
# Compiled at: 2016-08-05 22:41:47
# Size of source mod 2**32: 3580 bytes
import sys, subprocess, mimetypes, asyncio
from aiohttp import hdrs
from aiohttp.web_exceptions import HTTPNotFound, HTTPNotModified
import muffin
from muffin.urls import StaticRoute, StaticResource

class ExampleApplication(muffin.Application):

    def __init__(self):
        super().__init__('example', DEBUG=True)
        self.register_static_resource()

    def register_static_resource(self):
        route = CustomStaticRoute(None, '/', '.')
        resource = StaticResource(route)
        self.router._reg_resource(resource)


class CustomStaticRoute(StaticRoute):

    @asyncio.coroutine
    def handle(self, request):
        filename = request.match_info['filename']
        try:
            filepath = self._directory.joinpath(filename).resolve()
            filepath.relative_to(self._directory)
        except (ValueError, FileNotFoundError) as error:
            raise HTTPNotFound() from error
        except Exception as error:
            request.logger.exception(error)
            raise HTTPNotFound() from error

        if filepath.is_dir():
            filepath = filepath / 'index.plim'
            if not filepath.exists():
                raise HTTPNotFound()
        else:
            resp = yield from self.render_plim(request, filepath)
            return resp
        if filepath.suffix == '.plim':
            resp = yield from self.render_plim(request, filepath)
            return resp
        if filepath.suffix == '.pyj':
            resp = yield from self.compile_rapydscript(request, filepath)
            return resp
        st = filepath.stat()
        modsince = request.if_modified_since
        if modsince is not None and st.st_mtime <= modsince.timestamp():
            raise HTTPNotModified()
        ct, encoding = mimetypes.guess_type(str(filepath))
        if not ct:
            ct = 'application/octet-stream'
        resp = self._response_factory()
        resp.content_type = ct
        if encoding:
            resp.headers[hdrs.CONTENT_ENCODING] = encoding
        resp.last_modified = st.st_mtime
        file_size = st.st_size
        resp.content_length = file_size
        resp.set_tcp_cork(True)
        try:
            yield from resp.prepare(request)
            with filepath.open('rb') as (f):
                yield from self._sendfile(request, resp, f, file_size)
        finally:
            resp.set_tcp_nodelay(True)

        return resp

    async def render_plim(self, request, tmplfile):
        from mako.template import Template
        from mako.lookup import TemplateLookup
        from plim import preprocessor
        resp = self._response_factory()
        resp.content_type = 'text/html'
        await resp.prepare(request)
        lookup = TemplateLookup(directories=['.'], preprocessor=preprocessor)
        tmpl = Template(text=tmplfile.read_text(), lookup=lookup, preprocessor=preprocessor)
        output = tmpl.render().encode('utf-8')
        resp.content_length = len(output)
        resp.write(output)
        return resp

    async def compile_rapydscript(self, request, pyjfile):
        resp = self._response_factory()
        resp.content_type = 'text/javascript'
        await resp.prepare(request)
        cmd = [
         'rapydscript', str(pyjfile)]
        output = subprocess.check_output(cmd)
        resp.content_length = len(output)
        resp.write(output)
        return resp


app = ExampleApplication()