# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\yanglin\test/..\pybcs\httpc.py
# Compiled at: 2012-03-27 06:15:25
import urllib, urllib2, httplib, cookielib, os, re, sys, time, copy, logging, hmac, base64, hashlib, commands, mimetypes
from cStringIO import StringIO
from urlparse import urlparse
from common import shorten
logger = logging.getLogger('pyhttpclient')
READ_BODY_TO_MEMORY = 1048576
try:
    import pycurl
except:
    pass

def network(func):
    if not hasattr(func, 'attr'):
        func.attr = []
    func.attr += ['network']
    return func


class HTTPException(Exception):

    def __init__(self, resp, msg=None):
        Exception.__init__(self)
        self.resp = resp
        self.msg = msg

    def __str__(self):
        return 'HTTPExecption: ' + str(self.resp) + str(self.msg)


class FilePartReader:

    def __init__(self, fp, start, length):
        self.fp = fp
        self.fp.seek(start)
        self.length = length

    def read_callback(self, size):
        if self.length == 0:
            return ''
        if self.length > size:
            self.length -= size
            return self.fp.read(size)
        else:
            size = self.length
            self.length -= size
            return self.fp.read(size)

    def read_all(self):
        return self.read_callback(self.length)


class HTTPC:
    """ define the http client interface"""

    def __init__(self):
        pass

    def get(self, url, headers={}):
        raise NotImplementException()

    def head(self, url, headers={}):
        raise NotImplementException()

    def put(self, url, body='', headers={}):
        raise NotImplementException()

    def post(self, url, body='', headers={}):
        raise NotImplementException()

    def delete(self, url, headers={}):
        raise NotImplementException()

    def get_file(self, url, local_file, headers={}):
        raise NotImplementException()

    def put_file(self, url, local_file, headers={}):
        raise NotImplementException()

    def post_multipart(self, url, local_file, filename='file1', fields={}, headers={}):
        raise NotImplementException()

    def put_file_part(self, url, local_file, start, length, headers={}):
        raise NotImplementException()

    def _parse_resp_headers(self, resp_header):
        (status, header) = resp_header.split('\r\n\r\n')[(-2)].split('\r\n', 1)
        status = int(status.split(' ')[1])
        header = [ i.split(':', 1) for i in header.split('\r\n') ]
        header = [ i for i in header if len(i) > 1 ]
        header = [ [a.strip().lower(), b.strip()] for (a, b) in header ]
        return (
         status, dict(header))


