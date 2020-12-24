# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sushi/Projects/CTU/MI-PYT_B171/labelord/tests/tests_unit/test_github.py
# Compiled at: 2017-11-22 03:33:06
# Size of source mod 2**32: 5347 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from labelord.github import GitHub, GitHubError
LABELORD_REPO = 'MarekSuchanek/labelord'
UNEXISTING_REPO = 'MarekSuchanek/adsw51dwa1d5123aa'

def test_list_repositories(github):
    repositories = github.list_repositories()
    @py_assert2 = len(repositories)
    @py_assert5 = 49
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(repositories) if 'repositories' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repositories) else 'repositories',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = LABELORD_REPO in repositories
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (LABELORD_REPO, repositories)) % {'py0':@pytest_ar._saferepr(LABELORD_REPO) if 'LABELORD_REPO' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(LABELORD_REPO) else 'LABELORD_REPO',  'py2':@pytest_ar._saferepr(repositories) if 'repositories' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repositories) else 'repositories'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_list_repositories_with_bad_token(github_bad_token):
    with pytest.raises(GitHubError) as (err):
        github_bad_token.list_repositories()
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 401
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Bad credentials'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_list_labels_from_existing_repo(github):
    labels = github.list_labels(LABELORD_REPO)
    @py_assert2 = len(labels)
    @py_assert5 = 8
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(labels) if 'labels' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(labels) else 'labels',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = labels['bug']
    @py_assert3 = 'ee0701'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_list_labels_from_unexisting_repo(github):
    with pytest.raises(GitHubError) as (err):
        github.list_labels(UNEXISTING_REPO)
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 404
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Not Found'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_list_labels_with_bad_token(github_bad_token):
    with pytest.raises(GitHubError) as (err):
        github_bad_token.list_labels(LABELORD_REPO)
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 401
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Bad credentials'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_create_label_for_existing_repo(github):
    github.create_label(LABELORD_REPO, 'Testing', 'aaaaaa')


def test_create_label_that_already_exists(github):
    with pytest.raises(GitHubError) as (err):
        github.create_label(LABELORD_REPO, 'Testing', 'aaaaaa')
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 422
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Validation Failed'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_create_label_with_weird_color(github):
    with pytest.raises(GitHubError) as (err):
        github.create_label(LABELORD_REPO, 'Testing', 'aaaxxx')
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 422
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Validation Failed'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_create_label_for_unexisting_repo(github):
    with pytest.raises(GitHubError) as (err):
        github.create_label(UNEXISTING_REPO, 'Testing', 'aaaaaa')
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 404
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Not Found'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_create_label_with_bad_token(github_bad_token):
    with pytest.raises(GitHubError) as (err):
        github_bad_token.list_labels(LABELORD_REPO)
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 401
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Bad credentials'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_update_label_for_existing_repo(github):
    github.update_label(LABELORD_REPO, 'Testing 2', 'ababab', 'Testing')


def test_update_label_that_doesnt_exist(github):
    with pytest.raises(GitHubError) as (err):
        github.update_label(LABELORD_REPO, 'Testing', 'aaaaaa')
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 404
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Not Found'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_update_label_with_weird_color(github):
    with pytest.raises(GitHubError) as (err):
        github.update_label(LABELORD_REPO, 'Testing 2', 'aaaxxx')
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 422
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Validation Failed'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_update_label_for_unexisting_repo(github):
    with pytest.raises(GitHubError) as (err):
        github.update_label(UNEXISTING_REPO, 'Testing 2', 'aaaaaa')
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 404
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Not Found'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_delete_label_for_existing_repo(github):
    github.delete_label(LABELORD_REPO, 'Testing 2')


def test_delete_label_that_doesnt_exist(github):
    with pytest.raises(GitHubError) as (err):
        github.delete_label(LABELORD_REPO, 'Testing')
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 404
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Not Found'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_delete_label_for_unexisting_repo(github):
    with pytest.raises(GitHubError) as (err):
        github.delete_label(UNEXISTING_REPO, 'Testing 2')
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 404
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Not Found'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_error_properties(github):
    with pytest.raises(GitHubError) as (err):
        github.delete_label(UNEXISTING_REPO, 'Testing 2')
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.status_code
    @py_assert6 = 404
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.status_code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.message
    @py_assert6 = 'Not Found'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = err.value
    @py_assert3 = @py_assert1.code_message
    @py_assert6 = '404 - Not Found'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.code_message\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = err.value
    @py_assert4 = str(@py_assert2)
    @py_assert7 = 'GitHub: ERROR 404 - Not Found'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


@pytest.mark.parametrize(('data', 'signature', 'secret', 'encoding'), [
 (
  '{"data": "thisData"}'.encode('utf-8'),
  'sha1=ff00f668ad2b48568d5c72c01bd9b3b3c12032d6', 'key1', 'utf-8'),
 (
  'someMoreDataAsUTF8String'.encode('utf-8'),
  'sha1=7badf000d5b4eedfc0f40e7fe29c3f660849e081', 'key1', 'utf-8'),
 (
  '{"data": "thisData"}'.encode('utf-8'),
  'sha1=054ffbba526d7e94e1c9f99b6b33993dbd39b6c3', 'key2', 'utf-8'),
 (
  'someMoreDataAsUTF8String'.encode('utf-8'),
  'sha1=467a48608419b56e5ada01496baf4b12ef632304', 'key2', 'utf-8'),
 (
  ''.encode('utf-8'),
  'sha1=94a32c46d6a6ea7b9af8d0a4d134a9028d6e3124', 'key2', 'utf-8'),
 (
  'someMoreDataAsCP1250String'.encode('cp1250'),
  'sha1=993fc6ccf9fa1cfd650825d886d5343549448e52', 'key1', 'cp1250'),
 (
  '{"data": "thisData"}'.encode('cp1250'),
  'sha1=054ffbba526d7e94e1c9f99b6b33993dbd39b6c3', 'key2', 'cp1250')])
def test_verify_webhook_signature_correct(data, signature, secret, encoding):
    @py_assert1 = GitHub.webhook_verify_signature
    @py_assert7 = @py_assert1(data, signature, secret, encoding)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.webhook_verify_signature\n}(%(py3)s, %(py4)s, %(py5)s, %(py6)s)\n}') % {'py0':@pytest_ar._saferepr(GitHub) if 'GitHub' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GitHub) else 'GitHub',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py4':@pytest_ar._saferepr(signature) if 'signature' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(signature) else 'signature',  'py5':@pytest_ar._saferepr(secret) if 'secret' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(secret) else 'secret',  'py6':@pytest_ar._saferepr(encoding) if 'encoding' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(encoding) else 'encoding',  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert7 = None