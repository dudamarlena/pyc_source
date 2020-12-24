# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/test/util/test_fodder.py
# Compiled at: 2007-09-29 15:43:43
from rdflib import ConjunctiveGraph
from oort.test import mergepaths
from oort.util.fodder import load_fodder
CONTENT = mergepaths(__file__, 'fodder_contents/site')
graph = ConjunctiveGraph()
load_fodder(graph, CONTENT)