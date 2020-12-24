# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/omSipCreator/omSipCreator/omSipCreator.py
# Compiled at: 2017-11-01 08:18:27
"""
SIP Creator for Offline Media Images.
"""
import sys, os, shutil, glob, imp, argparse, codecs, csv, hashlib, logging
from operator import itemgetter
from itertools import groupby
from lxml import etree
from . import config
from .mods import createMODS
from .premis import addCreationEvent
from .premis import addObjectInstance
try:
    input = raw_input
except NameError:
    pass

config.scriptPath, config.scriptName = os.path.split(sys.argv[0])
if len(config.scriptName) == 0:
    config.scriptName = 'omSipCreator'
__version__ = '0.4.10'
parser = argparse.ArgumentParser(description='SIP Creator for Offline Media Images')

class Carrier():
    """Carrier class"""

    def __init__(self, jobID, PPN, imagePathFull, volumeNumber, carrierType):
        """Initialise Carrier class instance"""
        self.jobID = jobID
        self.PPN = PPN
        self.imagePathFull = imagePathFull
        self.volumeNumber = volumeNumber
        self.carrierType = carrierType


class PPNGroup():
    """PPNGroup class"""

    def __init__(self):
        """initialise PPNGroup class instance"""
        self.carriers = []
        self.PPN = ''
        self.carrierType = ''

    def append(self, carrier):
        """Append a carrier. Result of this is that below PPN-level properties
        are inherited from last appended carrier (values should be identical
        for all carriers within PPN, but important to do proper QA on this as
        results may be unexpected otherwise)
        """
        self.carriers.append(carrier)
        self.PPN = carrier.PPN
        self.carrierType = carrier.carrierType


def main_is_frozen():
    """Returns True if maijn function is frozen
    (e.g. PyInstaller/Py2Exe executable)
    """
    return hasattr(sys, 'frozen') or hasattr(sys, 'importers') or imp.is_frozen('__main__')


def get_main_dir():
    """Reurns installation directory"""
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])


def errorExit(errors, warnings):
    """Print errors and exit"""
    logging.info('Batch verification yielded ' + str(errors) + ' errors and ' + str(warnings) + ' warnings')
    sys.exit()


def checkFileExists(fileIn):
    """Check if file exists and exit if not"""
    if not os.path.isfile(fileIn):
        msg = 'file ' + fileIn + ' does not exist!'
        sys.stderr.write('Error: ' + msg + '\n')
        sys.exit()


def get_immediate_subdirectories(a_dir, ignoreDirs):
    """Returns list of immediate subdirectories
    Directories that end with suffixes defined by ignoreDirs are ignored
    """
    subDirs = []
    for root, dirs, files in os.walk(a_dir):
        for myDir in dirs:
            ignore = False
            for ignoreDir in ignoreDirs:
                if myDir.endswith(ignoreDir):
                    ignore = True

            if not ignore:
                subDirs.append(os.path.abspath(os.path.join(root, myDir)))

    return subDirs


def readChecksums(fileIn):
    """Read checksum file, return contents as nested list
    Also strip away any file paths if they exist (return names only)
    """
    try:
        data = []
        f = open(fileIn, 'r', encoding='utf-8')
        for row in f:
            rowSplit = row.split(' ', 1)
            fileName = rowSplit[1].strip()
            rowSplit[1] = os.path.basename(fileName)
            data.append(rowSplit)

        f.close()
        return data
    except IOError:
        logging.fatal("cannot read '" + fileIn + "'")
        config.errors += 1
        errorExit(config.errors, config.warnings)


def generate_file_sha512(fileIn):
    """Generate sha512 hash of file
    fileIn is read in chunks to ensure it will work with (very) large files as well
    Adapted from: http://stackoverflow.com/a/1131255/1209004
    """
    blocksize = 1048576
    m = hashlib.sha512()
    with open(fileIn, 'rb') as (f):
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)

    return m.hexdigest()


