# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marpel/Scrivania/github/Evaluation-Framework/evaluation_framework/manager.py
# Compiled at: 2020-01-21 09:44:15
import xml.etree.ElementTree as ET
from evaluation_framework.evaluationManager import EvaluationManager
from evaluation_framework.txt_dataManager import DataManager as TxtDataManager
from evaluation_framework.hdf5_dataManager import DataManager as Hdf5DataManager
available_tasks = [
 'Classification', 'Regression', 'Clustering',
 'DocumentSimilarity', 'EntityRelatedness', 'SemanticAnalogies']
available_file_formats = ['txt', 'hdf5']

class FrameworkManager:

    def __init__(self):
        print 'Start evaluation...'

    def evaluate(self, vector_filename, vector_file_format='txt', vector_size=200, parallel=False, tasks=available_tasks, similarity_metric='cosine', top_k=2, compare_with='_all', debugging_mode=False, analogy_function=None):
        self.vector_filename = vector_filename
        self.vector_file_format = vector_file_format
        self.vector_size = vector_size
        self.parallel = parallel
        self.tasks = tasks
        self.similarity_metric = similarity_metric
        self.analogy_function = analogy_function
        self.top_k = top_k
        self.compare_with = compare_with
        self.debugging_mode = debugging_mode
        self.check_parameters()
        if vector_file_format == 'txt':
            self.dataManager = TxtDataManager(self.debugging_mode)
        elif vector_file_format == 'hdf5':
            self.dataManager = Hdf5DataManager(self.debugging_mode)
        self.evaluation_manager = EvaluationManager(self.dataManager, self.debugging_mode)
        self.evaluation_manager.create_result_directory()
        self.evaluation_manager.initialize_vectors(vector_filename, vector_size)
        if parallel:
            scores_dictionary = self.evaluation_manager.run_tests_in_parallel(tasks, similarity_metric, top_k, analogy_function)
        else:
            scores_dictionary = self.evaluation_manager.run_tests_in_sequential(tasks, similarity_metric, top_k, analogy_function)
        self.evaluation_manager.compare_with(compare_with, scores_dictionary)

    def check_parameters(self):
        if self.vector_filename == None:
            raise Exception('The vector filename is a mandatory parameter.')
        if self.vector_file_format not in available_file_formats:
            raise Exception('Not supported file format. The managed file format are: ' + available_file_formats)
        if self.vector_size < 0:
            raise Exception('The vector size must be not negative.')
        if self.parallel != True and self.parallel != False:
            raise Exception('The parameter PARALLEL is boolean.')
        if self.tasks != '_all':
            for task in self.tasks:
                if task not in available_tasks:
                    raise Exception(task + ' is not a supported task. The managed tasks are ' + (', ').join(available_tasks) + " or '_all'.")

        if self.top_k < 0:
            raise Exception('The top_k value must be not negative.')
        if self.debugging_mode != True and self.debugging_mode != False:
            raise Exception('The parameter DEBUGGING_MODE is boolean.')
        return

    def get_parameters_xmlFile(self, xml_file):
        parameters_dict = {}
        tree = ET.parse(xml_file)
        root = tree.getroot()
        string_tags = [
         'vector_filename', 'vector_file_format', 'similarity_function']
        for tag in string_tags:
            actual_tag = root.find(tag)
            if actual_tag is not None:
                parameters_dict[tag] = actual_tag.text

        int_tags = [
         'vector_size', 'top_k']
        for tag in int_tags:
            actual_tag = root.find(tag)
            if actual_tag is not None:
                parameters_dict[tag] = int(actual_tag.text)

        boolean_tags = [
         'parallel', 'debugging_mode']
        for tag in boolean_tags:
            actual_tag = root.find(tag)
            if actual_tag is not None:
                parameters_dict[tag] = bool(actual_tag.text)

        tags = [
         'tasks', 'compare_with']
        for tag in tags:
            tag_values_list = []
            actual_tag_list = root.find(tag)
            if actual_tag_list is not None:
                for actual_tag in actual_tag_list.findall('value'):
                    tag_values_list.append(actual_tag.text)

                parameters_dict[tag] = tag_values_list

        return parameters_dict