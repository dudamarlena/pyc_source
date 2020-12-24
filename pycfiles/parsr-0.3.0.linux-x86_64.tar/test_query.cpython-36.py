# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/query/tests/test_query.py
# Compiled at: 2019-05-28 16:57:56
# Size of source mod 2**32: 1605 bytes
from parsr.query import all_, any_, lt, Entry, from_dict, startswith, endswith
simple_data = {'a':3, 
 'b':[
  'four', 'five'], 
 'c':[
  9, 15], 
 'd':{'e': 9.7}}
complex_tree = Entry(name='root', attrs=[
 1, 2, 3, 4],
  children=[
 Entry(name='child', attrs=[1, 1, 2]),
 Entry(name='child', attrs=[1, 1, 2, 3, 5]),
 Entry(name='child', attrs=[1, 1, 3, 5, 9]),
 Entry(name='dog', attrs=['woof'], children=[
  Entry(name='puppy', attrs=['smol']),
  Entry(name='puppy', attrs=['fluffy']),
  Entry(name='kitten', attrs=['wut'])])])

def test_from_dict():
    n = from_dict(simple_data)
    if not n:
        raise AssertionError
    elif not len(n) == 4:
        raise AssertionError


def test_values():
    n = from_dict(simple_data)
    if not n['a'].value == 3:
        raise AssertionError
    else:
        if not n['b'].string_value == 'four five':
            raise AssertionError
        else:
            if not n['b'].value == 'four five':
                raise AssertionError
            elif not n['c'].string_value == '9 15':
                raise AssertionError
            assert n['c'].value == '9 15'
        assert n['d']['e'].value == 9.7


def test_complex():
    t = complex_tree
    if not len(t['child']) == 3:
        raise AssertionError
    else:
        if not len(t[('child', 3)]) == 2:
            raise AssertionError
        else:
            if not len(t[('child', all_(lt(3)))]) == 1:
                raise AssertionError
            else:
                if not len(t[('child', any_(1))]) == 3:
                    raise AssertionError
                else:
                    assert len(t[('child', any_(9))]) == 1
                    assert len(t[('child', any_(2))]) == 2
                assert len(t['dog']['puppy']) == 2
            assert len(t[(startswith('chi') & endswith('ld'))]) == 3
        assert len(t[(startswith('chi') | startswith('do'))]) == 4