# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/plink_pipeline/fam_to_gender.py
# Compiled at: 2010-09-02 17:25:18
import optparse, sys, os, re, shutil
from mpgutils import utils

def main(argv=None):
    lstRequiredOptions = [
     'plateroot', 'familyfile']
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-f', '--familyfile', help='(Required) PLINK formatted .fam file')
    parser.add_option('-p', '--plateroot', help='(Required) Contains folders with larry-bird style files')
    parser.add_option('-d', '--outputdir', help='Define the directory for output files')
    parser.add_option('-n', '--outputname', default='Output', help='Define the file name root for the output files')
    parser.add_option('-m', '--celmap', dest='celmap', default=None, help='Cel Map file')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    if not dctOptions.outputdir:
        setattr(dctOptions, 'outputdir', sys.path[0])
    lstOptionsToCheck = [
     'familyfile', 'plateroot', 'outputdir']
    utils.validatePathArgs(dctOptions, lstOptionsToCheck, True)
    if dctOptions.celmap:
        dctCelFileMap = utils.readCelMapFile(dctOptions.celmap)
    else:
        dctCelFileMap = {}
    dctFamMap = utils.readFamFile(dctOptions.familyfile)
    pattern = re.compile('[.]larry_bird_calls', re.IGNORECASE)
    CallsPaths = utils.findFiles(dctOptions.plateroot, pattern)
    gender_output = os.path.join(dctOptions.plateroot, dctOptions.outputname + '.merged.gen')
    pattern = re.compile('[.]gender', re.IGNORECASE)
    GenderPaths = utils.findFiles(dctOptions.plateroot, pattern)
    pattern = re.compile('[.]larry_bird_confs', re.IGNORECASE)
    ConfsPaths = utils.findFiles(dctOptions.plateroot, pattern)
    if len(GenderPaths) == 0:
        print '\tNo Gender files were found; Creating from pedigree information.'
        MakeGenderFiles(CallsPaths, dctOptions, dctCelFileMap, dctFamMap)
        pattern = re.compile('[.]gender', re.IGNORECASE)
        GenderPaths = utils.findFiles(dctOptions.plateroot, pattern)
    if len(GenderPaths) != len(ConfsPaths):
        print '\tThe number of larry_bird_confs Files and gender files are not equal. Please check your path.'
        print '\tThere must be exactly one .gender file for each .larry_bird_confs file'
        print '\n\tPlease ensure your files follow these conventions:'
        print '\t\t.fam       1=male; 2=female; other=unknown'
        print '\t\t.gender    0=female; 1=male; 2=unknown'
        print '\n\tFound the following .gender files:'
        for path in GenderPaths:
            print '\t\t' + path

        if len(ConfsPaths) > 0:
            print '\tFound the following .larry_bird_confs files:'
            for path in ConfsPaths:
                print '\t\t' + path

        else:
            print '\tFound NO .larry_bird_confs files.'
        sys.exit(1)
    elif len(GenderPaths) == 1:
        print '\tCopying gender file to ' + gender_output
        shutil.copy(GenderPaths[0], gender_output)
    else:
        print '\tMerging gender files to ' + gender_output
        successFlag = MergeGenderFiles(GenderPaths, gender_output)
        if not successFlag:
            print '\tGender Merge Failed, please check your Pedigree file and celmap'
            sys.exit(2)
    print 'Finished -- FamToGender.Py\n'
    return


def MakeGenderFiles(CallsPaths, dctOptions, dctCelFileMap, dctFamMap):
    for file_path in CallsPaths:
        file = open(file_path)
        header_line = file.readline()
        celList = header_line.split()
        (outpath, outputname) = os.path.split(file_path)
        lstname = outputname.split('.')
        outputprefix = lstname[0]
        out_file = os.path.join(outpath, outputprefix + '.gender')
        fOut = open(out_file, 'w')
        print >> fOut, 'gender'
        for item in celList:
            celid = utils.stripCelExt(item)
            if celid == 'probeset_id':
                continue
            if getattr(dctOptions, 'celmap') is not None:
                if dctCelFileMap.has_key(celid):
                    celid = dctCelFileMap[celid]
            if dctFamMap.has_key(celid):
                fam_gender = dctFamMap[celid][4]
                if fam_gender == '1':
                    print >> fOut, 1
                elif fam_gender == '2':
                    print >> fOut, 0
                else:
                    print >> fOut, 2
            else:
                print '\tCould not find ' + celid + " -- Setting gender to 'Unknown'(2)"
                print >> fOut, 2

        fOut.close()

    return


def MergeGenderFiles(lstFiles, outFile):
    fOut = open(outFile, 'w')
    fOut.write('gender\n')
    for file in lstFiles:
        fIn = open(file, 'r')
        for line in fIn:
            if str(line).rstrip() == 'gender':
                continue
            fOut.write(line)

        fIn.close()

    fOut.close()
    return True


if __name__ == '__main__':
    main()