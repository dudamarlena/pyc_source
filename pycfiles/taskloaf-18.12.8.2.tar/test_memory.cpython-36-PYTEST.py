# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_memory.py
# Compiled at: 2018-02-26 01:13:14
# Size of source mod 2**32: 4676 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, gc, asyncio
from taskloaf.serialize import dumps, loads
import taskloaf.message_capnp
from taskloaf.memory import *
from taskloaf.run import null_comm_worker
from taskloaf.cluster import cluster
from taskloaf.test_decorators import mpi_procs
from taskloaf.mpi import mpiexisting
from taskloaf.get import remote_get
one_serialized = dumps(1)

def dref_serialization_tester(sfnc, dfnc):
    with null_comm_worker() as (w):
        mm = w.memory
        @py_assert1 = mm.n_entries
        @py_assert3 = @py_assert1()
        @py_assert6 = 0
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.n_entries\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(mm) if 'mm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mm) else 'mm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        dref = put(w, value=1)
        @py_assert1 = mm.n_entries
        @py_assert3 = @py_assert1()
        @py_assert6 = 0
        @py_assert5 = @py_assert3 > @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('>', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.n_entries\n}()\n} > %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(mm) if 'mm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mm) else 'mm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        dref_bytes = sfnc(dref)
        del dref
        @py_assert1 = mm.n_entries
        @py_assert3 = @py_assert1()
        @py_assert6 = 0
        @py_assert5 = @py_assert3 > @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('>', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.n_entries\n}()\n} > %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(mm) if 'mm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mm) else 'mm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        dref2 = dfnc(w, dref_bytes)
        del dref2
        gc.collect()
        @py_assert1 = w.memory
        @py_assert3 = @py_assert1.n_entries
        @py_assert5 = @py_assert3()
        @py_assert8 = 0
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.memory\n}.n_entries\n}()\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_dref_pickle_delete():
    dref_serialization_tester(dumps, loads)


def test_dref_encode_capnp():

    def serialize(dref):
        m = taskloaf.message_capnp.DistributedRef.new_message()
        dref.encode_capnp(m)
        return m.to_bytes()

    def deserialize(w, dref_b):
        m = taskloaf.message_capnp.DistributedRef.from_bytes(dref_b)
        return DistributedRef.decode_capnp(w, m)

    dref_serialization_tester(serialize, deserialize)


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


def test_alloc_creation():
    from contextlib import ExitStack
    import taskloaf.allocator
    for i in range(10):
        with ExitStack() as (es):
            a = taskloaf.allocator.Allocator(0, es)


def test_put_get_delete():
    with null_comm_worker() as (w):
        mm = w.memory
        dref = DistributedRef(w, w.addr + 1)
        mm.put(value=1, dref=dref)
        @py_assert1 = mm.available
        @py_assert4 = @py_assert1(dref)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.available\n}(%(py3)s)\n}') % {'py0':@pytest_ar._saferepr(mm) if 'mm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mm) else 'mm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dref) if 'dref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dref) else 'dref',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        @py_assert1 = mm.get_local
        @py_assert4 = @py_assert1(dref)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_local\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(mm) if 'mm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mm) else 'mm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dref) if 'dref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dref) else 'dref',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
        mm.delete(dref)
        @py_assert1 = mm.available
        @py_assert4 = @py_assert1(dref)
        @py_assert6 = not @py_assert4
        if not @py_assert6:
            @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.available\n}(%(py3)s)\n}') % {'py0':@pytest_ar._saferepr(mm) if 'mm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mm) else 'mm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dref) if 'dref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dref) else 'dref',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert4 = @py_assert6 = None


