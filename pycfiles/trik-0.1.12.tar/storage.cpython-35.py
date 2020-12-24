# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\trik\trik\yu\storage.py
# Compiled at: 2020-04-12 22:57:27
# Size of source mod 2**32: 223 bytes
import pickle

def save(file: str, thing):
    with open(file, 'wb') as (save_file):
        pickle.dump(thing, save_file)


def load(file: str):
    with open(file, 'rb') as (load_file):
        return pickle.load(load_file)