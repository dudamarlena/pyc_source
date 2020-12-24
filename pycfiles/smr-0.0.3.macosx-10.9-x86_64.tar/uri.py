# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/smr/uri.py
# Compiled at: 2014-07-27 16:57:55
from __future__ import absolute_import, division, print_function, unicode_literals
import boto
from boto.s3.key import Key
from datetime import timedelta
import os, re, sys, tempfile
S3_BUCKETS = {}

def get_s3_bucket(bucket_name, config):
    if bucket_name not in S3_BUCKETS:
        if config.aws_access_key and config.aws_secret_key:
            s3conn = boto.connect_s3(config.aws_access_key, config.aws_secret_key)
        else:
            s3conn = boto.connect_s3()
        S3_BUCKETS[bucket_name] = s3conn.get_bucket(bucket_name)
    return S3_BUCKETS[bucket_name]


def date_generator(end_date, num_days):
    for n in reversed(xrange(num_days)):
        yield end_date - timedelta(n)


def get_s3_uri(m, file_names, config):
    """
    populates file_names list with urls that matched the regex match object
    returns the total filesize of all the files matched
    """
    bucket_name = m.group(1)
    path = m.group(2)
    bucket = get_s3_bucket(bucket_name, config)
    result = 0
    if (config.start_date or config.date_range) and (b'{year' in path or b'{month' in path or b'{day' in path):
        for tmp_date in date_generator(config.end_date, config.date_range or (config.end_date - config.start_date).days + 1):
            for key in bucket.list(prefix=path.format(year=tmp_date.year, month=tmp_date.month, day=tmp_date.day)):
                file_names.append((b's3://{}/{}').format(bucket_name, key.name))
                result += key.size

    else:
        for key in bucket.list(prefix=path):
            file_names.append((b's3://{}/{}').format(bucket_name, key.name))
            result += key.size

    return result


def get_local_uri(m, file_names, _):
    """
    populates file_names list with urls that matched the regex match object
    returns the total filesize of all the files matched
    """
    path = m.group(2)
    result = 0
    for root, _, files in os.walk(path):
        for file_name in files:
            absolute_path = os.path.join(root, file_name)
            file_names.append((b'file:/{}').format(absolute_path))
            result += os.path.getsize(absolute_path)

    return result


def download_s3_uri(m, config):
    bucket_name = m.group(1)
    path = m.group(2)
    bucket = get_s3_bucket(bucket_name, config)
    k = Key(bucket)
    k.key = path
    with tempfile.NamedTemporaryFile(delete=False) as (temp_file):
        k.get_contents_to_filename(temp_file.name)
        return temp_file.name


def download_local_uri(m, _):
    return m.group(2)


def cleanup_s3_uri(temp_filename):
    try:
        os.unlink(temp_filename)
    except OSError:
        pass


URI_REGEXES = [
 (
  re.compile(b'^s3://([^/]+)/?(.*)', re.IGNORECASE), get_s3_uri, download_s3_uri, cleanup_s3_uri),
 (
  re.compile(b'^(file:/)?(/.*)', re.IGNORECASE), get_local_uri, download_local_uri, None)]

def get_uris(config):
    """ returns a tuple of total file size in bytes, and the list of files """
    file_names = []
    if config.INPUT_DATA is None:
        sys.stderr.write(b'you need to provide INPUT_DATA in config\n')
        sys.exit(1)
    if isinstance(config.INPUT_DATA, basestring):
        config.INPUT_DATA = [
         config.INPUT_DATA]
    file_size = 0
    for uri in config.INPUT_DATA:
        for regex, uri_method, _, _ in URI_REGEXES:
            m = regex.match(uri)
            if m is not None:
                file_size += uri_method(m, file_names, config)
                break

    print((b'going to process {} files...').format(len(file_names)))
    return (file_size, file_names)


def download(config, uri):
    for regex, _, dl_method, _ in URI_REGEXES:
        m = regex.match(uri)
        if m is not None:
            return dl_method(m, config)

    return


def cleanup(uri, temp_filename):
    for regex, _, _, cleanup_method in URI_REGEXES:
        m = regex.match(uri)
        if m is not None and cleanup_method is not None:
            return cleanup_method(temp_filename)

    return