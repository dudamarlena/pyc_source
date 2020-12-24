# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/biodb.py
# Compiled at: 2015-04-13 16:10:38
import urllib2 as urllib, os, os.path, config

def get_cachedir():
    return os.path.join(config.server_dir, 'dbcache/biodb/')


def addDBDir(handler):

    def wrap_handler(self, *args, **kwargs):
        return get_cachedir() + self.dbname + '/' + handler(self, *args, **kwargs)

    return wrap_handler


def validateID(handler):

    def wrap_handler(self, *args, **kwargs):
        if not self.isIDValid(args[0]):
            raise InvalidID()
        return handler(self, *args, **kwargs)

    return wrap_handler


class InvalidID(Exception):
    pass


class DBHandler:

    def isIDValid(self, val):
        return True

    def isFileValid(self, fh):
        return True

    @validateID
    @addDBDir
    def getFileLocation(self, val):
        return self.FileTemplate % val

    @validateID
    def getFileURL(self, val):
        return self.URLTemplate % val

    @validateID
    def downloadFile(self, val):
        try:
            u = urllib.urlopen(self.getFileURL(val))
        except urllib.HTTPError, e:
            if e.getcode() == 404:
                raise InvalidID()
            raise

        fname = self.getFileLocation(val)
        dirname = os.path.dirname(fname)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        buf = u.read()
        if not self.isFileValid(buf):
            raise InvalidID()
        localFile = open(self.getFileLocation(val), 'w')
        localFile.write(buf)
        localFile.close()

    @validateID
    def getFile(self, val):
        try:
            fh = open(self.getFileLocation(val), 'r')
        except:
            self.downloadFile(val)
            fh = open(self.getFileLocation(val), 'r')

        return fh


class SCOPHandler(DBHandler):

    def __init__(self):
        self.dbname = 'SCOP'
        self.URLTemplate = 'http://scop.berkeley.edu/astral/pdbstyle/ver=2.04&id=%s&output=file'

    def isIDValid(self, val):
        if len(val) != 7:
            return False
        if val[0] != 'd' or not val[1].isdigit() or not val[2:4].isalnum() or not (val[5].isalnum() or val[5] in ('_',
                                                                                                                  '.')) or not (val[6].isalnum() or val[6] == '_'):
            return False
        return True

    def isFileValid(self, buf):
        if buf.startswith('ERROR'):
            return False
        return True

    @validateID
    @addDBDir
    def getFileLocation(self, val):
        return '%s/%s.ent' % (val[2:4], val)


class PDBHandler(DBHandler):

    def __init__(self):
        self.dbname = 'PDB'
        self.URLTemplate = 'http://www.rcsb.org/pdb/files/%s.pdb'

    def isIDValid(self, val):
        if len(val) != 4:
            return False
        if not val[0].isdigit() or not val[1:3].isalnum():
            return False
        return True

    @validateID
    @addDBDir
    def getFileLocation(self, val):
        return '%s/%s.pdb' % (val[2:4], val)