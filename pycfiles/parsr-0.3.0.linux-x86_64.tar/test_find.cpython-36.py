# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/query/tests/test_find.py
# Compiled at: 2019-10-05 07:59:22
# Size of source mod 2**32: 1038 bytes
from parsr.query import Entry
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

def test_find_leaves():
    res = complex_tree.find('puppy')
    if not len(res) == 2:
        raise AssertionError
    else:
        assert res[0].name == 'puppy'
        assert res[1].name == 'puppy'


def test_find_roots():
    res = complex_tree.find('puppy', roots=True)
    if not len(res) == 1:
        raise AssertionError
    elif not res[0].name == 'root':
        raise AssertionError


def test_find_chain():
    res = complex_tree.find('dog').find('puppy')
    assert len(res) == 2