def test_decref_local():
    with null_comm_worker() as (w):
        mm = w.memory
        dref = put(w, value=1)
        @py_assert2 = mm.entries
        @py_assert4 = @py_assert2.keys
        @py_assert6 = @py_assert4()
        @py_assert8 = len(@py_assert6)
        @py_assert11 = 1
        @py_assert10 = @py_assert8 == @py_assert11
        if not @py_assert10:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.entries\n}.keys\n}()\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(mm) if 'mm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mm) else 'mm',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
        del dref
        gc.collect()
        @py_assert2 = mm.entries
        @py_assert4 = @py_assert2.keys
        @py_assert6 = @py_assert4()
        @py_assert8 = len(@py_assert6)
        @py_assert11 = 0
        @py_assert10 = @py_assert8 == @py_assert11
        if not @py_assert10:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.entries\n}.keys\n}()\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(mm) if 'mm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mm) else 'mm',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_decref_encode():
    with null_comm_worker() as (w):
        b = DecRefSerializer.serialize([1, 2, 3, 4]).to_bytes()
        m = taskloaf.message_capnp.Message.from_bytes(b)
        creator, _id, gen, n_children = DecRefSerializer.deserialize(w, m)
        @py_assert2 = 1
        @py_assert1 = creator == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (creator, @py_assert2)) % {'py0':@pytest_ar._saferepr(creator) if 'creator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(creator) else 'creator',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
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


def test_eager_put_gives_shmem_ptr():
    with null_comm_worker() as (w):
        memory = memoryview(bytes(10))
        dref = put(w, value=memory, eager_alloc=True)
        @py_assert1 = dref.shmem_ptr
        @py_assert3 = @py_assert1.needs_deserialize
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.shmem_ptr\n}.needs_deserialize\n}') % {'py0':@pytest_ar._saferepr(dref) if 'dref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dref) else 'dref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = dref.shmem_ptr
        @py_assert3 = @py_assert1.is_null
        @py_assert5 = @py_assert3()
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.shmem_ptr\n}.is_null\n}()\n}') % {'py0':@pytest_ar._saferepr(dref) if 'dref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dref) else 'dref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        dref = put(w, serialized=memory)
        @py_assert1 = dref.shmem_ptr
        @py_assert3 = @py_assert1.needs_deserialize
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.shmem_ptr\n}.needs_deserialize\n}') % {'py0':@pytest_ar._saferepr(dref) if 'dref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dref) else 'dref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = dref.shmem_ptr
        @py_assert3 = @py_assert1.is_null
        @py_assert5 = @py_assert3()
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.shmem_ptr\n}.is_null\n}()\n}') % {'py0':@pytest_ar._saferepr(dref) if 'dref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dref) else 'dref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_alloc_no_put():
    with null_comm_worker() as (w):
        dref = alloc(w, 16)
        mem = get(w, dref)
        mem[1] = 2
        @py_assert2 = len(mem)
        @py_assert5 = 16
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(mem) if 'mem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mem) else 'mem',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = w.remote_shmem.get(dref)[1]
        @py_assert3 = 2
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None


def test_get_deserializes():
    with null_comm_worker() as (w):
        dref = put(w, serialized=(taskloaf.serialize.dumps(15)))
        @py_assert3 = get(w, dref)
        @py_assert6 = 15
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(get) if 'get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get) else 'get',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(dref) if 'dref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dref) else 'dref',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert3 = @py_assert5 = @py_assert6 = None


@mpi_procs(2)
def test_get():

    async def f(w):
        dref = put(w, value=1)
        dref2 = put(w, value=one_serialized)
        dref3 = put(w, serialized=one_serialized)
        @py_assert0 = await remote_get(w, dref)
        @py_assert3 = 1
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = await remote_get(w, dref2)
        @py_assert2 = @py_assert0 == one_serialized
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, one_serialized)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(one_serialized) if 'one_serialized' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one_serialized) else 'one_serialized'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = await remote_get(w, dref3)
        @py_assert3 = 1
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

        async def g(w):
            @py_assert0 = await remote_get(w, dref)
            @py_assert3 = 1
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            @py_assert0 = await remote_get(w, dref2)
            @py_assert2 = @py_assert0 == one_serialized
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, one_serialized)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(one_serialized) if 'one_serialized' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one_serialized) else 'one_serialized'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            @py_assert0 = await remote_get(w, dref3)
            @py_assert3 = 1
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None

            def h(w):
                taskloaf.worker.shutdown(w)

            w.submit_work(0, h)

        w.submit_work(1, g)
        while True:
            await asyncio.sleep(0)

    cluster(2, f)


@mpi_procs(2)
def test_remote_double_get():

    async def f(w):
        dref = put(w, value=1)

        async def g(w):
            @py_assert0 = await remote_get(w, dref)
            @py_assert3 = 1
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None

        t1 = taskloaf.task(w, g, to=1)
        t2 = taskloaf.task(w, g, to=1)
        await t1
        await t2

    cluster(2, f)