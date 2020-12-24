# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/ext800/projects/fastsemsim/fastsemsim/fastsemsim/examples/load_annotation_corpus.py
# Compiled at: 2019-02-15 18:00:34
# Size of source mod 2**32: 6679 bytes
"""
Copyright 2011 Marco Mina. All rights reserved.

This file is part of fastSemSim

fastSemSim is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

fastSemSim is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with fastSemSim.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function
import fastsemsim, sys, os
if __name__ == '__main__':
    ontology_type = 'DiseaseOntology'
    ignore_parameters = {'ignore': {'regulates': False, 'has_part': True, 'negatively_regulates': False, 'positively_regulates': False, 'occurs_in': False, 'happens_during': True, 'lacks_plasma_membrane_part': True}}
    ontology_file_type = 'obo'
    ontology_source_file = None
    ac_source_file = None
    ac_species = 'human'
    ac_source_file_type = 'plain'
    ac_params = {}
    ac_params['filter'] = {}
    ac_params['filter']['EC'] = {}
    ac_params['filter']['taxonomy'] = {}
    ac_params['multiple'] = True
    ac_params['term first'] = False
    ac_params['separator'] = '\t'
    print('\n######################')
    print('# Loading ontology... #')
    print('######################\n')
    ontology = fastsemsim.load_ontology(source_file=ontology_source_file, file_type=ontology_file_type, ontology_type=ontology_type, ontology_descriptor=None, parameters=ignore_parameters)
    print('\n#################################')
    print('# Ontology successfully loaded.')
    print('#################################\n')
    print('source_file: ' + str(ontology_source_file))
    print('file_type: ' + str(ontology_file_type))
    print('ontology_type: ' + str(ontology_type))
    print('ignore_parameters: ' + str(ignore_parameters))
    print('Number of nodes: ' + str(ontology.node_number()))
    print('Number of edges: ' + str(ontology.edge_number()))
    print('\nType and number of edges:\n-------------\n' + str(ontology.edges['type'].value_counts()))
    print('-------------')
    print('\nInner edge number (within the ontology):\n-------------\n' + str(ontology.edges['inner'].value_counts()))
    print('-------------')
    print('\nIntra edge number (within the same namespace):\n-------------\n' + str(ontology.edges['intra'].value_counts()))
    print('-------------')
    print('\nOuter edges (link to other ontologies):\n-------------\n' + str(ontology.edges.loc[(ontology.edges['inner'] == False)]))
    print('-------------')
    print('\nInter edges (link between different namespaces - within the same ontology):\n-------------\n' + str(ontology.edges.loc[((ontology.edges['intra'] == False) & (ontology.edges['inner'] == True))]))
    print('-------------')
    print('\n######################')
    print('# Loading annotation corpus... #')
    print('######################\n')
    if ac_source_file is None:
        ac_descriptor = fastsemsim.dataset.get_default_annotation_corpus(ontology_type=ontology_type, ac_species=ac_species)
        ac = fastsemsim.load_ac(ontology, source_file=None, file_type=None, species=None, ac_descriptor=ac_descriptor, params=ac_params)
    else:
        ac = fastsemsim.load_ac(ontology, source_file=ac_source_file, file_type=ac_source_file_type, species=None, ac_descriptor=None, params=ac_params)
    ac.isConsistent()
    print('\n#################################')
    print('# Annotation corpus successfully loaded.')
    print('#################################\n')
    print('\n\n')
    print('AC source: ' + str(ac_source_file))
    print('ac source_type: ' + str(ac_source_file_type))
    print('ac_parameters: ' + str(ac_params))
    print('AC species: ' + str(ac_species))
    print('AC descriptor: ' + str(ac_descriptor))
    print('ac - Number of annotated proteins: ' + str(len(ac.annotations)))
    print('ac - Number of annotated terms: ' + str(len(ac.reverse_annotations)))
    print('-------------')