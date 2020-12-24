# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/py/py/_path/svnurl.py
# Compiled at: 2019-02-14 00:35:48
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
    """ path implementation that offers access to (possibly remote) subversion
    repositories. """
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
            return self._svnwrite(cmd, *args)
        else:
            args = [
             '-r', self.rev] + list(args)
            return self._svnwrite(cmd, *args)
            return

    def _svnwrite(self, cmd, *args):
        """ execute an svn command, append our own url """
        l = ['svn %s' % cmd]
        args = [ '"%s"' % self._escape(item) for item in args ]
        l.extend(args)
        l.append('"%s"' % self._encodedurl())
        string = (' ').join(l)
        if DEBUG:
            print 'execing %s' % string
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
        return

    def open(self, mode='r'):
        """ return an opened file with the given mode. """
        if mode not in ('r', 'rU'):
            raise ValueError('mode %r not supported' % (mode,))
        assert self.check(file=1)
        if self.rev is None:
            return self._svnpopenauth('svn cat "%s"' % (
             self._escape(self.strpath),))
        else:
            return self._svnpopenauth('svn cat -r %s "%s"' % (
             self.rev, self._escape(self.strpath)))
            return

    def dirpath(self, *args, **kwargs):
        """ return the directory path of the current path joined
            with any given path arguments.
        """
        l = self.strpath.split(self.sep)
        if len(l) < 4:
            raise py.error.EINVAL(self, 'base is not valid')
        else:
            if len(l) == 4:
                return self.join(*args, **kwargs)
            else:
                return self.new(basename='').join(*args, **kwargs)

    def mkdir(self, *args, **kwargs):
        """ create & return the directory joined with args.
        pass a 'msg' keyword argument to set the commit message.
        """
        commit_msg = kwargs.get('msg', 'mkdir by py lib invocation')
        createpath = self.join(*args)
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
        return

    def rename(self, target, msg='renamed by py lib invocation'):
        """ rename this path to target with checkin message msg. """
        if getattr(self, 'rev', None) is not None:
            raise py.error.EINVAL(self, 'revisions are immutable')
        self._svncmdexecauth('svn move -m "%s" --force "%s" "%s"' % (
         msg, self._escape(self), self._escape(target)))
        self._norev_delentry(self.dirpath())
        self._norev_delentry(self)
        return

    def remove(self, rec=1, msg='removed by py lib invocation'):
        """ remove a file or directory (or a directory tree if rec=1) with
checkin message msg."""
        if self.rev is not None:
            raise py.error.EINVAL(self, 'revisions are immutable')
        self._svncmdexecauth('svn rm -m "%s" "%s"' % (msg, self._escape(self)))
        self._norev_delentry(self.dirpath())
        return

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
        self._svncmdexecauth('svn export %s' % ((' ').join(args),))
        return topath

    def ensure--- This code section failed: ---

 L. 177         0  LOAD_GLOBAL           0  'getattr'
                3  LOAD_FAST             0  'self'
                6  LOAD_CONST               'rev'
                9  LOAD_CONST               None
               12  CALL_FUNCTION_3       3  None
               15  LOAD_CONST               None
               18  COMPARE_OP            9  is-not
               21  POP_JUMP_IF_FALSE    48  'to 48'

 L. 178        24  LOAD_GLOBAL           2  'py'
               27  LOAD_ATTR             3  'error'
               30  LOAD_ATTR             4  'EINVAL'
               33  LOAD_FAST             0  'self'
               36  LOAD_CONST               'revisions are immutable'
               39  CALL_FUNCTION_2       2  None
               42  RAISE_VARARGS_1       1  None
               45  JUMP_FORWARD          0  'to 48'
             48_0  COME_FROM            45  '45'

 L. 179        48  LOAD_FAST             0  'self'
               51  LOAD_ATTR             5  'join'
               54  LOAD_FAST             1  'args'
               57  CALL_FUNCTION_VAR_0     0  None
               60  STORE_FAST            3  'target'

 L. 180        63  LOAD_FAST             2  'kwargs'
               66  LOAD_ATTR             6  'get'
               69  LOAD_CONST               'dir'
               72  LOAD_CONST               0
               75  CALL_FUNCTION_2       2  None
               78  STORE_FAST            4  'dir'

 L. 181        81  SETUP_LOOP           63  'to 147'
               84  LOAD_FAST             3  'target'
               87  LOAD_ATTR             7  'parts'
               90  LOAD_CONST               'reverse'
               93  LOAD_GLOBAL           8  'True'
               96  CALL_FUNCTION_256   256  None
               99  GET_ITER         
              100  FOR_ITER             22  'to 125'
              103  STORE_FAST            5  'x'

 L. 182       106  LOAD_FAST             5  'x'
              109  LOAD_ATTR             9  'check'
              112  CALL_FUNCTION_0       0  None
              115  POP_JUMP_IF_FALSE   100  'to 100'

 L. 183       118  BREAK_LOOP       
              119  JUMP_BACK           100  'to 100'
              122  JUMP_BACK           100  'to 100'
              125  POP_BLOCK        

 L. 185       126  LOAD_GLOBAL           2  'py'
              129  LOAD_ATTR             3  'error'
              132  LOAD_ATTR            10  'ENOENT'
              135  LOAD_FAST             3  'target'
              138  LOAD_CONST               'has not any valid base!'
              141  CALL_FUNCTION_2       2  None
              144  RAISE_VARARGS_1       1  None
            147_0  COME_FROM            81  '81'

 L. 186       147  LOAD_FAST             5  'x'
              150  LOAD_FAST             3  'target'
              153  COMPARE_OP            2  ==
              156  POP_JUMP_IF_FALSE   226  'to 226'

 L. 187       159  LOAD_FAST             5  'x'
              162  LOAD_ATTR             9  'check'
              165  LOAD_CONST               'dir'
              168  LOAD_FAST             4  'dir'
              171  CALL_FUNCTION_256   256  None
              174  POP_JUMP_IF_TRUE    222  'to 222'

 L. 188       177  LOAD_FAST             4  'dir'
              180  POP_JUMP_IF_FALSE   201  'to 201'
              183  LOAD_GLOBAL           2  'py'
              186  LOAD_ATTR             3  'error'
              189  LOAD_ATTR            11  'ENOTDIR'
              192  LOAD_FAST             5  'x'
              195  CALL_FUNCTION_1       1  None
            198_0  COME_FROM           180  '180'
              198  JUMP_IF_TRUE_OR_POP   216  'to 216'
              201  LOAD_GLOBAL           2  'py'
              204  LOAD_ATTR             3  'error'
              207  LOAD_ATTR            12  'EISDIR'
              210  LOAD_FAST             5  'x'
              213  CALL_FUNCTION_1       1  None
            216_0  COME_FROM           198  '198'
              216  RAISE_VARARGS_1       1  None
              219  JUMP_FORWARD          0  'to 222'
            222_0  COME_FROM           219  '219'

 L. 189       222  LOAD_FAST             5  'x'
              225  RETURN_VALUE     
            226_0  COME_FROM           156  '156'

 L. 190       226  LOAD_FAST             3  'target'
              229  LOAD_ATTR            13  'relto'
              232  LOAD_FAST             5  'x'
              235  CALL_FUNCTION_1       1  None
              238  STORE_FAST            6  'tocreate'

 L. 191       241  LOAD_FAST             6  'tocreate'
              244  LOAD_ATTR            14  'split'
              247  LOAD_FAST             0  'self'
              250  LOAD_ATTR            15  'sep'
              253  LOAD_CONST               1
              256  CALL_FUNCTION_2       2  None
              259  LOAD_CONST               0
              262  BINARY_SUBSCR    
              263  STORE_FAST            7  'basename'

 L. 192       266  LOAD_GLOBAL           2  'py'
              269  LOAD_ATTR            16  'path'
              272  LOAD_ATTR            17  'local'
              275  LOAD_ATTR            18  'mkdtemp'
              278  CALL_FUNCTION_0       0  None
              281  STORE_FAST            8  'tempdir'

 L. 193       284  SETUP_FINALLY       114  'to 401'

 L. 194       287  LOAD_FAST             8  'tempdir'
              290  LOAD_ATTR            19  'ensure'
              293  LOAD_FAST             6  'tocreate'
              296  LOAD_CONST               'dir'
              299  LOAD_FAST             4  'dir'
              302  CALL_FUNCTION_257   257  None
              305  POP_TOP          

 L. 195       306  LOAD_CONST               'svn import -m "%s" "%s" "%s"'

 L. 196       309  LOAD_CONST               'ensure %s'
              312  LOAD_FAST             0  'self'
              315  LOAD_ATTR            20  '_escape'
              318  LOAD_FAST             6  'tocreate'
              321  CALL_FUNCTION_1       1  None
              324  BINARY_MODULO    

 L. 197       325  LOAD_FAST             0  'self'
              328  LOAD_ATTR            20  '_escape'
              331  LOAD_FAST             8  'tempdir'
              334  LOAD_ATTR             5  'join'
              337  LOAD_FAST             7  'basename'
              340  CALL_FUNCTION_1       1  None
              343  CALL_FUNCTION_1       1  None

 L. 198       346  LOAD_FAST             5  'x'
              349  LOAD_ATTR             5  'join'
              352  LOAD_FAST             7  'basename'
              355  CALL_FUNCTION_1       1  None
              358  LOAD_ATTR            21  '_encodedurl'
              361  CALL_FUNCTION_0       0  None
              364  BUILD_TUPLE_3         3 
              367  BINARY_MODULO    
              368  STORE_FAST            9  'cmd'

 L. 199       371  LOAD_FAST             0  'self'
              374  LOAD_ATTR            22  '_svncmdexecauth'
              377  LOAD_FAST             9  'cmd'
              380  CALL_FUNCTION_1       1  None
              383  POP_TOP          

 L. 200       384  LOAD_FAST             0  'self'
              387  LOAD_ATTR            23  '_norev_delentry'
              390  LOAD_FAST             5  'x'
              393  CALL_FUNCTION_1       1  None
              396  POP_TOP          
              397  POP_BLOCK        
              398  LOAD_CONST               None
            401_0  COME_FROM_FINALLY   284  '284'

 L. 202       401  LOAD_FAST             8  'tempdir'
              404  LOAD_ATTR            24  'remove'
              407  CALL_FUNCTION_0       0  None
              410  POP_TOP          
              411  END_FINALLY      

 L. 203       412  LOAD_FAST             3  'target'
              415  RETURN_VALUE     

