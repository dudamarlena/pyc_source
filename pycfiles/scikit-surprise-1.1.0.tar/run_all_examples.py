# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/run_all_examples.py
# Compiled at: 2018-05-27 10:16:01
from __future__ import absolute_import, division, print_function, unicode_literals
import sys, os, warnings
sys.stdout = open(os.devnull, b'w')
import load_from_dataframe, baselines_conf, generate_grid_search_cv_results_example, load_from_dataframe, run_all_examples, train_test_split, basic_usage, grid_search_usage, serialize_algorithm, use_cross_validation_iterators, k_nearest_neighbors, notebooks, similarity_conf, building_custom_algorithms, load_custom_dataset_predefined_folds, precision_recall_at_k, split_data_for_unbiased_estimation, evaluate_on_trainset, load_custom_dataset, predict_ratings, top_n_recommendations