# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/degex.py
# Compiled at: 2014-12-19 21:46:34
IUPAC_vals = {'A': 'A', 'B': 'CGT', 
   'C': 'C', 
   'D': 'AGT', 
   'G': 'G', 
   'H': 'ACT', 
   'K': 'GT', 
   'M': 'AC', 
   'N': 'GATC', 
   'R': 'AG', 
   'S': 'CG', 
   'T': 'T', 
   'V': 'ACG', 
   'W': 'AT', 
   'X': 'GATC', 
   'Y': 'CT'}

class dfs_node:

    def __init__(self, cum, rem):
        self.visited = False
        self.neighbors = []
        self.cumul_seq = cum
        self.remain_seq = rem


def dfs_expand_seq(curr_dfs_node, cum_list):
    curr_dfs_node.visited = True
    if len(curr_dfs_node.remain_seq) > 0:
        for nucleotide in IUPAC_vals[curr_dfs_node.remain_seq[0]]:
            curr_dfs_node.neighbors.append(dfs_node(curr_dfs_node.cumul_seq + nucleotide, curr_dfs_node.remain_seq[1:]))

        for neighbor in curr_dfs_node.neighbors:
            if neighbor.visited == False:
                dfs_expand_seq(neighbor, cum_list)

    elif len(curr_dfs_node.remain_seq) == 0:
        cum_list.append(curr_dfs_node.cumul_seq)


def expand_seq(seq):
    expanded_list = []
    start_node = dfs_node('', seq)
    dfs_expand_seq(start_node, expanded_list)
    return expanded_list


if __name__ == '__main__':
    import sys
    from Bio import SeqIO
    if len(sys.argv) == 3:
        inhandle = open(sys.argv[1], 'r')
        outhandle = open(sys.argv[2], 'w')
    else:
        if len(sys.argv) == 2:
            inhandle = open(sys.argv[1], 'r')
            outhandle = sys.stdout
        elif len(sys.argv) == 1:
            inhandle = sys.stdin
            outhandle = sys.stdout
        for record in SeqIO.parse(inhandle, 'fasta'):
            seq = record.seq.tostring().upper()
            expanded_seqs = expand_seq(seq)
            for i, s in enumerate(expanded_seqs):
                outhandle.write('>%s|%i\n%s\n' % (record.description, i + 1, s))