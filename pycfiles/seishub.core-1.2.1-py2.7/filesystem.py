# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\resources\filesystem.py
# Compiled at: 2010-12-23 17:42:43
"""
File system based resources.
"""
from seishub.core.exceptions import NotFoundError, ForbiddenError, InternalServerError
from seishub.core.processor.interfaces import IFileSystemResource, IScriptResource
from seishub.core.processor.resources.resource import Resource
from twisted.python import filepath
from twisted.web import static, script
from zope.interface import implements

class PythonScript(script.PythonScript):
    implements(IScriptResource)


class ResourceScript(script.ResourceScriptWrapper):
    implements(IScriptResource)


class FileSystemResource(Resource, filepath.FilePath):
    """
    A file system resource.
    """
    implements(IFileSystemResource)
    content_types = static.loadMimeTypes()
    content_encodings = {'.gz': 'gzip', '.bz2': 'bzip2'}
    type = None

    def __init__(self, path, default_type='text/html', registry=None, processors={'.epy': PythonScript, '.rpy': ResourceScript}, **kwargs):
        Resource.__init__(self, **kwargs)
        filepath.FilePath.__init__(self, path)
        self.restat()
        if self.isdir():
            self.category = 'folder'
            self.is_leaf = False
            self.folderish = True
        else:
            self.category = 'file'
            self.is_leaf = True
            self.folderish = False
        self.default_type = default_type
        self.registry = registry or static.Registry()
        self.processors = processors

    def getMetadata(self):
        self.restat()
        s = self.statinfo
        return {'size': s.st_size, 'uid': s.st_uid, 
           'gid': s.st_gid, 
           'permissions': s.st_mode, 
           'atime': s.st_atime, 
           'mtime': s.st_mtime, 
           'nlink': s.st_nlink}

    def getChild(self, id, request):
        self.restat()
        if not self.isdir():
            raise ForbiddenError('Item %s is not a valid path' % self.path)
        id = id.decode('utf-8')
        fpath = self.child(id)
        if not fpath.exists():
            raise NotFoundError('Item %s does not exists' % id)
        proc = self.processors.get(fpath.splitext()[1].lower())
        if proc:
            request.setHeader('content-type', 'text/html; charset=UTF-8')
            return proc(fpath.path, self.registry)
        return self._clone(fpath.path)

    def _clone(self, path):
        return self.__class__(path, default_type=self.default_type, registry=self.registry, processors=self.processors, hidden=self.hidden, public=self.public)

    def render_GET(self, request):
        """
        Returns either the content of the folder or the file object.
        """
        if not self.exists():
            raise NotFoundError('Item %s does not exists.' % self.path)
        if self.isdir():
            ids = sorted(self.listdir())
            children = {}
            for id in ids:
                safe_id = id.encode('UTF-8')
                children[safe_id] = self._clone(self.child(id).path)

            children.update(self.children)
            return children
        if self.isfile():
            return self
        msg = "I don't know how to handle item %s." % self.path
        raise InternalServerError(msg)