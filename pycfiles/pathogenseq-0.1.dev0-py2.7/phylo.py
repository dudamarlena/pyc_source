# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/pathogenseq/phylo.py
# Compiled at: 2018-07-14 05:50:46
import sys, subprocess
from .files import *
from .fasta import *

class phylo:
    """Class for running phylogenetic anaysis

        Args:
                fa_file(str): Fasta file containing the aligned whole genomes or SNPs
                prefix(str): Prefix for your results
                threads(int): Number of threads to use for multithreaded operations (default:4)
        Returns:
                phylo: A phylo class object
        """

    def __init__(self, fa_file, prefix, threads=4):
        self.params = {}
        if filecheck(fa_file):
            self.params['fa_file'] = fa_file
            self.fasta = fasta(fa_file)
            self.params['threads'] = threads
        self.params['prefix'] = prefix

    def examl(self):
        programs_check(['raxmlHPC', 'parse-examl', 'examl'])
        log('Converting to phylip')
        self.params['phylip_file'] = '%s.phylip' % self.params['prefix']
        self.fasta.write_philip(self.params['phylip_file'])
        log('Creating starting tree')
        cmd = 'raxmlHPC -y -m GTRCAT -p 12345 -s %(fa_file)s  -n StartingTree -T %(threads)s' % self.params
        run_cmd(cmd)
        log('Creating binary file')
        cmd = 'parse-examl -s %(phylip_file)s -n %(prefix)s -m DNA' % self.params
        run_cmd(cmd)
        log('Running EXaML')
        cmd = 'examl -s %(prefix)s.binary -n examl -m PSR -D -t RAxML_parsimonyTree.StartingTree' % self.params
        run_cmd(cmd)