# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/plink_pipeline/birdseye_to_cnv.py
# Compiled at: 2010-07-13 12:32:44
import optparse
from mpgutils import utils
import sys, os, re
dctCelFileMap = {}
dctFamMap = {}
dctFamMissing = {}

def main(argv=None):
    if not argv:
        argv = sys.argv
    lstRequiredOptions = [
     'familyfile', 'plateroot']
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-p', '--plateroot', help='(Required) Contains folders with larry-bird style files')
    parser.add_option('-f', '--familyfile', help='(Required) PLINK formatted .fam file')
    parser.add_option('-d', '--outputdir', help='(Required) Define the directory for output files')
    parser.add_option('-m', '--celmap', help='Cel Map file')
    parser.add_option('-n', '--outputname', default='Output', help='Define the file name root for the output files')
    parser.add_option('-q', '--quiet', action='store_false')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    if not dctOptions.outputdir:
        setattr(dctOptions, 'outputdir', sys.path[0])
    lstOptionsToCheck = [
     'familyfile', 'plateroot', 'outputdir']
    if dctOptions.celmap:
        lstOptionsToCheck.append('celmap')
    utils.validatePathArgs(dctOptions, lstOptionsToCheck, True)
    fOut = open(os.path.join(dctOptions.outputdir, dctOptions.outputname + '.cnv'), 'w')
    fOut.write('FID\tIID\tCHR\tBP1\tBP2\tTYPE\tSCORE\tSITE\n')
    dctFamMap = utils.readFamFile(dctOptions.familyfile)
    if dctOptions.celmap:
        dctCelMap = utils.readCelMapFile(dctOptions.celmap)
    else:
        dctCelMap = {}
    pattern = re.compile('[.]birdseye_calls', re.IGNORECASE)
    BirdsEyePaths = utils.findFiles(dctOptions.plateroot, pattern)
    for BirdsEyePath in BirdsEyePaths:
        BirdsEyeCallFile = open(BirdsEyePath)
        ReadPlateFile(BirdsEyeCallFile, fOut, dctOptions, dctFamMap, dctFamMissing, dctCelMap)

    if not dctOptions.quiet and len(dctFamMissing.keys()) > 0:
        print '\tFound individuals not in the Family Data:'
        for indiv in dctFamMissing.keys():
            print '\t' + indiv

    print 'Finished -- Birdseye_To_Cnv.Py\n'


def ReadPlateFile(BirdsEyeCallFile, fOut, dctOptions, dctFamMap, dctFamMissing, dctCelMap):
    header_complete = False
    for strLine in BirdsEyeCallFile:
        Fields = strLine.split()
        if header_complete == False:
            header_complete = True
            continue
        IID = utils.stripCelExt(Fields[0])
        if dctOptions.celmap:
            if dctCelMap.has_key(IID):
                IID = dctCelMap[IID]
        if dctFamMap.has_key(IID):
            FID = dctFamMap[IID][0]
        elif not dctFamMissing.has_key(IID):
            dctFamMissing[IID] = True
        continue
        Type = Fields[2]
        Chrom = Fields[3]
        SPos = Fields[4]
        EPos = Fields[5]
        Score = Fields[9]
        if Score == '-Inf':
            Score = 0
            continue
        Site = Fields[8]
        if Site == '-Inf':
            Site = 0
            continue
        fOut.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (FID, IID, Chrom, SPos, EPos, Type, Score, Site))


if __name__ == '__main__':
    main()