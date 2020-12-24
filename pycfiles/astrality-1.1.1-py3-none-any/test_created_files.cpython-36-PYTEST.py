# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/persistence/test_created_files.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 14638 bytes
"""Tests for astrality.persistence.CreatedFiles."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
import shutil, pytest
from astrality.persistence import CreatedFiles, CreationMethod

def test_that_file_is_created_with_created_files():
    """A file should be created to store module created files."""
    created_files = CreatedFiles()
    path = created_files.path
    @py_assert1 = path.name
    @py_assert4 = 'created_files.yml'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = path.exists
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_that_created_files_are_properly_persisted(create_temp_files):
    """Inserted files should be persisted properly."""
    created_files = CreatedFiles()
    @py_assert1 = created_files.by
    @py_assert3 = 'name'
    @py_assert5 = @py_assert1(module=@py_assert3)
    @py_assert8 = []
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.by\n}(module=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    a, b, c, d = create_temp_files(4)
    created_files.insert(module='name',
      creation_method=(CreationMethod.COPY),
      contents=[
     a],
      targets=[
     b])
    @py_assert1 = created_files.by
    @py_assert3 = 'name'
    @py_assert5 = @py_assert1(module=@py_assert3)
    @py_assert8 = [
     b]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.by\n}(module=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    created_files.insert(module='name',
      creation_method=(CreationMethod.COPY),
      contents=[
     a],
      targets=[
     b])
    @py_assert1 = created_files.by
    @py_assert3 = 'name'
    @py_assert5 = @py_assert1(module=@py_assert3)
    @py_assert8 = [
     b]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.by\n}(module=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    created_files.insert(module='name',
      creation_method=(CreationMethod.COPY),
      contents=[
     c],
      targets=[
     d])
    @py_assert1 = created_files.by
    @py_assert3 = 'name'
    @py_assert5 = @py_assert1(module=@py_assert3)
    @py_assert8 = [
     b, d]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.by\n}(module=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    del created_files
    created_files = CreatedFiles()
    @py_assert1 = created_files.by
    @py_assert3 = 'name'
    @py_assert5 = @py_assert1(module=@py_assert3)
    @py_assert8 = [
     b, d]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.by\n}(module=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_that_cleanup_method_removes_files(tmpdir, create_temp_files):
    """The cleanup method should remove all files created by module."""
    content1, content2, content3, content4, compilation1, compilation2, compilation4 = create_temp_files(7)
    symlink3 = Path(tmpdir, 'symlink3.tmp')
    symlink3.symlink_to(content3)
    created_files = CreatedFiles()
    created_files.insert(module='name',
      creation_method=(CreationMethod.COMPILE),
      contents=[
     content1, content2],
      targets=[
     compilation1, compilation2])
    created_files.insert(module='name',
      creation_method=(CreationMethod.SYMLINK),
      contents=[
     content3],
      targets=[
     symlink3])
    created_files.insert(module='other_module',
      creation_method=(CreationMethod.COMPILE),
      contents=[
     content4],
      targets=[
     compilation4])
    created_files.cleanup(module='name')
    for content in (content1, content2, content3, content4):
        @py_assert1 = content.exists
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None

    for cleaned_file in (compilation1, compilation2, symlink3):
        @py_assert1 = cleaned_file.exists
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(cleaned_file) if 'cleaned_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cleaned_file) else 'cleaned_file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    @py_assert1 = compilation4.exists
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(compilation4) if 'compilation4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compilation4) else 'compilation4',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = created_files.by
    @py_assert3 = 'name'
    @py_assert5 = @py_assert1(module=@py_assert3)
    @py_assert8 = []
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.by\n}(module=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    del created_files
    created_files = CreatedFiles()
    @py_assert1 = created_files.by
    @py_assert3 = 'name'
    @py_assert5 = @py_assert1(module=@py_assert3)
    @py_assert8 = []
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.by\n}(module=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_that_dry_run_is_respected(create_temp_files, caplog):
    """When dry_run is True, no files should be deleted."""
    content, target = create_temp_files(2)
    created_files = CreatedFiles()
    created_files.insert(module='name',
      creation_method=(CreationMethod.COPY),
      contents=[
     content],
      targets=[
     target])
    caplog.clear()
    created_files.cleanup(module='name', dry_run=True)
    @py_assert1 = content.exists
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = target.exists
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'SKIPPED: '
    @py_assert3 = caplog.record_tuples[0][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = created_files.by
    @py_assert3 = 'name'
    @py_assert5 = @py_assert1(module=@py_assert3)
    @py_assert8 = [
     target]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.by\n}(module=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_that_deleted_files_are_handled_gracefully_under_cleanup(create_temp_files):
    """When creations have been deleted they should be skipped."""
    content, target = create_temp_files(2)
    created_files = CreatedFiles()
    created_files.insert(module='name',
      creation_method=(CreationMethod.COPY),
      contents=[
     content],
      targets=[
     target])
    target.unlink()
    created_files.cleanup(module='name')


def test_that_inserting_non_existent_file_is_skipped(create_temp_files):
    """When creations have been deleted they should be skipped."""
    content, target = create_temp_files(2)
    target.unlink()
    created_files = CreatedFiles()
    created_files.insert(module='name',
      creation_method=(CreationMethod.COPY),
      contents=[
     content],
      targets=[
     target])
    @py_assert1 = created_files.by
    @py_assert3 = 'name'
    @py_assert5 = @py_assert1(module=@py_assert3)
    @py_assert8 = []
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.by\n}(module=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_that_creations_are_properly_hashed(create_temp_files):
    """Creations should be hashed according to file content."""
    target1, target2, target3, content = create_temp_files(4)
    target1.write_text('identical')
    target2.write_text('identical')
    target3.write_text('different')
    created_files = CreatedFiles()
    created_files.insert(module='name',
      creation_method=(CreationMethod.COPY),
      contents=[
     content, content, content],
      targets=[
     target1, target2, target3])
    @py_assert0 = created_files.creations['name'][str(target1)]['hash']
    @py_assert3 = created_files.creations['name'][str(target2)]['hash']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = created_files.creations['name'][str(target1)]['hash']
    @py_assert3 = created_files.creations['name'][str(target3)]['hash']
    @py_assert2 = @py_assert0 != @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_creating_created_files_object_for_specific_module(create_temp_files):
    """You should be able to construct a CreatedFiles wrapper for a module."""
    content, target = create_temp_files(2)
    created_files = CreatedFiles().wrapper_for(module='my_module')
    created_files.insert_creation(content=content,
      target=target,
      method=(CreationMethod.SYMLINK))


def test_backup_method(tmpdir, create_temp_files, patch_xdg_directory_standard):
    """Backup should perform backup of files not created by Astrality."""
    external_file, created_file, created_file_content = create_temp_files(3)
    external_file.write_text('original')
    created_file.write_text('new')
    created_file_content.write_text('content')
    created_files = CreatedFiles()
    created_files.insert(module='name',
      creation_method=(CreationMethod.COMPILE),
      contents=[
     created_file_content],
      targets=[
     created_file])
    @py_assert1 = created_file in created_files
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (created_file, created_files)) % {'py0':@pytest_ar._saferepr(created_file) if 'created_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_file) else 'created_file',  'py2':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = created_files.backup
    @py_assert3 = 'name'
    @py_assert6 = @py_assert1(module=@py_assert3, path=created_file)
    @py_assert9 = None
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.backup\n}(module=%(py4)s, path=%(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(created_file) if 'created_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_file) else 'created_file',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = external_file not in created_files
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py2)s', ), (external_file, created_files)) % {'py0':@pytest_ar._saferepr(external_file) if 'external_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(external_file) else 'external_file',  'py2':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert0 = created_files.creations['name'][str(created_file)]['backup']
    @py_assert3 = None
    @py_assert2 = @py_assert0 is @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    backup = created_files.backup(module='name', path=external_file)
    @py_assert1 = external_file.name
    @py_assert5 = backup.name
    @py_assert3 = @py_assert1 in @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} in %(py6)s\n{%(py6)s = %(py4)s.name\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(external_file) if 'external_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(external_file) else 'external_file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(backup) if 'backup' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backup) else 'backup',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = backup.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'original'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(backup) if 'backup' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backup) else 'backup',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = external_file.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(external_file) if 'external_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(external_file) else 'external_file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = backup.parent
    @py_assert5 = 'backups'
    @py_assert7 = patch_xdg_directory_standard / @py_assert5
    @py_assert8 = 'name'
    @py_assert10 = @py_assert7 / @py_assert8
    @py_assert3 = @py_assert1 == @py_assert10
    if not @py_assert3:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.parent\n} == ((%(py4)s / %(py6)s) / %(py9)s)', ), (@py_assert1, @py_assert10)) % {'py0':@pytest_ar._saferepr(backup) if 'backup' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backup) else 'backup',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(patch_xdg_directory_standard) if 'patch_xdg_directory_standard' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patch_xdg_directory_standard) else 'patch_xdg_directory_standard',  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = None
    @py_assert0 = created_files.creations['name'][str(external_file)]['backup']
    @py_assert5 = str(backup)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(backup) if 'backup' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backup) else 'backup',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    shutil.copy2(str(created_file_content), str(external_file))
    created_files.insert(module='name',
      creation_method=(CreationMethod.COPY),
      contents=[
     created_file_content],
      targets=[
     external_file])
    @py_assert0 = created_files.creations['name'][str(external_file)]['backup']
    @py_assert5 = str(backup)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(backup) if 'backup' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backup) else 'backup',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    @py_assert0 = created_files.creations['name'][str(external_file)]['method']
    @py_assert3 = 'copied'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = created_files.creations['name'][str(external_file)]['content']
    @py_assert5 = str(created_file_content)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(created_file_content) if 'created_file_content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_file_content) else 'created_file_content',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    @py_assert1 = external_file.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'content'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(external_file) if 'external_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(external_file) else 'external_file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    created_files.cleanup('name')
    @py_assert1 = external_file.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'original'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(external_file) if 'external_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(external_file) else 'external_file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_taking_backup_of_symlinks(create_temp_files):
    """Symlinks should be properly backed up."""
    original_symlink, original_target, new_target = create_temp_files(3)
    original_symlink.unlink()
    original_symlink.symlink_to(original_target)
    original_target.write_text('original content')
    @py_assert1 = original_symlink.resolve
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == original_target
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n} == %(py6)s', ), (@py_assert3, original_target)) % {'py0':@pytest_ar._saferepr(original_symlink) if 'original_symlink' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(original_symlink) else 'original_symlink',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(original_target) if 'original_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(original_target) else 'original_target'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = original_symlink.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'original content'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(original_symlink) if 'original_symlink' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(original_symlink) else 'original_symlink',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    created_files = CreatedFiles()
    created_files.backup(module='name', path=original_symlink)
    new_target.write_text('new content')
    original_symlink.symlink_to(new_target)
    created_files.insert(module='name',
      creation_method=(CreationMethod.SYMLINK),
      contents=[
     new_target],
      targets=[
     original_symlink])
    @py_assert1 = original_symlink.resolve
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == new_target
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n} == %(py6)s', ), (@py_assert3, new_target)) % {'py0':@pytest_ar._saferepr(original_symlink) if 'original_symlink' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(original_symlink) else 'original_symlink',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(new_target) if 'new_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_target) else 'new_target'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = original_symlink.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'new content'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(original_symlink) if 'original_symlink' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(original_symlink) else 'original_symlink',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    created_files.cleanup(module='name')
    @py_assert1 = original_symlink.resolve
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == original_target
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n} == %(py6)s', ), (@py_assert3, original_target)) % {'py0':@pytest_ar._saferepr(original_symlink) if 'original_symlink' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(original_symlink) else 'original_symlink',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(original_target) if 'original_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(original_target) else 'original_target'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = original_symlink.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'original content'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(original_symlink) if 'original_symlink' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(original_symlink) else 'original_symlink',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_creation_and_cleanup_of_directory(create_temp_files):
    """Created directories should be tracked."""
    created_files = CreatedFiles().wrapper_for(module='my_module')
    content, target = create_temp_files(2)
    created_files.insert_creation(content=None,
      target=(target.parent),
      method=(CreationMethod.MKDIR))
    created_files.insert_creation(content=content,
      target=target,
      method=(CreationMethod.COPY))
    global_created_files = CreatedFiles()
    creations = global_created_files.by('my_module')
    @py_assert2 = len(creations)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(creations) if 'creations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(creations) else 'creations',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = target.parent
    @py_assert3 = @py_assert1 in global_created_files
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.parent\n} in %(py4)s', ), (@py_assert1, global_created_files)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(global_created_files) if 'global_created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_created_files) else 'global_created_files'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = target in global_created_files
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (target, global_created_files)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(global_created_files) if 'global_created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_created_files) else 'global_created_files'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = target.parent
    @py_assert3 = @py_assert1.is_dir
    @py_assert5 = @py_assert3()
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parent\n}.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    external_file = target.parent / 'external.tmp'
    external_file.touch()
    global_created_files.cleanup(module='my_module')
    @py_assert1 = target.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = target.parent
    @py_assert3 = @py_assert1.is_dir
    @py_assert5 = @py_assert3()
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parent\n}.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = target.parent
    @py_assert5 = CreatedFiles()
    @py_assert3 = @py_assert1 in @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.parent\n} in %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(CreatedFiles) if 'CreatedFiles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(CreatedFiles) else 'CreatedFiles',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    external_file.unlink()
    global_created_files.cleanup(module='my_module')
    @py_assert1 = target.parent
    @py_assert3 = @py_assert1.is_dir
    @py_assert5 = @py_assert3()
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parent\n}.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_cleanup_of_recursive_directories(tmpdir):
    """Recursively created directories should be cleaned up."""
    tmpdir = Path(tmpdir)
    a = tmpdir / 'a'
    b = a / 'b'
    c = b / 'c'
    c.mkdir(parents=True)
    created_files = CreatedFiles().wrapper_for(module='my_module')
    for directory in (c, a, b):
        created_files.insert_creation(content=None,
          target=directory,
          method=(CreationMethod.MKDIR))

    content = tmpdir / 'content.tmp'
    target = c / 'target.tmp'
    content.touch()
    target.touch()
    created_files.insert_creation(content=content,
      target=target,
      method=(CreationMethod.COPY))
    CreatedFiles().cleanup(module='my_module')
    for directory in (a, b, c):
        @py_assert1 = directory.exists
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    @py_assert1 = target.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


@pytest.mark.parametrize('with_wrapper', (False, True))
def test_mkdir_method_of_created_files(tmpdir, with_wrapper):
    """CreatedFiles should be able to create and persist directories."""
    tmpdir = Path(tmpdir)
    a = tmpdir / 'a'
    a.mkdir(parents=True)
    b = a / 'b'
    c = b / 'c'
    created_files = CreatedFiles()
    if with_wrapper:
        created_files.wrapper_for(module='my_module').mkdir(path=c)
    else:
        created_files.mkdir(module='my_module', path=c)
    @py_assert1 = b.is_dir
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(b) if 'b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(b) else 'b',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = c.is_dir
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = created_files.by
    @py_assert4 = 'my_module'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = len(@py_assert6)
    @py_assert11 = 2
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.by\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert1 = b in created_files
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (b, created_files)) % {'py0':@pytest_ar._saferepr(b) if 'b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(b) else 'b',  'py2':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = c in created_files
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (c, created_files)) % {'py0':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py2':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = a not in created_files
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py2)s', ), (a, created_files)) % {'py0':@pytest_ar._saferepr(a) if 'a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a) else 'a',  'py2':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    created_files.cleanup(module='my_module')
    @py_assert1 = b.is_dir
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(b) if 'b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(b) else 'b',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = c.is_dir
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = a.is_dir
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(a) if 'a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a) else 'a',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None