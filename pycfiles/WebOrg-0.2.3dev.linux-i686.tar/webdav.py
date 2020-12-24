# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/weborg/lib/fs/webdav.py
# Compiled at: 2011-07-12 22:16:02
import httplib, tempfile, base64, os

class FileSystem:

    def __init__(self, host, port, username, password, root):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.root = root

    def listdir(self, path):
        """Return a list of file paths"""
        conn = httplib.HTTPSConnection(self.host, self.port)
        conn.request('PROPFIND', os.path.join(self.root, path), '<?xml version="1.0" encoding="utf-8" ?><propfind xmlns="DAV:"><prop><displayname/></prop></propfind>', {'Authorization': 'Basic ' + base64.encodestring((':').join([self.username, self.password]))[:-1], 'Content-Type': 'application/xml; charset="utf-8"', 
           'Depth': '1'})
        r = conn.getresponse()
        print r.status, r.reason, r.read()

    def get(self, path):
        """Returns a temp file path"""
        conn = httplib.HTTPSConnection(self.host, self.port)
        conn.request('GET', os.path.join(self.root, path), '', {'Authorization': 'Basic ' + base64.encodestring((':').join([self.username, self.password]))[:-1]})
        r = conn.getresponse()
        temppath = tempfile.mkstemp(suffix='.org')[1]
        fd = open(temppath, 'w')
        fd.write(r.read())
        fd.close()
        conn.close()
        return temppath

    def put(self, path, temppath):
        fd = open(temppath, 'r')
        content = fd.read()
        fd.close()
        conn = httplib.HTTPSConnection(self.host, self.port)
        conn.request('PUT', os.path.join(self.root, path), content, {'Authorization': 'Basic ' + base64.encodestring((':').join([self.username, self.password]))[:-1], 'Content-Length': str(len(content))})
        r = conn.getresponse()
        conn.close()

    def rm(self, path):
        os.remove(path)


def test():
    fs = FileSystem(host='disk.swissdisk.com', port=443, username='gombiuda', password='1101010101', root='/gombiuda/')
    tp = fs.get('test.txt')
    print open(tp).read()
    fs.listdir('/')


if __name__ == '__main__':
    test()