class CurlHTTPC(HTTPC):
    """use linux curl command , just for debug """

    def __init__(self, tmp_dir='/tmp/pyhttpclient/'):
        self.tmp_dir = tmp_dir
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

    def get(self, url, headers={}):
        return self._curl('curl -X "GET" %s "%s" ' % (
         self._headers2txt(headers), url))

    def head(self, url, headers={}):
        return self._curl('curl -X "HEAD" %s "%s" ' % (
         self._headers2txt(headers), url))

    def put(self, url, body='', headers={}):
        body = body.replace('"', '\\"')
        return self._curl('curl -X "PUT" %s "%s" -d "%s"' % (
         self._headers2txt(headers), url, body))

    def post(self, url, body='', headers={}):
        return self._curl('curl -X "POST" %s "%s" -d "%s"' % (
         self._headers2txt(headers), url, body))

    def delete(self, url, headers={}):
        return self._curl('curl -X "DELETE" %s "%s" ' % (
         self._headers2txt(headers), url))

    def get_file(self, url, local_file, headers={}):
        return self._curl('curl -X "GET" %s  "%s" ' % (
         self._headers2txt(headers), url), local_file)

    def put_file(self, url, local_file, headers={}):
        return self._curl('curl -X "PUT" %s "%s" -T %s' % (
         self._headers2txt(headers), url, local_file))

    def put_file_part(self, url, local_file, start, length, headers={}):
        logger.warn('it is a tragedy to use `put_file_part` on curl, YoU NeeD pycurl installed! ')
        data = FilePartReader(open(local_file, 'rb'), start, length).read_all()
        tmp_file = self._random_tmp_file('file_part%d-%d' % (start, start + length))
        f = file(tmp_file, 'wb')
        f.write(data)
        f.close()
        return self._curl('curl -X "PUT" %s "%s" -T %s' % (
         self._headers2txt(headers), url, tmp_file))

    def post_multipart(self, url, local_file, filename='file1', fields={}, headers={}):
        post_info = (' ').join([ '-F "%s=%s"' % (k, urllib.quote(v)) for (k, v) in fields.items() ])
        if local_file:
            post_info += ' -F "%s=@%s" ' % (filename, local_file)
        return self._curl('curl -X "POST" %s %s "%s" ' % (
         self._headers2txt(headers), post_info, url))

    def _random_tmp_file(self, key):
        from datetime import datetime
        name = str(datetime.now())
        name = name.replace(' ', '_')
        name = name.replace(':', '_')
        name = name.replace('.', '_')
        return self.tmp_dir + key + name

    def _headers2txt(self, headers):
        return (' ').join([ ' -H "%s: %s" ' % (k, v) for (k, v) in headers.items() ])

    def _curl(self, cmd, body_file=None):
        try:
            rst = self._curl_ll(cmd, body_file)
            return rst
        except Exception, e:
            raise HTTPException('detail: ' + str(e))

    def _curl_ll(self, cmd, body_file=None):
        if not body_file:
            body_file = self._random_tmp_file('body')
        header_file = self._random_tmp_file('header')
        logger.info('%s -v > %s' % (cmd, body_file))
        cmd = cmd.replace('curl', 'curl > %s --dump-header %s -s' % (body_file, header_file))
        logger.debug(cmd)
        (exitstatus, outtext) = commands.getstatusoutput(cmd)
        errs = [1792]
        if exitstatus in errs:
            raise HTTPException(None, 'error on curl: (%s, %s) on %s' % (exitstatus, outtext, cmd))
        resp_header = file(header_file).read()
        resp_body_size = os.path.getsize(body_file)
        if resp_body_size < READ_BODY_TO_MEMORY:
            resp_body = file(body_file).read()
        else:
            resp_body = ''
        logger.debug(resp_header)
        logger.debug(shorten(resp_body, 80))
        (status, header) = self._parse_resp_headers(resp_header)
        rst = {'status': status, 'header': header, 
           'body': resp_body, 
           'body_size': resp_body_size, 
           'body_file': body_file}
        if status in (200, 206):
            return rst
        else:
            raise HTTPException(rst)
        return


