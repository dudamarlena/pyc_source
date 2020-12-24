# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\vep_core\Serendip\MikeTM.py
# Compiled at: 2014-10-17 12:17:08
__author__ = 'Mike Gleicher'
defaultMetadataDir = 'C:/Users/Eric/Documents/Madison/VEP_Core/vep_core/Data/Metadata'
defaultModel = 'ShakespeareChunkedOptimized_50'
import numpy as N, scipy.stats as SS, csv
from collections import Counter, defaultdict

def buildPath(metadataDir=defaultMetadataDir, modelName=defaultModel, filename=''):
    return '%s/%s/TopicModel/%s' % (metadataDir, modelName, filename)


def readMatrix(metadataDir=defaultMetadataDir, model=defaultModel, file='theta.csv'):
    """
    read a full matrix - tricky part, we don't know how big
    also keeps a bunch of stats handy - so it returns multiple things

    as a DICTIONARY so you can remember what it is
    :param file:
    :return:
    """
    with open(buildPath(metadataDir, model, file)) as (fi):
        spm = []
        maxc = -1
        nz = 0
        maxV = 0
        minV = 1
        sread = csv.reader(fi)
        for row in sread:
            srow = []
            for i in range(len(row) / 2):
                c = int(row[(i * 2)])
                v = float(row[(i * 2 + 1)])
                if c > maxc:
                    maxc = c
                if v > maxV:
                    maxV = v
                if v < minV:
                    minV = v
                srow.append((c, v))
                nz += 1

            spm.append(srow)

        nrows = len(spm)
        ncols = maxc + 1
        print '%s: %d rows, %d columns, %d non-zeros (%4.1f%%) range[%g %g]' % (
         file, nrows, ncols, nz, 100.0 * float(nz) / float(ncols * nrows), maxV, minV)
        matr = N.zeros((nrows, ncols))
        for row, spr in enumerate(spm):
            for sv in spr:
                matr[(row, sv[0])] = sv[1]

        return {'matrix': matr, 'sparse-matrix': spm, 'non-zeros': nz, 'nz-range': (minV, maxV)}


class TopicModel:

    def __init__(self, metadataDir=defaultMetadataDir, model=defaultModel):
        self.name = model
        self.thetaD = readMatrix(metadataDir, model, 'theta.csv')
        self.theta = self.thetaD['matrix']
        self.thetaKD = None
        metadatafname = buildPath(metadataDir, model, 'metadata.csv')
        with open(metadatafname) as (mf):
            r = csv.reader(mf, skipinitialspace=True)
            self.metadatacols = r.next()
            skipline = r.next()
            datalines = [ i for i in r ]
        self.metadata = N.core.records.fromrecords(datalines, names=self.metadatacols)
        self.metadatacounts = dict()
        for k in self.metadatacols:
            self.metadatacounts[k] = Counter(self.metadata.field(k))

        return

    def groupByCol(self, colName):
        """
        returns a dictionary of all values of the column, each with a list of which rows have that value
        :param colName:
        :return:
        """
        lst = self.metadata.field(colName)
        groups = defaultdict(list)
        for i, r in enumerate(lst):
            groups[r].append(i)

        return groups

    def matricesByCol(self, colName, matrix=None):
        """
        returns a dictionary of matrices, one matrix per group in the column

        :param colName:
        :return:
        """
        if matrix == None:
            matrix = self.theta
        groups = self.groupByCol(colName)
        matrs = dict()
        for k in groups:
            matrs[k] = matrix[groups[k]]

        return matrs

    def colorRows(self, colName):
        """
        generates the javascript that re-colors the rows according to a data column

        prints it to the console
        :param colName:
        :return: nothing
        """
        groups = self.groupByCol(colName)
        for k in groups:
            print 'colorRows(', groups[k], ', "%s");' % self.metadatacolors[colName][k]

    def anovaCols(self, colName, excludes=[]):
        """
        does the annova hueristic to order the columns to seperate ALL classes in a column
        returns the ordering list

        :param colName:
        :return:
        """
        matrs = self.matricesByCol(colName)
        matrsEx = [ matrs[m] for m in matrs if m not in excludes ]
        anovas = [ SS.f_oneway(*[ m[:, i] for m in matrsEx ]) for i in range(self.theta.shape[1]) ]
        return anovas

    def anovaColsRanks(self, colName, excludes=[]):
        avals = self.anovaCols(colName, excludes)
        fvals = [ v[0] for v in avals ]
        return list(N.argsort(fvals))

    def contrastCols(self, colName, yes, no=[]):
        if not isinstance(yes, list):
            yes = [
             yes]
        if len(no) == 0:
            no = [ x for x in self.metadatacounts[colName] if x not in yes ]
        yesI = [ i for i, v in enumerate(self.metadata.field(colName)) if v in yes ]
        noI = [ i for i, v in enumerate(self.metadata.field(colName)) if v in no ]
        print 'contrast %s (%d) with %s (%d)' % (yes, len(yesI), no, len(noI))
        yesM = self.theta[yesI]
        noM = self.theta[noI]
        anovas = [ SS.f_oneway(yesM[:, i], noM[:, i]) for i in range(self.theta.shape[1]) ]
        return anovas

    def contrastColsRanks(self, colName, yes, no=[]):
        avals = self.contrastCols(colName, yes, no)
        fvals = [ v[0] for v in avals ]
        return list(N.argsort(fvals))

    def sortColsByDistance(self, listOfCols):
        if isinstance(listOfCols, int):
            listOfCols = [
             listOfCols]
        dst = [ min([ 1 - SS.spearmanr(self.theta[:, c], self.theta[:, i])[0] for c in listOfCols ]) for i in range(self.theta.shape[1])
              ]
        return list(N.argsort(dst))