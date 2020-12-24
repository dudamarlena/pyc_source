# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/plink_pipeline/make_tped.py
# Compiled at: 2010-07-13 13:48:51
__doc__ = 'usage %prog [options]\n\nMake a tped (transposed ped) file from apt-probeset-genotype -style calls and confs file'
from __future__ import division
import optparse, sys, re, os
from mpgutils import utils
lstRequiredOptions = [
 'metadir', 'plateroot']

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-p', '--plateroot', help='(Required) Contains folders with larry-bird style files')
    parser.add_option('-x', '--metadir', help='(Required) Meta_directory with GenomeWidemap')
    parser.add_option('-c', '--chip', default=6, help='Chip type analysis was run on')
    parser.add_option('-b', '--build', default=18, help='Human Genome Build used')
    parser.add_option('-n', '--outputname', default='Output', help='define the file name root for the output files')
    parser.add_option('-o', '--outputdir', help='define the directory for output files')
    parser.add_option('-t', '--threshold', type='float', default=0.1, help='A call with confidence value above this threshold is considered a no-call.')
    parser.add_option('-a', '--allelemap', default=True, help='Convert Probes to Alleles')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    if not dctOptions.outputdir:
        setattr(dctOptions, 'outputdir', sys.path[0])
    lstOptionsToCheck = ['plateroot', 'outputdir', 'metadir']
    utils.validatePathArgs(dctOptions, lstOptionsToCheck, True)
    pattern = re.compile('[.]merged[.]diploid', re.IGNORECASE)
    CallsPaths = utils.findFiles(dctOptions.plateroot, pattern)
    pattern = re.compile('[.]merged[.]fawkes[.]confs', re.IGNORECASE)
    ConfsPaths = utils.findFiles(dctOptions.plateroot, pattern)
    fCalls = open(CallsPaths[0])
    fConfs = open(ConfsPaths[0])
    pattern = re.compile('genomewidesnp_' + str(dctOptions.chip) + '[.]hg' + str(dctOptions.build) + '[.]map', re.IGNORECASE)
    map_files = utils.findFiles(dctOptions.metadir, pattern)
    if map_files:
        fMap = open(map_files[0])
    else:
        print '****No GenomeWide Map **** '
        sys.exit(1)
    if dctOptions.allelemap:
        pattern = re.compile('genomewidesnp_' + str(dctOptions.chip) + '_alleles[.]csv', re.IGNORECASE)
        allele_files = utils.findFiles(dctOptions.metadir, pattern)
        if allele_files:
            dctAlleleMap = utils.readAllelesFile(allele_files[0])
        else:
            print '****No Allele Map found, disabling Probe to Allele conversion**** '
            dctAlleleMap = {}
            setattr(dctOptions, 'allelemap', False)
    strHeader = utils.skipHeader(fCalls, 'probeset_id')
    iNumSamples = len(strHeader.split()) - 1
    strConfsHeader = utils.skipHeader(fConfs, 'probeset_id')
    if strHeader != strConfsHeader:
        raise Exception('Mismatch between calls and confs header lines')
    makePedFile(fCalls, fConfs, fMap, dctAlleleMap, iNumSamples, dctOptions)
    fCalls.close()
    fConfs.close()
    fMap.close()
    print 'Finished -- Make_Tped.Py\n'
    return


def makePedFile(fCalls, fConfs, fMap, dctAlleleMap, iNumSamples, dctOptions):
    fOut = open(os.path.join(dctOptions.outputdir, dctOptions.outputname + '.tped'), 'w')
    for strLine in fCalls:
        lstCalls = strLine.split()
        snp_id = lstCalls[0]
        lstCalls.pop(0)
        if dctOptions.allelemap:
            probeA = dctAlleleMap[snp_id][0]
            probeB = dctAlleleMap[snp_id][1]
        else:
            probeA = 'A'
            probeB = 'B'
        if len(lstCalls) != iNumSamples:
            raise Exception('Wrong number of calls on this line: ' + strLine)
        strConfs = fConfs.readline()
        lstConfs = [ float(val) for val in strConfs.split()[1:] ]
        if len(lstConfs) != iNumSamples:
            raise Exception('Wrong number of confidences on this line: ' + strConfs)
        strMap = fMap.readline()
        if strMap == '':
            raise Exception('Map file wrong for SNP: ' + snp_id)
        lstMap = strMap.split()
        lstOut = lstMap[:]
        for (i, strCall) in enumerate(lstCalls):
            if lstConfs[i] > dctOptions.threshold:
                strCall = '-1'
            if strCall == '-1':
                lstOut += ['0 0']
            elif strCall == '0':
                lstOut += [probeA + ' ' + probeA]
            elif strCall == '1':
                lstOut += [probeA + ' ' + probeB]
            elif strCall == '2':
                lstOut += [probeB + ' ' + probeB]
            else:
                raise Exception("Strange call '" + strCall + "' on line: " + strLine)

        print >> fOut, ('\t').join(lstOut)

    if fMap.readline() != '':
        raise Exception('Extra lines in map file')
    if fConfs.readline() != '':
        raise Exception('Extra lines in confs file')
    fOut.close()


if __name__ == '__main__':
    sys.exit(main())