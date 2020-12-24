# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spotsh/packageuploader.py
# Compiled at: 2011-02-23 06:44:21
import sys
from urlparse import urljoin, urlparse, urlsplit
import urllib2, os.path, socket
from email.Generator import _make_boundary
try:
    from json import loads, dumps
except:
    from simplejson import loads, dumps

def upload_package(client, pkg_path):
    upload_url = get_upload_url(client)
    result = upload(client, upload_url, pkg_path)
    return result


def get_upload_url(client):
    upload_url = client.get('/api/package/upload').read()
    return upload_url


def upload(client, upload_url, pkg_path):
    (content_type, prefix, suffix) = build_headers(os.path.basename(pkg_path))
    body_length = os.path.getsize(pkg_path)
    content_length = len(prefix) + body_length + len(suffix)
    url_parts = urlsplit(upload_url)
    client.connection.putrequest('POST', url_parts[2])
    client.connection.putheader('Content-Type', content_type)
    client.connection.putheader('Content-Length', content_length)
    client.connection.endheaders()
    client.connection.send(prefix)
    body_file = open(pkg_path)
    try:
        blocksize = 1024
        data = body_file.read(blocksize)
        while data:
            print '\rUploading: %2d%%...' % (body_file.tell() * 100 / body_length),
            sys.stdout.flush()
            client.connection.sock.sendall(data)
            data = body_file.read(blocksize)

    except socket.error, v:
        if v.args[0] == 32:
            client.connection.close()
        raise

    print '\rUpload completed.        '
    client.connection.send(suffix)
    response = client.connection.getresponse()
    if response.status == 200:
        return loads(response.read())
    if response.status in (302, 303):
        location = response.getheader('Location')
        return loads(urllib2.urlopen(location).read())
    raise Exception('Unknown return status: %s %s' % (response.status, response.reason))


def build_headers(filename, key_name='file'):
    boundary = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    PREFIX = []
    PREFIX.append('--' + boundary)
    PREFIX.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key_name, filename))
    PREFIX.append('Content-Type: %s' % 'application/octet-stream')
    PREFIX.append('')
    PREFIX.append('')
    SUFFIX = [
     '']
    SUFFIX.append('--' + boundary + '--')
    SUFFIX.append('')
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return (
     content_type, CRLF.join(PREFIX), CRLF.join(SUFFIX))