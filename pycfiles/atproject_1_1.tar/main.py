# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: att/Download/main.py
# Compiled at: 2017-03-18 10:25:16
from depend import run
import time, sys, os.path as path

class CustomLibrary:

    def __init__(self):
        self._torrent_path = ''
        self._download_path = ''

    @property
    def torrent_path(self):
        return self._torrent_path

    def torrent_path(self, value):
        self._torrent_path = value

    @property
    def download_path(self):
        return self._download_path

    def download_path(self, value):
        self._download_path = value

    def get(self):
        arguments = []
        arguments.append(self.torrent_path)
        run(arguments)