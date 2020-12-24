# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddgen/utils/_txs.py
# Compiled at: 2020-03-24 14:57:35
# Size of source mod 2**32: 2676 bytes
import re, typing
_tx_priorities = {'NM_':1, 
 'XM_':2, 
 'NR_':3, 
 'XR_':4}

def prioritize_refseq_transcripts(txs: typing.Union[(list, tuple, set)]):
    """RefSeq transcripts have following categories: {NM_, XM_, NR_, XR_}.
    If we have transcripts from multiple sources, we want to select the one coming from the source with highest priority.
    E.g. `NM_` has higher priority than `XM_`.

    If we have multiple transcripts from a single source, we want to select the one with smaller integer.
    E.g. `NM_123.4` has higher priority than `NM_124.4`.
    :param txs: iterable with transcript accession id strings

    """
    priorities = [_tx_priorities[tx[:3]] for tx in txs if tx[:3] in _tx_priorities]
    if priorities:
        max_observed_priority = min(priorities)
        if max_observed_priority == 1:
            nms = [tx for tx in txs if tx.startswith('NM_')]
            if len(nms) == 1:
                return nms[0]
            else:
                return _find_max_priority_within_single_source(nms, 'NM_')
        else:
            if max_observed_priority == 2:
                xms = [tx for tx in txs if tx.startswith('XM_')]
                if len(xms) == 1:
                    return xms[0]
                else:
                    return _find_max_priority_within_single_source(xms, 'XM_')
            else:
                if max_observed_priority == 3:
                    nrs = [tx for tx in txs if tx.startswith('NR_')]
                    if len(nrs) == 1:
                        return nrs[0]
                    else:
                        return _find_max_priority_within_single_source(nrs, 'NR_')
                elif max_observed_priority == 4:
                    xrs = [tx for tx in txs if tx.startswith('XR_')]
                    if len(xrs) == 1:
                        return xrs[0]
                    else:
                        return _find_max_priority_within_single_source(xrs, 'XR_')
    else:
        return


def _find_max_priority_within_single_source(txs, source):
    if len(txs) != 0:
        if len(txs) == 1:
            return txs[0]
        else:
            pt = re.compile('{}(?P<number>\\d+)\\.(?P<subscript>\\d*)'.format(source))
            numbers = [int(pt.match(tx).group('number')) for tx in txs]
            min_number = min(numbers)
            min_idx = numbers.index(min_number)
            return txs[min_idx]
    else:
        return