# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/glyphviewer/glyphviewer.py
# Compiled at: 2018-07-18 07:17:20
from blocks import blockbyint, namefromindex, indexfromname, numblocks
from fontTools import ttLib
import os.path, urllib, datetime, urllib2
PLAT_STANDARD_ID = 3
PLAT_UNIENC_ID = 1
PLAT_UCS4_ID = 10
ALL_CHAR_BLOCK = 'All Unicode Characters'
FONT_NAME_PLATID = 1
FONT_NAME_ENCID = 0
FONT_NAME_CPY = 0
FONT_NAME_FFY = 1
FONT_NAME_SFY = 2
FONT_NAME_USI = 3
FONT_NAME_FNM = 4
FONT_NAME_VSN = 5
FONT_NAME_PSC = 6
FONT_NAME_TMK = 7
FONT_NAME_MFC = 8
FONT_NAME_DES = 9
FONT_NAME_DCS = 10
FONT_NAME_URL = 11
FONT_NAME_URD = 12
FONT_NAME_LDS = 13
FONT_NAME_LIU = 14
GC_NOERROR = 0
GC_NORESOURCE = 1
GC_RETFAIL = 2
GC_TIMEOUT = 3
GC_TOOBIG = 4
GC_NOTAFONT = 5
GC_NOHEADER = 6
GC_NOUNICODE = 7
GC_OTHERERROR = 8
GC_WARNCORS = 9
FONT_MAX_SIZE = 3145728
FONT_TIMEOUT = 120
FONT_TIMEOUT_DELTA = datetime.timedelta(seconds=FONT_TIMEOUT)
GC_ERRORMSG = [
 '',
 'It cannot be opened.',
 'It cannot be accessed or retrieved.',
 'It too more than %d seconds to retrieve it.' % FONT_TIMEOUT,
 'It exceeds %d bytes in size. ' % FONT_MAX_SIZE,
 'It does not appear to be a legitimate font file.',
 'There is no font header found.',
 "The font does not appear to be a legitimate Unicode font. Did you select a 'Symbol' or     'Wingdings' font for processing? If so, shame on you.",
 "We don't know what's happened, but some error has arisen. Sorry about that.",
 'It is possible to analyse the font header, but CORS prevents the     display of the glyphs in the font. In this case, the browser will display characters     using some fall-back font, which should not be used as a guide to the appearance of the     font selected here.']
DODGY = 'Invalid HTML Characters'

def isvalhtml(ichar):
    """ Input: numerical value for character. Returns True if it corresponds
    to a legitimate HTML character; False otherwise.

    Note 1: not tested for characters beyond 65536.
    Note 2: makes 0 a dodgy character as well.
    """
    if ichar <= 31:
        return False
    if ichar >= 127 and ichar <= 159:
        return False
    if ichar == 65535 or ichar == 65534:
        return False
    if ichar >= 64976 and ichar <= 65007:
        return False
    return True


class TooBigException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TimeoutException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def sizecheck(count, blockSize, totalSize):
    sizeread = 0
    blocksize = blockSize
    if totalSize > FONT_MAX_SIZE:
        raise TooBigException(totalSize)
    if count * blocksize > FONT_MAX_SIZE:
        raise TooBigException(count * blocksize)


class glyphArray:
    """ Represents a array of unicode character with the name of its block
        (or "All Unicode Characters" if there is no particular block.
    """

    def __init__(self, blockName, codePoints):
        self.blockName = blockName
        self.codePoints = codePoints

    def __unicode__(self):
        return self.blockName + ': ' + unicode(self.codePoints) + '\n'

    def __str__(self):
        return unicode(self)


class fontHeader:
    """ Represents the header of a font - in a form presentable in HTML. """

    def __init__(self, ournametable):

        def stringex(font_name_id):
            our_data = ournametable.getName(font_name_id, FONT_NAME_PLATID, FONT_NAME_ENCID)
            self.ournametable = ournametable
            if our_data:
                return our_data.string
            else:
                return
                return

        self.copyright = stringex(FONT_NAME_CPY)
        self.fontfamily = stringex(FONT_NAME_FFY)
        self.subfamily = stringex(FONT_NAME_SFY)
        self.usi = stringex(FONT_NAME_USI)
        self.fullname = stringex(FONT_NAME_FNM)
        self.version = stringex(FONT_NAME_VSN)
        self.ps = stringex(FONT_NAME_PSC)
        self.trademark = stringex(FONT_NAME_TMK)
        self.manufac = stringex(FONT_NAME_MFC)
        self.designer = stringex(FONT_NAME_DES)
        self.description = stringex(FONT_NAME_DCS)
        self.urlfontven = stringex(FONT_NAME_URL)
        self.urlfontdes = stringex(FONT_NAME_URD)
        self.descrip = stringex(FONT_NAME_LDS)
        self.licenseurl = stringex(FONT_NAME_LIU)

    def __unicode__(self):
        return self.fullname

    def __str__(self):
        return unicode(self)


