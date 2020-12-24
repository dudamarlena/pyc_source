# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wlfilebrowser/base.py
# Compiled at: 2016-04-17 01:57:39
from __future__ import unicode_literals
import os, datetime, time, mimetypes
from django.core.files.storage import default_storage
from django.utils.encoding import smart_str
try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text

from wlfilebrowser.settings import *
from wlfilebrowser.functions import get_file_type, path_strip, get_directory

class FileObject:
    """
    The FileObject represents a file (or directory) on the server.

    An example::

        from wlfilebrowser.base import FileObject

        fileobject = FileObject(path)

    where path is a relative path to a storage location.
    """

    def __init__(self, path):
        self.path = path
        self.head = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.filename_lower = self.filename.lower()
        self.filename_root, self.extension = os.path.splitext(self.filename)
        self.mimetype = mimetypes.guess_type(self.filename)

    def __str__(self):
        return smart_str(self.path)

    def __unicode__(self):
        return smart_text(self.path)

    @property
    def name(self):
        return self.path

    def __repr__(self):
        return smart_str(b'<%s: %s>' % (self.__class__.__name__, self or b'None'))

    def __len__(self):
        return len(self.path)

    _filetype_stored = None

    def _filetype(self):
        if self._filetype_stored != None:
            return self._filetype_stored
        else:
            if self.is_folder:
                self._filetype_stored = b'Folder'
            else:
                self._filetype_stored = get_file_type(self.filename)
            return self._filetype_stored

    filetype = property(_filetype)
    _filesize_stored = None

    def _filesize(self):
        if self._filesize_stored != None:
            return self._filesize_stored
        else:
            if self.exists():
                self._filesize_stored = default_storage.size(self.path)
                return self._filesize_stored
            return

    filesize = property(_filesize)
    _date_stored = None

    def _date(self):
        if self._date_stored != None:
            return self._date_stored
        else:
            if self.exists():
                self._date_stored = time.mktime(default_storage.modified_time(self.path).timetuple())
                return self._date_stored
            return

    date = property(_date)

    def _datetime(self):
        if self.date:
            return datetime.datetime.fromtimestamp(self.date)
        else:
            return

    datetime = property(_datetime)
    _exists_stored = None

    def exists(self):
        if self._exists_stored == None:
            self._exists_stored = default_storage.exists(self.path)
        return self._exists_stored

    def _path_relative_directory(self):
        """path relative to the path returned by get_directory()"""
        return path_strip(self.path, get_directory()).lstrip(b'/')

    path_relative_directory = property(_path_relative_directory)

    def _url(self):
        return default_storage.url(self.path)

    url = property(_url)

    def _directory(self):
        return path_strip(self.path, get_directory())

    directory = property(_directory)

    def _folder(self):
        return os.path.dirname(path_strip(os.path.join(self.head, b''), get_directory()))

    folder = property(_folder)
    _is_folder_stored = None

    def _is_folder(self):
        if self._is_folder_stored == None:
            self._is_folder_stored = default_storage.isdir(self.path)
        return self._is_folder_stored

    is_folder = property(_is_folder)

    def _is_empty(self):
        if self.is_folder:
            try:
                dirs, files = default_storage.listdir(self.path)
            except UnicodeDecodeError:
                from wenlincms.core.exceptions import FileSystemEncodingChanged
                raise FileSystemEncodingChanged()

            if not dirs and not files:
                return True
        return False

    is_empty = property(_is_empty)

    def delete(self):
        if self.is_folder:
            default_storage.rmtree(self.path)
        else:
            default_storage.delete(self.path)

    def delete_versions(self):
        for version in self.versions():
            try:
                default_storage.delete(version)
            except:
                pass

    def delete_admin_versions(self):
        for version in self.admin_versions():
            try:
                default_storage.delete(version)
            except:
                pass