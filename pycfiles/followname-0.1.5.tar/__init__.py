# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /lvm1/home/sl/work/work20/pyfollower/pyfollowname/src/followname/__init__.py
# Compiled at: 2020-02-04 01:53:05
import os, time

class Follower(object):
    """        Implements tail --follow=name like GNU tail
        """
    line_terminators = ('\r\n', '\n', '\r')

    def __init__(self, filename, read_size=1024, all=False, end=False, debug=False):
        self.read_size = read_size
        self.filename = filename
        self.file = None
        self.testfile = None
        self.info = None
        self.testinfo = None
        self.all = all
        self.end = end
        self.debug = debug
        return

    def follow(self, delay=1.0):
        """                Iterator generator that returns lines as data is added to the file.

                Based on: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/157035
                """
        trailing = True
        while 1:
            if self.file is None:
                try:
                    self.file = open(self.filename, 'r')
                except IOError:
                    pass

                if self.file is None:
                    if self.debug:
                        print 'Could not open %s' % self.filename
                    time.sleep(delay)
                    continue
                self.info = os.fstat(self.file.fileno())
                if not self.all:
                    self.file.seek(0, 2)
                if self.debug:
                    print 'Opened %s inode: %d size: %d' % (self.filename, self.info.st_ino, self.info.st_size)
            else:
                self.info = os.fstat(self.file.fileno())
            line = self.file.readline()
            if line:
                if self.debug:
                    print 'Line: %s' % line
                if trailing and line in self.line_terminators:
                    trailing = False
                    continue
                if line[(-1)] in self.line_terminators:
                    line = line[:-1]
                    if line[-1:] == '\r\n' and '\r\n' in self.line_terminators:
                        line = line[:-1]
                trailing = False
                self.info = os.fstat(self.file.fileno())
                if self.debug:
                    print 'yield: %s' % line
                yield line
                continue
            try:
                self.testfile = open(self.filename, 'r')
            except IOError:
                pass

            if self.testfile is None:
                trailing = True
                time.sleep(delay)
                continue
            self.testinfo = os.fstat(self.testfile.fileno())
            if self.info.st_ino == self.testinfo.st_ino and self.info.st_size <= self.testinfo.st_size:
                self.testfile.close()
                self.testfile = None
                continue
            self.info = self.testinfo
            self.testinfo = None
            self.file.close()
            self.file = self.testfile
            self.testfile = None

        return

    def close(self):
        if self.file is not None:
            self.file.close()
        return


def follow():
    r"""        Iterator generator that returns lines as data is added to the file.

        >>> import os
        >>> f = open('test_follow.txt', 'w')
        >>> _ = f.write('Line 1\n')
        >>> _ = f.write('Line 2\n')
        >>> _ = f.write('Line 3\n')
        >>> _ = f.write('Line 4\n')
        >>> _ = f.write('Line 5\n')
        >>> f.flush()
        >>> generator = follow()
        >>> next(generator)
        'Line 1'
        >>> next(generator)
        'Line 2'
        >>> next(generator)
        'Line 3'
        >>> next(generator)
        'Line 4'
        >>> f.close()
        >>> os.remove('test_follow.txt')
        """
    follower = Follower('test_follow.txt', all=True)
    return follower.follow()


def _test():
    import doctest
    doctest.testmod()


def _main(filepath, options):
    follower = Follower(filepath, all=options.all, end=options.end)
    try:
        try:
            for line in follower.follow(delay=options.sleep):
                print line

        except KeyboardInterrupt:
            pass

    finally:
        follower.close()


def main():
    from optparse import OptionParser
    usage = 'usage: %prog [options] filename'
    parser = OptionParser(usage=usage)
    parser.add_option('-e', '--end', dest='end', action='store_true', default=False, help='display all data in file when started, default is new data only')
    parser.add_option('-a', '--all', dest='all', action='store_true', default=False, help='display all data in file when started, default is new data only')
    parser.add_option('-s', '--sleep-interval', dest='sleep', default=1.0, metavar='S', type='float', help='sleep  for  approximately  S  seconds between iterations')
    parser.add_option('-f', '--follow', dest='follow', default=False, action='store_true', help='output appended data as  the  file  grows')
    options, args = parser.parse_args()
    if args is None or len(args) == 0:
        parser.print_help()
        exit(1)
    _main(args[0], options)
    return


if __name__ == '__main__':
    main()