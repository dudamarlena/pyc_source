# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uta/parsers/seqgene.py
# Compiled at: 2014-08-27 16:21:43
import csv, itertools
from uta.exceptions import *

class SeqGeneParser(object):
    """parse mapping data as from ftp.ncbi.nih.gov/genomes/MapView/Homo_sapiens/sequence/current/initial_release/seq_gene.md.gz"""

    def __init__(self, fh, filter=None):
        self._fh = fh
        self._filter = filter if filter else (lambda r: True)
        header = self._fh.next().rstrip()
        if header != '#tax_id\tchromosome\tchr_start\tchr_stop\tchr_orient\tcontig\tctg_start\tctg_stop\tctg_orient\tfeature_name\tfeature_id\tfeature_type\tgroup_label\ttranscript\tevidence_code':
            raise UTAError(("file doesn't contain expected header; got:\n{header}").format(header=header))
        fields = header.replace('#', '').split('\t')
        self._csvreader = csv.DictReader(self._fh, fieldnames=fields, delimiter='\t')

    def __iter__(self):
        return self

    def next(self):
        for r in self._csvreader:
            if self._filter(r):
                return r

        raise StopIteration


if __name__ == '__main__':
    import gzip, prettytable, IPython, sys
    fh = gzip.open(sys.argv[1])
    nm_filter = lambda r: r['transcript'].startswith('NM_')
    sgparser = SeqGeneParser(fh, filter=nm_filter)
    slurp = list(sgparser)
    slurp.sort(key=lambda r: (r['transcript'], r['group_label'], r['chr_start'], r['chr_stop']))
    iter = itertools.groupby(slurp, key=lambda r: (r['transcript'], r['group_label']))
    for k, i in iter:
        print (
         k, len(list(i)))