def parseCommandLine():
    """Parse command-line arguments"""
    subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
    parser_verify = subparsers.add_parser('verify', help='only verify input batch without writing SIPs')
    parser_verify.add_argument('batchIn', action='store', type=str, help='input batch')
    parser_prune = subparsers.add_parser('prune', help="verify input batch, then write 'pruned' version                          of batch that omits all PPNs that have errors. Write PPNs with                          errors to a separate batch.")
    parser_prune.add_argument('batchIn', action='store', type=str, help='input batch')
    parser_prune.add_argument('batchErr', action='store', type=str, help='name of batch that will contain all PPNs with errors')
    parser_write = subparsers.add_parser('write', help="verify input batch and write SIPs. Before using                          'write' first run the 'verify' command and fix any reported errors.")
    parser_write.add_argument('batchIn', action='store', type=str, help='input batch')
    parser_write.add_argument('dirOut', action='store', type=str, help='output directory where SIPs are written')
    parser.add_argument('--version', '-v', action='version', version=__version__)
    args = parser.parse_args()
    return args


def printHelpAndExit():
    """Print usage message and exit"""
    print ''
    parser.print_help()
    sys.exit()


def processCarrier(carrier, fileGrp, SIPPath, sipFileCounterStart, counterTechMDStart):
    """Process contents of imagepath directory"""
    fileCounter = 1
    sipFileCounter = sipFileCounterStart
    counterTechMD = counterTechMDStart
    mimeTypeMap = {'application/x-iso9660-image': 'disk image', 
       'audio/flac': 'audio track', 
       'audio/wav': 'audio track'}
    skipChecksumVerification = False
    allFiles = glob.glob(carrier.imagePathFull + '/*')
    checksumFiles = [ i for i in allFiles if i.endswith('.sha512') ]
    noChecksumFiles = len(checksumFiles)
    if noChecksumFiles != 1:
        logging.error('jobID ' + carrier.jobID + ': found ' + str(noChecksumFiles) + " checksum files in directory '" + carrier.imagePathFull + "', expected 1")
        config.errors += 1
        skipChecksumVerification = True
    isobusterLogs = [ i for i in allFiles if i.endswith('isobuster.log') ]
    noIsobusterLogs = len(isobusterLogs)
    dBpowerampLogs = [ i for i in allFiles if i.endswith('dbpoweramp.log') ]
    noDbpowerampLogs = len(dBpowerampLogs)
    otherFiles = [ i for i in allFiles if not i.endswith(('.sha512', '.log')) ]
    noOtherFiles = len(otherFiles)
    if noOtherFiles == 0:
        logging.error('jobID ' + carrier.jobID + ": found no files in directory '" + carrier.imagePathFull)
        config.errors += 1
        config.failedPPNs.append(carrier.PPN)
    isOFiles = [ i for i in otherFiles if i.endswith(('.iso', '.ISO')) ]
    noIsoFiles = len(isOFiles)
    audioFiles = [ i for i in otherFiles if i.endswith(('.wav', '.WAV', 'flac', 'FLAC'))
                 ]
    noAudioFiles = len(audioFiles)
    if noIsoFiles > 0 and noIsobusterLogs != 1:
        logging.error('jobID ' + carrier.jobID + " : expected 1 file 'isobuster.log' in directory '" + carrier.imagePathFull + ' , found ' + str(noIsobusterLogs))
        config.errors += 1
        config.failedPPNs.append(carrier.PPN)
    if noAudioFiles > 0 and noDbpowerampLogs != 1:
        logging.error('jobID ' + carrier.jobID + " : expected 1 file 'dbpoweramp.log' in directory '" + carrier.imagePathFull + ' , found ' + str(noDbpowerampLogs))
        config.errors += 1
        config.failedPPNs.append(carrier.PPN)
    if not skipChecksumVerification:
        checksumsFromFile = readChecksums(checksumFiles[0])
        checksumsFromFile.sort(key=itemgetter(1))
        allFilesinChecksumFile = []
        for entry in checksumsFromFile:
            checksum = entry[0]
            fileName = entry[1]
            fileNameWithPath = os.path.normpath(carrier.imagePathFull + '/' + fileName)
            checksumCalculated = generate_file_sha512(fileNameWithPath)
            if checksumCalculated != checksum:
                logging.error('jobID ' + carrier.jobID + ": checksum mismatch for file '" + fileNameWithPath + "'")
                config.errors += 1
                config.failedPPNs.append(carrier.PPN)
            entry.append(str(os.path.getsize(fileNameWithPath)))
            allFilesinChecksumFile.append(fileNameWithPath)

        for f in otherFiles:
            if f not in allFilesinChecksumFile:
                logging.error('jobID ' + carrier.jobID + ": file '" + f + "' not referenced in '" + checksumFiles[0] + "'")
                config.errors += 1
                config.failedPPNs.append(carrier.PPN)

        divDiscName = etree.QName(config.mets_ns, 'div')
        divDisc = etree.Element(divDiscName, nsmap=config.NSMAP)
        divDisc.attrib['TYPE'] = carrier.carrierType
        divDisc.attrib['ORDER'] = carrier.volumeNumber
        if config.createSIPs:
            logging.info('creating carrier directory')
            dirVolume = os.path.join(SIPPath, carrier.carrierType, carrier.volumeNumber)
            try:
                os.makedirs(dirVolume)
            except OSError or IOError:
                logging.fatal('jobID ' + carrier.jobID + ": cannot create '" + dirVolume + "'")
                config.errors += 1
                errorExit(config.errors, config.warnings)

            logging.info('copying files to carrier directory')
            filesToCopy = [ i for i in checksumsFromFile if not i[1].endswith('.log') ]
            listTechMD = []
            for entry in filesToCopy:
                checksum = entry[0]
                fileName = entry[1]
                fileSize = entry[2]
                fileID = 'file_' + str(sipFileCounter)
                fIn = os.path.join(carrier.imagePathFull, fileName)
                fSIP = os.path.join(dirVolume, fileName)
                try:
                    shutil.copy2(fIn, fSIP)
                except OSError:
                    logging.fatal('jobID ' + carrier.jobID + ": cannot copy '" + fileName + "' to '" + fSIP + "'")
                    config.errors += 1
                    errorExit(config.errors, config.warnings)

                checksumCalculated = generate_file_sha512(fSIP)
                if checksumCalculated != checksum:
                    logging.error('jobID ' + carrier.jobID + ": checksum mismatch for file '" + fSIP + "'")
                    config.errors += 1
                    config.failedPPNs.append(carrier.PPN)
                fileElt = etree.SubElement(fileGrp, '{%s}file' % config.mets_ns)
                fileElt.attrib['ID'] = fileID
                fileElt.attrib['SIZE'] = fileSize
                fLocat = etree.SubElement(fileElt, '{%s}FLocat' % config.mets_ns)
                fLocat.attrib['LOCTYPE'] = 'URL'
                fLocat.attrib[etree.QName(config.xlink_ns, 'href')] = 'file:///' + carrier.carrierType + '/' + carrier.volumeNumber + '/' + fileName
                if fileName.endswith('.iso'):
                    mimeType = 'application/x-iso9660-image'
                elif fileName.endswith('.wav'):
                    mimeType = 'audio/wav'
                elif fileName.endswith('.flac'):
                    mimeType = 'audio/flac'
                else:
                    mimeType = 'application/octet-stream'
                fileElt.attrib['MIMETYPE'] = mimeType
                fileElt.attrib['CHECKSUM'] = checksum
                fileElt.attrib['CHECKSUMTYPE'] = 'SHA-512'
                divFile = etree.SubElement(divDisc, '{%s}div' % config.mets_ns)
                divFile.attrib['TYPE'] = mimeTypeMap[mimeType]
                divFile.attrib['ORDER'] = str(fileCounter)
                fptr = etree.SubElement(divFile, '{%s}fptr' % config.mets_ns)
                fptr.attrib['FILEID'] = fileID
                techMDPremisName = etree.QName(config.mets_ns, 'techMD')
                techMDPremis = etree.Element(techMDPremisName, nsmap=config.NSMAP)
                techMDPremisID = 'techMD_' + str(counterTechMD)
                techMDPremis.attrib['ID'] = techMDPremisID
                mdWrapObjectPremis = etree.SubElement(techMDPremis, '{%s}mdWrap' % config.mets_ns)
                mdWrapObjectPremis.attrib['MIMETYPE'] = 'text/xml'
                mdWrapObjectPremis.attrib['MDTYPE'] = 'PREMIS:OBJECT'
                mdWrapObjectPremis.attrib['MDTYPEVERSION'] = '3.0'
                xmlDataObjectPremis = etree.SubElement(mdWrapObjectPremis, '{%s}xmlData' % config.mets_ns)
                premisObjectInfo = addObjectInstance(fSIP, fileSize, mimeType, checksum)
                xmlDataObjectPremis.append(premisObjectInfo)
                listTechMD.append(techMDPremis)
                techMDIDs = techMDPremisID
                fileElt.attrib['ADMID'] = techMDIDs
                fileCounter += 1
                sipFileCounter += 1
                counterTechMD += 1

            premisCreationEvents = []
            if isobusterLogs != []:
                premisEvent = addCreationEvent(isobusterLogs[0])
                premisCreationEvents.append(premisEvent)
            if dBpowerampLogs != []:
                premisEvent = addCreationEvent(dBpowerampLogs[0])
                premisCreationEvents.append(premisEvent)
        else:
            premisCreationEvents = []
            listTechMD = []
    else:
        divDisc = etree.Element('rubbish')
        premisCreationEvents = []
        listTechMD = []
    return (fileGrp, divDisc, premisCreationEvents, listTechMD, sipFileCounter, counterTechMD)


