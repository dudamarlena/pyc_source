# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/base.py
# Compiled at: 2017-05-23 09:48:11
from __future__ import print_function, unicode_literals
import datetime, fnmatch, hashlib, json, os, os.path, re, time, requests
from six import string_types, text_type
from six.moves.urllib.parse import quote
from egnyte import exc, configuration
JSON_HEADERS = {b'content-type': b'application/json'}
DEFAULT_TIMEOUT = 30

class Session(object):
    """
    Provides persistent HTTPS connections to the Egnyte API
    """
    time_between_requests = None
    last_request_time = None

    def __init__(self, config=None):
        self.config = config if isinstance(config, dict) else configuration.load(config)
        domain = self.config[b'domain']
        if b'.' not in domain:
            domain += b'.egnyte.com'
        self._url_prefix = b'https://%s/' % domain
        self._session = requests.Session()
        if b'access_token' in self.config:
            self._session.headers[b'Authorization'] = b'Bearer %s' % self.config[b'access_token']
        if b'time_between_requests' in self.config:
            self.time_between_requests = config[b'time_between_requests']
        elif b'requests_per_second' in self.config:
            self.time_between_requests = 1.0 / float(self.config[b'requests_per_second'])

    def _respect_limits(self):
        if self.time_between_requests:
            if self.last_request_time is not None:
                since = time.time() - self.last_request_time
                if since < self.time_between_requests:
                    time.sleep(self.time_between_requests - since)
            self.last_request_time = time.time()
        return

    def _retry(self, func, *args, **kwargs):
        kwargs[b'timeout'] = int(self.config.get(b'timeout')) if self.config.get(b'timeout') is not None else DEFAULT_TIMEOUT
        while True:
            response = func(*args, **kwargs)
            if response.headers.get(b'x-mashery-error-code') == b'ERR_403_DEVELOPER_OVER_QPS':
                retry_after = float(response.headers.get(b'retry-after', b'1'))
                time.sleep(retry_after)
            else:
                return response

        return

    def GET(self, url, **kwargs):
        self._respect_limits()
        return self._retry(self._session.get, url, allow_redirects=False, **kwargs)

    def POST(self, url, json_data=None, **kwargs):
        self._respect_limits()
        if json_data is None:
            headers = {}
            data = kwargs.pop(b'data', None)
        else:
            headers = JSON_HEADERS
            data = json.dumps(json_data)
        if b'headers' in kwargs:
            headers.update(kwargs.pop(b'headers'))
        return self._retry(self._session.post, url, data=data, headers=headers, **kwargs)

    def PATCH(self, url, json_data=None, **kwargs):
        self._respect_limits()
        if json_data is None:
            headers = {}
            data = kwargs.pop(b'data', None)
        else:
            headers = JSON_HEADERS
            data = json.dumps(json_data)
        if b'headers' in kwargs:
            headers.update(kwargs.pop(b'headers'))
        return self._retry(self._session.patch, url, data=data, headers=headers, **kwargs)

    def DELETE(self, url, **kwargs):
        self._respect_limits()
        return self._retry(self._session.delete, url, **kwargs)

    def get_url(self, _path, **kwargs):
        if kwargs:
            kw = {k:encode_path(v) if isinstance(v, string_types) else str(v) for k, v in kwargs.items()}
            return self._url_prefix + _path % kw
        else:
            return self._url_prefix + _path

    def close(self):
        if hasattr(self, b'_session'):
            self._session.close()
            del self._session


class HasClient(object):
    """Base class for API wrappers and utils"""

    def __init__(self, _client, **kwargs):
        self._client = _client
        self.__dict__.update(kwargs)


class Resource(object):
    """Base wrapper for API resources (singular objects with specific URL)"""
    _lazy_attributes = ()
    _url_template = b''

    def __init__(self, _client, **kwargs):
        self._client = _client
        self.__dict__.update(kwargs)
        if b'_url' not in kwargs:
            self._url = self._client.get_url(self._url_template, **kwargs)

    def __getattr__(self, name):
        """If attribute is in _lazyAtrributes but we don't have it's value yet, fetch attributes from service."""
        if name in self._lazy_attributes:
            if name not in self.__dict__:
                self._fetch_attributes()
            if name in self.__dict__:
                return self.__dict__[name]
        raise AttributeError(self, name)

    def _update_attributes(self, json_dict):
        for key in self._lazy_attributes:
            if key in json_dict:
                self.__dict__[key] = json_dict[key]

    def _fetch_attributes(self):
        json = exc.default.check_json_response(self._client.GET(self._url))
        self._update_attributes(json)
        return json

    def check(self):
        """
        Check if this object exists in the cloud and current user has read permissions on it.
        Will raise an exception otherwise.
        """
        self._fetch_attributes()

    def __str__(self):
        return b'<%s: %s {%s} >' % (self.__class__.__name__, self._url, (b', ').join([ b'%s: %r' % (k, v) for k, v in sorted(self.__dict__.items()) if not k.startswith(b'_') ]))

    __repr__ = __str__

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        if isinstance(other, Resource):
            return self._client is other._client and self._url == other._url
        return NotImplemented

    def delete(self):
        exc.default.check_response(self._client.DELETE(self._url))


