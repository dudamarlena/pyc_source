# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_ontodoc.py
# Compiled at: 2020-04-10 04:40:37
# Size of source mod 2**32: 982 bytes
import sys, os
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology
from emmo.ontodoc import OntoDoc, DocPP
emmo = get_ontology()
emmo.load()
baseiri = 'http://emmo.info/'
iris = set((c.namespace.base_iri for c in emmo.classes()))
iris.update(set((c.namespace.base_iri for c in emmo.object_properties())))
for s in sorted(iris):
    print(s)

inputdir = os.path.abspath(os.path.join(thisdir, '..', '..', 'examples', 'emmodoc'))
inputfile = os.path.join(thisdir, 'doc.md')
ontodoc = OntoDoc(emmo)
with open(inputfile, 'rt') as (f):
    template = f.read()
docpp = DocPP(template, ontodoc, os.path.dirname(inputfile))
docpp.process()
with open('doc-output.md', 'wt') as (f):
    f.write(docpp.get_buffer())