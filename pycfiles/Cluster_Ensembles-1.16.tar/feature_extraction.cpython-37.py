# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/input_preprocess/feature_extraction.py
# Compiled at: 2019-06-11 07:56:19
# Size of source mod 2**32: 244 bytes


class FeatureExtractor(object):

    def __init__(self, files):
        self.files = files

    def retrieve_coords(self):
        return self._retrieve_coords()

    def retrieve_dihedrals(self):
        return self._retrieve_dihedrals()