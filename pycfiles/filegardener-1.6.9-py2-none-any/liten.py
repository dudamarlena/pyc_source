# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\liten.py
# Compiled at: 2008-12-26 05:27:50
__version__ = '0.1.5'
__date__ = '2008-12-25'
import os, datetime, re, sys, string, time, optparse, hashlib, pdb, ConfigParser
from itertools import chain
from fnmatch import fnmatch
LITEN_DEBUG_MODE = int(os.environ.get('LITEN_DEBUG', 0))
MESSAGE = 'LITEN DEBUG MODE ENABLED:'
if LITEN_DEBUG_MODE == 1:
    print '%s Print Mode' % MESSAGE
if LITEN_DEBUG_MODE == 2:
    print '%s pdb Mode' % MESSAGE

class ActionsMixin(object):
    """An Actions Mixin Class"""

    def remove(self, file, dryrun=False, interactive=False):
        """
           takes a path and deletes file/unlinks
           """
        if dryrun:
            print 'Dry Run:  %s [NOT DELETED]' % file
            return
        else:
            print 'DELETING:  %s' % file
            try:
                status = os.remove(file)
            except Exception, err:
                print err
                return status

        if interactive:
            input = raw_input('Do you really want to delete %s [N]/Y' % file)
            if input == 'Y':
                print 'DELETING:  %s' % file
                try:
                    status = os.remove(file)
                except Exception, err:
                    print err
                    return status

            elif input == 'N':
                print 'Skipping:  %s' % file
                return
            else:
                print 'Skipping:  %s' % file
                return
        return


class FileAttributes(object):

    def makeModDate(self, path):
        """
        Makes a modification date object
        """
        mod = time.strftime('%m/%d/%Y %I:%M:%S %p', time.localtime(os.path.getmtime(path)))
        return mod

    def makeCreateDate(self, path):
        """
        Makes a creation date object
        """
        create = time.strftime('%m/%d/%Y %I:%M:%S %p', time.localtime(os.path.getctime(path)))
        return create

    def createChecksum(self, path):
        """
        Reads in file.  Creates checksum of file line by line.
        Returns complete checksum total for file.

        """
        if LITEN_DEBUG_MODE == 2:
            pdb.set_trace()
        try:
            try:
                fp = open(path)
                checksum = hashlib.md5()
                while True:
                    buffer = fp.read(8192)
                    if not buffer:
                        break
                    checksum.update(buffer)

                fp.close()
                checksum = checksum.digest()
            except IOError:
                if self.verbose:
                    print 'IO error for %s' % path
                checksum = None
                if LITEN_DEBUG_MODE == 1:
                    print 'IO error for %s' % path

        finally:
            if LITEN_DEBUG_MODE:
                print 'Performing checksum on: %s' % path

        return checksum

    def createSearchDate(self):
        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        return date

    def createExt(self, file):
        """
        takes a file on a path and returns extension
        """
        (shortname, ext) = os.path.splitext(file)
        return ext

    def sizeType(self):
        """
        Calculates size based on input.

        Uses regex search of input to determine size type.
        """
        if LITEN_DEBUG_MODE == 2:
            pdb.set_trace()
        patterns = {'bytes': '1', 'KB': '1024', 
           'MB': '1048576', 
           'GB': '1073741824', 
           'TB': '1099511627776'}
        try:
            for key in patterns:
                value = patterns[key]
                if re.search(key, self.fileSize):
                    if LITEN_DEBUG_MODE:
                        print 'Key: %s Filesize: %s ' % (key, self.fileSize)
                        print 'Value: %s ' % value
                    byteValue = int(self.fileSize.strip(key)) * int(value)
                    break
            else:
                byteValue = int(self.fileSize.strip()) * int(1048576)

        except Exception, err:
            if LITEN_DEBUG_MODE:
                print 'Problem evaluating:', self.fileSize, Exception, err

        return byteValue


