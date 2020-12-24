# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sushi/Projects/CTU/MI-PYT_B171/labelord/tests/tests_web/test_index.py
# Compiled at: 2017-11-22 03:33:06
# Size of source mod 2**32: 1669 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_app_info(client_maker):
    client = client_maker('config_basic_web')
    result = client.get('/')
    @py_assert1 = result.status
    @py_assert4 = '200 OK'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    page = result.data.decode('utf-8')
    @py_assert0 = 'labelord'
    @py_assert4 = page.lower
    @py_assert6 = @py_assert4()
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.lower\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'master-to-master'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'webhook'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'GitHub'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_repos_list(client_maker):
    client = client_maker('config_basic_web')
    result = client.get('/')
    @py_assert1 = result.status
    @py_assert4 = '200 OK'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    page = result.data.decode('utf-8')
    @py_assert0 = 'MarekSuchanek/pyplayground'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'MarekSuchanek/repocribro'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'MarekSuchanek/labelord'
    @py_assert2 = @py_assert0 not in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_repos_list_other(client_maker):
    client = client_maker('config_3repos_web')
    result = client.get('/')
    @py_assert1 = result.status
    @py_assert4 = '200 OK'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    page = result.data.decode('utf-8')
    @py_assert0 = 'MarekSuchanek/pyplayground'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'MarekSuchanek/repocribro'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'MarekSuchanek/labelord'
    @py_assert2 = @py_assert0 not in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'MarekSuchanek/maze'
    @py_assert2 = @py_assert0 in page
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, page)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_repos_links(client_maker):
    client = client_maker('config_basic_web')
    result = client.get('/')
    @py_assert1 = result.status
    @py_assert4 = '200 OK'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    page = result.data.decode('utf-8')

    def gh_link(reposlug):
        return 'https://github.com/' + reposlug

    @py_assert1 = 'MarekSuchanek/pyplayground'
    @py_assert3 = gh_link(@py_assert1)
    @py_assert5 = @py_assert3 in page
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} in %(py6)s', ), (@py_assert3, page)) % {'py0':@pytest_ar._saferepr(gh_link) if 'gh_link' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gh_link) else 'gh_link',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = 'MarekSuchanek/repocribro'
    @py_assert3 = gh_link(@py_assert1)
    @py_assert5 = @py_assert3 in page
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} in %(py6)s', ), (@py_assert3, page)) % {'py0':@pytest_ar._saferepr(gh_link) if 'gh_link' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gh_link) else 'gh_link',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = 'MarekSuchanek/labelord'
    @py_assert3 = gh_link(@py_assert1)
    @py_assert5 = @py_assert3 not in page
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} not in %(py6)s', ), (@py_assert3, page)) % {'py0':@pytest_ar._saferepr(gh_link) if 'gh_link' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gh_link) else 'gh_link',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(page) if 'page' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(page) else 'page'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None