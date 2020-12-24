# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/MFCCFile.py
# Compiled at: 2008-03-29 07:06:06
import struct, sys, Numeric

class MFCCFile:

    def __init__(self, filename, DEBUG=0, BYTEORDER='@'):
        self.DEBUG = DEBUG
        self.BYTEORDER = BYTEORDER
        self.FileName = filename
        long_s = 4
        float_s = 4
        if not struct.pack('%sL' % self.BYTEORDER, 1) == struct.pack('L', 1):
            BYTESWAP = 1
        else:
            BYTESWAP = 0
        fp = open(filename, 'r')
        if DEBUG:
            sys.stderr.write('Opening file %s\n' % filename)
        str = fp.read(long_s)
        self.numSent = struct.unpack('%sL' % self.BYTEORDER, str)[0]
        if DEBUG:
            sys.stderr.write('    Number of sentences: %d\n' % self.numSent)
        str = fp.read(long_s)
        self.vecSize = struct.unpack('%sL' % self.BYTEORDER, str)[0]
        if DEBUG:
            sys.stderr.write('    Vector size: %d\n' % self.vecSize)
        self.sentLength = []
        for sent in range(self.numSent):
            str = fp.read(long_s)
            length = struct.unpack('%sL' % self.BYTEORDER, str)[0]
            self.sentLength.append(length)

        if DEBUG:
            sys.stderr.write('\n')
        self.sentList = []
        sentnum = 0
        index = 0
        veclength = self.vecSize * float_s
        if DEBUG:
            sys.stderr.write('    Loading sentences:')
        str = fp.read()
        for sent in range(self.numSent):
            if DEBUG:
                sys.stderr.write(' %d' % sent)
            sentdata = []
            for vec in range(self.sentLength[sent]):
                mfccvec = Numeric.fromstring(str[index:index + veclength], 'f')
                if BYTESWAP:
                    mfccvec = mfccvec.byteswapped()
                sentdata.append(mfccvec)
                index += veclength

            self.sentList.append(sentdata)

        fp.close()
        if DEBUG:
            sys.stderr.write('\n')

    def Save(self, filename):
        fh = open(filename, 'w')
        str = struct.pack('LL', self.numSent, self.vecSize)
        fh.write(str)
        for length in self.sentLength:
            str = struct.pack('L', length)
            fh.write(str)

        for utt in self.sentList:
            for vec in utt:
                str = vec.tostring()
                fh.write(str)

        fh.close()

    def ReturnSent(self, sentnum):
        return self.sentList[sentnum]

    def ReturnVector(self, sentnum, vecnum):
        return self.sentList[sentnum][vecnum]