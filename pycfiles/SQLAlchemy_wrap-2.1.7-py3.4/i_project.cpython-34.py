# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SQLAlchemy_wrap\interfaces\i_project.py
# Compiled at: 2019-08-20 12:27:39
# Size of source mod 2**32: 1270 bytes
import typing
from abc import abstractmethod
from .i_table import ITable

class IProject(ITable):

    @abstractmethod
    def update_or_insert(self, sample_id: str, content: dict):
        """
            if the current sample id is exists, it will update. otherwise insert new record
        :param sample_id:
        :param content: the content you want to insert
        :return:
        """
        pass

    @abstractmethod
    def get_by_sample_id(self, sample_id: str) -> dict:
        """
        :param sample_id: current project sample id
        :return: if the sample_id is exists, the dict that contain current project data,
                 like "{'small_data':"small_data_value',....}", otherwise return {}
        """
        pass

    @abstractmethod
    def remove_by_sample_id(self, sample_id: str):
        pass

    @abstractmethod
    def insert_by_sample_id(self, sample_id: str, content: dict):
        pass

    @abstractmethod
    def sample_id_exists(self, sample_id: str) -> bool:
        pass

    @abstractmethod
    def search(self, sample_id: str=0, operator: str='', started: str='', finished: str='',
               fields: typing.List[str]=None) -> typing.List[dict]:
        pass