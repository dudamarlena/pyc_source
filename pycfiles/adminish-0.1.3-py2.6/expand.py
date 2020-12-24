# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/adminish/expand.py
# Compiled at: 2010-02-03 12:26:21
from dottedish import api

def _expand_id(id, doc):
    eid = []
    if '*' in id:
        (prefix, suffix) = id.split('*')
        items = api.dotted(doc)[prefix[:-1]]
        key = prefix + '%(n)s' + suffix
        return (
         '%%%%(%s)s' % key, len(items))
    else:
        return (
         '%%%%(%s)s' % id, 1)


def _get_id(i, d, doc):
    id = ''
    while i < len(d):
        if d[i] == ')':
            i += 1
            return (
             i, _expand_id(id, doc))
        id += d[i]
        i += 1
    else:
        raise ValueError


def expand(d, doc):
    i = 0
    out = ''
    num_items = 1
    while i < len(d):
        if d[i] == '%':
            i += 2
            (i, id) = _get_id(i, d, doc)
            out += id[0]
            num_items = id[1]
        else:
            out += d[i]
        i += 1

    return (
     out, num_items)


if __name__ == '__main__':
    import unittest
    tests = [('this %(var)s is %(cool)s yes?', None, 'this %(var)s is %(cool)s yes?'),
     (
      '^ %(foo.*.so)s $', {'foo': [{'so': 1}, {'so': 2}]}, '^ %(foo.*.so)s $')]

    class TestExpand(unittest.TestCase):

        def test(self):
            for test in tests:
                self.assertEqual(expand(test[0], test[1]), test[2])


    unittest.main()