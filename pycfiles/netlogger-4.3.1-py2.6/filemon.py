# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/filemon.py
# Compiled at: 2009-12-08 17:43:28
"""
Monitor groups of files.

Example usage:
    def doSomething(data, arg=None):
        print arg,data['file'],'changed'
    m1 = MonitoredFiles(glob.glob("/etc/*.conf"))
    m2 = MonitoredFiles(glob.glob("/etc/myapp/*.cfg"))
    loopOverFiles((m1,m2), doSomething, dict(arg='foo'))
"""
from base64 import b64encode
import glob, os, signal, sys, time
from netlogger.nllog import DoesLogging
B64_TEXT_ATTR = 'text64'
READ_TEXT = 1
OPEN_FILE = 2
STDIN_FILENAME = '-'

class StatFile(DoesLogging):
    """Conveniently encapsulate result of os.stat() operations
    on a given file.
    """

    def __init__(self, path):
        DoesLogging.__init__(self)
        self.info = dict.fromkeys(('mode', 'ino', 'dev', 'nlink', 'uid', 'gid', 'size',
                                   'atime', 'mtime', 'ctime'), 0)
        if os.path.basename(path) == STDIN_FILENAME:
            self.path = None
            self.info['mtime'] = time.time()
            self.last_info = self.info
        else:
            self.path = path
        return

    def stat(self):
        if self.path is None:
            return
        else:
            try:
                d = os.stat(self.path)
            except os.error:
                self.info['mtime'] = -1
                return

            self.last_info = self.info.copy()
            self.info = {'mode': d[0], 'ino': d[1], 
               'dev': d[2], 
               'nlink': d[3], 
               'uid': d[4], 
               'gid': d[5], 
               'size': d[6], 
               'atime': d[7], 
               'mtime': d[8], 
               'ctime': d[9]}
            return

    def __cmp__(self, other):
        if isinstance(other, str):
            return cmp(self.path, other)
        else:
            return cmp(self.path, other.path)

    def __hash__(self):
        return hash(self.path)

    @property
    def changed(self):
        if self.last_info['mtime'] == 0:
            return 'new'
        else:
            if self.info['mtime'] == -1:
                return 'removed'
            else:
                if self.last_info['mtime'] < self.info['mtime']:
                    return 'modified'
                return
            return

    @property
    def name(self):
        return self.path

    def __repr__(self):
        return 'stat(%s)' % self.path


class ReadableStatFile(StatFile):

    def __init__(self, path):
        StatFile.__init__(self, path)
        if os.path.basename(path) == STDIN_FILENAME:
            self._rfile = sys.stdin
        else:
            self._rfile = open(path)

    def read(self, *args):
        return self._rfile.read(*args)

    def readline(self):
        return self._rfile.readline()


class MonitoredFiles(DoesLogging):
    """Monitor a group of files.
    """
    MAX_BYTES = 65536

    def __init__(self, files, group='none', options=()):
        DoesLogging.__init__(self)
        self._group = group
        self._read_text = READ_TEXT in options
        self._open_file = OPEN_FILE in options
        if self._open_file:
            self._wrapper = ReadableStatFile
        else:
            self._wrapper = StatFile
        self._files = map(self._wrapper, files)
        self._blacklist = {}

    def addFile(self, filename):
        """Add a file, unless it's already in the list, 
        or it's on the 'blacklist'.
        """
        if self._blacklist.has_key(filename):
            return
        for f in self._files:
            if f.path == filename:
                return

        self._files.append(self._wrapper(filename))

    def removeFile(self, f, blacklist=False):
        """Remove a file, unless it's not there"""
        try:
            self._files.remove(f)
            if blacklist:
                self._blacklist[f] = True
        except ValueError:
            pass

    def getFiles(self):
        return self._files

    def getChanged(self):
        """Generator that returns a pair with the
        name of the event ('modified', 'new', 'removed') and
        a dictionary containing
        file attributes and, optionally, base-64 encoded text whenever one
        of the files changes -- or None if no file in the list
        is different from last time.
        """
        while 1:
            is_changed, keep = False, []
            for (i, f) in enumerate(self._files):
                f.stat()
                c = f.changed
                if c:
                    self.log.debug('file %s changed: %s', f.path, c)
                    is_changed = True
                    data = f.info.copy()
                    realpath = os.path.realpath(f.path)
                    data['dir'], data['file'] = os.path.dirname(realpath), os.path.basename(realpath)
                    data['group'] = self._group
                    if c != 'removed':
                        if self._read_text:
                            rfile = file(f.path)
                            bytes = rfile.read(self.MAX_BYTES)
                            data[B64_TEXT_ATTR] = b64encode(bytes)
                        keep.append(i)
                    yield (
                     c, data)
                else:
                    keep.append(i)

            if is_changed:
                self._files = [ self._files[i] for i in keep ]
            else:
                yield

        return

    def __len__(self):
        return len(self._files)

    def __repr__(self):
        return (',').join(map(str, self._files))