class Liten(FileAttributes, ActionsMixin):
    """
    A base class for searching a file tree.

    Contains several methods for analyzing file objects.
    Main method is diskWalker, which walks filesystem and determines
    duplicates.

    You may modify the action that occurs when a duplicate is
    found my either creating an ActionsMixin method, or
    you can pass Liten a function that takes a file argument
    and process that file object.

    >>> Liten = Liten(spath='testData')
    >>> fakePath = 'testData/testDocOne.txt'
    >>> modDate = Liten.makeModDate(fakePath)
    >>> createDate = Liten.makeCreateDate(fakePath)
    >>> dupeFileOne = 'testData/testDocOne.txt'
    >>> checksumOne = Liten.createChecksum(dupeFileOne)
    >>> badChecksumAttempt = Liten.createChecksum('fileNotFound.txt')
    IO error for fileNotFound.txt
    >>> dupeFileTwo = 'testData/testDocTwo.txt'
    >>> checksumTwo = Liten.createChecksum(dupeFileTwo)
    >>> nonDupeFile = 'testData/testDocThree_wrong_match.txt'
    >>> checksumThree = Liten.createChecksum(nonDupeFile)
    >>> checksumOne == checksumTwo
    True
    >>> checksumOne == checksumThree
    False
    >>> SearchDate = Liten.createSearchDate()
    >>> createExt = Liten.createExt(dupeFileOne)
    >>> createExt
    '.txt'

    """

    def __init__(self, spath=None, fileSize='1MB', pattern='*', reportPath='LitenDuplicateReport.csv', config=None, verbose=True, delete=False, action=False):
        self.spath = spath
        self.reportPath = reportPath
        self.config = config
        self.fileSize = fileSize
        self.pattern = pattern
        self.verbose = verbose
        self.checksum_cache_key = {}
        self.checksum_cache_value = {}
        self.confirmed_dup_key = {}
        self.confirmed_dup_value = {}
        self.byte_cache = {}
        self.matches = []
        self.delete = delete
        self.action = action
        self.dupNumber = 0

    def _cacheChecksum(self, path, checksum, byteSize, file):
        checksum_cache_value = {'fullPath': path, 'checksum': checksum, 
           'modDate': self.makeCreateDate(path), 
           'dupNumber': self.dupNumber, 
           'searchDate': self.createSearchDate(), 
           'bytes': byteSize, 
           'fileType': None, 
           'fileExt': self.createExt(file)}
        self.checksum_cache_key[checksum] = checksum_cache_value
        return

    def diskWalker(self):
        """Walks Directory Tree Looking at Every File, while performing a
        duplicate match algorithm.

        Algorithm:
        This divides directory walk into doing either a more informed search
        if byte in key repository, or appending byte_size to list and moving
        to next file.  A md5 checksum is made of any file that has a byte size
        that has been found before.  The checksum is then used as the basis to
        determine duplicates.

        (Note that test includes .svn directory)

        >> from liten import Liten
        >>> Liten = Liten(spath='testData', verbose=False)
        >>> Liten.diskWalker()
        {}
        >>> Liten.fileSize="45bytes"
        >>> dupes = Liten.diskWalker()
        >>> print len(dupes)
        4

        """
        if LITEN_DEBUG_MODE == 2:
            pdb.set_trace()
        report = open(self.reportPath, 'w')
        if isinstance(self.spath, basestring):
            main_path = os.walk(self.spath)
        else:
            main_path = chain(*map(os.walk, self.spath))
        if LITEN_DEBUG_MODE == 1:
            print 'self.sizeType() %s' % self.sizeType()
        byteSizeThreshold = self.sizeType()
        self.dupNumber = 0
        byte_count = 0
        record_count = 0
        start = time.time()
        if self.verbose:
            print 'Printing dups over %s MB using md5 checksum:             [SIZE] [ORIG] [DUP] ' % int(byteSizeThreshold / 1048576)
        for (root, dirs, files) in main_path:
            for file in files:
                path = os.path.join(root, file)
                if os.path.isfile(path):
                    byte_size = os.path.getsize(path)
                    record_count += 1
                    if byte_size >= byteSizeThreshold:
                        if fnmatch(path, self.pattern):
                            if LITEN_DEBUG_MODE == 1:
                                print 'Matches: %s' % path
                            if byte_size not in self.byte_cache:
                                self.byte_cache[byte_size] = {'path': path, 'checksum': None}
                            else:
                                if LITEN_DEBUG_MODE == 1:
                                    print 'Doing checksum on %s' % path
                                checksum = self.createChecksum(path)
                                if checksum not in self.checksum_cache_key:
                                    orig_path = self.byte_cache[byte_size]['path']
                                    orig_checksum = self.byte_cache[byte_size]['checksum']
                                    if orig_checksum is None:
                                        orig_checksum = self.byte_cache[byte_size]['checksum'] = self.createChecksum(orig_path)
                                        self._cacheChecksum(orig_path, orig_checksum, byte_size, file)
                                if checksum not in self.checksum_cache_key:
                                    self._cacheChecksum(path, checksum, byte_size, file)
                                else:
                                    byte_count += byte_size
                                    self.dupNumber += 1
                                    orig_path = self.checksum_cache_key[checksum]['fullPath']
                                    orig_mod_date = self.checksum_cache_key[checksum]['modDate']
                                    if self.verbose:
                                        print byte_size / 1048576, 'MB ', 'ORIG: ',
                                        print orig_path, 'DUPE: ', path
                                    report.write('Duplicate Version,     Path,                                          Size,       ModDate\n')
                                    report.write('%s, %s, %s MB, %s\n' % ('Original',
                                     orig_path, byte_size / 1048576, orig_mod_date))
                                    dupeModDate = self.makeCreateDate(path)
                                    report.write('%s, %s, %s MB, %s\n' % ('Duplicate',
                                     path, byte_size / 1048576, dupeModDate))
                                    if self.action:
                                        self.action(path)
                                    elif self.delete:
                                        self.remove(path)
                                    self.confirmed_dup_key[orig_path] = self.checksum_cache_value
                                    confirmed_dup_value = {'fullPath': path, 'modDate': dupeModDate, 
                                       'dupNumber': self.dupNumber, 
                                       'searchDate': self.createSearchDate(), 
                                       'checksum': checksum, 
                                       'bytes': byte_size, 
                                       'fileType': None, 
                                       'fileExt': self.createExt(file)}
                                    self.confirmed_dup_key[path] = confirmed_dup_value

        if self.verbose:
            print '\n'
            print 'LITEN REPORT: \n'
            print 'Search Path:                 ', self.spath
            print 'Filtered For Pattern Match:  ', self.pattern
            if self.config:
                print 'Used config file:            ', self.config
            print 'Total Files Searched:        ', record_count
            print 'Wasted Space in Duplicates:  ', byte_count / 1048576, ' MB'
            print 'Report Generated at:         ', self.reportPath
            end = time.time()
            timer = end - start
            timer = long(timer / 60)
            print 'Search Time:                 ', timer, ' minutes\n'
        return self.confirmed_dup_key


