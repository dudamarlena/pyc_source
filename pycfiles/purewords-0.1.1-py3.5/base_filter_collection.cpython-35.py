# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filter_collection/base_filter_collection.py
# Compiled at: 2018-08-07 00:27:49
# Size of source mod 2**32: 1082 bytes
"""base filter collection"""

class BaseFilterCollection(object):

    def __init__(self):
        self.filter_collection = []

    def add(self, filter_object):
        self.filter_collection.append(filter_object)

    def summary(self):
        for num, filter_object in enumerate(self.filter_collection):
            print('{}: {}'.format(num, str(filter_object)))

    def get_size(self):
        return len(self.filter_collection)

    @staticmethod
    def show_process(sentence, process, verbose):
        if verbose:
            if process == 'origin':
                print('====================================')
            print('({}) {}'.format(process, sentence))

    def __call__(self, sentence, verbose=False):
        BaseFilterCollection.show_process(sentence, 'origin', verbose)
        for num, filter_object in enumerate(self.filter_collection):
            sentence = filter_object(sentence)
            BaseFilterCollection.show_process(sentence, '{}_{}'.format(str(num), filter_object.__class__.__name__), verbose)

        return sentence