class PyCurlHTTPC(HTTPC):

    def __init__(self, proxy=None, limit_rate=0):
        pass

    def get(self, url, headers={}):
        logger.info('pycurl -X GET "%s" ', url)
        self._init_curl('GET', url, headers)
        return self._do_request()

    def head(self, url, headers={}):
        logger.info('pycurl -X HEAD "%s" ', url)
        self._init_curl('HEAD', url, headers)
        return self._do_request()

    def delete(self, url, headers={}):
        logger.info('pycurl -X DELETE "%s" ', url)
        self._init_curl('DELETE', url, headers)
        return self._do_request()

    def get_file(self, url, local_file, headers={}):
        logger.info('pycurl -X GET "%s" > %s', url, local_file)
        self._init_curl('GET', url, headers, local_file)
        return self._do_request()

    def put(self, url, body='', headers={}):
        headers = copy.deepcopy(headers)
        logger.info('pycurl -X PUT -d "%s" "%s" ', shorten(body, 100), url)
        if not body:
            headersnew = {'Content-Length': '0'}
            headers.update(headersnew)
        self._init_curl('PUT', url, headers)
        req_buf = StringIO(body)
        self.c.setopt(pycurl.INFILESIZE, len(body))
        self.c.setopt(pycurl.READFUNCTION, req_buf.read)
        return self._do_request()

    def post(self, url, body='', headers={}, log=True):
        headers = copy.deepcopy(headers)
        if log:
            logger.info('pycurl -X POST "%s" ', url)
        headersnew = {'Content-Length': str(len(body))}
        headers.update(headersnew)
        self._init_curl('POST', url, headers)
        req_buf = StringIO(body)
        self.c.setopt(pycurl.READFUNCTION, req_buf.read)
        return self._do_request()

    def put_file(self, url, local_file, headers={}):
        logger.info('pycurl -X PUT -T"%s" "%s" ', local_file, url)
        self._init_curl('PUT', url, headers)
        filesize = os.path.getsize(local_file)
        self.c.setopt(pycurl.INFILESIZE, filesize)
        self.c.setopt(pycurl.INFILE, open(local_file))
        return self._do_request()

    def put_file_part(self, url, local_file, start, length, headers={}):
        logger.info('pycurl -X PUT -T"%s[%d->%d]" "%s" ', local_file, start, length, url)
        self._init_curl('PUT', url, headers)
        filesize = os.path.getsize(local_file)
        self.c.setopt(pycurl.INFILESIZE, length)
        self.c.setopt(pycurl.READFUNCTION, FilePartReader(open(local_file, 'rb'), start, length).read_callback)
        return self._do_request()

    def post_multipart(self, url, local_file, filename='file1', fields={}, headers={}):
        post_info = (' ').join([ '-F "%s=%s"' % (k, urllib.quote(v)) for (k, v) in fields.items() ])
        if local_file:
            post_info += ' -F "%s=@%s" ' % (filename, local_file)
        logger.info('pycurl -X POST %s "%s" ', post_info, url)
        self._init_curl('POST', url, headers)
        values = fields.items()
        if filename:
            values.append((filename, (pycurl.FORM_FILE, local_file)))
        self.c.setopt(pycurl.HTTPPOST, values)
        return self._do_request()

    def _do_request(self):
        self.c.perform()
        resp_header = self.c.resp_header_buf.getvalue()
        resp_body = self.c.resp_body_buf.getvalue()
        status = self.c.getinfo(pycurl.HTTP_CODE)
        (status, headers) = self._parse_resp_headers(resp_header)
        self.c.close()
        rst = {'status': status, 'header': headers, 
           'body': resp_body, 
           'body_file': self.c.resp_body_file}
        if status in (200, 206):
            return rst
        else:
            raise HTTPException(rst)

    def _init_curl(self, verb, url, headers, resp_body_file=None):
        self.c = pycurl.Curl()
        self.c.resp_header_buf = None
        self.c.resp_body_buf = None
        self.c.resp_body_file = None
        self.c.setopt(pycurl.DEBUGFUNCTION, self._curl_log)
        self.c.setopt(pycurl.VERBOSE, 1)
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 10)
        self.c.setopt(pycurl.SSL_VERIFYHOST, 0)
        self.c.setopt(pycurl.SSL_VERIFYPEER, 0)
        self.c.unsetopt(pycurl.CUSTOMREQUEST)
        if verb == 'GET':
            self.c.setopt(pycurl.HTTPGET, True)
        elif verb == 'PUT':
            self.c.setopt(pycurl.UPLOAD, True)
        elif verb == 'POST':
            self.c.setopt(pycurl.POST, True)
        elif verb == 'HEAD':
            self.c.setopt(pycurl.NOBODY, True)
        elif verb == 'DELETE':
            self.c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        else:
            raise KeyError('unknown verb ' + verb)
        self.c.setopt(pycurl.URL, url)
        if headers:
            headers = [ '%s: %s' % (k, v) for (k, v) in headers.items() ]
            self.c.setopt(pycurl.HTTPHEADER, headers)
        self.c.resp_header_buf = StringIO()
        self.c.resp_body_buf = StringIO()
        self.c.setopt(pycurl.HEADERFUNCTION, self.c.resp_header_buf.write)
        if resp_body_file:
            self.c.resp_body_file = resp_body_file
            f = file(resp_body_file, 'wb')
            self.c.setopt(pycurl.WRITEDATA, f)
        else:
            self.c.setopt(pycurl.WRITEFUNCTION, self.c.resp_body_buf.write)
        return

    def _curl_log(self, debug_type, debug_msg):
        curl_out = [
         pycurl.INFOTYPE_HEADER_OUT,
         pycurl.INFOTYPE_DATA_OUT,
         pycurl.INFOTYPE_SSL_DATA_OUT]
        curl_in = [pycurl.INFOTYPE_HEADER_IN,
         pycurl.INFOTYPE_DATA_IN,
         pycurl.INFOTYPE_SSL_DATA_IN]
        curl_info = [pycurl.INFOTYPE_TEXT]
        if debug_type in curl_out:
            logger.debug('> %s' % debug_msg.strip())
        elif debug_type in curl_in:
            logger.debug('< %s' % debug_msg.strip())
        else:
            logger.debug('I %s' % debug_msg.strip())


