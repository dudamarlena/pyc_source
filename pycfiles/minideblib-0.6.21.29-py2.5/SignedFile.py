# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/SignedFile.py
# Compiled at: 2007-11-06 15:08:00
import re, string

class SignedFile:
    _stream = None
    _eof = 0
    _signed = 0
    _signature = None
    _signatureversion = None
    _initline = None

    def __init__(self, stream):
        self._stream = stream
        line = stream.readline()
        if line == '-----BEGIN PGP SIGNED MESSAGE-----\n':
            self._signed = 1
            while 1:
                line = stream.readline()
                if len(line) == 0 or line == '\n':
                    break

        else:
            self._initline = line

    def readline(self):
        if self._eof:
            return ''
        if self._initline:
            line = self._initline
            self._initline = None
        else:
            line = self._stream.readline()
        if not self._signed:
            return line
        elif line == '-----BEGIN PGP SIGNATURE-----\n':
            self._eof = 1
            self._signature = []
            self._signatureversion = self._stream.readline()
            self._stream.readline()
            while 1:
                line = self._stream.readline()
                if len(line) == 0 or line == '-----END PGP SIGNATURE-----\n':
                    break
                self._signature.append(line)

            self._signature = string.join
            return ''
        return line

    def readlines(self):
        ret = []
        while 1:
            line = self.readline()
            if line != '':
                ret.append(line)
            else:
                break

        return ret

    def close(self):
        self._stream.close()

    def getSigned(self):
        return self._signed

    def getSignature(self):
        return self._signature

    def getSignatureVersion(self):
        return self._signatureversion


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 0:
        print 'Need one file as an argument'
        sys.exit(1)
    filename = sys.argv[1]
    f = SignedFile(open(filename))
    if f.getSigned():
        print '**** SIGNED ****'
    else:
        print '**** NOT SIGNED ****'
    lines = f.readlines()
    print lines
    if not f.getSigned():
        assert len(lines) == len(actuallines)
    else:
        print 'Signature: %s' % f.getSignature()