# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/core.py
# Compiled at: 2009-07-20 09:57:48
from sparrow.redland_backend import RedlandTripleStore
from sparrow.rdflib_backend import RDFLibTripleStore
from sparrow.sesame_backend import SesameTripleStore
from sparrow.allegro_backend import AllegroTripleStore

def database(backend, dburi):
    if backend == 'redland':
        db = RedlandTripleStore()
    elif backend == 'rdflib':
        db = RDFLibTripleStore()
    elif backend == 'sesame':
        db = SesameTripleStore()
    elif backend == 'allegro':
        db = AllegroTripleStore()
    else:
        raise ValueError('Unknown database backend: "%s"' % backend)
    db.connect(dburi)
    return db