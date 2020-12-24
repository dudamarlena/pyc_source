# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/isolyzer/isolyzer/isolyzer.py
# Compiled at: 2018-01-26 09:08:37
"""Verify if size of CD / DVD ISO image is consistent with the information in
its filesystem-level headers.
"""
from __future__ import division
import sys, os, mmap, time, glob, re, codecs, argparse, xml.etree.ElementTree as ET
from xml.dom import minidom
from six import u
from . import iso9660 as iso
from . import udf
from . import apple
from . import byteconv as bc
from . import shared
scriptPath, scriptName = os.path.split(sys.argv[0])
if len(scriptName) == 0:
    scriptName = 'isolyzer'
__version__ = '1.3.0'
parser = argparse.ArgumentParser(description='Verify file size of ISO image and extract technical information')

def printWarning(msg):
    """Print warning to stderr"""
    msgString = 'User warning: ' + msg + '\n'
    sys.stderr.write(msgString)


def errorExit(msg):
    """Print warning to stderr and exit"""
    msgString = 'Error: ' + msg + '\n'
    sys.stderr.write(msgString)
    sys.exit()


def checkFileExists(fileIn):
    """Check if file exists and exit if not"""
    if not os.path.isfile(fileIn):
        msg = fileIn + ' does not exist'
        errorExit(msg)


def fileToMemoryMap(filename):
    """Read contents of filename to memory map object"""
    f = open(filename, 'rb')
    platform = sys.platform
    try:
        if platform == 'win32':
            fileData = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            fileData = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
    except ValueError:
        fileData = ''

    f.close()
    return fileData


def makeHumanReadable(element, remapTable={}):
    """Takes element object, and returns a modified version in which all
    non-printable 'text' fields (which may contain numeric data or binary strings)
    are replaced by printable strings

    Property values in original tree may be mapped to alternative (more user-friendly)
    reportable values using a remapTable, which is a nested dictionary.
    TODO: add to separate module
    """
    for elt in element.iter():
        textIn = elt.text
        tag = elt.tag
        try:
            parameterMap = remapTable[tag]
            try:
                remappedValue = parameterMap[textIn]
            except KeyError:
                remappedValue = textIn

        except KeyError:
            remappedValue = textIn

        if sys.version.startswith('2'):
            numericTypes = [int, long, float, bool]
        else:
            numericTypes = [
             int, float, bool]
        if remappedValue is not None:
            textType = type(remappedValue)
            if textType == bytes:
                textOut = bc.bytesToText(remappedValue)
            elif textType in numericTypes:
                textOut = str(remappedValue)
            else:
                textOut = bc.removeControlCharacters(remappedValue).strip()
            elt.text = textOut

    return


def writeElement(elt, codec):
    """Writes element as XML to stdout using defined codec"""
    if sys.version.startswith('2'):
        xmlOut = ET.tostring(elt, 'UTF-8', 'xml')
    if sys.version.startswith('3'):
        xmlOut = ET.tostring(elt, 'unicode', 'xml')
    xmlPretty = minidom.parseString(xmlOut).toprettyxml('    ')
    xmlOut = xmlPretty
    codec.write(xmlOut)


def stripSurrogatePairs(ustring):
    """Removes surrogate pairs from a Unicode string"""
    if sys.version.startswith('3'):
        try:
            ustring.encode('utf-8')
        except UnicodeEncodeError:
            tmp = ustring.encode('utf-8', 'replace')
            ustring = tmp.decode('utf-8', 'ignore')

    if sys.version.startswith('2'):
        lone = re.compile(u('(?x)            # verbose expression (allows comments)\n            (                    # begin group\n            [\\ud800-\\udbff]      #   match leading surrogate\n            (?![\\udc00-\\udfff])  #   but only if not followed by trailing surrogate\n            )                    # end group\n            |                    #  OR\n            (                    # begin group\n            (?<![\\ud800-\\udbff]) #   if not preceded by leading surrogate\n            [\\udc00-\\udfff]      #   match trailing surrogate\n            )                   # end group\n            '))
        tmp = lone.sub('', ustring).encode('utf-8')
        ustring = tmp.decode('utf-8')
    return ustring


