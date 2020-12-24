# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_load.py
# Compiled at: 2020-04-10 04:40:37
# Size of source mod 2**32: 725 bytes
import sys, os
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology, World
import owlready2
emmodir = os.path.join(thisdir, '..', '..', '..', 'EMMO')
owlready2.set_log_level(0)
emmo = get_ontology('emmo')
emmo.load()
world = World()
inferred = world.get_ontology()
inferred.load()
if os.path.exists(os.path.join(emmodir, 'emmo.owl')):
    world2 = World()
    local = world2.get_ontology(os.path.join(emmodir, 'emmo.owl'))
    local.load(catalog_file=True)