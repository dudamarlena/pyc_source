# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/constants/tests/test_basic.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 5111 bytes
from __future__ import absolute_import, division, print_function
import six, numpy as np
from nose.tools import assert_equal
from skxray.core.constants.basic import BasicElement, element, basic

def smoke_test_element_creation():
    elements = sorted([elm for abbrev, elm in six.iteritems(basic) if isinstance(abbrev, int)])
    for e in elements:
        sym = e.sym
        name = e.name
        inits = [
         sym, sym.upper(), sym.lower(), sym.swapcase(), name,
         name.upper(), name.lower(), name.swapcase()]
        for init in inits:
            elem = BasicElement(init)

        elem = BasicElement(e.Z)
        str(elem)
        for field in element._fields:
            tuple_attr = getattr(basic[e.Z], field)
            elem_attr_dct = elem[str(field)]
            elem_attr = getattr(elem, field)
            try:
                if np.isnan(tuple_attr):
                    continue
            except TypeError:
                pass

            assert_equal(elem_attr_dct, tuple_attr)
            assert_equal(elem_attr, tuple_attr)
            assert_equal(elem_attr_dct, elem_attr)

    for e1, e2 in zip(elements, elements[1:]):
        assert_equal(e1.__lt__(e2), True)
        assert_equal(e1 < e2, True)
        assert_equal(e1.__eq__(e2), False)
        assert_equal(e1 == e2, False)
        assert_equal(e1 >= e2, False)
        assert_equal(e1 > e2, False)
        assert_equal(e2 < e1, False)
        assert_equal(e2.__lt__(e1), False)
        assert_equal(e2 <= e1, False)
        assert_equal(e2.__eq__(e1), False)
        assert_equal(e2 == e1, False)
        assert_equal(e2 >= e1, True)
        assert_equal(e2 > e1, True)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)