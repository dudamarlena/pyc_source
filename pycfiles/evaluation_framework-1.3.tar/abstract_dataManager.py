# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marpel/Scrivania/github/Evaluation-Framework/evaluation_framework/abstract_dataManager.py
# Compiled at: 2020-01-21 09:44:15
from abc import abstractmethod

class AbstractDataManager:

    def __init__(self):
        super().__init__()

    @abstractmethod
    def inizialize_vectors(self, vector_file, vector_size):
        pass

    @abstractmethod
    def read_vector_file(self, filename, vector_size):
        pass

    @abstractmethod
    def read_file(self, task, filename, columns):
        pass

    @abstractmethod
    def intersect_vectors_goldStandard(self, vectors, vector_filename, vector_size, goldStandard_data, goldStandard_filename, column_key, column_score):
        pass