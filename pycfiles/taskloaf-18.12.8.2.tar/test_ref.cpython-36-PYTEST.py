# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_ref.py
# Compiled at: 2018-03-14 15:18:07
# Size of source mod 2**32: 5837 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, gc, pickle, pytest, asyncio
from taskloaf.cluster import cluster
from taskloaf.object_ref import *
from taskloaf.refcounting import RefCopyException
from fixtures import w

def syncawait(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def test_make_ref(w):
    r = put(w, [12, 3, 4])
    @py_assert2 = r.get
    @py_assert4 = @py_assert2()
    @py_assert6 = syncawait(@py_assert4)
    @py_assert9 = [
     12, 3, 4]
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(syncawait) if 'syncawait' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syncawait) else 'syncawait',  'py1':@pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_objref_get(w):
    r = put(w, [12, 3, 4]).convert()
    @py_assert2 = r.get
    @py_assert4 = @py_assert2()
    @py_assert6 = syncawait(@py_assert4)
    @py_assert9 = [
     12, 3, 4]
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(syncawait) if 'syncawait' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syncawait) else 'syncawait',  'py1':@pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    w.object_cache.clear()
    @py_assert2 = r.get
    @py_assert4 = @py_assert2()
    @py_assert6 = syncawait(@py_assert4)
    @py_assert9 = [
     12, 3, 4]
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(syncawait) if 'syncawait' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syncawait) else 'syncawait',  'py1':@pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_objref_delete(w):

    def check_norefs(v):
        @py_assert1 = w.allocator
        @py_assert3 = @py_assert1.empty
        @py_assert5 = @py_assert3()
        @py_assert7 = @py_assert5 == v
        if not @py_assert7:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.allocator\n}.empty\n}()\n} == %(py8)s', ), (@py_assert5, v)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(v) if 'v' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(v) else 'v'}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert2 = w.ref_manager
        @py_assert4 = @py_assert2.entries
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        @py_assert13 = @py_assert8 == v
        if not @py_assert13:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.ref_manager\n}.entries\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('(%(py12)s) == %(py14)s', ), (@py_assert8, v)) % {'py12':@py_format11,  'py14':@pytest_ar._saferepr(v) if 'v' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(v) else 'v'}
            @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
            raise AssertionError(@pytest_ar._format_explanation(@py_format17))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert13 = None

    check_norefs(True)
    r = put(w, 10)
    check_norefs(True)
    objr = r.convert()
    check_norefs(False)
    del r
    check_norefs(False)
    del objr
    check_norefs(True)


def test_ref_conversion_caching(w):
    r = put(w, [12, 3, 4])
    objr = r.convert()
    @py_assert3 = isinstance(objr, ObjectRef)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(objr) if 'objr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(objr) else 'objr',  'py2':@pytest_ar._saferepr(ObjectRef) if 'ObjectRef' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ObjectRef) else 'ObjectRef',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    objr2 = r.convert()
    @py_assert1 = objr is objr2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (objr, objr2)) % {'py0':@pytest_ar._saferepr(objr) if 'objr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(objr) else 'objr',  'py2':@pytest_ar._saferepr(objr2) if 'objr2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(objr2) else 'objr2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_ref_pickle_exception(w):
    r = put(w, [12, 3, 4])
    objr = r.convert()
    with pytest.raises(RefCopyException):
        pickle.dumps(r)
    with pytest.raises(RefCopyException):
        pickle.dumps(objr)


def ref_serialization_tester(w, sfnc, dfnc):
    @py_assert2 = w.ref_manager
    @py_assert4 = @py_assert2.entries
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 0
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.ref_manager\n}.entries\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    ref = put(w, 10)
    objr = ref.convert()
    @py_assert2 = w.ref_manager
    @py_assert4 = @py_assert2.entries
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.ref_manager\n}.entries\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    ref_bytes = sfnc(objr)
    del ref
    del objr
    @py_assert2 = w.ref_manager
    @py_assert4 = @py_assert2.entries
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.ref_manager\n}.entries\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    objr2 = dfnc(w, ref_bytes)
    @py_assert2 = objr2.get
    @py_assert4 = @py_assert2()
    @py_assert6 = syncawait(@py_assert4)
    @py_assert9 = 10
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(syncawait) if 'syncawait' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syncawait) else 'syncawait',  'py1':@pytest_ar._saferepr(objr2) if 'objr2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(objr2) else 'objr2',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    del w.object_cache[objr2.key()]
    @py_assert2 = objr2.get
    @py_assert4 = @py_assert2()
    @py_assert6 = syncawait(@py_assert4)
    @py_assert9 = 10
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(syncawait) if 'syncawait' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syncawait) else 'syncawait',  'py1':@pytest_ar._saferepr(objr2) if 'objr2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(objr2) else 'objr2',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    del objr2
    gc.collect()
    @py_assert2 = w.ref_manager
    @py_assert4 = @py_assert2.entries
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 0
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.ref_manager\n}.entries\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = w.object_cache
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.object_cache\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def ref_serialize(ref):
    return ObjectMsg.serialize([ref, b'']).to_bytes()


