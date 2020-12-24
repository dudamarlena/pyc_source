# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/jprofile/jprofile/jprofile.py
# Compiled at: 2017-10-19 08:38:27
"""JPEG 2000 Automated Quality Assessment Tool

Automated quality control of JP2 images for KB digitisation projects
Wraps around jpylyzer
Johan van der Knijff

Requires Python v. 2.7.x + lxml library; Python 3 may work (but not tested)

Preconditions:

- Images that are to be analysed have a .jp2 extension (all others ignored!)
- Parent directory of master images is called 'master'
- Parent directory of access images is called 'access'
- Parent directory of target images is called 'targets-jp2'

Master, access and targets directories may be located in a subdirectory.
Other than that organisation of images may follow arbitrary directory structure
(jprofile does a recursive scan of whole directory tree of a batch)

Copyright 2013, 2017 Johan van der Knijff,
KB/National Library of the Netherlands
"""
import sys, os, imp, time, argparse, xml.etree.ElementTree as ET
from jpylyzer import jpylyzer
from lxml import isoschematron
from lxml import etree
from . import config
__version__ = '0.7.5'

def main_is_frozen():
    """Determine if this jprofile instance is 'frozen' executable"""
    return hasattr(sys, 'frozen') or hasattr(sys, 'importers') or imp.is_frozen('__main__')


def get_main_dir():
    """Return installation directory"""
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])


def errorExit(msg):
    """Write error to stderr and exit"""
    msgString = 'ERROR: ' + msg + '\n'
    sys.stderr.write(msgString)
    sys.exit()


def checkFileExists(fileIn):
    """Check if file exists and exit if not"""
    if not os.path.isfile(fileIn):
        msg = fileIn + ' does not exist!'
        errorExit(msg)


def checkDirExists(pathIn):
    """Check if directory exists and exit if not"""
    if not os.path.isdir(pathIn):
        msg = pathIn + ' does not exist!'
        errorExit(msg)


def openFileForAppend(wFile):
    """Opens file for writing in append + binary mode"""
    try:
        if sys.version.startswith('3'):
            f = open(wFile, 'a', encoding='utf-8')
        elif sys.version.startswith('2'):
            f = open(wFile, 'a')
        return f
    except Exception:
        msg = wFile + ' could not be written'
        errorExit(msg)


def removeFile(fileIn):
    """Remove a file"""
    try:
        if os.path.isfile(fileIn):
            os.remove(fileIn)
    except Exception:
        msg = 'Could not remove ' + fileIn
        errorExit(msg)


def constructFileName(fileIn, extOut, suffixOut):
    """Construct filename by replacing path by pathOut,
    adding suffix and extension
    """
    fileInTail = os.path.split(fileIn)[1]
    baseNameIn = os.path.splitext(fileInTail)[0]
    baseNameOut = baseNameIn + suffixOut + '.' + extOut
    fileOut = baseNameOut
    return fileOut


def parseCommandLine():
    """Parse command line"""
    parser = argparse.ArgumentParser(description='JP2 profiler for KB')
    parser.add_argument('batchDir', action='store', help='batch directory')
    parser.add_argument('prefixOut', action='store', help='prefix of output files')
    parser.add_argument('-p', '--profile', action='store', default='list', help='name of profile that defines schemas for master,                               access and target images. Type "l" or "list"                               to view all available profiles')
    parser.add_argument('--version', '-v', action='version', version=__version__)
    args = parser.parse_args()
    args.batchDir = os.path.normpath(args.batchDir)
    return args


def listProfiles(profilesDir):
    """List all available profiles"""
    profileNames = os.listdir(profilesDir)
    print '\nAvailable profiles:\n'
    for i in range(len(profileNames)):
        print profileNames[i]

    sys.exit()


