# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zbbert\bertmodel.py
# Compiled at: 2019-06-24 22:45:43
# Size of source mod 2**32: 2274 bytes
from kashgari.embeddings import BERTEmbedding
from kashgari.tasks.seq_labeling import BLSTMCRFModel
import os
os.environ['CUDA_VISIABLE_DEVICES'] = '0'
with open('C://Users//zhongbiao//Desktop//file//pk_bigadd_train.txt', 'rb') as (f):
    with open('C://Users//zhongbiao//Desktop//file//ProduceFromUuidAdd_test.txt', 'rb') as (validation):
        data = f.read().decode('utf-8')
        data2 = validation.read().decode('utf-8')
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

validate_data = data2.split('\r\n')
word2 = []
label2 = []
word_set2 = []
label_set2 = []
for i in validate_data:
    SP = i.split(' ')
    if len(SP) == 2:
        word2.append(SP[0])
        label2.append(SP[1])
    else:
        word_set2.append(word2)
        word2 = []
        label_set2.append(label2)
        label2 = []

model = BLSTMCRFModel.load_model('./Model_originalBIG3')
model.fit(word_set, label_set, epochs=10, batch_size=256)
model.save('./Model_originalBIGADD1')
model = BLSTMCRFModel.load_model('./Model_originalBIGADD1')
model.fit(word_set, label_set, epochs=10, batch_size=256)
model.save('./Model_originalBIGADD2')
model = BLSTMCRFModel.load_model('./Model_originalBIGADD2')
model.fit(word_set, label_set, epochs=10, batch_size=256)
model.save('./Model_originalBIGADD3')
model = BLSTMCRFModel.load_model('./Model_originalBIGADD3')
model.fit(word_set, label_set, epochs=10, batch_size=256)
model.save('./Model_originalBIGADD4')