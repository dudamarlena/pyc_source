# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bio_mimo/vcf.py
# Compiled at: 2016-10-14 07:12:13
# Size of source mod 2**32: 1580 bytes
import gzip
from collections import deque
from itertools import islice
from lhc.io.vcf import VcfIterator
from mimo import Stream

class StreamVcf(Stream):
    IN = [
     'vcf_file']
    OUT = ['vcf_header', 'variant']

    async def run(self, ins, outs):
        async for vcf_file in ins.vcf_file:
                        with gzip.open(vcf_file, 'rt', encoding='utf-8') if vcf_file.endswith('.gz') else open(vcf_file, encoding='utf-8') as (fileobj):
                iterator = VcfIterator(fileobj)
                await outs.vcf_header.push(iterator.header)
                for variant in iterator:
                    await outs.variant.push(variant)

        outs.vcf_header.close()
        outs.variant.close()


class GetVariantByInterval(Stream):
    IN = [
     'chromosome_interval', 'variant']
    OUT = ['variants']

    async def run(self, ins, outs):
        variants = deque()
        async for interval in ins.chromosome_interval:
                        while len(variants) > 0 and variants[0].pos < interval.start:
                variants.popleft()

            if ins.variant.is_open():
                if len(variants) == 0:
                    variants.append(await ins.variant.pop())
                while ins.variant.is_open() and variants[(-1)].pos < interval.stop:
                    variants.append(await ins.variant.pop())

            if variants[(-1)].pos < interval.stop:
                await outs.variants.push(list(variants))
            else:
                await outs.variants.push(list(islice(variants, 0, len(variants) - 1)))

        outs.variants.close()