def processPPN(PPN, carriers, dirOut, colsBatchManifest, batchIn, dirsInMetaCarriers, carrierTypeAllowedValues):
    """Process a PPN"""
    thisPPNGroup = PPNGroup()
    metsName = etree.QName(config.mets_ns, 'mets')
    mets = etree.Element(metsName, nsmap=config.NSMAP)
    mets.attrib[etree.QName(config.xsi_ns, 'schemaLocation')] = ('').join([
     config.metsSchema, ' ', config.modsSchema, ' ', config.premisSchema])
    dmdSec = etree.SubElement(mets, '{%s}dmdSec' % config.mets_ns)
    dmdSecID = 'dmdSec_1'
    dmdSec.attrib['ID'] = dmdSecID
    mdWrapDmd = etree.SubElement(dmdSec, '{%s}mdWrap' % config.mets_ns)
    mdWrapDmd.attrib['MDTYPE'] = 'MODS'
    mdWrapDmd.attrib['MDTYPEVERSION'] = '3.4'
    xmlDataDmd = etree.SubElement(mdWrapDmd, '{%s}xmlData' % config.mets_ns)
    amdSec = etree.SubElement(mets, '{%s}amdSec' % config.mets_ns)
    amdSecID = 'amdSec_1'
    amdSec.attrib['ID'] = amdSecID
    fileSec = etree.SubElement(mets, '{%s}fileSec' % config.mets_ns)
    fileGrp = etree.SubElement(fileSec, '{%s}fileGrp' % config.mets_ns)
    structMap = etree.SubElement(mets, '{%s}structMap' % config.mets_ns)
    structDivTop = etree.SubElement(structMap, '{%s}div' % config.mets_ns)
    structDivTop.attrib['TYPE'] = 'physical'
    structDivTop.attrib['LABEL'] = 'volumes'
    structDivTop.attrib['DMDID'] = dmdSecID
    fileCounterStart = 1
    carrierCounterStart = 1
    carrierCounter = carrierCounterStart
    counterDigiprovMD = 1
    counterTechMD = 1
    dirSIP = 'rubbish'
    if config.createSIPs:
        logging.info('creating SIP directory')
        dirSIP = os.path.join(dirOut, PPN)
        try:
            os.makedirs(dirSIP)
        except OSError:
            logging.fatal("cannot create '" + dirSIP + "'")
            config.errors += 1
            errorExit(config.errors, config.warnings)

    jobIDs = []
    volumeNumbers = []
    carrierTypes = []
    digiProvElementsPPN = []
    carriers = list(carriers)
    carriers.sort(key=itemgetter(3))
    carriersByType = groupby(carriers, itemgetter(3))
    for carrierTypeCarriers, carrierTypeGroup in carriersByType:
        volumeNumbersTypeGroup = []
        for carrier in carrierTypeGroup:
            jobID = carrier[colsBatchManifest['jobID']]
            volumeNumber = carrier[colsBatchManifest['volumeNo']]
            carrierType = carrier[colsBatchManifest['carrierType']]
            title = carrier[colsBatchManifest['title']]
            volumeID = carrier[colsBatchManifest['volumeID']]
            success = carrier[colsBatchManifest['success']]
            containsAudio = carrier[colsBatchManifest['containsAudio']]
            containsData = carrier[colsBatchManifest['containsData']]
            jobIDs.append(jobID)
            imagePathFull = os.path.normpath(os.path.join(batchIn, jobID))
            imagePathAbs = os.path.abspath(imagePathFull)
            dirsInMetaCarriers.append(imagePathAbs)
            if not os.path.isdir(imagePathFull):
                logging.error('jobID ' + jobID + ": '" + imagePathFull + "' is not a directory")
                config.errors += 1
                config.failedPPNs.append(PPN)
            thisCarrier = Carrier(jobID, PPN, imagePathFull, volumeNumber, carrierType)
            fileGrp, divDisc, premisEventsCarrier, listTechMD, fileCounter, counterTechMD = processCarrier(thisCarrier, fileGrp, dirSIP, fileCounterStart, counterTechMD)
            carrierID = 'disc_' + str(carrierCounter).zfill(3)
            digiProvID = 'digiprovMD_' + str(counterDigiprovMD)
            divDisc.attrib['ADMID'] = digiProvID
            for techMD in listTechMD:
                amdSec.append(techMD)

            digiprovMDName = etree.QName(config.mets_ns, 'digiprovMD')
            digiprovMD = etree.Element(digiprovMDName, nsmap=config.NSMAP)
            digiprovMD.attrib['ID'] = digiProvID
            mdWrapdigiprov = etree.SubElement(digiprovMD, '{%s}mdWrap' % config.mets_ns)
            mdWrapdigiprov.attrib['MIMETYPE'] = 'text/xml'
            mdWrapdigiprov.attrib['MDTYPE'] = 'PREMIS:EVENT'
            mdWrapdigiprov.attrib['MDTYPEVERSION'] = '3.0'
            xmlDatadigiprov = etree.SubElement(mdWrapdigiprov, '{%s}xmlData' % config.mets_ns)
            for premisEvent in premisEventsCarrier:
                xmlDatadigiprov.append(premisEvent)

            digiProvElementsPPN.append(digiprovMD)
            thisPPNGroup.append(thisCarrier)
            fileCounterStart = fileCounter
            counterTechMDStart = counterTechMD
            try:
                volumeNumbersTypeGroup.append(int(volumeNumber))
            except ValueError:
                logging.error('jobID ' + jobID + ": '" + volumeNumber + "' is illegal value for 'volumeNumber' (must be integer)")
                config.errors += 1
                config.failedPPNs.append(PPN)

            if carrierType not in carrierTypeAllowedValues:
                logging.error('jobID ' + jobID + ": '" + carrierType + "' is illegal value for 'carrierType'")
                config.errors += 1
                config.failedPPNs.append(PPN)
            carrierTypes.append(carrierType)
            if success != 'True':
                logging.error('jobID ' + jobID + ": value of 'success' not 'True'")
                config.errors += 1
                config.failedPPNs.append(PPN)
            if carrierType in ('cd-rom', 'dvd-rom', 'dvd-video') and containsData != 'True':
                logging.error('jobID ' + jobID + ": carrierType cannot be '" + carrierType + "'if 'containsData' is 'False'")
                config.errors += 1
                config.failedPPNs.append(PPN)
            elif carrierType == 'cd-audio' and containsAudio != 'True':
                logging.error('jobID ' + jobID + ": carrierType cannot be '" + carrierType + "'if 'containsAudio' is 'False'")
                config.errors += 1
                config.failedPPNs.append(PPN)
            structDivTop.append(divDisc)
            carrierCounter += 1
            counterDigiprovMD += 1

        volumeNumbers.append(volumeNumbersTypeGroup)

    mdMODS = createMODS(thisPPNGroup)
    xmlDataDmd.append(mdMODS)
    for digiProvMDElt in digiProvElementsPPN:
        amdSec.append(digiProvMDElt)

    if config.createSIPs:
        logging.info('writing METS file')
        if sys.version.startswith('3'):
            metsAsString = etree.tostring(mets, pretty_print=True, encoding='unicode')
        elif sys.version.startswith('2'):
            metsAsString = etree.tostring(mets, pretty_print=True, encoding='utf-8')
        metsFname = os.path.join(dirSIP, 'mets.xml')
        with open(metsFname, 'w', encoding='utf-8') as (text_file):
            text_file.write(metsAsString)
    uniquejobIDs = set(jobIDs)
    if len(uniquejobIDs) != len(jobIDs):
        logging.error('PPN ' + PPN + ": duplicate values found for 'jobID'")
        config.errors += 1
        config.failedPPNs.append(PPN)
    for volumeNumbersTypeGroup in volumeNumbers:
        uniqueVolumeNumbers = set(volumeNumbersTypeGroup)
        if len(uniqueVolumeNumbers) != len(volumeNumbersTypeGroup):
            logging.error('PPN ' + PPN + ' (' + carrierType + "): duplicate values found for 'volumeNumber'")
            config.errors += 1
            config.failedPPNs.append(PPN)
        volumeNumbersTypeGroup.sort()
        if volumeNumbersTypeGroup[0] != 1:
            logging.warning('PPN ' + PPN + ' (' + carrierType + "): expected '1' as lower value for 'volumeNumber', found '" + str(volumeNumbersTypeGroup[0]) + "'")
            config.warnings += 1
        if sorted(volumeNumbersTypeGroup) != list(range(min(volumeNumbersTypeGroup), max(volumeNumbersTypeGroup) + 1)):
            logging.warning('PPN ' + PPN + ' (' + carrierType + "): values for 'volumeNumber' are not consecutive")
            config.warnings += 1


