# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bio_mimo/window.py
# Compiled at: 2016-10-14 07:12:13
# Size of source mod 2**32: 712 bytes
from lhc.binf.genomic_coordinate import GenomicInterval as Interval
from mimo import Stream, azip

class StreamChromosomeWindows(Stream):
    IN = [
     'chromosome_id', 'chromosome_length']
    OUT = ['chromosome_interval']

    def __init__(self, window_length):
        super().__init__()
        self.window_length = window_length

    async def run(self, ins, outs):
        length = self.window_length
        async for chromosome_id, chromosome_length in azip(ins.chromosome_id, ins.chromosome_length):
                        for fr in range(0, chromosome_length, length):
                await outs.chromosome_interval.push(Interval(fr, fr + length, chromosome=chromosome_id))

        outs.chromosome_interval.close()