def readProfile(profile, profilesDir, schemasDir):
    """Read a profile and return dictionary with all associated schemas"""
    profile = os.path.join(profilesDir, profile)
    checkFileExists(profile)
    try:
        tree = ET.parse(profile)
        prof = tree.getroot()
    except Exception:
        msg = 'error parsing ' + profile
        errorExit(msg)

    schemaMasterElement = prof.find('schemaMaster')
    schemaAccessElement = prof.find('schemaAccess')
    schemaTargetRGBElement = prof.find('schemaTargetRGB')
    schemaTargetGrayElement = prof.find('schemaTargetGray')
    schemaTargetAccessRGBElement = prof.find('schemaTargetAccessRGB')
    schemaTargetAccessGrayElement = prof.find('schemaTargetAccessGray')
    schemaMaster = os.path.join(schemasDir, schemaMasterElement.text)
    schemaAccess = os.path.join(schemasDir, schemaAccessElement.text)
    schemaTargetRGB = os.path.join(schemasDir, schemaTargetRGBElement.text)
    schemaTargetGray = os.path.join(schemasDir, schemaTargetGrayElement.text)
    schemaTargetAccessRGB = os.path.join(schemasDir, schemaTargetAccessRGBElement.text)
    schemaTargetAccessGray = os.path.join(schemasDir, schemaTargetAccessGrayElement.text)
    checkFileExists(schemaMaster)
    checkFileExists(schemaAccess)
    checkFileExists(schemaTargetRGB)
    checkFileExists(schemaTargetGray)
    checkFileExists(schemaTargetAccessRGB)
    checkFileExists(schemaTargetAccessGray)
    schemas = {'schemaMaster': schemaMaster, 'schemaAccess': schemaAccess, 
       'schemaTargetRGB': schemaTargetRGB, 
       'schemaTargetGray': schemaTargetGray, 
       'schemaTargetAccessRGB': schemaTargetAccessRGB, 
       'schemaTargetAccessGray': schemaTargetAccessGray}
    return schemas


def readAsLXMLElt(xmlFile):
    """Parse XML file with lxml and return result as element object
    (not the same as Elementtree object!)
    """
    f = open(xmlFile, 'r')
    resultAsLXMLElt = etree.parse(f)
    f.close()
    return resultAsLXMLElt


def getFilesFromTree(rootDir, extensionString):
    """Walk down whole directory tree (including all subdirectories) and
    return list of those files whose extension contains user defined string
    NOTE: directory names are disabled here!!
    implementation is case insensitive (all search items converted to
    upper case internally!
    """
    extensionString = extensionString.upper()
    filesList = []
    for dirname, dirnames, filenames in os.walk(rootDir):
        for subdirname in dirnames:
            thisDirectory = os.path.join(dirname, subdirname)

        for filename in filenames:
            thisFile = os.path.join(dirname, filename)
            thisExtension = os.path.splitext(thisFile)[1]
            thisExtension = thisExtension.upper()
            if extensionString in thisExtension:
                filesList.append(thisFile)

    return filesList


def getPathComponentsAsList(path):
    """Returns a list that contains all path components (dir names) in path
    Adapted from:
    http://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python
    """
    drive, path_and_file = os.path.splitdrive(path)
    pathComponent, fileComponent = os.path.split(path_and_file)
    folders = []
    while 1:
        pathComponent, folder = os.path.split(pathComponent)
        if folder != '':
            folders.append(folder)
        else:
            if pathComponent != '':
                folders.append(pathComponent)
            break

    folders.reverse()
    return (folders, fileComponent)


def extractSchematron(report):
    """Parse output of Schematron validation and extract interesting bits"""
    outString = ''
    for elem in report.iter():
        if elem.tag == '{http://purl.oclc.org/dsdl/svrl}failed-assert':
            config.status = 'fail'
            test = elem.get('test')
            outString += 'Test "' + test + '" failed ('
            for subelem in elem.iter():
                if subelem.tag == '{http://purl.oclc.org/dsdl/svrl}text':
                    description = subelem.text
                    outString += description + ')' + config.lineSep

    return outString


def extractJpylyzer(resultJpylyzer):
    """Parse output of Jpylyzer and extract interesting bits"""
    outString = ''
    validationOutcome = resultJpylyzer.find('isValidJP2').text
    if validationOutcome == 'False':
        for element in resultJpylyzer.iter():
            if element.tag == 'tests':
                testsElt = element

        outString += '*** Jpylyzer JP2 validation errors:' + config.lineSep
        tests = list(testsElt.iter())
        for j in tests:
            if j.text == 'False':
                outString += 'Test ' + j.tag + ' failed' + config.lineSep

    return outString


