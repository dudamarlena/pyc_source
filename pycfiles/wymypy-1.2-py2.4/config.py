# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wymypy/libs/config.py
# Compiled at: 2007-01-27 04:38:58
import os, dict4ini

class Config(dict4ini.DictIni):
    __module__ = __name__
    file = '.wymypy'

    def __init__(self):
        file = os.path.join(os.path.expanduser('~'), Config.file)
        dict4ini.DictIni.__init__(self, file)
        if not os.path.isfile(file):
            self.makeDefault()

    def makeDefault(self):
        print 'Create config file, in home :', Config.file
        self.mpd.port = 6600
        self.mpd.host = 'localhost'
        self.server.port = 8080
        self.server.tagformat = '<b>%(artist)s</b> - %(title)s'
        self.save()


if __name__ == '__main__':
    pass