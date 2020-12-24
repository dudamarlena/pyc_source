# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hit9/uav/flask-idempotent2/tests/test_idempotent.py
# Compiled at: 2017-05-25 08:19:03
# Size of source mod 2**32: 2311 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, time, gevent, grequests
from gevent.wsgi import WSGIServer

def test_simple_cache(app, app_client):
    data = dict(email='hit9@icloud.com', password='1234567890')
    r = app_client.put('/user', data=data)
    @py_assert1 = r.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r', 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    r = app_client.put('/user', data=data)
    @py_assert1 = r.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r', 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    time.sleep(1)
    r = app_client.put('/user', data=data)
    @py_assert1 = r.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 != @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} != %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r', 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_no_db_events_idempotent(app, app_client):
    r = app_client.get('/random')
    @py_assert1 = r.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r', 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    data = r.json['result']
    r = app_client.get('/random')
    @py_assert1 = r.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r', 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = r.json['result']
    @py_assert2 = @py_assert0 == data
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, data)) % {'py3': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    time.sleep(1)
    r = app_client.get('/random')
    @py_assert1 = r.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r', 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = r.json['result']
    @py_assert2 = @py_assert0 != data
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py3)s', ), (@py_assert0, data)) % {'py3': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_simple_lock(app, app_client):

    def _start_real_server():
        http_server = WSGIServer(('', 54321), app)
        http_server.serve_forever()

    server_thread = gevent.spawn(_start_real_server)

    def _stop_real_server():
        gevent.sleep(1)
        gevent.kill(server_thread)

    api_data_with_lock = dict(email='hit10@icloud.com', password='1234567890')
    api_url_with_lock = 'http://localhost:54321/user_or_return'
    requests_for_api_with_lock = [grequests.put(api_url_with_lock, json=api_data_with_lock) for i in range(5)]
    api_data_without_lock = dict(email='hit1@icloud.com', password='1234567890')
    api_url_without_lock = 'http://localhost:54321/user_or_return_nolock'
    requests_for_api_without_lock = [grequests.put(api_url_without_lock, json=api_data_without_lock) for i in range(5)]
    rs1 = grequests.map(requests_for_api_with_lock, size=10)
    rs2 = grequests.map(requests_for_api_without_lock, size=10)
    stop_server_thread = gevent.spawn(_stop_real_server)
    stop_server_thread.join()
    @py_assert0 = [
     200]
    @py_assert2 = 5
    @py_assert4 = @py_assert0 * @py_assert2
    @py_assert6 = [r.status_code for r in rs1]
    @py_assert5 = @py_assert4 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('(%(py1)s * %(py3)s) == %(py7)s', ), (@py_assert4, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(@py_assert0), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert6 = None
    @py_assert0 = [200]
    @py_assert3 = [r.status_code for r in rs2[:1]]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = [500]
    @py_assert2 = 4
    @py_assert4 = @py_assert0 * @py_assert2
    @py_assert6 = [r.status_code for r in rs2[1:]]
    @py_assert5 = @py_assert4 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('(%(py1)s * %(py3)s) == %(py7)s', ), (@py_assert4, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(@py_assert0), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert6 = None