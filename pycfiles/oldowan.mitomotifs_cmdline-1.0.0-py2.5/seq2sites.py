# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-ppc/egg/oldowan/mitomotifs_cmdline/seq2sites.py
# Compiled at: 2008-08-16 22:10:12
import os, sys
from optparse import OptionParser
from oldowan.mitomotifs import seq2sites
from oldowan.mitomotifs import sites2str
from oldowan.fasta import fasta

def run_command():
    """Transform human mtDNA sequence to variable sites."""
    usage = 'usage: %prog [options] filename'
    parser = OptionParser(usage=usage)
    parser.add_option('-a', '--ambig-cutoff', dest='ambig_cutoff', type='int', default=10, help='how many ambiguous sites are acceptable')
    parser.add_option('-w', '--word-size', dest='word_size', type='int', default=15, help='word size in alignment (not generally changed)')
    parser.add_option('-m', '--mismatch-cutoff', dest='mismatch_cutoff', type='float', default=0.7, help='mismatch cutoff for alignment (not generally changed)')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print 'You must provide a filename!'
        print "Type 'seq2sites -h' for help."
        sys.exit(1)
    if not os.path.exists(args[0]):
        print 'ERROR: Could not find file: %s' % args[0]
        sys.exit(1)
    for entry in fasta(args[0], 'r'):
        sites = seq2sites(entry['sequence'], word_size=options.word_size, mismatch_cutoff=options.mismatch_cutoff, ambig_cutoff=options.ambig_cutoff)
        print '"%s","%s"' % (entry['name'], sites2str(sites))