# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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