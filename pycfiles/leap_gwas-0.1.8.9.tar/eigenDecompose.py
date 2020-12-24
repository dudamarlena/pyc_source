# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/omerw/git/leap/leap/regression/eigenDecompose.py
# Compiled at: 2015-04-03 03:44:17
import numpy as np, argparse, scipy.linalg as la, time, leapUtils, scipy.linalg.blas as blas, leapMain
np.set_printoptions(precision=3, linewidth=200)

def eigenDecompose(bed, outFile=None):
    bed = leapUtils._fixupBed(bed)
    t0 = time.time()
    print 'Computing kinship matrix...'
    XXT = leapUtils.symmetrize(blas.dsyrk(1.0, bed.val, lower=1)) / bed.val.shape[1]
    print 'Done in %0.2f' % (time.time() - t0), 'seconds'
    S, U = leapUtils.eigenDecompose(XXT)
    if outFile is not None:
        np.savez_compressed(outFile, arr_0=U, arr_1=S, XXT=XXT)
    eigen = dict([])
    eigen['XXT'] = XXT
    eigen['arr_0'] = U
    eigen['arr_1'] = S
    return eigen


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bfilesim', metavar='bfilesim', default=None, help='Binary plink file')
    parser.add_argument('--extractSim', metavar='extractSim', default=None, help='SNPs subset to use')
    parser.add_argument('--out', metavar='out', default=None, help='output file')
    parser.add_argument('--pheno', metavar='pheno', default=None, help='Phenotypes file (optional), only used for identifying unphenotyped individuals')
    parser.add_argument('--missingPhenotype', metavar='missingPhenotype', default='-9', help='identifier for missing values (default: -9)')
    args = parser.parse_args()
    if args.bfilesim is None:
        raise Exception('bfilesim must be supplied')
    if args.out is None:
        raise Exception('output file name must be supplied')
    bed, _ = leapUtils.loadData(args.bfilesim, args.extractSim, args.pheno, args.missingPhenotype, loadSNPs=True)
    leapMain.eigenDecompose(bed, args.out)