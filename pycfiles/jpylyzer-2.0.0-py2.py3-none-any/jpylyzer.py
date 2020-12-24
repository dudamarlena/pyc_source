# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/jpylyzer/jpylyzer/jpylyzer.py
# Compiled at: 2019-10-29 07:18:47
"""Jpylyzer validator for JPEG 200 Part 1 (JP2) images.

Requires: Python 2.7 (older versions won't work) OR Python 3.2 or more recent
  (Python 3.0 and 3.1 won't work either!)

Copyright (C) 2011 - 2017 Johan van der Knijff, Koninklijke Bibliotheek -
  National Library of the Netherlands

Contributors:
   Rene van der Ark, NL (refactoring of original code).
   Lars Buitinck, NL.
   Adam Retter, The National Archives, UK.
   Jaishree Davey, The National Archives, UK.
   Laura Damian, The National Archives, UK.
   Carl Wilson, Open Preservation Foundation, UK.
   Stefan Weil, UB Mannheim, DE.
   Adam Fritzler, Planet Labs, USA.
   Thomas Ledoux, Bibliotheque Nationale de France
"""
import sys, mmap, os, time, datetime, glob, argparse, codecs, re
from xml.dom import minidom
import xml.etree.ElementTree as ETree
from six import u
from . import config
from . import etpatch as ET
from . import boxvalidator as bv
from . import mix
from . import shared
SCRIPT_PATH, SCRIPT_NAME = os.path.split(sys.argv[0])
if not SCRIPT_NAME:
    SCRIPT_NAME = 'jpylyzer'
__version__ = '2.0.0rc1'
PARSER = argparse.ArgumentParser(description='JP2 image validator and properties extractor')
EXISTING_FILES = []
NS_STRING_1 = 'http://openpreservation.org/ns/jpylyzer/'
NS_STRING_2 = 'http://openpreservation.org/ns/jpylyzer/v2/'
XSI_NS_STRING = 'http://www.w3.org/2001/XMLSchema-instance'
LOC_SCHEMA_STRING_1 = 'http://openpreservation.org/ns/jpylyzer/ http://jpylyzer.openpreservation.org/jpylyzer-v-1-1.xsd'
LOC_SCHEMA_STRING_2 = 'http://openpreservation.org/ns/jpylyzer/v2/ http://jpylyzer.openpreservation.org/jpylyzer-v-2-0.xsd'

