# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/util/filemixin.py
# Compiled at: 2012-02-27 07:41:58


class FileMixin(object):
    """
    Used to provide auxiliary methods to objects simulating files.
    Objects must implement write, and read if they are input files.
    Also they should implement close.

    Other methods you may wish to override:
    * flush()
    * seek(offset[, whence])
    * tell()
    * truncate([size])

    Attributes you may wish to provide:
    * closed
    * encoding (you should also respect that in write())
    * mode
    * newlines (hard to support)
    * softspace
    """

    def flush(self):
        pass

    def next(self):
        return self.readline()

    def readline(self, size=None):
        output = []
        while 1:
            next = self.read(1)
            if not next:
                return ('').join(output)
            output.append(next)
            if size and size > 0 and len(output) >= size:
                return ('').join(output)
            if next == '\n':
                return ('').join(output)

    def xreadlines(self):
        return self

    def writelines(self, lines):
        for line in lines:
            self.write(line)