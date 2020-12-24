# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/py/py/_path/svnurl.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 14715 bytes
"""
module defining a subversion path object based on the external
command 'svn'. This modules aims to work with svn 1.3 and higher
but might also interact well with earlier versions.
"""
import os, sys, time, re, py
from py import path, process
from py._path import common
from py._path import svnwc as svncommon
from py._path.cacheutil import BuildcostAccessCache, AgingCache
DEBUG = False

class SvnCommandPath(svncommon.SvnPathBase):
    __doc__ = ' path implementation that offers access to (possibly remote) subversion\n    repositories. '
    _lsrevcache = BuildcostAccessCache(maxentries=128)
    _lsnorevcache = AgingCache(maxentries=1000, maxseconds=60.0)

    def __new__(cls, path, rev=None, auth=None):
        self = object.__new__(cls)
        if isinstance(path, cls):
            rev = path.rev
            auth = path.auth
            path = path.strpath
        svncommon.checkbadchars(path)
        path = path.rstrip('/')
        self.strpath = path
        self.rev = rev
        self.auth = auth
        return self

    def __repr__(self):
        if self.rev == -1:
            return 'svnurl(%r)' % self.strpath
        else:
            return 'svnurl(%r, %r)' % (self.strpath, self.rev)

    def _svnwithrev(self, cmd, *args):
        """ execute an svn command, append our own url and revision """
        if self.rev is None:
            return (self._svnwrite)(cmd, *args)
        else:
            args = [
             '-r', self.rev] + list(args)
            return (self._svnwrite)(cmd, *args)

    def _svnwrite(self, cmd, *args):
        """ execute an svn command, append our own url """
        l = [
         'svn %s' % cmd]
        args = ['"%s"' % self._escape(item) for item in args]
        l.extend(args)
        l.append('"%s"' % self._encodedurl())
        string = ' '.join(l)
        if DEBUG:
            print('execing %s' % string)
        out = self._svncmdexecauth(string)
        return out

    def _svncmdexecauth(self, cmd):
        """ execute an svn command 'as is' """
        cmd = svncommon.fixlocale() + cmd
        if self.auth is not None:
            cmd += ' ' + self.auth.makecmdoptions()
        return self._cmdexec(cmd)

    def _cmdexec(self, cmd):
        try:
            out = process.cmdexec(cmd)
        except py.process.cmdexec.Error:
            e = sys.exc_info()[1]
            if e.err.find('File Exists') != -1 or e.err.find('File already exists') != -1:
                raise py.error.EEXIST(self)
            raise

        return out

    def _svnpopenauth(self, cmd):
        """ execute an svn command, return a pipe for reading stdin """
        cmd = svncommon.fixlocale() + cmd
        if self.auth is not None:
            cmd += ' ' + self.auth.makecmdoptions()
        return self._popen(cmd)

    def _popen(self, cmd):
        return os.popen(cmd)

    def _encodedurl(self):
        return self._escape(self.strpath)

    def _norev_delentry(self, path):
        auth = self.auth and self.auth.makecmdoptions() or None
        self._lsnorevcache.delentry((str(path), auth))

    def open(self, mode='r'):
        """ return an opened file with the given mode. """
        if mode not in ('r', 'rU'):
            raise ValueError('mode %r not supported' % (mode,))
        elif not self.check(file=1):
            raise AssertionError
        if self.rev is None:
            return self._svnpopenauth('svn cat "%s"' % (
             self._escape(self.strpath),))
        else:
            return self._svnpopenauth('svn cat -r %s "%s"' % (
             self.rev, self._escape(self.strpath)))

    def dirpath(self, *args, **kwargs):
        """ return the directory path of the current path joined
            with any given path arguments.
        """
        l = self.strpath.split(self.sep)
        if len(l) < 4:
            raise py.error.EINVAL(self, 'base is not valid')
        else:
            if len(l) == 4:
                return (self.join)(*args, **kwargs)
            else:
                return (self.new(basename='').join)(*args, **kwargs)

    def mkdir(self, *args, **kwargs):
        """ create & return the directory joined with args.
        pass a 'msg' keyword argument to set the commit message.
        """
        commit_msg = kwargs.get('msg', 'mkdir by py lib invocation')
        createpath = (self.join)(*args)
        createpath._svnwrite('mkdir', '-m', commit_msg)
        self._norev_delentry(createpath.dirpath())
        return createpath

    def copy(self, target, msg='copied by py lib invocation'):
        """ copy path to target with checkin message msg."""
        if getattr(target, 'rev', None) is not None:
            raise py.error.EINVAL(target, 'revisions are immutable')
        self._svncmdexecauth('svn copy -m "%s" "%s" "%s"' % (msg,
         self._escape(self), self._escape(target)))
        self._norev_delentry(target.dirpath())

    def rename(self, target, msg='renamed by py lib invocation'):
        """ rename this path to target with checkin message msg. """
        if getattr(self, 'rev', None) is not None:
            raise py.error.EINVAL(self, 'revisions are immutable')
        self._svncmdexecauth('svn move -m "%s" --force "%s" "%s"' % (
         msg, self._escape(self), self._escape(target)))
        self._norev_delentry(self.dirpath())
        self._norev_delentry(self)

    def remove(self, rec=1, msg='removed by py lib invocation'):
        """ remove a file or directory (or a directory tree if rec=1) with
checkin message msg."""
        if self.rev is not None:
            raise py.error.EINVAL(self, 'revisions are immutable')
        self._svncmdexecauth('svn rm -m "%s" "%s"' % (msg, self._escape(self)))
        self._norev_delentry(self.dirpath())

    def export(self, topath):
        """ export to a local path

            topath should not exist prior to calling this, returns a
            py.path.local instance
        """
        topath = py.path.local(topath)
        args = ['"%s"' % (self._escape(self),),
         '"%s"' % (self._escape(topath),)]
        if self.rev is not None:
            args = [
             '-r', str(self.rev)] + args
        self._svncmdexecauth('svn export %s' % (' '.join(args),))
        return topath

    def ensure--- This code section failed: ---

 L. 177         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'rev'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  '3 positional arguments'
               10  LOAD_CONST               None
               12  COMPARE_OP               is-not
               14  POP_JUMP_IF_FALSE    30  'to 30'

 L. 178        16  LOAD_GLOBAL              py
               18  LOAD_ATTR                error
               20  LOAD_ATTR                EINVAL
               22  LOAD_FAST                'self'
               24  LOAD_STR                 'revisions are immutable'
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  RAISE_VARARGS_1       1  'exception'
             30_0  COME_FROM            14  '14'

 L. 179        30  LOAD_FAST                'self'
               32  LOAD_ATTR                join
               34  LOAD_FAST                'args'
               36  CALL_FUNCTION_EX      0  'positional arguments only'
               38  STORE_FAST               'target'

 L. 180        40  LOAD_FAST                'kwargs'
               42  LOAD_ATTR                get
               44  LOAD_STR                 'dir'
               46  LOAD_CONST               0
               48  CALL_FUNCTION_2       2  '2 positional arguments'
               50  STORE_FAST               'dir'

 L. 181        52  SETUP_LOOP           98  'to 98'
               54  LOAD_FAST                'target'
               56  LOAD_ATTR                parts
               58  LOAD_CONST               True
               60  LOAD_CONST               ('reverse',)
               62  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               64  GET_ITER         
               66  FOR_ITER             82  'to 82'
               68  STORE_FAST               'x'

 L. 182        70  LOAD_FAST                'x'
               72  LOAD_ATTR                check
               74  CALL_FUNCTION_0       0  '0 positional arguments'
               76  POP_JUMP_IF_FALSE    66  'to 66'

 L. 183        78  BREAK_LOOP       
             80_0  COME_FROM            76  '76'
               80  JUMP_BACK            66  'to 66'
               82  POP_BLOCK        

 L. 185        84  LOAD_GLOBAL              py
               86  LOAD_ATTR                error
               88  LOAD_ATTR                ENOENT
               90  LOAD_FAST                'target'
               92  LOAD_STR                 'has not any valid base!'
               94  CALL_FUNCTION_2       2  '2 positional arguments'
               96  RAISE_VARARGS_1       1  'exception'
             98_0  COME_FROM_LOOP       52  '52'

 L. 186        98  LOAD_FAST                'x'
              100  LOAD_FAST                'target'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   150  'to 150'

 L. 187       106  LOAD_FAST                'x'
              108  LOAD_ATTR                check
              110  LOAD_FAST                'dir'
              112  LOAD_CONST               ('dir',)
              114  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              116  POP_JUMP_IF_TRUE    146  'to 146'

 L. 188       118  LOAD_FAST                'dir'
              120  POP_JUMP_IF_FALSE   134  'to 134'
              122  LOAD_GLOBAL              py
              124  LOAD_ATTR                error
              126  LOAD_ATTR                ENOTDIR
              128  LOAD_FAST                'x'
              130  CALL_FUNCTION_1       1  '1 positional argument'
            132_0  COME_FROM           120  '120'
              132  JUMP_IF_TRUE_OR_POP   144  'to 144'
              134  LOAD_GLOBAL              py
              136  LOAD_ATTR                error
              138  LOAD_ATTR                EISDIR
              140  LOAD_FAST                'x'
              142  CALL_FUNCTION_1       1  '1 positional argument'
            144_0  COME_FROM           132  '132'
              144  RAISE_VARARGS_1       1  'exception'
            146_0  COME_FROM           116  '116'

 L. 189       146  LOAD_FAST                'x'
              148  RETURN_END_IF    
            150_0  COME_FROM           104  '104'

 L. 190       150  LOAD_FAST                'target'
              152  LOAD_ATTR                relto
              154  LOAD_FAST                'x'
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  STORE_FAST               'tocreate'

 L. 191       160  LOAD_FAST                'tocreate'
              162  LOAD_ATTR                split
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                sep
              168  LOAD_CONST               1
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  LOAD_CONST               0
              174  BINARY_SUBSCR    
              176  STORE_FAST               'basename'

 L. 192       178  LOAD_GLOBAL              py
              180  LOAD_ATTR                path
              182  LOAD_ATTR                local
              184  LOAD_ATTR                mkdtemp
              186  CALL_FUNCTION_0       0  '0 positional arguments'
              188  STORE_FAST               'tempdir'

 L. 193       190  SETUP_FINALLY       276  'to 276'

 L. 194       192  LOAD_FAST                'tempdir'
              194  LOAD_ATTR                ensure
              196  LOAD_FAST                'tocreate'
              198  LOAD_FAST                'dir'
              200  LOAD_CONST               ('dir',)
              202  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              204  POP_TOP          

 L. 195       206  LOAD_STR                 'svn import -m "%s" "%s" "%s"'

 L. 196       208  LOAD_STR                 'ensure %s'
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                _escape
              214  LOAD_FAST                'tocreate'
              216  CALL_FUNCTION_1       1  '1 positional argument'
              218  BINARY_MODULO    

 L. 197       220  LOAD_FAST                'self'
              222  LOAD_ATTR                _escape
              224  LOAD_FAST                'tempdir'
              226  LOAD_ATTR                join
              228  LOAD_FAST                'basename'
              230  CALL_FUNCTION_1       1  '1 positional argument'
              232  CALL_FUNCTION_1       1  '1 positional argument'

 L. 198       234  LOAD_FAST                'x'
              236  LOAD_ATTR                join
              238  LOAD_FAST                'basename'
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  LOAD_ATTR                _encodedurl
              244  CALL_FUNCTION_0       0  '0 positional arguments'
              246  BUILD_TUPLE_3         3 
              248  BINARY_MODULO    
              250  STORE_FAST               'cmd'

 L. 199       252  LOAD_FAST                'self'
              254  LOAD_ATTR                _svncmdexecauth
              256  LOAD_FAST                'cmd'
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  POP_TOP          

 L. 200       262  LOAD_FAST                'self'
              264  LOAD_ATTR                _norev_delentry
              266  LOAD_FAST                'x'
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  POP_TOP          
              272  POP_BLOCK        
              274  LOAD_CONST               None
            276_0  COME_FROM_FINALLY   190  '190'

 L. 202       276  LOAD_FAST                'tempdir'
              278  LOAD_ATTR                remove
              280  CALL_FUNCTION_0       0  '0 positional arguments'
              282  POP_TOP          
              284  END_FINALLY      

 L. 203       286  LOAD_FAST                'target'
              288  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RAISE_VARARGS_1' instruction at offset 144

    def _propget(self, name):
        res = self._svnwithrev('propget', name)
        return res[:-1]

    def _proplist(self):
        res = self._svnwithrev('proplist')
        lines = res.split('\n')
        lines = [x.strip() for x in lines[1:]]
        return svncommon.PropListDict(self, lines)

    def info(self):
        """ return an Info structure with svn-provided information. """
        parent = self.dirpath()
        nameinfo_seq = parent._listdir_nameinfo()
        bn = self.basename
        for name, info in nameinfo_seq:
            if name == bn:
                return info

        raise py.error.ENOENT(self)

    def _listdir_nameinfo(self):
        """ return sequence of name-info directory entries of self """

        def builder():
            try:
                res = self._svnwithrev('ls', '-v')
            except process.cmdexec.Error:
                e = sys.exc_info()[1]
                if e.err.find('non-existent in that revision') != -1:
                    raise py.error.ENOENT(self, e.err)
                else:
                    if e.err.find('E200009:') != -1:
                        raise py.error.ENOENT(self, e.err)
                    else:
                        if e.err.find('File not found') != -1:
                            raise py.error.ENOENT(self, e.err)
                        else:
                            if e.err.find('not part of a repository') != -1:
                                raise py.error.ENOENT(self, e.err)
                            else:
                                if e.err.find('Unable to open') != -1:
                                    raise py.error.ENOENT(self, e.err)
                                else:
                                    if e.err.lower().find('method not allowed') != -1:
                                        raise py.error.EACCES(self, e.err)
                raise py.error.Error(e.err)

            lines = res.split('\n')
            nameinfo_seq = []
            for lsline in lines:
                if lsline:
                    info = InfoSvnCommand(lsline)
                    if info._name != '.':
                        nameinfo_seq.append((info._name, info))

            nameinfo_seq.sort()
            return nameinfo_seq

        auth = self.auth and self.auth.makecmdoptions() or None
        if self.rev is not None:
            return self._lsrevcache.getorbuild((self.strpath, self.rev, auth), builder)
        else:
            return self._lsnorevcache.getorbuild((self.strpath, auth), builder)

    def listdir(self, fil=None, sort=None):
        """ list directory contents, possibly filter by the given fil func
            and possibly sorted.
        """
        if isinstance(fil, str):
            fil = common.FNMatcher(fil)
        else:
            nameinfo_seq = self._listdir_nameinfo()
            if len(nameinfo_seq) == 1:
                name, info = nameinfo_seq[0]
                if name == self.basename:
                    if info.kind == 'file':
                        raise py.error.ENOTDIR(self)
            paths = [self.join(name) for name, info in nameinfo_seq]
            if fil:
                paths = [x for x in paths if fil(x)]
        self._sortlist(paths, sort)
        return paths

    def log(self, rev_start=None, rev_end=1, verbose=False):
        """ return a list of LogEntry instances for this path.
rev_start is the starting revision (defaulting to the first one).
rev_end is the last revision (defaulting to HEAD).
if verbose is True, then the LogEntry instances also know which files changed.
"""
        if not self.check():
            raise AssertionError
        else:
            rev_start = rev_start is None and 'HEAD' or rev_start
            rev_end = rev_end is None and 'HEAD' or rev_end
            if rev_start == 'HEAD':
                if rev_end == 1:
                    rev_opt = ''
            rev_opt = '-r %s:%s' % (rev_start, rev_end)
        verbose_opt = verbose and '-v' or ''
        xmlpipe = self._svnpopenauth('svn log --xml %s %s "%s"' % (
         rev_opt, verbose_opt, self.strpath))
        from xml.dom import minidom
        tree = minidom.parse(xmlpipe)
        result = []
        for logentry in filter(None, tree.firstChild.childNodes):
            if logentry.nodeType == logentry.ELEMENT_NODE:
                result.append(svncommon.LogEntry(logentry))

        return result


