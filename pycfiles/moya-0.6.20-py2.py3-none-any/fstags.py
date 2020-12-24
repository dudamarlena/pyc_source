# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/fstags.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import absolute_import
from .. import namespaces
from ..elements import Attribute
from ..elements.elementbase import LogicElement
from ..tags.context import DataSetter
from ..compat import text_type
from fs.errors import FSError
from fs.path import dirname
import fs.walk
from fs import wildcard
import hashlib, logging
log = logging.getLogger(b'moya.fs')

class SetContents(LogicElement):
    """Set the contents of a file"""
    xmlns = namespaces.fs

    class Help:
        synopsis = b'write data to a file'

    fsobj = Attribute(b'Filesystem object', required=False, default=None)
    fs = Attribute(b'Filesystem name', required=False, default=None)
    path = Attribute(b'Destination path', required=True)
    contents = Attribute(b'File contents', type=b'expression', required=True, missing=False)

    def logic(self, context):
        params = self.get_parameters(context)
        params.contents
        if self.has_parameter(b'fsobj'):
            dst_fs = params.fsobj
        else:
            dst_fs = self.archive.lookup_filesystem(self, params.fs)
        try:
            dst_fs.makedirs(dirname(params.path), recreate=True)
            if hasattr(params.contents, b'read'):
                dst_fs.setfile(params.path, params.contents)
            elif isinstance(params.contents, bytes):
                dst_fs.setfile(params.path, params.contents)
            elif isinstance(params.contents, text_type):
                dst_fs.settext(params.path, params.contents)
        except Exception as e:
            self.throw(b'fs.set-contents.fail', (b'unable to set file contents ({})').format(e))

        log.debug(b"setcontents '%s'", params.path)


class RemoveFile(LogicElement):
    """Delete a file from a filesystem"""
    xmlns = namespaces.fs

    class Help:
        synopsis = b'delete a file'

    fsobj = Attribute(b'Filesystem object', required=False, default=None)
    fs = Attribute(b'Filesystem name', required=False, default=None)
    path = Attribute(b'Destination path', required=True)
    ifexists = Attribute(b'Only remove if the file exists?', type=b'boolean', required=False)

    def logic(self, context):
        params = self.get_parameters(context)
        if self.has_parameter(b'fsobj'):
            dst_fs = params.fsobj
        else:
            dst_fs = self.archive.lookup_filesystem(self, params.fs)
        if params.ifexists and dst_fs.isfile(params.path):
            return
        try:
            dst_fs.remove(params.path)
        except Exception as e:
            self.throw(b'fs.remove-file.fail', (b"unable to remove '{}' ({})").format(params.path, e))

        log.debug(b"removed '%s'", params.path)


class GetSyspath(DataSetter):
    """
    Get a system path for a path in a filesystem.

    A system path (or 'syspath') is a path that maps to the file on the
    OS filesystem. Not all filesystems can generate syspaths. If Moya is
    unable to generate a syspath it will throw a [c]get-syspath.no-
    syspath[/c] exception.

    """
    xmlns = namespaces.fs

    class Help:
        synopsis = b'get a system path'
        example = b'\n        <fs:get-syspath fs="templates" path="index.html" dst="index_template_path"/>\n        '

    fsobj = Attribute(b'Filesystem object', required=False, default=None)
    fs = Attribute(b'Filesystem name', required=False, default=None)
    path = Attribute(b'Destination path', required=True)

    def logic(self, context):
        params = self.get_parameters(context)
        if self.has_parameter(b'fsobj'):
            dst_fs = params.fsobj
        else:
            dst_fs = self.archive.lookup_filesystem(self, params.fs)
        try:
            syspath = dst_fs.getsyspath(params.path)
        except:
            self.throw(b'fs.get-syspath.no-syspath', (b"{!r} can not generate a syspath for '{}'").format(dst_fs, params.path))

        self.set_context(context, self.dst(context), syspath)


