# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/TarIO.py
# Compiled at: 2007-09-25 20:00:35
import ContainerIO, string

class TarIO(ContainerIO.ContainerIO):

    def __init__(self, tarfile, file):
        fh = open(tarfile, 'rb')
        while 1:
            s = fh.read(512)
            if len(s) != 512:
                raise IOError, 'unexpected end of tar file'
            name = s[:100]
            i = string.find(name, chr(0))
            if i == 0:
                raise IOError, 'cannot find subfile'
            if i > 0:
                name = name[:i]
            size = string.atoi(s[124:136], 8)
            if file == name:
                break
            fh.seek(size + 511 & -512, 1)

        ContainerIO.ContainerIO.__init__(self, fh, fh.tell(), size)