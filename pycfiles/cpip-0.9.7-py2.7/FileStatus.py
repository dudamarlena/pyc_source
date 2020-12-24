# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/FileStatus.py
# Compiled at: 2017-09-08 07:44:18
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__version__ = '0.9.5'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import os, sys, time, logging, hashlib, fnmatch
from optparse import OptionParser
from cpip import ExceptionCpip

class ExceptionFileStatus(ExceptionCpip):
    pass


class FileInfo(object):
    """Holds information on a text file."""

    def __init__(self, thePath):
        self._path = thePath
        self._sloc = 0
        self._size = 0
        self._hash = hashlib.md5()
        self._count = 0
        if self._path is not None:
            if not os.path.isfile(thePath):
                raise ExceptionFileStatus('Not a file path: %s' % thePath)
            self._size = os.path.getsize(self._path)
            self._sloc = 1
            for aLine in open(self._path).readlines():
                self._hash.update(aLine)
                self._sloc += 1

            self._count += 1
        return

    def writeHeader(self, theS=sys.stdout):
        """Writes header to stream."""
        theS.write('    SLOC  ')
        theS.write('    Size  ')
        theS.write('MD5')

    def write(self, theS=sys.stdout, incHash=True):
        """Writes the number of lines and bytes (optionally MD5) to stream."""
        theS.write('%8d  ' % self._sloc)
        theS.write('%8d  ' % self._size)
        if incHash:
            theS.write('%s' % self._hash.hexdigest())

    @property
    def sloc(self):
        """Lines in file."""
        return self._sloc

    @property
    def size(self):
        """Size in bytes."""
        return self._size

    @property
    def count(self):
        """Files processed."""
        return self._count

    def __iadd__(self, other):
        """Add other to me."""
        self._sloc += other.sloc
        self._size += other.size
        self._count += other.count
        return self


class FileInfoSet(object):
    """Contains information on a set of files."""

    def __init__(self, thePath, glob=None, isRecursive=False):
        self._infoMap = {}
        self.processPath(thePath, glob, isRecursive)

    def processPath(self, theP, glob=None, isRecursive=False):
        """Process a file or directory."""
        if os.path.isdir(theP):
            self.processDir(theP, glob, isRecursive)
        elif os.path.isfile(theP):
            self._infoMap[theP] = FileInfo(theP)

    def processDir(self, theDir, glob, isRecursive):
        """Read a directory and return a map of {path : class FileInfo, ...}"""
        assert os.path.isdir(theDir)
        for aName in os.listdir(theDir):
            p = os.path.join(theDir, aName)
            if os.path.isfile(p):
                if glob is not None:
                    for aPat in glob:
                        if fnmatch.fnmatch(aName, aPat):
                            self.processPath(p, glob, isRecursive)
                            break

                else:
                    self.processPath(p, glob, isRecursive)
            elif os.path.isdir(p) and isRecursive:
                self.processPath(p, glob, isRecursive)

        return

    def write(self, theS=sys.stdout):
        """Write summary to stream."""
        kS = sorted(self._infoMap.keys())
        fieldWidth = max([ len(k) for k in kS ])
        theS.write('%-*s  ' % (fieldWidth, 'File'))
        myTotal = FileInfo(None)
        myTotal.writeHeader(theS)
        theS.write('\n')
        for k in kS:
            theS.write('%-*s  ' % (fieldWidth, k))
            self._infoMap[k].write(theS)
            theS.write('\n')
            myTotal += self._infoMap[k]

        theS.write('%-*s  ' % (fieldWidth, '%s [%d]' % ('Total', myTotal.count)))
        myTotal.write(theS, incHash=False)
        theS.write('\n')
        return


def main():
    usage = 'usage: %prog [options] dir\nCounts files and sizes.'
    print 'Cmd: %s' % (' ').join(sys.argv)
    optParser = OptionParser(usage, version='%prog ' + __version__)
    optParser.add_option('-g', '--glob', type='string', dest='glob', default='*.py', help='Space separated list of file match patterns. [default: %default]')
    optParser.add_option('-l', '--loglevel', type='int', dest='loglevel', default=30, help='Log Level (debug=10, info=20, warning=30, error=40, critical=50) [default: %default]')
    optParser.add_option('-r', action='store_true', dest='recursive', default=False, help='Recursive. [default: %default]')
    opts, args = optParser.parse_args()
    clkStart = time.clock()
    logging.basicConfig(level=opts.loglevel, format='%(asctime)s %(levelname)-8s %(message)s', stream=sys.stdout)
    if len(args) != 1:
        optParser.print_help()
        optParser.error('No arguments!')
        return 1
    myFis = FileInfoSet(args[0], glob=opts.glob.split(), isRecursive=opts.recursive)
    myFis.write()
    clkExec = time.clock() - clkStart
    print 'CPU time = %8.3f (S)' % clkExec
    print 'Bye, bye!'
    return 0


if __name__ == '__main__':
    sys.exit(main())