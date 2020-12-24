# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\todopy\writer.py
# Compiled at: 2011-12-15 09:19:03
import codecs

class FileWriter(object):

    def __init__(self, filename):
        self.filename = filename

    def write(self, model):
        f = codecs.open(self.filename, mode='w', encoding='utf-8')
        for t in sorted(model, lambda x, y: cmp(x.id, y.id)):
            f.write(t.todo + '\n')