# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\storage.py
# Compiled at: 2016-04-08 05:23:51
# Size of source mod 2**32: 1392 bytes
from os import makedirs
from os.path import exists, dirname

class FileSystem:

    def open_input_stream(self, location):
        return open(location, 'r')

    def open_output_stream(self, location):
        if not exists(location):
            makedirs(dirname(location), exist_ok=True)
        return open(location, 'w')


class DataStorage:

    def __init__(self, parser, log, factory):
        self.parser = parser
        self.log = log
        self.report_factory = factory

    def model(self):
        return self.parser.parse()

    def log(self):
        return self.log

    def report_for(self, name, format):
        return self.report_factory(name, format)