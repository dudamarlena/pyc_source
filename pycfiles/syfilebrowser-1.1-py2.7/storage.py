# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syfilebrowser/storage.py
# Compiled at: 2016-01-26 01:30:27
from __future__ import unicode_literals
import os, shutil
from django.core.files.move import file_move_safe
from django.core.files.base import ContentFile

class StorageMixin(object):
    """
    Adds some useful methods to the Storage class.
    """

    def isdir(self, name):
        """
        Returns true if name exists and is a directory.
        """
        raise NotImplementedError()

    def isfile(self, name):
        """
        Returns true if name exists and is a regular file.
        """
        raise NotImplementedError()

    def move(self, old_file_name, new_file_name, allow_overwrite=False):
        """
        Moves safely a file from one location to another.

        If allow_ovewrite==False and new_file_name exists, raises an exception.
        """
        raise NotImplementedError()

    def makedirs(self, name):
        """
        Creates all missing directories specified by name. Analogue to os.mkdirs().
        """
        raise NotImplementedError()

    def rmtree(self, name):
        """
        Deletes a directory and everything it contains. Analogue to shutil.rmtree().
        """
        raise NotImplementedError()


class FileSystemStorageMixin(StorageMixin):

    def isdir(self, name):
        return os.path.isdir(self.path(name))

    def isfile(self, name):
        return os.path.isfile(self.path(name))

    def move(self, old_file_name, new_file_name, allow_overwrite=False):
        file_move_safe(self.path(old_file_name), self.path(new_file_name), allow_overwrite=True)

    def makedirs(self, name):
        os.makedirs(self.path(name))

    def rmtree(self, name):
        shutil.rmtree(self.path(name))


class S3BotoStorageMixin(StorageMixin):

    def isfile(self, name):
        return self.exists(name)

    def isdir(self, name):
        if not name:
            return True
        if self.isfile(name):
            return False
        name = self._normalize_name(self._clean_name(name))
        dirlist = self.bucket.list(self._encode_name(name))
        for item in dirlist:
            return True

        return False

    def move(self, old_file_name, new_file_name, allow_overwrite=False):
        if self.exists(new_file_name):
            if allow_overwrite:
                self.delete(new_file_name)
            else:
                raise b"The destination file '%s' exists and allow_overwrite is False" % new_file_name
        old_key_name = self._encode_name(self._normalize_name(self._clean_name(old_file_name)))
        new_key_name = self._encode_name(self._normalize_name(self._clean_name(new_file_name)))
        k = self.bucket.copy_key(new_key_name, self.bucket.name, old_key_name)
        if not k:
            raise b"Couldn't copy '%s' to '%s'" % (old_file_name, new_file_name)
        self.delete(old_file_name)

    def makedirs(self, name):
        self.save(name + b'/.folder', ContentFile(b''))

    def rmtree(self, name):
        name = self._normalize_name(self._clean_name(name))
        dirlist = self.bucket.list(self._encode_name(name))
        for item in dirlist:
            item.delete()


class GoogleStorageMixin(StorageMixin):

    def isfile(self, name):
        return self.exists(name)

    def isdir(self, name):
        if not name:
            return True
        if self.isfile(name):
            return False
        name = self._normalize_name(self._clean_name(name))
        dirlist = self.bucket.list(self._encode_name(name))
        for item in dirlist:
            return True

        return False

    def move(self, old_file_name, new_file_name, allow_overwrite=False):
        if self.exists(new_file_name):
            if allow_overwrite:
                self.delete(new_file_name)
            else:
                raise b"The destination file '%s' exists and allow_overwrite is False" % new_file_name
        old_key_name = self._encode_name(self._normalize_name(self._clean_name(old_file_name)))
        new_key_name = self._encode_name(self._normalize_name(self._clean_name(new_file_name)))
        k = self.bucket.copy_key(new_key_name, self.bucket.name, old_key_name)
        if not k:
            raise b"Couldn't copy '%s' to '%s'" % (old_file_name, new_file_name)
        self.delete(old_file_name)

    def makedirs(self, name):
        self.save(name + b'/.folder', ContentFile(b''))

    def rmtree(self, name):
        name = self._normalize_name(self._clean_name(name))
        dirlist = self.bucket.list(self._encode_name(name))
        for item in dirlist:
            item.delete()