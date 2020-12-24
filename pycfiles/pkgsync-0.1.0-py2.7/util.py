# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pkgsync/util.py
# Compiled at: 2013-03-02 17:41:30


def name_version(dist_spec):
    if '==' in dist_spec:
        return dist_spec.split('==')
    else:
        return (
         dist_spec, None)


class FileLikeResponseAdapter(object):

    def __init__(self, response):
        self.response = response
        self._line_generator = None
        self._read_generator = None
        return

    def readline(self, size=1024):
        if not self._line_generator:
            self._line_generator = self.response.iter_lines(chunk_size=size)
        try:
            return self._line_generator.next() + '\n'
        except StopIteration:
            return

    def read(self, size=1024):
        if not self._read_generator:
            self._read_generator = self.response.iter_content(chunk_size=size)
        try:
            return self._read_generator.next()
        except StopIteration:
            return

    def __iter__(self):
        return self.response.iter_lines()