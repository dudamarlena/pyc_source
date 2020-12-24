# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maciejczyzewski/teax/repository/teax/engines/tex.py
# Compiled at: 2016-02-03 14:19:32
import os, subprocess
from teax.system.engine import EngineObject, EngineFacade

@EngineFacade.register
class TexEngine(EngineObject):
    parseable_extensions = {'.tex'}

    def __init__(self, filename):
        self.filename = filename

    def start(self):
        subprocess.Popen('tex ' + os.path.basename(self.filename), stdout=subprocess.PIPE, shell=True).communicate()[0]

    @classmethod
    def match(cls, filename, points=0):
        source = open(filename, 'rt').read()
        if filename.endswith(tuple(cls.parseable_extensions)):
            points += 1
        if '\\bye' in source:
            points += 1
        return points