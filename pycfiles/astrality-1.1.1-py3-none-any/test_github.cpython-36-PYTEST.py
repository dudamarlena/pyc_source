# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/config/test_github.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 4023 bytes
"""Test module for enabled modules sourced from Github."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
import pytest
from astrality.exceptions import GithubModuleError
from astrality.github import clone_or_pull_repo, clone_repo
from astrality.utils import run_shell

@pytest.mark.slow
def test_clone_github_repo(tmpdir):
    modules_directory = Path(tmpdir.mkdir('modules'))
    repo_dir = clone_repo(user='jakobgm',
      repository='color-schemes.astrality',
      modules_directory=modules_directory)
    @py_assert1 = repo_dir.is_dir
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(repo_dir) if 'repo_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo_dir) else 'repo_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    module_config = repo_dir / 'modules.yml'
    @py_assert1 = module_config.is_file
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(module_config) if 'module_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_config) else 'module_config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = repo_dir.name
    @py_assert4 = 'color-schemes.astrality'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(repo_dir) if 'repo_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo_dir) else 'repo_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = repo_dir.parent
    @py_assert3 = @py_assert1.name
    @py_assert6 = 'jakobgm'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parent\n}.name\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(repo_dir) if 'repo_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo_dir) else 'repo_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


@pytest.mark.slow
def test_cloning_non_existent_github_repository(tmpdir):
    modules_directory = Path(tmpdir.mkdir('modules'))
    with pytest.raises(GithubModuleError):
        clone_repo(user='jakobgm',
          repository='i-will-never-create-this-repository',
          modules_directory=modules_directory)
    github_user_directory = modules_directory / 'jakobgm'
    @py_assert1 = github_user_directory.is_dir
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(github_user_directory) if 'github_user_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_user_directory) else 'github_user_directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    repository_directory = github_user_directory / 'i-will-never-create-this-repository'
    @py_assert1 = repository_directory.is_dir
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(repository_directory) if 'repository_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repository_directory) else 'repository_directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


@pytest.mark.slow
def test_cloning_two_repositories(tmpdir):
    modules_directory = Path(tmpdir.mkdir('modules'))
    clone_repo(user='jakobgm',
      repository='color-schemes.astrality',
      modules_directory=modules_directory)
    clone_repo(user='jakobgm',
      repository='solar-desktop.astrality',
      modules_directory=modules_directory)
    github_user_directory = modules_directory / 'jakobgm'
    @py_assert3 = github_user_directory.iterdir
    @py_assert5 = @py_assert3()
    @py_assert7 = tuple(@py_assert5)
    @py_assert9 = len(@py_assert7)
    @py_assert12 = 2
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.iterdir\n}()\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py2':@pytest_ar._saferepr(github_user_directory) if 'github_user_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_user_directory) else 'github_user_directory',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


@pytest.mark.slow
def test_cloning_one_existent_and_one_non_existent_repo(tmpdir):
    modules_directory = Path(tmpdir.mkdir('modules'))
    clone_repo(user='jakobgm',
      repository='color-schemes.astrality',
      modules_directory=modules_directory)
    with pytest.raises(GithubModuleError):
        clone_repo(user='jakobgm',
          repository='i-will-never-create-this-repository',
          modules_directory=modules_directory)
    github_user_directory = modules_directory / 'jakobgm'
    @py_assert3 = github_user_directory.iterdir
    @py_assert5 = @py_assert3()
    @py_assert7 = tuple(@py_assert5)
    @py_assert9 = len(@py_assert7)
    @py_assert12 = 1
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.iterdir\n}()\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py2':@pytest_ar._saferepr(github_user_directory) if 'github_user_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_user_directory) else 'github_user_directory',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


@pytest.mark.slow
def test_cloning_the_same_repo_twice(tmpdir):
    modules_directory = Path(tmpdir.mkdir('modules'))
    clone_repo(user='jakobgm',
      repository='color-schemes.astrality',
      modules_directory=modules_directory)
    config_file = modules_directory / 'jakobgm' / 'color-schemes.astrality' / 'config.yml'
    config_file.write_text('user edited')
    clone_repo(user='jakobgm',
      repository='color-schemes.astrality',
      modules_directory=modules_directory)
    with open(config_file) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = 'user edited'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


@pytest.mark.slow
def test_clone_or_pull_repository_by_updating_outdated_repository(tmpdir):
    modules_directory = Path(tmpdir.mkdir('modules'))
    repo_dir = clone_repo(user='jakobgm',
      repository='color-schemes.astrality',
      modules_directory=modules_directory)
    result = run_shell(command='git reset --hard 2b8941a',
      timeout=5,
      fallback=False,
      working_directory=repo_dir)
    @py_assert2 = False
    @py_assert1 = result is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    readme = repo_dir / 'README.rst'
    @py_assert1 = readme.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(readme) if 'readme' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(readme) else 'readme',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    updated_repo_dir = clone_or_pull_repo(user='jakobgm',
      repository='color-schemes.astrality',
      modules_directory=modules_directory)
    @py_assert1 = updated_repo_dir == repo_dir
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (updated_repo_dir, repo_dir)) % {'py0':@pytest_ar._saferepr(updated_repo_dir) if 'updated_repo_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated_repo_dir) else 'updated_repo_dir',  'py2':@pytest_ar._saferepr(repo_dir) if 'repo_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo_dir) else 'repo_dir'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = readme.is_file
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(readme) if 'readme' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(readme) else 'readme',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None