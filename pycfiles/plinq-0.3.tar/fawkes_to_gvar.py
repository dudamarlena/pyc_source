# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/plink_pipeline/fawkes_to_gvar.py
# Compiled at: 2010-08-11 20:51:41
import optparse, sys, os, getopt, re, shutil
from mpgutils import utils
dctIndivMap = {}
dctCallFile = {}
output_root = ''
output_name = 'Output'

def main(argv=None):
    if argv is None:
        argv = sys.argv
    lstRequiredOptions = [
     'familyfile', 'plateroot', 'metadir']
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-p', '--plateroot', dest='plateroot', help='(REQUIRED) Define the directory where the data plate info resides')
    parser.add_option('-f', '--familyfile', dest='familyfile', help='(REQUIRED) Define the directory for output files')
    parser.add_option('-x', '--metadir', help='(Required) Meta directory holding CNV data')
    parser.add_option('-n', '--outputname', default='Output', help='define the file name root for the output files')
    parser.add_option('-d', '--outputdir', help='define the directory for output files')
    parser.add_option('-t', '--threshold', default=0.1, help='define a cutoff for confidence data')
    parser.add_option('-m', '--celmap', dest='celmap', help='Cel Map file')
    parser.add_option('-c', '--chip', default=6, help='Chip Type')
    parser.add_option('-b', '--build', default=18, help='Human Genome Build')
    parser.add_option('-a', '--noallelemap', default=False, action='store_true', help='Do not convert Probes to Alleles')
    parser.add_option('-r', '--norscoding', default=False, action='store_true', help='Do not convert SNP id to RS id')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    if not dctOptions.outputdir:
        setattr(dctOptions, 'outputdir', sys.path[0])
    lstOptionsToCheck = [
     'familyfile', 'plateroot', 'outputdir', 'metadir']
    if dctOptions.celmap:
        lstOptionsToCheck.append('celmap')
    utils.validatePathArgs(dctOptions, lstOptionsToCheck, True)
    if not dctOptions.noallelemap:
        pattern = re.compile('genomewidesnp_' + str(dctOptions.chip) + '_alleles[.]csv', re.IGNORECASE)
        allele_files = utils.findFiles(dctOptions.metadir, pattern)
        if len(allele_files) > 0:
            dctAlleleMap = utils.readAllelesFile(allele_files[0])
        else:
            print '****No Allele Map Found**** '
            sys.exit(1)
    else:
        dctAlleleMap = {}
    if not dctOptions.norscoding:
        print '\tLooking SNP map: genomewidesnp_' + str(dctOptions.chip) + '.rs_snp_map'
        pattern = re.compile('genomewidesnp_' + str(dctOptions.chip) + '[.]rs_snp_map', re.IGNORECASE)
        map_files = utils.findFiles(dctOptions.metadir, pattern)
        if len(map_files > 0):
            dctMapFile = utils.readSnpMapFile(map_files[0])
        else:
            print '\t*** Could not find SNP map, disabling SNP to RS conversion ***'
            dctMapFile = {}
            setattr(dctOptions, 'norscoding', True)
    else:
        dctMapFile = {}
    pattern = re.compile('genomewidesnp_' + str(dctOptions.chip) + '[.]hg' + str(dctOptions.build) + '[.]map', re.IGNORECASE)
    map_files = utils.findFiles(dctOptions.metadir, pattern)
    map_copy = os.path.join(dctOptions.outputdir, dctOptions.outputname + '.fawkes.map')
    shutil.copy(map_files[0], map_copy)
    if dctOptions.celmap:
        dctCelMap = utils.readCelMapFile(dctOptions.celmap)
    else:
        dctCelMap = {}
    fam_copy = os.path.join(dctOptions.outputdir, dctOptions.outputname + '.fawkes.fam')
    shutil.copy(dctOptions.familyfile, fam_copy)
    dctFamMap = utils.readFamFile(dctOptions.familyfile)
    pattern = re.compile('[.]merged[.]fawkes[.]calls', re.IGNORECASE)
    CallsPaths = utils.findFiles(dctOptions.plateroot, pattern)
    pattern = re.compile('[.]merged[.]fawkes[.]confs', re.IGNORECASE)
    ConfsPaths = utils.findFiles(dctOptions.plateroot, pattern)
    if not len(CallsPaths) == len(ConfsPaths):
        print 'You are missing one or more files in your plate paths, please check file integrity'
        sys.exit(1)
    if not len(CallsPaths) > 0:
        print 'Unable to find any files'
    ProcessData(CallsPaths, ConfsPaths, dctOptions, dctCelMap, dctFamMap, dctAlleleMap, dctMapFile)
    print 'Finished -- Fawkes_To_Gvar.Py\n'
    return


