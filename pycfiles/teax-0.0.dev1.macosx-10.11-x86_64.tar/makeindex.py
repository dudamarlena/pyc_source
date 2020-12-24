# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maciejczyzewski/teax/repository/teax/plugins/makeindex.py
# Compiled at: 2016-02-03 14:51:11
import os, subprocess
from teax.system.plugin import PluginObject, PluginFacade

@PluginFacade.register
class MakeindexPlugin(PluginObject):
    parseable_extensions = {'.idx'}

    def __init__(self, filename):
        self.filename = filename
        self.basename = os.path.splitext(os.path.basename(filename))[0]

    def start(self):
        subprocess.Popen('makeindex ' + self.basename, stdout=subprocess.PIPE, shell=True).communicate()[0]

    @classmethod
    def is_active(cls, path):
        for filename in next(os.walk(path))[2]:
            if filename.endswith(tuple(cls.parseable_extensions)):
                return True

        return False