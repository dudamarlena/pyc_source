# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/omerw/git/leap/leap/findRelated.py
# Compiled at: 2014-12-25 11:37:34
import numpy as np, argparse, time, scipy.linalg.blas as blas, leapUtils
np.set_printoptions(precision=3, linewidth=200)
import leapMain

def findRelated(bed, outFile, cutoff):
    bed = leapUtils._fixupBed(bed)
    keepArr = leapUtils.findRelated(bed, cutoff)
    if outFile is not None:
        print 'Printing output to', outFile
        f = open(outFile, 'w')
        for i, (fid, iid) in enumerate(bed.iid):
            if keepArr[i]:
                f.write(fid + ' ' + iid + ' 0\n')
            else:
                f.write(fid + ' ' + iid + ' 1\n')

        f.close()
    return keepArr


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bfilesim', metavar='bfilesim', default=None, help='Binary plink file')
    parser.add_argument('--extractSim', metavar='extractSim', default=None, help='extractSim file')
    parser.add_argument('--cutoff', metavar='cutoff', type=float, default=0.05, help='Relationship cutoff (default 0.05)')
    parser.add_argument('--out', metavar='out', default=None, help='output file')
    parser.add_argument('--pheno', metavar='pheno', default=None, help='Phenotypes file (optional), only used for identifying unphenotyped individuals')
    parser.add_argument('--missingPhenotype', metavar='missingPhenotype', default='-9', help='identifier for missing values (default: -9)')
    args = parser.parse_args()
    if args.bfilesim is None:
        raise Exception('bfilesim must be supplied')
    if args.out is None:
        raise Exception('output file name must be supplied')
    bed, _ = leapUtils.loadData(args.bfilesim, args.extractSim, args.pheno, args.missingPhenotype, loadSNPs=True, standardize=True)
    leapMain.findRelated(bed, args.out, args.cutoff)