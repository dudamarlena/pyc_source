# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/jpylyzer/jpylyzer/boxvalidator.py
# Compiled at: 2019-10-08 11:09:01
"""Validator class for all boxes in JP2."""
from __future__ import division
import uuid, math
from . import config
from . import etpatch as ET
from . import byteconv as bc
from . import shared

class BoxValidator:
    """Marker tags/codes that identify all sub-boxes as hexadecimal strings.

    (Correspond to "Box Type" values, see ISO/IEC 15444-1 Section I.4)
    """
    typeMap = {'jp2i': 'intellectualPropertyBox', 
       'xml ': 'xmlBox', 
       'uuid': 'uuidBox', 
       'uinf': 'uuidInfoBox', 
       'jP  ': 'signatureBox', 
       'ftyp': 'fileTypeBox', 
       'jp2h': 'jp2HeaderBox', 
       'ihdr': 'imageHeaderBox', 
       'bpcc': 'bitsPerComponentBox', 
       'colr': 'colourSpecificationBox', 
       'pclr': 'paletteBox', 
       'cmap': 'componentMappingBox', 
       'cdef': 'channelDefinitionBox', 
       'res ': 'resolutionBox', 
       'jp2c': 'contiguousCodestreamBox', 
       'resc': 'captureResolutionBox', 
       'resd': 'displayResolutionBox', 
       'ulst': 'uuidListBox', 
       'url ': 'urlBox', 
       b'\xffQ': 'siz', 
       b'\xffR': 'cod', 
       b'\xff\\': 'qcd', 
       b'\xffd': 'com', 
       b'\xffS': 'coc', 
       b'\xff^': 'rgn', 
       b'\xff]': 'qcc', 
       b'\xff_': 'poc', 
       b'\xffU': 'tlm', 
       b'\xffW': 'plm', 
       b'\xffX': 'plt', 
       b'\xff`': 'ppm', 
       b'\xffa': 'ppt', 
       b'\xffc': 'crg', 
       b'\xff\x90': 'tilePart', 
       'icc': 'icc', 
       'startOfTile': 'sot'}
    boxTagMap = {v:k for k, v in typeMap.items()}

    def __init__(self, bType, boxContents, startOffset=None, components=None):
        """Initialise a BoxValidator."""
        if bType in self.typeMap:
            self.boxType = self.typeMap[bType]
        elif bType == 'JP2':
            self.characteristics = ET.Element('properties')
            self.tests = ET.Element('tests')
            self.boxType = 'JP2'
        elif bType == 'contiguousCodestreamBox':
            self.characteristics = ET.Element('properties')
            self.tests = ET.Element('tests')
            self.boxType = 'contiguousCodestreamBox'
        else:
            self.boxType = 'unknownBox'
        if bType not in ('JP2', 'contiguousCodestreamBox'):
            self.characteristics = ET.Element(self.boxType)
            self.tests = ET.Element(self.boxType)
        self.boxContents = boxContents
        self.startOffset = startOffset
        self.returnOffset = None
        self.isValid = None
        self.tilePartLength = None
        self.csiz = components
        self.bTypeString = bType
        return

    def validate(self):
        """Generic box validation function."""
        try:
            to_call = getattr(self, 'validate_' + self.boxType)
        except AttributeError:
            shared.printWarning("ignoring '" + self.boxType + "' (validator function not yet implemented)")
        else:
            to_call()

        return self

    def _isValid(self):
        for elt in self.tests.iter():
            if elt.text is False:
                return False

        return True

    def _getBox(self, byteStart, noBytes):
        """Parse JP2 box and return information on its size, type and contents."""
        boxLengthValue = bc.bytesToUInt(self.boxContents[byteStart:byteStart + 4])
        boxType = self.boxContents[byteStart + 4:byteStart + 8]
        contentsStartOffset = 8
        if boxLengthValue == 1:
            boxLengthValue = bc.bytesToULongLong(self.boxContents[byteStart + 8:byteStart + 16])
            contentsStartOffset = 16
        if boxLengthValue == 0:
            boxLengthValue = noBytes - byteStart
        byteEnd = byteStart + boxLengthValue
        boxContents = self.boxContents[byteStart + contentsStartOffset:byteEnd]
        return (
         boxLengthValue, boxType, byteEnd, boxContents)

    def _getMarkerSegment(self, offset):
        """Read marker segment that starts at offset.

        Return marker, size, contents and start offset of next marker.
        """
        marker = self.boxContents[offset:offset + 2]
        if marker in (b'\xffO', b'\xff\x93', b'\xff\xd9', b'\xff\x92'):
            length = 0
        else:
            length = bc.bytesToUShortInt(self.boxContents[offset + 2:offset + 4])
        contents = self.boxContents[offset + 2:offset + 2 + length]
        if length == -9999:
            offsetNext = -9999
        else:
            offsetNext = offset + length + 2
        return (marker, length, contents, offsetNext)

    def _calculateCompressionRatio(self, noBytes, bPCDepthValues, height, width):
        """Compute compression ratio.

        - noBytes: size of compressed image in bytes
        - bPCDepthValues: list with bits per component for each component
        - height, width: image height, width
        """
        bitsPerPixel = 0
        for i in range(len(bPCDepthValues)):
            bitsPerPixel += bPCDepthValues[i]

        bytesPerPixel = bitsPerPixel / 8
        sizeUncompressed = bytesPerPixel * height * width
        if noBytes != 0:
            compressionRatio = sizeUncompressed / noBytes
        else:
            compressionRatio = -9999
        return compressionRatio

    def _getBitValue(self, n, p):
        """Get the bit value of denary (base 10) number n.

        At the equivalent binary position p (binary count starts at position 1
        from the left).

        Only works if n can be expressed as 8 bits !!!
        """
        wordLength = 8
        shift = wordLength - p
        return n >> shift & 1

    def testFor(self, testType, testResult):
        """Add testResult node to tests element tree."""
        if config.OUTPUT_VERBOSE_FLAG is False:
            if testResult is False:
                self.tests.appendChildTagWithText(testType, testResult)
        else:
            self.tests.appendChildTagWithText(testType, testResult)

    def addCharacteristic(self, characteristic, charValue):
        """Add characteristic node to characteristics element tree."""
        self.characteristics.appendChildTagWithText(characteristic, charValue)

    def validate_unknownBox(self):
        """Process 'unknown'box.

        Although jpylyzer doesn't know anything about this box, we can at least
        report the 4 characters from the Box Type field (TBox) here.
        """
        boxType = self.bTypeString
        self.addCharacteristic('boxType', boxType)
        shared.printWarning('ignoring unknown box')

    def validate_signatureBox(self):
        """Signature box (ISO/IEC 15444-1 Section I.5.2)."""
        self.testFor('boxLengthIsValid', len(self.boxContents) == 4)
        self.testFor('signatureIsValid', self.boxContents[0:4] == b'\r\n\x87\n')

    def validate_fileTypeBox(self):
        """File type box (ISO/IEC 15444-1 Section I.5.2)."""
        numberOfCompatibilityFields = (len(self.boxContents) - 8) / 4
        self.testFor('boxLengthIsValid', numberOfCompatibilityFields == int(numberOfCompatibilityFields))
        br = self.boxContents[0:4]
        self.addCharacteristic('br', br)
        self.testFor('brandIsValid', br == 'jp2 ')
        minV = bc.bytesToUInt(self.boxContents[4:8])
        self.addCharacteristic('minV', minV)
        self.testFor('minorVersionIsValid', minV == 0)
        cLList = []
        offset = 8
        for _ in range(int(numberOfCompatibilityFields)):
            cL = self.boxContents[offset:offset + 4]
            self.addCharacteristic('cL', cL)
            cLList.append(cL)
            offset += 4

        self.testFor('compatibilityListIsValid', 'jp2 ' in cLList)

    def validate_jp2HeaderBox(self):
        """JP2 header box (superbox) (ISO/IEC 15444-1 Section I.5.3)."""
        subBoxTypes = []
        noBytes = len(self.boxContents)
        byteStart = 0
        boxLengthValue = 10
        while byteStart < noBytes and boxLengthValue not in (0, -9999):
            boxLengthValue, boxType, byteEnd, subBoxContents = self._getBox(byteStart, noBytes)
            resultsBox = BoxValidator(boxType, subBoxContents).validate()
            testsBox = resultsBox.tests
            characteristicsBox = resultsBox.characteristics
            byteStart = byteEnd
            subBoxTypes.append(boxType)
            self.tests.appendIfNotEmpty(testsBox)
            self.characteristics.append(characteristicsBox)

        self.testFor('containsImageHeaderBox', self.boxTagMap['imageHeaderBox'] in subBoxTypes)
        self.testFor('containsColourSpecificationBox', self.boxTagMap['colourSpecificationBox'] in subBoxTypes)
        sign = self.characteristics.findElementText('imageHeaderBox/bPCSign')
        depth = self.characteristics.findElementText('imageHeaderBox/bPCDepth')
        if sign == 1 and depth == 128:
            self.testFor('containsBitsPerComponentBox', self.boxTagMap['bitsPerComponentBox'] in subBoxTypes)
        try:
            firstJP2HeaderBoxIsImageHeaderBox = subBoxTypes[0] == self.boxTagMap['imageHeaderBox']
        except Exception:
            firstJP2HeaderBoxIsImageHeaderBox = False

        self.testFor('firstJP2HeaderBoxIsImageHeaderBox', firstJP2HeaderBoxIsImageHeaderBox)
        self.testFor('noMoreThanOneImageHeaderBox', subBoxTypes.count(self.boxTagMap['imageHeaderBox']) <= 1)
        self.testFor('noMoreThanOneBitsPerComponentBox', subBoxTypes.count(self.boxTagMap['bitsPerComponentBox']) <= 1)
        self.testFor('noMoreThanOnePaletteBox', subBoxTypes.count(self.boxTagMap['paletteBox']) <= 1)
        self.testFor('noMoreThanOneComponentMappingBox', subBoxTypes.count(self.boxTagMap['componentMappingBox']) <= 1)
        self.testFor('noMoreThanOneChannelDefinitionBox', subBoxTypes.count(self.boxTagMap['channelDefinitionBox']) <= 1)
        self.testFor('noMoreThanOneResolutionBox', subBoxTypes.count(self.boxTagMap['resolutionBox']) <= 1)
        colourSpecificationBoxesAreContiguous = shared.listOccurrencesAreContiguous(subBoxTypes, self.boxTagMap['colourSpecificationBox'])
        self.testFor('colourSpecificationBoxesAreContiguous', colourSpecificationBoxesAreContiguous)
        if self.boxTagMap['paletteBox'] in subBoxTypes and self.boxTagMap['componentMappingBox'] not in subBoxTypes or self.boxTagMap['componentMappingBox'] in subBoxTypes and self.boxTagMap['paletteBox'] not in subBoxTypes:
            paletteAndComponentMappingBoxesOnlyTogether = False
        else:
            paletteAndComponentMappingBoxesOnlyTogether = True
        self.testFor('paletteAndComponentMappingBoxesOnlyTogether', paletteAndComponentMappingBoxesOnlyTogether)

    def validate_imageHeaderBox(self):
        """Image header box (ISO/IEC 15444-1 Section I.5.3.1).

        This is a fixed-length box that contains generic image info.
        """
        self.testFor('boxLengthIsValid', len(self.boxContents) == 14)
        height = bc.bytesToUInt(self.boxContents[0:4])
        self.addCharacteristic('height', height)
        width = bc.bytesToUInt(self.boxContents[4:8])
        self.addCharacteristic('width', width)
        self.testFor('heightIsValid', 1 <= height <= 4294967295)
        self.testFor('widthIsValid', 1 <= width <= 4294967295)
        nC = bc.bytesToUShortInt(self.boxContents[8:10])
        self.addCharacteristic('nC', nC)
        self.testFor('nCIsValid', 1 <= nC <= 16384)
        bPC = bc.bytesToUnsignedChar(self.boxContents[10:11])
        bPCSign = self._getBitValue(bPC, 1)
        self.addCharacteristic('bPCSign', bPCSign)
        bPCDepth = (bPC & 127) + 1
        self.addCharacteristic('bPCDepth', bPCDepth)
        bPCDepthIsWithinAllowedRange = 1 <= bPCDepth <= 38
        bitDepthIsVariable = 1 <= bPC <= 255
        if bPCDepthIsWithinAllowedRange or bitDepthIsVariable:
            bPCIsValid = True
        else:
            bPCIsValid = False
        self.testFor('bPCIsValid', bPCIsValid)
        c = bc.bytesToUnsignedChar(self.boxContents[11:12])
        self.addCharacteristic('c', c)
        self.testFor('cIsValid', c == 7)
        unkC = bc.bytesToUnsignedChar(self.boxContents[12:13])
        self.addCharacteristic('unkC', unkC)
        self.testFor('unkCIsValid', 0 <= unkC <= 1)
        iPR = bc.bytesToUnsignedChar(self.boxContents[13:14])
        self.addCharacteristic('iPR', iPR)
        self.testFor('iPRIsValid', 0 <= iPR <= 1)

    def validate_bitsPerComponentBox(self):
        """Validate Bits per component box (ISO/IEC 15444-1 Section I.5.3.2).

        Optional box that specifies bit depth of each component.
        """
        numberOfBPFields = len(self.boxContents)
        for i in range(numberOfBPFields):
            bPC = bc.bytesToUnsignedChar(self.boxContents[i:i + 1])
            bPCSign = self._getBitValue(bPC, 1)
            self.addCharacteristic('bPCSign', bPCSign)
            bPCDepth = (bPC & 127) + 1
            self.addCharacteristic('bPCDepth', bPCDepth)
            self.testFor('bPCIsValid', 1 <= bPCDepth <= 38)

    def validate_colourSpecificationBox(self):
        """Colour specification box (ISO/IEC 15444-1 Section I.5.3.3).

        This box defines one method for interpreting colourspace of decompressed
        image data.
        """
        length = len(self.boxContents)
        meth = bc.bytesToUnsignedChar(self.boxContents[0:1])
        self.addCharacteristic('meth', meth)
        self.testFor('methIsValid', 1 <= meth <= 2)
        prec = bc.bytesToUnsignedChar(self.boxContents[1:2])
        self.addCharacteristic('prec', prec)
        self.testFor('precIsValid', prec == 0)
        approx = bc.bytesToUnsignedChar(self.boxContents[2:3])
        self.addCharacteristic('approx', approx)
        self.testFor('approxIsValid', approx == 0)
        if meth == 1:
            enumCS = bc.bytesToUInt(self.boxContents[3:length])
            self.addCharacteristic('enumCS', enumCS)
            self.testFor('enumCSIsValid', enumCS in (16, 17, 18))
        elif meth == 2:
            profile = self.boxContents[3:length]
            iccResults = BoxValidator('icc', profile).validate()
            iccCharacteristics = iccResults.characteristics
            self.characteristics.append(iccCharacteristics)
            profileSize = iccCharacteristics.findElementText('profileSize')
            self.testFor('iccSizeIsValid', profileSize == len(profile))
            profileClass = iccCharacteristics.findElementText('profileClass')
            self.testFor('iccPermittedProfileClass', profileClass in ('scnr', 'mntr'))
            tagSignatureElements = iccCharacteristics.findall('tag')
            tagSignatures = []
            for i in range(len(tagSignatureElements)):
                tagSignatures.append(tagSignatureElements[i].text)

            self.testFor('iccNoLUTBasedProfile', 'A2B0' not in tagSignatures)
        elif meth == 3:
            profile = self.boxContents[3:length]
            iccResults = BoxValidator('icc', profile).validate()
            iccCharacteristics = iccResults.characteristics
            self.characteristics.append(iccCharacteristics)

    def validate_icc(self):
        """Extract characteristics (property-value pairs) of ICC profile.

        Note that although values are stored in  'text' property of sub-elements,
        they may have a type other than 'text' (binary string, integers, lists)
        This means that some post-processing (conversion to text) is needed to
        write these property-value pairs to XML
        """
        profileSize = bc.bytesToUInt(self.boxContents[0:4])
        self.addCharacteristic('profileSize', profileSize)
        preferredCMMType = self.boxContents[4:8]
        self.addCharacteristic('preferredCMMType', preferredCMMType)
        profileMajorRevision = bc.bytesToUnsignedChar(self.boxContents[8:9])
        profileMinorRevisionByte = bc.bytesToUnsignedChar(self.boxContents[9:10])
        profileMinorRevision = profileMinorRevisionByte >> 4
        profileBugFixRevision = profileMinorRevisionByte & 15
        profileVersion = '%s.%s.%s' % (
         profileMajorRevision, profileMinorRevision, profileBugFixRevision)
        self.addCharacteristic('profileVersion', profileVersion)
        profileClass = self.boxContents[12:16]
        self.addCharacteristic('profileClass', profileClass)
        colourSpace = self.boxContents[16:20]
        self.addCharacteristic('colourSpace', colourSpace)
        profileConnectionSpace = self.boxContents[20:24]
        self.addCharacteristic('profileConnectionSpace', profileConnectionSpace)
        year = bc.bytesToUShortInt(self.boxContents[24:26])
        month = bc.bytesToUnsignedChar(self.boxContents[27:28])
        day = bc.bytesToUnsignedChar(self.boxContents[29:30])
        hour = bc.bytesToUnsignedChar(self.boxContents[31:32])
        minute = bc.bytesToUnsignedChar(self.boxContents[33:34])
        second = bc.bytesToUnsignedChar(self.boxContents[35:36])
        dateString = '%d/%02d/%02d' % (year, month, day)
        timeString = '%02d:%02d:%02d' % (hour, minute, second)
        dateTimeString = '%s, %s' % (dateString, timeString)
        self.addCharacteristic('dateTimeString', dateTimeString)
        profileSignature = self.boxContents[36:40]
        self.addCharacteristic('profileSignature', profileSignature)
        primaryPlatform = self.boxContents[40:44]
        self.addCharacteristic('primaryPlatform', primaryPlatform)
        profileFlags = bc.bytesToUnsignedChar(self.boxContents[44:45])
        embeddedProfile = self._getBitValue(profileFlags, 1)
        self.addCharacteristic('embeddedProfile', embeddedProfile)
        profileCannotBeUsedIndependently = self._getBitValue(profileFlags, 2)
        self.addCharacteristic('profileCannotBeUsedIndependently', profileCannotBeUsedIndependently)
        deviceManufacturer = self.boxContents[48:52]
        self.addCharacteristic('deviceManufacturer', deviceManufacturer)
        deviceModel = self.boxContents[52:56]
        self.addCharacteristic('deviceModel', deviceModel)
        deviceAttributes = bc.bytesToUnsignedChar(self.boxContents[56:57])
        transparency = self._getBitValue(deviceAttributes, 1)
        self.addCharacteristic('transparency', transparency)
        glossiness = self._getBitValue(deviceAttributes, 2)
        self.addCharacteristic('glossiness', glossiness)
        polarity = self._getBitValue(deviceAttributes, 3)
        self.addCharacteristic('polarity', polarity)
        colour = self._getBitValue(deviceAttributes, 4)
        self.addCharacteristic('colour', colour)
        renderingIntent = bc.bytesToUShortInt(self.boxContents[66:68])
        self.addCharacteristic('renderingIntent', renderingIntent)
        connectionSpaceIlluminantX = round(bc.bytesToUInt(self.boxContents[68:72]) / 65536, 4)
        self.addCharacteristic('connectionSpaceIlluminantX', connectionSpaceIlluminantX)
        connectionSpaceIlluminantY = round(bc.bytesToUInt(self.boxContents[72:76]) / 65536, 4)
        self.addCharacteristic('connectionSpaceIlluminantY', connectionSpaceIlluminantY)
        connectionSpaceIlluminantZ = round(bc.bytesToUInt(self.boxContents[76:80]) / 65536, 4)
        self.addCharacteristic('connectionSpaceIlluminantZ', connectionSpaceIlluminantZ)
        profileCreator = self.boxContents[80:84]
        self.addCharacteristic('profileCreator', profileCreator)
        profileID = bc.bytesToHex(self.boxContents[84:100])
        self.addCharacteristic('profileID', profileID)
        tagCount = bc.bytesToUInt(self.boxContents[128:132])
        tagCount = min(tagCount, 4096)
        tagSignatures = []
        tagOffsets = []
        tagSizes = []
        tagStart = 132
        for i in range(tagCount):
            tagSignature = self.boxContents[tagStart:tagStart + 4]
            tagOffset = bc.bytesToUInt(self.boxContents[tagStart + 4:tagStart + 8])
            tagSize = bc.bytesToUInt(self.boxContents[tagStart + 8:tagStart + 12])
            self.addCharacteristic('tag', tagSignature)
            tagSignatures.append(tagSignature)
            tagOffsets.append(tagOffset)
            tagSizes.append(tagSize)
            tagStart += 12

        try:
            i = tagSignatures.index('desc')
            descStartOffset = tagOffsets[i]
            descSize = tagSizes[i]
            descTag = self.boxContents[descStartOffset:descStartOffset + descSize]
            descriptionLength = bc.bytesToUInt(descTag[8:12])
            description = descTag[12:12 + descriptionLength - 1]
        except Exception:
            description = ''

        self.addCharacteristic('description', description)

    def validate_paletteBox(self):
        """Palette box (ISO/IEC 15444-1 Section I.5.3.4).

        Optional box that specifies a palette
        """
        nE = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('nE', nE)
        self.testFor('nEIsValid', 1 <= nE <= 1024)
        nPC = bc.bytesToUnsignedChar(self.boxContents[2:3])
        self.addCharacteristic('nPC', nPC)
        self.testFor('nPCIsValid', 1 <= nPC <= 255)
        for i in range(nPC):
            b = bc.bytesToUnsignedChar(self.boxContents[3 + i:4 + i])
            bSign = self._getBitValue(b, 1)
            self.addCharacteristic('bSign', bSign)
            bDepth = (b & 127) + 1
            self.addCharacteristic('bDepth', bDepth)
            self.testFor('bDepthIsValid', 1 <= bDepth <= 38)
            bDepthPadded = math.ceil(bDepth / 8) * 8
            bytesPadded = int(bDepthPadded / 8)
            offset = nPC + 3 + i * (nE * bytesPadded)
            for _ in range(nE):
                cPAsBytes = self.boxContents[offset:offset + bytesPadded]
                cP = bc.bytesToInteger(cPAsBytes)
                self.addCharacteristic('cP', cP)
                offset += bytesPadded

    def validate_componentMappingBox(self):
        """Component mapping box (ISO/IEC 15444-1 Section I.5.3.5).

        This box defines how image channels are identified from actual
        components
        """
        numberOfChannels = int(len(self.boxContents) / 4)
        offset = 0
        for _ in range(numberOfChannels):
            cMP = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
            self.addCharacteristic('cMP', cMP)
            self.testFor('cMPIsValid', 0 <= cMP <= 16384)
            mTyp = bc.bytesToUnsignedChar(self.boxContents[offset + 2:offset + 3])
            self.addCharacteristic('mTyp', mTyp)
            self.testFor('mTypIsValid', 0 <= mTyp <= 1)
            pCol = bc.bytesToUnsignedChar(self.boxContents[offset + 3:offset + 4])
            self.addCharacteristic('pCol', pCol)
            if mTyp == 0:
                pColIsValid = pCol == 0
            else:
                pColIsValid = True
            self.testFor('pColIsValid', pColIsValid)
            offset += 4

    def validate_channelDefinitionBox(self):
        """Channel definition box (ISO/IEC 15444-1 Section I.5.3.6).

        This box specifies the meaning of the samples in each channel in the
        image.
        """
        n = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('n', n)
        self.testFor('nIsValid', 1 <= n <= 65535)
        boxLengthIsValid = len(self.boxContents) - 2 == n * 6
        self.testFor('boxLengthIsValid', boxLengthIsValid)
        offset = 2
        for _ in range(n):
            cN = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
            self.addCharacteristic('cN', cN)
            self.testFor('cNIsValid', 0 <= cN <= 65535)
            cTyp = bc.bytesToUShortInt(self.boxContents[offset + 2:offset + 4])
            self.addCharacteristic('cTyp', cTyp)
            self.testFor('cTypIsValid', 0 <= cTyp <= 65535)
            cAssoc = bc.bytesToUShortInt(self.boxContents[offset + 4:offset + 6])
            self.addCharacteristic('cAssoc', cAssoc)
            self.testFor('cAssocIsValid', 0 <= cTyp <= 65535)
            offset += 6

    def validate_resolutionBox(self):
        """Resolution box (superbox)(ISO/IEC 15444-1 Section I.5.3.7.

        Specifies the capture and/or default display grid resolutions of
        the image.
        """
        tagCaptureResolutionBox = 'resc'
        tagDisplayResolutionBox = 'resd'
        subBoxTypes = []
        noBytes = len(self.boxContents)
        byteStart = 0
        boxLengthValue = 10
        while byteStart < noBytes and boxLengthValue not in (0, -9999):
            boxLengthValue, boxType, byteEnd, subBoxContents = self._getBox(byteStart, noBytes)
            resultsBox = BoxValidator(boxType, subBoxContents).validate()
            testsBox = resultsBox.tests
            characteristicsBox = resultsBox.characteristics
            byteStart = byteEnd
            subBoxTypes.append(boxType)
            self.tests.appendIfNotEmpty(testsBox)
            self.characteristics.append(characteristicsBox)

        self.testFor('containsCaptureOrDisplayResolutionBox', tagCaptureResolutionBox in subBoxTypes or tagDisplayResolutionBox in subBoxTypes)
        self.testFor('noMoreThanOneCaptureResolutionBox', subBoxTypes.count(tagCaptureResolutionBox) <= 1)
        self.testFor('noMoreThanOneDisplayResolutionBox', subBoxTypes.count(tagDisplayResolutionBox) <= 1)

    def validate_captureResolutionBox(self):
        """Capture  Resolution Box (ISO/IEC 15444-1 Section I.5.3.7.1)."""
        self.testFor('boxLengthIsValid', len(self.boxContents) == 10)
        vRcN = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('vRcN', vRcN)
        self.testFor('vRcNIsValid', 1 <= vRcN <= 65535)
        vRcD = bc.bytesToUShortInt(self.boxContents[2:4])
        self.addCharacteristic('vRcD', vRcD)
        self.testFor('vRcDIsValid', 1 <= vRcD <= 65535)
        hRcN = bc.bytesToUShortInt(self.boxContents[4:6])
        self.addCharacteristic('hRcN', hRcN)
        self.testFor('hRcNIsValid', 1 <= hRcN <= 65535)
        hRcD = bc.bytesToUShortInt(self.boxContents[6:8])
        self.addCharacteristic('hRcD', hRcD)
        self.testFor('hRcDIsValid', 1 <= hRcD <= 65535)
        vRcE = bc.bytesToSignedChar(self.boxContents[8:9])
        self.addCharacteristic('vRcE', vRcE)
        self.testFor('vRcEIsValid', -128 <= vRcE <= 127)
        hRcE = bc.bytesToSignedChar(self.boxContents[9:10])
        self.addCharacteristic('hRcE', hRcE)
        self.testFor('hRcEIsValid', -128 <= hRcE <= 127)
        vRescInPixelsPerMeter = vRcN / vRcD * 10 ** vRcE
        self.addCharacteristic('vRescInPixelsPerMeter', round(vRescInPixelsPerMeter, 2))
        hRescInPixelsPerMeter = hRcN / hRcD * 10 ** hRcE
        self.addCharacteristic('hRescInPixelsPerMeter', round(hRescInPixelsPerMeter, 2))
        vRescInPixelsPerInch = vRescInPixelsPerMeter * 0.0254
        self.addCharacteristic('vRescInPixelsPerInch', round(vRescInPixelsPerInch, 2))
        hRescInPixelsPerInch = hRescInPixelsPerMeter * 0.0254
        self.addCharacteristic('hRescInPixelsPerInch', round(hRescInPixelsPerInch, 2))

    def validate_displayResolutionBox(self):
        """Default Display  Resolution Box (ISO/IEC 15444-1 Section I.5.3.7.2)."""
        self.testFor('boxLengthIsValid', len(self.boxContents) == 10)
        vRdN = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('vRdN', vRdN)
        self.testFor('vRdNIsValid', 1 <= vRdN <= 65535)
        vRdD = bc.bytesToUShortInt(self.boxContents[2:4])
        self.addCharacteristic('vRdD', vRdD)
        self.testFor('vRdDIsValid', 1 <= vRdD <= 65535)
        hRdN = bc.bytesToUShortInt(self.boxContents[4:6])
        self.addCharacteristic('hRdN', hRdN)
        self.testFor('hRdNIsValid', 1 <= hRdN <= 65535)
        hRdD = bc.bytesToUShortInt(self.boxContents[6:8])
        self.addCharacteristic('hRdD', hRdD)
        self.testFor('hRdDIsValid', 1 <= hRdD <= 65535)
        vRdE = bc.bytesToSignedChar(self.boxContents[8:9])
        self.addCharacteristic('vRdE', vRdE)
        self.testFor('vRdEIsValid', -128 <= vRdE <= 127)
        hRdE = bc.bytesToSignedChar(self.boxContents[9:10])
        self.addCharacteristic('hRdE', hRdE)
        self.testFor('hRdEIsValid', -128 <= hRdE <= 127)
        vResdInPixelsPerMeter = vRdN / vRdD * 10 ** vRdE
        self.addCharacteristic('vResdInPixelsPerMeter', round(vResdInPixelsPerMeter, 2))
        hResdInPixelsPerMeter = hRdN / hRdD * 10 ** hRdE
        self.addCharacteristic('hResdInPixelsPerMeter', round(hResdInPixelsPerMeter, 2))
        vResdInPixelsPerInch = vResdInPixelsPerMeter * 0.0254
        self.addCharacteristic('vResdInPixelsPerInch', round(vResdInPixelsPerInch, 2))
        hResdInPixelsPerInch = hResdInPixelsPerMeter * 0.0254
        self.addCharacteristic('hResdInPixelsPerInch', round(hResdInPixelsPerInch, 2))

    def validate_contiguousCodestreamBox(self):
        """Validate Contiguous codestream box (ISO/IEC 15444-1 Section I.5.4)."""
        length = len(self.boxContents)
        offset = 0
        marker, _, segContents, offsetNext = self._getMarkerSegment(offset)
        self.testFor('codestreamStartsWithSOCMarker', marker == b'\xffO')
        offset = offsetNext
        marker, _, segContents, offsetNext = self._getMarkerSegment(offset)
        foundSIZMarker = marker == b'\xffQ'
        self.testFor('foundSIZMarker', foundSIZMarker)
        if foundSIZMarker:
            resultsSIZ = BoxValidator(marker, segContents).validate()
            testsSIZ = resultsSIZ.tests
            characteristicsSIZ = resultsSIZ.characteristics
            self.tests.appendIfNotEmpty(testsSIZ)
            self.characteristics.append(characteristicsSIZ)
            csiz = characteristicsSIZ.findElementText('csiz')
            offset = offsetNext
            foundCODMarker = False
            foundQCDMarker = False
            while marker != b'\xff\x90' and offsetNext != -9999:
                marker, _, segContents, offsetNext = self._getMarkerSegment(offset)
                if marker == b'\xffR':
                    foundCODMarker = True
                    resultsCOD = BoxValidator(marker, segContents).validate()
                    testsCOD = resultsCOD.tests
                    characteristicsCOD = resultsCOD.characteristics
                    self.tests.appendIfNotEmpty(testsCOD)
                    self.characteristics.append(characteristicsCOD)
                    offset = offsetNext
                elif marker == b'\xffS':
                    resultsCOC = BoxValidator(marker, segContents, components=csiz).validate()
                    testsCOC = resultsCOC.tests
                    characteristicsCOC = resultsCOC.characteristics
                    self.tests.appendIfNotEmpty(testsCOC)
                    self.characteristics.append(characteristicsCOC)
                    offset = offsetNext
                elif marker == b'\xff\\':
                    foundQCDMarker = True
                    resultsQCD = BoxValidator(marker, segContents).validate()
                    testsQCD = resultsQCD.tests
                    characteristicsQCD = resultsQCD.characteristics
                    self.tests.appendIfNotEmpty(testsQCD)
                    self.characteristics.append(characteristicsQCD)
                    offset = offsetNext
                elif marker == b'\xff]':
                    resultsQCC = BoxValidator(marker, segContents, components=csiz).validate()
                    testsQCC = resultsQCC.tests
                    characteristicsQCC = resultsQCC.characteristics
                    self.tests.appendIfNotEmpty(testsQCC)
                    self.characteristics.append(characteristicsQCC)
                    offset = offsetNext
                elif marker == b'\xff^':
                    resultsRGN = BoxValidator(marker, segContents, components=csiz).validate()
                    testsRGN = resultsRGN.tests
                    characteristicsRGN = resultsRGN.characteristics
                    self.tests.appendIfNotEmpty(testsRGN)
                    self.characteristics.append(characteristicsRGN)
                    offset = offsetNext
                elif marker == b'\xff_':
                    resultsPOC = BoxValidator(marker, segContents, components=csiz).validate()
                    testsPOC = resultsPOC.tests
                    characteristicsPOC = resultsPOC.characteristics
                    self.tests.appendIfNotEmpty(testsPOC)
                    self.characteristics.append(characteristicsPOC)
                    offset = offsetNext
                elif marker == b'\xffc':
                    resultsCRG = BoxValidator(marker, segContents, components=csiz).validate()
                    testsCRG = resultsCRG.tests
                    characteristicsCRG = resultsCRG.characteristics
                    self.tests.appendIfNotEmpty(testsCRG)
                    self.characteristics.append(characteristicsCRG)
                    offset = offsetNext
                elif marker == b'\xffd':
                    resultsCOM = BoxValidator(marker, segContents).validate()
                    testsCOM = resultsCOM.tests
                    characteristicsCOM = resultsCOM.characteristics
                    self.tests.appendIfNotEmpty(testsCOM)
                    self.characteristics.append(characteristicsCOM)
                    offset = offsetNext
                elif marker == b'\xff\x90':
                    pass
                elif marker in (b'\xffU', b'\xffW', b'\xff`'):
                    resultsOther = BoxValidator(marker, segContents).validate()
                    testsOther = resultsOther.tests
                    characteristicsOther = resultsOther.characteristics
                    self.tests.appendIfNotEmpty(testsOther)
                    self.characteristics.append(characteristicsOther)
                    offset = offsetNext
                else:
                    offset = offsetNext

            self.testFor('foundCODMarker', foundCODMarker)
            self.testFor('foundQCDMarker', foundQCDMarker)
            numberOfTilesExpected = self.characteristics.findElementText('siz/numberOfTiles')
            if not numberOfTilesExpected:
                numberOfTilesExpected = 0
            numberOfTilesExpected = min(numberOfTilesExpected, 65535)
            tileIndices = []
            tilePartsPerTileExpected = {}
            tilePartsPerTileFound = {}
            for i in range(numberOfTilesExpected):
                tilePartsPerTileFound[i] = 0

            tilePartCharacteristics = ET.Element('tileParts')
            tilePartTests = ET.Element('tileParts')
            while marker == b'\xff\x90':
                marker = self.boxContents[offset:offset + 2]
                if marker == b'\xff\x90':
                    resultsTilePart = BoxValidator(marker, self.boxContents, startOffset=offset, components=csiz).validate()
                    testsTilePart = resultsTilePart.tests
                    characteristicsTilePart = resultsTilePart.characteristics
                    offsetNext = resultsTilePart.returnOffset
                    tilePartTests.appendIfNotEmpty(testsTilePart)
                    tilePartCharacteristics.append(characteristicsTilePart)
                    tileIndex = characteristicsTilePart.findElementText('sot/isot')
                    tilePartsOfTile = characteristicsTilePart.findElementText('sot/tnsot')
                    if tileIndex not in tileIndices:
                        tileIndices.append(tileIndex)
                    if tilePartsOfTile != 0:
                        tilePartsPerTileExpected[tileIndex] = tilePartsOfTile
                    try:
                        tilePartsPerTileFound[tileIndex] = tilePartsPerTileFound[tileIndex] + 1
                    except KeyError:
                        break

                    if offsetNext != offset:
                        offset = offsetNext
                    else:
                        break

            self.testFor('foundExpectedNumberOfTiles', len(tileIndices) == numberOfTilesExpected)
            self.testFor('foundExpectedNumberOfTileParts', len(set(tilePartsPerTileExpected.items())) == len(set(tilePartsPerTileFound.items())))
            self.characteristics.append(tilePartCharacteristics)
            self.tests.appendIfNotEmpty(tilePartTests)
            ccocElements = self.characteristics.findall('coc/ccoc') + self.characteristics.findall('tileParts/tilePart/coc/ccoc')
            ccocValues = []
            for ccocElement in ccocElements:
                ccocValues.append(ccocElement.text)

            if ccocValues:
                self.testFor('maxOneCcocPerComponent', len(set(ccocValues)) == len(ccocValues))
            cqccElements = self.characteristics.findall('qcc/cqcc') + self.characteristics.findall('tileParts/tilePart/qcc/cqcc')
            cqccValues = []
            for cqccElement in cqccElements:
                cqccValues.append(cqccElement.text)

            if cqccValues:
                self.testFor('maxOneCqccPerComponent', len(set(cqccValues)) == len(cqccValues))
            self.testFor('foundEOCMarker', self.boxContents[length - 2:length] == b'\xff\xd9')
        self.isValid = self._isValid()

    def validate_siz(self):
        """Image and tile size (SIZ) header fields (ISO/IEC 15444-1 Section A.5.1)."""
        lsiz = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lsiz', lsiz)
        self.testFor('lsizIsValid', 41 <= lsiz <= 49190)
        rsiz = bc.bytesToUShortInt(self.boxContents[2:4])
        self.addCharacteristic('rsiz', rsiz)
        self.testFor('rsizIsValid', rsiz in (0, 1, 2))
        xsiz = bc.bytesToUInt(self.boxContents[4:8])
        self.addCharacteristic('xsiz', xsiz)
        self.testFor('xsizIsValid', 1 <= xsiz <= 4294967295)
        ysiz = bc.bytesToUInt(self.boxContents[8:12])
        self.addCharacteristic('ysiz', ysiz)
        self.testFor('ysizIsValid', 1 <= ysiz <= 4294967295)
        xOsiz = bc.bytesToUInt(self.boxContents[12:16])
        self.addCharacteristic('xOsiz', xOsiz)
        self.testFor('xOsizIsValid', 0 <= xOsiz <= 4294967294)
        yOsiz = bc.bytesToUInt(self.boxContents[16:20])
        self.addCharacteristic('yOsiz', yOsiz)
        self.testFor('yOsizIsValid', 0 <= yOsiz <= 4294967294)
        xTsiz = bc.bytesToUInt(self.boxContents[20:24])
        self.addCharacteristic('xTsiz', xTsiz)
        self.testFor('xTsizIsValid', 1 <= xTsiz <= 4294967295)
        yTsiz = bc.bytesToUInt(self.boxContents[24:28])
        self.addCharacteristic('yTsiz', yTsiz)
        self.testFor('yTsizIsValid', 1 <= yTsiz <= 4294967295)
        xTOsiz = bc.bytesToUInt(self.boxContents[28:32])
        self.addCharacteristic('xTOsiz', xTOsiz)
        self.testFor('xTOsizIsValid', 0 <= xTOsiz <= 4294967294)
        yTOsiz = bc.bytesToUInt(self.boxContents[32:36])
        self.addCharacteristic('yTOsiz', yTOsiz)
        self.testFor('yTOsizIsValid', 0 <= yTOsiz <= 4294967294)
        if xTsiz != 0 and yTsiz != 0:
            numberOfTilesX = math.ceil((xsiz - xOsiz) / xTsiz)
            numberOfTilesY = math.ceil((ysiz - yOsiz) / yTsiz)
            numberOfTiles = int(numberOfTilesX * numberOfTilesY)
        else:
            numberOfTiles = 0
        self.addCharacteristic('numberOfTiles', numberOfTiles)
        csiz = bc.bytesToUShortInt(self.boxContents[36:38])
        self.addCharacteristic('csiz', csiz)
        self.testFor('csizIsValid', 1 <= csiz <= 16384)
        self.testFor('lsizConsistentWithCsiz', lsiz == 38 + 3 * csiz)
        offset = 38
        for _ in range(csiz):
            ssiz = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
            ssizSign = self._getBitValue(ssiz, 1)
            self.addCharacteristic('ssizSign', ssizSign)
            ssizDepth = (ssiz & 127) + 1
            self.addCharacteristic('ssizDepth', ssizDepth)
            self.testFor('ssizIsValid', 1 <= ssizDepth <= 38)
            xRsiz = bc.bytesToUnsignedChar(self.boxContents[offset + 1:offset + 2])
            self.addCharacteristic('xRsiz', xRsiz)
            self.testFor('xRsizIsValid', 1 <= xRsiz <= 255)
            yRsiz = bc.bytesToUnsignedChar(self.boxContents[offset + 2:offset + 3])
            self.addCharacteristic('yRsiz', yRsiz)
            self.testFor('yRsizIsValid', 1 <= yRsiz <= 255)
            offset += 3

    def validate_cod(self):
        """Coding style default (COD) header fields (ISO/IEC 15444-1 Section A.6.1)."""
        lcod = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lcod', lcod)
        lcodIsValid = 12 <= lcod <= 45
        self.testFor('lcodIsValid', lcodIsValid)
        scod = bc.bytesToUnsignedChar(self.boxContents[2:3])
        precincts = self._getBitValue(scod, 8)
        self.addCharacteristic('precincts', precincts)
        sop = self._getBitValue(scod, 7)
        self.addCharacteristic('sop', sop)
        eph = self._getBitValue(scod, 6)
        self.addCharacteristic('eph', eph)
        sGcod = self.boxContents[3:7]
        order = bc.bytesToUnsignedChar(sGcod[0:1])
        self.addCharacteristic('order', order)
        orderIsValid = order in (0, 1, 2, 3, 4)
        self.testFor('orderIsValid', orderIsValid)
        layers = bc.bytesToUShortInt(sGcod[1:3])
        self.addCharacteristic('layers', layers)
        layersIsValid = 1 <= layers <= 65535
        self.testFor('layersIsValid', layersIsValid)
        multipleComponentTransformation = bc.bytesToUnsignedChar(sGcod[3:4])
        self.addCharacteristic('multipleComponentTransformation', multipleComponentTransformation)
        multipleComponentTransformationIsValid = multipleComponentTransformation in (0,
                                                                                     1)
        self.testFor('multipleComponentTransformationIsValid', multipleComponentTransformationIsValid)
        levels = bc.bytesToUnsignedChar(self.boxContents[7:8])
        self.addCharacteristic('levels', levels)
        levelsIsValid = 0 <= levels <= 32
        self.testFor('levelsIsValid', levelsIsValid)
        if precincts == 1:
            lcodExpected = 13 + levels
        else:
            lcodExpected = 12
        lcodConsistencyCheck = lcod == lcodExpected
        self.testFor('lcodConsistencyCheck', lcodConsistencyCheck)
        codeBlockWidthExponent = bc.bytesToUnsignedChar(self.boxContents[8:9]) + 2
        self.addCharacteristic('codeBlockWidth', 2 ** codeBlockWidthExponent)
        codeBlockWidthExponentIsValid = 2 <= codeBlockWidthExponent <= 10
        self.testFor('codeBlockWidthExponentIsValid', codeBlockWidthExponentIsValid)
        codeBlockHeightExponent = bc.bytesToUnsignedChar(self.boxContents[9:10]) + 2
        self.addCharacteristic('codeBlockHeight', 2 ** codeBlockHeightExponent)
        codeBlockHeightExponentIsValid = 2 <= codeBlockHeightExponent <= 10
        self.testFor('codeBlockHeightExponentIsValid', codeBlockHeightExponentIsValid)
        sumHeightWidthExponentIsValid = codeBlockWidthExponent + codeBlockHeightExponent <= 12
        self.testFor('sumHeightWidthExponentIsValid', sumHeightWidthExponentIsValid)
        codeBlockStyle = bc.bytesToUnsignedChar(self.boxContents[10:11])
        codingBypass = self._getBitValue(codeBlockStyle, 8)
        self.addCharacteristic('codingBypass', codingBypass)
        resetOnBoundaries = self._getBitValue(codeBlockStyle, 7)
        self.addCharacteristic('resetOnBoundaries', resetOnBoundaries)
        termOnEachPass = self._getBitValue(codeBlockStyle, 6)
        self.addCharacteristic('termOnEachPass', termOnEachPass)
        vertCausalContext = self._getBitValue(codeBlockStyle, 5)
        self.addCharacteristic('vertCausalContext', vertCausalContext)
        predTermination = self._getBitValue(codeBlockStyle, 4)
        self.addCharacteristic('predTermination', predTermination)
        segmentationSymbols = self._getBitValue(codeBlockStyle, 3)
        self.addCharacteristic('segmentationSymbols', segmentationSymbols)
        transformation = bc.bytesToUnsignedChar(self.boxContents[11:12])
        self.addCharacteristic('transformation', transformation)
        transformationIsValid = transformation in (0, 1)
        self.testFor('transformationIsValid', transformationIsValid)
        if precincts == 1:
            offset = 12
            for i in range(levels + 1):
                precinctByte = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
                ppx = precinctByte & 15
                precinctSizeX = 2 ** ppx
                self.addCharacteristic('precinctSizeX', precinctSizeX)
                if i != 0:
                    precinctSizeXIsValid = precinctSizeX >= 2
                else:
                    precinctSizeXIsValid = True
                self.testFor('precinctSizeXIsValid', precinctSizeXIsValid)
                ppy = precinctByte >> 4 & 15
                precinctSizeY = 2 ** ppy
                self.addCharacteristic('precinctSizeY', precinctSizeY)
                if i != 0:
                    precinctSizeYIsValid = precinctSizeY >= 2
                else:
                    precinctSizeYIsValid = True
                self.testFor('precinctSizeYIsValid', precinctSizeYIsValid)
                offset += 1

        else:
            for i in range(levels + 1):
                precinctSizeX = 32768
                self.addCharacteristic('precinctSizeX', precinctSizeX)
                precinctSizeY = 32768
                self.addCharacteristic('precinctSizeY', precinctSizeY)

    def validate_coc(self):
        """Coding style component (COC) header fields (ISO/IEC 15444-1 Section A.6.2)."""
        lcoc = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lcoc', lcoc)
        lcocIsValid = 9 <= lcoc <= 43
        self.testFor('lcocIsValid', lcocIsValid)
        if self.csiz < 257:
            ccoc = bc.bytesToUnsignedChar(self.boxContents[2:3])
            ccocIsValid = 0 <= ccoc <= 255
            offset = 3
        else:
            ccoc = bc.bytesToUShortInt(self.boxContents[2:4])
            ccocIsValid = 0 <= ccoc <= 16383
            offset = 4
        self.addCharacteristic('ccoc', ccoc)
        self.testFor('ccocIsValid', ccocIsValid)
        scoc = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
        precincts = self._getBitValue(scoc, 8)
        self.addCharacteristic('precincts', precincts)
        offset += 1
        levels = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
        self.addCharacteristic('levels', levels)
        levelsIsValid = 0 <= levels <= 32
        self.testFor('levelsIsValid', levelsIsValid)
        if precincts == 1 and self.csiz < 257:
            lcocExpected = 10 + levels
        else:
            if precincts == 1 and self.csiz >= 257:
                lcocExpected = 11 + levels
            elif precincts == 0 and self.csiz < 257:
                lcocExpected = 9
            else:
                lcocExpected = 10
            lcocConsistencyCheck = lcoc == lcocExpected
            self.testFor('lcocConsistencyCheck', lcocConsistencyCheck)
            offset += 1
            codeBlockWidthExponent = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1]) + 2
            self.addCharacteristic('codeBlockWidth', 2 ** codeBlockWidthExponent)
            codeBlockWidthExponentIsValid = 2 <= codeBlockWidthExponent <= 10
            self.testFor('codeBlockWidthExponentIsValid', codeBlockWidthExponentIsValid)
            offset += 1
            codeBlockHeightExponent = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1]) + 2
            self.addCharacteristic('codeBlockHeight', 2 ** codeBlockHeightExponent)
            codeBlockHeightExponentIsValid = 2 <= codeBlockHeightExponent <= 10
            self.testFor('codeBlockHeightExponentIsValid', codeBlockHeightExponentIsValid)
            sumHeightWidthExponentIsValid = codeBlockWidthExponent + codeBlockHeightExponent <= 12
            self.testFor('sumHeightWidthExponentIsValid', sumHeightWidthExponentIsValid)
            offset += 1
            codeBlockStyle = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
            codingBypass = self._getBitValue(codeBlockStyle, 8)
            self.addCharacteristic('codingBypass', codingBypass)
            resetOnBoundaries = self._getBitValue(codeBlockStyle, 7)
            self.addCharacteristic('resetOnBoundaries', resetOnBoundaries)
            termOnEachPass = self._getBitValue(codeBlockStyle, 6)
            self.addCharacteristic('termOnEachPass', termOnEachPass)
            vertCausalContext = self._getBitValue(codeBlockStyle, 5)
            self.addCharacteristic('vertCausalContext', vertCausalContext)
            predTermination = self._getBitValue(codeBlockStyle, 4)
            self.addCharacteristic('predTermination', predTermination)
            segmentationSymbols = self._getBitValue(codeBlockStyle, 3)
            self.addCharacteristic('segmentationSymbols', segmentationSymbols)
            offset += 1
            transformation = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
            self.addCharacteristic('transformation', transformation)
            transformationIsValid = transformation in (0, 1)
            self.testFor('transformationIsValid', transformationIsValid)
            if precincts == 1:
                offset += 1
                for i in range(levels + 1):
                    precinctByte = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
                    ppx = precinctByte & 15
                    precinctSizeX = 2 ** ppx
                    self.addCharacteristic('precinctSizeX', precinctSizeX)
                    if i != 0:
                        precinctSizeXIsValid = precinctSizeX >= 2
                    else:
                        precinctSizeXIsValid = True
                    self.testFor('precinctSizeXIsValid', precinctSizeXIsValid)
                    ppy = precinctByte >> 4 & 15
                    precinctSizeY = 2 ** ppy
                    self.addCharacteristic('precinctSizeY', precinctSizeY)
                    if i != 0:
                        precinctSizeYIsValid = precinctSizeY >= 2
                    else:
                        precinctSizeYIsValid = True
                    self.testFor('precinctSizeYIsValid', precinctSizeYIsValid)
                    offset += 1

            else:
                for i in range(levels + 1):
                    precinctSizeX = 32768
                    self.addCharacteristic('precinctSizeX', precinctSizeX)
                    precinctSizeY = 32768
                    self.addCharacteristic('precinctSizeY', precinctSizeY)

    def validate_rgn(self):
        """Region of interest (RGN) header fields (ISO/IEC 15444-1 Section A.6.3)."""
        lrgn = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lrgn', lrgn)
        lrgnIsValid = 5 <= lrgn <= 6
        self.testFor('lrgnIsValid', lrgnIsValid)
        if self.csiz < 257:
            crgn = bc.bytesToUnsignedChar(self.boxContents[2:3])
            crgnIsValid = 0 <= crgn <= 255
            offset = 3
        else:
            crgn = bc.bytesToUShortInt(self.boxContents[2:4])
            crgnIsValid = 0 <= crgn <= 16383
            offset = 4
        self.addCharacteristic('crgn', crgn)
        self.testFor('crgnIsValid', crgnIsValid)
        roiStyle = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
        self.addCharacteristic('roiStyle', roiStyle)
        roiStyleIsValid = roiStyle == 0
        self.testFor('roiStyleIsValid', roiStyleIsValid)
        offset += 1
        roiShift = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
        self.addCharacteristic('roiShift', roiShift)
        roiShiftIsValid = 0 <= roiShift <= 255
        self.testFor('roiShiftIsValid', roiShiftIsValid)

    def validate_qcd(self):
        """Quantization default (QCD) header fields (ISO/IEC 15444-1 Section A.6.4)."""
        lqcd = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lqcd', lqcd)
        lqcdIsValid = 4 <= lqcd <= 197
        self.testFor('lqcdIsValid', lqcdIsValid)
        sqcd = bc.bytesToUnsignedChar(self.boxContents[2:3])
        qStyle = sqcd & 31
        self.addCharacteristic('qStyle', qStyle)
        qStyleIsValid = qStyle in (0, 1, 2)
        self.testFor('qStyleIsValid', qStyleIsValid)
        guardBits = sqcd >> 5 & 7
        self.addCharacteristic('guardBits', guardBits)
        if qStyle == 0:
            levels = int((lqcd - 4) / 3)
        elif qStyle == 2:
            levels = int((lqcd - 5) / 6)
        offset = 3
        if qStyle == 0:
            for _ in range(levels):
                spqcd = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
                epsilon = spqcd >> 3 & 31
                self.addCharacteristic('epsilon', epsilon)
                offset += 1

        elif qStyle == 1:
            spqcd = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
            mu = spqcd & 2047
            self.addCharacteristic('mu', mu)
            epsilon = spqcd >> 11 & 31
            self.addCharacteristic('epsilon', epsilon)
        elif qStyle == 2:
            for _ in range(levels):
                spqcd = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
                mu = spqcd & 2047
                self.addCharacteristic('mu', mu)
                epsilon = spqcd >> 11 & 31
                self.addCharacteristic('epsilon', epsilon)
                offset += 2

    def validate_qcc(self):
        """Quantization component (QCD) header fields (ISO/IEC 15444-1 Section A.6.5)."""
        lqcc = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lqcc', lqcc)
        lqccIsValid = 5 <= lqcc <= 199
        self.testFor('lqccIsValid', lqccIsValid)
        if self.csiz < 257:
            cqcc = bc.bytesToUnsignedChar(self.boxContents[2:3])
            offset = 3
        else:
            cqcc = bc.bytesToUShortInt(self.boxContents[2:4])
            offset = 4
        self.addCharacteristic('cqcc', cqcc)
        sqcc = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
        qStyle = sqcc & 31
        self.addCharacteristic('qStyle', qStyle)
        qStyleIsValid = qStyle in (0, 1, 2)
        self.testFor('qStyleIsValid', qStyleIsValid)
        guardBits = sqcc >> 5 & 7
        self.addCharacteristic('guardBits', guardBits)
        if qStyle == 0 and self.csiz < 257:
            levels = int((lqcc - 4) / 3)
        elif qStyle == 2:
            levels = int((lqcc - 5) / 6)
        if qStyle == 0 and self.csiz < 257:
            levels = int((lqcc - 5) / 3)
        elif qStyle == 2 and self.csiz < 257:
            levels = int((lqcc - 6) / 6)
        elif qStyle == 0 and self.csiz >= 257:
            levels = int((lqcc - 6) / 3)
        elif qStyle == 2 and self.csiz >= 257:
            levels = int((lqcc - 7) / 6)
        if qStyle == 0:
            for _ in range(levels):
                spqcc = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
                epsilon = spqcc >> 3 & 31
                self.addCharacteristic('epsilon', epsilon)
                offset += 1

        elif qStyle == 1:
            spqcc = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
            mu = spqcc & 2047
            self.addCharacteristic('mu', mu)
            epsilon = spqcc >> 11 & 31
            self.addCharacteristic('epsilon', epsilon)
        elif qStyle == 2:
            for _ in range(levels):
                spqcc = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
                mu = spqcc & 2047
                self.addCharacteristic('mu', mu)
                epsilon = spqcc >> 11 & 31
                self.addCharacteristic('epsilon', epsilon)
                offset += 2

    def validate_poc(self):
        """Progression order change (POC) header fields (ISO/IEC 15444-1 Section A.6.6)."""
        lpoc = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lpoc', lpoc)
        lpocIsValid = 9 <= lpoc <= 65535
        self.testFor('lpocIsValid', lpocIsValid)
        if self.csiz < 257:
            progOrderChanges = int((lpoc - 2) / 7)
        else:
            progOrderChanges = int((lpoc - 2) / 9)
        offset = 2
        for _ in range(progOrderChanges):
            rspoc = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
            self.addCharacteristic('rspoc', rspoc)
            rspocIsValid = 0 <= rspoc <= 32
            self.testFor('rspocIsValid', rspocIsValid)
            offset += 1
            if self.csiz < 257:
                cspoc = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
                cspocIsValid = 0 <= cspoc <= 255
                offset += 1
            else:
                cspoc = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
                cspocIsValid = 0 <= cspoc <= 16383
                offset += 2
            self.addCharacteristic('cspoc', cspoc)
            self.testFor('cspocIsValid', cspocIsValid)
            lyepoc = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
            self.addCharacteristic('lyepoc', lyepoc)
            lyepocIsValid = 1 <= lyepoc <= 65535
            self.testFor('lyepocIsValid', lyepocIsValid)
            offset += 2
            repoc = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
            self.addCharacteristic('repoc', repoc)
            repocIsValid = rspoc + 1 <= repoc <= 33
            self.testFor('repocIsValid', repocIsValid)
            offset += 1
            if self.csiz < 257:
                cepoc = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
                cepocIsValid = cspoc + 1 <= cepoc <= 255 or cepoc == 0
                offset += 1
            else:
                cepoc = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
                cepocIsValid = cspoc + 1 <= cepoc <= 16384 or cepoc == 0
                offset += 2
            self.addCharacteristic('cepoc', cepoc)
            self.testFor('cepocIsValid', cepocIsValid)
            order = bc.bytesToUnsignedChar(self.boxContents[offset:offset + 1])
            self.addCharacteristic('order', order)
            orderIsValid = order in (0, 1, 2, 3, 4)
            self.testFor('orderIsValid', orderIsValid)
            offset += 1

    def validate_crg(self):
        """Component registration (CRG) marker (ISO/IEC 15444-1 Section A.9.1)."""
        lcrg = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lcrg', lcrg)
        lcrgIsValid = 6 <= lcrg <= 65534
        self.testFor('lcrgIsValid', lcrgIsValid)
        offset = 2
        for _ in range(self.csiz):
            xcrg = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
            self.addCharacteristic('xcrg', xcrg)
            xcrgIsValid = 0 <= xcrg <= 65535
            self.testFor('xcrgIsValid', xcrgIsValid)
            offset += 2
            ycrg = bc.bytesToUShortInt(self.boxContents[offset:offset + 2])
            self.addCharacteristic('ycrg', ycrg)
            ycrgIsValid = 0 <= ycrg <= 65535
            self.testFor('ycrgIsValid', ycrgIsValid)
            offset += 2

    def validate_com(self):
        """Codestream comment (COM) (ISO/IEC 15444-1 Section A.9.2)."""
        lcom = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lcom', lcom)
        lcomIsValid = 5 <= lcom <= 65535
        self.testFor('lcomIsValid', lcomIsValid)
        rcom = bc.bytesToUShortInt(self.boxContents[2:4])
        self.addCharacteristic('rcom', rcom)
        rcomIsValid = 0 <= rcom <= 1
        self.testFor('rcomIsValid', rcomIsValid)
        comment = self.boxContents[4:lcom]
        if rcom == 0:
            commentIsValid = True
            comment = bc.bytesToHex(comment)
        elif rcom == 1:
            try:
                comment = comment.decode('iso-8859-15', 'strict')
            except UnicodeError:
                comment = ''

            if bc.removeControlCharacters(comment) == comment:
                commentIsValid = True
            else:
                commentIsValid = False
        else:
            commentIsValid = False
        self.testFor('commentIsValid', commentIsValid)
        if commentIsValid:
            self.addCharacteristic('comment', comment)

    def validate_sot(self):
        """Start of tile-part (SOT) marker segment (ISO/IEC 15444-1 Section A.4.2)."""
        lsot = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('lsot', lsot)
        lsotIsValid = lsot == 10
        self.testFor('lsotIsValid', lsotIsValid)
        isot = bc.bytesToUShortInt(self.boxContents[2:4])
        self.addCharacteristic('isot', isot)
        isotIsValid = 0 <= isot <= 65534
        self.testFor('isotIsValid', isotIsValid)
        psot = bc.bytesToUInt(self.boxContents[4:8])
        self.addCharacteristic('psot', psot)
        psotIsValid = not 1 <= psot <= 13
        self.testFor('psotIsValid', psotIsValid)
        tpsot = bc.bytesToUnsignedChar(self.boxContents[8:9])
        self.addCharacteristic('tpsot', tpsot)
        tpsotIsValid = 0 <= tpsot <= 254
        self.testFor('tpsotIsValid', tpsotIsValid)
        tnsot = bc.bytesToUnsignedChar(self.boxContents[9:10])
        self.addCharacteristic('tnsot', tnsot)
        self.tilePartLength = psot

    def validate_tlm(self):
        """Empty function."""
        pass

    def validate_plm(self):
        """Empty function."""
        pass

    def validate_plt(self):
        """Empty function."""
        pass

    def validate_ppm(self):
        """Empty function."""
        pass

    def validate_ppt(self):
        """Empty function."""
        pass

    def validate_tilePart(self):
        """Analyse tile part that starts at offsetStart and perform cursory validation.

        Precondition: offsetStart points to SOT marker

        Limitations:

         - COD, COC, QCD, QCC and RGN are markers only allowed in first tile-part
           of a tile; there is currently no check on this (may be added later)
        """
        offset = self.startOffset
        marker, _, segContents, offsetNext = self._getMarkerSegment(offset)
        resultsSOT = BoxValidator('startOfTile', segContents).validate()
        testsSOT = resultsSOT.tests
        characteristicsSOT = resultsSOT.characteristics
        tilePartLength = resultsSOT.tilePartLength
        self.tests.appendIfNotEmpty(testsSOT)
        self.characteristics.append(characteristicsSOT)
        offset = offsetNext
        while marker != b'\xff\x93' and offsetNext != -9999:
            marker, _, segContents, offsetNext = self._getMarkerSegment(offset)
            if marker == b'\xffR':
                resultsCOD = BoxValidator(marker, segContents).validate()
                testsCOD = resultsCOD.tests
                characteristicsCOD = resultsCOD.characteristics
                self.tests.appendIfNotEmpty(testsCOD)
                self.characteristics.append(characteristicsCOD)
                offset = offsetNext
            elif marker == b'\xffS':
                resultsCOC = BoxValidator(marker, segContents, components=self.csiz).validate()
                testsCOC = resultsCOC.tests
                characteristicsCOC = resultsCOC.characteristics
                self.tests.appendIfNotEmpty(testsCOC)
                self.characteristics.append(characteristicsCOC)
                offset = offsetNext
            elif marker == b'\xff\\':
                resultsQCD = BoxValidator(marker, segContents).validate()
                testsQCD = resultsQCD.tests
                characteristicsQCD = resultsQCD.characteristics
                self.tests.appendIfNotEmpty(testsQCD)
                self.characteristics.append(characteristicsQCD)
                offset = offsetNext
            elif marker == b'\xff]':
                resultsQCC = BoxValidator(marker, segContents, components=self.csiz).validate()
                testsQCC = resultsQCC.tests
                characteristicsQCC = resultsQCC.characteristics
                self.tests.appendIfNotEmpty(testsQCC)
                self.characteristics.append(characteristicsQCC)
                offset = offsetNext
            elif marker == b'\xff^':
                resultsRGN = BoxValidator(marker, segContents, components=self.csiz).validate()
                testsRGN = resultsRGN.tests
                characteristicsRGN = resultsRGN.characteristics
                self.tests.appendIfNotEmpty(testsRGN)
                self.characteristics.append(characteristicsRGN)
                offset = offsetNext
            elif marker == b'\xff_':
                resultsPOC = BoxValidator(marker, segContents, components=self.csiz).validate()
                testsPOC = resultsPOC.tests
                characteristicsPOC = resultsPOC.characteristics
                self.tests.appendIfNotEmpty(testsPOC)
                self.characteristics.append(characteristicsPOC)
                offset = offsetNext
            elif marker == b'\xffd':
                resultsCOM = BoxValidator(marker, segContents).validate()
                testsCOM = resultsCOM.tests
                characteristicsCOM = resultsCOM.characteristics
                self.tests.appendIfNotEmpty(testsCOM)
                self.characteristics.append(characteristicsCOM)
                offset = offsetNext
            elif marker in (b'\xffa', b'\xffX'):
                resultsOther = BoxValidator(marker, segContents).validate()
                testsOther = resultsOther.tests
                characteristicsOther = resultsOther.characteristics
                self.tests.appendIfNotEmpty(testsOther)
                self.characteristics.append(characteristicsOther)
                offset = offsetNext
            else:
                offset = offsetNext

        self.testFor('foundSODMarker', marker == b'\xff\x93')
        offsetNextTilePart = self.startOffset + tilePartLength
        if tilePartLength != 0:
            markerNextTilePart = self.boxContents[offsetNextTilePart:offsetNextTilePart + 2]
            foundNextTilePartOrEOC = markerNextTilePart in (b'\xff\x90', b'\xff\xd9')
            self.testFor('foundNextTilePartOrEOC', foundNextTilePartOrEOC)
        self.returnOffset = offsetNextTilePart

    def validate_xmlBox(self):
        """XML Box (ISO/IEC 15444-1 Section I.7.1)."""
        data = self.boxContents
        try:
            dataAsElement = ET.fromstring(data)
            self.characteristics.append(dataAsElement)
            containsWellformedXML = True
        except Exception:
            containsWellformedXML = False
            if config.EXTRACT_NULL_TERMINATED_XML_FLAG:
                try:
                    data = bc.removeNullTerminator(data)
                    dataAsElement = ET.fromstring(data)
                    self.characteristics.append(dataAsElement)
                except Exception:
                    pass

        self.testFor('containsWellformedXML', containsWellformedXML)

    def validate_uuidBox(self):
        """UUID Box (ISO/IEC 15444-1 Section I.7.2).

        For details on UUIDs see: http://tools.ietf.org/html/rfc4122.html

        Box contains 16-byte identifier, followed by block of data.
        Format of data is defined outside of the scope of JPEG 2000,
        so in most cases there's not much to validate here. Exception:
        if uuid = be7acfcb-97a9-42e8-9c71-999491e3afac this indicates
        presence of XMP metadata.
        """
        boxLength = len(self.boxContents)
        self.testFor('boxLengthIsValid', boxLength > 16)
        boxUUID = str(uuid.UUID(bytes=self.boxContents[0:16]))
        if boxUUID == 'be7acfcb-97a9-42e8-9c71-999491e3afac':
            data = self.boxContents[16:boxLength]
            try:
                dataAsElement = ET.fromstring(data)
                self.characteristics.append(dataAsElement)
                containsWellformedXML = True
            except:
                containsWellformedXML = False
                if config.EXTRACT_NULL_TERMINATED_XML_FLAG:
                    try:
                        data = bc.removeNullTerminator(data)
                        dataAsElement = ET.fromstring(data)
                        self.characteristics.append(dataAsElement)
                    except:
                        pass

            self.testFor('containsWellformedXML', containsWellformedXML)
        else:
            self.addCharacteristic('uuid', boxUUID)

    def validate_uuidInfoBox(self):
        """UUID Info box (superbox)(ISO/IEC 15444-1 Section I.7.3).

        Provides additional information on vendor-specific UUIDs.
        """
        tagListBox = 'ulst'
        tagURLBox = 'url '
        subBoxTypes = []
        noBytes = len(self.boxContents)
        byteStart = 0
        boxLengthValue = 10
        while byteStart < noBytes and boxLengthValue not in (0, -9999):
            boxLengthValue, boxType, byteEnd, subBoxContents = self._getBox(byteStart, noBytes)
            resultsBox = BoxValidator(boxType, subBoxContents).validate()
            testsBox = resultsBox.tests
            characteristicsBox = resultsBox.characteristics
            byteStart = byteEnd
            subBoxTypes.append(boxType)
            self.tests.appendIfNotEmpty(testsBox)
            self.characteristics.append(characteristicsBox)

        self.testFor('containsOneListBox', subBoxTypes.count(tagListBox) == 1)
        self.testFor('containsOneURLBox', subBoxTypes.count(tagURLBox) == 1)

    def validate_uuidListBox(self):
        """UUID List box (ISO/IEC 15444-1 Section I.7.3.1).

        Contains a list of UUIDs.
        """
        nU = bc.bytesToUShortInt(self.boxContents[0:2])
        self.addCharacteristic('nU', nU)
        self.testFor('boxLengthIsValid', len(self.boxContents) == nU * 16 + 2)
        offset = 2
        for _ in range(nU):
            boxUUID = str(uuid.UUID(bytes=self.boxContents[offset:offset + 16]))
            self.addCharacteristic('uuid', boxUUID)
            offset += 16

    def validate_urlBox(self):
        """Data Entry URL box (ISO/IEC 15444-1 Section I.7.3.2).

        Contains URL that can be used to obtain more information
        about UUIDs in UUID List box.
        """
        version = bc.bytesToUnsignedChar(self.boxContents[0:1])
        self.addCharacteristic('version', version)
        self.testFor('versionIsValid', version == 0)
        flag = self.boxContents[1:4]
        self.testFor('flagIsValid', flag == '\x00\x00\x00')
        loc = self.boxContents[4:len(self.boxContents)]
        self.testFor('locHasNullTerminator', loc.endswith('\x00'))
        loc = bc.removeNullTerminator(loc)
        try:
            loc.decode('utf-8', 'strict')
            self.testFor('locIsUTF8', True)
        except UnicodeDecodeError:
            self.testFor('locIsUTF8', False)

        self.addCharacteristic('loc', loc)

    def validate_JP2(self):
        """Top-level function for JP2 validation.

        1. Parses all top-level boxes in JP2 byte object, and calls separate validator
           function for each of these
        2. Checks for presence of all required top-level boxes
        3. Checks if JP2 header properties are consistent with corresponding properties
           in codestream header
        """
        tagSignatureBox = 'jP  '
        tagFileTypeBox = 'ftyp'
        tagJP2HeaderBox = 'jp2h'
        tagIntellectualPropertyBox = 'jp2i'
        tagContiguousCodestreamBox = 'jp2c'
        boxTypes = []
        noBytes = len(self.boxContents)
        byteStart = 0
        boxLengthValue = 10
        while byteStart < noBytes and boxLengthValue not in (0, -9999):
            boxLengthValue, boxType, byteEnd, boxContents = self._getBox(byteStart, noBytes)
            resultsBox = BoxValidator(boxType, boxContents).validate()
            testsBox = resultsBox.tests
            characteristicsBox = resultsBox.characteristics
            byteStart = byteEnd
            boxTypes.append(boxType)
            self.tests.appendIfNotEmpty(testsBox)
            self.characteristics.append(characteristicsBox)

        containsSignatureBox = tagSignatureBox in boxTypes
        containsFileTypeBox = tagFileTypeBox in boxTypes
        containsJP2HeaderBox = tagJP2HeaderBox in boxTypes
        containsContiguousCodestreamBox = tagContiguousCodestreamBox in boxTypes
        self.testFor('containsSignatureBox', containsSignatureBox)
        self.testFor('containsFileTypeBox', containsFileTypeBox)
        self.testFor('containsJP2HeaderBox', containsJP2HeaderBox)
        self.testFor('containsContiguousCodestreamBox', containsContiguousCodestreamBox)
        iPR = self.characteristics.findElementText('jp2HeaderBox/imageHeaderBox/iPR')
        if iPR == 1:
            containsIntellectualPropertyBox = tagIntellectualPropertyBox in boxTypes
            self.testFor('containsIntellectualPropertyBox', containsIntellectualPropertyBox)
        try:
            firstBoxIsSignatureBox = boxTypes[0] == tagSignatureBox
        except Exception:
            firstBoxIsSignatureBox = False

        try:
            secondBoxIsFileTypeBox = boxTypes[1] == tagFileTypeBox
        except Exception:
            secondBoxIsFileTypeBox = False

        try:
            positionJP2HeaderBox = boxTypes.index(tagJP2HeaderBox)
            positionFirstContiguousCodestreamBox = boxTypes.index(tagContiguousCodestreamBox)
            if positionFirstContiguousCodestreamBox > positionJP2HeaderBox > 1:
                locationJP2HeaderBoxIsValid = True
            else:
                locationJP2HeaderBoxIsValid = False
        except Exception:
            locationJP2HeaderBoxIsValid = False

        self.testFor('firstBoxIsSignatureBox', firstBoxIsSignatureBox)
        self.testFor('secondBoxIsFileTypeBox', secondBoxIsFileTypeBox)
        self.testFor('locationJP2HeaderBoxIsValid', locationJP2HeaderBoxIsValid)
        noMoreThanOneSignatureBox = boxTypes.count(tagSignatureBox) <= 1
        noMoreThanOneFileTypeBox = boxTypes.count(tagFileTypeBox) <= 1
        noMoreThanOneJP2HeaderBox = boxTypes.count(tagJP2HeaderBox) <= 1
        self.testFor('noMoreThanOneSignatureBox', noMoreThanOneSignatureBox)
        self.testFor('noMoreThanOneFileTypeBox', noMoreThanOneFileTypeBox)
        self.testFor('noMoreThanOneJP2HeaderBox', noMoreThanOneJP2HeaderBox)
        jp2ImageHeader = self.characteristics.find('jp2HeaderBox/imageHeaderBox')
        sizHeader = self.characteristics.find('contiguousCodestreamBox/siz')
        if jp2ImageHeader is not None and sizHeader is not None:
            height = jp2ImageHeader.findElementText('height')
            ysiz = sizHeader.findElementText('ysiz')
            yOsiz = sizHeader.findElementText('yOsiz')
            heightConsistentWithSIZ = height == ysiz - yOsiz
            self.testFor('heightConsistentWithSIZ', heightConsistentWithSIZ)
            width = jp2ImageHeader.findElementText('width')
            xsiz = sizHeader.findElementText('xsiz')
            xOsiz = sizHeader.findElementText('xOsiz')
            widthConsistentWithSIZ = width == xsiz - xOsiz
            self.testFor('widthConsistentWithSIZ', widthConsistentWithSIZ)
            nC = jp2ImageHeader.findElementText('nC')
            csiz = sizHeader.findElementText('csiz')
            nCConsistentWithSIZ = nC == csiz
            self.testFor('nCConsistentWithSIZ', nCConsistentWithSIZ)
            bPCSign = jp2ImageHeader.findElementText('bPCSign')
            bPCDepth = jp2ImageHeader.findElementText('bPCDepth')
            if bPCSign == 1 and bPCDepth == 128:
                bpcBox = self.characteristics.find('jp2HeaderBox/bitsPerComponentBox')
                bPCSignValues = bpcBox.findAllText('bPCSign')
                bPCDepthValues = bpcBox.findAllText('bPCDepth')
            else:
                bPCSignValues = []
                for _ in range(nC):
                    bPCSignValues.append(bPCSign)

                bPCDepthValues = []
                for _ in range(nC):
                    bPCDepthValues.append(bPCDepth)

            ssizSignValues = sizHeader.findAllText('ssizSign')
            ssizDepthValues = sizHeader.findAllText('ssizDepth')
            bPCSignConsistentWithSIZ = bPCSignValues == ssizSignValues
            self.testFor('bPCSignConsistentWithSIZ', bPCSignConsistentWithSIZ)
            bPCDepthConsistentWithSIZ = bPCDepthValues == ssizDepthValues
            self.testFor('bPCDepthConsistentWithSIZ', bPCDepthConsistentWithSIZ)
            compressionRatio = self._calculateCompressionRatio(noBytes, bPCDepthValues, height, width)
            compressionRatio = round(compressionRatio, 2)
            self.addCharacteristic('compressionRatio', compressionRatio)
        self.isValid = self._isValid()
        return