class GetMD5(DataSetter):
    """Get the MD5 of a file"""
    xmlns = namespaces.fs

    class Help:
        synopsis = b'get the md5 of a file'

    fsobj = Attribute(b'Filesystem object', required=False, default=None)
    fs = Attribute(b'Filesystem name', required=False, default=None)
    path = Attribute(b'Path of file', required=True)

    def get_value(self, context):
        params = self.get_parameters(context)
        if self.has_parameter(b'fsobj'):
            fs = params.fsobj
        else:
            fs = self.archive.lookup_filesystem(self, params.fs)
        m = hashlib.md5()
        try:
            with fs.open(params.path, b'rb') as (f):
                while 1:
                    chunk = f.read(16384)
                    if not chunk:
                        break
                    m.update(chunk)

        except FSError:
            self.throw(b'fs.get-md5.fail', (b"unable to read file '{}'").format(params.path))
        else:
            return m.hexdigest()


class GetInfo(DataSetter):
    xmlns = namespaces.fs

    class Help:
        synopsis = b'get an info object for a file'

    fsobj = Attribute(b'Filesystem object', required=False, default=None)
    fs = Attribute(b'Filesystem name', required=False, default=None)
    path = Attribute(b'Path of file', type=b'expression', required=True)

    def get_value(self, context):
        params = self.get_parameters(context)
        if self.has_parameter(b'fsobj'):
            fs = params.fsobj
        else:
            fs = self.archive.lookup_filesystem(self, params.fs)
        try:
            info = fs.getinfo(params.path)
        except FSError:
            self.throw(b'fs.get-info.fail', (b"unable to get info for path '{}'").format(params.path))
        else:
            return info


class GetSize(DataSetter):
    xmlns = namespaces.fs

    class Help:
        synopsis = b'get the size of a file'

    fsobj = Attribute(b'Filesystem object', required=False, default=None)
    fs = Attribute(b'Filesystem name', required=False, default=None)
    path = Attribute(b'Path of file', type=b'expression', required=True)

    def get_value(self, context):
        params = self.get_parameters(context)
        path = text_type(params.path)
        if self.has_parameter(b'fsobj'):
            fs = params.fsobj
        else:
            fs = self.archive.lookup_filesystem(self, params.fs)
        try:
            info = fs.getsize(path)
        except FSError:
            self.throw(b'fs.get-size.fail', (b"unable to get info for path '{}'").format(params.path))
        else:
            return info


class MoyaWalker(fs.walk.Walker):

    def __init__(self, exclude_dirs):
        self.exclude_dirs = exclude_dirs

    def check_open_dir(self, fs, info):
        return not self.exclude_dirs(info.name)


class WalkFiles(DataSetter):
    """Recursively get a list of files in a filesystem."""
    xmlns = namespaces.fs

    class Help:
        synopsis = b'recursively list files in a directory'

    fsobj = Attribute(b'Filesystem object', required=False, default=None)
    path = Attribute(b'Path to walk', required=False, default=b'/')
    fs = Attribute(b'Filesystem name', required=False, default=None)
    files = Attribute(b'One or more wildcards to filter results by, e.g "*.py, *.js"', type=b'commalist', default=b'*')
    excludedirs = Attribute(b'Directory wildcards to exclude form walk, e.g. "*.git, *.svn"', type=b'commalist', default=None)
    search = Attribute(b"Search method ('breadth' or 'depth')", default=b'breadth', choices=[b'breadth', b'depth'])
    dst = Attribute(b'Destination', required=True, type=b'reference')

    def logic(self, context):
        params = self.get_parameters(context)
        if self.has_parameter(b'fsobj'):
            walk_fs = params.fsobj
        else:
            walk_fs = self.archive.get_filesystem(params.fs)
        if params.excludedirs:
            walker = MoyaWalker(wildcard.get_matcher(params.excludedirs, True))
        else:
            walker = fs.walk.Walker()
        paths = list(walker.files(walk_fs, params.path, search=params.search, filter=params.files or None))
        self.set_context(context, params.dst, paths)
        return