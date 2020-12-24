# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mhclovac/mhclovac_run.py
# Compiled at: 2019-12-11 06:05:45
# Size of source mod 2**32: 1313 bytes
"""Entry point for mhclovac"""
import sys
from mhclovac.misc import *
from mhclovac.argument_parser import parse_args

def worker(sequence, seq_name, args, output):
    sequence = str(sequence).upper()
    seq_name = str(seq_name)
    models_dict = load_models()
    standardizer, regressor = models_dict[args.hla]
    for i in range(len(sequence) - args.peptide_length + 1):
        peptide = sequence[i:i + args.peptide_length]
        X = get_feature_vector(peptide)
        X = standardizer.transform(X)
        score = regressor.predict(X)[0]
        total_score = np.power(10, score)
        line = '\t'.join([seq_name, args.hla, peptide, str(total_score)])
        output.write(line + '\n')


def run():
    args = parse_args(sys.argv[1:])
    output = open(args.output, 'w') if args.output else sys.stdout
    if args.print_header:
        print_header(output)
    if args.fasta:
        for seq_name, sequence in fasta_reader(args.fasta):
            worker(sequence, seq_name, args, output)

    else:
        if args.sequence:
            seq_name = args.sequence_name or 'unknown'
            worker(args.sequence, seq_name, args, output)
        else:
            raise RuntimeError('Must provide sequence or fasta file')


def main():
    sys.exit(run())