# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/objectstore/azure_blob.py
# Compiled at: 2019-04-28 04:54:30
"""
Object Store plugin for the Microsoft Azure Block Blob Storage system
"""
import logging, os, shutil, threading, time
from datetime import datetime
try:
    from azure.common import AzureHttpError
    from azure.storage import CloudStorageAccount
    from azure.storage.blob import BlockBlobService
    from azure.storage.blob.models import Blob
except ImportError:
    BlockBlobService = None

from galaxy.exceptions import ObjectInvalid, ObjectNotFound
from galaxy.util import directory_hash_id, umask_fix_perms
from galaxy.util.path import safe_relpath
from galaxy.util.sleeper import Sleeper
from ..objectstore import convert_bytes, ObjectStore
NO_BLOBSERVICE_ERROR_MESSAGE = 'ObjectStore configured, but no azure.storage.blob dependency available.Please install and properly configure azure.storage.blob or modify Object Store configuration.'
log = logging.getLogger(__name__)

def parse_config_xml(config_xml):
    try:
        auth_xml = config_xml.findall('auth')[0]
        account_name = auth_xml.get('account_name')
        account_key = auth_xml.get('account_key')
        container_xml = config_xml.find('container')
        container_name = container_xml.get('name')
        max_chunk_size = int(container_xml.get('max_chunk_size', 250))
        c_xml = config_xml.findall('cache')[0]
        cache_size = float(c_xml.get('size', -1))
        staging_path = c_xml.get('path', None)
        tag, attrs = 'extra_dir', ('type', 'path')
        extra_dirs = config_xml.findall(tag)
        if not extra_dirs:
            msg = ('No {tag} element in XML tree').format(tag=tag)
            log.error(msg)
            raise Exception(msg)
        extra_dirs = [ dict((k, e.get(k)) for k in attrs) for e in extra_dirs ]
        return {'auth': {'account_name': account_name, 
                    'account_key': account_key}, 
           'container': {'name': container_name, 
                         'max_chunk_size': max_chunk_size}, 
           'cache': {'size': cache_size, 
                     'path': staging_path}, 
           'extra_dirs': extra_dirs}
    except Exception:
        log.exception('Malformed ObjectStore Configuration XML -- unable to continue')
        raise

    return


