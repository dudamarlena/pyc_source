# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plink_pipeline/birdseye_merger.py
# Compiled at: 2008-12-16 12:10:22
import sys, numpy
from numpy import *

def main(argv=None):
    if not argv:
        argv = sys.argv
    lstRequiredOptions = ['plateroot']
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-p', '--plateroot', help='(Required) Define the directory where the data plate info resides')
    parser.add_option('-o', '--outputdir', help='Define the directory for output files')
    parser.add_option('-n', '--outputname', default='Output', help='define the file name root for the output files')
    parser.add_option('-l', '--lodcut', default=5, help='define a cutoff for confidence data')
    parser.add_option('-m', '--sizecut', help='CNV size cutoff')
    parser.add_option('-q', '--quiet', action='store_true', dest='quiet')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    if not dctOptions.outputdir:
        setattr(dctOptions, 'outputdir', sys.path[0])
    lstOptionsToCheck = ['familyfile', 'plateroot', 'outputdir']
    if dctOptions.celmap:
        lstOptionsToCheck.append('celmap')
    utils.validatePathArgs(dctOptions, lstOptionsToCheck, True)
    LOD_cutoff = float(sys.argv[3])
    size_cutoff = float(sys.argv[4])
    remainingsegments = pylab.load(sys.argv[1], delimiter='\t', skiprows=1, usecols=range(1, 10))
    outfile = sys.argv[2]
    fileout = open(outfile, 'w')
    num2id = {}
    f = open(sys.argv[1], 'r')
    f.readline()
    for line in f:
        values = line.split()
        num2id[int(values[1])] = values[0]

    f.close()
    format = [
     '%d', '%d', '%d', '%d', '%d', '%0.2f', '%d', '%d', '%0.2f']
    numsegsleft = size(remainingsegments, 0)
    while numsegsleft > 0:
        i = 1
        while i < numsegsleft and remainingsegments[(i, 0)] == remainingsegments[(i - 1, 0)] and remainingsegments[(i, 2)] == remainingsegments[(i - 1, 2)]:
            i += 1

        segments = remainingsegments[0:i, :]
        remainingsegments = remainingsegments[i:numsegsleft, :]
        numsegsleft = size(remainingsegments, 0)
        normal = 2
        if segments[(0, 2)] == 23:
            if sum(segments[(segments[:, 1] == 1, 6)]) > sum(segments[(segments[:, 1] == 2, 6)]):
                normal = 1
        segind = argmin(segments[:, 8])
        while segments[(segind, 8)] < LOD_cutoff:
            prevind = segind - 1
            nextind = segind + 1
            if prevind >= 0 and nextind < size(segments, 0):
                if (segments[(prevind, (0, 1, 2))] == segments[(nextind, (0, 1, 2))]).all():
                    segments[prevind, :] = mergesegments(segments[(prevind, segind, nextind), :])
                    segments = segments[r_[(arange(0, segind), arange(nextind + 1, size(segments, 0)))], :]
                else:
                    segments = segments[r_[(arange(0, segind), arange(nextind, size(segments, 0)))], :]
            else:
                segments = segments[r_[(arange(0, segind), arange(nextind, size(segments, 0)))], :]
            if size(segments, 0) == 0:
                break
            segind = argmin(segments[:, 8])

        if size(segments, 0) == 0:
            continue
        temp = where((segments[:, 6] < size_cutoff) & (segments[:, 1] == normal))
        poppablesegments = temp[0]
        while size(poppablesegments) > 0:
            segind = poppablesegments[argmin(segments[(poppablesegments, 8)])]
            prevind = segind - 1
            nextind = segind + 1
            if prevind >= 0 and nextind < size(segments, 0):
                if (segments[(prevind, (0, 1, 2))] == segments[(nextind, (0, 1, 2))]).all() and segments[(prevind, 8)] + segments[(nextind, 8)] - segments[(segind, 8)] >= LOD_cutoff:
                    segments[prevind, :] = mergesegments(segments[(prevind, segind, nextind), :])
                    segments = segments[r_[(arange(0, segind), arange(nextind + 1, size(segments, 0)))], :]
                else:
                    segments = segments[r_[(arange(0, segind), arange(nextind, size(segments, 0)))], :]
            else:
                segments = segments[r_[(arange(0, segind), arange(nextind, size(segments, 0)))], :]
            temp = where((segments[:, 6] < size_cutoff) & (segments[:, 1] == normal))
            poppablesegments = temp[0]

        if size(segments, 0) == 0:
            continue
        temp = where((segments[:, 6] >= size_cutoff) & (segments[:, 1] != normal))
        segments = segments[temp[0], :]
        print2darraytofile(fileout, segments, format)

    fileout.close()


def mergesegments(segments):
    newsegment = zeros(size(segments, 1))
    newsegment[0:3] = segments[0, 0:3]
    newsegment[3] = segments[(0, 3)]
    newsegment[4] = segments[(2, 4)]
    newsegment[6] = newsegment[4] - newsegment[3]
    newsegment[7] = sum(segments[0:3, 7])
    if newsegment[7] >= 1000:
        newsegment[8] = newsegment[7]
        newsegment[5] = newsegment[7]
    else:
        newsegment[8] = segments[(0, 8)] + segments[(2, 8)] - segments[(1, 8)]
        newsegment[5] = 10 ** (newsegment[8] / newsegment[7])
    return newsegment


def print1darraytofile(fileout, row, format):
    assert size(row) == size(format)
    outstring = num2id[row[0]]
    for i in range(0, numcols):
        outstring = outstring + '\t' + format[i] % row[i]

    print >> fileout, outstring


def print2darraytofile(fileout, segments, format):
    if size(shape(array)) == 1:
        print1darraytofile(fileout, segments, format)
        return
    numcols = size(segments, 1)
    assert numcols == size(format)
    for row in segments:
        outstring = num2id[row[0]]
        for i in range(0, numcols):
            outstring = outstring + '\t' + format[i] % row[i]

        print >> fileout, outstring


def print1darray(row, format):
    assert size(row) == size(format)
    outstring = num2id[row[0]]
    for i in range(0, numcols):
        outstring = outstring + '\t' + format[i] % row[i]

    print outstring


def print2darray(segments, format):
    if size(shape(segments)) == 1:
        print1darray(segments, format)
        return
    numcols = size(segments, 1)
    assert numcols == size(format)
    for row in segments:
        outstring = num2id[row[0]]
        for i in range(0, numcols):
            outstring = outstring + '\t' + format[i] % row[i]

        print outstring


if __name__ == '__main__':
    main()