class MonitoredFilesManager(DoesLogging):
    EVENT_PREFIX = 'nl.config.'
    DEFAULT_SIGNALS = (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)

    def __init__(self, config_file=None, args=None, patterns=None, options=(
 READ_TEXT,), signals=DEFAULT_SIGNALS, sleep=1, scan=60, on_changed=None, **kw):
        """Sleep for 'sleep' seconds on every loop with no data.
        Re-scan the file patterns, from 'args' or the config file,
        every 'scan' seconds.

        Whenever a file removal, addition, or modification is detected,
        call the 'on_changed' callback with the provided keyword arguments,
        and two positional arguments: how-changed (string), and a 
        dictionary representing new state.

        The signals given in 'signals' will be handled by stopping the
        endless loop in loop(); to disable this behavior, just pass an
        empty list or tuple, i.e. signals=().
        """
        DoesLogging.__init__(self)
        self.sleep, self.scan = sleep, scan
        for signo in signals:
            signal.signal(signo, self.stopLoop)

        self._stop = False
        if config_file is not None:
            self._patterns = self._readConfig()
        elif patterns is not None:
            self._patterns = patterns
        else:
            self._patterns = {'default': args}
        if on_changed is None:
            self._onChanged = self._writeChanged
        else:
            self._onChanged = on_changed
        self._on_changed_kw = kw
        self._options = options
        self.mfile_groups = {}
        return

    def _writeChanged(self, how, data, writer=None):
        """Write an event for a changed file."""
        writer.write(event=(self.EVENT_PREFIX + how), **data)

    def _readConfig(self):
        p = ConfigParser.RawConfigParser()
        success = p.read(self._config_file)
        if not success:
            raise ConfigParser.ParsingError('cannot parse file %s' % self._config_file)
        patterns = {}
        for section in p.sections():
            patterns[section] = []
            for (name, value) in p.items(section):
                if name == 'files':
                    for pattern in value.split(','):
                        patterns[section].append(pattern)

                else:
                    raise ConfigParser.ParsingError("unknown parameter '%s' in section %s. expected 'files'" % (
                     name, section))

        return patterns

    def _getFileGroups(self):
        groups = {}
        for k in self._patterns.keys():
            groups[k] = []
            for p in self._patterns[k]:
                if p == STDIN_FILENAME:
                    groups[k].append(p)
                else:
                    groups[k].extend(glob.glob(p))

        return groups

    def getGroups(self):
        return self.mfile_groups

    def isEmpty(self):
        return sum(map(len, self.mfile_groups.values())) == 0

    def loopInit(self):
        """Initialize monitored file groups and timers for loopOnce
        """
        self.mfile_groups = {}
        for (g, files) in self._getFileGroups().items():
            self.mfile_groups[g] = MonitoredFiles(files, group=g, options=self._options)

        self.last_scan = time.time()

    def loopOnce(self, do_sleep=True):
        """Loop once (unless stopped) over the list of monitored files.
        """
        some_changed = False
        for (g, mfile) in self.mfile_groups.items():
            if self._stop:
                break
            for change in mfile.getChanged():
                if self._stop or change is None:
                    break
                self._onChanged(*change, **self._on_changed_kw)
                some_changed = True

        if self._stop:
            return
        else:
            if not some_changed and do_sleep:
                time.sleep(self.sleep)
            t = time.time()
            if t - self.last_scan >= self.scan:
                new_files = self._getFileGroups()
                for (g, filenames) in new_files.items():
                    if self.mfile_groups.has_key(g):
                        for filename in filenames:
                            self.mfile_groups[g].addFile(filename)

                    else:
                        self.mfile_groups[g] = MonitoredFiles(filenames, group=g)

                self.last_scan = t
            return

    def loop(self):
        """Loop over the lists of monitored files until one of the signals
        is received or until somebody else calls stopLoop().
        """
        self.loopInit()
        while not self._stop:
            self.loopOnce()

    def stopLoop(self, signo, frame):
        """Stop any current or future loopOverFiles().
        """
        self._stop = True