# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plink_pipeline/fam_to_gender.py
# Compiled at: 2009-01-27 09:41:58
import optparse, sys, os, getopt, re
from mpgutils import utils

def main(argv=None):
    lstRequiredOptions = [
     'plateroot', 'familyfile']
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-f', '--familyfile', help='(Required) PLINK formatted .fam file')
    parser.add_option('-p', '--plateroot', help='(Required) Contains folders with larry-bird style files')
    parser.add_option('-d', '--outputdir', help='Define the directory for output files')
    parser.add_option('-n', '--outputname', default='Output', help='Define the file name root for the output files')
    parser.add_option('-m', '--celmap', help='Cel Map file')
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
    dctFamMap = utils.readFamFile(dctOptions.familyfile)
    dctCelFileMap = utils.readCelMapFile(dctOptions.celmap)
    pattern = re.compile('[.]larry_bird_calls', re.IGNORECASE)
    CallsPaths = utils.findFiles(dctOptions.plateroot, pattern)
    MakeGenderFiles(CallsPaths, dctOptions, dctCelFileMap, dctFamMap)
    print 'Finished -- FamToGender.Py\n'


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
            if dctOptions.celmap:
                if dctCelFileMap.has_key(celid):
                    celid = dctCelFileMap[celid]
            if dctFamMap.has_key(celid):
                print >> fOut, dctFamMap[celid][4]
            else:
                print '\tCould not find ' + celid + ' in pedigree, setting gender to 0'
                print >> fOut, 0

        fOut.close()


if __name__ == '__main__':
    main()