class AzureBlobObjectStore(ObjectStore):
    """
    Object store that stores objects as blobs in an Azure Blob Container. A local
    cache exists that is used as an intermediate location for files between
    Galaxy and Azure.
    """
    store_type = 'azure_blob'

    def __init__(self, config, config_dict):
        super(AzureBlobObjectStore, self).__init__(config, config_dict)
        self.transfer_progress = 0
        auth_dict = config_dict['auth']
        container_dict = config_dict['container']
        cache_dict = config_dict['cache']
        self.account_name = auth_dict.get('account_name')
        self.account_key = auth_dict.get('account_key')
        self.container_name = container_dict.get('name')
        self.max_chunk_size = container_dict.get('max_chunk_size', 250)
        self.cache_size = cache_dict.get('size', -1)
        self.staging_path = cache_dict.get('path') or self.config.object_store_cache_path
        self._initialize()

    def _initialize(self):
        if BlockBlobService is None:
            raise Exception(NO_BLOBSERVICE_ERROR_MESSAGE)
        self._configure_connection()
        if self.cache_size != -1:
            self.cache_size = self.cache_size * 1073741824
            self.sleeper = Sleeper()
            self.cache_monitor_thread = threading.Thread(target=self.__cache_monitor)
            self.cache_monitor_thread.start()
            log.info('Cache cleaner manager started')
        return

    def to_dict(self):
        as_dict = super(AzureBlobObjectStore, self).to_dict()
        as_dict.update({'auth': {'account_name': self.account_name, 
                    'account_key': self.account_key}, 
           'container': {'name': self.container_name, 
                         'max_chunk_size': self.max_chunk_size}, 
           'cache': {'size': self.cache_size, 
                     'path': self.staging_path}})
        return as_dict

    @classmethod
    def parse_xml(clazz, config_xml):
        return parse_config_xml(config_xml)

    def _configure_connection(self):
        log.debug('Configuring Connection')
        self.account = CloudStorageAccount(self.account_name, self.account_key)
        self.service = self.account.create_block_blob_service()

    def _construct_path(self, obj, base_dir=None, dir_only=None, extra_dir=None, extra_dir_at_root=False, alt_name=None, obj_dir=False, **kwargs):
        if extra_dir and extra_dir != os.path.normpath(extra_dir):
            log.warning('extra_dir is not normalized: %s', extra_dir)
            raise ObjectInvalid('The requested object is invalid')
        if alt_name:
            if not safe_relpath(alt_name):
                log.warning('alt_name would locate path outside dir: %s', alt_name)
                raise ObjectInvalid('The requested object is invalid')
            alt_name = os.path.normpath(alt_name)
        rel_path = os.path.join(*directory_hash_id(obj.id))
        if extra_dir is not None:
            if extra_dir_at_root:
                rel_path = os.path.join(extra_dir, rel_path)
            else:
                rel_path = os.path.join(rel_path, extra_dir)
        if obj_dir:
            rel_path = os.path.join(rel_path, str(obj.id))
        if base_dir:
            base = self.extra_dirs.get(base_dir)
            return os.path.join(base, rel_path)
        else:
            if not dir_only:
                rel_path = os.path.join(rel_path, alt_name if alt_name else 'dataset_%s.dat' % obj.id)
            return rel_path

    def _fix_permissions(self, rel_path):
        """ Set permissions on rel_path"""
        for basedir, _, files in os.walk(rel_path):
            umask_fix_perms(basedir, self.config.umask, 511, self.config.gid)
            for filename in files:
                path = os.path.join(basedir, filename)
                if os.path.islink(path):
                    continue
                umask_fix_perms(path, self.config.umask, 438, self.config.gid)

    def _get_cache_path(self, rel_path):
        return os.path.abspath(os.path.join(self.staging_path, rel_path))

    def _get_transfer_progress(self):
        return self.transfer_progress

    def _get_size_in_azure(self, rel_path):
        try:
            properties = self.service.get_blob_properties(self.container_name, rel_path)
            if type(properties) is Blob:
                properties = properties.properties
            if properties:
                size_in_bytes = properties.content_length
                return size_in_bytes
        except AzureHttpError:
            log.exception("Could not get size of blob '%s' from Azure", rel_path)
            return -1

    def _in_azure(self, rel_path):
        try:
            exists = self.service.exists(self.container_name, rel_path)
        except AzureHttpError:
            log.exception("Trouble checking existence of Azure blob '%s'", rel_path)
            return False

        return exists

    def _in_cache(self, rel_path):
        """ Check if the given dataset is in the local cache. """
        cache_path = self._get_cache_path(rel_path)
        return os.path.exists(cache_path)

    def _pull_into_cache(self, rel_path):
        rel_path_dir = os.path.dirname(rel_path)
        if not os.path.exists(self._get_cache_path(rel_path_dir)):
            os.makedirs(self._get_cache_path(rel_path_dir))
        file_ok = self._download(rel_path)
        self._fix_permissions(self._get_cache_path(rel_path_dir))
        return file_ok

    def _transfer_cb(self, complete, total):
        self.transfer_progress = float(complete) / float(total) * 100

    def _download(self, rel_path):
        local_destination = self._get_cache_path(rel_path)
        try:
            log.debug("Pulling '%s' into cache to %s", rel_path, local_destination)
            if self.cache_size > 0 and self._get_size_in_azure(rel_path) > self.cache_size:
                log.critical('File %s is larger (%s) than the cache size (%s). Cannot download.', rel_path, self._get_size_in_azure(rel_path), self.cache_size)
                return False
            self.transfer_progress = 0
            self.service.get_blob_to_path(self.container_name, rel_path, local_destination, progress_callback=self._transfer_cb)
            return True
        except AzureHttpError:
            log.exception("Problem downloading '%s' from Azure", rel_path)

        return False

    def _push_to_os(self, rel_path, source_file=None, from_string=None):
        """
        Push the file pointed to by ``rel_path`` to the object store naming the blob
        ``rel_path``. If ``source_file`` is provided, push that file instead while
        still using ``rel_path`` as the blob name.
        If ``from_string`` is provided, set contents of the file to the value of
        the string.
        """
        try:
            source_file = source_file or self._get_cache_path(rel_path)
            if not os.path.exists(source_file):
                log.error("Tried updating blob '%s' from source file '%s', but source file does not exist.", rel_path, source_file)
                return False
            if os.path.getsize(source_file) == 0:
                log.debug("Wanted to push file '%s' to azure blob '%s' but its size is 0; skipping.", source_file, rel_path)
                return True
            if from_string:
                self.service.create_blob_from_text(self.container_name, rel_path, from_string, progress_callback=self._transfer_cb)
                log.debug("Pushed data from string '%s' to blob '%s'", from_string, rel_path)
            else:
                start_time = datetime.now()
                log.debug("Pushing cache file '%s' of size %s bytes to '%s'", source_file, os.path.getsize(source_file), rel_path)
                self.transfer_progress = 0
                self.service.create_blob_from_path(self.container_name, rel_path, source_file, progress_callback=self._transfer_cb)
                end_time = datetime.now()
                log.debug("Pushed cache file '%s' to blob '%s' (%s bytes transfered in %s sec)", source_file, rel_path, os.path.getsize(source_file), end_time - start_time)
            return True
        except AzureHttpError:
            log.exception("Trouble pushing to Azure Blob '%s' from file '%s'", rel_path, source_file)

        return False

    def exists(self, obj, **kwargs):
        in_cache = in_azure = False
        rel_path = self._construct_path(obj, **kwargs)
        in_cache = self._in_cache(rel_path)
        in_azure = self._in_azure(rel_path)
        dir_only = kwargs.get('dir_only', False)
        base_dir = kwargs.get('base_dir', None)
        if dir_only:
            if in_cache or in_azure:
                return True
            if base_dir:
                if not os.path.exists(rel_path):
                    os.makedirs(rel_path)
                return True
            return False
        if in_cache and not in_azure:
            self._push_to_os(rel_path, source_file=self._get_cache_path(rel_path))
            return True
        else:
            if in_azure:
                return True
            else:
                return False

            return

    def file_ready(self, obj, **kwargs):
        """
        A helper method that checks if a file corresponding to a dataset is
        ready and available to be used. Return ``True`` if so, ``False`` otherwise.
        """
        rel_path = self._construct_path(obj, **kwargs)
        if self._in_cache(rel_path):
            local_size = os.path.getsize(self._get_cache_path(rel_path))
            remote_size = self._get_size_in_azure(rel_path)
            if local_size == remote_size:
                return True
            log.debug('Waiting for dataset %s to transfer from OS: %s/%s', rel_path, local_size, remote_size)
        return False

    def create(self, obj, **kwargs):
        if not self.exists(obj, **kwargs):
            extra_dir = kwargs.get('extra_dir', None)
            extra_dir_at_root = kwargs.get('extra_dir_at_root', False)
            dir_only = kwargs.get('dir_only', False)
            alt_name = kwargs.get('alt_name', None)
            rel_path = os.path.join(*directory_hash_id(obj.id))
            if extra_dir is not None:
                if extra_dir_at_root:
                    rel_path = os.path.join(extra_dir, rel_path)
                else:
                    rel_path = os.path.join(rel_path, extra_dir)
            cache_dir = os.path.join(self.staging_path, rel_path)
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            if not dir_only:
                rel_path = os.path.join(rel_path, alt_name if alt_name else 'dataset_%s.dat' % obj.id)
                open(os.path.join(self.staging_path, rel_path), 'w').close()
                self._push_to_os(rel_path, from_string='')
        return

    def empty(self, obj, **kwargs):
        if self.exists(obj, **kwargs):
            return bool(self.size(obj, **kwargs) > 0)
        raise ObjectNotFound('objectstore.empty, object does not exist: %s, kwargs: %s' % (str(obj), str(kwargs)))

    def size(self, obj, **kwargs):
        rel_path = self._construct_path(obj, **kwargs)
        if self._in_cache(rel_path):
            try:
                return os.path.getsize(self._get_cache_path(rel_path))
            except OSError as ex:
                log.info("Could not get size of file '%s' in local cache, will try Azure. Error: %s", rel_path, ex)

        elif self.exists(obj, **kwargs):
            return self._get_size_in_azure(rel_path)
        log.warning("Did not find dataset '%s', returning 0 for size", rel_path)
        return 0

    def delete(self, obj, entire_dir=False, **kwargs):
        rel_path = self._construct_path(obj, **kwargs)
        extra_dir = kwargs.get('extra_dir', None)
        base_dir = kwargs.get('base_dir', None)
        dir_only = kwargs.get('dir_only', False)
        obj_dir = kwargs.get('obj_dir', False)
        try:
            if base_dir and dir_only and obj_dir:
                shutil.rmtree(os.path.abspath(rel_path))
                return True
            if entire_dir and extra_dir:
                shutil.rmtree(self._get_cache_path(rel_path))
                blobs = self.service.list_blobs(self.container_name, prefix=rel_path)
                for blob in blobs:
                    log.debug('Deleting from Azure: %s', blob)
                    self.service.delete_blob(self.container_name, blob.name)

                return True
            os.unlink(self._get_cache_path(rel_path))
            if self._in_azure(rel_path):
                log.debug('Deleting from Azure: %s', rel_path)
                self.service.delete_blob(self.container_name, rel_path)
                return True
        except AzureHttpError:
            log.exception("Could not delete blob '%s' from Azure", rel_path)
        except OSError:
            log.exception('%s delete error', self.get_filename(obj, **kwargs))

        return False

    def get_data(self, obj, start=0, count=-1, **kwargs):
        rel_path = self._construct_path(obj, **kwargs)
        if not self._in_cache(rel_path):
            self._pull_into_cache(rel_path)
        data_file = open(self._get_cache_path(rel_path), 'r')
        data_file.seek(start)
        content = data_file.read(count)
        data_file.close()
        return content

    def get_filename(self, obj, **kwargs):
        rel_path = self._construct_path(obj, **kwargs)
        base_dir = kwargs.get('base_dir', None)
        dir_only = kwargs.get('dir_only', False)
        obj_dir = kwargs.get('obj_dir', False)
        if base_dir and dir_only and obj_dir:
            return os.path.abspath(rel_path)
        else:
            cache_path = self._get_cache_path(rel_path)
            if self._in_cache(rel_path):
                return cache_path
            if self.exists(obj, **kwargs):
                if dir_only:
                    return cache_path
                if self._pull_into_cache(rel_path):
                    return cache_path
            raise ObjectNotFound('objectstore.get_filename, no cache_path: %s, kwargs: %s' % (str(obj), str(kwargs)))
            return

    def update_from_file(self, obj, file_name=None, create=False, **kwargs):
        if create is True:
            self.create(obj, **kwargs)
        elif self.exists(obj, **kwargs):
            rel_path = self._construct_path(obj, **kwargs)
            if file_name:
                source_file = os.path.abspath(file_name)
                cache_file = self._get_cache_path(rel_path)
                try:
                    if source_file != cache_file:
                        shutil.copy2(source_file, cache_file)
                    self._fix_permissions(cache_file)
                except OSError:
                    log.exception("Trouble copying source file '%s' to cache '%s'", source_file, cache_file)

            else:
                source_file = self._get_cache_path(rel_path)
            self._push_to_os(rel_path, source_file)
        else:
            raise ObjectNotFound('objectstore.update_from_file, object does not exist: %s, kwargs: %s' % (str(obj), str(kwargs)))

    def get_object_url(self, obj, **kwargs):
        if self.exists(obj, **kwargs):
            rel_path = self._construct_path(obj, **kwargs)
            try:
                url = self.service.make_blob_url(container_name=self.container_name, blob_name=rel_path)
                return url
            except AzureHttpError:
                log.exception("Trouble generating URL for dataset '%s'", rel_path)

        return

    def get_store_usage_percent(self):
        return 0.0

    def __cache_monitor(self):
        time.sleep(2)
        while self.running:
            total_size = 0
            file_list = []
            for dirpath, _, filenames in os.walk(self.staging_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    file_size = os.path.getsize(filepath)
                    total_size += file_size
                    last_access_time = time.localtime(os.stat(filepath)[7])
                    file_tuple = (
                     last_access_time, filepath, file_size)
                    file_list.append(file_tuple)

            file_list.sort()
            cache_limit = self.cache_size * 0.9
            if total_size > cache_limit:
                log.info('Initiating cache cleaning: current cache size: %s; clean until smaller than: %s', convert_bytes(total_size), convert_bytes(cache_limit))
                delete_this_much = total_size - cache_limit
                deleted_amount = 0
                for entry in enumerate(file_list):
                    if deleted_amount < delete_this_much:
                        deleted_amount += entry[2]
                        os.remove(entry[1])
                    else:
                        log.debug('Cache cleaning done. Total space freed: %s', convert_bytes(deleted_amount))

            self.sleeper.sleep(30)