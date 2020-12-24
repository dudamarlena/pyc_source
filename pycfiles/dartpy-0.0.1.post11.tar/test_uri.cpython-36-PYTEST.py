# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/dev/prl/dart/pybind11/python/tests/unit/common/test_uri.py
# Compiled at: 2019-01-11 23:38:31
# Size of source mod 2**32: 744 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, platform, pytest
from dartpy.common import Uri

def test_from_string_valid_uri_returns_true():
    uri = Uri()
    @py_assert1 = uri.fromString
    @py_assert3 = 'ftp://ftp.is.co.za/rfc/rfc1808.txt'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = True
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.fromString\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = uri.fromString
    @py_assert3 = 'http://www.ietf.org/rfc/rfc2396.txt'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = True
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.fromString\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = uri.fromString
    @py_assert3 = 'ldap://[2001:db8::7]/c=GB?objectClass?one'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = True
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.fromString\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = uri.fromString
    @py_assert3 = 'mailto:John.Doe@example.com'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = True
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.fromString\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = uri.fromString
    @py_assert3 = 'news:comp.infosystems.www.servers.unix'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = True
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.fromString\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = uri.fromString
    @py_assert3 = 'tel:+1-816-555-1212'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = True
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.fromString\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = uri.fromString
    @py_assert3 = 'telnet://192.0.2.16:80/'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = True
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.fromString\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = uri.fromString
    @py_assert3 = 'urn:oasis:names:specification:docbook:dtd:xml:4.1.2'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = True
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.fromString\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


if __name__ == '__main__':
    pytest.main()