# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/FileDropper.py
# Compiled at: 2009-06-23 05:16:10
"""Interact with FileDropper.com"""
import os.path, re, socket, urllib, urllib2
from types import StringTypes
from BeautifulSoup import BeautifulSoup
import poster.encode, poster.streaminghttp
FD_PERM_PUBLIC = 0
FD_PERM_PASSWORD = 1
FD_PERM_PRIVATE = 2
FD_URL = 'http://www.filedropper.com/'
FD_LOGIN_URL = FD_URL + 'login.php'
FD_PREMIUM_URL = FD_URL + 'premium.php'
FD_UPLOAD_URL = FD_URL + 'index.php?xml=true'
FD_PERM_URL = FD_PREMIUM_URL + '?action=setpermissions&%(varset)s&id=%(id)d'
FD_DELETE_URL = FD_PREMIUM_URL + '?action=delete&id=%d'
FD_MAX_SIZE = 5 * 1073741824
FD_ERROR_NOT_LOGGED_IN = 1
FD_ERROR_PERMISSIONS = 2
FD_ERROR_FILE_TOO_BIG = 3
FD_ERROR_UPLOAD = 4
FD_ERROR_INVALID_PASSWORD = 5
FD_ERROR_REQUEST = 6
FD_ERRORS = {FD_ERROR_NOT_LOGGED_IN: 'Not logged in', 
   FD_ERROR_PERMISSIONS: 'Invalid permissions', 
   FD_ERROR_FILE_TOO_BIG: 'File is too big', 
   FD_ERROR_UPLOAD: 'Error while uploading a file', 
   FD_ERROR_INVALID_PASSWORD: 'Invalid password', 
   FD_ERROR_REQUEST: 'Problem with the request'}
FD_RE_LIST = re.compile("^unhide\\('(\\d+)'\\)")

class FileDropperException(Exception):

    def __init__(self, errno):
        self.errno = errno
        self.errmsg = FD_ERRORS[errno]

    def __str__(self):
        return '[FileDropper error %d] %s' % (self.errno, self.errmsg)


upload_callback = None
psshc = poster.streaminghttp.StreamingHTTPConnection

class FileDropperHTTPConnection(psshc):

    def send(self, value):
        """Send ``value`` to the server.

        ``value`` can be a string object, a file-like object that supports
        a .read() method, or an iterable object that supports a .next()
        method.
        """
        if self.sock is None:
            if self.auto_open:
                self.connect()
            else:
                raise NotConnected()
        if self.debuglevel > 0:
            print 'send:', repr(value)
        try:
            blocksize = 8192
            total = -1
            try:
                total = len(value)
            except TypeError:
                pass

            sent = 0
            if hasattr(value, 'read'):
                if self.debuglevel > 0:
                    print 'sendIng a read()able'
                print 'sendIng a read()able'
                data = value.read(blocksize)
                while data:
                    self.sock.sendall(data)
                    sent += len(data)
                    if callable(upload_callback):
                        upload_callback(sent, total)
                    data = value.read(blocksize)

            if hasattr(value, 'next'):
                if self.debuglevel > 0:
                    print 'sendIng an iterable'
                print 'sendIng an iterable'
                for data in value:
                    self.sock.sendall(data)
                    sent += len(data)
                    if callable(upload_callback):
                        upload_callback(sent, total)

            else:
                self.sock.sendall(value)
                if callable(upload_callback):
                    upload_callback(total, total)
        except socket.error, v:
            if v[0] == 32:
                self.close()
            raise

        return


poster.streaminghttp.StreamingHTTPConnection = FileDropperHTTPConnection