class ProcessConfig(object):
    """
    Reads in optional configuration file that replaces command line options
    """

    def __init__(self, file='config.ini'):
        self.file = file

    def readConfig(self):
        """reads and processes config file and returns results"""
        Config = ConfigParser.ConfigParser()
        Config.read(self.file)
        sections = Config.sections()
        for parameter in sections:
            try:
                path = Config.items(parameter)[0][1]
                if LITEN_DEBUG_MODE == 1:
                    print 'Config file path: %s' % path
            except:
                path = None

            try:
                pattern = Config.items(parameter)[1][1]
                if LITEN_DEBUG_MODE == 1:
                    print 'Config file pattern: %s' % pattern
            except:
                pattern = None

            try:
                size = Config.items(parameter)[2][1]
                if LITEN_DEBUG_MODE == 1:
                    print 'Config file size: %s' % size
            except:
                size = None

        return (
         path, size, pattern)


class LitenController(object):
    """
    Controller for DiskStat Command Line Tool.
    Handles optionparser parameters and setup.
    """

    def run(self):
        """Run method for Class"""
        if LITEN_DEBUG_MODE == 2:
            pdb.set_trace()
        descriptionMessage = '\n        A command line tool for detecting duplicates using md5 checksums.\n        '
        p = optparse.OptionParser(description=descriptionMessage, prog='liten', version='liten %s' % __version__, usage='%prog [options] [starting dir1] [dir2] ...')
        p.add_option('--config', '-c', help='Path to read in config file')
        p.add_option('--size', '-s', help='File Size Example:  10bytes, 10KB, 10MB,10GB,10TB                     plain number defaults to MB (1 = 1MB)', default='1MB')
        p.add_option('--pattern', '-p', help='Pattern Match Examples: *.txt, *.iso, music[0-5].mp3', default='*')
        p.add_option('--quiet', '-q', action='store_true', help='Suppresses all STDOUT.', default=False)
        p.add_option('--delete', '-d', action='store_true', help='DELETES all duplicate matches permanently!', default=False)
        p.add_option('--report', '-r', help='Path to store duplicate report. Default CWD', default='LitenDuplicateReport.csv')
        p.add_option('--test', '-t', action='store_true', help='Runs doctest.')
        (options, arguments) = p.parse_args()
        if options.test:
            _test()
            sys.exit(0)
        if options.config:
            if LITEN_DEBUG_MODE == 2:
                pdb.set_trace()
            process = ProcessConfig(file=options.config)
            try:
                config = process.readConfig()
                print config
                path = config[0]
                size = config[1]
                pattern = config[2]
                print 'Using %s, path=%s, size=%s, pattern=%s' % (
                 options.config, path, size, pattern)
                start = Liten(spath=path, fileSize=size, pattern=pattern, config=options.config)
                start.diskWalker()
                sys.exit(0)
            except Exception, err:
                print 'Problem parsing config file: %s' % options.config
                print err
                sys.exit(1)

        if options.quiet:
            verbose = False
        else:
            verbose = True
        if len(arguments) > 0:
            for arg in arguments:
                if not os.path.isdir(arg):
                    print "Search path does't exist or is not a directory: %s" % arg
                    sys.exit(1)

            try:
                start = Liten(spath=arguments, fileSize=options.size, pattern=options.pattern, reportPath=options.report, verbose=verbose, delete=options.delete)
                start.diskWalker()
            except UnboundLocalError, err:
                print err
                if LITEN_DEBUG_MODE == 1:
                    print 'Error: %s' % err
                print 'Invalid Search Size Parameter: %s run --help for help' % options.size
                sys.exit(1)

        else:
            p.print_help()


def main():
    """Runs liten."""
    create = LitenController()
    create.run()


def _test():
    """Runs doctests."""
    import doctest
    doctest.testmod(verbose=True)


if __name__ == '__main__':
    main()