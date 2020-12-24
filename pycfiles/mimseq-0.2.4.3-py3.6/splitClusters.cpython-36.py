# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimseq/splitClusters.py
# Compiled at: 2020-04-14 04:47:56
# Size of source mod 2**32: 8788 bytes
from __future__ import absolute_import
import pandas as pd, numpy as np, logging
from .ssAlign import aligntRNA
from collections import defaultdict
log = logging.getLogger(__name__)

def dd():
    return defaultdict(dict)


def splitIsodecoder(tRNA_dict, cluster_dict, mismatch_dict, insert_dict, cluster_perPos_mismatchMembers, out_dir, experiment_name):
    log.info('\n+------------------------------------------------------------------------------+\t\t\n| Characterizing cluster mismatches for read splitting by unique tRNA sequence |\t\t\n+------------------------------------------------------------------------------+')
    isodecoder_sizes = defaultdict(int)
    unique_isodecoderMMs = defaultdict(dd)
    log.info('** Assessing mismatches between cluster members and parent... **')
    for cluster, mismatches in mismatch_dict.items():
        mismatches = sorted(mismatches, reverse=True)
        curr_isodecoders = 1
        detected_seqs = defaultdict(list)
        detected_seqs = [tRNA_dict[cluster]['sequence']]
        detected_clusters = [cluster]
        cluster_members = {tRNA:data['sequence'] for tRNA, data in tRNA_dict.items() if tRNA in cluster_dict[cluster]}
        parent_size = len([tRNA for tRNA, sequence in cluster_members.items() if sequence.upper() == tRNA_dict[cluster]['sequence'].upper()])
        isodecoder_num = len(set([sequences.upper() for sequences in cluster_members.values()]))
        for pos in mismatches:
            if curr_isodecoders < isodecoder_num:
                type_count = defaultdict(list)
                mismatch_members = {tRNA:sequence for tRNA, sequence in cluster_members.items() if tRNA in cluster_perPos_mismatchMembers[cluster][pos]}
                for tRNA, sequence in mismatch_members.items():
                    if sequence.upper() not in detected_seqs and tRNA not in detected_clusters:
                        try:
                            ins_num = len(set([ins for ins in insert_dict[cluster] if tRNA in insert_dict[cluster][ins] if ins < pos]))
                            type_count[sequence[(pos - ins_num)]].append(tRNA)
                            detected_seqs.append(sequence.upper())
                        except IndexError:
                            continue

                for identity, tRNAs in type_count.items():
                    if len(tRNAs) == 1:
                        detected_clusters.append(tRNAs[0])
                        isodecoder_items = [tRNA for tRNA, sequence in cluster_members.items() if sequence.upper() == tRNA_dict[tRNAs[0]]['sequence'].upper()]
                        isodecoder_sizes[tRNAs[0]] = len(isodecoder_items)
                        cluster_dict[cluster] = [tRNA for tRNA in cluster_dict[cluster] if tRNA not in isodecoder_items]
                        curr_isodecoders += 1
                        unique_isodecoderMMs[cluster][pos][identity.upper()] = tRNAs[0]
                    elif len(tRNAs) > 1:
                        for tRNA in tRNAs:
                            sequence = tRNA_dict[tRNA]['sequence'].upper()
                            detected_seqs.remove(sequence)

        for insertion, members in insert_dict[cluster].items():
            if curr_isodecoders < isodecoder_num:
                type_count = defaultdict(list)
                insert_members = {tRNA:sequence for tRNA, sequence in cluster_members.items() if tRNA in members}
                isodecoders_withIns = len(set([num for tRNA in list(insert_members.keys()) for num in tRNA.split('-')[(-2)]]))
                if isodecoders_withIns == 1:
                    for tRNA, sequence in insert_members.items():
                        if sequence.upper() not in detected_seqs and tRNA not in detected_clusters:
                            type_count['insertion'].append(tRNA)
                            detected_seqs.append(sequence.upper())

                for identity, tRNAs in type_count.items():
                    if len(tRNAs) == 1:
                        detected_clusters.append(tRNAs[0])
                        isodecoder_items = [tRNA for tRNA, sequence in cluster_members.items() if sequence.upper() == tRNA_dict[tRNAs[0]]['sequence'].upper()]
                        isodecoder_size = len(isodecoder_items)
                        isodecoder_sizes[tRNAs[0]] = isodecoder_size
                        cluster_dict[cluster] = [tRNA for tRNA in cluster_dict[cluster] if tRNA not in isodecoder_items]
                        curr_isodecoders += 1
                        unique_isodecoderMMs[cluster][insertion][identity] = tRNAs[0]
                    elif len(tRNAs) > 1:
                        for tRNA in tRNAs:
                            sequence = tRNA_dict[tRNA]['sequence'].upper()
                            detected_seqs.remove(sequence)

    splitBool = list()
    for cluster, members in cluster_dict.items():
        cluster_size = len(members)
        isodecoder_sizes[cluster] = cluster_size
        remaining_isodecoders = set([data['sequence'].upper() for member, data in tRNA_dict.items() if member in members])
        if len(remaining_isodecoders) > 1:
            splitBool.append(cluster)

    total_detected_isodecoders = 0
    with open(out_dir + experiment_name + 'isodecoderInfo.txt', 'w') as (isodecoderInfo):
        isodecoderInfo.write('Isodecoder\tsize\n')
        for isodecoder, size in isodecoder_sizes.items():
            isodecoderInfo.write(isodecoder + '\t' + str(size) + '\n')
            if isodecoder not in splitBool:
                total_detected_isodecoders += 1

    with open(out_dir + experiment_name + '_isodecoderTranscripts.fa', 'w') as (tempSeqs):
        for seq in isodecoder_sizes.keys():
            tempSeqs.write('>' + seq + '\n' + tRNA_dict[seq]['sequence'] + '\n')

    aligntRNA(tempSeqs.name, out_dir)
    total_isodecoders = len(set([data['sequence'].upper() for tRNA, data in tRNA_dict.items()]))
    log.info('Total unique tRNA sequenes in input: {}'.format(total_isodecoders))
    log.info('Total deconvoluted unique tRNA sequences: {}'.format(total_detected_isodecoders))
    return (
     unique_isodecoderMMs, splitBool, isodecoder_sizes)


def getIsodecoderSizes(out_dir, experiment_name, tRNAdict):
    isodecoder_sizes = defaultdict(int)
    already_added = set()
    for tRNA in tRNAdict:
        if tRNA not in already_added:
            sameSeq = [tRNAs for tRNAs, data in tRNAdict.items() if data['sequence'] == tRNAdict[tRNA]['sequence']]
            already_added.update(sameSeq)
            isodecoder_sizes[tRNA] = len(sameSeq)

    with open(out_dir + experiment_name + 'isodecoderInfo.txt', 'w') as (isodecoderInfo):
        isodecoderInfo.write('Isodecoder\tsize\n')
        for isodecoder, size in isodecoder_sizes.items():
            isodecoderInfo.write(isodecoder + '\t' + str(size) + '\n')

    return isodecoder_sizes