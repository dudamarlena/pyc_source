# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fhsu/work/muffin-playground/muffin_playground/__init__.py
# Compiled at: 2016-09-15 21:35:24
# Size of source mod 2**32: 8563 bytes
import sys, json, subprocess, mimetypes
from pathlib import Path
import asyncio
from aiohttp import hdrs
from aiohttp.web import HTTPFound
from aiohttp.web_exceptions import HTTPNotFound, HTTPNotModified
import muffin
from muffin.urls import StaticRoute, StaticResource
from mako.template import Template
from mako.lookup import TemplateLookup
from plim import preprocessor
from . import watcher
__version__ = '0.0.10'
ERROR_JAVASCRIPT = "\ndocument.body.onload = function() {\n    document.body.innerHTML = '';\n    var pre = document.createElement('pre');\n    pre.innerText = %s;\n    document.body.appendChild(pre);\n}\n"
resources = Path(__file__).parent / 'resources'
lookup = TemplateLookup(directories=[
 '.', str(resources)], preprocessor=preprocessor)

class Application(muffin.Application):

    def __init__(self, *args, **kwargs):
        if 'DEBUG' not in kwargs:
            kwargs['DEBUG'] = True
        if 'name' not in kwargs:
            kwargs['name'] = 'playground'
        self.client_debug = kwargs.pop('client_debug', True)
        super().__init__(*args, **kwargs)
        if self.client_debug:
            self.debug_sockets = set()
            self.router.add_route('GET', '/__debug.js', debug_js)
            self.router.add_route('GET', '/__debug__/', self._debug_websocket)

            def start_callback(app):
                self.watcher = watcher.Watcher(dir='.', app=self)
                self.watcher.start()
                self.on_shutdown.append(lambda app: self.watcher.stop())

            self.register_on_start(start_callback)

    def register_special_static_route(self, prefix='/', directory='.'):

        def start_callback(app):
            err_fn = self._write_debug_sockets if self.client_debug else (lambda x: None)
            route = SpecialFileStaticRoute(name=None, prefix=prefix, directory=directory, client_debug=self.client_debug, error_reporting_func=err_fn)
            self.router.register_route(route)
            self.router.add_static('/boilerplate/', str(resources))

        self.register_on_start(start_callback)

    def render(self, tmpl_file, **kwargs):
        if not isinstance(tmpl_file, Path):
            tmpl_file = Path(tmpl_file)
        return render(tmpl_file, **kwargs)

    def start_task_in_executor(self, fn, *args):
        return start_task_in_executor(fn, *args)

    async def _debug_websocket(self, request):
        ws = muffin.WebSocketResponse()
        await ws.prepare(request)
        self.debug_sockets.add(ws)
        async for msg in ws:
                        pass

        self.debug_sockets.remove(ws)
        return ws

    def _write_debug_sockets(self, data):
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        for ws in self.debug_sockets:
            ws.send_str(data)


class SpecialFileStaticRoute(StaticRoute):

    def __init__(self, *args, **kwargs):
        self.client_debug = kwargs.pop('client_debug', True)
        self._report_error = kwargs.pop('error_reporting_func', None)
        super().__init__(*args, **kwargs)

    async def handle(self, request):
        """
        Based on the code in:

        https://github.com/KeepSafe/aiohttp/blob/v0.22.5/aiohttp/web_urldispatcher.py

        """
        filename = request.match_info['filename']
        try:
            filepath = self._directory.joinpath(filename).resolve()
            filepath.relative_to(self._directory)
        except (ValueError, FileNotFoundError) as error:
            raise HTTPNotFound() from error
        except Exception as error:
            request.app.logger.exception(error)
            raise HTTPNotFound() from error

        resp = await self.handle_special_file(request, filepath)
        if resp is not None:
            return resp
        if not filepath.is_file():
            raise HTTPNotFound()
        ret = await self._file_sender.send(request, filepath)
        return ret

    async def handle_special_file(self, request, filepath):
        if filepath.is_dir():
            filepath2 = filepath / 'index.plim'
            if not filepath2.exists():
                raise HTTPNotFound()
            else:
                return await self.render_plim(filepath2)
            if filepath.suffix == '.plim':
                return await self.render_plim(filepath)
            if filepath.suffix == '.pyj':
                return await self.render_rapydscript(filepath)
            if filepath.suffix == '.styl':
                return await self.render_stylus(filepath)

    async def render_plim(self, tmpl_file):
        html = render(tmpl_file)
        if self.client_debug:
            html = html.replace('<head>', '<head><script src="/__debug.js"></script>')
        return muffin.Response(content_type='text/html', text=html)

    async def render_rapydscript(self, pyj_file):
        cmd = [
         'rapydscript', str(pyj_file),
         '--js-version', '6',
         '--import-path', str(resources)]
        code, stdout, stderr = await check_output(cmd)
        if code == 0:
            output = stdout
        else:
            output = b'/*\n\n' + stderr + b'\n\n*/'
            self._report_error(stderr)
        return muffin.Response(content_type='text/javascript', body=output)

    async def render_stylus(self, stylus_file):
        cmd = [
         'stylus', '-p', str(stylus_file)]
        code, stdout, stderr = await check_output(cmd)
        if code == 0:
            output = stdout
        else:
            output = b'/*\n\n' + stderr + b'\n\n*/'
            self._report_error(stderr)
        return muffin.Response(content_type='text/css', body=output)


class WebSocketWriter:

    def __init__(self, wsresponse):
        self.resp = wsresponse

    def write(self, **kwargs):
        if not self.resp.closed:
            self.resp.send_str(json.dumps(kwargs))


class ThreadSafeWebSocketWriter:

    def __init__(self, wsresponse):
        self.resp = wsresponse
        self.loop = asyncio.get_event_loop()

    def write(self, **kwargs):
        if not self.resp.closed:
            data = json.dumps(kwargs)
            self.loop.call_soon_threadsafe(self.resp.send_str, data)


class WebSocketHandler(muffin.Handler):

    async def get(self, request):
        self.request = request
        ws = muffin.WebSocketResponse()
        self.websocket = ws
        await ws.prepare(request)
        await self.on_open()
        async for msg in ws:
                        await self.on_message(msg)

        await self.on_close()
        await ws.close()
        return ws

    async def on_message(self, msg):
        pass

    async def on_open(self):
        pass

    async def on_close(self):
        pass


def render(tmpl_file, **kwargs):
    tmpl = Template(text=tmpl_file.read_text(), lookup=lookup, preprocessor=preprocessor)
    return tmpl.render(**kwargs)


def start_task_in_executor(fn, *args):
    """Execute the given function using the default ThreadPoolExecutor."""
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, fn, *args)


async def check_output(cmd):
    """Basically the asynchronous version of subprocess.check_output()."""
    proc = await asyncio.create_subprocess_exec(*cmd, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return (proc.returncode, stdout, stderr)


async def debug_js(request):
    return muffin.Response(content_type='text/javascript', body=(resources / 'debug.js').read_bytes())


def get_error_javascript(stderr):
    result = ERROR_JAVASCRIPT % json.dumps(stderr.decode('utf-8'))
    return result.encode('utf-8')