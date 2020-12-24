# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\throwbin\PasteModel.py
# Compiled at: 2020-01-25 11:10:03
# Size of source mod 2**32: 166 bytes


class PasteModel:

    def __init__(self, status: str, id: str):
        self.status = status
        self.id = id
        self.link = 'http://throwbin.io/' + id