# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fritz/github/posterior/treecat/treecat/__main__.py
# Compiled at: 2017-08-14 23:03:39
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import multiprocessing
from parsable import parsable
from treecat.config import make_config
from treecat.format import guess_schema
from treecat.format import import_data
from treecat.format import pickle_dump
from treecat.format import pickle_load
parsable = parsable.Parsable()
parsable(guess_schema)
parsable(import_data)

@parsable
def train(dataset_in, ensemble_out, **options):
    """Train a TreeCat ensemble model on imported data."""
    from treecat.training import train_ensemble
    dataset = pickle_load(dataset_in)
    ragged_index = dataset['schema']['ragged_index']
    data = dataset['data']
    tree_prior = dataset['schema']['tree_prior']
    config = make_config(**options)
    ensemble = train_ensemble(ragged_index, data, tree_prior, config)
    pickle_dump(ensemble, ensemble_out)


if __name__ == '__main__':
    if hasattr(multiprocessing, 'set_start_method'):
        multiprocessing.set_start_method('spawn')
    parsable()