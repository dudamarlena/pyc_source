# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sopex/__init__.py
# Compiled at: 2013-02-13 09:15:16
from chunker import PennTreebackChunker
from extractor import SOPExtractor
chunker = PennTreebackChunker()
extractor = SOPExtractor(chunker)

def extract(sentence):
    global extractor
    sentence = sentence if sentence[(-1)] == '.' else sentence + '.'
    sop_triplet = extractor.extract(sentence)
    return sop_triplet