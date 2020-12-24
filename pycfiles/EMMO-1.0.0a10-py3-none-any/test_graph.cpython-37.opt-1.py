# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_graph.py
# Compiled at: 2020-04-10 04:40:37
# Size of source mod 2**32: 1030 bytes
import sys, os
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology
emmo = get_ontology()
emmo.load()
graph = emmo.get_dot_graph(relations='is_a')
graph.write_svg('taxonomy.svg')
graph.write_pdf('taxonomy.pdf')
entity_graph = emmo.get_dot_graph('EMMO')
entity_graph.write_svg('taxonomy2.svg')
substrate_graph = emmo.get_dot_graph('Item', relations=True, leafs='Physical',
  parents='Item',
  style='uml')
substrate_graph.write_svg('merotopology_graph.svg')
property_graph = emmo.get_dot_graph('Property')
property_graph.write_svg('property_graph.svg')
emmo._default_style['graph']['rankdir'] = 'BT'
relations_graph = emmo.get_dot_graph('EMMORelation')
relations_graph.write_pdf('relation_graph.pdf')
relations_graph.write_png('relation_graph.png')