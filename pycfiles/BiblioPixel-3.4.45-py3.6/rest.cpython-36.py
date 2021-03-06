# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/rest/rest.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1144 bytes
import pathlib
from . import rest_server
from .. import control
from ...util import server_cache
PORT = 8787
ROOT_FOLDER = pathlib.Path(__file__).parents[3] / 'ui' / 'rest'
INDEX_FILE = 'index.html'

class Rest(control.ExtractedControl, server_cache.StaticCache):
    OPEN_PAGE = False
    SERVER_CLASS = rest_server.RestServer

    def __init__(self, *args, port=PORT, external_access=False, open_page=None, root_folder=ROOT_FOLDER, index_file=INDEX_FILE, **kwds):
        (super().__init__)(*args, **kwds)
        if open_page is None:
            open_page = self.OPEN_PAGE
        cached_server = self.cache().get_server(port,
          external_access=external_access, open_page=open_page,
          root_folder=root_folder,
          index_file=index_file)
        self.rest_server = cached_server.server

    def set_project(self, project):
        self.rest_server.set_project(project)
        super().set_project(project)

    def cleanup(self):
        self.rest_server.set_project(None)
        super().cleanup()

    def _make_thread(self):
        return self.rest_server


class OpenPage(Rest):
    OPEN_PAGE = True