# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_graph2.py
# Compiled at: 2020-04-10 04:40:37
# Size of source mod 2**32: 2448 bytes
import sys, os
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology
from emmo.graph import OntoGraph
outdir = 'test_graph2'
if not os.path.exists(outdir):
    os.makedirs(outdir)
os.chdir(outdir)
emmo = get_ontology()
emmo.load()
g = OntoGraph(emmo, (emmo.hasPart), leafs=('mereotopological', 'semiotical', 'connected'))
g.save('hasPart.svg')
g.save('MaterialState.png')
g = OntoGraph(emmo, (emmo.MaterialState), relations='all', addnodes=True, edgelabels=None)
g.save('MaterialState.png')
g = OntoGraph(emmo, (emmo.ElementaryParticle), relations='all', addnodes=True, edgelabels=None)
g.save('ElementaryParticle.png')
g = OntoGraph(emmo, (emmo.SIBaseUnit), relations='all', addnodes=True, edgelabels=True,
  addconstructs=False,
  graph_attr={'rankdir': 'RL'})
g.add_legend()
g.save('SIBaseUnit.png')
g = OntoGraph(emmo, (emmo.EMMORelation), relations='all', edgelabels=None)
g.save('EMMORelation.png')
g = OntoGraph(emmo, (emmo.Quantity), leafs=[
 emmo.DerivedQuantity, emmo.BaseQuantity,
 emmo.PhysicalConstant],
  relations='all',
  edgelabels=None,
  addnodes=True,
  addconstructs=True,
  graph_attr={'rankdir': 'RL'})
g.add_legend()
g.save('Quantity.svg')
g = OntoGraph(emmo)
g.add_legend('all')
g.save('legend.png')
g = OntoGraph(emmo, (emmo.EMMO), leafs=[emmo.Perspective, emmo.Elementary])
g.save('top.png')
leafs = set()
for s in emmo.Perspective.subclasses():
    leafs.update(s.subclasses())

g = OntoGraph(emmo, (emmo.Perspective), leafs=leafs, parents=1)
g.save('Perspectives.png')
leafs = {
 emmo.Interpreter, emmo.Conventional, emmo.Icon, emmo.Observation,
 emmo.Object}
hidden = {emmo.SIUnitSymbol, emmo.SpecialUnit, emmo.Manufacturing,
 emmo.Engineered, emmo.PhysicalPhenomenon}
semiotic = emmo.get_branch((emmo.Holistic), leafs=(leafs.union(hidden)))
semiotic.difference_update(hidden)
g = OntoGraph(emmo)
g.add_entities(semiotic, relations='all', edgelabels=False)
g.save('Semiotic.png')
g.add_legend()
g.save('Semiotic+legend.png')
legend = OntoGraph(emmo)
legend.add_legend(g.get_relations())
legend.save('Semiotic-legend.png')