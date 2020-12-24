# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pytest/_pytest/capture.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 13441 bytes
"""
per-test stdout/stderr capturing mechanism.

"""
from __future__ import with_statement
import sys, os
from tempfile import TemporaryFile
import py, pytest
from py.io import TextIO
unicode = py.builtin.text
patchsysdict = {0:'stdin', 
 1:'stdout',  2:'stderr'}

def pytest_addoption(parser):
    group = parser.getgroup('general')
    group._addoption('--capture',
      action='store', default=('fd' if hasattr(os, 'dup') else 'sys'),
      metavar='method',
      choices=['fd', 'sys', 'no'],
      help='per-test capturing method: one of fd|sys|no.')
    group._addoption('-s',
      action='store_const', const='no', dest='capture', help='shortcut for --capture=no.')


@pytest.mark.hookwrapper
def pytest_load_initial_conftests(early_config, parser, args):
    ns = early_config.known_args_namespace
    pluginmanager = early_config.pluginmanager
    capman = CaptureManager(ns.capture)
    pluginmanager.register(capman, 'capturemanager')
    pluginmanager.add_shutdown(capman.reset_capturings)

    def silence_logging_at_shutdown():
        if 'logging' in sys.modules:
            sys.modules['logging'].raiseExceptions = False

    pluginmanager.add_shutdown(silence_logging_at_shutdown)
    capman.init_capturings()
    outcome = yield
    out, err = capman.suspendcapture()
    if outcome.excinfo is not None:
        sys.stdout.write(out)
        sys.stderr.write(err)


class CaptureManager:

    def __init__(self, method):
        self._method = method

    def _getcapture(self, method):
        if method == 'fd':
            return MultiCapture(out=True, err=True, Capture=FDCapture)
        else:
            if method == 'sys':
                return MultiCapture(out=True, err=True, Capture=SysCapture)
            if method == 'no':
                return MultiCapture(out=False, err=False, in_=False)
        raise ValueError('unknown capturing method: %r' % method)

    def init_capturings(self):
        assert not hasattr(self, '_capturing')
        self._capturing = self._getcapture(self._method)
        self._capturing.start_capturing()

    def reset_capturings(self):
        cap = self.__dict__.pop('_capturing', None)
        if cap is not None:
            cap.pop_outerr_to_orig()
            cap.stop_capturing()

    def resumecapture(self):
        self._capturing.resume_capturing()

    def suspendcapture(self, in_=False):
        self.deactivate_funcargs()
        cap = getattr(self, '_capturing', None)
        if cap is not None:
            outerr = cap.readouterr()
            cap.suspend_capturing(in_=in_)
            return outerr

    def activate_funcargs(self, pyfuncitem):
        capfuncarg = pyfuncitem.__dict__.pop('_capfuncarg', None)
        if capfuncarg is not None:
            capfuncarg._start()
            self._capfuncarg = capfuncarg

    def deactivate_funcargs(self):
        capfuncarg = self.__dict__.pop('_capfuncarg', None)
        if capfuncarg is not None:
            capfuncarg.close()

    @pytest.mark.hookwrapper
    def pytest_make_collect_report(self, collector):
        if isinstance(collector, pytest.File):
            self.resumecapture()
            outcome = yield
            out, err = self.suspendcapture()
            rep = outcome.get_result()
            if out:
                rep.sections.append(('Captured stdout', out))
            if err:
                rep.sections.append(('Captured stderr', err))
        else:
            yield

    @pytest.mark.hookwrapper
    def pytest_runtest_setup(self, item):
        self.resumecapture()
        yield
        self.suspendcapture_item(item, 'setup')

    @pytest.mark.hookwrapper
    def pytest_runtest_call(self, item):
        self.resumecapture()
        self.activate_funcargs(item)
        yield
        self.suspendcapture_item(item, 'call')

    @pytest.mark.hookwrapper
    def pytest_runtest_teardown(self, item):
        self.resumecapture()
        yield
        self.suspendcapture_item(item, 'teardown')

    @pytest.mark.tryfirst
    def pytest_keyboard_interrupt(self, excinfo):
        self.reset_capturings()

    @pytest.mark.tryfirst
    def pytest_internalerror(self, excinfo):
        self.reset_capturings()

    def suspendcapture_item(self, item, when):
        out, err = self.suspendcapture()
        item.add_report_section(when, 'out', out)
        item.add_report_section(when, 'err', err)


