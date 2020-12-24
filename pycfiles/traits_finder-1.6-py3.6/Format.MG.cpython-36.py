# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/Format.MG.py
# Compiled at: 2019-06-23 00:07:35
# Size of source mod 2**32: 1539 bytes
import argparse, os
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-i', help='input dir',
  type=str,
  default='.',
  metavar='current dir (.)')
parser.add_argument('-f', help='input filename',
  type=str,
  default='input.faa',
  metavar='input.faa')
args = parser.parse_args()

def hmmformat(hmmresult):
    f1 = open(hmmresult + '2.txt', 'a')
    for line in open(hmmresult, 'r'):
        if str(line)[0] == '#':
            pass
        else:
            line = str(line).replace(' # ', '#')
            while line != str(line).replace('  ', ' '):
                line = str(line).replace('  ', ' ')

            line = str(line).replace(' ', '\t')
            line = str(line).replace('#', ' # ')
            filedir, filename = os.path.split(hmmresult)
            filename = filename.split('.hmm')[0]
            f1.write(filename + '_' + line)

    f1.close()


hmmformat(os.path.join(args.i, args.f))