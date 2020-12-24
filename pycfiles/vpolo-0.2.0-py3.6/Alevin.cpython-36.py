# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vpolo/avs_tools/Alevin.py
# Compiled at: 2019-09-19 11:28:06
# Size of source mod 2**32: 4351 bytes
from collections import defaultdict
from itertools import combinations
import Dedup

def get_seen_and_dedup_counts(eq_obj, umis):
    umi_set = set([k for k, _ in umis.items()])
    count = Dedup.dedup(umis, True)
    return (
     umi_set, count)


def remove_seen_UMI_and_dedup(umis, seen):
    new_umis_set = set(umis.keys()) - seen
    new_umis = {k:v for k, v in umis.items() if k in new_umis_set}
    return Dedup.dedup(new_umis, True)


def rescue_UMI(eq_obj, min_set_txps, predictions):
    new_eqclasses = defaultdict(lambda : defaultdict(int))
    for i in range(eq_obj.num_eqclasses):
        try:
            labels = eq_obj.labels[i]
        except:
            print('ERROR: wrong Number of eqclasses provided')
            exit(1)

        umis = eq_obj.umis[i]
        new_label = []
        genes_set = set([])
        for label in labels:
            txp_name = eq_obj.txps_list[label]
            genes_set.add(eq_obj.txp_to_gene_dict[txp_name])
            if txp_name in min_set_txps:
                new_label.append(label)

        if len(genes_set) == 1:
            sorted_labels = tuple(sorted(new_label))
            for umi, count in umis.items():
                new_eqclasses[sorted_labels][umi] += count

        else:
            print('ERROR: {} Eqclass has txps from differen gene', i)
            exit(1)

    print('New Alevin Eqclasses: ', new_eqclasses)
    seen = defaultdict(set)
    for labels, umis in new_eqclasses.items():
        if len(labels) == 1:
            txp = list(labels)[0]
            txp_name = eq_obj.txps_list[txp]
            gene = eq_obj.txp_to_gene_dict[txp_name]
            if txp in seen:
                print('ERROR: more than one 1-length eqclass for txp: ', txp)
            seen[txp], dedup_count = get_seen_and_dedup_counts(eq_obj, umis)
            predictions[gene] += dedup_count

    for labels, umis in new_eqclasses.items():
        if len(labels) > 1:
            seenUMIlist = set([])
            genes_set = set([])
            for txp in labels:
                txp_name = eq_obj.txps_list[txp]
                genes_set.add(eq_obj.txp_to_gene_dict[txp_name])
                if txp in seen:
                    seenUMIlist |= seen[txp]

            if len(genes_set) > 1:
                print('ERROR: Eqclass has txps from different gene: ', labels)
                exit(1)
            dedup_count = remove_seen_UMI_and_dedup(umis, seenUMIlist)
            predictions[list(genes_set)[0]] += dedup_count


def check_set_coverage(eq_obj, txpList):
    for eqclass in eq_obj.labels:
        covered = False
        for txp in eqclass:
            txp_name = eq_obj.txps_list[txp]
            if txp_name in txpList:
                covered = True
                break

        if not covered:
            return False

    return True


def get_set_cover(eq_obj):
    right_set = eq_obj.txps_list
    grouping = 0
    min_txps = set([])
    while 1:
        grouping = grouping + 1
        is_covered = False
        for txps in combinations(right_set, grouping):
            curr_min_txp_set = set(txps)
            is_covered = check_set_coverage(eq_obj, curr_min_txp_set)
            if is_covered:
                min_txps |= set(txps)
                break

        if is_covered:
            break

    print('min_set of txps for Alevin: ', min_txps)
    return min_txps


def get_prediction(eq_obj):
    predictions = {}
    for gene in eq_obj.genes_list:
        predictions[gene] = 0

    min_set_txps = get_set_cover(eq_obj)
    rescue_UMI(eq_obj, min_set_txps, predictions)
    return predictions