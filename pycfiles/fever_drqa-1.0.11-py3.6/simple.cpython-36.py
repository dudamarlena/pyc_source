# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqa/retriever/simple.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 385 bytes


class Simple(object):

    def __init__(self, lines):
        self.lines = lines

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def path(self):
        pass

    def get_doc_ids(self):
        return list(range(len(self.lines)))

    def get_doc_text(self, line):
        return self.lines[line]

    def close(self):
        pass