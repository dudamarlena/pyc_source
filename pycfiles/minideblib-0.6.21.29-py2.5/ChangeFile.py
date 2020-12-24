# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/ChangeFile.py
# Compiled at: 2007-11-06 15:08:00
__revision__ = 'r' + '$Revision: 58 $'[11:-2]
__all__ = ['ChangeFile', 'ChangeFileException']
import os, re, string, stat, popen2
from minideblib import DpkgControl
from minideblib import SignedFile
from minideblib.LoggableObject import LoggableObject

class ChangeFileException(Exception):
    """Exception generated in error situations"""

    def __init__(self, value):
        Exception.__init__(self)
        self._value = value

    def __repr__(self):
        return `(self._value)`

    def __str__(self):
        return `(self._value)`


class ChangeFile(DpkgControl.DpkgParagraph, LoggableObject):

    def __init__(self):
        DpkgControl.DpkgParagraph.__init__(self)
        self.dsc = False

    def load_from_file(self, filename):
        if filename[-4:] == '.dsc':
            self.dsc = True
        fhdl = SignedFile.SignedFile(open(filename))
        self.load(fhdl)
        fhdl.close()

    def getFiles(self):
        out = []
        try:
            files = self['files']
        except KeyError:
            return []

        if self.dsc:
            lineregexp = re.compile('^([0-9a-f]{32})[ \t]+(\\d+)[ \t]+([0-9a-zA-Z][-+:.,=~0-9a-zA-Z_]+)$')
        else:
            lineregexp = re.compile('^([0-9a-f]{32})[ \t]+(\\d+)[ \t]+([-/a-zA-Z0-9]+)[ \t]+([-a-zA-Z0-9]+)[ \t]+([0-9a-zA-Z][-+:.,=~0-9a-zA-Z_]+)$')
        for line in files:
            if line == '':
                continue
            match = lineregexp.match(line)
            if match is None:
                raise ChangeFileException('Couldn\'t parse file entry "%s" in Files field of .changes' % (line,))
            if self.dsc:
                out.append((match.group(1), match.group(2), '', '', match.group(3)))
            else:
                out.append((match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)))

        return out

    def verify(self, sourcedir):
        for (md5sum, size, section, prioriy, filename) in self.getFiles():
            self._verify_file_integrity(os.path.join(sourcedir, filename), int(size), md5sum)

    def _verify_file_integrity(self, filename, expected_size, expected_md5sum):
        self._logger.debug('Checking integrity of %s' % (filename,))
        try:
            statbuf = os.stat(filename)
            if not stat.S_ISREG(statbuf[stat.ST_MODE]):
                raise ChangeFileException('%s is not a regular file' % (filename,))
            size = statbuf[stat.ST_SIZE]
        except OSError, excp:
            raise ChangeFileException("Can't stat %s: %s" % (filename, excp.strerror))

        if size != expected_size:
            raise ChangeFileException('File size for %s does not match that specified in .dsc' % (filename,))
        if self._get_file_md5sum(filename) != expected_md5sum:
            raise ChangeFileException('md5sum for %s does not match that specified in .dsc' % (filename,))
        self._logger.debug('Verified md5sum %s and size %s for %s' % (expected_md5sum, expected_size, filename))

    def _get_file_md5sum(self, filename):
        if os.access('/usr/bin/md5sum', os.X_OK):
            cmd = '/usr/bin/md5sum %s' % (filename,)
            self._logger.debug('Running: %s' % (cmd,))
            child = popen2.Popen3(cmd, 1)
            child.tochild.close()
            erroutput = child.childerr.read()
            child.childerr.close()
            if erroutput != '':
                child.fromchild.close()
                raise ChangeFileException('md5sum returned error output "%s"' % (erroutput,))
            (md5sum, filename) = string.split(child.fromchild.read(), None, 1)
            child.fromchild.close()
            status = child.wait()
            if not (status is None or os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0):
                if os.WIFEXITED(status):
                    msg = 'md5sum exited with error code %d' % (os.WEXITSTATUS(status),)
                elif os.WIFSTOPPED(status):
                    msg = 'md5sum stopped unexpectedly with signal %d' % (os.WSTOPSIG(status),)
                elif os.WIFSIGNALED(status):
                    msg = 'md5sum died with signal %d' % (os.WTERMSIG(status),)
                raise ChangeFileException(msg)
            return md5sum.strip()
        import md5
        fhdl = open(filename)
        md5sum = md5.new()
        buf = fhdl.read(8192)
        while buf != '':
            md5sum.update(buf)
            buf = fhdl.read(8192)

        fhdl.close()
        return md5sum.hexdigest()