# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webdb/interface/file.py
# Compiled at: 2018-02-19 04:07:25
# Size of source mod 2**32: 4539 bytes
"""
Web interface for file access.
"""
import cherrypy, logging
logger = logging.getLogger(__name__)

@cherrypy.expose
class DispatchedFile(object):
    __doc__ = '\n\tThis is the class that actually serves a file.\n\tSee the documentation of FileInterface, about the usage.\n\t'

    def __init__(self, dispatcher, inject, nickname):
        self._dispatcher = dispatcher
        self._inject = inject
        self._nickname = nickname
        self._file = None

    def before_operation(self):
        self._file = self._dispatcher.dispatch_file(self._nickname, self._inject())

    def GET(self, offset=0, chunk_size=0):
        self.before_operation()
        try:
            offset = int(offset)
        except:
            cherrypy.response.headers['Status'] = 400
            return (b'cannot convert {} to int').format(offset)

        try:
            chunk_size = int(chunk_size)
        except:
            cherrypy.response.headers['Status'] = 400
            return (b'cannot convert {} to int').format(chunk_size)
        else:
            try:
                file_part = self._file.get_file_part(offset, chunk_size)
            except Exception as e:
                cherrypy.response.headers['Status'] = 404
                logger.error(e, exc_info=True)
                return str(e).encode('UTF-8')

            cherrypy.response.headers['Status'] = 200
            cherrypy.response.headers['Content-Type'] = 'application/octet-stream'
            return file_part

    def POST(self, offset=0):
        self.before_operation()
        try:
            offset = int(offset)
        except:
            cherrypy.response.headers['Status'] = 400
            return (b'cannot convert {} to int').format(offset)
        else:
            try:
                self._file.copy_file_part(offset, cherrypy.request.body)
            except Exception as e:
                cherrypy.response.headers['Status'] = 404
                logger.error(e, exc_info=True)
                return str(e).encode('UTF-8')

            cherrypy.response.headers['Status'] = 204

    def DELETE(self, truncate=None):
        self.before_operation()
        try:
            truncate = int(truncate)
        except:
            truncate = None

        try:
            if truncate != None:
                self._file.truncate(truncate)
            else:
                self._file.remove_file()
        except Exception as e:
            cherrypy.response.headers['Status'] = 404
            logger.error(e, exc_info=True)
            return str(e).encode('UTF-8')

        cherrypy.response.headers['Status'] = 204

    def PUT(self):
        self.before_operation()
        try:
            self._file.create_file()
        except Exception as e:
            cherrypy.response.headers['Status'] = 404
            logger.error(e, exc_info=True)
            return str(e).encode('UTF-8')

        cherrypy.response.headers['Status'] = 204


class FileInterface(object):
    __doc__ = '\n\tServes files. \n\tA HTTP POST will write (a part of ) the file,\n\tHTTP GET will return (a part of) the file.\n\n\t**Interface:**\n\n\tFiles are associated with a path. Assuming that the interface\n\tis mounted under ``/files``, it will dispatch ``/files/foo/bar.baz``\n\tto the path ``foo/bar.baz``. This path is passed to the dispatcher\n\tinstance and the actual FileOverlay will be dispatched.\n\n\tOne can delete the file using HTTP DELETE. If the argument ``?truncate=<bytes>``\n\tis supplied, the file will be truncated to ``<bytes>``. \n\t**NOTE**: if ``<bytes>`` cannot be converted to an integer, the file\n\twill be deleted.\n\n\tThe file can be created expicily by using HTTP PUT.\n\n\tOne can receive (a part) of a file using HTTP GET. If ``offset``\n\tis provided the file part will start at byte ``offset``. If\n\t``chunk_size`` is provided at most ``chunk_size`` bytes will be\n\treturned.\n\n\tHTTP POST will set (a part) of a file. If ``offset`` is provided\n\tthe file part will be written at ``offset``. Content-Type must be\n\t``application/octet-stream``.\n\n\tIf the POST/DELETE/PUT request succeed Status 204 will be set.\n\tIf GET succeeds Status 200 will be set and the (binary) file content\n\twill be returned. Content-Type in this case is ``application/octet-stream``.\n\n\tIf any request fails Status 404 will be set and a (more or less) helpful\n\terror message will be returned. If an argument cannot be parsed properly\n\tStatus 400 will be set and an error message will be returned.\n\n\tThe constructor argument ``inject`` is a callable that returns the second\n\targument of the dispatcher\'s dispatch_file. Usually this will be something\n\tlike ``lambda: cherrypy.session["username"]``.\n\n\tXXX:\n\t***NOTE***:\n\n\tYoun MUST (!) add ``{\'request.dispatch\': cherrypy.dispatch.MethodDispatcher()}``\n\tto your application config. If you forget that cherrypy will not be able to\n\tdispatch the methods properly.\n\t'

    def __init__(self, dispatcher, inject):
        self._dispatcher = dispatcher
        self._inject = inject

    def _cp_dispatch(self, vpath):
        nickname = '/'.join(vpath)
        vpath.clear()
        return DispatchedFile(self._dispatcher, self._inject, nickname)