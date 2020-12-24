# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/TiffIO.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 48431 bytes
__author__ = 'V.A. Sole - ESRF Data Analysis'
__contact__ = 'sole@esrf.fr'
__license__ = 'MIT'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
__date__ = '29/10/2018'
import sys, os, struct, numpy, logging
from fabio.third_party import six
ALLOW_MULTIPLE_STRIPS = False
TAG_ID = {256: 'NumberOfColumns', 
 257: 'NumberOfRows', 
 258: 'BitsPerSample', 
 259: 'Compression', 
 262: 'PhotometricInterpretation', 
 270: 'ImageDescription', 
 272: 'Model', 
 273: 'StripOffsets', 
 277: 'SamplesPerPixel', 
 278: 'RowsPerStrip', 
 279: 'StripByteCounts', 
 305: 'Software', 
 306: 'Date', 
 320: 'Colormap', 
 339: 'SampleFormat'}
TAG_NUMBER_OF_COLUMNS = 256
TAG_NUMBER_OF_ROWS = 257
TAG_BITS_PER_SAMPLE = 258
TAG_PHOTOMETRIC_INTERPRETATION = 262
TAG_COMPRESSION = 259
TAG_IMAGE_DESCRIPTION = 270
TAG_MODEL = 272
TAG_STRIP_OFFSETS = 273
TAG_SAMPLES_PER_PIXEL = 277
TAG_ROWS_PER_STRIP = 278
TAG_STRIP_BYTE_COUNTS = 279
TAG_SOFTWARE = 305
TAG_DATE = 306
TAG_COLORMAP = 320
TAG_SAMPLE_FORMAT = 339
FIELD_TYPE = {1: ('BYTE', 'B'), 
 2: ('ASCII', 's'), 
 3: ('SHORT', 'H'), 
 4: ('LONG', 'I'), 
 5: ('RATIONAL', 'II'), 
 6: ('SBYTE', 'b'), 
 7: ('UNDEFINED', 'B'), 
 8: ('SSHORT', 'h'), 
 9: ('SLONG', 'i'), 
 10: ('SRATIONAL', 'ii'), 
 11: ('FLOAT', 'f'), 
 12: ('DOUBLE', 'd')}
FIELD_TYPE_OUT = {'B': 1, 
 's': 2, 
 'H': 3, 
 'I': 4, 
 'II': 5, 
 'b': 6, 
 'h': 8, 
 'i': 9, 
 'ii': 10, 
 'f': 11, 
 'd': 12}
SAMPLE_FORMAT_UINT = 1
SAMPLE_FORMAT_INT = 2
SAMPLE_FORMAT_FLOAT = 3
SAMPLE_FORMAT_VOID = 4
SAMPLE_FORMAT_COMPLEXINT = 5
SAMPLE_FORMAT_COMPLEXIEEEFP = 6
logger = logging.getLogger(__name__)

