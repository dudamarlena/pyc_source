# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/rest/rest_server.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2496 bytes
import contextlib, flask, pathlib, traceback, urllib
from . import flask_server, decorator
from ...util import data_file

class RestServer:

    def __init__(self, port, external_access, open_page, root_folder, index_file):
        root_folder = pathlib.Path(root_folder)
        static_folder = str(root_folder / 'static')
        index_file = pathlib.Path(index_file)
        if not index_file.is_absolute():
            index_file = root_folder / index_file
        self.index_file = str(index_file)
        self.project = None
        self.port = port
        self.flask_server = flask_server.FlaskServer(port,
          external_access, open_page, static_folder=static_folder)
        route = self.flask_server.app.route
        route('/get/<address>', methods=['GET'])(self.get)
        route('/set/<address>/<value>', methods=['GET'])(self.quoted_put)
        route('/single/<address>', methods=['GET'])(self.get)
        route('/single/<address>', methods=['PUT'])(self.put)
        route('/multi', methods=['GET'])(self.multi_get)
        route('/multi/<address>', methods=['GET'])(self.multi_get)
        route('/multi', methods=['PUT'])(self.multi_put)
        route('/multi/<address>', methods=['PUT'])(self.multi_put)
        self.flask_server.start()

    def set_project(self, project):
        self.project = project

    def index(self):
        with open(self.index_file) as (fp):
            return fp.read()

    @decorator.single
    def get(self, editor):
        return self._get(editor)

    @decorator.single
    def quoted_put(self, editor, value):
        unquoted = urllib.parse.unquote_plus(value)
        return self._set(editor, unquoted)

    @decorator.single
    def put(self, editor):
        value = flask.request.values['value']
        return self._set(editor, value)

    @decorator.multi
    def multi_get(self, editor, address):
        return self._get(editor)

    @decorator.multi
    def multi_put(self, editor, address):
        value = flask.request.values[address]
        return self._set(editor, value)

    def _get(self, editor):
        return data_file.dumps((editor.get()), use_yaml=False)

    def _set(self, editor, value):
        loaded = data_file.loads(value)
        editor.set(loaded)
        return True

    @contextlib.contextmanager
    def _abort(self, code):
        try:
            yield
        except:
            if self.verbose:
                traceback.print_exc()
            flask.abort(code)