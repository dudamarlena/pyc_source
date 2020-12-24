# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kevin/src/cdbcli/build/lib/cdbcli/environment.py
# Compiled at: 2016-07-14 23:26:52
import sys

class Environment(object):

    def __init__(self, current_db=None):
        self.current_db = current_db
        self.output_stream = sys.stdout

    def output(self, text):
        self.output_stream.write(text)
        self.output_stream.write('\n')
        self.output_stream.flush()