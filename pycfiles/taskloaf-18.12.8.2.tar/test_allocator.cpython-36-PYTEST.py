# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_allocator.py
# Compiled at: 2018-02-26 18:00:38
# Size of source mod 2**32: 5372 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, struct, pytest
from contextlib import closing
import numpy as np
from taskloaf.allocator import *
block_manager = BlockManager('/dev/shm/pool', taskloaf.shmem.page4kb)

def check_ptr(ptr):
    x = np.frombuffer(ptr.deref())
    n = x.shape[0]
    x[:] = np.arange(n)
    for i in range(n):
        @py_assert0 = x[i]
        @py_assert2 = @py_assert0 == i
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, i)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = struct.unpack('d', ptr.deref()[i * 8:(i + 1) * 8])[0]
        @py_assert2 = @py_assert0 == i
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, i)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


def test_pool_block():
    with closing(PoolBlock(block_manager, 2048, 4096)) as (pb):
        @py_assert1 = pb.empty
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.empty\n}()\n}') % {'py0':@pytest_ar._saferepr(pb) if 'pb' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pb) else 'pb',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        ptr1 = pb.malloc()
        check_ptr(ptr1)
        ptr2 = pb.malloc()
        @py_assert2 = 1
        @py_assert4 = -@py_assert2
        @py_assert1 = ptr2 != @py_assert4
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != -%(py3)s', ), (ptr2, @py_assert4)) % {'py0':@pytest_ar._saferepr(ptr2) if 'ptr2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr2) else 'ptr2',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        null = pb.malloc()
        @py_assert2 = 1
        @py_assert4 = -@py_assert2
        @py_assert1 = null == @py_assert4
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == -%(py3)s', ), (null, @py_assert4)) % {'py0':@pytest_ar._saferepr(null) if 'null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(null) else 'null',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert1 = pb.empty
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.empty\n}()\n}') % {'py0':@pytest_ar._saferepr(pb) if 'pb' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pb) else 'pb',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        pb.free(ptr1)
        @py_assert1 = pb.empty
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.empty\n}()\n}') % {'py0':@pytest_ar._saferepr(pb) if 'pb' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pb) else 'pb',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        ptr3 = pb.malloc()
        @py_assert1 = ptr3.start
        @py_assert5 = ptr1.start
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.start\n} == %(py6)s\n{%(py6)s = %(py4)s.start\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(ptr3) if 'ptr3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr3) else 'ptr3',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(ptr1) if 'ptr1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr1) else 'ptr1',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        pb.free(ptr2)
        pb.free(ptr3)
        @py_assert1 = pb.empty
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.empty\n}()\n}') % {'py0':@pytest_ar._saferepr(pb) if 'pb' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pb) else 'pb',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None


def test_reload_block():
    block = block_manager.new_block(80)
    np.frombuffer(block.shmem.mem)[:] = np.arange(10)
    with closing(load_memory_block(block.filepath, block.idx)) as (block2):
        np.testing.assert_almost_equal(np.frombuffer(block2.shmem.mem), np.arange(10))
    block_manager.free_block(block)


