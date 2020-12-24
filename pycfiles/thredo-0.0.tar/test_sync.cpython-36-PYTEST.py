# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/beazley/Desktop/Projects/thredo/tests/test_sync.py
# Compiled at: 2018-07-23 11:44:03
# Size of source mod 2**32: 8140 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, thredo

def test_event_wait():
    evt = thredo.Event()
    result = []

    def waiter():
        evt.wait()
        result.append('waiter')

    def main():
        t = thredo.spawn(waiter)
        result.append('start')
        evt.set()
        t.join()

    thredo.run(main)
    @py_assert2 = ['start', 'waiter']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    evt.clear()
    @py_assert1 = evt.is_set
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_set\n}()\n}' % {'py0':@pytest_ar._saferepr(evt) if 'evt' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(evt) else 'evt',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_event_wait_cancel():
    evt = thredo.Event()
    result = []

    def waiter():
        try:
            evt.wait()
            result.append('waiter')
        except thredo.ThreadCancelled:
            result.append('cancel')

    def main():
        t = thredo.spawn(waiter)
        result.append('start')
        t.cancel()

    thredo.run(main)
    @py_assert2 = ['start', 'cancel']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_lock():
    lock = thredo.Lock()
    result = []

    def child():
        with lock:
            result.append('child')

    def main():
        lock.acquire()
        if lock.locked():
            result.append('locked')
        try:
            t = thredo.spawn(child)
            result.append('parent')
        finally:
            lock.release()

        t.join()

    thredo.run(main)
    @py_assert2 = ['locked', 'parent', 'child']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_lock_cancel():
    lock = thredo.Lock()
    result = []

    def child():
        try:
            with lock:
                result.append('child')
        except thredo.ThreadCancelled:
            result.append('cancel')

    def main():
        lock.acquire()
        try:
            t = thredo.spawn(child)
            result.append('parent')
            t.cancel()
        finally:
            lock.release()

    thredo.run(main)
    @py_assert2 = ['parent', 'cancel']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_lock_race():
    lock = thredo.Lock()
    evt = thredo.Event()
    n = 0

    def incr(count):
        nonlocal n
        evt.wait()
        while count > 0:
            with lock:
                n += 1
            count -= 1

    def decr(count):
        nonlocal n
        evt.wait()
        while count > 0:
            with lock:
                n -= 1
            count -= 1

    def main():
        t1 = thredo.spawn(incr, 10000)
        t2 = thredo.spawn(decr, 10000)
        evt.set()
        t1.join()
        t2.join()

    thredo.run(main)
    @py_assert2 = 0
    @py_assert1 = n == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (n, @py_assert2)) % {'py0':@pytest_ar._saferepr(n) if 'n' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n) else 'n',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_semaphore():
    lock = thredo.Semaphore()
    result = []

    def child():
        with lock:
            result.append('child')

    def main():
        lock.acquire()
        result.append(lock.value)
        try:
            t = thredo.spawn(child)
            result.append('parent')
        finally:
            lock.release()

        t.join()

    thredo.run(main)
    @py_assert2 = [0, 'parent', 'child']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_semaphore_cancel():
    lock = thredo.Semaphore()
    result = []

    def child():
        try:
            with lock:
                result.append('child')
        except thredo.ThreadCancelled:
            result.append('cancel')

    def main():
        lock.acquire()
        try:
            t = thredo.spawn(child)
            result.append('parent')
            t.cancel()
        finally:
            lock.release()

    thredo.run(main)
    @py_assert2 = ['parent', 'cancel']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_semaphore_race():
    lock = thredo.Semaphore()
    evt = thredo.Event()
    n = 0

    def incr(count):
        nonlocal n
        evt.wait()
        while count > 0:
            with lock:
                n += 1
            count -= 1

    def decr(count):
        nonlocal n
        evt.wait()
        while count > 0:
            with lock:
                n -= 1
            count -= 1

    def main():
        t1 = thredo.spawn(incr, 10000)
        t2 = thredo.spawn(decr, 10000)
        evt.set()
        t1.join()
        t2.join()

    thredo.run(main)
    @py_assert2 = 0
    @py_assert1 = n == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (n, @py_assert2)) % {'py0':@pytest_ar._saferepr(n) if 'n' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n) else 'n',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_rlock():
    lock = thredo.RLock()
    result = []

    def child():
        with lock:
            result.append('child')

    def main():
        lock.acquire()
        if lock.locked():
            result.append('locked')
        try:
            t = thredo.spawn(child)
            result.append('parent')
        finally:
            lock.release()

        t.join()

    thredo.run(main)
    @py_assert2 = ['locked', 'parent', 'child']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_rlock_cancel():
    lock = thredo.RLock()
    result = []

    def child():
        try:
            with lock:
                result.append('child')
        except thredo.ThreadCancelled:
            result.append('cancel')

    def main():
        lock.acquire()
        try:
            t = thredo.spawn(child)
            result.append('parent')
            t.cancel()
        finally:
            lock.release()

    thredo.run(main)
    @py_assert2 = ['parent', 'cancel']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_rlock_race():
    lock = thredo.RLock()
    evt = thredo.Event()
    n = 0

    def incr(count):
        nonlocal n
        evt.wait()
        while count > 0:
            with lock:
                n += 1
            count -= 1

    def decr(count):
        nonlocal n
        evt.wait()
        while count > 0:
            with lock:
                n -= 1
            count -= 1

    def main():
        t1 = thredo.spawn(incr, 10000)
        t2 = thredo.spawn(decr, 10000)
        evt.set()
        t1.join()
        t2.join()

    thredo.run(main)
    @py_assert2 = 0
    @py_assert1 = n == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (n, @py_assert2)) % {'py0':@pytest_ar._saferepr(n) if 'n' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n) else 'n',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_condition():
    lock = thredo.Condition()
    result = []

    def child():
        with lock:
            result.append('child')

    def main():
        lock.acquire()
        if lock.locked():
            result.append('locked')
        try:
            t = thredo.spawn(child)
            result.append('parent')
        finally:
            lock.release()

        t.join()

    thredo.run(main)
    @py_assert2 = ['locked', 'parent', 'child']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_condition_cancel():
    lock = thredo.Condition()
    result = []

    def child():
        try:
            with lock:
                result.append('child')
        except thredo.ThreadCancelled:
            result.append('cancel')

    def main():
        lock.acquire()
        try:
            t = thredo.spawn(child)
            result.append('parent')
            t.cancel()
        finally:
            lock.release()

    thredo.run(main)
    @py_assert2 = ['parent', 'cancel']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_condition_race():
    lock = thredo.Condition()
    evt = thredo.Event()
    n = 0

    def incr(count):
        nonlocal n
        evt.wait()
        while count > 0:
            with lock:
                n += 1
            count -= 1

    def decr(count):
        nonlocal n
        evt.wait()
        while count > 0:
            with lock:
                n -= 1
            count -= 1

    def main():
        t1 = thredo.spawn(incr, 10000)
        t2 = thredo.spawn(decr, 10000)
        evt.set()
        t1.join()
        t2.join()

    thredo.run(main)
    @py_assert2 = 0
    @py_assert1 = n == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (n, @py_assert2)) % {'py0':@pytest_ar._saferepr(n) if 'n' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n) else 'n',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_condition_wait_notify():
    n = 0
    lock = thredo.Condition(thredo.Lock())
    result = []

    def waiter():
        current = n
        while 1:
            with lock:
                while current == n:
                    lock.wait()

                result.append(('consume', n))
                current = n
            if n >= 5:
                break

    def producer():
        nonlocal n
        while n < 5:
            thredo.sleep(0.1)
            with lock:
                n += 1
                result.append(('produce', n))
                lock.notify()

    def main():
        t1 = thredo.spawn(waiter)
        t2 = thredo.spawn(producer)
        t1.join()
        t2.join()

    thredo.run(main)
    @py_assert2 = [('produce', 1), ('consume', 1), ('produce', 2), ('consume', 2), ('produce', 3), ('consume', 3), ('produce', 4), ('consume', 4), ('produce', 5), ('consume', 5)]
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None