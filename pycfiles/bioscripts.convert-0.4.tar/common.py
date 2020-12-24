# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/f0/paul/Projects/Bioscripts/bioscripts.convert/bioscripts/convert/common.py
# Compiled at: 2011-08-09 09:50:01
"""
Functions shared between scripts.

"""
__docformat__ = 'restructuredtext en'
from os import path
from optparse import OptionParser
from defs import *
__all__ = [
 'make_optparser']

def parse_args(name):
    """
        Construct the optparser for either script.
        
        Since they have an identical API, just pass a name for the descriptions.
        """
    usage = '%prog [opts] FORMAT INFILES ...'
    version = 'version %s' % VERSION
    optparser = OptionParser(usage=usage, version=version, epilog=EPILOG)
    optparser.add_option('--input-format', '-i', dest='input_format', help='The format of the input %s files. If not supplied, this will be\n\t\t\tinferred from the extension of the files.' % name, metavar='FORMAT', default='')
    optparser.add_option('--output-extension', '-e', dest='output_extension', help='The extension of the output %s files. If not supplied,\n\t\tthis will be inferred from the output format.' % name, metavar='EXTENSION', default='')
    optparser.add_option('--seqtype', '-t', dest='seqtype', help='The type of sequence (dna or protein) being converted. Often\n\t\t\tthis can be inferred from the input file, but sometimes must be\n\t\t\texplicitly set.', default='', metavar='TYPE')
    (opts, pargs) = optparser.parse_args()
    if len(pargs) < 1:
        optparser.error('No output format specified')
    out_fmt = pargs[0].strip().lower()
    if out_fmt not in KNOWN_FMTS:
        optparser.error('unknown output format')
    if opts.input_format and opts.input_format not in KNOWN_FMTS:
        optparser.error('unknown input format')
    infiles = pargs[1:]
    if not infiles:
        optparser.error('No input files specified')
    seqtype = opts.seqtype.strip().lower()
    if opts.seqtype not in ('dna', 'protein', ''):
        optparser.error('unknown sequence type')
    elif opts.seqtype == 'dna':
        alphabet = BIOSEQ_ALPHABET_DNA
    elif opts.seqtype == 'protein':
        alphabet = BIOSEQ_ALPHABET_PROTEIN
    else:
        alphabet = None
    opts.seqtype = alphabet
    return (
     out_fmt, infiles, opts)


def dir_base_ext(in_path):
    (dir_name, file_name) = path.split(in_path)
    (base_name, orig_ext) = path.splitext(file_name)
    if orig_ext.startswith('.'):
        orig_ext = orig_ext[1:]
    return (
     dir_name, base_name, orig_ext)


def make_out_path(dir_name, base_name, ext):
    return path.join(dir_name, '%s.%s' % (base_name, ext))