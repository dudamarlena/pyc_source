# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/util/cpio.py
# Compiled at: 2019-03-03 16:57:38
from pprint import pprint
import sys
from struct import unpack, pack
import os
ISDIR = 16384
ISFIFO = 4096
ISREG = 32768
ISBLK = 24576
ISCHR = 8192
ISCTG = 36864
ISLNK = 40960
ISOCK = 49152
IFMT = 61440
MODEMASK = 511
TRAILER = 'TRAILER!!!'
NEW_MAGIC = 29121
CRC_MAGIC = 29122
OLD_MAGIC = 29127

def version():
    return '0.1'


class CpioArchive(object):

    def __init__(self, cpiofile=None, fileobj=None, mode='rb'):
        if fileobj:
            self.ifile = fileobj
        else:
            self.ifile = open(cpiofile, mode)

    def is_cpiofile(self, cpiofile=None, fileobj=None):
        if fileobj:
            magic = int(fileobj.read(6), 8)
        else:
            magic = int(open(cpiofile, 'r').read(6), 8)
        if magic in [NEW_MAGIC, CRC_MAGIC, OLD_MAGIC]:
            return True

    def read_old_ascii_cpio_record(self):
        f = {}
        try:
            f['dev'] = int(self.ifile.read(6), 8)
            f['ino'] = int(self.ifile.read(6), 8)
            f['mode'] = int(self.ifile.read(6), 8)
            f['uid'] = int(self.ifile.read(6), 8)
            f['gid'] = int(self.ifile.read(6), 8)
            f['nlink'] = int(self.ifile.read(6), 8)
            f['rdev'] = int(self.ifile.read(6), 8)
            f['mtime'] = int(self.ifile.read(11), 8)
            f['namesize'] = int(self.ifile.read(6), 8)
            f['filesize'] = int(self.ifile.read(11), 8)
            f['name'] = self.ifile.read(f.get('namesize'))[:-1]
            f['data'] = self.ifile.read(f.get('filesize'))
        except:
            print 'ERROR: cpio record trunked (incomplete archive)'
            return

        return f

    def extract_files(self, files=None, outpath='.'):
        print 'Extracting files from CPIO archive'
        while 1:
            try:
                hdr = int(self.ifile.read(6), 8)
            except:
                print 'ERROR: cpio record trunked (incomplete archive)'
                break

            if hdr != OLD_MAGIC:
                raise NotImplementedError
            f = self.read_old_ascii_cpio_record()
            if f and f.get('name') == TRAILER:
                break
            if files:
                if f.get('name') not in files:
                    print 'Skipped %s' % f.get('name')
                    continue
            fullOutPath = os.path.join(outpath, f.get('name').strip('../'))
            print 'x %s' % fullOutPath
            if f.get('mode') & IFMT == ISFIFO:
                if not os.path.isdir(os.path.dirname(fullOutPath)):
                    os.makedirs(os.path.dirname(fullOutPath), 493)
                os.mkfifo(fullOutPath, f.get('mode') & MODEMASK)
                os.chmod(fullOutPath, f.get('mode') & MODEMASK)
            if f.get('mode') & IFMT == ISDIR:
                if not os.path.isdir(fullOutPath):
                    os.makedirs(fullOutPath, f.get('mode') & MODEMASK)
            if f.get('mode') & IFMT == ISBLK:
                raise NotImplementedError
            if f.get('mode') & IFMT == ISCHR:
                raise NotImplementedError
            if f.get('mode') & IFMT == ISLNK:
                raise NotImplementedError
            if f.get('mode') & IFMT == ISOCK:
                raise NotImplementedError
            if f.get('mode') & IFMT == ISCTG or f.get('mode') & IFMT == ISREG:
                if not os.path.isdir(os.path.dirname(fullOutPath)):
                    os.makedirs(os.path.dirname(fullOutPath), 493)
                fd = open(fullOutPath, 'wb')
                fd.write(f.get('data'))
            os.chmod(fullOutPath, f.get('mode') & MODEMASK)


if __name__ == '__main__':
    a = CpioArchive(sys.argv[1], mode='rb')
    a.extract_files()