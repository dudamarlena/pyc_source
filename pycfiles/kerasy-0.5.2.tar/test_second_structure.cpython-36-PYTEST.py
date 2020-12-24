# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/Bio/test_second_structure.py
# Compiled at: 2020-05-11 01:44:04
# Size of source mod 2**32: 952 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from kerasy.Bio.second_structure import Nussinov, Zuker
from kerasy.utils import generateSeq
len_sequences = 100

def get_test_data():
    sequence = generateSeq(size=len_sequences, nucleic_acid='DNA',
      weights=None,
      seed=123)
    sequence = ''.join(sequence)
    return sequence


def test_nussinov():
    sequence = get_test_data()
    model = Nussinov()
    model.load_params()
    score, structure_info = model.predict(sequence, verbose=(-1), ret_val=True)
    stack = []
    for i, symbol in enumerate(structure_info):
        if symbol == '(':
            stack.append(i)
        else:
            if symbol == ')':
                @py_assert1 = model.is_bp
                @py_assert3 = sequence[stack.pop(-1)]
                @py_assert5 = sequence[i]
                @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
                if not @py_assert7:
                    @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_bp\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format9))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_zuker():
    sequence = get_test_data()
    model = Zuker()
    model.load_params()
    score, structure_info = model.predict(sequence, verbose=(-1), ret_val=True)