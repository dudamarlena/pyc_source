# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_refcounting.py
# Compiled at: 2018-03-07 22:50:17
# Size of source mod 2**32: 705 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from taskloaf.refcounting import *
from fixtures import w

def test_refcount_simple():
    rc = RefCount()
    @py_assert1 = rc.alive
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.alive\n}()\n}') % {'py0':@pytest_ar._saferepr(rc) if 'rc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rc) else 'rc',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    rc.dec_ref(0, 0)
    @py_assert1 = rc.alive
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.alive\n}()\n}') % {'py0':@pytest_ar._saferepr(rc) if 'rc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rc) else 'rc',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_refcount_dead():
    rc = RefCount()
    rc.dec_ref(0, 2)
    rc.dec_ref(1, 0)
    rc.dec_ref(1, 0)
    @py_assert1 = rc.alive
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.alive\n}()\n}') % {'py0':@pytest_ar._saferepr(rc) if 'rc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rc) else 'rc',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_refcount_alive():
    rc = RefCount()
    rc.dec_ref(0, 2)
    rc.dec_ref(1, 0)
    rc.dec_ref(1, 1)
    @py_assert1 = rc.alive
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.alive\n}()\n}') % {'py0':@pytest_ar._saferepr(rc) if 'rc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rc) else 'rc',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_decref_encode(w):
    b = DecRefMsg.serialize([2, 3, 4]).to_bytes()
    m = taskloaf.message_capnp.Message.from_bytes(b)
    _id, gen, n_children = DecRefMsg.deserialize(w, m)
    @py_assert2 = 2
    @py_assert1 = _id == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (_id, @py_assert2)) % {'py0':@pytest_ar._saferepr(_id) if '_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_id) else '_id',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 3
    @py_assert1 = gen == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (gen, @py_assert2)) % {'py0':@pytest_ar._saferepr(gen) if 'gen' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gen) else 'gen',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 4
    @py_assert1 = n_children == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (n_children, @py_assert2)) % {'py0':@pytest_ar._saferepr(n_children) if 'n_children' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n_children) else 'n_children',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None