def ref_deserialize(w, ref_b):
    m = taskloaf.message_capnp.Message.from_bytes(ref_b)
    return ObjectMsg.deserialize(w, m)[0]


def test_objref_encode_capnp(w):
    ref_serialization_tester(w, ref_serialize, ref_deserialize)


def test_put_encode(w):
    ref = put(w, 10)
    ref2 = ref_deserialize(w, ref_serialize(ref))
    @py_assert2 = ref2.get
    @py_assert4 = @py_assert2()
    @py_assert6 = syncawait(@py_assert4)
    @py_assert9 = 10
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(syncawait) if 'syncawait' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syncawait) else 'syncawait',  'py1':@pytest_ar._saferepr(ref2) if 'ref2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref2) else 'ref2',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_put_bytes(w):
    x = bytes([10, 11])
    for blob in [x, memoryview(x)]:
        ref = put(w, blob).convert()
        blob2 = syncawait(ref.get())
        @py_assert1 = blob == blob2
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (blob, blob2)) % {'py0':@pytest_ar._saferepr(blob) if 'blob' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blob) else 'blob',  'py2':@pytest_ar._saferepr(blob2) if 'blob2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blob2) else 'blob2'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None


def test_alloc(w):
    ref = alloc(w, 100)
    @py_assert3 = ref.get
    @py_assert5 = @py_assert3()
    @py_assert7 = syncawait(@py_assert5)
    @py_assert9 = len(@py_assert7)
    @py_assert12 = 100
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.get\n}()\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(syncawait) if 'syncawait' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syncawait) else 'syncawait',  'py2':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


async def wait_to_die():
    for i in range(2500):
        await asyncio.sleep(0.01)


def test_submit_ref_work():

    async def f(w):
        ref = put(w, 1)
        @py_assert1 = ref._id
        @py_assert4 = 0
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

        async def g(w):
            @py_assert1 = ref.ref
            @py_assert3 = @py_assert1._id
            @py_assert6 = 0
            @py_assert5 = @py_assert3 == @py_assert6
            if not @py_assert5:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ref\n}._id\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
            submit_ref_work(w, 0, taskloaf.worker.shutdown)

        submit_ref_work(w, 1, g)
        await wait_to_die()

    cluster(2, f)


