# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sopex/example.py
# Compiled at: 2013-02-13 08:35:11
import sys
from chunker import PennTreebackChunker
from extractor import SOPExtractor
if __name__ == '__main__':
    sentences = ['Monkeys are destroying the garden.',
     'No man can serve two masters.',
     'When students travel to US, they usually go by air.',
     'The Earth revolves around the sun.',
     'Honesty is the best policy.',
     'John F. Kennedy was elected as US President in 1960.',
     'The quick brown fox jumps over the lazy dog.',
     'A rare black squirrel has become a regular visitor to a suburban garden',
     "As with every Sony PDA before it, the NR70 series is equipped with Sony's own memory stick expansion."]
    chunker = PennTreebackChunker()
    extractor = SOPExtractor(chunker)
    for sentence in sentences:
        sop_triplet = extractor.extract(sentence)
        print '%s --[%s]--> %s' % (sop_triplet.subject, sop_triplet.predicate, sop_triplet.object)

    extractor.close()