class FileDropper:
    """Builds an empty FileDropper object that may be used for uploading files
    to FileDropper.com, get details about files in a premium account, change
    their permission or delete them."""

    def __init__(self):
        self.logged_in = False
        self.url = urllib2.build_opener(poster.streaminghttp.StreamingHTTPHandler, poster.streaminghttp.StreamingHTTPRedirectHandler, urllib2.HTTPCookieProcessor)

    def __del__(self):
        if self.logged_in:
            self.logout()

    def login(self, username, password):
        """Log into the premium account with the given username and password."""
        data = urllib.urlencode({'username': username, 'password': password})
        res = self.url.open(FD_LOGIN_URL, data)
        dst_url = res.geturl()
        self.logged_in = res.getcode() == 200 and dst_url == FD_PREMIUM_URL
        return self.logged_in

    def logout(self):
        """Log out from a premium account."""
        if not self.logged_in:
            raise FileDropperException(FD_ERROR_NOT_LOGGED_IN)
        self.url.open(FD_URL + 'login.php?action=logout')

    def list(self):
        """Get a list of files in the file manager of a premium account.

        The return value is a list of 7-value tuples of the form
        (file_name, id, downloads, size, date, permissions, public_url)"""
        if not self.logged_in:
            raise FileDropperException(FD_ERROR_NOT_LOGGED_IN)
        html = self.url.open(FD_PREMIUM_URL).read()
        soup = BeautifulSoup(html)
        tags = [ tag.parent for tag in soup.findAll('a', onclick=FD_RE_LIST) ]
        files = []
        for tag in tags:
            file_name = tag.a.string.strip()
            m = FD_RE_LIST.search(tag.a['onclick'])
            file_id = int(m.group(1))
            div = tag.div
            downloads = int(div.contents[2].replace('|', '').strip())
            size = div.contents[4].replace('|', '').strip()
            date = div.contents[6].replace('&nbsp;', '').strip()
            raw_perm = div.find('span', id='fileperms[%d]' % file_id)
            permissions = -1
            if raw_perm.span.string == 'Private':
                permissions = FD_PERM_PRIVATE
            elif raw_perm.span.string == 'Public':
                if raw_perm.b is not None:
                    permissions = FD_PERM_PUBLIC
                else:
                    permissions = FD_PERM_PASSWORD
            else:
                raise FileDropperException(FD_ERROR_PERMISSIONS)
            public_url = div.find('input', type='text')['value']
            value = (
             file_name, file_id, downloads, size, date, permissions, public_url)
            files.append(value)

        return files

    def upload(self, filename):
        """Upload the specified file"""
        if os.path.getsize(filename) > FD_MAX_SIZE:
            raise FileDropperException(FD_ERROR_FILE_TOO_BIG)
        base_name = os.path.basename(filename)
        mp1 = poster.encode.MultipartParam('Filename', base_name)
        mp2 = poster.encode.MultipartParam('file', filename=base_name, filetype='application/octet-stream', fileobj=open(filename))
        (data, headers) = poster.encode.multipart_encode([mp1, mp2])
        req = urllib2.Request(FD_UPLOAD_URL, data, headers)
        res = self.url.open(req)
        tmp_url = res.read()
        try:
            res = self.url.open(FD_URL + tmp_url[1:])
        except urllib2.HTTPError, exc:
            if exc.code == 404:
                return exc.geturl()
            raise exc

        raise FileDropperException(FD_ERROR_UPLOAD)

    def set_perm(self, file_id, perm, password=None):
        """Set new permissions for the specified file"""
        if not self.logged_in:
            raise FileDropperException(FD_ERROR_NOT_LOGGED_IN)
        query = {'id': file_id}
        if perm == FD_PERM_PUBLIC:
            query['varset'] = 'public=true'
            self.set_perm(file_id, FD_PERM_PRIVATE)
        elif perm == FD_PERM_PRIVATE:
            query['varset'] = 'private=true'
        elif perm == FD_PERM_PASSWORD:
            if type(password) not in StringTypes or password.strip() == '':
                raise FileDropperException(FD_ERROR_INVALID_PASSWORD)
            query['varset'] = urllib.urlencode({'password': password})
        else:
            raise FileDropperException(FD_ERROR_PERMISSIONS)
        url = FD_PERM_URL % query
        res = self.url.open(url)
        txt = res.read()
        if res.getcode() != 200:
            raise FileDropperException(FD_ERROR_REQUEST)
        return txt

    def delete(self, file_id):
        """Delete the specified file"""
        if not self.logged_in:
            raise FileDropperException(FD_ERROR_NOT_LOGGED_IN)
        res = self.url.open(FD_DELETE_URL % file_id)
        txt = res.read()
        if res.getcode() != 200:
            raise FileDropperException(FD_ERROR_REQUEST)
        return txt


if __name__ == '__main__':
    from getpass import getpass
    import sys
    fd = FileDropper()
    user = raw_input('Username: ')
    if user != '':
        password = getpass()
        if not fd.login(user, password):
            print 'Login failed'
    print 'Current files:'
    print fd.list()
    print
    uploaded_file = fd.upload('test.txt')
    print 'Upload: %s' % uploaded_file
    print
    print 'New files:'
    lst = fd.list()
    print lst
    file_id = -1
    for file_data in lst:
        if file_data[6] == uploaded_file:
            file_id = file_data[1]
            break

    if file_id == -1:
        print "Can't find file ID :-("
        sys.exit(1)
    print
    print 'Making the file private:'
    fd.set_perm(file_id, FD_PERM_PRIVATE)
    print fd.list()
    print
    print 'Making the file password-protected:'
    fd.set_perm(file_id, FD_PERM_PASSWORD, 'passtest')
    print fd.list()
    print
    print 'Making the file public again:'
    fd.set_perm(file_id, FD_PERM_PUBLIC)
    print fd.list()
    print
    print 'Making the file private again:'
    fd.set_perm(file_id, FD_PERM_PRIVATE)
    print fd.list()
    print
    print 'Deleting the file:'
    fd.delete(file_id)
    print fd.list()