def processJP2(JP2):
    """Process one JP2"""
    config.status = 'pass'
    schemaMatch = True
    ptOutString = ''
    pathComponents, fName = getPathComponentsAsList(JP2)
    if 'master' in pathComponents:
        mySchema = config.schemaMasterLXMLElt
    elif 'access' in pathComponents:
        mySchema = config.schemaAccessLXMLElt
    elif 'targets-jp2_access' in pathComponents:
        if '_MTF_GRAY_' in fName:
            mySchema = config.schemaTargetAccessGrayLXMLElt
        else:
            mySchema = config.schemaTargetAccessRGBLXMLElt
    elif 'targets-jp2' in pathComponents:
        if '_MTF_GRAY_' in fName:
            mySchema = config.schemaTargetGrayLXMLElt
        else:
            mySchema = config.schemaTargetRGBLXMLElt
    else:
        schemaMatch = False
        config.status = 'fail'
        description = 'Name of parent directory does not match any schema'
        ptOutString += description + config.lineSep
    if schemaMatch:
        try:
            resultJpylyzer = jpylyzer.checkOneFile(JP2)
            resultAsXML = ET.tostring(resultJpylyzer, 'UTF-8', 'xml')
        except Exception:
            config.status = 'fail'
            description = 'Error running jpylyzer'
            ptOutString += description + config.lineSep

        try:
            schematron = isoschematron.Schematron(mySchema, store_report=True)
            resJpylyzerLXML = etree.fromstring(resultAsXML)
            schemaValidationResult = schematron.validate(resJpylyzerLXML)
            report = schematron.validation_report
        except Exception:
            config.status = 'fail'
            description = 'Schematron validation resulted in an error'
            ptOutString += description + config.lineSep

        try:
            schOutString = extractSchematron(report)
            ptOutString += schOutString
        except Exception:
            config.status = 'fail'
            description = 'Error processing Schematron output'
            ptOutString += description + config.lineSep

        try:
            jpOutString = extractJpylyzer(resultJpylyzer)
            ptOutString += jpOutString
        except Exception:
            config.status = 'fail'
            description = 'Error processing Jpylyzer output'
            ptOutString += description + config.lineSep
            raise

    if config.status == 'fail':
        config.fFailed.write(JP2 + config.lineSep)
        config.fFailed.write('*** Schema validation errors:' + config.lineSep)
        config.fFailed.write(ptOutString)
        config.fFailed.write('####' + config.lineSep)
    statusLine = JP2 + ',' + config.status + config.lineSep
    config.fStatus.write(statusLine)


def main():
    """Main function"""
    packageDir = os.path.dirname(os.path.abspath(__file__))
    if main_is_frozen():
        profilesDir = os.path.join(os.path.dirname(sys.executable), 'profiles')
        schemasDir = os.path.join(os.path.dirname(sys.executable), 'schemas')
    else:
        profilesDir = os.path.join(packageDir, 'profiles')
        schemasDir = os.path.join(packageDir, 'schemas')
    checkDirExists(profilesDir)
    args = parseCommandLine()
    batchDir = args.batchDir
    prefixOut = args.prefixOut
    profile = args.profile
    if profile in ('l', 'list'):
        listProfiles(profilesDir)
    schemas = readProfile(profile, profilesDir, schemasDir)
    schemaMaster = schemas['schemaMaster']
    schemaAccess = schemas['schemaAccess']
    schemaTargetRGB = schemas['schemaTargetRGB']
    schemaTargetGray = schemas['schemaTargetGray']
    schemaTargetAccessRGB = schemas['schemaTargetAccessRGB']
    schemaTargetAccessGray = schemas['schemaTargetAccessGray']
    config.schemaMasterLXMLElt = readAsLXMLElt(schemaMaster)
    config.schemaAccessLXMLElt = readAsLXMLElt(schemaAccess)
    config.schemaTargetRGBLXMLElt = readAsLXMLElt(schemaTargetRGB)
    config.schemaTargetGrayLXMLElt = readAsLXMLElt(schemaTargetGray)
    config.schemaTargetAccessRGBLXMLElt = readAsLXMLElt(schemaTargetAccessRGB)
    config.schemaTargetAccessGrayLXMLElt = readAsLXMLElt(schemaTargetAccessGray)
    config.lineSep = '\n'
    statusLog = os.path.normpath(prefixOut + '_status.csv')
    removeFile(statusLog)
    config.fStatus = openFileForAppend(statusLog)
    failedLog = os.path.normpath(prefixOut + '_failed.txt')
    removeFile(failedLog)
    config.fFailed = openFileForAppend(failedLog)
    listJP2s = getFilesFromTree(batchDir, 'jp2')
    start = time.clock()
    print 'jprofile started: ' + time.asctime()
    for i in range(len(listJP2s)):
        myJP2 = os.path.abspath(listJP2s[i])
        processJP2(myJP2)

    end = time.clock()
    config.fStatus.close()
    config.fFailed.close()
    print 'jprofile ended: ' + time.asctime()
    timeElapsed = end - start
    timeInMinutes = round(timeElapsed / 60, 2)
    print 'Elapsed time: ' + str(timeInMinutes) + ' minutes'


if __name__ == '__main__':
    main()