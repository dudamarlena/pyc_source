# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/core/HINMINE/IO.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 766 bytes
from .dataStructures import HeterogeneousInformationNetwork
import numpy as np

def load_hinmine_object(infile, label_delimiter='---', weight_tag=False, targets=True):
    net = infile
    hin = HeterogeneousInformationNetwork(net, label_delimiter, weight_tag, target_tag=targets)
    train_indices = []
    test_indices = []
    for index, node in enumerate(hin.node_list):
        if len(hin.graph.node[node]['labels']) > 0:
            train_indices.append(index)
        else:
            test_indices.append(index)

    hin.split_to_indices(train_indices=train_indices, test_indices=test_indices)
    if targets:
        hin.create_label_matrix()
    return hin