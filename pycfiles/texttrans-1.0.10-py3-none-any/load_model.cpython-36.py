# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mitsuharu/Documents/GitHub/text-trans/data/load_model.py
# Compiled at: 2019-06-11 02:06:06
# Size of source mod 2**32: 240 bytes
import os, pickle
dir_path = os.path.abspath(os.path.dirname(__file__))
file_en = 'en.pki'
file_en_path = os.path.join(dir_path, file_en)

def model_en():
    model_data = pickle.load(open(file_en_path, 'rb'))
    return model_data