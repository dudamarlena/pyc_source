# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vpolo/avs_tools/EqClass.py
# Compiled at: 2019-09-19 11:28:06
# Size of source mod 2**32: 2207 bytes
from collections import defaultdict

class Eqclasses:
    __doc__ = '\n    Read In eqclass file for running downstream tasks\n    '

    def __init__(self, fname):
        print('Using File ', fname)
        self.txp_to_gene_dict = defaultdict(str)
        self.gene_to_txp_dict = defaultdict(set)
        self.labels = []
        self.umis = []
        self.txps_list = []
        self.populate_eqclass(fname)

    def populate_eqclass(self, fname):
        with open(fname) as (f):
            self.num_transcripts = int(f.readline())
            self.num_eqclasses = int(f.readline())
            for i in range(self.num_transcripts):
                txp, gene = f.readline().strip().split(' ')
                if txp in self.txp_to_gene_dict:
                    print('ERROR: redundant entry for txp {} in txp to gene Map', txp)
                    print('Exiting')
                    exit(1)
                self.txps_list.append(txp)
                self.txp_to_gene_dict[txp] = gene
                self.gene_to_txp_dict[gene].add(i)

            self.genes_list = set(self.txp_to_gene_dict.values())
            self.num_genes = len(self.genes_list)
            for line in f:
                toks = line.strip().split(' ')
                num_labels = int(toks[0])
                labels = tuple(map(int, toks[1:num_labels + 1]))
                umi_dict = defaultdict(int)
                for i in range(num_labels + 1, len(toks), 2):
                    umi_dict[toks[i]] = int(toks[(i + 1)])

                self.labels.append(labels)
                self.umis.append(umi_dict)

        print('Found {} Transcripts, {} Genes, {} Eqclasses'.format(self.num_transcripts, self.num_genes, self.num_eqclasses))
        print('Imported Transcript To Gene Map:')
        print(self.txp_to_gene_dict)
        print('Imported Gene to Transcript Map:')
        print(self.gene_to_txp_dict)
        print('List of Imported Eqclasses')
        print(self.labels)
        print('List of Imported UMI & counts to corresponding eqclass label')
        print(self.umis)