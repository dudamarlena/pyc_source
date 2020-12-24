# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/test_filewatcher.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 3710 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, shutil
from sys import platform
from pathlib import Path
import pytest
from watchdog.observers import Observer
from astrality.filewatcher import DirectoryWatcher
from astrality.tests.utils import Retry
MACOS = platform == 'darwin'

@pytest.yield_fixture
def watch_dir(tmpdir):
    """Instanciate a directory watcher and stop it after its use."""
    watched_directory = Path(tmpdir)
    test_file1 = watched_directory / 'tmp_test_file1'
    recursive_dir = watched_directory / 'test_folder'
    test_file2 = recursive_dir / 'tmp_test_file2'

    class EventSaver:
        __doc__ = 'Mock class for testing callback function.'

        def __init__(self):
            self.called = 0
            self.argument = None

        def save_argument(self, path: Path) -> None:
            self.called += 1
            self.argument = path

    event_saver = EventSaver()
    dir_watcher = DirectoryWatcher(directory=watched_directory,
      on_modified=(event_saver.save_argument))
    yield (
     watched_directory,
     recursive_dir,
     test_file1,
     test_file2,
     dir_watcher,
     event_saver)
    dir_watcher.stop()
    if test_file1.is_file():
        os.remove(test_file1)
    if test_file2.is_file():
        os.remove(test_file2)
    if recursive_dir.is_dir():
        shutil.rmtree(recursive_dir)


@pytest.mark.skipif(MACOS, reason='Flaky on MacOS')
@pytest.mark.slow
def test_filesystem_watcher(watch_dir):
    """
    Test correct callback invocation on directory watching.

    Sometimes the on_modified function is called several times by watchdog,
    for a unknown reason. It might be other tests which interfer. We therefore
    check if the lower bound of calls is satisfied, but do not test the exact
    number of calls to on_modified.
    """
    watched_directory, recursive_dir, test_file1, test_file2, dir_watcher, event_saver = watch_dir
    dir_watcher.start()
    @py_assert1 = event_saver.argument
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.argument\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(event_saver) if 'event_saver' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_saver) else 'event_saver',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = event_saver.called
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.called\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(event_saver) if 'event_saver' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_saver) else 'event_saver',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    test_file1.touch()
    retry = Retry()
    @py_assert1 = event_saver.argument
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.argument\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(event_saver) if 'event_saver' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_saver) else 'event_saver',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = event_saver.called
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.called\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(event_saver) if 'event_saver' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_saver) else 'event_saver',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    test_file1.write_text('test_content')
    @py_assert1 = lambda : event_saver.argument == test_file1
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = event_saver.called
    @py_assert4 = 1
    @py_assert3 = @py_assert1 >= @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.called\n} >= %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(event_saver) if 'event_saver' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_saver) else 'event_saver',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    recursive_dir.mkdir(parents=True)
    @py_assert1 = lambda : event_saver.argument == test_file1
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : event_saver.called >= 1
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    test_file2.write_text('test')
    @py_assert1 = lambda : event_saver.argument == test_file2
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = event_saver.called
    @py_assert4 = 2
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.called\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(event_saver) if 'event_saver' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_saver) else 'event_saver',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_logging_of_os_errors(monkeypatch, tmpdir, caplog):
    """Filesystem watcher can fail due to limits, and it should be logged."""

    def raiser(self):
        raise OSError('inotify watch limit reached')

    monkeypatch.setattr(Observer,
      name='start',
      value=raiser)
    dir_watcher = DirectoryWatcher(directory=tmpdir,
      on_modified=(lambda x: x))
    caplog.clear()
    dir_watcher.start()
    @py_assert0 = 'inotify watch limit reached'
    @py_assert3 = caplog.record_tuples[0][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    dir_watcher.stop()