# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanghunkang/dev/aascraw/venv/lib/python3.7/site-packages/aascraw/storage.py
# Compiled at: 2019-08-27 10:45:41
# Size of source mod 2**32: 5314 bytes
import numpy as np

def recurse(prefix, matrix, index):
    if index < len(matrix):
        candidate_tuples = []
        for candidate in matrix[index]:
            candidate_tuples = candidate_tuples + recurse(prefix + [candidate], matrix, index + 1)

    else:
        candidate_tuples = [
         prefix]
    return candidate_tuples


class Storage:

    def __init__(self, schema_length, consistency_embedding_length, use_default_kernels):
        self.records = []
        self.element_kernels = []
        self.tuple_kernels = []
        self._Storage__schema_length = schema_length
        self._Storage__consistency_embedding_length = consistency_embedding_length
        self.count = 1
        self.maximum_rank_delta = 1
        if use_default_kernels == True:
            for i in range(self._Storage__schema_length):
                self.add_element_kernel(SOME_KERNEL, i)

            self.add_tuple_kernel(SOME_KERNEL)

    def __calculate_elementwise_rank(self, records_being_evaluated):
        existing_records = self._Storage__sample_existing_records()
        for record_being_evaluated in records_being_evaluated:
            elementwise_rank = np.zeros(self._Storage__schema_length)
            for kernel, element_id in self.element_kernels:
                elementwise_rank += kernel(record_being_evaluated, existing_records, element_id, self._Storage__schema_length)

            record_being_evaluated['rank_delta'] = elementwise_rank

        return records_being_evaluated

    def __calculate_tuplewise_rank(self, tuple_sample, results):
        tuplewise_rank_delta = np.zeros(self._Storage__consistency_embedding_length)
        existing_records = self._Storage__sample_existing_records()
        for xpath_set in tuple_sample:
            for kernel in self.tuple_kernels:
                tuplewise_rank_delta += kernel(xpath_set, existing_records)

        return tuplewise_rank_delta

    def __sample_tuple(self, records):
        sample_size = 5
        tuple_sample = []
        for i in range(self._Storage__schema_length):
            records_sorted_by_rank_delta = sorted(records, key=(lambda x: x['rank_delta'][i]))
            candidates_for_schema_i = records_sorted_by_rank_delta[:sample_size]
            tuple_sample.append(candidates_for_schema_i)

        result = recurse([], tuple_sample, 0)
        return result

    def __sample_existing_records(self):
        return self.records

    def add_sample_data(self, sample_data, real_data=False):
        for sample_record in sample_data:
            for i, element in enumerate(sample_record):
                record = {'deliverer_action':'HREF::SAMPLE_ACTION', 
                 'filterer_action':'SAMPLE_ACTION', 
                 'crawled_data':element, 
                 'index':i, 
                 'rank_delta':self.maximum_rank_delta}
                self.records.append(record)

    def add_element_kernel(self, kernel, element_index):
        self.element_kernels.append((kernel, element_index))

    def add_tuple_kernel(self, kernel):
        self.tuple_kernels.append(kernel)

    def evaluate_results(self, results, will_save=True):
        results = self._Storage__calculate_elementwise_rank(results)
        tuple_sample = self._Storage__sample_tuple(results)
        self._Storage__calculate_tuplewise_rank(tuple_sample, results)

    def get_rank_delta(self):
        return ([], [])