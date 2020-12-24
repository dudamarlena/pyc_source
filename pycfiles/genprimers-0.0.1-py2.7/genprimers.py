# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/lib/genprimers.py
# Compiled at: 2017-03-26 22:13:47
from lib import parse_args
from lib import PrimersGenerator
from list_module import list_sequences

def primers(args):
    """
    """
    pg = PrimersGenerator(args)
    pg.run_pipeline()


def index(args):
    """
    """
    pass


def list_seqs(args):
    """
    """
    list_sequences(args.list_fasta)


def main():
    args = parse_args()
    if args.subparser_name == 'primers':
        primers(args)
    elif args.subparser_name == 'index':
        index(args)
    else:
        list_seqs(args)