class TiffIO(object):

    def __init__(self, filename, mode=None, cache_length=20, mono_output=False):
        if mode is None:
            mode = 'rb'
        if 'b' not in mode:
            mode = mode + 'b'
        if 'a' in mode.lower():
            raise IOError("Mode %s makes no sense on TIFF files. Consider 'rb+'" % mode)
        if 'w' in mode and '+' not in mode:
            mode += '+'
        if hasattr(filename, 'seek') and hasattr(filename, 'read'):
            fd = filename
            self._access = None
        else:
            fd = open(filename, mode)
            self._access = mode
        self._initInternalVariables(fd)
        self._maxImageCacheLength = cache_length
        self._forceMonoOutput = mono_output

    def __enter__(self):
        return self

    def __exit__(self, *arg):
        self.close()

    def _initInternalVariables(self, fd=None):
        if fd is None:
            fd = self.fd
        else:
            self.fd = fd
        fd.seek(0)
        order = fd.read(2).decode()
        if len(order):
            if order == 'II':
                fileOrder = 'little'
                self._structChar = '<'
            else:
                if order == 'MM':
                    fileOrder = 'big'
                    self._structChar = '>'
                else:
                    raise IOError('File is not a Mar CCD file, nor a TIFF file')
                a = fd.read(2)
                fortyTwo = struct.unpack(self._structChar + 'H', a)[0]
                if fortyTwo != 42:
                    raise IOError('Invalid TIFF version %d' % fortyTwo)
                else:
                    logger.debug('VALID TIFF VERSION')
            if sys.byteorder != fileOrder:
                swap = True
            else:
                swap = False
        else:
            if sys.byteorder == 'little':
                self._structChar = '<'
            else:
                self._structChar = '>'
            swap = False
        self._swap = swap
        self._IFD = []
        self._imageDataCacheIndex = []
        self._imageDataCache = []
        self._imageInfoCacheIndex = []
        self._imageInfoCache = []
        self.getImageFileDirectories(fd)

    def __makeSureFileIsOpen(self):
        if not self.fd.closed:
            return
        logger.debug('Reopening closed file')
        fileName = self.fd.name
        if self._access is None:
            newFile = open(fileName, 'rb')
        else:
            newFile = open(fileName, self._access)
        self.fd = newFile

    def __makeSureFileIsClosed(self):
        if self._access is None:
            logger.debug('Not closing not owned file')
            return
        if not self.fd.closed:
            self.fd.close()

    def close(self):
        return self._TiffIO__makeSureFileIsClosed()

    def getNumberOfImages(self):
        self._updateIFD()
        return len(self._IFD)

    def _updateIFD(self):
        self._TiffIO__makeSureFileIsOpen()
        self.getImageFileDirectories()
        self._TiffIO__makeSureFileIsClosed()

    def getImageFileDirectories(self, fd=None):
        if fd is None:
            fd = self.fd
        else:
            self.fd = fd
        st = self._structChar
        fd.seek(4)
        self._IFD = []
        nImages = 0
        fmt = st + 'I'
        inStr = fd.read(struct.calcsize(fmt))
        if not len(inStr):
            offsetToIFD = 0
        else:
            offsetToIFD = struct.unpack(fmt, inStr)[0]
        logger.debug('Offset to first IFD = %d', offsetToIFD)
        while offsetToIFD != 0:
            self._IFD.append(offsetToIFD)
            nImages += 1
            fd.seek(offsetToIFD)
            fmt = st + 'H'
            numberOfDirectoryEntries = struct.unpack(fmt, fd.read(struct.calcsize(fmt)))[0]
            logger.debug('Number of directory entries = %d', numberOfDirectoryEntries)
            fmt = st + 'I'
            fd.seek(offsetToIFD + 2 + 12 * numberOfDirectoryEntries)
            offsetToIFD = struct.unpack(fmt, fd.read(struct.calcsize(fmt)))[0]
            logger.debug('Next Offset to IFD = %d', offsetToIFD)

        logger.debug('Number of images found = %d', nImages)
        return nImages

    def _parseImageFileDirectory(self, nImage):
        offsetToIFD = self._IFD[nImage]
        st = self._structChar
        fd = self.fd
        fd.seek(offsetToIFD)
        fmt = st + 'H'
        numberOfDirectoryEntries = struct.unpack(fmt, fd.read(struct.calcsize(fmt)))[0]
        logger.debug('Number of directory entries = %d', numberOfDirectoryEntries)
        fmt = st + 'HHI4s'
        tagIDList = []
        fieldTypeList = []
        nValuesList = []
        valueOffsetList = []
        for _ in range(numberOfDirectoryEntries):
            tagID, fieldType, nValues, valueOffset = struct.unpack(fmt, fd.read(12))
            tagIDList.append(tagID)
            fieldTypeList.append(fieldType)
            nValuesList.append(nValues)
            if nValues == 1:
                ftype, vfmt = FIELD_TYPE[fieldType]
                if ftype not in ('ASCII', 'RATIONAL', 'SRATIONAL'):
                    vfmt = st + vfmt
                    data = valueOffset[0:struct.calcsize(vfmt)]
                    if struct.calcsize(vfmt) > len(data):
                        logger.warning("Data at tag id '%s' is smaller than expected", tagID)
                        data = data + b'\x00' * (struct.calcsize(vfmt) - len(data))
                    actualValue = struct.unpack(vfmt, data)[0]
                    valueOffsetList.append(actualValue)
                else:
                    valueOffsetList.append(valueOffset)
            else:
                if nValues < 5 and fieldType == 2:
                    ftype, vfmt = FIELD_TYPE[fieldType]
                    vfmt = st + '%d%s' % (nValues, vfmt)
                    actualValue = struct.unpack(vfmt, valueOffset[0:struct.calcsize(vfmt)])[0]
                    valueOffsetList.append(actualValue)
                else:
                    valueOffsetList.append(valueOffset)
            if logger.getEffectiveLevel() == logging.DEBUG:
                if tagID in TAG_ID:
                    logger.debug('tagID = %s', TAG_ID[tagID])
                else:
                    logger.debug('tagID        = %d', tagID)
                logger.debug('fieldType    = %s', FIELD_TYPE[fieldType][0])
                logger.debug('nValues      = %d', nValues)

        return (tagIDList, fieldTypeList, nValuesList, valueOffsetList)

    def _readIFDEntry(self, tag, tagIDList, fieldTypeList, nValuesList, valueOffsetList):
        fd = self.fd
        st = self._structChar
        idx = tagIDList.index(tag)
        nValues = nValuesList[idx]
        output = []
        _ftype, vfmt = FIELD_TYPE[fieldTypeList[idx]]
        vfmt = st + '%d%s' % (nValues, vfmt)
        requestedBytes = struct.calcsize(vfmt)
        if nValues == 1:
            output.append(valueOffsetList[idx])
        else:
            if requestedBytes < 5:
                output.append(valueOffsetList[idx])
            else:
                fd.seek(struct.unpack(st + 'I', valueOffsetList[idx])[0])
                output = struct.unpack(vfmt, fd.read(requestedBytes))
            if fieldTypeList[idx] == 2:
                cleaned_output = []
                for raw in output:
                    index = raw.find(b'\x00')
                    if index != -1:
                        raw = raw[0:index]
                    try:
                        text = raw.decode('utf-8')
                    except UnicodeDecodeError:
                        logger.warning('TIFF file tag %d contains non ASCII/UTF-8 characters. ', tag)
                        text = raw.decode('utf-8', errors='replace')
                        text = text.replace('�', '?')

                    cleaned_output.append(text)

                if isinstance(output, tuple):
                    output = tuple(cleaned_output)
            else:
                output = cleaned_output
        return output

    def getData(self, nImage, **kw):
        if nImage >= len(self._IFD):
            self._updateIFD()
        return self._readImage(nImage, **kw)

    def getImage(self, nImage):
        return self.getData(nImage)

    def getInfo(self, nImage, **kw):
        if nImage >= len(self._IFD):
            self._updateIFD()
        return self._readInfo(nImage)

    def _readInfo(self, nImage, close=True):
        if nImage in self._imageInfoCacheIndex:
            logger.debug('Reading info from cache')
            return self._imageInfoCache[self._imageInfoCacheIndex.index(nImage)]
        self._TiffIO__makeSureFileIsOpen()
        tagIDList, fieldTypeList, nValuesList, valueOffsetList = self._parseImageFileDirectory(nImage)
        nColumns = valueOffsetList[tagIDList.index(TAG_NUMBER_OF_COLUMNS)]
        nRows = valueOffsetList[tagIDList.index(TAG_NUMBER_OF_ROWS)]
        idx = tagIDList.index(TAG_BITS_PER_SAMPLE)
        nBits = valueOffsetList[idx]
        if nValuesList[idx] != 1:
            nBits = self._readIFDEntry(TAG_BITS_PER_SAMPLE, tagIDList, fieldTypeList, nValuesList, valueOffsetList)
        if TAG_COLORMAP in tagIDList:
            idx = tagIDList.index(TAG_COLORMAP)
            tmpColormap = self._readIFDEntry(TAG_COLORMAP, tagIDList, fieldTypeList, nValuesList, valueOffsetList)
            if max(tmpColormap) > 255:
                tmpColormap = numpy.array(tmpColormap, dtype=numpy.uint16)
                tmpColormap = (tmpColormap / 256.0).astype(numpy.uint8)
            else:
                tmpColormap = numpy.array(tmpColormap, dtype=numpy.uint8)
            tmpColormap.shape = (3, -1)
            colormap = numpy.zeros((tmpColormap.shape[(-1)], 3), tmpColormap.dtype)
            colormap[:, :] = tmpColormap.T
            tmpColormap = None
        else:
            colormap = None
        if TAG_SAMPLE_FORMAT in tagIDList:
            sampleFormat = valueOffsetList[tagIDList.index(TAG_SAMPLE_FORMAT)]
        else:
            sampleFormat = SAMPLE_FORMAT_VOID
        compression = False
        compression_type = 1
        if TAG_COMPRESSION in tagIDList:
            compression_type = valueOffsetList[tagIDList.index(TAG_COMPRESSION)]
            if compression_type == 1:
                compression = False
            else:
                compression = True
            interpretation = 1
            if TAG_PHOTOMETRIC_INTERPRETATION in tagIDList:
                interpretation = valueOffsetList[tagIDList.index(TAG_PHOTOMETRIC_INTERPRETATION)]
            else:
                logger.debug('WARNING: Non standard TIFF. Photometric interpretation TAG missing')
            helpString = ''
            if TAG_IMAGE_DESCRIPTION in tagIDList:
                imageDescription = self._readIFDEntry(TAG_IMAGE_DESCRIPTION, tagIDList, fieldTypeList, nValuesList, valueOffsetList)
                if type(imageDescription) in [type([1]), type((1, ))]:
                    imageDescription = helpString.join(imageDescription)
            else:
                imageDescription = '%d/%d' % (nImage + 1, len(self._IFD))
            if TAG_MODEL in tagIDList:
                model = self._readIFDEntry(TAG_MODEL, tagIDList, fieldTypeList, nValuesList, valueOffsetList)
            else:
                model = None
            defaultSoftware = 'Unknown Software'
            if TAG_SOFTWARE in tagIDList:
                software = self._readIFDEntry(TAG_SOFTWARE, tagIDList, fieldTypeList, nValuesList, valueOffsetList)
                if isinstance(software, (tuple, list)):
                    software = helpString.join(software)
            else:
                software = defaultSoftware
            if software == defaultSoftware:
                try:
                    if imageDescription.upper().startswith('IMAGEJ'):
                        software = imageDescription.split('=')[0]
                except Exception:
                    pass

                if TAG_DATE in tagIDList:
                    date = self._readIFDEntry(TAG_DATE, tagIDList, fieldTypeList, nValuesList, valueOffsetList)
                    if type(date) in [type([1]), type((1, ))]:
                        date = helpString.join(date)
                else:
                    date = 'Unknown Date'
                stripOffsets = self._readIFDEntry(TAG_STRIP_OFFSETS, tagIDList, fieldTypeList, nValuesList, valueOffsetList)
                if TAG_ROWS_PER_STRIP in tagIDList:
                    rowsPerStrip = self._readIFDEntry(TAG_ROWS_PER_STRIP, tagIDList, fieldTypeList, nValuesList, valueOffsetList)[0]
                else:
                    rowsPerStrip = nRows
                    logger.warning('Non standard TIFF. Rows per strip TAG missing')
                if TAG_STRIP_BYTE_COUNTS in tagIDList:
                    stripByteCounts = self._readIFDEntry(TAG_STRIP_BYTE_COUNTS, tagIDList, fieldTypeList, nValuesList, valueOffsetList)
                else:
                    logger.warning('Non standard TIFF. Strip byte counts TAG missing')
                    if hasattr(nBits, 'index'):
                        expectedSum = 0
                        for n in nBits:
                            expectedSum += int(nRows * nColumns * n / 8)

                    else:
                        expectedSum = int(nRows * nColumns * nBits / 8)
                    stripByteCounts = [
                     expectedSum]
                if close:
                    self._TiffIO__makeSureFileIsClosed()
                if self._forceMonoOutput and interpretation > 1:
                    nBits = 32
                    colormap = None
                    sampleFormat = SAMPLE_FORMAT_FLOAT
                    interpretation = 1
                    useInfoCache = False
                    logger.debug('FORCED MONO')
        else:
            useInfoCache = True
        info = {}
        info['nRows'] = nRows
        info['nColumns'] = nColumns
        info['nBits'] = nBits
        info['compression'] = compression
        info['compression_type'] = compression_type
        info['imageDescription'] = imageDescription
        info['stripOffsets'] = stripOffsets
        info['rowsPerStrip'] = rowsPerStrip
        info['stripByteCounts'] = stripByteCounts
        info['software'] = software
        info['date'] = date
        info['colormap'] = colormap
        info['sampleFormat'] = sampleFormat
        info['photometricInterpretation'] = interpretation
        if model is not None:
            info['model'] = model
        infoDict = {}
        testString = 'PyMca'
        if software.startswith(testString):
            descriptionString = imageDescription
            items = descriptionString.split('=')
            for i in range(int(len(items) / 2)):
                key = '%s' % items[(i * 2)]
                value = '%s' % items[(i * 2 + 1)][:-1]
                infoDict[key] = value

        info['info'] = infoDict
        if self._maxImageCacheLength > 0 and useInfoCache:
            self._imageInfoCacheIndex.insert(0, nImage)
            self._imageInfoCache.insert(0, info)
            if len(self._imageInfoCacheIndex) > self._maxImageCacheLength:
                self._imageInfoCacheIndex = self._imageInfoCacheIndex[:self._maxImageCacheLength]
                self._imageInfoCache = self._imageInfoCache[:self._maxImageCacheLength]
        return info

    def _readImage(self, nImage, **kw):
        logger.debug('Reading image %d', nImage)
        if 'close' in kw:
            close = kw['close']
        else:
            close = True
        rowMin = kw.get('rowMin', None)
        rowMax = kw.get('rowMax', None)
        if nImage in self._imageDataCacheIndex:
            logger.debug('Reading image data from cache')
            return self._imageDataCache[self._imageDataCacheIndex.index(nImage)]
        self._TiffIO__makeSureFileIsOpen()
        if self._forceMonoOutput:
            oldMono = True
        else:
            oldMono = False
        try:
            self._forceMonoOutput = False
            info = self._readInfo(nImage, close=False)
            self._forceMonoOutput = oldMono
        except Exception:
            logger.debug('Backtrace', exc_info=True)
            self._forceMonoOutput = oldMono
            raise

        compression = info['compression']
        compression_type = info['compression_type']
        if compression:
            if compression_type != 32773:
                raise IOError('Compressed TIFF images not supported except packbits')
        else:
            logger.debug('Using PackBits compression')
        interpretation = info['photometricInterpretation']
        if interpretation == 2:
            pass
        else:
            if interpretation == 3:
                pass
            else:
                if interpretation > 2:
                    raise IOError('Only grayscale images supported')
                nRows = info['nRows']
                nColumns = info['nColumns']
                nBits = info['nBits']
                colormap = info['colormap']
                sampleFormat = info['sampleFormat']
                if rowMin is None:
                    rowMin = 0
                if rowMax is None:
                    rowMax = nRows - 1
                if rowMin < 0:
                    rowMin = nRows - rowMin
                if rowMax < 0:
                    rowMax = nRows - rowMax
                if rowMax < rowMin:
                    txt = 'Max Row smaller than Min Row. Reverse selection not supported'
                    raise NotImplemented(txt)
                if rowMin >= nRows:
                    raise IndexError('Image only has %d rows' % nRows)
                if rowMax >= nRows:
                    raise IndexError('Image only has %d rows' % nRows)
                if sampleFormat == SAMPLE_FORMAT_FLOAT:
                    if nBits == 32:
                        dtype = numpy.float32
                    else:
                        if nBits == 64:
                            dtype = numpy.float64
                        else:
                            raise ValueError('Unsupported number of bits for a float: %d' % nBits)
                else:
                    if sampleFormat in [SAMPLE_FORMAT_UINT, SAMPLE_FORMAT_VOID]:
                        if nBits in [8, (8, 8, 8), [8, 8, 8]]:
                            dtype = numpy.uint8
                        else:
                            if nBits in [16, (16, 16, 16), [16, 16, 16]]:
                                dtype = numpy.uint16
                            else:
                                if nBits in [32, (32, 32, 32), [32, 32, 32]]:
                                    dtype = numpy.uint32
                                else:
                                    if nBits in [64, (64, 64, 64), [64, 64, 64]]:
                                        dtype = numpy.uint64
                                    else:
                                        raise ValueError('Unsupported number of bits for unsigned int: %s' % (nBits,))
                    else:
                        if sampleFormat == SAMPLE_FORMAT_INT:
                            if nBits in [8, (8, 8, 8), [8, 8, 8]]:
                                dtype = numpy.int8
                            else:
                                if nBits in [16, (16, 16, 16), [16, 16, 16]]:
                                    dtype = numpy.int16
                                else:
                                    if nBits in [32, (32, 32, 32), [32, 32, 32]]:
                                        dtype = numpy.int32
                                    else:
                                        if nBits in [64, (64, 64, 64), [64, 64, 64]]:
                                            dtype = numpy.int64
                                        else:
                                            raise ValueError('Unsupported number of bits for signed int: %s' % (nBits,))
                        else:
                            raise ValueError('Unsupported combination. Bits = %s  Format = %d' % (nBits, sampleFormat))
                        if hasattr(nBits, 'index'):
                            image = numpy.zeros((nRows, nColumns, len(nBits)), dtype=dtype)
                        else:
                            if colormap is not None:
                                image = numpy.zeros((nRows, nColumns, 3), dtype=dtype)
                            else:
                                image = numpy.zeros((nRows, nColumns), dtype=dtype)
                fd = self.fd
                stripOffsets = info['stripOffsets']
                rowsPerStrip = info['rowsPerStrip']
                stripByteCounts = info['stripByteCounts']
                rowStart = 0
                if len(stripOffsets) == 1:
                    bytesPerRow = int(stripByteCounts[0] / rowsPerStrip)
                    nBytes = stripByteCounts[0]
                    if nRows == rowsPerStrip:
                        actualBytesPerRow = int(image.nbytes / nRows)
                        if actualBytesPerRow != bytesPerRow:
                            logger.warning('Bogus StripByteCounts information')
                            bytesPerRow = actualBytesPerRow
                            nBytes = (rowMax - rowMin + 1) * bytesPerRow
                        fd.seek(stripOffsets[0] + rowMin * bytesPerRow)
                        readout = numpy.frombuffer(fd.read(nBytes), dtype).copy()
                        if self._swap:
                            readout.byteswap(True)
                        if hasattr(nBits, 'index'):
                            readout.shape = (
                             -1, nColumns, len(nBits))
                        else:
                            if info['colormap'] is not None:
                                readout = colormap[readout]
                                readout.shape = (-1, nColumns, 3)
                            else:
                                readout.shape = (
                                 -1, nColumns)
                        image[...] = readout
                    else:
                        for i in range(len(stripOffsets)):
                            nRowsToRead = rowsPerStrip
                            rowEnd = int(min(rowStart + nRowsToRead, nRows))
                            if rowEnd < rowMin:
                                rowStart += nRowsToRead
                                continue
                                if rowStart > rowMax:
                                    break
                                fd.seek(stripOffsets[i])
                                nBytes = stripByteCounts[i]
                                if compression_type == 32773:
                                    try:
                                        bufferBytes = bytes()
                                    except Exception:
                                        bufferBytes = ''

                                    readBytes = 0
                                    tmpBuffer = fd.read(nBytes)
                                    while readBytes < nBytes:
                                        n = struct.unpack('b', tmpBuffer[readBytes:readBytes + 1])[0]
                                        readBytes += 1
                                        if n >= 0:
                                            bufferBytes += tmpBuffer[readBytes:readBytes + (n + 1)]
                                            readBytes += n + 1
                                        elif n > -128:
                                            bufferBytes += (-n + 1) * tmpBuffer[readBytes:readBytes + 1]
                                            readBytes += 1
                                        else:
                                            continue

                                    readout = numpy.frombuffer(bufferBytes, dtype).copy()
                                    if self._swap:
                                        readout.byteswap(True)
                                    if hasattr(nBits, 'index'):
                                        readout.shape = (
                                         -1, nColumns, len(nBits))
                                    else:
                                        if info['colormap'] is not None:
                                            readout = colormap[readout]
                                            readout.shape = (-1, nColumns, 3)
                                        else:
                                            readout.shape = (
                                             -1, nColumns)
                                    image[rowStart:rowEnd, :] = readout
                                else:
                                    readout = numpy.frombuffer(fd.read(nBytes), dtype).copy()
                                    if self._swap:
                                        readout.byteswap(True)
                                    if hasattr(nBits, 'index'):
                                        readout.shape = (
                                         -1, nColumns, len(nBits))
                                    else:
                                        if colormap is not None:
                                            readout = colormap[readout]
                                            readout.shape = (-1, nColumns, 3)
                                        else:
                                            readout.shape = (
                                             -1, nColumns)
                                        image[rowStart:rowEnd, :] = readout
                                rowStart += nRowsToRead

                    if close:
                        self._TiffIO__makeSureFileIsClosed()
                    if len(image.shape) == 3 and self._forceMonoOutput:
                        image = (image[:, :, 0] * 0.114 + image[:, :, 1] * 0.587 + image[:, :, 2] * 0.299).astype(numpy.float32)
                    if rowMin == 0 and rowMax == nRows - 1:
                        self._imageDataCacheIndex.insert(0, nImage)
                        self._imageDataCache.insert(0, image)
                        if len(self._imageDataCacheIndex) > self._maxImageCacheLength:
                            self._imageDataCacheIndex = self._imageDataCacheIndex[:self._maxImageCacheLength]
                            self._imageDataCache = self._imageDataCache[:self._maxImageCacheLength]
                        return image

    def writeImage(self, image0, info=None, software=None, date=None):
        if software is None:
            software = 'PyMca.TiffIO'
        self._TiffIO__makeSureFileIsOpen()
        fd = self.fd
        if not len(image0.shape):
            raise ValueError('Empty image')
        if len(image0.shape) == 1:
            image = image0[:]
            image.shape = (1, -1)
        else:
            image = image0
        if image.dtype == numpy.float64:
            image = image.astype(numpy.float32)
        fd.seek(0)
        mode = fd.mode
        name = fd.name
        if 'w' in mode:
            self._TiffIO__makeSureFileIsClosed()
            fd = None
            if os.path.exists(name):
                os.remove(name)
            fd = open(name, mode='wb+')
            self._initEmptyFile(fd)
        self.fd = fd
        self._TiffIO__makeSureFileIsOpen()
        fd = self.fd
        fd.seek(0, os.SEEK_END)
        endOfFile = fd.tell()
        if fd.tell() == 0:
            self._initEmptyFile(fd)
            fd.seek(0, os.SEEK_END)
            endOfFile = fd.tell()
        self._initInternalVariables(fd)
        st = self._structChar
        nImages = self.getImageFileDirectories()
        logger.debug('File contains %d images', nImages)
        if nImages == 0:
            fd.seek(4)
            fmt = st + 'I'
            fd.write(struct.pack(fmt, endOfFile))
        else:
            fd.seek(self._IFD[(-1)])
            fmt = st + 'H'
            numberOfDirectoryEntries = struct.unpack(fmt, fd.read(struct.calcsize(fmt)))[0]
            fmt = st + 'I'
            pos = self._IFD[(-1)] + 2 + 12 * numberOfDirectoryEntries
            fd.seek(pos)
            fmt = st + 'I'
            fd.write(struct.pack(fmt, endOfFile))
        fd.flush()
        fd.seek(0, os.SEEK_END)
        if info is None:
            description = info
        else:
            description = ''
            for key in info.keys():
                description += '%s=%s\n' % (key, info[key])

        outputIFD = self._getOutputIFD(image, description=description, software=software, date=date)
        fd.write(outputIFD)
        if self._swap:
            fd.write(image.byteswap().tobytes())
        else:
            fd.write(image.tobytes())
        fd.flush()
        self.fd = fd
        self._TiffIO__makeSureFileIsClosed()

    def _initEmptyFile(self, fd=None):
        if fd is None:
            fd = self.fd
        if sys.byteorder == 'little':
            order = 'II'
            fileOrder = 'little'
            self._structChar = '<'
        else:
            order = 'MM'
            fileOrder = 'big'
            self._structChar = '>'
        st = self._structChar
        if fileOrder == sys.byteorder:
            self._swap = False
        else:
            self._swap = True
        fd.seek(0)
        if sys.version < '3.0':
            fd.write(struct.pack(st + '2s', order))
            fd.write(struct.pack(st + 'H', 42))
            fd.write(struct.pack(st + 'I', 0))
        else:
            fd.write(struct.pack(st + '2s', bytes(order, 'utf-8')))
            fd.write(struct.pack(st + 'H', 42))
            fd.write(struct.pack(st + 'I', 0))
        fd.flush()

    def _getOutputIFD(self, image, description=None, software=None, date=None):
        nDirectoryEntries = 9
        imageDescription = None
        if description is not None:
            descriptionLength = len(description)
            while descriptionLength < 4:
                description = description + ' '
                descriptionLength = len(description)

            if isinstance(description, six.text_type):
                raw = description.encode('utf-8')
        else:
            if sys.version >= '3.0':
                raw = bytes(description, 'utf-8')
            elif isinstance(description, str):
                try:
                    raw = description.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        raw = description.decode('latin-1')
                    except UnicodeDecodeError:
                        raw = description

                if sys.version > '2.6':
                    raw = raw.encode('utf-8', errors='ignore')
                imageDescription = struct.pack('%ds' % len(raw), raw)
                nDirectoryEntries += 1
            if software is not None:
                softwareLength = len(software)
                while softwareLength < 4:
                    software = software + ' '
                    softwareLength = len(software)

                if sys.version >= '3.0':
                    software = bytes(software, 'utf-8')
                softwarePackedString = struct.pack('%ds' % softwareLength, software)
                nDirectoryEntries += 1
            else:
                softwareLength = 0
            if date is not None:
                dateLength = len(date)
                if sys.version >= '3.0':
                    date = bytes(date, 'utf-8')
                datePackedString = struct.pack('%ds' % dateLength, date)
                dateLength = len(datePackedString)
                nDirectoryEntries += 1
            else:
                dateLength = 0
        if len(image.shape) == 2:
            nRows, nColumns = image.shape
            nChannels = 1
        else:
            if len(image.shape) == 3:
                nRows, nColumns, nChannels = image.shape
            else:
                raise RuntimeError('Image does not have the right shape')
        dtype = image.dtype
        bitsPerSample = int(dtype.str[(-1)]) * 8
        compression = 1
        if nChannels == 1:
            interpretation = 1
            bitsPerSampleLength = 0
        else:
            if nChannels == 3:
                interpretation = 2
                bitsPerSampleLength = 6
                nDirectoryEntries += 1
            else:
                raise RuntimeError('Image with %d color channel(s) not supported' % nChannels)
            if imageDescription is not None:
                descriptionLength = len(imageDescription)
            else:
                descriptionLength = 0
            self.fd.seek(0, os.SEEK_END)
            endOfFile = self.fd.tell()
            if endOfFile == 0:
                endOfFile = 8
            if ALLOW_MULTIPLE_STRIPS:
                if not nRows % 4:
                    rowsPerStrip = int(nRows / 4)
                else:
                    if not nRows % 10:
                        rowsPerStrip = int(nRows / 10)
                    else:
                        if not nRows % 8:
                            rowsPerStrip = int(nRows / 8)
                        else:
                            if not nRows % 4:
                                rowsPerStrip = int(nRows / 4)
                            else:
                                if not nRows % 2:
                                    rowsPerStrip = int(nRows / 2)
                                else:
                                    rowsPerStrip = nRows
            else:
                rowsPerStrip = nRows
            stripByteCounts = int(nColumns * rowsPerStrip * bitsPerSample * nChannels / 8)
            if descriptionLength > 4:
                stripOffsets0 = endOfFile + dateLength + descriptionLength + 2 + 12 * nDirectoryEntries + 4
            else:
                stripOffsets0 = endOfFile + dateLength + 2 + 12 * nDirectoryEntries + 4
            if softwareLength > 4:
                stripOffsets0 += softwareLength
            stripOffsets0 += bitsPerSampleLength
            stripOffsets = [
             stripOffsets0]
            stripOffsetsLength = 0
            stripOffsetsString = None
            st = self._structChar
            if rowsPerStrip != nRows:
                nStripOffsets = int(nRows / rowsPerStrip)
                fmt = st + 'I'
                stripOffsetsLength = struct.calcsize(fmt) * nStripOffsets
                stripOffsets0 += stripOffsetsLength
                stripOffsets0 += stripOffsetsLength
                stripOffsets = []
                for i in range(nStripOffsets):
                    value = stripOffsets0 + i * stripByteCounts
                    stripOffsets.append(value)
                    if i == 0:
                        stripOffsetsString = struct.pack(fmt, value)
                        stripByteCountsString = struct.pack(fmt, stripByteCounts)
                    else:
                        stripOffsetsString += struct.pack(fmt, value)
                        stripByteCountsString += struct.pack(fmt, stripByteCounts)

            logger.debug('IMAGE WILL START AT %d', stripOffsets[0])
            if dtype in [numpy.float32, numpy.float64] or dtype.str[(-2)] == 'f':
                sampleFormat = SAMPLE_FORMAT_FLOAT
            else:
                if dtype in [numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64]:
                    sampleFormat = SAMPLE_FORMAT_UINT
                else:
                    if dtype in [numpy.int8, numpy.int16, numpy.int32, numpy.int64]:
                        sampleFormat = SAMPLE_FORMAT_INT
                    else:
                        raise ValueError('Unsupported data type %s' % dtype)
        info = {}
        info['nColumns'] = nColumns
        info['nRows'] = nRows
        info['nBits'] = bitsPerSample
        info['compression'] = compression
        info['photometricInterpretation'] = interpretation
        info['stripOffsets'] = stripOffsets
        if interpretation == 2:
            info['samplesPerPixel'] = 3
        info['rowsPerStrip'] = rowsPerStrip
        info['stripByteCounts'] = stripByteCounts
        info['date'] = date
        info['sampleFormat'] = sampleFormat
        outputIFD = ''
        if sys.version > '2.6':
            outputIFD = eval('b""')
        fmt = st + 'H'
        outputIFD += struct.pack(fmt, nDirectoryEntries)
        fmt = st + 'HHII'
        outputIFD += struct.pack(fmt, TAG_NUMBER_OF_COLUMNS, FIELD_TYPE_OUT['I'], 1, info['nColumns'])
        outputIFD += struct.pack(fmt, TAG_NUMBER_OF_ROWS, FIELD_TYPE_OUT['I'], 1, info['nRows'])
        if info['photometricInterpretation'] == 1:
            fmt = st + 'HHIHH'
            outputIFD += struct.pack(fmt, TAG_BITS_PER_SAMPLE, FIELD_TYPE_OUT['H'], 1, info['nBits'], 0)
        else:
            if info['photometricInterpretation'] == 2:
                fmt = st + 'HHII'
                outputIFD += struct.pack(fmt, TAG_BITS_PER_SAMPLE, FIELD_TYPE_OUT['H'], 3, info['stripOffsets'][0] - 2 * stripOffsetsLength - descriptionLength - dateLength - softwareLength - bitsPerSampleLength)
            else:
                raise RuntimeError('Unsupported photometric interpretation')
            fmt = st + 'HHIHH'
            outputIFD += struct.pack(fmt, TAG_COMPRESSION, FIELD_TYPE_OUT['H'], 1, info['compression'], 0)
            fmt = st + 'HHIHH'
            outputIFD += struct.pack(fmt, TAG_PHOTOMETRIC_INTERPRETATION, FIELD_TYPE_OUT['H'], 1, info['photometricInterpretation'], 0)
            if imageDescription is not None:
                descriptionLength = len(imageDescription)
                if descriptionLength > 4:
                    fmt = st + 'HHII'
                    outputIFD += struct.pack(fmt, TAG_IMAGE_DESCRIPTION, FIELD_TYPE_OUT['s'], descriptionLength, info['stripOffsets'][0] - 2 * stripOffsetsLength - descriptionLength)
                else:
                    fmt = st + 'HHI%ds' % descriptionLength
                    outputIFD += struct.pack(fmt, TAG_IMAGE_DESCRIPTION, FIELD_TYPE_OUT['s'], descriptionLength, imageDescription)
                if len(stripOffsets) == 1:
                    fmt = st + 'HHII'
                    outputIFD += struct.pack(fmt, TAG_STRIP_OFFSETS, FIELD_TYPE_OUT['I'], 1, info['stripOffsets'][0])
                else:
                    fmt = st + 'HHII'
                    outputIFD += struct.pack(fmt, TAG_STRIP_OFFSETS, FIELD_TYPE_OUT['I'], len(stripOffsets), info['stripOffsets'][0] - 2 * stripOffsetsLength)
                if info['photometricInterpretation'] == 2:
                    fmt = st + 'HHIHH'
                    outputIFD += struct.pack(fmt, TAG_SAMPLES_PER_PIXEL, FIELD_TYPE_OUT['H'], 1, info['samplesPerPixel'], 0)
                fmt = st + 'HHII'
                outputIFD += struct.pack(fmt, TAG_ROWS_PER_STRIP, FIELD_TYPE_OUT['I'], 1, info['rowsPerStrip'])
                if len(stripOffsets) == 1:
                    fmt = st + 'HHII'
                    outputIFD += struct.pack(fmt, TAG_STRIP_BYTE_COUNTS, FIELD_TYPE_OUT['I'], 1, info['stripByteCounts'])
            else:
                fmt = st + 'HHII'
                outputIFD += struct.pack(fmt, TAG_STRIP_BYTE_COUNTS, FIELD_TYPE_OUT['I'], len(stripOffsets), info['stripOffsets'][0] - stripOffsetsLength)
            if software is not None:
                if softwareLength > 4:
                    fmt = st + 'HHII'
                    outputIFD += struct.pack(fmt, TAG_SOFTWARE, FIELD_TYPE_OUT['s'], softwareLength, info['stripOffsets'][0] - 2 * stripOffsetsLength - descriptionLength - softwareLength - dateLength)
            else:
                fmt = st + 'HHI%ds' % softwareLength
                outputIFD += struct.pack(fmt, TAG_SOFTWARE, FIELD_TYPE_OUT['s'], softwareLength, softwarePackedString)
        if date is not None:
            fmt = st + 'HHII'
            outputIFD += struct.pack(fmt, TAG_DATE, FIELD_TYPE_OUT['s'], dateLength, info['stripOffsets'][0] - 2 * stripOffsetsLength - descriptionLength - dateLength)
        fmt = st + 'HHIHH'
        outputIFD += struct.pack(fmt, TAG_SAMPLE_FORMAT, FIELD_TYPE_OUT['H'], 1, info['sampleFormat'], 0)
        fmt = st + 'I'
        outputIFD += struct.pack(fmt, 0)
        if info['photometricInterpretation'] == 2:
            outputIFD += struct.pack('HHH', info['nBits'], info['nBits'], info['nBits'])
        if softwareLength > 4:
            outputIFD += softwarePackedString
        if date is not None:
            outputIFD += datePackedString
        if imageDescription is not None and descriptionLength > 4:
            outputIFD += imageDescription
        if stripOffsetsString is not None:
            outputIFD += stripOffsetsString
            outputIFD += stripByteCountsString
        return outputIFD