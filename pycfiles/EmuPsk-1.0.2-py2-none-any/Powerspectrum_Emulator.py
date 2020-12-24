# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ht/PycharmProjects/THANN/Powerspectrum_Emulator.py
# Compiled at: 2019-11-19 18:10:57
import keras as ks
path = '/home/ht/Desktop/NN'
model = ks.models.load_model(path + '/EMuPk222.h5')

def pk_pred(params):
    pk_pred = model.predict(params)
    return pk_pred