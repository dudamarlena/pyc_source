# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sling/tasks/scan.py
# Compiled at: 2019-11-01 07:27:20
import argparse, sling

def run():
    parser = argparse.ArgumentParser(description='Run hmmscan to search for hits in the genome', usage='sling scan [options] <id> <hmm_db>')
    parser.add_argument('--prep_id', help='ID of prepare run [default: same as --id]', metavar='STR')
    parser.add_argument('-c', '--cpu', type=int, help='Number of CPUs to use [%(default)s]', default=8, metavar='INT')
    parser.add_argument('-o', '--out_dir', help='Working for all the output files', metavar='PATH', default='.')
    parser.add_argument('--hmmsearch', help='HMM search executable (set to hmmscan if wish to run scan not search) [Default: hmmsearch]', metavar='STR', default='hmmsearch')
    parser.add_argument('--hmmpress', help='HMM press executable [relevant for hmmscan only] [Default: hmmpress]', metavar='STR', default='hmmpress')
    parser.add_argument('id', help='ID of scan run', metavar='STR')
    parser.add_argument('hmm_db', help='Name of the predefined HMM database ' + str(sling.utils.databases) + ' OR path to custom HMM file', metavar='STR/FILE')
    options = parser.parse_args()
    sling.scan.run(options)