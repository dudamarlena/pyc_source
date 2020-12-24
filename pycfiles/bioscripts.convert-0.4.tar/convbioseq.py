# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/f0/paul/Projects/Bioscripts/bioscripts.convert/bioscripts/convert/convbioseq.py
# Compiled at: 2011-08-10 10:19:17
"""
Convert biosequences from one format to another.

"""
__docformat__ = 'restructuredtext en'
__author__ = 'Paul-Michael Agapow <agapow@bbsrc.ac.uk>'
from exceptions import BaseException
from Bio import SeqIO, AlignIO
from defs import *
import common
try:
    from bioscripts.convert import __version__
except:
    __version__ = 'unknown'

def main():
    (out_fmt, infiles, opts) = common.parse_args('biosequence')
    for in_path in infiles:
        (dir, base, ext) = common.dir_base_ext(in_path)
        in_fmt = (opts.input_format or EXT_TO_FORMAT.get(ext, '')).lower()
        assert in_fmt, 'no known input format specified'
        out_path = common.make_out_path(dir, base, opts.output_extension or FORMAT_TO_EXT[out_fmt])
        in_hndl = open(in_path, 'rb')
        in_seqs = [ x for x in SeqIO.parse(in_hndl, in_fmt) ]
        in_hndl.close()
        assert in_seqs, 'No sequences read from %s. Perhaps the file is not in %s format.' % (file_name, in_fmt)
        out_hndl = open(out_path, 'wb')
        if opts.seqtype:
            for s in in_seqs:
                s.alphabet = opts.seqtype

        if out_fmt in ('nexus', ):
            from Bio.Align import MultipleSeqAlignment
            aln = MultipleSeqAlignment(in_seqs, alphabet=opts.seqtype or BIOSEQ_ALPHABET_PROTEIN)
            AlignIO.write(aln, out_hndl, out_fmt)
        else:
            SeqIO.write(in_seqs, out_hndl, out_fmt)
        out_hndl.close()


if __name__ == '__main__':
    try:
        main()
    except BaseException, err:
        if _DEV_MODE:
            raise
        else:
            print err
    except:
        print 'An unknown error occurred.\n'