def parseCommandLine():
    """Parse command line"""
    parser.add_argument('ISOImages', action='store', type=str, help='input ISO image(s) (wildcards allowed)')
    parser.add_argument('--version', '-v', action='version', version=__version__)
    parser.add_argument('--offset', '-o', type=int, help='offset (in sectors) of ISO image on CD (analogous to                         -N option in cdinfo)', action='store', dest='sectorOffset', default=0)
    args = parser.parse_args()
    return args


def processImage(image, offset):
    """Process one image"""
    checkFileExists(image)
    imageRoot = ET.Element('image')
    fileInfo = ET.Element('fileInfo')
    statusInfo = ET.Element('statusInfo')
    fileName = os.path.basename(image)
    filePath = os.path.abspath(image)
    fileNameCleaned = stripSurrogatePairs(fileName)
    filePathCleaned = stripSurrogatePairs(filePath)
    shared.addProperty(fileInfo, 'fileName', fileNameCleaned)
    shared.addProperty(fileInfo, 'filePath', filePathCleaned)
    shared.addProperty(fileInfo, 'fileSizeInBytes', str(os.path.getsize(image)))
    try:
        lastModifiedDate = time.ctime(os.path.getmtime(image))
    except ValueError:
        lastModifiedDate = time.ctime(0)

    shared.addProperty(fileInfo, 'fileLastModified', lastModifiedDate)
    tests = ET.Element('tests')
    fileSystems = ET.Element('fileSystems')
    success = True
    try:
        isoFileSize = os.path.getsize(image)
        containsAppleMasterDirectoryBlock = False
        containsHFSPlusVolumeHeader = False
        containsAppleFS = False
        isoBytes = fileToMemoryMap(image)
        containsISO9660Signature = isoBytes[32769:32774] == 'CD001' and isoBytes[34817:34822] == 'CD001'
        containsApplePartitionMap = isoBytes[0:2] == 'ER' and isoBytes[512:514] == 'PM'
        if isoBytes[1024:1026] == 'BD':
            containsAppleMasterDirectoryBlock = True
            fileSystemApple = 'HFS'
        if isoBytes[1024:1026] == b'\xd2\xd7':
            containsAppleMasterDirectoryBlock = True
            fileSystemApple = 'MFS'
        if isoBytes[1024:1026] == 'H+':
            containsHFSPlusVolumeHeader = True
            fileSystemApple = 'HFS+'
        if isoBytes[1024:1026] == 'HX':
            containsHFSPlusVolumeHeader = True
            fileSystemApple = 'HFS+'
        if containsApplePartitionMap or containsAppleMasterDirectoryBlock or containsHFSPlusVolumeHeader:
            containsAppleFS = True
            fsApple = ET.Element('fileSystem')
        if containsApplePartitionMap:
            appleZeroBlockData = isoBytes[0:512]
            try:
                appleZeroBlockInfo = apple.parseZeroBlock(appleZeroBlockData)
                fsApple.append(appleZeroBlockInfo)
                parsedAppleZeroBlock = True
            except Exception:
                parsedAppleZeroBlock = False

            partitionTypes = []
            applePartitionMapData = isoBytes[512:1024]
            try:
                applePartitionMapInfo = apple.parsePartitionMap(applePartitionMapData)
                partitionType = applePartitionMapInfo.find('partitionType').text
                partitionTypes.append(partitionType)
                fsApple.append(applePartitionMapInfo)
                parsedApplePartitionMap = True
            except Exception:
                parsedApplePartitionMap = False
                partitionType = ''

            if partitionType == 'Apple_HFS':
                offsetHFS = 512 * applePartitionMapInfo.find('partitionBlockStart').text
                masterDirectoryBlockData = isoBytes[offsetHFS + 1024:offsetHFS + 1536]
                try:
                    masterDirectoryBlockInfo = apple.parseMasterDirectoryBlock(masterDirectoryBlockData)
                    fsApple.append(masterDirectoryBlockInfo)
                    parsedMasterDirectoryBlock = True
                except Exception:
                    parsedMasterDirectoryBlock = False

            pOffset = 1024
            for pMap in range(0, applePartitionMapInfo.find('numberOfPartitionEntries').text - 1):
                applePartitionMapData = isoBytes[pOffset:pOffset + 512]
                try:
                    applePartitionMapInfo = apple.parsePartitionMap(applePartitionMapData)
                    partitionType = applePartitionMapInfo.find('partitionType').text
                    partitionTypes.append(partitionType)
                    fsApple.append(applePartitionMapInfo)
                    parsedApplePartitionMap = True
                except Exception:
                    parsedApplePartitionMap = False
                    partitionType = ''

                if partitionType == 'Apple_HFS':
                    offsetHFS = 512 * applePartitionMapInfo.find('partitionBlockStart').text
                    masterDirectoryBlockData = isoBytes[offsetHFS + 1024:offsetHFS + 1536]
                    try:
                        masterDirectoryBlockInfo = apple.parseMasterDirectoryBlock(masterDirectoryBlockData)
                        fsApple.append(masterDirectoryBlockInfo)
                        parsedMasterDirectoryBlock = True
                    except Exception:
                        parsedMasterDirectoryBlock = False

                pOffset += 512

            if 'Apple_MFS' in partitionTypes:
                fileSystemApple = 'MFS'
            elif 'Apple_HFS' in partitionTypes:
                fileSystemApple = 'HFS'
            elif 'Apple_HFSX' in partitionTypes:
                fileSystemApple = 'HFS+'
            else:
                fileSystemApple = 'Unknown'
        if containsHFSPlusVolumeHeader:
            hfsPlusHeaderData = isoBytes[1024:1536]
            try:
                hfsPlusHeaderInfo = apple.parseHFSPlusVolumeHeader(hfsPlusHeaderData)
                fsApple.append(hfsPlusHeaderInfo)
                parsedHFSPlusVolumeHeader = True
            except Exception:
                parsedHFSPlusVolumeHeader = False

        if containsAppleMasterDirectoryBlock:
            masterDirectoryBlockData = isoBytes[1024:1536]
            try:
                masterDirectoryBlockInfo = apple.parseMasterDirectoryBlock(masterDirectoryBlockData)
                fsApple.append(masterDirectoryBlockInfo)
                parsedMasterDirectoryBlock = True
            except Exception:
                parsedMasterDirectoryBlock = False

        volumeDescriptorType = -1
        noISOVolumeDescriptors = 0
        parsedPrimaryVolumeDescriptor = False
        byteStart = 32768
        if containsISO9660Signature:
            fsISO = ET.Element('fileSystem')
            while volumeDescriptorType != 255 and volumeDescriptorType != -9999:
                volumeDescriptorType, volumeDescriptorData, byteEnd = iso.getVolumeDescriptor(isoBytes, byteStart)
                noISOVolumeDescriptors += 1
                if volumeDescriptorType == 1:
                    try:
                        pvdInfo = iso.parsePrimaryVolumeDescriptor(volumeDescriptorData)
                        fsISO.append(pvdInfo)
                        parsedPrimaryVolumeDescriptor = True
                    except Exception:
                        parsedPrimaryVolumeDescriptor = False

                byteStart = byteEnd

        noExtendedVolumeDescriptors = 0
        volumeDescriptorIdentifier = 'CD001'
        while volumeDescriptorIdentifier in ('CD001', 'BEA01', 'NSR02', 'NSR03', 'BOOT2',
                                             'TEA01'):
            volumeDescriptorIdentifier, volumeDescriptorData, byteEnd = udf.getExtendedVolumeDescriptor(isoBytes, byteStart)
            if volumeDescriptorIdentifier in ('BEA01', 'NSR02', 'NSR03', 'BOOT2', 'TEA01'):
                noExtendedVolumeDescriptors += 1
            byteStart = byteEnd

        containsUDF = noExtendedVolumeDescriptors > 0
        if containsUDF:
            fsUDF = ET.Element('fileSystem')
            byteStart = 524288
            anchorVolumeDescriptorPointer = isoBytes[byteStart:byteStart + 512]
            descriptorTag = anchorVolumeDescriptorPointer[0:16]
            mainVolumeDescriptorSequenceExtent = anchorVolumeDescriptorPointer[16:24]
            reserveVolumeDescriptorSequenceExtent = anchorVolumeDescriptorPointer[24:32]
            tagIdentifier = bc.bytesToUShortIntL(descriptorTag[0:2])
            descriptorVersion = bc.bytesToUShortIntL(descriptorTag[2:4])
            extentLength = bc.bytesToUIntL(mainVolumeDescriptorSequenceExtent[0:4])
            extentLocation = bc.bytesToUIntL(mainVolumeDescriptorSequenceExtent[4:8])
            byteStart = 2048 * extentLocation
            noUDFVolumeDescriptors = 0
            while tagIdentifier != 8 and tagIdentifier != -9999:
                tagIdentifier, volumeDescriptorData, byteEnd = udf.getVolumeDescriptor(isoBytes, byteStart)
                if tagIdentifier == 6:
                    try:
                        lvdInfo = udf.parseLogicalVolumeDescriptor(volumeDescriptorData)
                        fsUDF.append(lvdInfo)
                        parsedUDFLogicalVolumeDescriptor = True
                        integritySequenceExtentLocation = lvdInfo.find('integritySequenceExtentLocation').text
                        integritySequenceExtentLength = lvdInfo.find('integritySequenceExtentLength').text
                        try:
                            lvidTagIdentifier, lvidVolumeDescriptorData, lVIDbyteEnd = udf.getVolumeDescriptor(isoBytes, 2048 * integritySequenceExtentLocation)
                            lvidInfo = udf.parseLogicalVolumeIntegrityDescriptor(lvidVolumeDescriptorData)
                            fsUDF.append(lvidInfo)
                            parsedUDFLogicalVolumeIntegrityDescriptor = True
                        except Exception:
                            parsedUDFLogicalVolumeIntegrityDescriptor = False

                    except Exception:
                        parsedUDFLogicalVolumeDescriptor = False

                if tagIdentifier == 5:
                    try:
                        pdInfo = udf.parsePartitionDescriptor(volumeDescriptorData)
                        fsUDF.append(pdInfo)
                        parsedUDFPartitionDescriptor = True
                    except Exception:
                        parsedUDFPartitionDescriptor = False

                noUDFVolumeDescriptors += 1
                byteStart = byteEnd

        if containsISO9660Signature:
            fsISO.attrib['TYPE'] = 'ISO 9660'
            fileSystems.append(fsISO)
        if containsAppleFS:
            fsApple.attrib['TYPE'] = fileSystemApple
            fileSystems.append(fsApple)
        if containsUDF:
            fsUDF.attrib['TYPE'] = 'UDF'
            fileSystems.append(fsUDF)
        if len(fileSystems) == 0:
            containsKnownFileSystem = False
        else:
            containsKnownFileSystem = True
        shared.addProperty(tests, 'containsKnownFileSystem', str(containsKnownFileSystem))
        sizeExpectedPVD = 0
        sizeExpectedZeroBlock = 0
        sizeExpectedMDB = 0
        sizeExpectedHFSPlus = 0
        sizeExpectedUDF = 0
        calculatedSizeExpected = False
        if parsedPrimaryVolumeDescriptor:
            sizeExpectedPVD = (pvdInfo.find('volumeSpaceSize').text - offset) * pvdInfo.find('logicalBlockSize').text
        if containsApplePartitionMap and parsedAppleZeroBlock:
            sizeExpectedZeroBlock = appleZeroBlockInfo.find('blockCount').text * appleZeroBlockInfo.find('blockSize').text
        if containsAppleMasterDirectoryBlock and parsedMasterDirectoryBlock:
            sizeExpectedMDB = masterDirectoryBlockInfo.find('blockCount').text * masterDirectoryBlockInfo.find('blockSize').text
        if containsHFSPlusVolumeHeader and parsedHFSPlusVolumeHeader:
            sizeExpectedHFSPlus = hfsPlusHeaderInfo.find('blockCount').text * hfsPlusHeaderInfo.find('blockSize').text
        if containsUDF and parsedUDFLogicalVolumeDescriptor and parsedUDFLogicalVolumeIntegrityDescriptor:
            sizeExpectedUDF = (pdInfo.find('partitionLength').text + pdInfo.find('partitionStartingLocation').text) * lvdInfo.find('logicalBlockSize').text
        sizeExpected = max([sizeExpectedPVD,
         sizeExpectedZeroBlock,
         sizeExpectedMDB,
         sizeExpectedHFSPlus,
         sizeExpectedUDF])
        diffSize = isoFileSize - sizeExpected
        diffSizeSectors = diffSize / 2048
        imageSmallerThanExpected = False
        if diffSize == 0 and sizeExpected != 0:
            imageHasExpectedSize = True
        elif diffSize > 0:
            imageHasExpectedSize = False
        else:
            imageHasExpectedSize = False
            imageSmallerThanExpected = True
        shared.addProperty(tests, 'sizeExpected', sizeExpected)
        shared.addProperty(tests, 'sizeActual', isoFileSize)
        shared.addProperty(tests, 'sizeDifference', diffSize)
        shared.addProperty(tests, 'sizeDifferenceSectors', diffSizeSectors)
        shared.addProperty(tests, 'sizeAsExpected', imageHasExpectedSize)
        shared.addProperty(tests, 'smallerThanExpected', imageSmallerThanExpected)
    except Exception as ex:
        success = False
        exceptionType = type(ex)
        if exceptionType == MemoryError:
            failureMessage = 'memory error (file size too large)'
        elif exceptionType == IOError:
            failureMessage = 'I/O error (cannot open file)'
        elif exceptionType == RuntimeError:
            failureMessage = 'runtime error (please report to developers)'
        else:
            failureMessage = 'unknown error (please report to developers)'
        printWarning(failureMessage)

    shared.addProperty(statusInfo, 'success', str(success))
    if not success:
        shared.addProperty(statusInfo, 'failureMessage', failureMessage)
    imageRoot.append(fileInfo)
    imageRoot.append(statusInfo)
    shared.addProperty(imageRoot, 'sectorOffset', str(offset))
    imageRoot.append(tests)
    imageRoot.append(fileSystems)
    return imageRoot


def main():
    """Main command line application"""
    global err
    global out
    if sys.version.startswith('2'):
        out = codecs.getwriter('UTF-8')(sys.stdout)
        err = codecs.getwriter('UTF-8')(sys.stderr)
    else:
        if sys.version.startswith('3'):
            out = codecs.getwriter('UTF-8')(sys.stdout.buffer)
            err = codecs.getwriter('UTF-8')(sys.stderr.buffer)
        args = parseCommandLine()
        ISOImages = glob.glob(args.ISOImages)
        sectorOffset = args.sectorOffset
        root = ET.Element('isolyzer')
        toolInfo = ET.Element('toolInfo')
        shared.addProperty(toolInfo, 'toolName', scriptName)
        shared.addProperty(toolInfo, 'toolVersion', __version__)
        root.append(toolInfo)
        for image in ISOImages:
            result = processImage(image, sectorOffset)
            root.append(result)

    makeHumanReadable(root)
    writeElement(root, out)


if __name__ == '__main__':
    main()