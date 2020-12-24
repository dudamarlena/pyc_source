# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/DpkgDebPackage.py
# Compiled at: 2007-11-06 15:08:00
__revision__ = 'r' + '$Revision: 49 $'[11:-2]
__all__ = ['DpkgDebPackage', 'DpkgDebPackageException']
import os, re, glob, shutil, gzip, tempfile, commands, errno
from minideblib.DpkgControl import DpkgParagraph
from minideblib.DpkgVersion import DpkgVersion
from minideblib.LoggableObject import LoggableObject

class DpkgDebPackageException(Exception):
    """General exception which could be raised by DpkgDebPackage"""

    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg


class DpkgDebPackage(LoggableObject):
    """This class represent complete information about Debian binary package"""

    def __init__(self, pkgfile=None):
        """ path -- path to .deb package """
        self.control = DpkgParagraph()
        self.md5sums = None
        self.__md5files = None
        self.changes = None
        self.news = None
        self.files = None
        self.__raw_files = None
        self.path = None
        if pkgfile:
            self.path = os.path.abspath(pkgfile)
            if not os.path.isfile(self.path):
                raise DpkgDebPackageException('Unable to locate file: %s' % self.path)
            self.load_control()
        return

    def load(self, path=None, getfiles=True, getchanges='both'):
        """ Loads .deb file for processing """
        path_changed = False
        if not path and not self.path:
            raise DpkgDebPackageException('No deb file specified')
        if path:
            new_path = os.path.abspath(path)
            if new_path != self.path:
                self.path = new_path
                path_changed = True
        if not os.path.isfile(self.path):
            raise DpkgDebPackageException('Unable to locate file: %s' % self.path)
        if path_changed or not self.control:
            self.load_control()
        if getchanges:
            self.load_changes(getchanges)
        if getfiles:
            self.load_contents()

    def load_contents(self):
        """ Reads contents of .deb file into memory """
        if self.path and os.path.isfile(self.path):
            self.__raw_files = self.__list_contents()
            if self.__raw_files:
                self.files = [ fname[5] for fname in self.__raw_files ]
        else:
            raise DpkgDebPackageException('Unable to locate file: %s' % self.path)

    def load_changes(self, getchanges='both'):
        """ Reads changelog and/or news information into memory """
        if self.path and os.path.isfile(self.path):
            (news, changes) = self.__extract_changes(getchanges)
            self.news = news
            self.changes = changes
        else:
            raise DpkgDebPackageException('Unable to locate file: %s' % self.path)

    def load_control(self):
        """ Reads control information into memory """
        if self.path:
            if os.path.isfile(self.path):
                tempdir = self.__extract_control()
                fhdl = open(os.path.join(tempdir, 'control'), 'r')
                self.control = DpkgParagraph()
                self.control.load(fhdl)
                fhdl.close()
                self.__parse_md5sums(tempdir) or self._logger.warning("Can't parse md5sums")
            else:
                self.__md5files = [ xsum[1] for xsum in self.md5sums ]
            shutil.rmtree(tempdir, True)
        else:
            raise DpkgDebPackageException('Unable to locate file: %s' % self.path)

    def __extract_changes(self, which, since_version=None):
        """Extract changelog entries, news or both from the package.
        If since_version is specified, only return entries later than the specified version.
        returns a sequence of Changes objects."""

        def changelog_variations(filename):
            """Return list of all possible changelog/news locations"""
            formats = [
             'usr/doc/*/%s.gz',
             'usr/share/doc/*/%s.gz',
             'usr/doc/*/%s',
             'usr/share/doc/*/%s',
             './usr/doc/*/%s.gz',
             './usr/share/doc/*/%s.gz',
             './usr/doc/*/%s',
             './usr/share/doc/*/%s']
            return [ format % filename for format in formats ]

        news_filenames = changelog_variations('NEWS.Debian')
        changelog_filenames = changelog_variations('changelog.Debian')
        changelog_filenames_native = changelog_variations('changelog')
        filenames = []
        if which == 'both' or which == 'news':
            filenames.extend(news_filenames)
        if which == 'both' or which == 'changelogs':
            filenames.extend(changelog_filenames)
            filenames.extend(changelog_filenames_native)
        tempdir = self.extract_contents(filenames)
        news = None
        for filename in news_filenames:
            news = self.__read_changelog(os.path.join(tempdir, filename), since_version)
            if news:
                break

        changelog = None
        for batch in (changelog_filenames, changelog_filenames_native):
            for filename in batch:
                changelog = self.__read_changelog(os.path.join(tempdir, filename), since_version)
                if changelog:
                    break

            if changelog:
                break

        shutil.rmtree(tempdir, True)
        return (
         news, changelog)

    def __extract_control(self):
        """Extracts content of control.tar.gz from .deb package"""
        try:
            tempdir = tempfile.mkdtemp(prefix='dpkgdebpackage')
        except AttributeError:
            tempdir = tempfile.mktemp()
            os.mkdir(tempdir)

        extract_command = 'ar p %s control.tar.gz | tar zxf - -C %s 2>/dev/null' % (self.path, tempdir)
        os.system(extract_command)
        return tempdir

    def extract_contents(self, filenames):
        """Extracts partial contents of Debian package to temporary directory"""
        try:
            tempdir = tempfile.mkdtemp(prefix='dpkgdebpackage')
        except AttributeError:
            tempdir = tempfile.mktemp()
            os.mkdir(tempdir)

        extract_command = 'ar p %s data.tar.gz |tar zxf - -C %s %s 2>/dev/null' % (
         self.path,
         tempdir,
         (' ').join([ "'%s'" % filen for filen in filenames ]))
        os.system(extract_command)
        return tempdir

    def __parse_md5sums(self, tempdir):
        """Parses md5sums file from extracted control section of debian package"""
        path = os.path.join(tempdir, 'md5sums')
        if not os.access(path, os.R_OK):
            print "Can't open file %s" % path
            return False
        self.md5sums = []
        fhdl = open(path, 'r')
        for line in fhdl.readlines():
            if line[33] != ' ':
                print '33 is not a space.\n %s' % line
                fhdl.close()
                return False
            argl = [
             line[:32].strip(), line[34:].strip()]
            self.md5sums.append(argl)

        fhdl.close()
        return True

    def __list_contents(self):
        """Returns filelist of data.tar.gz"""
        (status, output) = commands.getstatusoutput('ar p %s data.tar.gz | tar ztvf -' % self.path)
        if status != 0:
            return []
        files = [ line.split() for line in output.splitlines() ]
        return files

    def __read_changelog(self, filename, since_version):
        """Read changelog up to specified version"""
        changelog_header = re.compile('^\\S+ \\((?P<version>.*)\\) .*;.*urgency=(?P<urgency>\\w+).*')
        filenames = glob.glob(filename)
        fhdl = None
        for filename in filenames:
            try:
                if filename.endswith('.gz'):
                    fhdl = gzip.GzipFile(filename)
                else:
                    fhdl = open(filename)
                break
            except IOError, ioerr:
                if ioerr.errno == errno.ENOENT:
                    pass
                else:
                    raise

        if not fhdl:
            return
        changes = ''
        is_debian_changelog = 0
        for line in fhdl.readlines():
            match = changelog_header.match(line)
            if match:
                is_debian_changelog = 1
                if since_version:
                    if DpkgVersion(match.group('version')) <= since_version:
                        break
            changes += line

        fhdl.close()
        if not is_debian_changelog:
            return
        return changes