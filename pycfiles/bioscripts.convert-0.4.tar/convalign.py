# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/f0/paul/Projects/Bioscripts/bioscripts.convert/bioscripts/convert/convalign.py
# Compiled at: 2011-08-10 10:51:58
"""
Convert alignments from one format to another.

"""
__docformat__ = 'restructuredtext en'
from exceptions import BaseException
from Bio import AlignIO
from defs import *
import common
try:
    from bioscripts.convert import __version__
except:
    __version__ = 'unknown'

def main():
    (out_fmt, infiles, opts) = common.parse_args('alignment')
    for in_path in infiles:
        (dir, base, ext) = common.dir_base_ext(in_path)
        in_fmt = (opts.input_format or EXT_TO_FORMAT.get(ext, '')).lower()
        assert in_fmt, 'no known input format specified'
        out_path = common.make_out_path(dir, base, opts.output_extension or FORMAT_TO_EXT[out_fmt])
        in_hndl = open(in_path, 'rb')
        in_alns = [ x for x in AlignIO.parse(in_hndl, in_fmt) ]
        in_hndl.close()
        assert in_alns, 'No alignments read from %s. Perhaps the file is not in %s format.' % (file_name, in_fmt)
        out_hndl = open(out_path, 'wb')
        if opts.seqtype:
            for s in in_alns:
                s._alphabet = opts.seqtype

        AlignIO.write(in_alns, out_hndl, out_fmt)
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