# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blobs/controllers/files.py
# Compiled at: 2008-02-19 12:19:12
import logging, hashlib
from paste.fileapp import FileApp
from paste.httpheaders import CONTENT_DISPOSITION
import simplejson
from blobs.controllers import *
log = logging.getLogger(__name__)

class FilesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='html'):
        """GET /files: All items in the collection."""
        files = File.query.filter_by(dtime=None).order_by(File.filename).all()
        if format == 'html':
            c.files = files
            return render('/index.mako')
        else:
            files = [ (f.hash, f.size, f.filename) for f in files ]
            return simplejson.dumps(files)
        return

    def create(self):
        """POST /files: Create a new item."""
        fp = request.params.get('file')
        if fp is None or not hasattr(fp, 'file'):
            abort(400, 'Invalid file')
        hsh = request.params.get('hash')
        sha = hashlib.sha1()
        size = 0
        while True:
            block = fp.file.read(4096)
            if not block:
                break
            size += len(block)
            sha.update(block)

        if hsh and hsh.lower() != sha.hexdigest():
            abort(400, 'Hash mismatch %s %s %s' % (hsh, sha.hexdigest(), size))
        else:
            hsh = sha.hexdigest()
            f = File.query.filter_by(dtime=None, hash=hsh).first()
            if not f:
                f = File(hash=hsh, size=size, type=fp.type, filename=fp.filename)
                fp.file.seek(0)
                h.saveBlob(hsh, fp.file)
                Session.save(f)
                Session.commit()
            redirect_to(h.url_for(action='index'))
        return

    def new(self, format='html'):
        """GET /files/new: Form to create a new item."""
        pass

    def update(self, id):
        """PUT /files/id: Update an existing item."""
        pass

    def delete(self, id):
        """DELETE /files/id: Delete an existing item."""
        f = File.query.filter_by(dtime=None, hash=id).first()
        if not f:
            abort(404)
        f.delete()
        redirect_to(h.url_for(action='index'))
        return

    def show(self, id, format='html'):
        """GET /files/id: Show a specific item."""
        f = File.query.filter_by(dtime=None, hash=id).first()
        if not f:
            abort(404)
        f.atime = h.now()
        Session.commit()
        headers = []
        CONTENT_DISPOSITION.update(headers, filename=f.filename, inline=True)
        app = FileApp(h.getBlobPath(f.hash), content_type=f.type or None, headers=headers)
        return app(request.environ, self.start_response)

    def edit(self, id, format='html'):
        """GET /files/id;edit: Form to edit an existing item."""
        pass