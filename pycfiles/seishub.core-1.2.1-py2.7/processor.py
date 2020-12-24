# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\processor.py
# Compiled at: 2010-12-23 17:42:43
"""
Request processor.

The processor resolves a resource request containing:

  (1) a method, e.g. GET, PUT, POST, DELETE, etc.,
  (2) a absolute path, e.g. '/folder2/resource1' and
  (3) header information, e.g. {'content-type': 'text/html'}) 

into one of the resource objects of the resource tree object. Errors should be
handled by raising a SeisHubError instance.
"""
from StringIO import StringIO
from seishub.core.exceptions import SeisHubError, NotFoundError
from seishub.core.util.path import splitPath
from twisted.web import http
import urllib
MAXIMAL_URL_LENGTH = 1000
PUT = 'PUT'
GET = 'GET'
POST = 'POST'
DELETE = 'DELETE'
MOVE = 'MOVE'
HEAD = 'HEAD'
OPTIONS = 'OPTIONS'
ALLOWED_HTTP_METHODS = [
 GET, PUT, POST, DELETE, MOVE, HEAD, OPTIONS]

class Processor:
    """
    General class for processing a resource request.
    
    This class is the layer underneath services like HTTP(S), SFTP and WebDAV.
    """

    def __init__(self, env):
        self.env = env
        self.received_headers = {}
        self.code = http.OK
        self.headers = {}
        self.content = StringIO()
        self.data = StringIO()
        self.args = {}
        self.args0 = {}
        self.prepath = []
        self.postpath = []
        self.tree = self.env.tree
        self.allowed_methods = ALLOWED_HTTP_METHODS

    def run(self, method, path='/', content=None, received_headers={}):
        """
        A shortcut to call Processor.process() with default arguments.
        """
        self.prepath = []
        self.postpath = []
        self.method = method
        self.path = str(path)
        if content:
            self.content = content
        if received_headers:
            self.received_headers = received_headers
        return self.process()

    def process(self):
        """
        Working through the process chain.
        
        This method returns either a dictionary for a folder node containing 
        objects implementing the L{IResource} interface or a single object 
        for a leaf node, like a file or document resource.
        """
        if isinstance(self.path, unicode):
            raise TypeError('URL must be a str instance, not unicode!')
        self.path = urllib.unquote(self.path)
        if len(self.path) >= MAXIMAL_URL_LENGTH:
            raise SeisHubError(code=http.REQUEST_URI_TOO_LONG)
        self.postpath = splitPath(self.path)
        self.method = self.method.upper()
        if self.method not in ALLOWED_HTTP_METHODS:
            msg = 'HTTP %s is not implemented.' % self.method
            raise SeisHubError(code=http.NOT_ALLOWED, message=msg)
        self.content.seek(0, 0)
        self.data = self.content.read()
        for id in self.args:
            if not len(self.args[id]):
                continue
            self.args0[id] = self.args[id][0]

        return self.render()

    def render(self):
        """
        Return the rendered result of a child object.
        
        This method should be overwritten in any inheriting class to further
        validate and format the output.
        """
        child = getChildForRequest(self.env.tree, self)
        return child.render(self)

    def setHeader(self, id, value):
        self.headers[id] = value

    def getUser(self):
        try:
            return self.user
        except:
            return

        return


def getChildForRequest(resource, request):
    """
    Traverse resource tree to find who will handle the request.
    """
    while request.postpath and not resource.is_leaf:
        id = request.postpath.pop(0)
        request.prepath.append(id)
        resource = resource.getChildWithDefault(id, request)
        if not resource:
            raise NotFoundError('Resource %s not found.' % request.path)

    return resource