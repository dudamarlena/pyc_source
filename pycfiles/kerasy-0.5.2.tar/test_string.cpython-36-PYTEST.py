# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/Bio/test_string.py
# Compiled at: 2020-05-11 00:24:08
# Size of source mod 2**32: 658 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.Bio.string import ALPHABETS, StringSearch
num_charactors = 10
len_string = 100000
len_query = 5

def get_test_data():
    rnd = np.random.RandomState(1)
    string = ''.join(rnd.choice(ALPHABETS[:num_charactors], len_string))
    query = ''.join(rnd.choice(ALPHABETS[:num_charactors], len_query))
    return (string, query)


def test_string_search():
    string, query = get_test_data()
    db = StringSearch()
    db.build(string)
    positions = db.search(query)
    if isinstance(positions, np.ndarray):
        @py_assert1 = [string[pos:pos + len_query] == query for pos in positions]
        @py_assert3 = any(@py_assert1)
        if not @py_assert3:
            @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(any) if 'any' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(any) else 'any',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None