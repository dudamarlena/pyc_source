# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/flaker/urllib2_file.py
# Compiled at: 2009-05-23 12:15:04
"""
enable to upload files using multipart/form-data

idea from:
upload files in python:
 http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306

timeoutsocket.py: overriding Python socket API:
 http://www.timo-tasi.org/python/timeoutsocket.py
 http://mail.python.org/pipermail/python-announce-list/2001-December/001095.html

import urllib2_files
import urllib2
u = urllib2.urlopen('http://site.com/path' [, data])

data can be a mapping object or a sequence of two-elements tuples
(like in original urllib2.urlopen())
varname still need to be a string and
value can be string of a file object
eg:
  ((varname, value),
   (varname2, value),
  )
  or
  { name:  value,
    name2: value2
  }

"""
import os, socket, sys, stat, mimetypes, mimetools, httplib, urllib, urllib2
CHUNK_SIZE = 65536

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def send_data(v_vars, v_files, boundary, sock=None):
    l = 0
    for (k, v) in v_vars:
        buffer = ''
        buffer += '--%s\r\n' % boundary
        buffer += 'Content-Disposition: form-data; name="%s"\r\n' % k
        buffer += '\r\n'
        buffer += v + '\r\n'
        if sock:
            sock.send(buffer)
        l += len(buffer)

    for (k, v) in v_files:
        fd = v
        file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
        name = fd.name.split('/')[(-1)]
        if isinstance(name, unicode):
            name = name.encode('UTF-8')
        buffer = ''
        buffer += '--%s\r\n' % boundary
        buffer += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (
         k, name)
        buffer += 'Content-Type: %s\r\n' % get_content_type(name)
        buffer += 'Content-Length: %s\r\n' % file_size
        buffer += '\r\n'
        l += len(buffer)
        if sock:
            sock.send(buffer)
            if hasattr(fd, 'seek'):
                fd.seek(0)

    while True:
        chunk = fd.read(CHUNK_SIZE)
        if not chunk:
            break
        sock.send(chunk)
        l += file_size

    buffer = '\r\n'
    buffer += '--%s--\r\n' % boundary
    buffer += '\r\n'
    if sock:
        sock.send(buffer)
    l += len(buffer)
    return l


class newHTTPHandler(urllib2.BaseHandler):

    def http_open(self, req):
        return self.do_open(httplib.HTTP, req)

    def do_open(self, http_class, req):
        data = req.get_data()
        v_files = []
        v_vars = []
        if req.has_data() and type(data) != str:
            if hasattr(data, 'items'):
                data = data.items()
            else:
                try:
                    if len(data) and not isinstance(data[0], tuple):
                        raise TypeError
                except TypeError:
                    (ty, va, tb) = sys.exc_info()
                    raise TypeError, 'not a valid non-string sequence or mapping object', tb

                for (k, v) in data:
                    if hasattr(v, 'read'):
                        v_files.append((k, v))
                    else:
                        v_vars.append((k, v))

        if len(v_vars) > 0 and len(v_files) == 0:
            data = urllib.urlencode(v_vars)
            v_files = []
            v_vars = []
        host = req.get_host()
        if not host:
            raise urllib2.URLError('no host given')
        h = http_class(host)
        if req.has_data():
            h.putrequest('POST', req.get_selector())
            if 'Content-type' not in req.headers:
                if len(v_files) > 0:
                    boundary = mimetools.choose_boundary()
                    l = send_data(v_vars, v_files, boundary)
                    h.putheader('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
                    h.putheader('Content-length', str(l))
                else:
                    h.putheader('Content-type', 'application/x-www-form-urlencoded')
                    if 'Content-length' not in req.headers:
                        h.putheader('Content-length', '%d' % len(data))
        else:
            h.putrequest('GET', req.get_selector())
        (scheme, sel) = urllib.splittype(req.get_selector())
        (sel_host, sel_path) = urllib.splithost(sel)
        h.putheader('Host', sel_host or host)
        for (name, value) in self.parent.addheaders:
            name = name.capitalize()
            if name not in req.headers:
                h.putheader(name, value)

        for (k, v) in req.headers.items():
            h.putheader(k, v)

        try:
            h.endheaders()
        except socket.error, err:
            raise urllib2.URLError(err)

        if req.has_data():
            if len(v_files) > 0:
                l = send_data(v_vars, v_files, boundary, h)
            elif len(v_vars) > 0:
                data = urllib.urlencode(v_vars)
                h.send(data)
            else:
                h.send(data)
        (code, msg, hdrs) = h.getreply()
        fp = h.getfile()
        if code == 200:
            resp = urllib.addinfourl(fp, hdrs, req.get_full_url())
            resp.code = code
            resp.msg = msg
            return resp
        else:
            return self.parent.error('http', req, fp, code, msg, hdrs)


urllib2._old_HTTPHandler = urllib2.HTTPHandler
urllib2.HTTPHandler = newHTTPHandler

class newHTTPSHandler(newHTTPHandler):

    def https_open(self, req):
        return self.do_open(httplib.HTTPS, req)


urllib2.HTTPSHandler = newHTTPSHandler
if __name__ == '__main__':
    import getopt, urllib2, urllib2_file, string, sys

    def usage(progname):
        print '\nSYNTAX: %s -u url -f file [-v]\n' % progname


    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hvu:f:')
    except getopt.GetoptError, errmsg:
        print 'ERROR:', errmsg
        sys.exit(1)
    else:
        v_url = ''
        v_verbose = 0
        v_file = ''
        for (name, value) in opts:
            if name in ('-h', ):
                usage(sys.argv[0])
                sys.exit(0)
            elif name in ('-v', ):
                v_verbose += 1
            elif name in ('-u', ):
                v_url = value
            elif name in ('-f', ):
                v_file = value
            else:
                print 'invalid argument:', name
                sys.exit(2)

        error = 0
        if v_url == '':
            print 'need -u'
            error += 1
        if v_file == '':
            print 'need -f'
            error += 1
        if error > 0:
            sys.exit(3)
        fd = open(v_file, 'r')
        data = {'filename': fd}
        req = urllib2.Request(v_url, data, {})
        try:
            u = urllib2.urlopen(req)
        except urllib2.HTTPError, errobj:
            print 'HTTPError:', errobj.code
        else:
            buf = u.read()
            print 'OK'