def generatePropertiesRemapTable():
    """Generate nested dictionary.

    Dictionary is used to map 'raw' property values (mostly integer values)
    to corresponding text descriptions.
    """
    enumerationsMap = {}
    yesNoMap = {}
    yesNoMap[0] = 'no'
    yesNoMap[1] = 'yes'
    signMap = {}
    signMap[0] = 'unsigned'
    signMap[1] = 'signed'
    cMap = {}
    cMap[7] = 'jpeg2000'
    methMap = {}
    methMap[1] = 'Enumerated'
    methMap[2] = 'Restricted ICC'
    methMap[3] = 'Any ICC'
    methMap[4] = 'Vendor Colour'
    enumCSMap = {}
    enumCSMap[16] = 'sRGB'
    enumCSMap[17] = 'greyscale'
    enumCSMap[18] = 'sYCC'
    profileClassMap = {}
    profileClassMap['scnr'] = 'Input Device Profile'
    profileClassMap['mntr'] = 'Display Device Profile'
    profileClassMap['prtr'] = 'Output Device Profile'
    profileClassMap['link'] = 'DeviceLink Profile'
    profileClassMap['spac'] = 'ColorSpace Conversion Profile'
    profileClassMap['abst'] = 'Abstract Profile'
    profileClassMap['nmcl'] = 'Named Colour Profile'
    primaryPlatformMap = {}
    primaryPlatformMap['APPL'] = 'Apple Computer, Inc.'
    primaryPlatformMap['MSFT'] = 'Microsoft Corporation'
    primaryPlatformMap['SGI'] = 'Silicon Graphics, Inc.'
    primaryPlatformMap['SUNW'] = 'Sun Microsystems, Inc.'
    transparencyMap = {}
    transparencyMap[0] = 'Reflective'
    transparencyMap[1] = 'Transparent'
    glossinessMap = {}
    glossinessMap[0] = 'Glossy'
    glossinessMap[1] = 'Matte'
    polarityMap = {}
    polarityMap[0] = 'Positive'
    polarityMap[1] = 'Negative'
    colourMap = {}
    colourMap[0] = 'Colour'
    colourMap[1] = 'Black and white'
    renderingIntentMap = {}
    renderingIntentMap[0] = 'Perceptual'
    renderingIntentMap[1] = 'Media-Relative Colorimetric'
    renderingIntentMap[2] = 'Saturation'
    renderingIntentMap[3] = 'ICC-Absolute Colorimetric'
    mTypMap = {}
    mTypMap[0] = 'direct use'
    mTypMap[1] = 'palette mapping'
    cTypMap = {}
    cTypMap[0] = 'colour'
    cTypMap[1] = 'opacity'
    cTypMap[2] = 'premultiplied opacity'
    cTypMap[65535] = 'not specified'
    cAssocMap = {}
    cAssocMap[0] = 'all colours'
    cAssocMap[65535] = 'no colours'
    rsizMap = {}
    rsizMap[0] = 'ISO/IEC 15444-1'
    rsizMap[1] = 'Profile 0'
    rsizMap[2] = 'Profile 1'
    precinctsMap = {}
    precinctsMap[0] = 'default'
    precinctsMap[1] = 'user defined'
    orderMap = {}
    orderMap[0] = 'LRCP'
    orderMap[1] = 'RLCP'
    orderMap[2] = 'RPCL'
    orderMap[3] = 'PCRL'
    orderMap[4] = 'CPRL'
    transformationMap = {}
    transformationMap[0] = '9-7 irreversible'
    transformationMap[1] = '5-3 reversible'
    roiStyleMap = {}
    roiStyleMap[0] = 'Implicit ROI (maximum shift)'
    qStyleMap = {}
    qStyleMap[0] = 'no quantization'
    qStyleMap[1] = 'scalar derived'
    qStyleMap[2] = 'scalar expounded'
    registrationMap = {}
    registrationMap[0] = 'binary'
    registrationMap[1] = 'ISO/IEC 8859-15 (Latin)'
    enumerationsMap['unkC'] = yesNoMap
    enumerationsMap['iPR'] = yesNoMap
    enumerationsMap['profileClass'] = profileClassMap
    enumerationsMap['primaryPlatform'] = primaryPlatformMap
    enumerationsMap['embeddedProfile'] = yesNoMap
    enumerationsMap['profileCannotBeUsedIndependently'] = yesNoMap
    enumerationsMap['transparency'] = transparencyMap
    enumerationsMap['glossiness'] = glossinessMap
    enumerationsMap['polarity'] = polarityMap
    enumerationsMap['colour'] = colourMap
    enumerationsMap['renderingIntent'] = renderingIntentMap
    enumerationsMap['bSign'] = signMap
    enumerationsMap['mTyp'] = mTypMap
    if not config.LEGACY_XML_FLAG:
        enumerationsMap['precincts'] = precinctsMap
    else:
        enumerationsMap['precincts'] = yesNoMap
    enumerationsMap['sop'] = yesNoMap
    enumerationsMap['eph'] = yesNoMap
    enumerationsMap['multipleComponentTransformation'] = yesNoMap
    enumerationsMap['codingBypass'] = yesNoMap
    enumerationsMap['resetOnBoundaries'] = yesNoMap
    enumerationsMap['termOnEachPass'] = yesNoMap
    enumerationsMap['vertCausalContext'] = yesNoMap
    enumerationsMap['predTermination'] = yesNoMap
    enumerationsMap['segmentationSymbols'] = yesNoMap
    enumerationsMap['bPCSign'] = signMap
    enumerationsMap['ssizSign'] = signMap
    enumerationsMap['c'] = cMap
    enumerationsMap['meth'] = methMap
    enumerationsMap['enumCS'] = enumCSMap
    enumerationsMap['cTyp'] = cTypMap
    enumerationsMap['cAssoc'] = cAssocMap
    enumerationsMap['order'] = orderMap
    enumerationsMap['roiStyle'] = roiStyleMap
    enumerationsMap['transformation'] = transformationMap
    enumerationsMap['rsiz'] = rsizMap
    enumerationsMap['qStyle'] = qStyleMap
    enumerationsMap['rcom'] = registrationMap
    return enumerationsMap


