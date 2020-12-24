# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vshekar/anaconda3/lib/python3.7/site-packages/recommender/recommender_pipeline.py
# Compiled at: 2019-06-17 16:12:19
# Size of source mod 2**32: 3282 bytes
import json, os, numpy as np, pandas as pd
from recommender.generator import Generator, MLmodel
from recommender.mutual_information import MutualInformation, DESCRIPTORS_TO_REMOVE

def generate_reaction_grid():
    grid_params_filename = '../sample_data/grid_params.json'
    compounds_filename = '../sample_data/triples_and_amounts.json'
    reaction_generator = Generator(compounds_filename, grid_params_filename)
    reaction_generator.generate_grid()
    descriptor_list_file = '../sample_data/descriptors_list.json'
    reaction_generator.generate_descriptors(descriptor_list_file)
    reaction_generator.generate_expanded_grid()
    return reaction_generator


def reaction_sieve(reaction_generator):
    model = MLmodel()
    potential_reactions = model.sieve(reaction_generator.all_combos_expanded)
    return potential_reactions


def recommend(potential_reactions, top_k):
    dataset = pd.read_csv('../sample_data/test_data_full.csv',
      low_memory=False)
    dataset_org = dataset.iloc[:6000]
    dataset_new = dataset.iloc[-100:]
    descriptors_to_keep = [col for col in dataset.columns if col not in DESCRIPTORS_TO_REMOVE]
    desc_to_keep_testing = [col for col in dataset.columns if col not in DESCRIPTORS_TO_REMOVE] + [
     'boolean_crystallisation_outcome_manual_0']
    dataset_new = dataset_new[desc_to_keep_testing].values
    compound_column_labels = ['compound_0', 'compound_1', 'compound_2']
    mi = MutualInformation(dataset_org, 'boolean_crystallisation_outcome_manual_0', compound_column_labels, descriptors_to_keep)
    recommended_reactions = mi.get_recommended_reactions(top_k, potential_reactions[[col for col in potential_reactions.columns if col not in DESCRIPTORS_TO_REMOVE]])
    return recommended_reactions


if __name__ == '__main__':
    os.environ['CXCALC_PATH'] = '/Applications/MarvinSuite/bin'
    reaction_generator = generate_reaction_grid()
    pred_sucessful_reaction = reaction_sieve(reaction_generator)
    recommended_reactions = recommend(pred_sucessful_reaction, 10)
    print(recommended_reactions)