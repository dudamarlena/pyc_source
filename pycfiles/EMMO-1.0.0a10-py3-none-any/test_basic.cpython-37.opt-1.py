# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_basic.py
# Compiled at: 2020-04-10 04:40:37
# Size of source mod 2**32: 1331 bytes
import sys, os, itertools
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology
import owlready2
emmo = get_ontology()
emmo.load()
onto = get_ontology('onto.owl')
onto.imported_ontologies.append(emmo)
onto.base_iri = 'http://emmo.info/examples/test#'
with onto:

    class Hydrogen(emmo.Atom):
        pass


    class Oxygen(emmo.Atom):
        pass


    class H2O(emmo.Molecule):
        __doc__ = 'Water molecule.'
        emmo.hasSpatialDirectPart.exactly(2, Hydrogen)
        emmo.hasSpatialDirectPart.exactly(1, Oxygen)


    H1 = Hydrogen()
    H2 = Hydrogen()
    O = Oxygen()
    w = H2O()
    w.hasSpatialDirectPart = [H1, H2, O]
onto.sync_attributes(name_policy='sequential', name_prefix='myonto_')
assert 'myonto_0' in onto
assert 'myonto_6' in onto
onto.sync_attributes(name_policy='uuid', name_prefix='onto_')
assert w.name.startswith('onto_')
assert len(w.name) == 41
for e in itertools.chain(onto.classes(), onto.individuals()):
    owlready2.destroy_entity(e)