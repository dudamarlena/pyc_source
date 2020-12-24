# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/beazley/Desktop/Projects/thredo/tests/test_queue.py
# Compiled at: 2018-07-23 11:43:45
# Size of source mod 2**32: 2119 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, thredo

def test_queue_simple():
    results = []

    def consumer(q):
        while True:
            item = q.get()
            if item is None:
                break
            results.append(item)
            q.task_done()

        q.task_done()

    def producer(q):
        results.append('start')
        for n in range(3):
            q.put(n)

        q.put(None)
        q.join()
        results.append('done')

    def main():
        q = thredo.Queue()
        t1 = thredo.spawn(consumer, q)
        t2 = thredo.spawn(producer, q)
        t1.join()
        t2.join()

    thredo.run(main)
    @py_assert2 = ['start', 0, 1, 2, 'done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_queue_get_cancel():
    results = []

    def consumer(q):
        while True:
            try:
                item = q.get()
            except thredo.ThreadCancelled:
                results.append('cancel')
                raise

    def main():
        q = thredo.Queue()
        t = thredo.spawn(consumer, q)
        results.append('start')
        t.cancel()

    thredo.run(main)
    @py_assert2 = ['start', 'cancel']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_queue_put_cancel():
    results = []

    def producer(q):
        while True:
            try:
                q.put(True)
            except thredo.ThreadCancelled:
                results.append('cancel')
                raise

    def main():
        q = thredo.Queue(maxsize=1)
        t = thredo.spawn(producer, q)
        results.append('start')
        thredo.sleep(0.1)
        t.cancel()

    thredo.run(main)
    @py_assert2 = ['start', 'cancel']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_queue_join_cancel():
    results = []

    def producer(q):
        q.put(True)
        try:
            q.join()
        except thredo.ThreadCancelled:
            results.append('cancel')
            raise

    def main():
        q = thredo.Queue(maxsize=1)
        t = thredo.spawn(producer, q)
        results.append('start')
        thredo.sleep(0.1)
        t.cancel()

    thredo.run(main)
    @py_assert2 = ['start', 'cancel']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None