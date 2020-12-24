# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ppoteralski/PycharmProjects/sqlalchemy-stdimage/.venv/lib/python3.6/site-packages/flask_image_alchemy/storages/file.py
# Compiled at: 2017-02-20 04:45:46
# Size of source mod 2**32: 1034 bytes
from os import makedirs, remove
from os.path import exists, split
from flask_image_alchemy.storages.base import BaseStorage

class FileStorage(BaseStorage):
    MEDIA_PATH = ''

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.MEDIA_PATH = app.config.get('MEDIA_PATH', '')

    def _create_dir_if_needed(self, file_name):
        directory, _ = split(file_name)
        if directory:
            if not exists(directory):
                makedirs(directory)

    def read(self, file_name):
        with open(self.MEDIA_PATH + file_name, 'r') as (file):
            return file.read()

    def write(self, file_obj, file_name):
        full_path = self.MEDIA_PATH + file_name
        self._create_dir_if_needed(full_path)
        with open(full_path, 'wb+') as (file):
            file.write(file_obj.read())

    def delete(self, file_name):
        try:
            remove(self.MEDIA_PATH + file_name)
        except FileNotFoundError:
            pass