# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/pygwt.py
# Compiled at: 2008-09-03 09:02:13
sNextHashId = 0

def getNextHashId():
    global sNextHashId
    sNextHashId += 1
    return sNextHashId


def getHashCode(o):
    JS('\n    return (o == null) ? 0 :\n        (o.$H ? o.$H : (o.$H = pygwt_getNextHashId()));\n    ')


def getModuleName():
    JS('\n    return $moduleName;\n    ')


def getModuleBaseURL():
    print 'TODO'
    return ''
    JS('\n    // this is intentionally not using $doc, because we want the module\'s own url\n    var s = document.location.href;\n    \n    // Pull off any hash.\n    var i = s.indexOf(\'#\');\n    if (i != -1)\n        s = s.substring(0, i);\n    \n    // Pull off any query string.\n    i = s.indexOf(\'?\');\n    if (i != -1)\n        s = s.substring(0, i);\n    \n    // Rip off everything after the last slash.\n    i = s.lastIndexOf(\'/\');\n    if (i != -1)\n        s = s.substring(0, i);\n\n    return (s.length > 0) ? s + "/" : "";\n    ')