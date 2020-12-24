# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/paradise4paws/lib/buildout/eggs/hidash-0.2.21-py2.7.egg/hidash/static/libs/bootstrap/test-infra/s3_cache.py
# Compiled at: 2017-01-20 05:06:58
from __future__ import absolute_import, unicode_literals, print_function, division
from sys import argv
from os import environ, stat, remove as _delete_file
from os.path import isfile, dirname, basename, abspath
from hashlib import sha256
from subprocess import check_call as run
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError
NEED_TO_UPLOAD_MARKER = b'.need-to-upload'
BYTES_PER_MB = 1048576
try:
    BUCKET_NAME = environ[b'TWBS_S3_BUCKET']
except KeyError:
    raise SystemExit(b'TWBS_S3_BUCKET environment variable not set!')

def _sha256_of_file(filename):
    hasher = sha256()
    with open(filename, b'rb') as (input_file):
        hasher.update(input_file.read())
    file_hash = hasher.hexdigest()
    print((b'sha256({}) = {}').format(filename, file_hash))
    return file_hash


def _delete_file_quietly(filename):
    try:
        _delete_file(filename)
    except (OSError, IOError):
        pass


def _tarball_size(directory):
    kib = stat(_tarball_filename_for(directory)).st_size // BYTES_PER_MB
    return (b'{} MiB').format(kib)


def _tarball_filename_for(directory):
    return abspath((b'./{}.tar.gz').format(basename(directory)))


def _create_tarball(directory):
    print((b'Creating tarball of {}...').format(directory))
    run([b'tar', b'-czf', _tarball_filename_for(directory), b'-C', dirname(directory), basename(directory)])


def _extract_tarball(directory):
    print((b'Extracting tarball of {}...').format(directory))
    run([b'tar', b'-xzf', _tarball_filename_for(directory), b'-C', dirname(directory)])


def download(directory):
    _delete_file_quietly(NEED_TO_UPLOAD_MARKER)
    try:
        print((b'Downloading {} tarball from S3...').format(friendly_name))
        key.get_contents_to_filename(_tarball_filename_for(directory))
    except S3ResponseError as err:
        open(NEED_TO_UPLOAD_MARKER, b'a').close()
        print(err)
        raise SystemExit((b'Cached {} download failed!').format(friendly_name))

    print((b'Downloaded {}.').format(_tarball_size(directory)))
    _extract_tarball(directory)
    print((b'{} successfully installed from cache.').format(friendly_name))


def upload(directory):
    _create_tarball(directory)
    print((b'Uploading {} tarball to S3... ({})').format(friendly_name, _tarball_size(directory)))
    key.set_contents_from_filename(_tarball_filename_for(directory))
    print((b'{} cache successfully updated.').format(friendly_name))
    _delete_file_quietly(NEED_TO_UPLOAD_MARKER)


if __name__ == b'__main__':
    argv.pop(0)
    if len(argv) != 4:
        raise SystemExit(b'USAGE: s3_cache.py <download | upload> <friendly name> <dependencies file> <directory>')
    mode, friendly_name, dependencies_file, directory = argv
    conn = S3Connection()
    bucket = conn.lookup(BUCKET_NAME, validate=False)
    if bucket is None:
        raise SystemExit(b'Could not access bucket!')
    dependencies_file_hash = _sha256_of_file(dependencies_file)
    key = Key(bucket, dependencies_file_hash)
    key.storage_class = b'REDUCED_REDUNDANCY'
    if mode == b'download':
        download(directory)
    elif mode == b'upload':
        if isfile(NEED_TO_UPLOAD_MARKER):
            upload(directory)
        else:
            print(b'No need to upload anything.')
    else:
        raise SystemExit((b'Unrecognized mode {!r}').format(mode))