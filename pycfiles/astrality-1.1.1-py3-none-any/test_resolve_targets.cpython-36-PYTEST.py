# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/utils/test_resolve_targets.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 2834 bytes
"""Tests for utils.resolve_targets."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.utils import resolve_targets

def test_resolving_non_existent_file():
    """When `content` does not exist, no targets should be returned."""
    targets = resolve_targets(content=(Path('/does/not/exist')),
      target=(Path('/')),
      include='.*')
    @py_assert2 = {}
    @py_assert1 = targets == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (targets, @py_assert2)) % {'py0':@pytest_ar._saferepr(targets) if 'targets' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(targets) else 'targets',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_resolving_target_of_content_file():
    """When `content` is a file, the target root is used."""
    targets = resolve_targets(content=(Path(__file__)),
      target=(Path('/does/not/exist')),
      include='.*')
    @py_assert2 = {Path(__file__): Path('/does/not/exist')}
    @py_assert1 = targets == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (targets, @py_assert2)) % {'py0':@pytest_ar._saferepr(targets) if 'targets' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(targets) else 'targets',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_resolving_target_file_to_directory():
    """When content is a file, but target is a directory, keep filename."""
    targets = resolve_targets(content=(Path(__file__)),
      target=(Path('/tmp')),
      include='.*')
    @py_assert2 = {Path(__file__): Path('/tmp/test_resolve_targets.py')}
    @py_assert1 = targets == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (targets, @py_assert2)) % {'py0':@pytest_ar._saferepr(targets) if 'targets' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(targets) else 'targets',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_resolving_content_directory(tmpdir):
    """Directory hierarchy should be preserved at target."""
    temp_dir = Path(tmpdir)
    file1 = temp_dir / 'file1'
    file1.touch()
    file2 = temp_dir / 'file2'
    file2.touch()
    recursive_dir = temp_dir / 'recursive'
    recursive_dir.mkdir()
    file3 = temp_dir / 'recursive' / 'file3'
    file3.touch()
    targets = resolve_targets(content=temp_dir,
      target=(Path('/a/b')),
      include='.*')
    @py_assert2 = {file1: Path('/a/b/file1'), file2: Path('/a/b/file2'), file3: Path('/a/b/recursive/file3')}
    @py_assert1 = targets == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (targets, @py_assert2)) % {'py0':@pytest_ar._saferepr(targets) if 'targets' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(targets) else 'targets',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_filtering_based_on_include(tmpdir):
    """Only files that match the regex should be included."""
    temp_dir = Path(tmpdir)
    file1 = temp_dir / 'file1'
    file1.touch()
    file2 = temp_dir / 'file2'
    file2.touch()
    recursive_dir = temp_dir / 'recursive'
    recursive_dir.mkdir()
    file3 = temp_dir / 'recursive' / 'file3'
    file3.touch()
    targets = resolve_targets(content=temp_dir,
      target=(Path('/a/b')),
      include='.+3')
    @py_assert2 = {file3: Path('/a/b/recursive/file3')}
    @py_assert1 = targets == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (targets, @py_assert2)) % {'py0':@pytest_ar._saferepr(targets) if 'targets' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(targets) else 'targets',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_renaming_based_on_include(tmpdir):
    """Targets should be renameable based on the include capture group."""
    temp_dir = Path(tmpdir)
    file1 = temp_dir / 'file1'
    file1.touch()
    file2 = temp_dir / 'file2'
    file2.touch()
    recursive_dir = temp_dir / 'recursive'
    recursive_dir.mkdir()
    file3 = temp_dir / 'recursive' / 'file3'
    file3.touch()
    targets = resolve_targets(content=temp_dir,
      target=(Path('/a/b')),
      include='.+(\\d)')
    @py_assert2 = {file1: Path('/a/b/1'), file2: Path('/a/b/2'), file3: Path('/a/b/recursive/3')}
    @py_assert1 = targets == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (targets, @py_assert2)) % {'py0':@pytest_ar._saferepr(targets) if 'targets' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(targets) else 'targets',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None