Parse error at or near `RAISE_VARARGS_1' instruction at offset 216

    def _propget(self, name):
        res = self._svnwithrev('propget', name)
        return res[:-1]

    def _proplist(self):
        res = self._svnwithrev('proplist')
        lines = res.split('\n')
        lines = [ x.strip() for x in lines[1:] ]
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
                elif e.err.find('E200009:') != -1:
                    raise py.error.ENOENT(self, e.err)
                elif e.err.find('File not found') != -1:
                    raise py.error.ENOENT(self, e.err)
                elif e.err.find('not part of a repository') != -1:
                    raise py.error.ENOENT(self, e.err)
                elif e.err.find('Unable to open') != -1:
                    raise py.error.ENOENT(self, e.err)
                elif e.err.lower().find('method not allowed') != -1:
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
            return

    def listdir(self, fil=None, sort=None):
        """ list directory contents, possibly filter by the given fil func
            and possibly sorted.
        """
        if isinstance(fil, str):
            fil = common.FNMatcher(fil)
        nameinfo_seq = self._listdir_nameinfo()
        if len(nameinfo_seq) == 1:
            name, info = nameinfo_seq[0]
            if name == self.basename and info.kind == 'file':
                raise py.error.ENOTDIR(self)
        paths = [ self.join(name) for name, info in nameinfo_seq ]
        if fil:
            paths = [ x for x in paths if fil(x) ]
        self._sortlist(paths, sort)
        return paths

    def log(self, rev_start=None, rev_end=1, verbose=False):
        """ return a list of LogEntry instances for this path.
rev_start is the starting revision (defaulting to the first one).
rev_end is the last revision (defaulting to HEAD).
if verbose is True, then the LogEntry instances also know which files changed.
"""
        assert self.check()
        rev_start = rev_start is None and 'HEAD' or rev_start
        rev_end = rev_end is None and 'HEAD' or rev_end
        if rev_start == 'HEAD' and rev_end == 1:
            rev_opt = ''
        else:
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


class InfoSvnCommand():
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


class PathEntry():

    def __init__(self, ppart):
        self.strpath = ppart.firstChild.nodeValue.encode('UTF-8')
        self.action = ppart.getAttribute('action').encode('UTF-8')
        if self.action == 'A':
            self.copyfrom_path = ppart.getAttribute('copyfrom-path').encode('UTF-8')
            if self.copyfrom_path:
                self.copyfrom_rev = int(ppart.getAttribute('copyfrom-rev'))