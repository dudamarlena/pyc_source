# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/beazley/Desktop/Projects/thredo/tests/test_core.py
# Compiled at: 2018-07-23 11:42:36
# Size of source mod 2**32: 2372 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, thredo, time

def basic_thread(x, y):
    return x + y


def test_good():
    result = thredo.run(basic_thread, 2, 2)
    @py_assert2 = 4
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_bad():
    try:
        result = thredo.run(basic_thread, 2, '2')
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None
    except BaseException as e:
        @py_assert2 = type(e)
        @py_assert4 = @py_assert2 == TypeError
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None


def test_good_spawn():
    result = []

    def main():
        t = thredo.spawn(basic_thread, 2, 2)
        result.append(t.join())

    thredo.run(main)
    @py_assert2 = [4]
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_bad_spawn():
    result = []

    def main():
        t = thredo.spawn(basic_thread, 2, '2')
        try:
            t.join()
        except thredo.ThreadError as e:
            result.append('error')
            result.append(type(e.__cause__))

    thredo.run(main)
    @py_assert2 = ['error', TypeError]
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_sleep():
    result = []

    def main():
        start = time.time()
        thredo.sleep(1.0)
        end = time.time()
        result.append(end - start)

    thredo.run(main)
    @py_assert0 = result[0]
    @py_assert3 = 1.0
    @py_assert2 = @py_assert0 > @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_sleep_cancel():
    result = []

    def child():
        try:
            thredo.sleep(10)
        except thredo.ThreadCancelled:
            result.append('cancel')

    def main():
        t = thredo.spawn(child)
        thredo.sleep(0.1)
        t.cancel()

    thredo.run(main)
    @py_assert2 = ['cancel']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_timeout():
    result = []

    def main():
        try:
            thredo.timeout_after(0.25, thredo.sleep, 1)
        except thredo.ThreadTimeout:
            result.append('timeout')

    thredo.run(main)
    @py_assert2 = ['timeout']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_timeout_context():
    result = []

    def main():
        try:
            with thredo.timeout_after(0.25):
                thredo.sleep(1)
        except thredo.ThreadTimeout:
            result.append('timeout')

    thredo.run(main)
    @py_assert2 = ['timeout']
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_ignore():

    def main():
        thredo.ignore_after(0.25, thredo.sleep, 1)

    start = time.time()
    thredo.run(main)
    end = time.time()
    @py_assert2 = end - start
    @py_assert4 = 1
    @py_assert3 = @py_assert2 < @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('<', ), (@py_assert3,), ('(%(py0)s - %(py1)s) < %(py5)s', ), (@py_assert2, @py_assert4)) % {'py0':@pytest_ar._saferepr(end) if 'end' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(end) else 'end',  'py1':@pytest_ar._saferepr(start) if 'start' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(start) else 'start',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert3 = @py_assert4 = None


def test_ignore_context():

    def main():
        with thredo.ignore_after(0.25):
            thredo.sleep(1)

    start = time.time()
    thredo.run(main)
    end = time.time()
    @py_assert2 = end - start
    @py_assert4 = 1
    @py_assert3 = @py_assert2 < @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('<', ), (@py_assert3,), ('(%(py0)s - %(py1)s) < %(py5)s', ), (@py_assert2, @py_assert4)) % {'py0':@pytest_ar._saferepr(end) if 'end' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(end) else 'end',  'py1':@pytest_ar._saferepr(start) if 'start' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(start) else 'start',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert3 = @py_assert4 = None