def fileToMemoryMap(filename):
    """Read contents of filename to memory map object."""
    f = open(filename, 'rb')
    platform = config.PLATFORM
    try:
        if platform == 'win32':
            fileData = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            fileData = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
    except ValueError:
        fileData = ''

    f.close()
    return fileData


def checkOneFile(path, validationFormat='jp2'):
    """Process one file and return analysis result as element object."""
    if config.LEGACY_XML_FLAG:
        elementRootName = 'jpylyzer'
        nsString = NS_STRING_1
        locSchemaString = LOC_SCHEMA_STRING_1
    else:
        elementRootName = 'file'
        nsString = NS_STRING_2
        locSchemaString = LOC_SCHEMA_STRING_2
    if config.INPUT_RECURSIVE_FLAG or config.INPUT_WRAPPER_FLAG:
        root = ET.Element(elementRootName)
    else:
        root = ET.Element(elementRootName, {'xmlns': nsString, 'xmlns:xsi': XSI_NS_STRING, 
           'xsi:schemaLocation': locSchemaString})
    if config.LEGACY_XML_FLAG:
        toolInfo = ET.Element('toolInfo')
    fileInfo = ET.Element('fileInfo')
    statusInfo = ET.Element('statusInfo')
    fileName = os.path.basename(path)
    filePath = os.path.abspath(path)
    fileNameCleaned = stripSurrogatePairs(fileName)
    filePathCleaned = stripSurrogatePairs(filePath)
    if config.LEGACY_XML_FLAG:
        toolInfo.appendChildTagWithText('toolName', SCRIPT_NAME)
        toolInfo.appendChildTagWithText('toolVersion', __version__)
    fileInfo.appendChildTagWithText('fileName', fileNameCleaned)
    fileInfo.appendChildTagWithText('filePath', filePathCleaned)
    fileInfo.appendChildTagWithText('fileSizeInBytes', str(os.path.getsize(path)))
    try:
        dt = os.path.getmtime(path)
        lastModifiedDate = datetime.datetime.fromtimestamp(dt).isoformat()
    except ValueError:
        dt = time.ctime(0)
        lastModifiedDate = datetime.datetime.fromtimestamp(dt).isoformat()

    fileInfo.appendChildTagWithText('fileLastModified', lastModifiedDate)
    success = True
    try:
        fileData = fileToMemoryMap(path)
        if validationFormat == 'jp2':
            resultsJP2 = bv.BoxValidator('JP2', fileData).validate()
        elif validationFormat == 'j2c':
            resultsJP2 = bv.BoxValidator('contiguousCodestreamBox', fileData).validate()
        fileIsValid = resultsJP2.isValid
        tests = resultsJP2.tests
        characteristics = resultsJP2.characteristics
        if fileData != '':
            fileData.close()
        remapTable = generatePropertiesRemapTable()
        tests.makeHumanReadable()
        characteristics.makeHumanReadable(remapTable)
    except Exception as ex:
        fileIsValid = False
        success = False
        exceptionType = type(ex)
        if exceptionType == MemoryError:
            failureMessage = 'memory error (file size too large)'
        elif exceptionType == IOError:
            failureMessage = 'I/O error (cannot open file)'
        elif exceptionType == RuntimeError:
            failureMessage = 'runtime error, please report to developers by creating ' + 'an issue at https://github.com/openpreserve/jpylyzer/issues'
        else:
            failureMessage = 'unknown error, please report to developers by creating ' + 'an issue at https://github.com/openpreserve/jpylyzer/issues'
        shared.printWarning(failureMessage)
        tests = ET.Element('tests')
        characteristics = ET.Element('properties')

    if config.MIX_FLAG != 0 and fileIsValid:
        mixProperties = mix.Mix(config.MIX_FLAG).generateMix(characteristics)
    statusInfo.appendChildTagWithText('success', str(success))
    if not success:
        statusInfo.appendChildTagWithText('failureMessage', failureMessage)
    if config.LEGACY_XML_FLAG:
        root.append(toolInfo)
    root.append(fileInfo)
    root.append(statusInfo)
    if config.LEGACY_XML_FLAG:
        root.appendChildTagWithText('isValidJP2', str(fileIsValid))
    else:
        root.appendChildTagWithText('isValid', str(fileIsValid))
        root.findall('.//isValid')[0].set('format', config.VALIDATION_FORMAT)
    root.append(tests)
    root.append(characteristics)
    extension = ET.Element('propertiesExtension')
    if config.MIX_FLAG != 0:
        root.append(extension)
        if validationFormat == 'jp2' and fileIsValid:
            extension.append(mixProperties)
    return root


