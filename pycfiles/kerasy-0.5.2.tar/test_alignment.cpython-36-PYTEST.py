# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/Bio/test_alignment.py
# Compiled at: 2020-05-10 06:35:01
# Size of source mod 2**32: 1199 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from kerasy.utils import generateSeq
from kerasy.Bio.alignment import NeedlemanWunshGotoh, SmithWaterman, BackwardNeedlemanWunshGotoh, PairHMM
len_sequences = 30

def get_test_data():
    seqX, seqY = generateSeq(size=(2, len_sequences), nucleic_acid='DNA',
      weights=None,
      seed=123)
    return (seqX, seqY)


def _test_alignment(Model, path='alignment.json', **kwargs):
    seqX, seqY = get_test_data()
    model = Model(**kwargs)
    model.load_params()
    score = model.align_score(seqX, seqY, verbose=(-1))
    model.save_params(path)
    model_ = Model(**kwargs)
    model_.load_params(path)
    score_ = model_.align_score(seqX, seqY, verbose=(-1))
    os.remove(path)
    @py_assert1 = score == score_
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (score, score_)) % {'py0':@pytest_ar._saferepr(score) if 'score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(score) else 'score',  'py2':@pytest_ar._saferepr(score_) if 'score_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(score_) else 'score_'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_needleman_wunsh_gotoh():
    _test_alignment(NeedlemanWunshGotoh)


def test_smith_waterman():
    _test_alignment(SmithWaterman)


def test_backward_needleman_wunsh_gotoh():
    _test_alignment(BackwardNeedlemanWunshGotoh)


def test_pair_hmm():
    _test_alignment(PairHMM)