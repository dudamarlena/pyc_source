# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: examples/w_repeats/chimp/2000/config.py
# Compiled at: 2018-10-01 11:48:44
import os
exp_dir = os.path.dirname(__file__)
configuration = {'experiment_name': 'Chimp 2000', 
   'experiment_info': '\n        6 genomes are taken as input: Chimpanzee, Mouse, Rat, Dog, Opossum.\n        Chimpanzee genome is fragment with repeats of length >= 2000 bp\n        All duplicated genes are filtered out.\n        (((chimpanzee,(mouse, rat)),(cat,dog)),opossum); is utilized for observed genome set.\n    ', 
   'gos-asm': {'input': {'block_orders_file_paths': [
                                                   os.path.join(exp_dir, 'blocks.txt')], 
                         'phylogenetic_tree': '(((chimpanzee,(mouse, rat)),(cat,dog)),opossum);', 
                         'target_organisms': [
                                            'chimpanzee'], 
                         'repeats_bridges_file': os.path.join(exp_dir, 'bridges.txt')}, 
               'output': {'dir': os.path.join(exp_dir, 'output')}}, 
   'mgra': {'executable_path': '/Users/aganezov/research/mgra/build/src/mgra/indel_mgra'}, 
   'algorithm': {'executable_containers': [], 'pipeline': {'entries_names': [
                                              'task_input',
                                              'tmc_wrapper_CCA_balanced',
                                              'cyclic_wrapper_MGRA_CCA_balanced',
                                              'tmc_wrapper_phylo',
                                              'task_output']}}}