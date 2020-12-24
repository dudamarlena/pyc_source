# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/beazley/Desktop/Projects/thredo/tests/test_io.py
# Compiled at: 2018-07-23 11:43:27
# Size of source mod 2**32: 17517 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, thredo
from thredo.socket import *

def test_read_partial():
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        client, addr = sock.accept()
        try:
            client.send(b'OK')
            s = client.as_stream()
            line = s.readline()
            results.append(line)
            data = s.read(2)
            results.append(data)
            data = s.read(1000)
            results.append(data)
        finally:
            client.close()
            sock.close()

    def test_client(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'hello\nworld\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     b'hello\n', b'wo', b'rld\n']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_readall():
    results = []
    evt = thredo.Event()

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            results.append('handler start')
            client.send(b'OK')
            with client.as_stream() as (s):
                data = s.readall()
                results.append(data)
                results.append('handler done')
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'Msg1\n')
        thredo.sleep(0.1)
        sock.send(b'Msg2\n')
        thredo.sleep(0.1)
        sock.send(b'Msg3\n')
        thredo.sleep(0.1)
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     'handler start', b'Msg1\nMsg2\nMsg3\n', 'handler done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_readall_partial():
    results = []
    evt = thredo.Event()

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            client.send(b'OK')
            s = client.as_stream()
            line = s.readline()
            results.append(line)
            data = s.readall()
            results.append(data)
            s.close()
        finally:
            client.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'hello\nworld\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [b'hello\n', b'world\n']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_readall_timeout():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            results.append('handler start')
            client.send(b'OK')
            s = client.as_stream()
            try:
                data = thredo.timeout_after(0.5, s.readall)
            except thredo.ThreadTimeout as e:
                results.append(e.bytes_read)

            results.append('handler done')
        finally:
            sock.close()
            client.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'Msg1\n')
        thredo.sleep(1)
        sock.send(b'Msg2\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     'handler start', b'Msg1\n', 'handler done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_read_exactly():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            results.append('handler start')
            client.send(b'OK')
            s = client.as_stream()
            for n in range(3):
                results.append(s.read_exactly(5))

            results.append('handler done')
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'Msg1\nMsg2\nMsg3\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     'handler start', b'Msg1\n', b'Msg2\n', b'Msg3\n', 'handler done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_read_exactly_incomplete():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            client.send(b'OK')
            s = client.as_stream()
            try:
                s.read_exactly(100)
            except EOFError as e:
                results.append(e.bytes_read)

        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'Msg1\nMsg2\nMsg3\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert0 = results[0]
    @py_assert3 = b'Msg1\nMsg2\nMsg3\n'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_read_exactly_timeout():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            results.append('handler start')
            client.send(b'OK')
            s = client.as_stream()
            try:
                data = thredo.timeout_after(0.5, s.read_exactly, 10)
                results.append(data)
            except thredo.ThreadTimeout as e:
                results.append(e.bytes_read)

            results.append('handler done')
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'Msg1\n')
        thredo.sleep(1)
        sock.send(b'Msg2\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     'handler start', b'Msg1\n', 'handler done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_readline():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            results.append('handler start')
            client.send(b'OK')
            s = client.as_stream()
            for n in range(3):
                results.append(s.readline())

            results.append('handler done')
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'Msg1\nMsg2\nMsg3\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     'handler start', b'Msg1\n', b'Msg2\n', b'Msg3\n', 'handler done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_readlines():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            client.send(b'OK')
            results.append('handler start')
            s = client.as_stream()
            results.extend(s.readlines())
            results.append('handler done')
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'Msg1\nMsg2\nMsg3\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     'handler start', b'Msg1\n', b'Msg2\n', b'Msg3\n', 'handler done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_readlines_timeout():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            client.send(b'OK')
            results.append('handler start')
            s = client.as_stream()
            try:
                thredo.timeout_after(0.5, s.readlines)
            except thredo.ThreadTimeout as e:
                results.extend(e.lines_read)

            results.append('handler done')
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'Msg1\nMsg2\n')
        thredo.sleep(1)
        sock.send(b'Msg3\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     'handler start', b'Msg1\n', b'Msg2\n', 'handler done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_writelines():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            results.append('handler start')
            client.send(b'OK')
            s = client.as_stream()
            results.append(s.readall())
            results.append('handler done')
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        s = sock.as_stream()
        s.writelines([b'Msg1\n', b'Msg2\n', b'Msg3\n'])
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     'handler start', b'Msg1\nMsg2\nMsg3\n', 'handler done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_writelines_timeout():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            client.send(b'OK')
            s = client.as_stream()
            thredo.sleep(1)
            results.append(s.readall())
        finally:
            client.close()
            sock.close()

    def line_generator():
        n = 0
        while True:
            yield b'Msg%d\n' % n
            n += 1

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        s = sock.as_stream()
        try:
            thredo.timeout_after(0.5, s.writelines, line_generator())
        except thredo.ThreadTimeout as e:
            results.append(e.bytes_written)

        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert0 = results[0]
    @py_assert4 = results[1]
    @py_assert6 = len(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_write_timeout():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            client.send(b'OK')
            s = client.as_stream()
            thredo.sleep(1)
            results.append(s.readall())
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        s = sock.as_stream()
        try:
            msg = b'x' * 10000000
            thredo.timeout_after(0.5, s.write, msg)
        except thredo.ThreadTimeout as e:
            results.append(e.bytes_written)

        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert0 = results[0]
    @py_assert4 = results[1]
    @py_assert6 = len(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_iterline():
    evt = thredo.Event()
    results = []

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            results.append('handler start')
            client.send(b'OK')
            s = client.as_stream()
            for line in s:
                results.append(line)

            results.append('handler done')
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.recv(8)
        sock.send(b'Msg1\nMsg2\nMsg3\n')
        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        serv.join()
        client.join()

    thredo.run(main)
    @py_assert2 = [
     'handler start', b'Msg1\n', b'Msg2\n', b'Msg3\n', 'handler done']
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_sendall_cancel():
    evt = thredo.Event()
    start = thredo.Event()
    results = {}

    def server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(address)
        sock.listen(1)
        evt.set()
        client, addr = sock.accept()
        try:
            start.wait()
            nrecv = 0
            while True:
                data = client.recv(1000000)
                if not data:
                    break
                nrecv += len(data)

            results['handler'] = nrecv
        finally:
            client.close()
            sock.close()

    def test_client(address):
        evt.wait()
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        try:
            sock.sendall(b'x' * 10000000)
        except thredo.ThreadCancelled as e:
            results['sender'] = e.bytes_sent

        sock.close()

    def main():
        serv = thredo.spawn(server, ('', 25000))
        client = thredo.spawn(test_client, ('localhost', 25000))
        thredo.sleep(0.1)
        client.cancel()
        start.set()
        serv.join()

    thredo.run(main)
    @py_assert0 = results['handler']
    @py_assert3 = results['sender']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None