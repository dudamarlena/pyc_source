# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/storedoc/local.py
# Compiled at: 2019-08-12 00:59:01
# Size of source mod 2**32: 593 bytes
import os

class LocalStorage(object):

    def _get_filename(self, file):
        *_, filename = file.filename.split('/')
        return filename

    def save_file(self, file, folder=''):
        filename = self._get_filename(file)
        media_location = os.path.join(os.getcwd(), filename)
        if folder:
            if not os.path.exists(folder):
                os.mkdir(folder)
        if folder:
            media_location = os.path.join(os.path.abspath(os.path.join(os.getcwd(), folder)), filename)
        file.save(media_location)
        return media_location