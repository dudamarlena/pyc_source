# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/spyda/processors.py
# Compiled at: 2013-02-04 19:51:27
try:
    from calais import Calais
except ImportError:
    Calais = None

if Calais is not None:

    def process_calais(content, key):
        calais = Calais(key)
        response = calais.analyze(content)
        people = [ entity['name'] for entity in getattr(response, 'entities', []) if entity['_type'] == 'Person' ]
        return {'people': people}