def checkNullArgs(args):
    """Check if the passed args list.

    Exits program if invalid or no input argument is supplied.
    """
    if not args:
        print ''
        PARSER.print_help()
        sys.exit(config.ERR_CODE_NO_IMAGES)


def checkNoInput(files):
    """Check passed input files list.

    Results in any existing input files at all (and exits if not).
    """
    if not files:
        shared.printWarning('no images to check!')
        sys.exit(config.ERR_CODE_NO_IMAGES)


def printHelpAndExit():
    """Print help message and exit."""
    print ''
    PARSER.print_help()
    sys.exit()


def stripSurrogatePairs(ustring):
    """Remove surrogate pairs from a Unicode string."""
    if config.PYTHON_VERSION.startswith(config.PYTHON_3):
        try:
            ustring.encode('utf-8')
        except UnicodeEncodeError:
            tmp = ustring.encode('utf-8', 'replace')
            ustring = tmp.decode('utf-8', 'ignore')

    if config.PYTHON_VERSION.startswith(config.PYTHON_2):
        lone = re.compile(u('(?x)            # verbose expression (allows comments)\n            (                    # begin group\n            [\\ud800-\\udbff]      #   match leading surrogate\n            (?![\\udc00-\\udfff])  #   but only if not followed by trailing surrogate\n            )                    # end group\n            |                    #  OR\n            (                    # begin group\n            (?<![\\ud800-\\udbff]) #   if not preceded by leading surrogate\n            [\\udc00-\\udfff]      #   match trailing surrogate\n            )                   # end group\n            '))
        tmp = lone.sub('', ustring).encode('utf-8')
        ustring = tmp.decode('utf-8')
    return ustring


def getFiles(searchpattern):
    """Append paths of all files that match search pattern to EXISTING_FILES."""
    results = glob.glob(searchpattern)
    for f in results:
        if os.path.isfile(f):
            EXISTING_FILES.append(f)


def getFilesWithPatternFromTree(rootDir, pattern):
    """Recurse into directory tree and return list of all files.

    NOTE: directory names are disabled here!!
    """
    for dirname, dirnames, _ in os.walk(rootDir):
        for subdirname in dirnames:
            thisDirectory = os.path.join(dirname, subdirname)
            searchpattern = os.path.join(thisDirectory, pattern)
            getFiles(searchpattern)


def getFilesFromTree(rootDir):
    """Recurse into directory tree and return list of all files.

    NOTE: directory names are disabled here!!
    """
    for dirname, dirnames, filenames in os.walk(rootDir):
        for subdirname in dirnames:
            thisDirectory = os.path.join(dirname, subdirname)

        for filename in filenames:
            thisFile = os.path.join(dirname, filename)
            EXISTING_FILES.append(thisFile)


