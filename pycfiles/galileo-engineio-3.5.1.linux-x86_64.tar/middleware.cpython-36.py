# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/engineio/middleware.py
# Compiled at: 2019-08-30 19:22:57
# Size of source mod 2**32: 3596 bytes


class WSGIApp(object):
    __doc__ = "WSGI application middleware for Engine.IO.\n\n    This middleware dispatches traffic to an Engine.IO application. It can\n    also serve a list of static files to the client, or forward unrelated\n    HTTP traffic to another WSGI application.\n\n    :param engineio_app: The Engine.IO server. Must be an instance of the\n                         ``engineio.Server`` class.\n    :param wsgi_app: The WSGI app that receives all other traffic.\n    :param static_files: A dictionary where the keys are URLs that should be\n                         served as static files. For each URL, the value is\n                         a dictionary with ``content_type`` and ``filename``\n                         keys. This option is intended to be used for serving\n                         client files during development.\n    :param engineio_path: The endpoint where the Engine.IO application should\n                          be installed. The default value is appropriate for\n                          most cases.\n\n    Example usage::\n\n        import engineio\n        import eventlet\n\n        eio = engineio.Server()\n        app = engineio.WSGIApp(eio, static_files={\n            '/': {'content_type': 'text/html', 'filename': 'index.html'},\n            '/index.html': {'content_type': 'text/html',\n                            'filename': 'index.html'},\n        })\n        eventlet.wsgi.server(eventlet.listen(('', 8000)), app)\n    "

    def __init__(self, engineio_app, wsgi_app=None, static_files=None, engineio_path='engine.io'):
        self.engineio_app = engineio_app
        self.wsgi_app = wsgi_app
        self.engineio_path = engineio_path.strip('/')
        self.static_files = static_files or {}

    def __call__(self, environ, start_response):
        if 'gunicorn.socket' in environ:

            class Input(object):

                def __init__(self, socket):
                    self.socket = socket

                def get_socket(self):
                    return self.socket

            environ['eventlet.input'] = Input(environ['gunicorn.socket'])
        else:
            path = environ['PATH_INFO']
            if path is not None:
                if path.startswith('/{0}/'.format(self.engineio_path)):
                    return self.engineio_app.handle_request(environ, start_response)
            if path in self.static_files:
                start_response('200 OK', [
                 (
                  'Content-Type', self.static_files[path]['content_type'])])
                with open(self.static_files[path]['filename'], 'rb') as (f):
                    return [
                     f.read()]
            else:
                if self.wsgi_app is not None:
                    return self.wsgi_app(environ, start_response)
                else:
                    start_response('404 Not Found', [('Content-type', 'text/plain')])
                    return ['Not Found']


class Middleware(WSGIApp):
    __doc__ = 'This class has been renamed to ``WSGIApp`` and is now deprecated.'

    def __init__(self, engineio_app, wsgi_app=None, engineio_path='engine.io'):
        super(Middleware, self).__init__(engineio_app, wsgi_app, engineio_path=engineio_path)