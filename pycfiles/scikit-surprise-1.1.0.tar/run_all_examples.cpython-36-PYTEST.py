# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/run_all_examples.py
# Compiled at: 2019-09-12 16:07:08
# Size of source mod 2**32: 1156 bytes
"""Run all the examples (except for benchmark.py). Just used as some kind of
functional test... If no warning / errors is output, it should be fine.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, os, warnings
sys.stdout = open(os.devnull, 'w')
from building_custom_algorithms import mean_rating_user_item
from building_custom_algorithms import most_basic_algorithm2
from building_custom_algorithms import most_basic_algorithm
from building_custom_algorithms import with_baselines_or_sim
import load_custom_dataset_predefined_folds, load_from_dataframe, baselines_conf, generate_grid_search_cv_results_example, load_from_dataframe, train_test_split, basic_usage, grid_search_usage, serialize_algorithm, use_cross_validation_iterators, k_nearest_neighbors, similarity_conf, precision_recall_at_k, split_data_for_unbiased_estimation, evaluate_on_trainset, load_custom_dataset, predict_ratings, top_n_recommendations