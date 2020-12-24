# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_text_utils.py
# Compiled at: 2018-10-16 16:42:12
# Size of source mod 2**32: 3776 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, en_coref_md, pytest
from ..utils import text_utils

@pytest.fixture
def nlp():
    """Returns an instance of a spaCy's nlp object after replacing the default tokenizer with
    our modified one."""
    custom_nlp = en_coref_md.load()
    custom_nlp.tokenizer = text_utils.biomedical_tokenizer(custom_nlp)
    return custom_nlp


def test_biomedical_tokenizer(nlp):
    """Asserts that call to customized spaCy tokenizer returns the expected results.
    """
    blank_text = ''
    blank_expected = []
    simple_text = 'This is an easy test.'
    simple_expected = ['This', 'is', 'an', 'easy', 'test', '.']
    complicated_test = "This test's tokenizers handeling of very-tricky situations, 3X, more/or/less."
    complicated_expected = [
     'This', 'test', "'", 's', 'tokenizers', 'handeling', 'of',
     'very', '-', 'tricky', 'situations', ',', '3X', ',', 'more', '/', 'or',
     '/', 'less', '.']
    from_CHED_ds = 'The results have shown that the degradation product p-choloroaniline is not a significant factor in chlorhexidine-digluconate associated erosive cystitis.'
    from_CHED_ds_expected = [
     'The', 'results', 'have', 'shown', 'that', 'the', 'degradation',
     'product', 'p', '-', 'choloroaniline', 'is', 'not', 'a', 'significant',
     'factor', 'in', 'chlorhexidine', '-', 'digluconate', 'associated',
     'erosive', 'cystitis', '.']
    from_DISO_ds = 'Rats were treated with seven day intravenous infusion of fucoidan (30 micrograms h-1) or vehicle.'
    from_DISO_expected = [
     'Rats', 'were', 'treated', 'with', 'seven', 'day', 'intravenous',
     'infusion', 'of', 'fucoidan', '(', '30', 'micrograms', 'h', '-', '1',
     ')', 'or', 'vehicle', '.']
    from_LIVB_ds = 'Methanoregula formicica sp. nov., a methane-producing archaeon isolated from methanogenic sludge.'
    from_LIVB_ds_expected = [
     'Methanoregula', 'formicica', 'sp', '.', 'nov', '.', ',', 'a',
     'methane', '-', 'producing', 'archaeon', 'isolated', 'from',
     'methanogenic', 'sludge', '.']
    from_PRGE_ds = 'Here we report the cloning, expression, and biochemical characterization of the 32-kDa subunit of human (h) TFIID, termed hTAFII32.'
    from_PRGE_ds_expected = [
     'Here', 'we', 'report', 'the', 'cloning', ',', 'expression', ',',
     'and', 'biochemical', 'characterization', 'of', 'the', '32', '-',
     'kDa', 'subunit', 'of', 'human', '(', 'h', ')', 'TFIID', ',', 'termed',
     'hTAFII32', '.']
    @py_assert0 = [t.text for t in nlp(blank_text)]
    @py_assert2 = @py_assert0 == blank_expected
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, blank_expected)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(blank_expected) if 'blank_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_expected) else 'blank_expected'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = [t.text for t in nlp(simple_text)]
    @py_assert2 = @py_assert0 == simple_expected
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, simple_expected)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(simple_expected) if 'simple_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(simple_expected) else 'simple_expected'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = [t.text for t in nlp(complicated_test)]
    @py_assert2 = @py_assert0 == complicated_expected
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, complicated_expected)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(complicated_expected) if 'complicated_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complicated_expected) else 'complicated_expected'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = [t.text for t in nlp(from_CHED_ds)]
    @py_assert2 = @py_assert0 == from_CHED_ds_expected
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, from_CHED_ds_expected)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(from_CHED_ds_expected) if 'from_CHED_ds_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(from_CHED_ds_expected) else 'from_CHED_ds_expected'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = [t.text for t in nlp(from_DISO_ds)]
    @py_assert2 = @py_assert0 == from_DISO_expected
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, from_DISO_expected)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(from_DISO_expected) if 'from_DISO_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(from_DISO_expected) else 'from_DISO_expected'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = [t.text for t in nlp(from_LIVB_ds)]
    @py_assert2 = @py_assert0 == from_LIVB_ds_expected
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, from_LIVB_ds_expected)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(from_LIVB_ds_expected) if 'from_LIVB_ds_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(from_LIVB_ds_expected) else 'from_LIVB_ds_expected'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = [t.text for t in nlp(from_PRGE_ds)]
    @py_assert2 = @py_assert0 == from_PRGE_ds_expected
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, from_PRGE_ds_expected)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(from_PRGE_ds_expected) if 'from_PRGE_ds_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(from_PRGE_ds_expected) else 'from_PRGE_ds_expected'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None