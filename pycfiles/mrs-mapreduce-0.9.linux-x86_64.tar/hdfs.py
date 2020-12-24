# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amcnabb/python/mrs/hdfs.py
# Compiled at: 2012-10-17 16:08:11
"""Connect to a Hadoop Distributed File System (HDFS) server over WebHDFS.

The low-level API is implemented as functions of the form:
    hdfs_operation(server, username, path, **args)
The `server` is of the form 'addr:port' (where the port defaults to
`DEFAULT_PORT`).  The low-level API is a thin wrapper around the protocol
specification defined at:
    http://hadoop.apache.org/common/docs/r1.0.0/webhdfs.html

Assumes that authentication is disabled on the server (it believes whatever
username you give).  All paths must be absolute, but you can call
`hdfs_get_home_directory` to help interpret your own relative URLs.

There are a few reasons that we don't use a proxy-style class as in RPC, etc.
First, WebHDFS does not seem to support persistent HTTP connections.  Second,
even if it did, it would still be hard to manage persistent HTTP connections
in conjunction with a higher-level API that can read a file in chunks.  Third,
in practice, these often get called one at a time and in different spots, so
the proxy object would be created unnecessarily over and over.
"""
from __future__ import division
import getpass, json, urllib
try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    import urlparse
    from urllib import quote
    from urllib import urlencode
except ImportError:
    import urllib.parse as urlparse
    from urllib.parse import quote
    from urllib.parse import urlencode

DEFAULT_PORT = 50070

def urlsplit(url):
    """Split an HDFS URL into a (server, username, path) tuple.

    If the URL's scheme is not 'hdfs', returns None.
    """
    fields = urlparse.urlsplit(url)
    if fields.scheme != 'hdfs':
        return None
    else:
        if fields.port:
            server = (':').join((fields.hostname, fields.port))
        else:
            server = fields.hostname
        if fields.username:
            username = fields.username
        else:
            username = getpass.getuser()
        return (
         server, username, fields.path)


def hdfs_open(server, username, path, **args):
    """Read a file.

    Returns a filelike object (specifically, an httplib response object).
    """
    datanode_url = datanode_url(server, username, path, **args)
    response = _datanode_request(server, username, 'GET', datanode_url)
    if response.status == httplib.OK:
        return response
    content = response.read()
    _raise_error(response.status, content)


def datanode_url(server, username, path, **args):
    """Finds the URL on the datanode associated with an HDFS path."""
    response = _namenode_request(server, username, 'GET', path, 'OPEN', args)
    content = response.read()
    _check_code(response.status, content, httplib.TEMPORARY_REDIRECT)
    datanode_url = response.getheader('Location')
    return datanode_url


def hdfs_get_home_directory(server, username):
    """Returns the path to the home directory of the configured user."""
    response = _namenode_request(server, username, 'GET', '/', 'GETHOMEDIRECTORY')
    content = response.read()
    _check_code(response.status, content)
    path_json = json.loads(content)
    homedir = path_json['Path']
    return homedir


def hdfs_get_file_status(server, username, path):
    """List a directory.

    Returns a dictionaries which contains the keys "accessTime",
    "blockSize", "group", "length", "modificationTime", "owner",
    "pathSuffix", "permission", "replication", and "type".
    """
    response = _namenode_request(server, username, 'GET', path, 'GETFILESTATUS')
    content = response.read()
    _check_code(response.status, content)
    filestatuses_json = json.loads(content)
    return filestatuses_json['FileStatus']


def hdfs_list_status(server, username, path):
    """List a directory.

    Returns a list of dictionaries, one for each file.  Each dictionary
    includes the keys "accessTime", "blockSize", "group", "length",
    "modificationTime", "owner", "pathSuffix", "permission",
    "replication", and "type".
    """
    response = _namenode_request(server, username, 'GET', path, 'LISTSTATUS')
    content = response.read()
    _check_code(response.status, content)
    filestatuses_json = json.loads(content)
    return filestatuses_json['FileStatuses']['FileStatus']


def hdfs_get_contents_summary(server, username, path):
    """Get content summary of a directory.

    Returns a dictionary containing the keys "directoryCount",
    "fileCount", "length", "quota", "spaceConsumed", and "spaceQuota".
    """
    response = _namenode_request(server, username, 'GET', path, 'LISTSTATUS')
    content = response.read()
    _check_code(response.status, content)
    filestatuses_json = json.loads(content)
    return filestatuses_json['FileStatuses']['FileStatus']