def test_get():
    one_serialized = pickle.dumps(1)

    async def f(w):
        ref = put(w, 1)
        ref2 = alloc(w, len(one_serialized))
        buf = await ref2.get()
        buf[:] = one_serialized
        @py_assert0 = await ref.get()
        @py_assert3 = 1
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = await ref2.get()
        @py_assert2 = @py_assert0 == one_serialized
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, one_serialized)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(one_serialized) if 'one_serialized' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one_serialized) else 'one_serialized'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

        async def g(w):
            @py_assert0 = await ref.get()
            @py_assert3 = 1
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            @py_assert1 = ref.key
            @py_assert3 = @py_assert1()
            @py_assert7 = w.object_cache
            @py_assert5 = @py_assert3 in @py_assert7
            if not @py_assert5:
                @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.key\n}()\n} in %(py8)s\n{%(py8)s = %(py6)s.object_cache\n}', ), (@py_assert3, @py_assert7)) % {'py0':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py8':@pytest_ar._saferepr(@py_assert7)}
                @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                raise AssertionError(@pytest_ar._format_explanation(@py_format11))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
            @py_assert0 = await ref2.get()
            @py_assert2 = @py_assert0 == one_serialized
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, one_serialized)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(one_serialized) if 'one_serialized' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one_serialized) else 'one_serialized'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            @py_assert1 = ref2.key
            @py_assert3 = @py_assert1()
            @py_assert7 = w.object_cache
            @py_assert5 = @py_assert3 in @py_assert7
            if not @py_assert5:
                @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.key\n}()\n} in %(py8)s\n{%(py8)s = %(py6)s.object_cache\n}', ), (@py_assert3, @py_assert7)) % {'py0':@pytest_ar._saferepr(ref2) if 'ref2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref2) else 'ref2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py8':@pytest_ar._saferepr(@py_assert7)}
                @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                raise AssertionError(@pytest_ar._format_explanation(@py_format11))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
            v1 = asyncio.ensure_future(ref._remote_get())
            await asyncio.sleep(0)
            @py_assert1 = w.object_cache[ref.key()]
            @py_assert4 = asyncio.Future
            @py_assert6 = isinstance(@py_assert1, @py_assert4)
            if not @py_assert6:
                @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py2)s, %(py5)s\n{%(py5)s = %(py3)s.Future\n})\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(asyncio) if 'asyncio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(asyncio) else 'asyncio',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert4 = @py_assert6 = None
            @py_assert0 = await ref.get()
            @py_assert3 = 1
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            @py_assert1 = w.object_cache[ref.key()]
            @py_assert4 = isinstance(@py_assert1, int)
            if not @py_assert4:
                @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py5':@pytest_ar._saferepr(@py_assert4)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert4 = None
            @py_assert0 = await v1
            @py_assert3 = 1
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            submit_ref_work(w, 0, taskloaf.worker.shutdown)

        submit_ref_work(w, 1, g)
        await wait_to_die()

    cluster(2, f)


def test_remote_double_get():

    async def f(w):
        ref = put(w, 1)

        async def g(w):
            @py_assert0 = await ref.get()
            @py_assert3 = 1
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            v1 = ref._remote_get()
            @py_assert0 = await v1
            @py_assert3 = 1
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None

            def h(w):
                if not hasattr(w, 'x'):
                    w.x = 0
                else:
                    taskloaf.worker.shutdown(w)

            submit_ref_work(w, 0, h)

        submit_ref_work(w, 1, g)
        submit_ref_work(w, 1, g)
        await wait_to_die()

    cluster(2, f)


def test_put_delete_ref(w):

    def f():
        ref = put(w, 1).convert()
        ref2 = put(w, ref).convert()
        del ref
        del ref2
        import gc
        gc.collect()

    f()
    @py_assert2 = w.ref_manager
    @py_assert4 = @py_assert2.entries
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 0
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.ref_manager\n}.entries\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_multiuse_msgs():
    """
    Here, ref is deserialized multiple times on different workers.
    But, ref is only serialized (and the child count incremented)
    once on the main worker.
    So, the ref count will be 2 while there will be 3 live references.
    """

    async def f(w):

        async def fnc():
            v = await fnc.ref.get()
            @py_assert2 = 1
            @py_assert1 = v == @py_assert2
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (v, @py_assert2)) % {'py0':@pytest_ar._saferepr(v) if 'v' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(v) else 'v',  'py3':@pytest_ar._saferepr(@py_assert2)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None
            del fnc.ref

        fnc.ref = put(w, 1)
        w.finished = False

        async def g(w):
            fnc = await g.ref_fnc.get()
            await fnc()
            del fnc
            del g.ref_fnc

            def h(w):
                w.finished = True

            w.submit_work(0, h)
            w.object_cache.clear()
            import gc
            gc.collect()

        g.ref_fnc = put(w, fnc)
        submit_ref_work(w, 1, g)
        submit_ref_work(w, 2, g)
        w.submit_work(1, taskloaf.worker.shutdown)
        w.submit_work(2, taskloaf.worker.shutdown)
        del fnc.ref
        del g.ref_fnc
        while not w.finished:
            await asyncio.sleep(0)

        for i in range(200):
            if not w.allocator.empty():
                await asyncio.sleep(0.01)
                continue

        @py_assert1 = w.allocator
        @py_assert3 = @py_assert1.empty
        @py_assert5 = @py_assert3()
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.allocator\n}.empty\n}()\n}') % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    cluster(3, f)