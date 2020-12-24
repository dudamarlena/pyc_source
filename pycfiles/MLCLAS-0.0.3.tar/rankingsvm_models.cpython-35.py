# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/multi_label_classification/mlclas/svm/rankingsvm_models.py
# Compiled at: 2016-05-20 00:14:01
# Size of source mod 2**32: 1380 bytes


class AllLabelInfo:

    def __init__(self):
        self.eachProduct = []
        self.totalProduct = 0
        self.eachRange = []
        self.labels = []
        self.notLabels = []
        self.labelsNum = []
        self.notLabelsNum = []

    def append(self, label_array, not_array):
        self.labels.append(label_array)
        self.notLabels.append(not_array)
        self.labelsNum.append(len(label_array))
        self.notLabelsNum.append(len(not_array))
        new_index = self.totalProduct
        product = len(label_array) * len(not_array)
        self.eachRange.append((new_index, new_index + product))
        self.eachProduct.append(product)
        self.totalProduct += product

    def get_shape(self, index, elaborate=False):
        if elaborate is False:
            return (self.labelsNum[index], self.notLabelsNum[index])
        else:
            return (
             (
              self.labelsNum[index], self.notLabelsNum[index]), self.labels[index], self.notLabels[index])

    def get_range(self, index):
        return self.eachRange[index]

    def get_each_product(self, index):
        return self.eachProduct[index]