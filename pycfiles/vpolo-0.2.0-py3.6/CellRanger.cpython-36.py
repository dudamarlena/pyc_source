# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vpolo/avs_tools/CellRanger.py
# Compiled at: 2019-09-19 11:28:06
# Size of source mod 2**32: 1221 bytes
from collections import defaultdict
import Dedup

def get_prediction(eq_obj):
    predictions = {}
    for gene in eq_obj.genes_list:
        predictions[gene] = 0

    umi_genes = defaultdict(tuple)
    for eqId, label in enumerate(eq_obj.labels):
        gene_set = set([])
        for txp in label:
            txp_name = eq_obj.txps_list[txp]
            gene = eq_obj.txp_to_gene_dict[txp_name]
            gene_set.add(gene)

        if len(gene_set) == 1:
            gene_name = list(gene_set)[0]
            for umi, count in eq_obj.umis[eqId].items():
                if umi in umi_genes[umi]:
                    if umi_genes[umi][1] > count:
                        continue
                umi_genes[umi] = (
                 gene_name, count)

        else:
            print('ERROR: gene set for eqclass {} not 1 length for CellRanger'.format(label))

    gene_umis = defaultdict(lambda : defaultdict(int))
    for umi, (gene, count) in umi_genes.items():
        gene_umis[gene][umi] += count

    for gene, umis in gene_umis.items():
        predictions[gene] = Dedup.dedup(umis, False)

    return predictions