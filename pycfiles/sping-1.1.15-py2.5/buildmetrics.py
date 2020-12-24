# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\PS\buildmetrics.py
# Compiled at: 2002-01-21 21:51:42
import sys, string
print sys.version
from fontTools.agl import UV2AGL
import fontTools.afmLib, pidPS, fontinfo
M_aglName = UV2AGL[ord('M')]
from pyart._fontmap import font2file

def font2afm(adobeFontName):
    pfb = font2file[adobeFontName]
    afm = pfb[:-3] + 'afm'
    return afm


def getAFM(adobeFontName):
    afmFileName = font2afm(adobeFontName)
    return fontTools.afmLib.AFM(path=afmFileName)


def latin1FontWidth_DictCode(afm, pid_font_name):
    """Returns python code for a dictionary mapping a PID font name to an array of
    glyph widths as described in the afm class"""
    dictCodeStr = []
    widthArraySubStr = []
    dictCodeStr.append(" '%s': [ " % string.lower(pid_font_name))
    for latin1 in range(256):
        if UV2AGL.has_key(latin1):
            name = UV2AGL[latin1]
        else:
            name = '.notdef'
        if afm._chars.has_key(name):
            metric = afm._chars[name]
        else:
            try:
                metric = afm['.notdef']
            except KeyError:
                try:
                    metric = afm[M_aglName]
                except KeyError:
                    metric = (
                     -1, 250, (0, 0, 0, 0))

        (stdchr, width, bbox) = metric
        widthArraySubStr.append('%s' % width)

    dictCodeStr.append(string.join(widthArraySubStr, ', '))
    dictCodeStr.append(']')
    return string.join(dictCodeStr, ' ')


def generateCache():
    code = []
    for fontname in fontinfo.StandardRomanFonts:
        print 'doing font %s' % fontname
        afm = getAFM(fontname)
        code.append(latin1FontWidth_DictCode(afm, string.lower(fontname)))

    fp = open('latin1MetricsCache.py', 'w')
    fp.write('FontWidths = {  \n')
    code = string.join(code, ',\n')
    fp.write(code)
    fp.write('} \n')
    fp.close()


if __name__ == '__main__':
    print 'Generating latin1MetricsCache.py'
    generateCache()