def ProcessData(CallsPaths, ConfsPaths, dctOptions, dctCelMap, dctFamMap, dctAlleleMap, dctMapFile):
    fOut = open(os.path.join(dctOptions.outputdir, dctOptions.outputname + '.fawkes.gvar'), 'w')
    fOut.write('FID\tIID\tNAME\tAL1\tDOS1\tAL2\tDOS2\n')
    dctFamMissing = {}
    dropped_count = 0
    gathered_count = 0
    indiv_count = 0
    for file_number in range(len(CallsPaths)):
        CallsFile = open(CallsPaths[file_number])
        ConfsFile = open(ConfsPaths[file_number])
        calls_line = CallsFile.readline()
        confs_line = ConfsFile.readline()
        CelList = []
        calls_fields = calls_line.split()
        confs_fields = confs_line.split()
        for items in range(len(calls_fields)):
            if calls_fields[items] == confs_fields[items]:
                CelList.append(calls_fields[items])
                continue
            else:
                print 'Headers are not the same'
                sys.exit(1)

        if dctOptions.celmap:
            CelList = RemoveCels(CelList, dctOptions, dctCelMap)
        for calls_line in CallsFile:
            confs_line = ConfsFile.readline()
            calls_fields = calls_line.split()
            confs_fields = confs_line.split()
            total_indiv = 0.0
            skipped_indiv = 0.0
            snp_check = False
            if not snp_check:
                if calls_fields[0] == confs_fields[0]:
                    snp_check = True
                    snp_id = calls_fields[0]
                else:
                    print 'CNVs are not in the proper order, please verify your Birdsuite output and try again'
                    sys.exit(1)
            if dctOptions.noallelemap:
                probeA = 'A'
                probeB = 'B'
            elif dctAlleleMap.has_key(snp_id):
                probeA = dctAlleleMap[snp_id][0]
                probeB = dctAlleleMap[snp_id][1]
            else:
                print 'Allele map is missing important data for ' + snp_id
                print 'Please fix this and restart the pipeline'
                sys.exit(1)
            if not dctOptions.norscoding:
                if dctMapFile.has_key(snp_id):
                    snp_id = dctMapFile[snp_id]
                else:
                    print 'SNP to RS Map is missing data for ' + snp_id
                    print 'Please fix this and restart the pipeline'
                    sys.exit(1)
            for index in range(1, len(calls_fields)):
                total_indiv += 1
                if dctFamMap.has_key(CelList[index]):
                    cel_id = CelList[index]
                    strCall = calls_fields[index]
                    conf = confs_fields[index]
                    if strCall is None:
                        iA = -1
                        iB = -1
                    else:
                        (iA, iB) = [ int(strVal) for strVal in strCall.split(',') ]
                    if iA == -1:
                        if iB != -1:
                            print 'Strange call (' + strCall + ') for SNP ' + snp_id
                            sys.exit(2)
                    if iA + iB != 2:
                        if float(conf) < float(dctOptions.threshold):
                            gathered_count += 1
                            if conf == 'NA' or float(conf) == -9:
                                fOut.write('%s\t%s\t%s\t0\t1\t0\t1\n' % (dctFamMap[cel_id][0], cel_id, snp_id))
                            else:
                                fOut.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (dctFamMap[cel_id][0], cel_id, snp_id, probeA, iA, probeB, iB))
                        else:
                            dropped_count += 1
                    else:
                        continue
                elif not dctFamMissing.has_key(CelList[index]):
                    dctFamMissing[CelList[index]] = True
                else:
                    continue

        indiv_count += len(CelList)

    if dropped_count > 0:
        print '\t(%s) of (%s)\tEvents Failed thresholding' % (dropped_count, gathered_count)
    if len(dctFamMissing.keys()) > 0:
        print '\t(%s) of (%s)\tIndividuals not in the Family Data' % (len(dctFamMissing.keys()), indiv_count)
        for indiv in dctFamMissing.keys():
            print '\t' + indiv

    fOut.close()
    return


def RemoveCels(list, dctOptions, dctCelMap):
    for index in range(len(list)):
        item = list[index]
        item = utils.stripCelExt(item)
        if dctOptions.celmap and not item == 'cnp_id':
            if dctCelMap.has_key(item):
                item = dctCelMap[item]
        list[index] = item

    return list


if __name__ == '__main__':
    main()
# global output_name ## Warning: Unused global
# global output_root ## Warning: Unused global