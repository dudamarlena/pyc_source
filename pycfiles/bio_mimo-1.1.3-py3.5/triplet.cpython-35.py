# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bio_mimo/triplet.py
# Compiled at: 2016-10-14 07:12:13
# Size of source mod 2**32: 620 bytes
from collections import Counter
from mimo import Stream
from lhc.binf.sequence.reverse_complement import reverse_complement

class GetTriplets(Stream):
    IN = [
     'sequence']
    OUT = ['triplet']

    async def run(self, ins, outs):
        async for sequence in ins.sequence:
                        triplets = Counter()
            for i in range(len(sequence) - 2):
                triplet = sequence[i:i + 3]
                if triplet[1] not in 'ctCT':
                    triplet = reverse_complement(triplet)
                triplets[triplet] += 1

            await outs.triplet.push(triplets)

        outs.triplet.close()