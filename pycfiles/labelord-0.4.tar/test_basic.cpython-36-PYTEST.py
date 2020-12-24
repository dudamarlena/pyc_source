# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sushi/Projects/CTU/MI-PYT_B171/labelord/tests/tests_web/test_basic.py
# Compiled at: 2017-11-22 03:33:06
# Size of source mod 2**32: 882 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_homepage(client_maker):
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


def test_webhook_ping(client_maker, utils):
    client = client_maker('config_basic_web')
    result = client.post('/',
      data=(utils.load_data('pyplayground_ping_webhook')),
      headers={'X-Hub-Signature':'sha1=b7a7bacc401abde76ef575b2f3f436ae28aad8ec', 
     'X-GitHub-Event':'ping', 
     'X-Github-Delivery':'64603d10-a3bb-11e7-82bc-0764f2d1a900', 
     'X-Request-Id':'e118e5e1-6763-4854-8b19-595c27b00135'})
    @py_assert1 = result.status
    @py_assert4 = '200 OK'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None