def findFiles(recurse, paths):
    """Find all files that match a wildcard expression and add their paths to EXISTING_FILES."""
    WILDCARD = '*'
    for root in paths:
        if config.PYTHON_VERSION.startswith(config.PYTHON_2):
            root = unicode(root, 'utf-8')
        if os.path.isfile(root):
            EXISTING_FILES.append(root)
        elif WILDCARD in root:
            if not os.path.isabs(root):
                root = os.path.abspath(root)
            filesList = glob.glob(root)
            if len(filesList) == 1 and os.path.isdir(filesList[0]):
                root = filesList[0]
            if len(filesList) == 1 and os.path.isfile(filesList[0]):
                EXISTING_FILES.append(filesList[0])
            if len(filesList) > 1:
                for f in filesList:
                    if os.path.isfile(f):
                        EXISTING_FILES.append(f)

        elif not os.path.isdir(root) and not os.path.isfile(root):
            msg = root + ' does not exist'
            shared.printWarning(msg)
        if recurse:
            if not os.path.isabs(root):
                root = os.path.abspath(root)
            if WILDCARD in root:
                pathAndFilePattern = os.path.split(root)
                path = pathAndFilePattern[0]
                filePattern = pathAndFilePattern[1]
                filenameAndExtension = os.path.splitext(filePattern)
                if WILDCARD in path:
                    filepath = glob.glob(path)
                    if len(filepath) == 1:
                        getFilesWithPatternFromTree(filepath[0], filePattern)
                    if len(filepath) > 1:
                        for f in filepath:
                            if os.path.isdir(f):
                                getFilesWithPatternFromTree(f, filePattern)

                elif WILDCARD in filePattern:
                    getFilesWithPatternFromTree(path, filePattern)
                elif WILDCARD in filenameAndExtension:
                    filenameAndExtension = os.path.splitext(filePattern)
                    extension = WILDCARD + filenameAndExtension[1]
                    getFilesWithPatternFromTree(path, extension)
            elif os.path.isdir(root):
                getFilesFromTree(root)


def writeElement(elt, codec):
    """Write element as XML to stdout using defined codec."""
    if config.PYTHON_VERSION.startswith(config.PYTHON_2):
        xmlOut = ET.tostring(elt, 'UTF-8', 'xml')
    if config.PYTHON_VERSION.startswith(config.PYTHON_3):
        xmlOut = ET.tostring(elt, 'unicode', 'xml')
    if not config.NO_PRETTY_XML_FLAG:
        xmlPretty = minidom.parseString(xmlOut).toprettyxml('    ')
        xmlAsList = xmlPretty.split('\n')
        del xmlAsList[0]
        xmlOut = ('\n').join(xmlAsList)
        codec.write(xmlOut)
    else:
        if config.PYTHON_VERSION.startswith(config.PYTHON_2):
            ETree.ElementTree(elt).write(codec, xml_declaration=False)
        if config.PYTHON_VERSION.startswith(config.PYTHON_3):
            codec.write(xmlOut)


def checkFiles(recurse, wrap, paths):
    """Check the input argument path(s) for existing files and analyse them."""
    if config.LEGACY_XML_FLAG:
        locSchemaString = LOC_SCHEMA_STRING_1
    else:
        locSchemaString = LOC_SCHEMA_STRING_2
    findFiles(recurse, paths)
    checkNoInput(EXISTING_FILES)
    if config.PYTHON_VERSION.startswith(config.PYTHON_2):
        out = codecs.getwriter(config.UTF8_ENCODING)(sys.stdout)
    else:
        if config.PYTHON_VERSION.startswith(config.PYTHON_3):
            out = codecs.getwriter(config.UTF8_ENCODING)(sys.stdout.buffer)
        if config.LEGACY_XML_FLAG:
            nsString = NS_STRING_1
        else:
            nsString = NS_STRING_2
        if wrap or recurse:
            xmlHead = "<?xml version='1.0' encoding='UTF-8'?>\n"
            if not config.LEGACY_XML_FLAG:
                xmlHead += '<jpylyzer xmlns="' + nsString + '" '
            else:
                xmlHead += '<results xmlns="' + nsString + '" '
            xmlHead += 'xmlns:xsi="' + XSI_NS_STRING + '" '
            xmlHead += 'xsi:schemaLocation="' + locSchemaString + '">\n'
        else:
            xmlHead = "<?xml version='1.0' encoding='UTF-8'?>\n"
        out.write(xmlHead)
        if not config.LEGACY_XML_FLAG:
            toolInfo = ET.Element('toolInfo')
            toolInfo.appendChildTagWithText('toolName', SCRIPT_NAME)
            toolInfo.appendChildTagWithText('toolVersion', __version__)
            writeElement(toolInfo, out)
        for path in EXISTING_FILES:
            xmlElement = checkOneFile(path, config.VALIDATION_FORMAT)
            writeElement(xmlElement, out)

    if wrap or recurse:
        if not config.LEGACY_XML_FLAG:
            out.write('</jpylyzer>\n')
        else:
            out.write('</results>\n')


