# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Павел\git\musket_all\musket_ml\examples\modules\datasets.py
# Compiled at: 2019-10-24 06:15:09
# Size of source mod 2**32: 877 bytes
from musket_core import datasets, genericcsv, coders, image_datasets

@datasets.dataset_provider(origin='train.csv', kind='GenericDataSet')
def getTitanic():
    return genericcsv.GenericCSVDataSet('train.csv', ['Sex', 'Fare', 'Age', 'Pclass'], ['Survived'], [], {'Sex':'binary', 
     'Fare':'normalized_number',  'Age':'normalized_number',  'Pclass':'one_hot',  'Survived':'binary'},
      input_groups={'0': ['Sex', 'Fare', 'Age', 'Pclass']})


@datasets.dataset_provider(origin='saltExists.csv', kind='BinaryClassificationDataSet')
def getSe():
    return image_datasets.BinaryClassificationDataSet(['images'], 'saltExists.csv', 'ImageId', 'Class')


@datasets.dataset_provider(origin='train.csv', kind='BinarySegmentationDataSet')
def getSaltTrain():
    return image_datasets.BinarySegmentationDataSet(['images', 'images'], 'salt.csv', 'id', 'rle_mask')