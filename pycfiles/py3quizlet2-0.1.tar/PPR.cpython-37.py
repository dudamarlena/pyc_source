# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/network_classification/PPR.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 4584 bytes
from ..node_ranking import *
from ..general.benchmark_classification import *
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import f1_score
import time, numpy as np, multiprocessing as mp
from sklearn.model_selection import StratifiedKFold, StratifiedShuffleSplit
from sklearn import preprocessing

def construct_PPR_matrix(graph_matrix, parallel=False):
    """
    PPR matrix is the matrix of features used for classification --- this is the spatially intense version of the classifier
    """
    n = graph_matrix.shape[1]
    vectors = np.zeros((n, n))
    results = run_PPR(graph_matrix, parallel=parallel)
    for result in results:
        if result != None:
            if isinstance(result, list):
                for ppr in result:
                    vectors[ppr[0], :] = ppr[1]

            else:
                ppr = result
                vectors[ppr[0], :] = ppr[1]

    return vectors


def construct_PPR_matrix_targets(graph_matrix, targets, parallel=False):
    n = graph_matrix.shape[1]
    vectors = np.empty((len(targets), n))
    tar_map = dict(zip(targets, range(len(targets))))
    results = run_PPR(graph_matrix, targets=targets, parallel=parallel)
    for result in results:
        vectors[tar_map[result[0]], :] = vectors[1]

    return vectors


def validate_ppr(core_network, labels, dataset_name='test', repetitions=5, random_seed=123, multiclass_classifier=None, target_nodes=None, parallel=False):
    """
    The main validation class --- use this to obtain CV results!
    """
    if multiclass_classifier is None:
        multiclass_classifier = SVC(kernel='linear', C=1, probability=True)
    df = pd.DataFrame()
    for k in range(repetitions):
        if target_nodes is not None:
            print('Subnetwork ranking in progress..')
            vectors = construct_PPR_matrix_targets(core_network, target_nodes, parallel=parallel)
            labels = labels[target_nodes]
        else:
            vectors = construct_PPR_matrix(core_network, parallel=parallel)
        nz = np.count_nonzero(labels, axis=0)
        wnz = np.argwhere(nz > 2).T[0]
        labels = labels[:, wnz]
        for j in np.arange(0.1, 0.5, 0.1):
            print('Train size:{}, method {}'.format(j, 'PPR'))
            print(vectors.shape, labels.shape)
            rs = StratifiedShuffleSplit(n_splits=10, test_size=0.5, random_state=random_seed)
            micros = []
            macros = []
            times = []
            new_train_y = []
            for y in labels:
                new_train_y.append(list(y).index(1))

            onedim_labels = np.array(new_train_y)
            for X_train, X_test in rs.split(vectors, new_train_y):
                start = time.time()
                train_x = vectors[X_train]
                test_x = vectors[X_test]
                train_labels = labels[X_train]
                test_labels = labels[X_test]
                train_labels_first = onedim_labels[X_train]
                test_labels_second = onedim_labels[X_test]
                clf = multiclass_classifier
                clf.fit(train_x, train_labels_first)
                preds = clf.predict(test_x)
                mi = f1_score(test_labels_second, preds, average='micro')
                ma = f1_score(test_labels_second, preds, average='macro')
                end = time.time()
                elapsed = end - start
                micros.append(mi)
                macros.append(ma)
                times.append(elapsed)

            outarray = {'percent_train':np.round(1 - j, 1), 
             'micro_F':np.mean(micros),  'macro_F':np.mean(macros),  'setting':'PPR',  'dataset':dataset_name,  'time':np.mean(times)}
            df = df.append(outarray, ignore_index=True)

    df = df.reset_index()
    return df