error_capsysfderror = 'cannot use capsys and capfd at the same time'

@pytest.fixture
def capsys(request):
    """enables capturing of writes to sys.stdout/sys.stderr and makes
    captured output available via ``capsys.readouterr()`` method calls
    which return a ``(out, err)`` tuple.
    """
    if 'capfd' in request._funcargs:
        raise request.raiseerror(error_capsysfderror)
    request.node._capfuncarg = c = CaptureFixture(SysCapture)
    return c


@pytest.fixture
def capfd(request):
    """enables capturing of writes to file descriptors 1 and 2 and makes
    captured output available via ``capfd.readouterr()`` method calls
    which return a ``(out, err)`` tuple.
    """
    if 'capsys' in request._funcargs:
        request.raiseerror(error_capsysfderror)
    if not hasattr(os, 'dup'):
        pytest.skip('capfd funcarg needs os.dup')
    request.node._capfuncarg = c = CaptureFixture(FDCapture)
    return c


class CaptureFixture:

    def __init__(self, captureclass):
        self.captureclass = captureclass

    def _start(self):
        self._capture = MultiCapture(out=True, err=True, in_=False, Capture=(self.captureclass))
        self._capture.start_capturing()

    def close(self):
        cap = self.__dict__.pop('_capture', None)
        if cap is not None:
            self._outerr = cap.pop_outerr_to_orig()
            cap.stop_capturing()

    def readouterr(self):
        try:
            return self._capture.readouterr()
        except AttributeError:
            return self._outerr


def safe_text_dupfile(f, mode, default_encoding='UTF8'):
    """ return a open text file object that's a duplicate of f on the
        FD-level if possible.
    """
    encoding = getattr(f, 'encoding', None)
    try:
        fd = f.fileno()
    except Exception:
        if 'b' not in getattr(f, 'mode', ''):
            if hasattr(f, 'encoding'):
                return f
    else:
        newfd = os.dup(fd)
        if 'b' not in mode:
            mode += 'b'
        f = os.fdopen(newfd, mode, 0)
    return EncodedFile(f, encoding or default_encoding)


class EncodedFile(object):
    errors = 'strict'

    def __init__(self, buffer, encoding):
        self.buffer = buffer
        self.encoding = encoding

    def write(self, obj):
        if isinstance(obj, unicode):
            obj = obj.encode(self.encoding, 'replace')
        self.buffer.write(obj)

    def writelines(self, linelist):
        data = ''.join(linelist)
        self.write(data)

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, 'buffer'), name)


class MultiCapture(object):
    out = err = in_ = None

    def __init__(self, out=True, err=True, in_=True, Capture=None):
        if in_:
            self.in_ = Capture(0)
        else:
            if out:
                self.out = Capture(1)
            if err:
                self.err = Capture(2)

    def start_capturing(self):
        if self.in_:
            self.in_.start()
        else:
            if self.out:
                self.out.start()
            if self.err:
                self.err.start()

    def pop_outerr_to_orig(self):
        """ pop current snapshot out/err capture and flush to orig streams. """
        out, err = self.readouterr()
        if out:
            self.out.writeorg(out)
        if err:
            self.err.writeorg(err)
        return (
         out, err)

    def suspend_capturing(self, in_=False):
        if self.out:
            self.out.suspend()
        else:
            if self.err:
                self.err.suspend()
            if in_:
                if self.in_:
                    self.in_.suspend()
                    self._in_suspended = True

    def resume_capturing(self):
        if self.out:
            self.out.resume()
        else:
            if self.err:
                self.err.resume()
            if hasattr(self, '_in_suspended'):
                self.in_.resume()
                del self._in_suspended

    def stop_capturing(self):
        """ stop capturing and reset capturing streams """
        if hasattr(self, '_reset'):
            raise ValueError('was already stopped')
        else:
            self._reset = True
            if self.out:
                self.out.done()
            if self.err:
                self.err.done()
            if self.in_:
                self.in_.done()

    def readouterr(self):
        """ return snapshot unicode value of stdout/stderr capturings. """
        return (self.out.snap() if self.out is not None else '',
         self.err.snap() if self.err is not None else '')