class InfoSvnCommand:
    lspattern = re.compile('^ *(?P<rev>\\d+) +(?P<author>.+?) +(0? *(?P<size>\\d+))? *(?P<date>\\w+ +\\d{2} +[\\d:]+) +(?P<file>.*)$')

    def __init__(self, line):
        match = self.lspattern.match(line)
        data = match.groupdict()
        self._name = data['file']
        if self._name[(-1)] == '/':
            self._name = self._name[:-1]
            self.kind = 'dir'
        else:
            self.kind = 'file'
        self.created_rev = int(data['rev'])
        self.last_author = data['author']
        self.size = data['size'] and int(data['size']) or 0
        self.mtime = parse_time_with_missing_year(data['date'])
        self.time = self.mtime * 1000000

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def parse_time_with_missing_year(timestr):
    """ analyze the time part from a single line of "svn ls -v"
    the svn output doesn't show the year makes the 'timestr'
    ambigous.
    """
    import calendar
    t_now = time.gmtime()
    tparts = timestr.split()
    month = time.strptime(tparts.pop(0), '%b')[1]
    day = time.strptime(tparts.pop(0), '%d')[2]
    last = tparts.pop(0)
    try:
        if ':' in last:
            raise ValueError()
        year = time.strptime(last, '%Y')[0]
        hour = minute = 0
    except ValueError:
        hour, minute = time.strptime(last, '%H:%M')[3:5]
        year = t_now[0]
        t_result = (
         year, month, day, hour, minute, 0, 0, 0, 0)
        if t_result > t_now:
            year -= 1

    t_result = (
     year, month, day, hour, minute, 0, 0, 0, 0)
    return calendar.timegm(t_result)


class PathEntry:

    def __init__(self, ppart):
        self.strpath = ppart.firstChild.nodeValue.encode('UTF-8')
        self.action = ppart.getAttribute('action').encode('UTF-8')
        if self.action == 'A':
            self.copyfrom_path = ppart.getAttribute('copyfrom-path').encode('UTF-8')
            if self.copyfrom_path:
                self.copyfrom_rev = int(ppart.getAttribute('copyfrom-rev'))