class HttplibHTTPC(HTTPC):

    def __init__(self):
        pass

    def request(self, verb, url, data, headers={}):
        response = self.send_request(verb, url, data, headers)
        if verb == 'HEAD':
            response.close()
            resp_body = ''
        else:
            resp_body = response.read()
        for (k, v) in response.getheaders():
            logger.debug('< %s: %s' % (k, v))

        logger.debug('< ' + shorten(data, 1024))
        rst = {'status': response.status, 'header': dict(response.getheaders()), 
           'body': resp_body, 
           'body_file': None}
        if response.status in (200, 206):
            return rst
        else:
            raise HTTPException(rst)
        return

    def send_request(self, verb, url, data, headers={}):
        logger.info('httplibcurl -X "%s" "%s" ', verb, url)
        for (k, v) in headers.items():
            logger.debug('> %s: %s' % (k, v))

        logger.debug('\n')
        logger.debug('> ' + shorten(data, 1024))
        o = urlparse(url)
        host = o.netloc
        path = o.path
        if o.query:
            path += '?'
            path += o.query
        if o.scheme == 'https':
            conn = httplib.HTTPSConnection(host)
        else:
            conn = httplib.HTTPConnection(host)
        conn.request(verb, path, data, headers)
        response = conn.getresponse()
        return response

    def get(self, url, headers={}):
        return self.request('GET', url, '', headers)

    def head(self, url, headers={}):
        return self.request('HEAD', url, '', headers)

    def put(self, url, body='', headers={}):
        headers = copy.deepcopy(headers)
        if 'Content-Length' not in headers:
            headers.update({'Content-Length': str(len(body))})
        return self.request('PUT', url, body, headers)

    def post(self, url, body='', headers={}):
        headers = copy.deepcopy(headers)
        if 'Content-Type' not in headers:
            headers.update({'Content-Type': 'application/octet-stream'})
        if 'Content-Length' not in headers:
            headers.update({'Content-Length': str(len(body))})
        return self.request('POST', url, body, headers)

    def delete(self, url, headers={}):
        return self.request('DELETE', url, '', headers)

    def get_file(self, url, local_file, headers={}):
        response = self.send_request('GET', url, '', headers)
        fout = open(local_file, 'wb')
        CHUNK = 262144
        while True:
            data = response.read(CHUNK)
            if not data:
                break
            fout.write(data)

        fout.close()
        rst = {'status': response.status, 'header': dict(response.getheaders()), 
           'body': None, 
           'body_file': local_file}
        if response.status in (200, 206):
            return rst
        else:
            raise HTTPException(rst)
        return

    def put_file(self, url, local_file, headers={}):
        return self.put(url, file(local_file).read(), headers)

    def post_multipart(self, url, local_file, filename='file1', fields={}, headers={}):
        headers = copy.deepcopy(headers)
        if local_file and filename:
            f = (
             filename, os.path.basename(local_file), open(local_file).read())
            f_list = [f]
        else:
            f_list = []
        (content_type, body) = encode_multipart_formdata(fields.items(), f_list)
        headersnew = {'Content-Type': content_type, 'Content-Length': str(len(body))}
        headers.update(headersnew)
        return self.post(url, body, headers)

    def put_file_part(self, url, local_file, start, length, headers={}):
        logger.warn('it is a tragedy to use `put_file_part` by httplib , YoU NeeD pycurl installed! ')
        data = FilePartReader(open(local_file, 'rb'), start, length).read_all()
        return self.put(url, data, headers)


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)

    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % _get_content_type(filename))
        L.append('')
        L.append(value)

    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return (content_type, body)


def _get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def select_best_httpc():
    import platform
    try:
        import pycurl
        logger.debug('use pycurl httpclient')
        return PyCurlHTTPC
    except:
        logger.debug('use httplib httpclient')
        return HttplibHTTPC


__all__ = [
 'network', 'HTTPException', 'CurlHTTPC', 'PyCurlHTTPC', 'HttplibHTTPC', 'select_best_httpc', 'logger']