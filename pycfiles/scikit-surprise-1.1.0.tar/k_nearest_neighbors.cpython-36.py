# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/k_nearest_neighbors.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 2085 bytes
"""
This module illustrates how to retrieve the k-nearest neighbors of an item. The
same can be done for users with minor changes. There's a lot of boilerplate
because of the id conversions, but it all boils down to the use of
algo.get_neighbors().
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import io
from surprise import KNNBaseline
from surprise import Dataset
from surprise import get_dataset_dir

def read_item_names():
    """Read the u.item file from MovieLens 100-k dataset and return two
    mappings to convert raw ids into movie names and movie names into raw ids.
    """
    file_name = get_dataset_dir() + '/ml-100k/ml-100k/u.item'
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as (f):
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]

    return (
     rid_to_name, name_to_rid)


data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
sim_options = {'name':'pearson_baseline',  'user_based':False}
algo = KNNBaseline(sim_options=sim_options)
algo.fit(trainset)
rid_to_name, name_to_rid = read_item_names()
toy_story_raw_id = name_to_rid['Toy Story (1995)']
toy_story_inner_id = algo.trainset.to_inner_iid(toy_story_raw_id)
toy_story_neighbors = algo.get_neighbors(toy_story_inner_id, k=10)
toy_story_neighbors = (algo.trainset.to_raw_iid(inner_id) for inner_id in toy_story_neighbors)
toy_story_neighbors = (rid_to_name[rid] for rid in toy_story_neighbors)
print()
print('The 10 nearest neighbors of Toy Story are:')
for movie in toy_story_neighbors:
    print(movie)