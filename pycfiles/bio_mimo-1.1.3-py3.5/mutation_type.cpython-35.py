# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bio_mimo/mutation_type.py
# Compiled at: 2016-10-14 07:12:13
# Size of source mod 2**32: 539 bytes
from lhc.binf.sequence.reverse_complement import reverse_complement
from mimo import Stream

class GetMutationType(Stream):
    IN = [
     'variant']
    OUT = ['mutation_type']

    async def run(self, ins, outs):
        async for variant in ins.variant:
                        if variant.ref in 'CTct':
                await outs.mutation_type.push((variant.ref, variant.alt[0]))
            else:
                await outs.mutation_type.push((reverse_complement(variant.ref), reverse_complement(variant.alt[0])))

        outs.mutation_type.close()