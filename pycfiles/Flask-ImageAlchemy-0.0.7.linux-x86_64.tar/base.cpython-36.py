# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ppoteralski/PycharmProjects/sqlalchemy-stdimage/.venv/lib/python3.6/site-packages/flask_image_alchemy/storages/base.py
# Compiled at: 2017-02-15 11:02:06
# Size of source mod 2**32: 233 bytes
from abc import abstractmethod

class BaseStorage:

    @abstractmethod
    def read(self, file_name):
        pass

    @abstractmethod
    def write(self, data, file_name):
        pass

    @abstractmethod
    def delete(self, file_name):
        pass