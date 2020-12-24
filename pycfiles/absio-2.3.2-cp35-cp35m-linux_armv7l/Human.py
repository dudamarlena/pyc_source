# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/seq/seq/Human.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = "\nFast access to human sequence data in fasta format.\n\nThe human genome doesn't fit in the memory of many computers\nin text format.  This interface provides a quick way to extract\narbitrary pieces of sequence from disk.\n\n   Usage:\n\nfrom TAMO.Seq.Human import get_seq\n\ntxt = get_seq('chr1',5678910,5778910)\n# -or -\ntxt = get_seq(1,5678910,5778910)\n\ntxt = get_seq('chrX',5678910,5778910)\n# -or -\ntxt = get_seq('X',5678910,5778910)\n\n#-or-\n\ntxt = get_seq('chrX:5679010-567890')\n\nCopyright (2005) Whitehead Institute for Biomedical Research (except as noted below)\nAll Rights Reserved\n\nAuthor: David Benjamin Gordon\n"
import TAMO.paths
CHROMOROOT = TAMO.paths.HumanSeqdir
ChrD = {}

class ChromoFasta:
    """
    Rapid access into large Human Chromosome Files.  Index positions should
    be taken directly from BLAST/BLAT output (no +/-1, or pythonish adding 1
    to get the last letter.
    """

    def __init__(self, chromosome):
        if type(chromosome) != type('') or chromosome.find('chr') != 0:
            chromosome = 'chr%s' % chromosome
        self.chromo = chromosome
        self.file = '%s/%s.fa' % (CHROMOROOT, self.chromo)
        TAMO.paths.CHECK(self.file, 'Human')
        self.FID = open(self.file)
        self.sniff_info()

    def __del__(self):
        self.FID.close()

    def sniff_info(self):
        self.FID.seek(0)
        head = self.FID.readline()
        first = self.FID.readline()
        self.offset = len(head)
        self.linelen = len(first) - 1

    def get_range(self, start, end):
        startoffset = self.compute_offset(start)
        endoffset = self.compute_offset(end) + 1
        self.FID.seek(startoffset)
        text = self.FID.read(endoffset - startoffset)
        text = text.replace('\n', '')
        return text

    def compute_offset(self, idx):
        """
        compute_offset(idx)

        Example:  If pos = 246, and linelen = 50,
        then linenum = int(246 / 50)  = 4
        endpos       = 246 - ( 4* 50) = 46

        but each line actually contains a "
" at the end,
        and the count starts at self.offset, so the seek
        position is:
        
        self.offset + linenum * (self.linelen + 1) + endpos - 1  #Counting from 1
        """
        linenum = int(idx / self.linelen)
        endpos = idx - linenum * self.linelen
        ans = self.offset + linenum * (self.linelen + 1) + endpos - 1
        return ans


def get_seq(chr, start=None, end=None):
    """
    txt = get_seq('chr1',5678910,5778910)
    # -or -
    txt = get_seq(1,5678910,5778910)
    
    txt = get_seq('chrX',5678910,5778910)
    # -or -
    txt = get_seq('X',5678910,5778910)
    
    #-or-
    
    txt = get_seq('chrX:5679010-567890')
    """
    if type(chr) != type('') or chr.find('chr') != 0:
        chr = 'chr%s' % chr
    if start == None and chr.find(':') > 0:
        _chr, _range = chr.split(':')
        chr = _chr
        start, end = _range.split('-')
        start, end = int(start), int(end)
    if not ChrD.has_key(chr):
        ChrD[chr] = ChromoFasta(chr)
    return ChrD[chr].get_range(start, end)