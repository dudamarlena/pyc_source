# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marpel/Scrivania/github/Evaluation-Framework/evaluation_framework/abstract_evaluationManager.py
# Compiled at: 2020-01-21 09:44:15
from abc import abstractmethod

class AbstractEvaluationManager:

    def __init__(self, debugging_mode):
        super().__init__()

    @abstractmethod
    def initialize_vectors(self, vector_file, vec_size):
        pass

    @abstractmethod
    def run_tests_in_sequential(self, tasks, similarity_metric, top_k, analogy_function=None):
        pass

    @abstractmethod
    def run_tests_in_parallel(self, tasks, similarity_metric, top_k, analogy_function=None):
        pass

    @abstractmethod
    def create_result_directory(self):
        pass

    @abstractmethod
    def compare_with(self, compare_with):
        pass