def test_pool():
    with closing(Pool(block_manager, 2048)) as (p):
        ptr1 = p.malloc()
        ptr2 = p.malloc()
        ptr3 = p.malloc()
        @py_assert2 = 1
        @py_assert4 = -@py_assert2
        @py_assert1 = ptr3 != @py_assert4
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != -%(py3)s', ), (ptr3, @py_assert4)) % {'py0':@pytest_ar._saferepr(ptr3) if 'ptr3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr3) else 'ptr3',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert2 = @py_assert4 = None
        @py_assert1 = ptr1.block
        @py_assert5 = ptr2.block
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.block\n} == %(py6)s\n{%(py6)s = %(py4)s.block\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(ptr1) if 'ptr1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr1) else 'ptr1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(ptr2) if 'ptr2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr2) else 'ptr2',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = ptr1.block
        @py_assert5 = ptr3.block
        @py_assert3 = @py_assert1 != @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.block\n} != %(py6)s\n{%(py6)s = %(py4)s.block\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(ptr1) if 'ptr1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr1) else 'ptr1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(ptr3) if 'ptr3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr3) else 'ptr3',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None


def test_pool_dealloc_block():
    with closing(Pool(block_manager, 2048)) as (p):
        ptrs = [p.malloc() for i in range(6)]
        @py_assert2 = p.blocks
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 3
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.blocks\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert2 = p.free_list
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 0
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.free_list\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        for ptr in ptrs[2:]:
            p.free(ptr)

        @py_assert2 = p.free_list
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.free_list\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert2 = p.blocks
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 2
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.blocks\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def alloc_ptrs_then(f):
    with closing(Pool(block_manager, 2048)) as (p):
        ptrs = [p.malloc() for i in range(6)]
        f(p)


def check_no_blocks_leftover():
    @py_assert2 = block_manager.blocks
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.blocks\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(block_manager) if 'block_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(block_manager) else 'block_manager',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    for i in range(block_manager.idx):
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.exists
        @py_assert6 = block_manager.get_path
        @py_assert9 = @py_assert6(i)
        @py_assert11 = @py_assert3(@py_assert9)
        @py_assert13 = not @py_assert11
        if not @py_assert13:
            @py_format14 = ('' + 'assert not %(py12)s\n{%(py12)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py10)s\n{%(py10)s = %(py7)s\n{%(py7)s = %(py5)s.get_path\n}(%(py8)s)\n})\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(block_manager) if 'block_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(block_manager) else 'block_manager',  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_pool_deletes_blocks():
    idxs = alloc_ptrs_then(lambda p: None)
    check_no_blocks_leftover()


def test_pool_deletes_blocks_on_exception():
    with pytest.raises(Exception):
        idxs = alloc_ptrs_then(lambda p: [][0])
    check_no_blocks_leftover()


def test_alloc_mmap():
    with closing(ShmemAllocator(block_manager)) as (a):
        ptr = a.malloc(int(100000.0))
        check_ptr(ptr)
        @py_assert1 = block_manager.check_location_exists
        @py_assert4 = @py_assert1(ptr)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.check_location_exists\n}(%(py3)s)\n}') % {'py0':@pytest_ar._saferepr(block_manager) if 'block_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(block_manager) else 'block_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ptr) if 'ptr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr) else 'ptr',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        a.free(ptr)
        @py_assert1 = block_manager.check_location_exists
        @py_assert4 = @py_assert1(ptr)
        @py_assert6 = not @py_assert4
        if not @py_assert6:
            @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.check_location_exists\n}(%(py3)s)\n}') % {'py0':@pytest_ar._saferepr(block_manager) if 'block_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(block_manager) else 'block_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ptr) if 'ptr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptr) else 'ptr',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert4 = @py_assert6 = None


def test_allocator_get_pool():
    with closing(ShmemAllocator(block_manager)) as (a):
        for i in range(8, 100):
            @py_assert1 = a.get_pool
            @py_assert4 = @py_assert1(i)
            @py_assert6 = @py_assert4.chunk_size
            @py_assert8 = @py_assert6 >= i
            if not @py_assert8:
                @py_format10 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_pool\n}(%(py3)s)\n}.chunk_size\n} >= %(py9)s', ), (@py_assert6, i)) % {'py0':@pytest_ar._saferepr(a) if 'a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a) else 'a',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i'}
                @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
                raise AssertionError(@pytest_ar._format_explanation(@py_format12))
            @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
            @py_assert1 = a.get_pool
            @py_assert4 = @py_assert1(i)
            @py_assert6 = @py_assert4.chunk_size
            @py_assert8 = 2
            @py_assert10 = @py_assert6 / @py_assert8
            @py_assert11 = @py_assert10 < i
            if not @py_assert11:
                @py_format13 = @pytest_ar._call_reprcompare(('<', ), (@py_assert11,), ('(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_pool\n}(%(py3)s)\n}.chunk_size\n} / %(py9)s) < %(py12)s', ), (@py_assert10, i)) % {'py0':@pytest_ar._saferepr(a) if 'a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a) else 'a',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i'}
                @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
                raise AssertionError(@pytest_ar._format_explanation(@py_format15))
            @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_alloc_pool():
    with closing(ShmemAllocator(block_manager)) as (a):
        ptrs = []
        for i in range(8, 100):
            ptrs.append(a.malloc(i))
            @py_assert0 = ptrs[(-1)]
            @py_assert2 = @py_assert0.end
            @py_assert4 = ptrs[(-1)]
            @py_assert6 = @py_assert4.start
            @py_assert8 = @py_assert2 - @py_assert6
            @py_assert9 = @py_assert8 == i
            if not @py_assert9:
                @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('(%(py3)s\n{%(py3)s = %(py1)s.end\n} - %(py7)s\n{%(py7)s = %(py5)s.start\n}) == %(py10)s', ), (@py_assert8, i)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i'}
                @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None

        for ptr in ptrs:
            a.free(ptr)

        @py_assert1 = a.empty
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.empty\n}()\n}') % {'py0':@pytest_ar._saferepr(a) if 'a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a) else 'a',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None


