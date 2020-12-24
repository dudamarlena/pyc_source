# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/convertTmplPathToModuleName.py
# Compiled at: 2019-09-22 10:12:27
import os.path, string
from Cheetah.compat import unicode
letters = None
try:
    letters = string.ascii_letters
except AttributeError:
    letters = string.letters

_l = ['_'] * 256
for c in string.digits + letters:
    _l[ord(c)] = c

_pathNameTransChars = ('').join(_l)
del _l
del c

def convertTmplPathToModuleName(tmplPath, _pathNameTransChars=_pathNameTransChars, splitdrive=os.path.splitdrive):
    try:
        moduleName = splitdrive(tmplPath)[1].translate(_pathNameTransChars)
    except (UnicodeError, TypeError):
        moduleName = unicode(splitdrive(tmplPath)[1]).translate(unicode(_pathNameTransChars))

    return moduleName