class NoCapture:
    __init__ = start = done = suspend = resume = lambda *args: None


class FDCapture:
    __doc__ = ' Capture IO to/from a given os-level filedescriptor. '

    def __init__(self, targetfd, tmpfile=None):
        self.targetfd = targetfd
        try:
            self.targetfd_save = os.dup(self.targetfd)
        except OSError:
            self.start = lambda : None
            self.done = lambda : None
        else:
            if targetfd == 0:
                assert not tmpfile, 'cannot set tmpfile with stdin'
                tmpfile = open(os.devnull, 'r')
                self.syscapture = SysCapture(targetfd)
            else:
                if tmpfile is None:
                    f = TemporaryFile()
                    with f:
                        tmpfile = safe_text_dupfile(f, mode='wb+')
                if targetfd in patchsysdict:
                    self.syscapture = SysCapture(targetfd, tmpfile)
                else:
                    self.syscapture = NoCapture()
                self.tmpfile = tmpfile
                self.tmpfile_fd = tmpfile.fileno()

    def __repr__(self):
        return '<FDCapture %s oldfd=%s>' % (self.targetfd, self.targetfd_save)

    def start(self):
        """ Start capturing on targetfd using memorized tmpfile. """
        try:
            os.fstat(self.targetfd_save)
        except (AttributeError, OSError):
            raise ValueError('saved filedescriptor not valid anymore')

        os.dup2(self.tmpfile_fd, self.targetfd)
        self.syscapture.start()

    def snap(self):
        f = self.tmpfile
        f.seek(0)
        res = f.read()
        if res:
            enc = getattr(f, 'encoding', None)
            if enc:
                if isinstance(res, bytes):
                    res = py.builtin._totext(res, enc, 'replace')
            f.truncate(0)
            f.seek(0)
            return res
        else:
            return ''

    def done(self):
        """ stop capturing, restore streams, return original capture file,
        seeked to position zero. """
        targetfd_save = self.__dict__.pop('targetfd_save')
        os.dup2(targetfd_save, self.targetfd)
        os.close(targetfd_save)
        self.syscapture.done()
        self.tmpfile.close()

    def suspend(self):
        self.syscapture.suspend()
        os.dup2(self.targetfd_save, self.targetfd)

    def resume(self):
        self.syscapture.resume()
        os.dup2(self.tmpfile_fd, self.targetfd)

    def writeorg(self, data):
        """ write to original file descriptor. """
        if py.builtin._istext(data):
            data = data.encode('utf8')
        os.write(self.targetfd_save, data)


class SysCapture:

    def __init__(self, fd, tmpfile=None):
        name = patchsysdict[fd]
        self._old = getattr(sys, name)
        self.name = name
        if tmpfile is None:
            if name == 'stdin':
                tmpfile = DontReadFromInput()
            else:
                tmpfile = TextIO()
        self.tmpfile = tmpfile

    def start(self):
        setattr(sys, self.name, self.tmpfile)

    def snap(self):
        f = self.tmpfile
        res = f.getvalue()
        f.truncate(0)
        f.seek(0)
        return res

    def done(self):
        setattr(sys, self.name, self._old)
        del self._old
        self.tmpfile.close()

    def suspend(self):
        setattr(sys, self.name, self._old)

    def resume(self):
        setattr(sys, self.name, self.tmpfile)

    def writeorg(self, data):
        self._old.write(data)
        self._old.flush()


class DontReadFromInput:
    __doc__ = 'Temporary stub class.  Ideally when stdin is accessed, the\n    capturing should be turned off, with possibly all data captured\n    so far sent to the screen.  This should be configurable, though,\n    because in automated test runs it is better to crash than\n    hang indefinitely.\n    '
    encoding = None

    def read(self, *args):
        raise IOError('reading from stdin while output is captured')

    readline = read
    readlines = read
    __iter__ = read

    def fileno(self):
        raise ValueError('redirected Stdin is pseudofile, has no fileno()')

    def isatty(self):
        return False

    def close(self):
        pass