# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/objectstore/s3.py
# Compiled at: 2019-04-28 04:54:30
"""
Object Store plugin for the Amazon Simple Storage Service (S3)
"""
import logging, multiprocessing, os, shutil, subprocess, threading, time
from datetime import datetime
try:
    import boto
    from boto.exception import S3ResponseError
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
except ImportError:
    boto = None

from galaxy.exceptions import ObjectInvalid, ObjectNotFound
from galaxy.util import directory_hash_id, string_as_bool, umask_fix_perms, which
from galaxy.util.path import safe_relpath
from galaxy.util.sleeper import Sleeper
from .s3_multipart_upload import multipart_upload
from ..objectstore import convert_bytes, ObjectStore
NO_BOTO_ERROR_MESSAGE = 'S3/Swift object store configured, but no boto dependency available.Please install and properly configure boto or modify object store configuration.'
log = logging.getLogger(__name__)
logging.getLogger('boto').setLevel(logging.INFO)

def parse_config_xml(config_xml):
    try:
        a_xml = config_xml.findall('auth')[0]
        access_key = a_xml.get('access_key')
        secret_key = a_xml.get('secret_key')
        b_xml = config_xml.findall('bucket')[0]
        bucket_name = b_xml.get('name')
        use_rr = string_as_bool(b_xml.get('use_reduced_redundancy', 'False'))
        max_chunk_size = int(b_xml.get('max_chunk_size', 250))
        cn_xml = config_xml.findall('connection')
        if not cn_xml:
            cn_xml = {}
        else:
            cn_xml = cn_xml[0]
        host = cn_xml.get('host', None)
        port = int(cn_xml.get('port', 6000))
        multipart = string_as_bool(cn_xml.get('multipart', 'True'))
        is_secure = string_as_bool(cn_xml.get('is_secure', 'True'))
        conn_path = cn_xml.get('conn_path', '/')
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
        return {'auth': {'access_key': access_key, 
                    'secret_key': secret_key}, 
           'bucket': {'name': bucket_name, 
                      'use_reduced_redundancy': use_rr, 
                      'max_chunk_size': max_chunk_size}, 
           'connection': {'host': host, 
                          'port': port, 
                          'multipart': multipart, 
                          'is_secure': is_secure, 
                          'conn_path': conn_path}, 
           'cache': {'size': cache_size, 
                     'path': staging_path}, 
           'extra_dirs': extra_dirs}
    except Exception:
        log.exception('Malformed ObjectStore Configuration XML -- unable to continue')
        raise

    return


class CloudConfigMixin(object):

    def _config_to_dict(self):
        return {'auth': {'access_key': self.access_key, 
                    'secret_key': self.secret_key}, 
           'bucket': {'name': self.bucket, 
                      'use_reduced_redundancy': self.use_rr}, 
           'connection': {'host': self.host, 
                          'port': self.port, 
                          'multipart': self.multipart, 
                          'is_secure': self.is_secure, 
                          'conn_path': self.conn_path}, 
           'cache': {'size': self.cache_size, 
                     'path': self.staging_path}}


