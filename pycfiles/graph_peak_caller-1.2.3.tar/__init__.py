# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ivargry/dev/graph_peak_caller/graph_peak_caller/sample/__init__.py
# Compiled at: 2018-08-24 06:06:37
import logging
from .sparsegraphpileup import SamplePileupGenerator

def get_fragment_pileup(graph, input_intervals, info, reporter=None):
    logging.info('Creating fragment pileup, using fragment length %d and read length %d' % (
     info.fragment_length, info.read_length))
    spg = SamplePileupGenerator(graph, info.fragment_length - info.read_length)
    return spg.run(input_intervals, reporter)