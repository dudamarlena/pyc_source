# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncPac/parse.py
# Compiled at: 2019-09-13 20:43:43
# Size of source mod 2**32: 719 bytes
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='LncPac')
    parser.add_argument('-m', '--model', help='please choose a prediction model ', required=True)
    parser.add_argument('-o', '--output', help='output file name')
    parser.add_argument('-i', '--input', dest='fasta', help='input file', required=True, default='fasta')
    parser.add_argument('-r', '--reverse', help='also check the reverse strand')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    output = args.output
    backup = args.backup
    filepath = args.filepath
    project = args.project