class S3ObjectStore(ObjectStore, CloudConfigMixin):
    """
    Object store that stores objects as items in an AWS S3 bucket. A local
    cache exists that is used as an intermediate location for files between
    Galaxy and S3.
    """
    store_type = 's3'

    def __init__(self, config, config_dict):
        super(S3ObjectStore, self).__init__(config)
        self.transfer_progress = 0
        auth_dict = config_dict['auth']
        bucket_dict = config_dict['bucket']
        connection_dict = config_dict.get('connection', {})
        cache_dict = config_dict['cache']
        self.access_key = auth_dict.get('access_key')
        self.secret_key = auth_dict.get('secret_key')
        self.bucket = bucket_dict.get('name')
        self.use_rr = bucket_dict.get('use_reduced_redundancy', False)
        self.max_chunk_size = bucket_dict.get('max_chunk_size', 250)
        self.host = connection_dict.get('host', None)
        self.port = connection_dict.get('port', 6000)
        self.multipart = connection_dict.get('multipart', True)
        self.is_secure = connection_dict.get('is_secure', True)
        self.conn_path = connection_dict.get('conn_path', '/')
        self.cache_size = cache_dict.get('size', -1)
        self.staging_path = cache_dict.get('path') or self.config.object_store_cache_path
        extra_dirs = dict((e['type'], e['path']) for e in config_dict.get('extra_dirs', []))
        self.extra_dirs.update(extra_dirs)
        log.debug('Object cache dir:    %s', self.staging_path)
        log.debug('       job work dir: %s', self.extra_dirs['job_work'])
        self._initialize()
        return

    def _initialize(self):
        if boto is None:
            raise Exception(NO_BOTO_ERROR_MESSAGE)
        self.s3server = {'access_key': self.access_key, 'secret_key': self.secret_key, 
           'is_secure': self.is_secure, 
           'max_chunk_size': self.max_chunk_size, 
           'host': self.host, 
           'port': self.port, 
           'use_rr': self.use_rr, 
           'conn_path': self.conn_path}
        self._configure_connection()
        self.bucket = self._get_bucket(self.bucket)
        if self.cache_size != -1:
            self.cache_size = self.cache_size * 1073741824
            self.sleeper = Sleeper()
            self.cache_monitor_thread = threading.Thread(target=self.__cache_monitor)
            self.cache_monitor_thread.start()
            log.info('Cache cleaner manager started')
        if which('axel'):
            self.use_axel = True
        else:
            self.use_axel = False
        return

    def _configure_connection(self):
        log.debug('Configuring S3 Connection')
        self.conn = S3Connection(self.access_key, self.secret_key)

    @classmethod
    def parse_xml(clazz, config_xml):
        return parse_config_xml(config_xml)

    def to_dict(self):
        as_dict = super(S3ObjectStore, self).to_dict()
        as_dict.update(self._config_to_dict())
        return as_dict

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
                self.__clean_cache(file_list, delete_this_much)
            self.sleeper.sleep(30)

    def __clean_cache(self, file_list, delete_this_much):
        """ Keep deleting files from the file_list until the size of the deleted
        files is greater than the value in delete_this_much parameter.

        :type file_list: list
        :param file_list: List of candidate files that can be deleted. This method
            will start deleting files from the beginning of the list so the list
            should be sorted accordingly. The list must contains 3-element tuples,
            positioned as follows: position 0 holds file last accessed timestamp
            (as time.struct_time), position 1 holds file path, and position 2 has
            file size (e.g., (<access time>, /mnt/data/dataset_1.dat), 472394)

        :type delete_this_much: int
        :param delete_this_much: Total size of files, in bytes, that should be deleted.
        """
        deleted_amount = 0
        for entry in file_list:
            if deleted_amount < delete_this_much:
                deleted_amount += entry[2]
                os.remove(entry[1])
            else:
                log.debug('Cache cleaning done. Total space freed: %s', convert_bytes(deleted_amount))
                return

    def _get_bucket(self, bucket_name):
        """ Sometimes a handle to a bucket is not established right away so try
        it a few times. Raise error is connection is not established. """
        for i in range(5):
            try:
                bucket = self.conn.get_bucket(bucket_name)
                log.debug("Using cloud object store with bucket '%s'", bucket.name)
                return bucket
            except S3ResponseError:
                try:
                    log.debug("Bucket not found, creating s3 bucket with handle '%s'", bucket_name)
                    self.conn.create_bucket(bucket_name)
                except S3ResponseError:
                    log.exception("Could not get bucket '%s', attempt %s/5", bucket_name, i + 1)
                    time.sleep(2)

        raise S3ResponseError

    def _fix_permissions(self, rel_path):
        """ Set permissions on rel_path"""
        for basedir, _, files in os.walk(rel_path):
            umask_fix_perms(basedir, self.config.umask, 511, self.config.gid)
            for filename in files:
                path = os.path.join(basedir, filename)
                if os.path.islink(path):
                    continue
                umask_fix_perms(path, self.config.umask, 438, self.config.gid)

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
            rel_path = '%s/' % rel_path
            if not dir_only:
                rel_path = os.path.join(rel_path, alt_name if alt_name else 'dataset_%s.dat' % obj.id)
            return rel_path

    def _get_cache_path(self, rel_path):
        return os.path.abspath(os.path.join(self.staging_path, rel_path))

    def _get_transfer_progress(self):
        return self.transfer_progress

    def _get_size_in_s3(self, rel_path):
        try:
            key = self.bucket.get_key(rel_path)
            if key:
                return key.size
        except S3ResponseError:
            log.exception("Could not get size of key '%s' from S3", rel_path)
            return -1

    def _key_exists(self, rel_path):
        exists = False
        try:
            is_dir = rel_path[(-1)] == '/'
            if is_dir:
                keyresult = self.bucket.get_all_keys(prefix=rel_path)
                if len(keyresult) > 0:
                    exists = True
                else:
                    exists = False
            else:
                key = Key(self.bucket, rel_path)
                exists = key.exists()
        except S3ResponseError:
            log.exception("Trouble checking existence of S3 key '%s'", rel_path)
            return False

        if rel_path[0] == '/':
            raise
        return exists

    def _in_cache(self, rel_path):
        """ Check if the given dataset is in the local cache and return True if so. """
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
        self.transfer_progress += 10

    def _download(self, rel_path):
        try:
            log.debug("Pulling key '%s' into cache to %s", rel_path, self._get_cache_path(rel_path))
            key = self.bucket.get_key(rel_path)
            if self.cache_size > 0 and key.size > self.cache_size:
                log.critical('File %s is larger (%s) than the cache size (%s). Cannot download.', rel_path, key.size, self.cache_size)
                return False
            if self.use_axel:
                log.debug("Parallel pulled key '%s' into cache to %s", rel_path, self._get_cache_path(rel_path))
                ncores = multiprocessing.cpu_count()
                url = key.generate_url(7200)
                ret_code = subprocess.call(['axel', '-a', '-n', ncores, url])
                if ret_code == 0:
                    return True
            else:
                log.debug("Pulled key '%s' into cache to %s", rel_path, self._get_cache_path(rel_path))
                self.transfer_progress = 0
                key.get_contents_to_filename(self._get_cache_path(rel_path), cb=self._transfer_cb, num_cb=10)
                return True
        except S3ResponseError:
            log.exception("Problem downloading key '%s' from S3 bucket '%s'", rel_path, self.bucket.name)

        return False

    def _push_to_os(self, rel_path, source_file=None, from_string=None):
        """
        Push the file pointed to by ``rel_path`` to the object store naming the key
        ``rel_path``. If ``source_file`` is provided, push that file instead while
        still using ``rel_path`` as the key name.
        If ``from_string`` is provided, set contents of the file to the value of
        the string.
        """
        try:
            source_file = source_file if source_file else self._get_cache_path(rel_path)
            if os.path.exists(source_file):
                key = Key(self.bucket, rel_path)
                if os.path.getsize(source_file) == 0 and key.exists():
                    log.debug("Wanted to push file '%s' to S3 key '%s' but its size is 0; skipping.", source_file, rel_path)
                    return True
                if from_string:
                    key.set_contents_from_string(from_string, reduced_redundancy=self.use_rr)
                    log.debug("Pushed data from string '%s' to key '%s'", from_string, rel_path)
                else:
                    start_time = datetime.now()
                    log.debug("Pushing cache file '%s' of size %s bytes to key '%s'", source_file, os.path.getsize(source_file), rel_path)
                    mb_size = os.path.getsize(source_file) / 1000000.0
                    if mb_size < 10 or not self.multipart:
                        self.transfer_progress = 0
                        key.set_contents_from_filename(source_file, reduced_redundancy=self.use_rr, cb=self._transfer_cb, num_cb=10)
                    else:
                        multipart_upload(self.s3server, self.bucket, key.name, source_file, mb_size)
                    end_time = datetime.now()
                    log.debug("Pushed cache file '%s' to key '%s' (%s bytes transfered in %s sec)", source_file, rel_path, os.path.getsize(source_file), end_time - start_time)
                return True
            log.error("Tried updating key '%s' from source file '%s', but source file does not exist.", rel_path, source_file)
        except S3ResponseError:
            log.exception("Trouble pushing S3 key '%s' from file '%s'", rel_path, source_file)

        return False

    def file_ready(self, obj, **kwargs):
        """
        A helper method that checks if a file corresponding to a dataset is
        ready and available to be used. Return ``True`` if so, ``False`` otherwise.
        """
        rel_path = self._construct_path(obj, **kwargs)
        if self._in_cache(rel_path):
            if os.path.getsize(self._get_cache_path(rel_path)) == self._get_size_in_s3(rel_path):
                return True
            log.debug('Waiting for dataset %s to transfer from OS: %s/%s', rel_path, os.path.getsize(self._get_cache_path(rel_path)), self._get_size_in_s3(rel_path))
        return False

    def exists(self, obj, **kwargs):
        in_cache = in_s3 = False
        rel_path = self._construct_path(obj, **kwargs)
        if self._in_cache(rel_path):
            in_cache = True
        in_s3 = self._key_exists(rel_path)
        dir_only = kwargs.get('dir_only', False)
        base_dir = kwargs.get('base_dir', None)
        if dir_only:
            if in_cache or in_s3:
                return True
            if base_dir:
                if not os.path.exists(rel_path):
                    os.makedirs(rel_path)
                return True
            return False
        if in_cache and not in_s3:
            self._push_to_os(rel_path, source_file=self._get_cache_path(rel_path))
            return True
        else:
            if in_s3:
                return True
            else:
                return False

            return

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
        raise ObjectNotFound('objectstore.empty, object does not exist: %s, kwargs: %s' % (
         str(obj), str(kwargs)))

    def size(self, obj, **kwargs):
        rel_path = self._construct_path(obj, **kwargs)
        if self._in_cache(rel_path):
            try:
                return os.path.getsize(self._get_cache_path(rel_path))
            except OSError as ex:
                log.info("Could not get size of file '%s' in local cache, will try S3. Error: %s", rel_path, ex)

        elif self.exists(obj, **kwargs):
            return self._get_size_in_s3(rel_path)
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
                results = self.bucket.get_all_keys(prefix=rel_path)
                for key in results:
                    log.debug('Deleting key %s', key.name)
                    key.delete()

                return True
            os.unlink(self._get_cache_path(rel_path))
            if self._key_exists(rel_path):
                key = Key(self.bucket, rel_path)
                log.debug('Deleting key %s', key.name)
                key.delete()
                return True
        except S3ResponseError:
            log.exception("Could not delete key '%s' from S3", rel_path)
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
        base_dir = kwargs.get('base_dir', None)
        dir_only = kwargs.get('dir_only', False)
        obj_dir = kwargs.get('obj_dir', False)
        rel_path = self._construct_path(obj, **kwargs)
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
            raise ObjectNotFound('objectstore.get_filename, no cache_path: %s, kwargs: %s' % (
             str(obj), str(kwargs)))
            return

    def update_from_file(self, obj, file_name=None, create=False, **kwargs):
        if create:
            self.create(obj, **kwargs)
        if self.exists(obj, **kwargs):
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
            raise ObjectNotFound('objectstore.update_from_file, object does not exist: %s, kwargs: %s' % (
             str(obj), str(kwargs)))

    def get_object_url(self, obj, **kwargs):
        if self.exists(obj, **kwargs):
            rel_path = self._construct_path(obj, **kwargs)
            try:
                key = Key(self.bucket, rel_path)
                return key.generate_url(expires_in=86400)
            except S3ResponseError:
                log.exception("Trouble generating URL for dataset '%s'", rel_path)

        return

    def get_store_usage_percent(self):
        return 0.0


class SwiftObjectStore(S3ObjectStore):
    """
    Object store that stores objects as items in a Swift bucket. A local
    cache exists that is used as an intermediate location for files between
    Galaxy and Swift.
    """
    store_type = 'swift'

    def _configure_connection(self):
        log.debug('Configuring Swift Connection')
        self.conn = boto.connect_s3(aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key, is_secure=self.is_secure, host=self.host, port=self.port, calling_format=boto.s3.connection.OrdinaryCallingFormat(), path=self.conn_path)