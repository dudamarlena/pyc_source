# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/storage/cloudfiles.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 8383 bytes
"""
Make it so that ``import cloudfiles`` does not pick THIS file, but the
python-cloudfiles one.

http://docs.python.org/whatsnew/2.5.html#pep-328-absolute-and-relative-imports
"""
from __future__ import absolute_import
from mediagoblin.storage import StorageInterface, clean_listy_filepath
import cloudfiles, mimetypes, logging
_log = logging.getLogger(__name__)

class CloudFilesStorage(StorageInterface):
    __doc__ = "\n    OpenStack/Rackspace Cloud's Swift/CloudFiles support\n    "
    local_storage = False

    def __init__(self, **kwargs):
        self.param_container = kwargs.get('cloudfiles_container')
        self.param_user = kwargs.get('cloudfiles_user')
        self.param_api_key = kwargs.get('cloudfiles_api_key')
        self.param_host = kwargs.get('cloudfiles_host')
        self.param_use_servicenet = kwargs.get('cloudfiles_use_servicenet')
        mimetypes.add_type('video/webm', 'webm')
        if not self.param_host:
            _log.info('No CloudFiles host URL specified, defaulting to Rackspace US')
        self.connection = cloudfiles.get_connection(username=self.param_user, api_key=self.param_api_key, servicenet=True if self.param_use_servicenet == 'true' or self.param_use_servicenet == True else False)
        _log.debug('Connected to {0} (auth: {1})'.format(self.connection.connection.host, self.connection.auth.host))
        if not self.param_container == self.connection.get_container(self.param_container):
            self.container = self.connection.create_container(self.param_container)
            self.container.make_public(ttl=7200)
        else:
            self.container = self.connection.get_container(self.param_container)
        _log.debug('Container: {0}'.format(self.container.name))
        self.container_uri = self.container.public_ssl_uri()

    def _resolve_filepath(self, filepath):
        return '/'.join(clean_listy_filepath(filepath))

    def file_exists(self, filepath):
        try:
            self.container.get_object(self._resolve_filepath(filepath))
            return True
        except cloudfiles.errors.NoSuchObject:
            return False

    def get_file(self, filepath, *args, **kwargs):
        """
        - Doesn't care about the "mode" argument.
        """
        try:
            obj = self.container.get_object(self._resolve_filepath(filepath))
        except cloudfiles.errors.NoSuchObject:
            obj = self.container.create_object(self._resolve_filepath(filepath))
            mimetype = mimetypes.guess_type(filepath[(-1)])
            if mimetype[0]:
                obj.content_type = mimetype[0]
                obj.metadata = {'mime-type': mimetype[0]}
            else:
                obj.content_type = 'application/octet-stream'
                obj.metadata = {'mime-type': 'application/octet-stream'}

        return CloudFilesStorageObjectWrapper(obj, *args, **kwargs)

    def delete_file(self, filepath):
        try:
            try:
                self.container.delete_object(self._resolve_filepath(filepath))
            except cloudfiles.container.ResponseError:
                pass

        finally:
            pass

    def file_url(self, filepath):
        return '/'.join([
         self.container_uri,
         self._resolve_filepath(filepath)])

    def copy_locally(self, filepath, dest_path):
        """
        Copy this file locally.

        A basic working method for this is provided that should
        function both for local_storage systems and remote storge
        systems, but if more efficient systems for copying locally
        apply to your system, override this method with something more
        appropriate.
        """
        with self.get_file(filepath, 'rb') as (source_file):
            with open(dest_path, 'wb') as (dest_file):
                for data in source_file:
                    dest_file.write(data)

    def copy_local_to_storage(self, filename, filepath):
        """
        Copy this file from locally to the storage system.

        This is kind of the opposite of copy_locally.  It's likely you
        could override this method with something more appropriate to
        your storage system.
        """
        _log.debug('Sending {0} to cloudfiles...'.format(filepath))
        with self.get_file(filepath, 'wb') as (dest_file):
            with open(filename, 'rb') as (source_file):
                dest_file.send(source_file)

    def get_file_size(self, filepath):
        """Returns the file size in bytes"""
        obj = self.container.get_object(self._resolve_filepath(filepath))
        return obj.total_bytes


class CloudFilesStorageObjectWrapper:
    __doc__ = "\n    Wrapper for python-cloudfiles's cloudfiles.storage_object.Object\n    used to circumvent the mystic `medium.jpg` corruption issue, where\n    we had both python-cloudfiles and PIL doing buffering on both\n    ends and causing breakage.\n\n    This wrapper currently meets mediagoblin's needs for a public_store\n    file-like object.\n    "

    def __init__(self, storage_object, *args, **kwargs):
        self.storage_object = storage_object

    def read(self, *args, **kwargs):
        _log.debug('Reading {0}'.format(self.storage_object.name))
        return self.storage_object.read(*args, **kwargs)

    def write(self, data, *args, **kwargs):
        self.storage_object.write(data, *args, **kwargs)

    def send(self, *args, **kw):
        self.storage_object.send(*args, **kw)

    def close(self):
        """
        Not sure we need anything here.
        """
        pass

    def __enter__(self):
        """
        Context Manager API implementation
        http://docs.python.org/library/stdtypes.html#context-manager-types
        """
        return self

    def __exit__(self, *exc_info):
        """
        Context Manger API implementation
        see self.__enter__()
        """
        self.close()

    def __iter__(self, **kwargs):
        """Make CloudFile an iterator, yielding 8192 bytes by default

        This returns a generator object that can be used to getting the
        object's content in a memory efficient way.

        Warning: The HTTP response is only complete after this generator
        has raised a StopIteration. No other methods can be called until
        this has occurred."""
        return self.storage_object.stream(**kwargs)