def glyphCatcher(fontName, bStoreInBlocks=False, debugMode=False, bCheckCORS=False):
    """ This is the main meat of the glyphviewer application. The function
        takes a font, extracts the header and a list of the glyphs it
        supports. Or attempts to...

        Return values are of the form:
        (error code, fontHeader, sequence of glyphArray,)

        Arguments:
        fontName: the file name or URL for a font.
        bStoreInBlocks: if False, the function returns a stored sequence of
        integers for the glyphs. if True, the function returns a sequence of
        sequences, each corresponding to blocks in Unicode.
        debugMode: if True, fontName can be a file name. If False, fontName
        must be a URL. This is generally the same value as settings.DEBUG.
        bCheckCORS: whether to check for Cross Origin Resource Sharing
    """

    def _cleanup(arg):
        """ Only called in the routine. """
        if bUseTempFile:
            if os.path.exists(resourceName):
                os.unlink(resourceName)
        return arg

    DodgyGlyphArray = glyphArray(DODGY, [])
    bUseTempFile = False
    retrievalInfo = None
    bCORSBlues = False
    if fontName == None:
        fontName = ''
    if os.path.exists(fontName) & debugMode:
        resourceName = fontName
    else:
        opener = urllib.FancyURLopener({})
        try:
            nowtime = datetime.datetime.now()
            retrievalInfo = opener.retrieve(fontName, reporthook=sizecheck)
            if bCheckCORS:
                if 'Access-Control-Allow-Origin' not in retrievalInfo[1]:
                    bCORSBlues = True
                elif retrievalInfo[1]['Access-Control-Allow-Origin'] != '*':
                    bCORSBlues = True
        except TooBigException:
            return (
             GC_TOOBIG, None, None)
        except TimeoutException:
            return (
             GC_TIMEOUT, None, None)
        except:
            return (
             GC_RETFAIL, None, None)

        resourceName = retrievalInfo[0]
        bUseTempFile = True
    try:
        ourFont = ttLib.TTFont(resourceName)
    except ttLib.TTLibError:
        print ttLib.TTLibError.message
        return _cleanup((GC_NOTAFONT, None, None))
    except:
        return _cleanup((GC_OTHERERROR, None, None))

    if bCORSBlues:
        ourgoodoutcome = GC_WARNCORS
    else:
        ourgoodoutcome = GC_NOERROR
    try:
        cmaptable = ourFont['cmap'].getcmap(PLAT_STANDARD_ID, PLAT_UCS4_ID)
        if cmaptable is None:
            cmaptable = ourFont['cmap'].getcmap(PLAT_STANDARD_ID, PLAT_UNIENC_ID)
            if cmaptable is None:
                return _cleanup((GC_NOUNICODE, None, None))
        ourheader = fontHeader(ourFont['name'])
    except:
        return _cleanup((GC_NOHEADER, None, None))

    if bStoreInBlocks:
        blockcontents = [ [] for i in range(numblocks()) ]
        for i in cmaptable.cmap.keys():
            if not isvalhtml(i):
                DodgyGlyphArray.codePoints.append(i)
            else:
                blockcontents[indexfromname(blockbyint(i))].append(i)

        [ i.sort() for i in blockcontents ]
        blockarrangements = [
         DodgyGlyphArray]
        for i in range(numblocks()):
            if len(blockcontents[i]) > 0:
                blockarrangements.append(glyphArray(namefromindex(i), blockcontents[i]))

        return _cleanup((ourgoodoutcome, ourheader, blockarrangements))
    else:
        blockcontents = list(cmaptable.cmap.keys())
        blockcontents.sort()
        ExcellentGlyphArray = glyphArray(ALL_CHAR_BLOCK, [])
        for i in blockcontents:
            if isvalhtml(i):
                ExcellentGlyphArray.codePoints.append(i)
            else:
                DodgyGlyphArray.codePoints.append(i)

        return _cleanup((ourgoodoutcome, ourheader, [DodgyGlyphArray, ExcellentGlyphArray]))
        return


if __name__ == '__main__':
    print glyphCatcher('', True)
    content = glyphCatcher('http://themes.googleusercontent.com/static/fonts/robotoslab/v1/y7lebkjgREBJK96VQi37ZobN6UDyHWBl620a-IRfuBk.woff', False)
    header = content[1]
    print header
    print header.urlfontven
    print header.urlfontdes
    body = content[2]
    for i in body:
        print i