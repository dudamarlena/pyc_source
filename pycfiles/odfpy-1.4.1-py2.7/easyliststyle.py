# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/easyliststyle.py
# Compiled at: 2020-01-18 11:47:38
import re, sys, os.path
sys.path.append(os.path.dirname(__file__))
from odf.style import Style, TextProperties, ListLevelProperties
from odf.text import ListStyle, ListLevelStyleNumber, ListLevelStyleBullet
_MAX_LIST_LEVEL = 10
SHOW_ALL_LEVELS = True
SHOW_ONE_LEVEL = False

def styleFromString(name, specifiers, delim, spacing, showAllLevels):
    specArray = specifiers.split(delim)
    return styleFromList(name, specArray, spacing, showAllLevels)


def styleFromList(styleName, specArray, spacing, showAllLevels):
    bullet = ''
    numPrefix = ''
    numSuffix = ''
    numberFormat = ''
    cssLengthNum = 0
    cssLengthUnits = ''
    numbered = False
    displayLevels = 0
    listStyle = ListStyle(name=styleName)
    numFormatPattern = re.compile('([1IiAa])')
    cssLengthPattern = re.compile('([^a-z]+)\\s*([a-z]+)?')
    m = cssLengthPattern.search(spacing)
    if m != None:
        cssLengthNum = float(m.group(1))
        if m.lastindex == 2:
            cssLengthUnits = m.group(2)
    i = 0
    while i < len(specArray):
        specification = specArray[i]
        m = numFormatPattern.search(specification)
        if m != None:
            numberFormat = m.group(1)
            numPrefix = specification[0:m.start(1)]
            numSuffix = specification[m.end(1):]
            bullet = ''
            numbered = True
            if showAllLevels:
                displayLevels = i + 1
            else:
                displayLevels = 1
        else:
            bullet = specification
            numPrefix = ''
            numSuffix = ''
            numberFormat = ''
            displayLevels = 1
            numbered = False
        if numbered:
            lls = ListLevelStyleNumber(level=i + 1)
            if numPrefix != '':
                lls.setAttribute('numprefix', numPrefix)
            if numSuffix != '':
                lls.setAttribute('numsuffix', numSuffix)
            lls.setAttribute('displaylevels', displayLevels)
        else:
            lls = ListLevelStyleBullet(level=i + 1, bulletchar=bullet[0])
        llp = ListLevelProperties()
        llp.setAttribute('spacebefore', str(cssLengthNum * (i + 1)) + cssLengthUnits)
        llp.setAttribute('minlabelwidth', str(cssLengthNum) + cssLengthUnits)
        lls.addElement(llp)
        listStyle.addElement(lls)
        i += 1

    return listStyle