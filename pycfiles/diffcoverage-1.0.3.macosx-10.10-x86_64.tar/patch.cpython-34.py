# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewcrosio/projects/expenses/virtualenv/lib/python3.4/site-packages/diffcoverage/patch.py
# Compiled at: 2016-02-03 09:18:16
# Size of source mod 2**32: 35426 bytes
""" Patch utility to apply unified diffs

    Brute-force line-by-line non-recursive parsing

    Copyright (c) 2008-2011 anatoly techtonik
    Available under the terms of MIT license

    Project home: http://code.google.com/p/python-patch/

    $Id: patch.py 150 2011-10-07 09:31:02Z techtonik $
    $HeadURL: http://python-patch.googlecode.com/svn/trunk/patch.py $

MIT License
-----------

Copyright (c) 2008-2011 anatoly techtonik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
import logging, re
from StringIO import StringIO
import urllib2
from os.path import exists, isabs, isfile, abspath, normpath
import os
debugmode = False
logger = logging.getLogger(__name__)
debug = logger.debug
info = logger.info
warning = logger.warning
DIFF = PLAIN = 'plain'
GIT = 'git'
HG = MERCURIAL = 'mercurial'
SVN = SUBVERSION = 'svn'
MIXED = MIXED = 'mixed'

def fromfile(filename):
    """Parse patch file and return PatchSet() object for error reporting"""
    debug('reading %s' % filename)
    with open(filename, 'rb') as (patch_file):
        return PatchSet(patch_file)


def fromstring(s):
    """Parse text string and return PatchSet() object"""
    return PatchSet(StringIO(s))


def fromurl(url):
    """Read patch from URL"""
    return PatchSet(urllib2.urlopen(url))


class Hunk(object):
    __doc__ = ' Parsed hunk data container (hunk starts with @@ -R +R @@) '

    def __init__(self):
        self.startsrc = None
        self.linessrc = None
        self.starttgt = None
        self.linestgt = None
        self.invalid = False
        self.text = []


class Patch(object):
    __doc__ = ' Patch for a single file '

    def __init__(self):
        self.source = None
        self.target = None
        self.hunks = []
        self.hunkends = []
        self.header = []
        self.type = None


class PatchSet(object):

    def __init__(self, stream=None):
        self.name = None
        self.items = []
        self.type = None
        if stream:
            self.parse(stream)

    def __len__(self):
        return len(self.items)

    def parse(self, stream):
        """parse unified diff return True on success"""
        lineends = dict(lf=0, crlf=0, cr=0)
        nexthunkno = 0
        p = None
        hunk = None
        hunkactual = dict(linessrc=None, linestgt=None)

        class wrapumerate(enumerate):
            __doc__ = 'Enumerate wrapper that uses boolean end of stream status instead of\n            StopIteration exception, and properties to access line information.\n            '

            def __init__(self, *args, **kwargs):
                self._exhausted = False
                self._lineno = False
                self._line = False

            def next(self):
                """Try to read the next line and return True if it is available,
                   False if end of stream is reached."""
                if self._exhausted:
                    return False
                try:
                    self._lineno, self._line = super(wrapumerate, self).next()
                except StopIteration:
                    self._exhausted = True
                    self._line = False
                    return False

                return True

            @property
            def is_empty(self):
                return self._exhausted

            @property
            def line(self):
                return self._line

            @property
            def lineno(self):
                return self._lineno

        headscan = True
        filenames = False
        hunkhead = False
        hunkbody = False
        hunkskip = False
        hunkparsed = False
        re_hunk_start = re.compile('^@@ -(\\d+)(,(\\d+))? \\+(\\d+)(,(\\d+))?')
        errors = 0
        header = []
        srcname = None
        tgtname = None
        fe = wrapumerate(stream)
        while fe.next():
            if hunkparsed:
                hunkparsed = False
                if re_hunk_start.match(fe.line):
                    hunkhead = True
                else:
                    if fe.line.startswith('--- '):
                        filenames = True
                    else:
                        headscan = True
            if headscan:
                while not fe.is_empty and not fe.line.startswith('--- '):
                    header.append(fe.line)
                    fe.next()

                if fe.is_empty:
                    if p == None:
                        errors += 1
                        warning('warning: no patch data is found')
                    else:
                        info('%d unparsed bytes left at the end of stream' % len(''.join(header)))
                    continue
                headscan = False
                filenames = True
            line = fe.line
            lineno = fe.lineno
            if hunkbody:
                pass
            if re.match('^[- \\+\\\\]', line):
                if line.endswith('\r\n'):
                    p.hunkends['crlf'] += 1
                else:
                    if line.endswith('\n'):
                        p.hunkends['lf'] += 1
                    else:
                        if line.endswith('\r'):
                            p.hunkends['cr'] += 1
                        if line.startswith('-'):
                            hunkactual['linessrc'] += 1
                        else:
                            if line.startswith('+'):
                                hunkactual['linestgt'] += 1
                            elif not line.startswith('\\'):
                                hunkactual['linessrc'] += 1
                                hunkactual['linestgt'] += 1
                hunk.text.append(line)
            else:
                warning('invalid hunk no.%d at %d for target file %s' % (
                 nexthunkno, lineno + 1, p.target))
                hunk.invalid = True
                p.hunks.append(hunk)
                errors += 1
                hunkbody = False
                hunkskip = True
            if hunkactual['linessrc'] > hunk.linessrc or hunkactual['linestgt'] > hunk.linestgt:
                warning('extra lines for hunk no.%d at %d for target %s' % (
                 nexthunkno, lineno + 1, p.target))
                hunk.invalid = True
                p.hunks.append(hunk)
                errors += 1
                hunkbody = False
                hunkskip = True
            elif hunk.linessrc == hunkactual['linessrc']:
                if hunk.linestgt == hunkactual['linestgt']:
                    p.hunks.append(hunk)
                    hunkbody = False
                    hunkparsed = True
                    ends = p.hunkends
                    if (ends['cr'] != 0) + (ends['crlf'] != 0) + (ends['lf'] != 0) > 1:
                        warning('inconsistent line ends in patch hunks for %s' % p.source)
                    if debugmode:
                        debuglines = dict(ends)
                        debuglines.update(file=p.target, hunk=nexthunkno)
                        debug('crlf: %(crlf)d  lf: %(lf)d  cr: %(cr)d\t - file: %(file)s hunk: %(hunk)d' % debuglines)
                    continue
            if hunkskip:
                if re_hunk_start.match(line):
                    hunkskip = False
                    hunkhead = True
            else:
                if line.startswith('--- '):
                    hunkskip = False
                    filenames = True
                    if debugmode:
                        if len(self.items) > 0:
                            debug('- %2d hunks for %s' % (len(p.hunks), p.source))
                if filenames:
                    if line.startswith('--- '):
                        if srcname != None:
                            warning('skipping false patch for %s' % srcname)
                            srcname = None
                        re_filename = '^--- ([^\t]+)'
                        match = re.match(re_filename, line)
                        if match:
                            srcname = match.group(1).strip()
                        else:
                            warning('skipping invalid filename at line %d' % lineno)
                            errors += 1
                            filenames = False
                            headscan = True
                    else:
                        if not line.startswith('+++ '):
                            if srcname != None:
                                warning('skipping invalid patch with no target for %s' % srcname)
                                errors += 1
                                srcname = None
                            else:
                                warning('skipping invalid target patch')
                            filenames = False
                            headscan = True
                        else:
                            if tgtname != None:
                                warning('skipping invalid patch - double target at line %d' % lineno)
                                errors += 1
                                srcname = None
                                tgtname = None
                                filenames = False
                                headscan = True
                            else:
                                re_filename = '^\\+\\+\\+ ([^\t]+)'
                                match = re.match(re_filename, line)
                                if not match:
                                    warning('skipping invalid patch - no target filename at line %d' % lineno)
                                    errors += 1
                                    srcname = None
                                    filenames = False
                                    headscan = True
                                else:
                                    if p:
                                        self.items.append(p)
                                    p = Patch()
                                    p.source = srcname
                                    srcname = None
                                    p.target = match.group(1).strip()
                                    p.header = header
                                    header = []
                                    filenames = False
                                    hunkhead = True
                                    nexthunkno = 0
                                    p.hunkends = lineends.copy()
                                    continue
            if hunkhead:
                match = re.match('^@@ -(\\d+)(,(\\d+))? \\+(\\d+)(,(\\d+))?', line)
                if not match:
                    if not p.hunks:
                        warning('skipping invalid patch with no hunks for file %s' % p.source)
                        errors += 1
                        hunkhead = False
                        headscan = True
                        continue
                    else:
                        hunkhead = False
                        headscan = True
                else:
                    hunk = Hunk()
                    hunk.startsrc = int(match.group(1))
                    hunk.linessrc = 1
                    if match.group(3):
                        hunk.linessrc = int(match.group(3))
                    hunk.starttgt = int(match.group(4))
                    hunk.linestgt = 1
                    if match.group(6):
                        hunk.linestgt = int(match.group(6))
                    hunk.invalid = False
                    hunk.text = []
                    hunkactual['linessrc'] = hunkactual['linestgt'] = 0
                    hunkhead = False
                    hunkbody = True
                    nexthunkno += 1
                    continue
                    continue

        self.items.append(p)
        if not hunkparsed:
            if hunkskip:
                warning('warning: finished with warnings, some hunks may be invalid')
            else:
                if headscan:
                    if len(self.items) == 0:
                        warning('error: no patch data found!')
                else:
                    warning('error: patch stream is incomplete!')
                    errors += 1
        if debugmode:
            if len(self.items) > 0:
                debug('- %2d hunks for %s' % (len(p.hunks), p.source))
        debug('total files: %d  total hunks: %d' % (len(self.items),
         sum(len(p.hunks) for p in self.items)))
        for idx, p in enumerate(self.items):
            self.items[idx].type = self._detect_type(p)

        types = set([p.type for p in self.items])
        if len(types) > 1:
            self.type = MIXED
        else:
            self.type = types.pop()
        if not self._normalize_filenames():
            errors += 1
        return errors == 0

    def _detect_type(self, p):
        """ detect and return type for the specified Patch object
            analyzes header and filenames info

            NOTE: must be run before filenames are normalized
        """
        if len(p.header) > 1 and p.header[(-2)].startswith('Index: ') and p.header[(-1)].startswith('=' * 67):
            return SVN
        for idx in reversed(range(len(p.header))):
            if p.header[idx].startswith('diff --git'):
                break

        if len(p.header) > 1:
            if re.match('diff --git a/[\\w/.]+ b/[\\w/.]+', p.header[idx]):
                if re.match('index \\w{7}..\\w{7} \\d{6}', p.header[(idx + 1)]):
                    if p.source.startswith('a/') and p.target.startswith('b/'):
                        return GIT
        if len(p.header) > 0:
            if re.match('diff -r \\w{12} .*', p.header[(-1)]) and (p.source.startswith('a/') or p.source == '/dev/null') and (p.target.startswith('b/') or p.target == '/dev/null'):
                return HG
        return PLAIN

    def _normalize_filenames(self):
        """ sanitize filenames, normalizing paths
            TODO think about using forward slashes for crossplatform issues
                 (diff/patch were born as a unix utility after all)
            return True on success
        """
        errors = 0
        for i, p in enumerate(self.items):
            if p.type in (HG, GIT):
                debug('stripping a/ and b/ prefixes')
                if p.source != '/dev/null':
                    if not p.source.startswith('a/'):
                        warning('invalid source filename')
                    else:
                        p.source = p.source[2:]
                if p.target != '/dev/null':
                    if not p.target.startswith('b/'):
                        warning('invalid target filename')
                    else:
                        p.target = p.target[2:]
                p.source = normpath(p.source)
                p.target = normpath(p.target)
                if p.source.startswith('..' + os.sep):
                    warning('error: stripping parent path for source file patch no.%d' % (i + 1))
                    errors += 1
                    while p.source.startswith('..' + os.sep):
                        p.source = p.source.partition(os.sep)[2]

                if p.target.startswith('..' + os.sep):
                    warning('error: stripping parent path for target file patch no.%d' % (i + 1))
                    errors += 1
                    while p.target.startswith('..' + os.sep):
                        p.target = p.target.partition(os.sep)[2]

                if isabs(p.source) or isabs(p.target):
                    errors += 1
                    warning('error: absolute paths are not allowed for file patch no.%d' % (i + 1))
                    if isabs(p.source):
                        p.source = p.source.partition(os.sep)[2]
                    if isabs(p.target):
                        p.target = p.target.partition(os.sep)[2]
                    self.items[i].source = p.source
                    self.items[i].target = p.target

        return errors == 0

    def diffstat(self):
        """ calculate diffstat and return as a string
            Notes:
              - original diffstat ouputs target filename
              - single + or - shouldn't escape histogram
        """
        names = []
        insert = []
        delete = []
        namelen = 0
        maxdiff = 0
        for patch in self.items:
            i, d = (0, 0)
            for hunk in patch.hunks:
                for line in hunk.text:
                    if line.startswith('+'):
                        i += 1
                    elif line.startswith('-'):
                        d += 1
                        continue

            names.append(patch.target)
            insert.append(i)
            delete.append(d)
            namelen = max(namelen, len(patch.target))
            maxdiff = max(maxdiff, i + d)

        output = ''
        statlen = len(str(maxdiff))
        for i, n in enumerate(names):
            format = ' %-' + str(namelen) + 's | %' + str(statlen) + 's %s\n'
            hist = ''
            width = len(format % ('', '', ''))
            histwidth = max(2, 80 - width)
            if maxdiff < histwidth:
                hist = '+' * insert[i] + '-' * delete[i]
            else:
                iratio = float(insert[i]) / maxdiff * histwidth
                dratio = float(delete[i]) / maxdiff * histwidth
                iwidth = 1 if 0 < iratio < 1 else int(iratio)
                dwidth = 1 if 0 < dratio < 1 else int(dratio)
                hist = '+' * int(iwidth) + '-' * int(dwidth)
            output += format % (names[i], insert[i] + delete[i], hist)

        output += ' %d files changed, %d insertions(+), %d deletions(-)' % (
         len(names), sum(insert), sum(delete))
        return output

    def apply(self):
        """ apply parsed patch
            return True on success
        """
        total = len(self.items)
        errors = 0
        for i, p in enumerate(self.items):
            f2patch = p.source
            if not exists(f2patch):
                f2patch = p.target
                if not exists(f2patch):
                    warning('source/target file does not exist\n--- %s\n+++ %s' % (
                     p.source, f2patch))
                    errors += 1
                    continue
                if not isfile(f2patch):
                    warning('not a file - %s' % f2patch)
                    errors += 1
                    continue
                filename = f2patch
                debug('processing %d/%d:\t %s' % (i + 1, total, filename))
                f2fp = open(filename)
                hunkno = 0
                hunk = p.hunks[hunkno]
                hunkfind = []
                hunkreplace = []
                validhunks = 0
                canpatch = False
                for lineno, line in enumerate(f2fp):
                    if lineno + 1 < hunk.startsrc:
                        continue
                    elif lineno + 1 == hunk.startsrc:
                        hunkfind = [x[1:].rstrip('\r\n') for x in hunk.text if x[0] in ' -']
                        hunkreplace = [x[1:].rstrip('\r\n') for x in hunk.text if x[0] in ' +']
                        hunklineno = 0
                    if lineno + 1 < hunk.startsrc + len(hunkfind) - 1:
                        if line.rstrip('\r\n') == hunkfind[hunklineno]:
                            hunklineno += 1
                        else:
                            info('file %d/%d:\t %s' % (i + 1, total, filename))
                            info(" hunk no.%d doesn't match source file at line %d" % (
                             hunkno + 1, lineno))
                            info('  expected: %s' % hunkfind[hunklineno])
                            info('  actual  : %s' % line.rstrip('\r\n'))
                            hunkno += 1
                            if hunkno < len(p.hunks):
                                hunk = p.hunks[hunkno]
                                continue
                            else:
                                break
                    if lineno + 1 == hunk.startsrc + len(hunkfind) - 1:
                        debug(' hunk no.%d for file %s  -- is ready to be patched' % (
                         hunkno + 1, filename))
                        hunkno += 1
                        validhunks += 1
                        if hunkno < len(p.hunks):
                            hunk = p.hunks[hunkno]
                        else:
                            if validhunks == len(p.hunks):
                                canpatch = True
                                break
                            else:
                                continue
                else:
                    if hunkno < len(p.hunks):
                        warning('premature end of source file %s at hunk %d' % (
                         filename, hunkno + 1))
                        errors += 1

                f2fp.close()
                if validhunks < len(p.hunks):
                    if self._match_file_hunks(filename, p.hunks):
                        warning('already patched  %s' % filename)
                    else:
                        warning('source file is different - %s' % filename)
                        errors += 1
                if canpatch:
                    backupname = filename + '.orig'
                    if exists(backupname):
                        warning("can't backup original file to %s - aborting" % backupname)
                    else:
                        import shutil
                        shutil.move(filename, backupname)
                        if self.write_hunks(backupname, filename, p.hunks):
                            info('successfully patched %d/%d:\t %s' % (i + 1, total, filename))
                            os.unlink(backupname)
                        else:
                            errors += 1
                            warning('error patching file %s' % filename)
                            shutil.copy(filename, filename + '.invalid')
                            warning('invalid version is saved to %s' % filename + '.invalid')
                            shutil.move(backupname, filename)
                            continue

        return errors == 0

    def can_patch(self, filename):
        """ Check if specified filename can be patched. Returns None if file can
        not be found among source filenames. False if patch can not be applied
        clearly. True otherwise.

        :returns: True, False or None
        """
        filename = abspath(filename)
        for p in self.items:
            if filename == abspath(p.source):
                return self._match_file_hunks(filename, p.hunks)

    def _match_file_hunks(self, filepath, hunks):
        matched = True
        fp = open(abspath(filepath))

        class NoMatch(Exception):
            pass

        lineno = 1
        line = fp.readline()
        try:
            for hno, h in enumerate(hunks):
                while lineno < h.starttgt:
                    if not len(line):
                        debug('check failed - premature eof before hunk: %d' % (hno + 1))
                        raise NoMatch
                    line = fp.readline()
                    lineno += 1

                for hline in h.text:
                    if hline.startswith('-'):
                        continue
                    if not len(line):
                        debug('check failed - premature eof on hunk: %d' % (hno + 1))
                        raise NoMatch
                    if line.rstrip('\r\n') != hline[1:].rstrip('\r\n'):
                        debug('file is not patched - failed hunk: %d' % (hno + 1))
                        raise NoMatch
                    line = fp.readline()
                    lineno += 1

        except NoMatch:
            matched = False

        fp.close()
        return matched

    def patch_stream(self, instream, hunks):
        """ Generator that yields stream patched with hunks iterable

            Converts lineends in hunk lines to the best suitable format
            autodetected from input
        """
        hunks = iter(hunks)
        srclineno = 1
        lineends = {'\n': 0,  '\r\n': 0,  '\r': 0}

        def get_line():
            """
            local utility function - return line from source stream
            collecting line end statistics on the way
            """
            line = instream.readline()
            if line.endswith('\r\n'):
                lineends['\r\n'] += 1
            else:
                if line.endswith('\n'):
                    lineends['\n'] += 1
                elif line.endswith('\r'):
                    lineends['\r'] += 1
            return line

        for hno, h in enumerate(hunks):
            debug('hunk %d' % (hno + 1))
            while srclineno < h.startsrc:
                yield get_line()
                srclineno += 1

            for hline in h.text:
                if hline.startswith('-') or hline.startswith('\\'):
                    get_line()
                    srclineno += 1
                    continue
                else:
                    if not hline.startswith('+'):
                        get_line()
                        srclineno += 1
                    line2write = hline[1:]
                    if sum([bool(lineends[x]) for x in lineends]) == 1:
                        newline = [x for x in lineends if lineends[x] != 0][0]
                        yield line2write.rstrip('\r\n') + newline
                    else:
                        yield line2write

        for line in instream:
            yield line

    def write_hunks(self, srcname, tgtname, hunks):
        src = open(srcname, 'rb')
        tgt = open(tgtname, 'wb')
        debug('processing target file %s' % tgtname)
        tgt.writelines(self.patch_stream(src, hunks))
        tgt.close()
        src.close()
        return True


if __name__ == '__main__':
    from optparse import OptionParser
    from os.path import exists
    import sys
    opt = OptionParser(usage='1. %prog [options] unified.diff\n       2. %prog [options] http://host/patch\n       3. %prog [options] -- < unified.diff', version='python-patch %s' % __version__)
    opt.add_option('-q', '--quiet', action='store_const', dest='verbosity', const=0, help='print only warnings and errors', default=1)
    opt.add_option('-v', '--verbose', action='store_const', dest='verbosity', const=2, help='be verbose')
    opt.add_option('--diffstat', action='store_true', dest='diffstat', help='print diffstat and exit')
    opt.add_option('--debug', action='store_true', dest='debugmode', help='debug mode')
    options, args = opt.parse_args()
    if not args and sys.argv[-1:] != ['--']:
        opt.print_version()
        opt.print_help()
        sys.exit()
    readstdin = sys.argv[-1:] == ['--'] and not args
    debugmode = options.debugmode
    verbosity_levels = {0: logging.WARNING,  1: logging.INFO,  2: logging.DEBUG}
    loglevel = verbosity_levels[options.verbosity]
    logformat = '%(message)s'
    if debugmode:
        loglevel = logging.DEBUG
        logformat = '%(levelname)8s %(message)s'
    logger.setLevel(loglevel)
    loghandler = logging.StreamHandler()
    loghandler.setFormatter(logging.Formatter(logformat))
    logger.addHandler(loghandler)
    if readstdin:
        patch = PatchSet(sys.stdin)
    else:
        patchfile = args[0]
        urltest = patchfile.split(':')[0]
        if ':' in patchfile and urltest.isalpha() and len(urltest) > 1:
            patch = fromurl(patchfile)
        else:
            if not exists(patchfile) or not isfile(patchfile):
                sys.exit('patch file does not exist - %s' % patchfile)
            patch = fromfile(patchfile)
        if options.diffstat:
            print(patch.diffstat())
            sys.exit(0)
    patch.apply() or sys.exit(-1)