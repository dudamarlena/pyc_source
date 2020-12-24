# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py
# Compiled at: 2019-10-21 04:50:21
# Size of source mod 2**32: 3730 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from liar.ijusthelp import rewrite_dict
from liar.iamaliar import IAmALiar
from liar.model.blurb import blurb

class TestClassIBlurb:
    small_number_records = 30
    blurb_maker = IAmALiar(small_number_records)
    test_blurb = rewrite_dict(blurb, {'name':'test_blurb', 
     'language':'english',  'min':800,  'max':1000})

    def test_plaintext_phrase(self):
        plaintext_phrase = rewrite_dict(self.test_blurb, {'method': 'plaintext_phrase'})
        d = self.blurb_maker.get_data([plaintext_phrase])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=23)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=24)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '\n'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=25)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '.'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=26)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_plaintext_title(self):
        plaintext_title = rewrite_dict(self.test_blurb, {'method': 'plaintext_title'})
        d = self.blurb_maker.get_data([plaintext_title])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=33)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=34)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '\n'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=35)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_plaintext_sentence(self):
        plaintext_sentence = rewrite_dict(self.test_blurb, {'method': 'plaintext_sentence'})
        d = self.blurb_maker.get_data([plaintext_sentence])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=42)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=43)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '\n'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=44)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '.'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=45)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_plaintext_sentences(self):
        plaintext_sentences = rewrite_dict(self.test_blurb, {'method': 'plaintext_sentences'})
        d = self.blurb_maker.get_data([plaintext_sentences])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=52)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<li>'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=53)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '\n'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=54)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '.'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=55)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_plaintext_bullets(self):
        plaintext_bullets = rewrite_dict(self.test_blurb, {'method': 'plaintext_bullets'})
        d = self.blurb_maker.get_data([plaintext_bullets])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=62)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<li>'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=63)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '\n'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=64)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_plaintext_paragraphs(self):
        plaintext_paragraphs = rewrite_dict(self.test_blurb, {'method': 'plaintext_paragraphs'})
        d = self.blurb_maker.get_data([plaintext_paragraphs])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=71)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<p>'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 not in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=72)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = '\n'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=73)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_html_paragraph(self):
        html_paragraph = rewrite_dict(self.test_blurb, {'method': 'html_paragraph'})
        d = self.blurb_maker.get_data([html_paragraph])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=80)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<p>'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=81)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_html_bullets(self):
        html_bullets = rewrite_dict(self.test_blurb, {'method': 'html_bullets'})
        d = self.blurb_maker.get_data([html_bullets])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=86)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<li>'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=87)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_html_paragraphs(self):
        html_paragraphs = rewrite_dict(self.test_blurb, {'method': 'html_paragraphs'})
        d = self.blurb_maker.get_data([html_paragraphs])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=94)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<p>'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=95)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_html(self):
        html = rewrite_dict(self.test_blurb, {'method': 'html'})
        d = self.blurb_maker.get_data([html])
        @py_assert2 = len(d)
        @py_assert6 = self.small_number_records
        @py_assert4 = @py_assert2 == @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=100)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.small_number_records\n}', ), (@py_assert2, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '<p>'
        @py_assert3 = d[0]['test_blurb']
        @py_assert2 = @py_assert0 in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_iblurb.py', lineno=101)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None