def test_block_frees_memory():
    start_mem = get_memory_used()
    nbytes = block_manager.page_size * 1000
    with closing(block_manager.new_block(nbytes)) as (b):
        A = np.frombuffer(b.shmem.mem)
        A[:] = np.random.rand(A.shape[0])
        @py_assert1 = get_memory_used()
        @py_assert4 = @py_assert1 - start_mem
        @py_assert5 = @py_assert4 >= nbytes
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert5,), ('(%(py2)s\n{%(py2)s = %(py0)s()\n} - %(py3)s) >= %(py6)s', ), (@py_assert4, nbytes)) % {'py0':@pytest_ar._saferepr(get_memory_used) if 'get_memory_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_memory_used) else 'get_memory_used',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(start_mem) if 'start_mem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(start_mem) else 'start_mem',  'py6':@pytest_ar._saferepr(nbytes) if 'nbytes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nbytes) else 'nbytes'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert4 = @py_assert5 = None
    @py_assert1 = get_memory_used()
    @py_assert4 = @py_assert1 - start_mem
    @py_assert5 = @py_assert4 < nbytes
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('<', ), (@py_assert5,), ('(%(py2)s\n{%(py2)s = %(py0)s()\n} - %(py3)s) < %(py6)s', ), (@py_assert4, nbytes)) % {'py0':@pytest_ar._saferepr(get_memory_used) if 'get_memory_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_memory_used) else 'get_memory_used',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(start_mem) if 'start_mem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(start_mem) else 'start_mem',  'py6':@pytest_ar._saferepr(nbytes) if 'nbytes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nbytes) else 'nbytes'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert5 = None


def benchmark():
    sizes = [
     16, 32, 40, 48, 372, 1100, 12348, 100000]
    n = 50000
    ptrs = []
    from taskloaf.timer import Timer
    import gc
    t = Timer()
    block_manager = BlockManager('/dev/shm/pool', taskloaf.shmem.page4kb)
    ratio_malloc = 0.99
    with closing(ShmemAllocator(block_manager, block_size_exponent=20)) as (a):
        start_mem = get_memory_used()
        for i in range(n):
            if np.random.rand() > ratio_malloc and len(ptrs) > 0:
                idx = np.random.randint(0, len(ptrs))
                p = ptrs.pop(idx)
                a.free(p)
            else:
                idx = np.random.randint(0, len(sizes))
                s = sizes[idx]
                ptrs.append(a.malloc(s))
                A = np.frombuffer((ptrs[(-1)].deref()), dtype=(np.uint8))
                A[:] = 0.0

        print('before free', get_memory_used() - start_mem)
        before_free_mem = get_memory_used()
        total_freed = 0
        for p in ptrs:
            total_freed += p.end - p.start
            a.free(p)

        total_released = before_free_mem - get_memory_used()
        print('freed comparison', total_freed, total_released, total_released / total_freed)
        print('after free', get_memory_used() - start_mem)
        del ptrs
        gc.collect()
        print('after gc collect', get_memory_used() - start_mem)
        @py_assert1 = a.empty
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.empty\n}()\n}') % {'py0':@pytest_ar._saferepr(a) if 'a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a) else 'a',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
    del block_manager
    del a
    gc.collect()
    print('after close', get_memory_used() - start_mem)
    t.report('random malloc free x' + str(n))


if __name__ == '__main__':
    benchmark()