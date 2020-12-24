# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\trik\trik\yu\classification.py
# Compiled at: 2020-04-12 22:57:27
# Size of source mod 2**32: 535 bytes
import numpy

def generate_label_matrix(classification, default: int=0):
    index_map = {}
    index_reverse_map = {}
    index = 0
    for c in classification:
        if c not in index_map:
            index_map[c] = index
            index_reverse_map[index] = c
            index += 1

    dimension = len(index_map)
    class_matrix = default * numpy.ones([len(classification), dimension])
    for i, c in enumerate(classification):
        class_matrix[(i, index_map[c])] = 1

    return (
     class_matrix, index_map, index_reverse_map)