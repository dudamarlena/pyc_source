# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blake/code/vivint-selenium-docker/tests/test_pool.py
# Compiled at: 2017-11-07 17:20:30
# Size of source mod 2**32: 3081 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from selenium_docker.pool import DriverPool, DriverPoolValueError, DriverPoolRuntimeException

class BogusDriver:
    __doc__ = ' No-op object class. '


def test_pool_instantiation(factory):
    pool = DriverPool(5, factory=factory)
    @py_assert1 = pool.size
    @py_assert4 = 5
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.size\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = pool.name
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 6
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.name\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = pool._drivers
    @py_assert3 = @py_assert1.qsize
    @py_assert5 = @py_assert3()
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s._drivers\n}.qsize\n}()\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = pool._drivers
    @py_assert3 = @py_assert1.maxsize
    @py_assert7 = pool.size
    @py_assert5 = @py_assert3 == @py_assert7
    if not @py_assert5:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s._drivers\n}.maxsize\n} == %(py8)s\n{%(py8)s = %(py6)s.size\n}', ), (@py_assert3, @py_assert7)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = pool.is_processing
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.is_processing\n}') % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = pool.proxy
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.proxy\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    pool.quit()


def test_no_proxy(factory):
    pool = DriverPool(5, use_proxy=False, factory=factory)
    @py_assert1 = pool.proxy
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.proxy\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    pool.close()


def test_bogus_drver_cls(factory):
    with pytest.raises(DriverPoolValueError):
        DriverPool(1, factory=factory, driver_cls=BogusDriver)


@pytest.mark.parametrize('proxy', [True, False])
def test_cleanup_browser(proxy, factory):

    def work(driver, item):
        @py_assert2 = True
        @py_assert1 = item is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (item, @py_assert2)) % {'py0':@pytest_ar._saferepr(item) if 'item' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(item) else 'item',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        return item

    pool = DriverPool(3, use_proxy=proxy, factory=factory)
    @py_assert1 = pool._use_proxy
    @py_assert3 = @py_assert1 is proxy
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._use_proxy\n} is %(py4)s', ), (@py_assert1, proxy)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    results = [x for x in pool.execute(work, [
     True, True],
      preserve_order=proxy,
      auto_clean=False)]
    if proxy:
        @py_assert1 = pool.proxy
        @py_assert3 = @py_assert1.factory
        @py_assert7 = pool.factory
        @py_assert5 = @py_assert3 is @py_assert7
        if not @py_assert5:
            @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.proxy\n}.factory\n} is %(py8)s\n{%(py8)s = %(py6)s.factory\n}', ), (@py_assert3, @py_assert7)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = pool.is_processing
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.is_processing\n}') % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    pool.close()
    @py_assert1 = pool.proxy
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.proxy\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = pool.is_processing
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.is_processing\n}') % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = all(results)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py1':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert2 = len(results)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = pool._drivers
    @py_assert3 = @py_assert1.qsize
    @py_assert5 = @py_assert3()
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s._drivers\n}.qsize\n}()\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    pool.quit()
    @py_assert2 = pool.factory
    @py_assert4 = @py_assert2.containers
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 0
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.factory\n}.containers\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = pool.proxy
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.proxy\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_async_failures(factory):
    pool = DriverPool(2, factory=factory, use_proxy=False)
    with pytest.raises(DriverPoolValueError):
        pool.execute_async(True)
    with pytest.raises(DriverPoolValueError):
        pool.execute_async(int, callback=True)
    with pytest.raises(DriverPoolRuntimeException):
        pool.execute_async((lambda s: s is True), items=[True, True])
        pool.execute_async((lambda s: s is True), items=[True, True])
    pool.stop_async()
    @py_assert1 = pool.is_processing
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.is_processing\n}') % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    with pytest.raises(DriverPoolValueError):
        pool.execute_async(lambda s: s is True)
        pool.add_async()
    with pytest.raises(DriverPoolRuntimeException):
        pool.execute_async(lambda s: s is True)
        pool.execute(int, [])
    pool.quit()


@pytest.mark.current
def test_async_execution(factory):
    pool = DriverPool(1, factory=factory, use_proxy=False)
    pool.execute_async(lambda a, b: isinstance(b, int))
    pool.add_async(1, 2, 3, 4)
    pool.add_async([1, 2, 3, 4])
    @py_assert3 = pool.results
    @py_assert5 = False
    @py_assert7 = @py_assert3(block=@py_assert5)
    @py_assert9 = list(@py_assert7)
    @py_assert11 = all(@py_assert9)
    if not @py_assert11:
        @py_format13 = ('' + 'assert %(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py1)s(%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.results\n}(block=%(py6)s)\n})\n})\n}') % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    pool.add_async(1, 2, 3, 4)
    pool.add_async([1, 2, 3, 4])
    @py_assert3 = pool.results
    @py_assert5 = True
    @py_assert7 = @py_assert3(block=@py_assert5)
    @py_assert9 = list(@py_assert7)
    @py_assert11 = all(@py_assert9)
    if not @py_assert11:
        @py_format13 = ('' + 'assert %(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py1)s(%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.results\n}(block=%(py6)s)\n})\n})\n}') % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert3 = pool.results
    @py_assert5 = False
    @py_assert7 = @py_assert3(block=@py_assert5)
    @py_assert9 = list(@py_assert7)
    @py_assert11 = len(@py_assert9)
    @py_assert14 = 0
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py1)s(%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.results\n}(block=%(py6)s)\n})\n})\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    pool.quit()
    pool.execute_async(lambda a, b: isinstance(b, bool))
    pool.add_async(True, False)
    @py_assert1 = pool.stop_async
    @py_assert3 = @py_assert1()
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stop_async\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(pool) if 'pool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pool) else 'pool',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    pool.quit()