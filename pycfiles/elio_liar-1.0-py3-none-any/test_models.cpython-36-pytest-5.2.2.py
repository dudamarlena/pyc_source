# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py
# Compiled at: 2019-10-21 04:50:21
# Size of source mod 2**32: 2113 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from liar.model.raw import raw_collection
from liar.model.blurb import blurb_collection
from liar.model.business import business_model
from liar.model.common import common_collection
from liar.model.date import date_collection
from liar.model.float import float_collection
from liar.model.int import int_collection
from liar.model.location import standard_address_model
from liar.model.marketing import marketing_model
from liar.model.personal import personal_model
from liar.model.primitive import primitive_collection
from liar.model.time import time_collection
from liar.ijusthelp import rewrite_dict
from liar.iamaliar import IAmALiar
number_records = 3
maker = IAmALiar(number_records)

class TestClassModels:

    def test_raw(self):
        d = maker.get_data(raw_collection)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=26)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_blurb(self):
        d = maker.get_data(blurb_collection)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=30)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_business(self):
        d = maker.get_data(business_model)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=34)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_common(self):
        d = maker.get_data(common_collection)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=38)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_date(self):
        d = maker.get_data(date_collection)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=42)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_float(self):
        d = maker.get_data(float_collection)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=46)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_int(self):
        d = maker.get_data(int_collection)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=50)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_location(self):
        d = maker.get_data(standard_address_model)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=54)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_marketing(self):
        d = maker.get_data(marketing_model)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=58)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_personal(self):
        d = maker.get_data(personal_model)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=62)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_primitive(self):
        d = maker.get_data(primitive_collection)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=66)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_time(self):
        d = maker.get_data(time_collection)
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_models.py', lineno=70)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None