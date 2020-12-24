# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_modules.py
# Compiled at: 2020-04-10 04:40:37
# Size of source mod 2**32: 593 bytes
import sys, os
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology
from emmo.graph import plot_modules, get_module_dependencies, check_module_dependencies
iri = 'http://emmo.info/emmo/1.0.0-alpha'
emmo = get_ontology(iri)
emmo.load()
modules = get_module_dependencies(emmo)
plot_modules(iri, filename='modules.png', modules=modules)
check_module_dependencies(modules)