def get_access_token(config):
    session = Session(config)
    url = session.get_url(b'puboauth/token')
    data = dict(client_id=config[b'api_key'], username=config[b'login'], password=config[b'password'], grant_type=b'password')
    response = session.POST(url, data, headers={b'content-type': b'application/x-www-form-urlencoded'})
    return exc.default.check_json_response(response)[b'access_token']


class _FileChunk(object):
    """Wrapper for chunk of the file that also calculates SHA512 checksum while file is read"""

    def __init__(self, fp, start, size):
        self.fp = fp
        self.position = start
        self.left = self.size = size
        self.sha = hashlib.sha512()

    def read(self, size=None):
        if size is None or size > self.left:
            size = self.left
        result = self.fp.read(size)
        self.sha.update(result)
        self.left -= len(result)
        return result

    def rewind(self):
        self.fp.seek(self.position)
        self.left = self.size
        self.sha = hashlib.sha512()


def split_file_into_chunks(fp, file_size, chunk_size):
    """
    Split file-like object into sequence of file-like objects, each of
    those with size no greater than chunk_size bytes.
    Those are just wrappers to the original file-like objects. They should be fully
    read sequentially, and they cannot be used concurrently with
    the original object.
    """
    position = 0
    while position < file_size:
        yield _FileChunk(fp, position, min(chunk_size, file_size - position))
        position += chunk_size


def get_file_size(fp):
    """Get size of the file or length of a bytes object"""
    fp.seek(0, 2)
    size = fp.tell()
    fp.seek(0, 0)
    return size


def date_format(date):
    if isinstance(date, (datetime.datetime, datetime.date)):
        return date.strftime(b'%Y-%m-%d')
    else:
        return date


def encode_path(path):
    if isinstance(path, text_type):
        path = path.encode(b'utf-8')
    return quote(path, b'/')


class FileDownload(object):
    """
    Provides the file length and other metadata.
    Delegates reads to underlying request's response.
    """

    def __init__(self, response, file):
        self.response = response
        self.file = file
        self.closed = False

    def __len__(self):
        return int(self.response.headers[b'content-length'])

    def write_to(self, fp, progress_callback=None):
        """
        Copy data to a file, then close the source.
        Optional progress_callback should have the signature of ProgressCallbacks.download_progress
        """
        downloaded = 0
        with self:
            for chunk in self.iter_content():
                fp.write(chunk)
                if progress_callback is not None:
                    downloaded += len(chunk)
                    progress_callback(self.file, self.file.size, downloaded)

        return

    def save_to(self, path, progress_callback=None):
        """
        Create a new file and save the contents
        Optional progress_callback should have the signature of ProgressCallbacks.download_progress
        """
        with open(path, b'wb') as (fp):
            self.write_to(fp, progress_callback)

    def close(self):
        if not self.closed:
            self.response.close()

    def read(self, size=None, decode_content=True):
        """
        Wrap urllib3 response.
        size - How much of the content to read. If specified, caching is skipped because it doesn't make sense to cache partial content as the full response.
        decode_content - If True, will attempt to decode the body based on the 'content-encoding' header.
        """
        return self.response.raw.read(size, decode_content)

    def __iter__(self, **kwargs):
        """
        Iterate response body line by line.
        You can specify alternate delimiter with delimiter parameter.
        """
        return self.response.iter_lines(**kwargs)

    def iter_content(self, chunk_size=16384):
        return self.response.iter_content(chunk_size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


DEFAULT_EXCLUDES = fnmatch.translate(b'.*')
DEFAULT_EXCLUDES_RE = re.compile(DEFAULT_EXCLUDES).match

def make_excluded(excludes=None):
    if excludes is None:
        return DEFAULT_EXCLUDES_RE
    else:
        patterns = [
         DEFAULT_EXCLUDES]
        patterns.extend(fnmatch.translated(x) for x in excludes)
        return re.compile((b'|').join(patterns)).match


def generate_paths(roots, excludes=None):
    """
    Walk set of paths in local filesystem, and for each file and directory generate a tuple of
    (is directory, absolute path, path relative root used to get to that file)
    """
    excluded = make_excluded(excludes)
    for root in roots:
        base = os.path.basename(root)
        if not excluded(base):
            is_dir = os.path.isdir(root)
            yield (is_dir, root, base)
            if is_dir:
                prefix_len = len(os.path.dirname(root))
                for dirpath, dirnames, filenames in os.walk(root, topdown=True, followlinks=True):
                    relpath = dirpath[prefix_len:].strip(b'/')
                    for is_dir, names in ((False, filenames), (True, dirnames)):
                        for name in names:
                            if not excluded(name):
                                yield (
                                 is_dir, os.path.join(dirpath, name), b'%s/%s' % (relpath, name))


def filter_none_values(dict):
    """Return dictionary with values that are None filtered out"""
    return {k:v for k, v in dict.items() if v is not None if v is not None}


class ResultList(list):
    """
    List with additional attributes representing a partial list of objects that exist in the cloud.
    total_count: Count of all objects that exist.
    offset: Starting index of this slice of results.
    """

    def __init__(self, data, total_count, offset):
        super(ResultList, self).__init__(data)
        self.total_count = total_count
        self.offset = offset