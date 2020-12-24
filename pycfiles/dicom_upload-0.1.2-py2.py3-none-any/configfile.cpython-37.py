# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/configfile.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 6763 bytes
__doc__ = '\nconfigfile.py - Human-readable text configuration file library \nCopyright 2010  Luke Campagnola\nDistributed under MIT/X11 license. See license.txt for more infomation.\n\nUsed for reading and writing dictionary objects to a python-like configuration\nfile format. Data structures may be nested and contain any data type as long\nas it can be converted to/from a string using repr and eval.\n'
import re, os, sys
from .pgcollections import OrderedDict
GLOBAL_PATH = None
from . import units
from .python2_3 import asUnicode
from .Qt import QtCore
from .Point import Point
from .colormap import ColorMap
import numpy

class ParseError(Exception):

    def __init__(self, message, lineNum, line, fileName=None):
        self.lineNum = lineNum
        self.line = line
        self.fileName = fileName
        Exception.__init__(self, message)

    def __str__(self):
        if self.fileName is None:
            msg = 'Error parsing string at line %d:\n' % self.lineNum
        else:
            msg = "Error parsing config file '%s' at line %d:\n" % (self.fileName, self.lineNum)
        msg += '%s\n%s' % (self.line, self.message)
        return msg


def writeConfigFile(data, fname):
    s = genString(data)
    fd = open(fname, 'w')
    fd.write(s)
    fd.close()


def readConfigFile(fname):
    global GLOBAL_PATH
    if GLOBAL_PATH is not None:
        fname2 = os.path.join(GLOBAL_PATH, fname)
        if os.path.exists(fname2):
            fname = fname2
    GLOBAL_PATH = os.path.dirname(os.path.abspath(fname))
    try:
        fd = open(fname)
        s = asUnicode(fd.read())
        fd.close()
        s = s.replace('\r\n', '\n')
        s = s.replace('\r', '\n')
        data = parseString(s)[1]
    except ParseError:
        sys.exc_info()[1].fileName = fname
        raise
    except:
        print('Error while reading config file %s:' % fname)
        raise

    return data


def appendConfigFile(data, fname):
    s = genString(data)
    fd = open(fname, 'a')
    fd.write(s)
    fd.close()


def genString(data, indent=''):
    s = ''
    for k in data:
        sk = str(k)
        if len(sk) == 0:
            print(data)
            raise Exception('blank dict keys not allowed (see data above)')
        if not sk[0] == ' ':
            if ':' in sk:
                print(data)
                raise Exception('dict keys must not contain ":" or start with spaces [offending key is "%s"]' % sk)
            if isinstance(data[k], dict):
                s += indent + sk + ':\n'
                s += genString(data[k], indent + '    ')
            else:
                s += indent + sk + ': ' + repr(data[k]) + '\n'

    return s


def parseString(lines, start=0):
    data = OrderedDict()
    if isinstance(lines, basestring):
        lines = lines.split('\n')
        lines = [l for l in lines if re.search('\\S', l) if not re.match('\\s*#', l)]
    indent = measureIndent(lines[start])
    ln = start - 1
    try:
        while 1:
            ln += 1
            if ln >= len(lines):
                break
            l = lines[ln]
            if not re.match('\\s*#', l):
                if not re.search('\\S', l):
                    continue
                else:
                    lineInd = measureIndent(l)
                    if lineInd < indent:
                        ln -= 1
                        break
                    else:
                        if lineInd > indent:
                            raise ParseError('Indentation is incorrect. Expected %d, got %d' % (indent, lineInd), ln + 1, l)
                        else:
                            if ':' not in l:
                                raise ParseError('Missing colon', ln + 1, l)
                            k, p, v = l.partition(':')
                            k = k.strip()
                            v = v.strip()
                            local = units.allUnits.copy()
                            local['OrderedDict'] = OrderedDict
                            local['readConfigFile'] = readConfigFile
                            local['Point'] = Point
                            local['QtCore'] = QtCore
                            local['ColorMap'] = ColorMap
                            local['array'] = numpy.array
                            for dtype in ('int8', 'uint8', 'int16', 'uint16', 'float16',
                                          'int32', 'uint32', 'float32', 'int64',
                                          'uint64', 'float64'):
                                local[dtype] = getattr(numpy, dtype)

                            if len(k) < 1:
                                raise ParseError('Missing name preceding colon', ln + 1, l)
                            if k[0] == '(' and k[(-1)] == ')':
                                try:
                                    k1 = eval(k, local)
                                    if type(k1) is tuple:
                                        k = k1
                                except:
                                    pass

                                if re.search('\\S', v) and v[0] != '#':
                                    try:
                                        val = eval(v, local)
                                    except:
                                        ex = sys.exc_info()[1]
                                        raise ParseError("Error evaluating expression '%s': [%s: %s]" % (v, ex.__class__.__name__, str(ex)), ln + 1, l)

                            else:
                                if ln + 1 >= len(lines) or measureIndent(lines[(ln + 1)]) <= indent:
                                    val = {}
                        ln, val = parseString(lines, start=(ln + 1))
                data[k] = val

    except ParseError:
        raise
    except:
        ex = sys.exc_info()[1]
        raise ParseError('%s: %s' % (ex.__class__.__name__, str(ex)), ln + 1, l)

    return (
     ln, data)


def measureIndent(s):
    n = 0
    while n < len(s) and s[n] == ' ':
        n += 1

    return n


if __name__ == '__main__':
    import tempfile
    fn = tempfile.mktemp()
    tf = open(fn, 'w')
    cf = "\nkey: 'value'\nkey2:              ##comment\n                   ##comment\n    key21: 'value' ## comment\n                   ##comment\n    key22: [1,2,3]\n    key23: 234  #comment\n    "
    tf.write(cf)
    tf.close()
    print('=== Test:===')
    num = 1
    for line in cf.split('\n'):
        print('%02d   %s' % (num, line))
        num += 1

    print(cf)
    print('============')
    data = readConfigFile(fn)
    print(data)
    os.remove(fn)