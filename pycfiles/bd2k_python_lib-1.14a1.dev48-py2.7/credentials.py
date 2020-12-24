# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/ec2/credentials.py
# Compiled at: 2018-05-03 13:55:55
import errno, logging, threading, time
from datetime import datetime
import os
from bd2k.util.files import mkdir_p
log = logging.getLogger(__name__)
cache_path = '~/.cache/aws/cached_temporary_credentials'
datetime_format = '%Y-%m-%dT%H:%M:%SZ'

def datetime_to_str(dt):
    """
    Convert a naive (implicitly UTC) datetime object into a string, explicitly UTC.

    >>> datetime_to_str( datetime( 1970, 1, 1, 0, 0, 0 ) )
    '1970-01-01T00:00:00Z'
    """
    return dt.strftime(datetime_format)


def str_to_datetime(s):
    """
    Convert a string, explicitly UTC into a naive (implicitly UTC) datetime object.

    >>> str_to_datetime( '1970-01-01T00:00:00Z' )
    datetime.datetime(1970, 1, 1, 0, 0)

    Just to show that the constructor args for seconds and microseconds are optional:
    >>> datetime(1970, 1, 1, 0, 0, 0)
    datetime.datetime(1970, 1, 1, 0, 0)
    """
    return datetime.strptime(s, datetime_format)


monkey_patch_lock = threading.RLock()
_populate_keys_from_metadata_server_orig = None

def enable_metadata_credential_caching():
    """
    Monkey-patches Boto to allow multiple processes using it to share one set of cached, temporary
    IAM role credentials. This helps avoid hitting request limits imposed on the metadata service
    when too many processes concurrently request those credentials. Function is idempotent.

    This function should be called before any AWS connections attempts are made with Boto.
    """
    global _populate_keys_from_metadata_server_orig
    with monkey_patch_lock:
        if _populate_keys_from_metadata_server_orig is None:
            from boto.provider import Provider
            _populate_keys_from_metadata_server_orig = Provider._populate_keys_from_metadata_server
            Provider._populate_keys_from_metadata_server = _populate_keys_from_metadata_server
    return


def disable_metadata_credential_caching():
    """
    Reverse the effect of enable_metadata_credential_caching()
    """
    global _populate_keys_from_metadata_server_orig
    with monkey_patch_lock:
        if _populate_keys_from_metadata_server_orig is not None:
            from boto.provider import Provider
            Provider._populate_keys_from_metadata_server = _populate_keys_from_metadata_server_orig
            _populate_keys_from_metadata_server_orig = None
    return


def _populate_keys_from_metadata_server(self):
    path = os.path.expanduser(cache_path)
    tmp_path = path + '.tmp'
    while True:
        log.debug('Attempting to read cached credentials from %s.', path)
        try:
            with open(path, 'r') as (f):
                content = f.read()
                if content:
                    record = content.split('\n')
                    assert len(record) == 4
                    self._access_key = record[0]
                    self._secret_key = record[1]
                    self._security_token = record[2]
                    self._credential_expiry_time = str_to_datetime(record[3])
                else:
                    log.debug('%s is empty. Credentials are not temporary.', path)
                    return
        except IOError as e:
            if e.errno == errno.ENOENT:
                log.debug('Cached credentials are missing.')
                dir_path = os.path.dirname(path)
                if not os.path.exists(dir_path):
                    log.debug('Creating parent directory %s', dir_path)
                    mkdir_p(dir_path)
            else:
                raise
        else:
            if self._credentials_need_refresh():
                log.debug('Cached credentials are expired.')
            else:
                log.debug('Cached credentials exist and are still fresh.')
                return
            log.debug('Racing to create %s.', tmp_path)
            try:
                fd = os.open(tmp_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 384)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    log.debug('Lost the race to create %s. Waiting on winner to remove it.', tmp_path)
                    while os.path.exists(tmp_path):
                        time.sleep(0.1)

                    log.debug('Winner removed %s. Trying from the top.', tmp_path)
                else:
                    raise

            try:
                try:
                    log.debug('Won the race to create %s. Requesting credentials from metadata service.', tmp_path)
                    _populate_keys_from_metadata_server_orig(self)
                except:
                    os.close(fd)
                    fd = None
                    log.debug('Failed to obtain credentials, removing %s.', tmp_path)
                    os.unlink(tmp_path)
                    raise
                else:
                    if self._credential_expiry_time is None:
                        os.close(fd)
                        fd = None
                        log.debug('Credentials are not temporary. Leaving %s empty and renaming it to %s.', tmp_path, path)
                    else:
                        log.debug('Writing credentials to %s.', tmp_path)
                        with os.fdopen(fd, 'w') as (fh):
                            fd = None
                            fh.write(('\n').join([
                             self._access_key,
                             self._secret_key,
                             self._security_token,
                             datetime_to_str(self._credential_expiry_time)]))
                        log.debug('Wrote credentials to %s. Renaming it to %s.', tmp_path, path)
                    os.rename(tmp_path, path)
                    return

            finally:
                if fd is not None:
                    os.close(fd)

    return