def hdfs_create(server, username, path, data, **args):
    """Create and write to a file.

    The `data` parameter can be either a string or a file (but not necessarily
    a filelike in general--it needs to define either `__len__()` or
    `fileno()`.
    """
    response = _namenode_request(server, username, 'PUT', path, 'CREATE', args)
    content = response.read()
    _check_code(response.status, content, httplib.TEMPORARY_REDIRECT)
    datanode_url = response.getheader('Location')
    response = _datanode_request(server, username, 'PUT', datanode_url, data)
    content = response.read()
    _check_code(response.status, content, httplib.CREATED)


def hdfs_append(server, username, path, data, **args):
    """Append to a file.

    Note that the HDFS server may or may not support appending.  The `data`
    parameter can be either a string or a file (but not necessarily a filelike
    in general--it needs to define either `__len__()` or `fileno()`.
    """
    response = _namenode_request(server, username, 'PUT', path, 'APPEND', args)
    response.read()
    _check_code(response.status, content, httplib.TEMPORARY_REDIRECT)
    datanode_url = response.getheader('Location')
    response = _datanode_request(server, username, 'PUT', datanode_url, data)
    content = response.read()
    _check_code(response.status, content, httplib.OK)


def hdfs_mkdirs(server, username, path, **args):
    """Make a directory."""
    response = _namenode_request(server, username, 'PUT', path, 'MKDIRS', args)
    content = response.read()
    _check_code(response.status, content)
    boolean_json = json.loads(content)
    return boolean_json['boolean']


def hdfs_rename(server, username, path1, path2):
    """Rename a file or directory."""
    response = _namenode_request(server, username, 'PUT', path, 'RENAME', {'destination': path2})
    content = response.read()
    _check_code(response.status, content)
    boolean_json = json.loads(content)
    return boolean_json['boolean']


def hdfs_delete(server, username, path, **args):
    """Make a directory."""
    response = _namenode_request(server, username, 'DELETE', path, 'DELETE', args)
    content = response.read()
    _check_code(response.status, content)
    boolean_json = json.loads(content)
    return boolean_json['boolean']


def hdfs_set_permission(server, username, path, **args):
    """Set permissions of a file or directory."""
    response = _namenode_request(server, username, 'PUT', path, 'SETPERMISSION', args)
    content = response.read()
    _check_code(response.status, content)


def hdfs_set_owner(server, username, path, **args):
    """Set the owner of a file or directory."""
    response = _namenode_request(server, username, 'PUT', path, 'SETOWNER', args)
    content = response.read()
    _check_code(response.status, content)


def _namenode_conn(server):
    """Make and return a new http connection to the namenode."""
    fields = server.split(':')
    addr = fields[0]
    if len(fields) == 1:
        port = DEFAULT_PORT
    else:
        port = fields[1]
    return httplib.HTTPConnection(addr, port)


def _namenode_request(server, username, method, path, op, args=None, body=None):
    """Send a PUT request to the namenode.

    Returns the HTTPResponse object, which is filelike. Note that this
    response object must be fully read before beginning to read any
    subsequent response.
    """
    request_uri = _request_uri(server, username, path, op, args)
    namenode_conn = _namenode_conn(server)
    namenode_conn.request(method, request_uri, body)
    response = namenode_conn.getresponse()
    return response


def _datanode_request(server, username, method, url, body=None):
    """Send a PUT request to the datanode.

    Returns the HTTPResponse object, which is filelike. Note that this
    response object must be fully read before beginning to read any
    subsequent response.
    """
    host = urlparse.urlsplit(url)[1]
    datanode_conn = httplib.HTTPConnection(host)
    datanode_conn.request(method, url, body)
    response = datanode_conn.getresponse()
    return response


def _request_uri(server, username, path, op, args=None):
    """Builds a webhdfs request URI from a path, operation, and args.

    The `args` argument is a dictionary used to construct the query. All
    parts of the resulting request URI are properly quoted.
    """
    assert path.startswith('/')
    quoted_path = quote('/webhdfs/v1' + path)
    query = {'op': op, 'user.name': username}
    if args:
        query.update(args)
    quoted_query = urlencode(query)
    request_uri = '%s?%s' % (quoted_path, quoted_query)
    return request_uri


class IllegalArgumentException(Exception):
    pass


class SecurityException(Exception):
    pass


class IOException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


exceptions = {400: IllegalArgumentException, 401: SecurityException, 
   403: IOException, 
   404: FileNotFoundException}

def _check_code(code, content, expected_code=httplib.OK):
    """Raise a remote exception if necessary."""
    if code == expected_code:
        return
    _raise_error(code, content)


def _raise_error(code, content):
    """Raise a remote exception."""
    try:
        exception_cls = exceptions[code]
    except KeyError:
        raise RuntimeError('Unknown webhdfs error code: %s' % code)

    exception_json = json.loads(content)
    message = exception_json['RemoteException']['message']
    raise exception_cls(message)