def parseCommandLine():
    """Parse command line arguments."""
    PARSER.add_argument('--format', '-f', action='store', type=str, dest='fmt', default='jp2', help='validation format; allowed values: jp2, j2c (default: jp2)')
    PARSER.add_argument('--legacyout', '-l', action='store_true', dest='legacyXMLFlag', default=False, help='report output in jpylyzer 1.x format (provided for backward                                 compatibility only)')
    PARSER.add_argument('--mix', type=int, choices=[1, 2], dest='mixFlag', default=0, help='report additional output in NISO MIX format (version 1.0 or 2.0)')
    PARSER.add_argument('--nopretty', action='store_true', dest='noPrettyXMLFlag', default=False, help='suppress pretty-printing of XML output')
    PARSER.add_argument('--nullxml', action='store_true', dest='extractNullTerminatedXMLFlag', default=False, help="extract null-terminated XML content from XML and UUID boxes                                 (doesn't affect validation)")
    PARSER.add_argument('--recurse', '-r', action='store_true', dest='inputRecursiveFlag', default=False, help='when analysing a directory, recurse into subdirectories                                 (implies --wrapper)')
    PARSER.add_argument('--verbose', action='store_true', dest='outputVerboseFlag', default=False, help='report test results in verbose format')
    PARSER.add_argument('--version', '-v', action='version', version=__version__)
    PARSER.add_argument('--wrapper', '-w', action='store_true', dest='inputWrapperFlag', default=False, help="wrap output for individual image(s) in 'results' XML element                                 (deprecated in jpylyzer 2.x, only takes effect if                                 --legacyout is used)")
    PARSER.add_argument('jp2In', action='store', type=str, nargs='+', help='input JP2 image(s), may be one or more (whitespace-separated) path                                 expressions; prefix wildcard (*) with backslash (\\) in Linux')
    args = PARSER.parse_args()
    return args


def main():
    """Main command line application."""
    args = parseCommandLine()
    jp2In = args.jp2In
    if not jp2In:
        printHelpAndExit()
    config.OUTPUT_VERBOSE_FLAG = args.outputVerboseFlag
    config.EXTRACT_NULL_TERMINATED_XML_FLAG = args.extractNullTerminatedXMLFlag
    config.INPUT_RECURSIVE_FLAG = args.inputRecursiveFlag
    config.INPUT_WRAPPER_FLAG = args.inputWrapperFlag
    config.NO_PRETTY_XML_FLAG = args.noPrettyXMLFlag
    config.VALIDATION_FORMAT = args.fmt.lower()
    config.LEGACY_XML_FLAG = args.legacyXMLFlag
    config.MIX_FLAG = args.mixFlag
    if config.VALIDATION_FORMAT not in ('jp2', 'j2c'):
        msg = "'" + config.VALIDATION_FORMAT + "'  is not a supported value for --format"
        shared.errorExit(msg)
    if config.LEGACY_XML_FLAG and config.VALIDATION_FORMAT == 'j2c':
        msg = ' j2c format is supported if --legacyout is set'
        shared.errorExit(msg)
    if not config.LEGACY_XML_FLAG:
        config.INPUT_WRAPPER_FLAG = True
    if config.LEGACY_XML_FLAG:
        config.MIX_FLAG = 0
    if config.VALIDATION_FORMAT == 'j2c':
        config.MIX_FLAG = 0
    checkFiles(config.INPUT_RECURSIVE_FLAG, config.INPUT_WRAPPER_FLAG, jp2In)


if __name__ == '__main__':
    main()