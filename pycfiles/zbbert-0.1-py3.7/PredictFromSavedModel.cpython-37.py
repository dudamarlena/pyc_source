# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zbbert\PredictFromSavedModel.py
# Compiled at: 2019-06-05 03:31:51
# Size of source mod 2**32: 872 bytes
from kashgari.tasks.seq_labeling import BLSTMCRFModel
from TextProcess import pause
new_model = BLSTMCRFModel.load_model('./ModelTest')

def textprocess(string):
    ReList = []
    for i in string:
        ReList.append(i)

    return ReList


with open('C://Users//zhongbiao//Desktop//file//ProduceFromUuid_test.txt', 'rb') as (f):
    data = f.read().decode('utf-8')
train_data = data.split('\r\n')
word = []
label = []
word_set = []
label_set = []
for i in train_data:
    SP = i.split(' ')
    if len(SP) == 2:
        word.append(SP[0])
        label.append(SP[1])
    else:
        word_set.append(word)
        word = []
        label_set.append(label)
        label = []

new_model.evaluate(word_set, label_set)