# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aaronrusso/Alma Mater Studiorum Università di Bologna/Andrea Zanellini - Data Analysis/Workspace/Aaron/libraries development/ubm-python-libraries/ubm/acquisition/dataset/components/internal.py
# Compiled at: 2017-11-11 18:57:39
# Size of source mod 2**32: 640 bytes


class Temperatures:
    EXCHANGER_1 = 'TScamb1'
    EXCHANGER_2 = 'TScamb2'
    COOLER_1 = 'TCool1'
    COOLER_2 = 'TCool2'
    COOLER_3 = 'TCool3'

    def __init__(self, dataset):
        self.dataset = dataset

    def get_exchanger_1(self):
        return self.dataset.get_data()[self.EXCHANGER_1]

    def get_exchanger_2(self):
        return self.dataset.get_data()[self.EXCHANGER_2]

    def get_cooler_1(self):
        return self.dataset.get_data()[self.COOLER_1]

    def get_cooler_2(self):
        return self.dataset.get_data()[self.COOLER_2]

    def get_cooler_3(self):
        return self.dataset.get_data()[self.COOLER_3]