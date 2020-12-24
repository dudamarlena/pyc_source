# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/gpk_hdr.py
# Compiled at: 2009-03-11 19:25:28
import os, re, die

def uq(s, qc):
    if qc and len(s) >= 2 and s[0] == qc and s[(-1)] == qc:
        return s[1:-1]
    return s


class hdr:
    _bad = re.compile('[^a-zA-Z_0-9.-]')

    def __init__(self, fn):
        self.fn = fn
        self.data = None
        self.modified = 0
        return

    def has_key(self, key):
        if self.data is None:
            self.read()
        return self.data.has_key(key)

    def items(self):
        if self.data is None:
            self.read()
        return self.data.items()

    def get(self, key, default=None, qc=None):
        if self.data is None:
            self.read()
        o = self.data.get(key, default)
        if qc:
            return uq(o, qc)
        else:
            return o

    def set(self, key, value, qc=None):
        if self.data is None:
            self.read()
        if self.has_key(key):
            self.data['#%s' % key] = self.data[key]
        if qc:
            self.data[key] = '%s%s%s' % (qc, value, qc)
        else:
            self.data[key] = value
        self.modified += 1
        return

    def __del__(self):
        self.close()

    def close(self):
        if not self.modified:
            return
        else:
            if self.data is None:
                return
            self.write()
            return

    def write(self):
        fd = open('%s.tmp' % self.fn, 'w')
        tmp = self.data.items()
        tmp.sort()
        for k, v in tmp:
            if self._bad.search(k) and not k.startswith('#'):
                die.warn('Bad key will be ignored: %s' % k)
            else:
                fd.writelines('%s=%s\n' % (k, v))

        fd.flush()
        os.fsync(fd.fileno())
        fd.close()
        if os.access(self.fn, os.R_OK):
            os.rename(self.fn, '%s.bak' % self.fn)
        os.rename('%s.tmp' % self.fn, self.fn)
        self.modified = 0

    def read(self):
        self.data = {'FILENAME': self.fn}
        die.note('file', self.fn)
        n = 1
        for x in open(self.fn, 'r'):
            die.note('line', n)
            x = x.strip()
            if x == '':
                n += 1
                continue
            try:
                k, v = x.split('=', 1)
                self.data[k] = v
            except:
                if not x.startswith('#'):
                    raise

            n += 1


if __name__ == '__main__':
    import sys
    x = hdr(sys.argv[1])
    x.set('TEST', 1, qc=1)
    x.write()