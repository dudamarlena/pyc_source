# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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