def main():
    """Main CLI function"""
    logFile = 'omsipcreator.log'
    logFormatter = logging.Formatter('%(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    packageDir = os.path.dirname(os.path.abspath(__file__))
    toolsDirUser = os.path.join(packageDir, 'tools')
    fileBatchManifest = 'manifest.csv'
    fileBatchLog = 'batch.log'
    requiredColsBatchManifest = [
     'jobID',
     'PPN',
     'volumeNo',
     'carrierType',
     'title',
     'volumeID',
     'success',
     'containsAudio',
     'containsData']
    carrierTypeAllowedValues = [
     'cd-rom',
     'cd-audio',
     'dvd-rom',
     'dvd-video']
    config.mets_ns = 'http://www.loc.gov/METS/'
    config.mods_ns = 'http://www.loc.gov/mods/v3'
    config.premis_ns = 'http://www.loc.gov/premis/v3'
    config.ebucore_ns = 'urn:ebu:metadata-schema:ebuCore_2017'
    config.xlink_ns = 'http://www.w3.org/1999/xlink'
    config.xsi_ns = 'http://www.w3.org/2001/XMLSchema-instance'
    config.metsSchema = 'http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/mets.xsd'
    config.modsSchema = 'http://www.loc.gov/mods/v3 https://www.loc.gov/standards/mods/v3/mods-3-4.xsd'
    config.premisSchema = 'http://www.loc.gov/premis/v3 https://www.loc.gov/standards/premis/premis.xsd'
    config.ebucoreSchema = 'https://raw.githubusercontent.com/ebu/ebucore/master/ebucore.xsd'
    config.NSMAP = {'mets': config.mets_ns, 'mods': config.mods_ns, 
       'premis': config.premis_ns, 
       'ebucore': config.ebucore_ns, 
       'xlink': config.xlink_ns, 
       'xsi': config.xsi_ns}
    config.errors = 0
    config.warnings = 0
    config.failedPPNs = []
    if sys.version.startswith('2'):
        out = codecs.getwriter('UTF-8')(sys.stdout)
        err = codecs.getwriter('UTF-8')(sys.stderr)
    elif sys.version.startswith('3'):
        out = codecs.getwriter('UTF-8')(sys.stdout.buffer)
        err = codecs.getwriter('UTF-8')(sys.stderr.buffer)
    config.createSIPs = False
    config.pruneBatch = False
    args = parseCommandLine()
    action = args.subcommand
    if action is None:
        printHelpAndExit()
    batchIn = os.path.normpath(args.batchIn)
    if action == 'write':
        dirOut = os.path.normpath(args.dirOut)
        config.createSIPs = True
    elif action == 'prune':
        batchErr = os.path.normpath(args.batchErr)
        dirOut = None
        config.pruneBatch = True
    else:
        dirOut = None
    if sys.platform is 'win32':
        config.mediaInfoExe = os.path.join(toolsDirUser, 'mediainfo', 'MediaInfo.exe')
    else:
        if sys.platform in ('linux', 'linux2'):
            config.mediaInfoExe = '/usr/bin/mediainfo'
        checkFileExists(config.mediaInfoExe)
        if not os.path.isdir(batchIn):
            logging.fatal('input batch directory does not exist')
            config.errors += 1
            errorExit(config.errors, config.warnings)
        ignoreDirs = [
         'jobs', 'jobsFailed']
        dirsInBatch = get_immediate_subdirectories(batchIn, ignoreDirs)
        dirsInMetaCarriers = []
        batchManifest = os.path.join(batchIn, fileBatchManifest)
        if not os.path.isfile(batchManifest):
            logging.fatal('file ' + batchManifest + ' does not exist')
            config.errors += 1
            errorExit(config.errors, config.warnings)
        try:
            if sys.version.startswith('3'):
                fBatchManifest = open(batchManifest, 'r', encoding='utf-8')
            elif sys.version.startswith('2'):
                fBatchManifest = open(batchManifest, 'rb')
            batchManifestCSV = csv.reader(fBatchManifest)
            headerBatchManifest = next(batchManifestCSV)
            rowsBatchManifest = [ row for row in batchManifestCSV ]
            fBatchManifest.close()
        except IOError:
            logging.fatal('cannot read ' + batchManifest)
            config.errors += 1
            errorExit(config.errors, config.warnings)
        except csv.Error:
            logging.fatal('error parsing ' + batchManifest)
            config.errors += 1
            errorExit(config.errors, config.warnings)

        colsHeader = len(headerBatchManifest)
        rowCount = 1
        for row in rowsBatchManifest:
            rowCount += 1
            colsRow = len(row)
            if colsRow == 0:
                rowsBatchManifest.remove(row)
            elif colsRow != colsHeader:
                logging.fatal('wrong number of columns in row ' + str(rowCount) + " of '" + batchManifest + "'")
                config.errors += 1
                errorExit(config.errors, config.warnings)

        if config.createSIPs:
            if os.path.isdir(dirOut):
                out.write("This will overwrite existing directory '" + dirOut + "' and remove its contents!\nDo you really want to proceed (Y/N)? > ")
                response = input()
                if response.upper() == 'Y':
                    try:
                        shutil.rmtree(dirOut)
                    except OSError:
                        logging.fatal("cannot remove '" + dirOut + "'")
                        config.errors += 1
                        errorExit(config.errors, config.warnings)

            try:
                os.makedirs(dirOut)
            except OSError:
                logging.fatal("cannot create '" + dirOut + "'")
                config.errors += 1
                errorExit(config.errors, config.warnings)

        for requiredCol in requiredColsBatchManifest:
            occurs = headerBatchManifest.count(requiredCol)
            if occurs != 1:
                logging.fatal('found ' + str(occurs) + " occurrences of column '" + requiredCol + "' in " + batchManifest + ' (expected 1)')
                config.errors += 1
                errorExit(config.errors, config.warnings)

        colsBatchManifest = {}
        col = 0
        for header in headerBatchManifest:
            colsBatchManifest[header] = col
            col += 1

        rowsBatchManifest.sort(key=itemgetter(1))
        metaCarriersByPPN = groupby(rowsBatchManifest, itemgetter(1))
        for PPN, carriers in metaCarriersByPPN:
            logging.info('Processing PPN ' + PPN)
            processPPN(PPN, carriers, dirOut, colsBatchManifest, batchIn, dirsInMetaCarriers, carrierTypeAllowedValues)

        diffDirs = list(set(dirsInBatch) - set(dirsInMetaCarriers))
        for directory in diffDirs:
            logging.error('PPN ' + PPN + ": directory '" + directory + "' not referenced in '" + batchManifest + "'")
            config.errors += 1
            config.failedPPNs.append(PPN)

    logging.info('Verify / write resulted in ' + str(config.errors) + ' errors and ' + str(config.warnings) + ' warnings')
    config.errors = 0
    config.warnings = 0
    config.failedPPNs = list(set(config.failedPPNs))
    if config.pruneBatch and config.failedPPNs != []:
        logging.info('Start pruning')
        if os.path.isdir(batchErr):
            out.write("\nThis will overwrite existing directory '" + batchErr + "' and remove its contents!\nDo you really want to proceed (Y/N)? > ")
            response = input()
            if response.upper() == 'Y':
                try:
                    shutil.rmtree(batchErr)
                except OSError:
                    logging.fatal("cannot remove '" + batchErr + "'")
                    config.errors += 1
                    errorExit(config.errors, config.warnings)

            else:
                logging.error("exiting because user pressed 'N'")
                errorExit(config.errors, config.warnings)
        try:
            os.makedirs(batchErr)
        except OSError or IOError:
            logging.fatal("Cannot create directory '" + batchErr + "'")
            config.errors += 1
            errorExit(config.errors, config.warnings)

        batchManifestErr = os.path.join(batchErr, fileBatchManifest)
        fileBatchManifestTemp = 'tmp.csv'
        batchManifestTemp = os.path.join(batchIn, fileBatchManifestTemp)
        try:
            if sys.version.startswith('3'):
                fbatchManifestErr = open(batchManifestErr, 'w', encoding='utf-8')
                fbatchManifestTemp = open(batchManifestTemp, 'w', encoding='utf-8')
            elif sys.version.startswith('2'):
                fbatchManifestErr = open(batchManifestErr, 'wb')
                fbatchManifestTemp = open(batchManifestTemp, 'wb')
        except IOError:
            logging.fatal('cannot write batch manifest')
            config.errors += 1
            errorExit(config.errors, config.warnings)

        csvErr = csv.writer(fbatchManifestErr, lineterminator='\n')
        csvTemp = csv.writer(fbatchManifestTemp, lineterminator='\n')
        csvErr.writerow(headerBatchManifest)
        csvTemp.writerow(headerBatchManifest)
        for row in rowsBatchManifest:
            jobID = row[0]
            PPN = row[1]
            if PPN in config.failedPPNs:
                skipChecksumVerification = False
                imagePathIn = os.path.normpath(os.path.join(batchIn, jobID))
                imagePathErr = os.path.normpath(os.path.join(batchErr, jobID))
                imagePathInAbs = os.path.abspath(imagePathIn)
                imagePathErrAbs = os.path.abspath(imagePathErr)
                if os.path.isdir(imagePathInAbs):
                    try:
                        os.makedirs(imagePathErrAbs)
                    except OSError or IOError:
                        logging.error('jobID ' + jobID + ": could not create directory '" + imagePathErrAbs)
                        config.errors += 1

                    allFiles = glob.glob(imagePathInAbs + '/*')
                    logging.info('Copying files to error batch')
                    for fileIn in allFiles:
                        fileBaseName = os.path.basename(fileIn)
                        fileErr = os.path.join(imagePathErrAbs, fileBaseName)
                        try:
                            shutil.copy2(fileIn, fileErr)
                        except IOError or OSError:
                            logging.error('jobID ' + jobID + ": cannot copy '" + fileIn + "' to '" + fileErr + "'")
                            config.errors += 1

                        checksumIn = generate_file_sha512(fileIn)
                        checksumErr = generate_file_sha512(fileErr)
                        if checksumIn != checksumErr:
                            logging.error('jobID ' + jobID + ": checksum of '" + fileIn + "' does not match '" + fileErr + "'")
                            config.errors += 1

                logging.info('Writing batch manifest entry (batchErr)')
                csvErr.writerow(row)
                if os.path.isdir(imagePathInAbs):
                    logging.info("Removing  directory '" + imagePathInAbs + "' from batchIn")
                    try:
                        shutil.rmtree(imagePathInAbs)
                    except OSError:
                        logging.error("cannot remove '" + imagePathInAbs + "'")
                        config.errors += 1

            else:
                logging.info('Writing batch manifest entry (batchIn)')
                csvTemp.writerow(row)

        fbatchManifestErr.close()
        fbatchManifestTemp.close()
        fileBatchManifestOld = os.path.splitext(fileBatchManifest)[0] + '.old'
        batchManifestOld = os.path.join(batchIn, fileBatchManifestOld)
        os.rename(batchManifest, batchManifestOld)
        os.rename(batchManifestTemp, batchManifest)
        logging.info("Saved old batch manifest in batchIn as '" + fileBatchManifestOld + "'")
        batchLogIn = os.path.join(batchIn, fileBatchLog)
        batchLogErr = os.path.join(batchErr, fileBatchLog)
        shutil.copy2(batchLogIn, batchLogErr)
        logging.info('Pruning resulted in additional ' + str(config.errors) + ' errors and ' + str(config.warnings) + ' warnings')
    return


if __name__ == '__main__':
    main()