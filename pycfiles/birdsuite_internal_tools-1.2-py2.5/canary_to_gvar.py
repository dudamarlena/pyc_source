# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plink_pipeline/canary_to_gvar.py
# Compiled at: 2009-06-09 16:56:00
import optparse
from mpgutils import utils
import sys, os, getopt, re, shutil
dctFamMap = {}
dctCelFileMap = {}
dctIndivMap = {}
dctCallFile = {}

def main(argv=None):
    if argv is None:
        argv = sys.argv
    lstRequiredOptions = ['familyfile', 'plateroot']
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-f', '--familyfile', help='(Required) Define the directory for output files')
    parser.add_option('-p', '--plateroot', help='(Required) Define the directory where the data plate info resides')
    parser.add_option('-o', '--outputdir', help='Define the directory for output files')
    parser.add_option('-n', '--outputname', default='Output', help='define the file name root for the output files')
    parser.add_option('-t', '--threshold', default=0.1, help='define a cutoff for confidence data')
    parser.add_option('-m', '--celmap', dest='celmap', help='Cel Map file')
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
    plate_root = utils.validatePath(dctOptions.plateroot)
    pattern = re.compile('[.]canary_calls', re.IGNORECASE)
    CallsPaths = utils.findFiles(plate_root, pattern)
    pattern = re.compile('[.]canary_confs', re.IGNORECASE)
    ConfsPaths = utils.findFiles(plate_root, pattern)
    if not len(CallsPaths) == len(ConfsPaths):
        print 'You are missing one or more files in your plate paths, please check file integrity'
        sys.exit(1)
    fam_copy = os.path.join(dctOptions.outputdir, dctOptions.outputname + '.canary.fam')
    shutil.copy(dctOptions.familyfile, fam_copy)
    ReadFamFile(dctOptions.familyfile)
    if dctOptions.celmap:
        ReadCelMapFile(dctOptions.celmap)
    for calls_path in CallsPaths:
        ReadCallsFile(calls_path, dctOptions)

    fOut = open(os.path.join(dctOptions.outputdir, dctOptions.outputname + '.canary.gvar'), 'w')
    fOut.write('FID\tIID\tNAME\tAL1\tDOS1\tAL2\tDOS2\n')
    ReadConfsFiles(ConfsPaths, dctOptions, fOut)
    print 'Finished Canary_To_Gvar.Py\n'
    return


def MakeMap(list, dctOptions):
    global dctCelFileMap
    count = 0
    returnMap = {}
    for item in list:
        item = StripCelExt(item)
        if dctOptions.celmap and not item == 'cnp_id':
            if dctCelFileMap.has_key(item):
                item = dctCelFileMap[item]
        returnMap[item] = count
        count += 1

    return returnMap


def StripCelExt(item):
    p = re.compile('[.]cel', re.IGNORECASE)
    m = p.search(item)
    if m:
        item = item[:-4]
    return item


def ReadCelMapFile(cel_map_file):
    CelMapFile = open(cel_map_file)
    for strLine in CelMapFile:
        if strLine[0] == '#':
            continue
        Fields = strLine.split()
        CelID = Fields[0]
        CelID = StripCelExt(CelID)
        IID = Fields[1]
        dctCelFileMap[CelID] = IID


def ReadFamFile(family_file):
    global dctFamMap
    FamilyFile = open(family_file)
    for strLine in FamilyFile:
        Fam_Value = []
        if strLine[0] == '#':
            continue
        Fields = strLine.split()
        IID = Fields[1]
        FID = Fields[0]
        dctFamMap[IID] = FID


def ReadCallsFile(calls_path, dctOptions):
    global dctCallFile
    CallsFile = open(calls_path)
    header_complete = False
    for strLine in CallsFile:
        CallFileFields = strLine.split()
        if not header_complete:
            dctCallFile = MakeMap(CallFileFields, dctOptions)
            for key in dctCallFile.keys():
                if not dctIndivMap.has_key(key):
                    dctCNVType = {}
                    dctIndivMap[key] = dctCNVType

            header_complete = True
            continue
        CNVID = CallFileFields[0]
        for key in dctCallFile.keys():
            if dctCallFile[key] == 0:
                continue
            Field = CallFileFields[dctCallFile[key]]
            tmpMap = dctIndivMap[key]
            if Field == 'NA':
                tmpMap[CNVID] = int(-9)
            else:
                tmpMap[CNVID] = int(Field)


def ReadConfsFiles(ConfsPaths, dctOptions, gvarFile):
    dctFamMissing = {}
    dctCNVMissing = {}
    dropped_count = 0
    gathered_count = 0
    indiv_count = 0
    for confs_path in ConfsPaths:
        ConfsFile = open(confs_path)
        header_complete = False
        for strLine in ConfsFile:
            ConfFileFields = strLine.split()
            if header_complete == False:
                dctConfFile = MakeMap(ConfFileFields, dctOptions)
                header_complete = True
                continue
            CNVID = ConfFileFields[0]
            for key in dctConfFile.keys():
                if dctIndivMap.has_key(key):
                    if key == 'cnp_id':
                        continue
                    else:
                        tmpMap = dctIndivMap[key]
                        if tmpMap.has_key(CNVID) and dctFamMap.has_key(key):
                            field = ConfFileFields[dctConfFile[key]]
                            if field == 'NA':
                                gvarFile.write('%s\t%s\t%s\t0\t1\t0\t1\n' % (dctFamMap[key], key, CNVID))
                            elif float(field) > float(dctOptions.threshold) or float(field) == -9 or tmpMap[CNVID] == -9:
                                if float(field) > float(dctOptions.threshold):
                                    dropped_count += 1
                                gvarFile.write('%s\t%s\t%s\t0\t1\t0\t1\n' % (dctFamMap[key], key, CNVID))
                            else:
                                gvarFile.write('%s\t%s\t%s\tX\t0\tA\t%s\n' % (dctFamMap[key], key, CNVID, tmpMap[CNVID]))
                                gathered_count += 1
                        elif not tmpMap.has_key(CNVID):
                            if not dctCNVMissing.has_key(key):
                                dctCNVMissing[key] = True
                            continue
                        elif not dctFamMap.has_key(key):
                            if not dctFamMissing.has_key(key):
                                dctFamMissing[key] = True
                            continue
                else:
                    print key + ' is missing'
                    continue

        indiv_count += len(ConfFileFields)

    if not dctOptions.quiet and dropped_count > 0:
        print '\t(%s) of (%s)\tFailed thresholding' % (dropped_count, gathered_count)
    if not dctOptions.quiet and len(dctFamMissing.keys()) > 0:
        print '\t(%s) of (%s)\t\tIndividuals not in the Family Data' % (len(dctFamMissing.keys()), indiv_count)
        for indiv in dctFamMissing.keys():
            print '\t' + indiv


if __name__ == '__main__':
    main()