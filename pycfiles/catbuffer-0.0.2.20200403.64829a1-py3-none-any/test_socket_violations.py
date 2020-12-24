# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./tests/test_socket_violations.py
# Compiled at: 2014-08-28 16:31:11
import os, socket, testify as T, catbox

def _catbox_it(f):
    result = catbox.run(f, collect_only=True, network=False, writable_paths=[])
    return (
     result.code, result.violations)


class TestSocketViolations(T.TestCase):

    def assert_violations(self, violations, kind, args):
        matching = [ v_arg for (v_kind, _, v_arg) in violations if v_kind == kind ]
        if type(args) is int:
            self.assertEquals(args, len(matching))
        else:
            self.assertEquals(args, matching)

    def test_sock_tcp_ipv4(self):
        s1 = socket.socket()
        s1.listen(1)
        (host, port) = s1.getsockname()

        def run():
            s2 = socket.socket()
            s2.connect((host, port))
            s2.close()

        (code, v) = _catbox_it(run)
        self.assertEquals(0, code)
        self.assertEquals(2, len(v))
        self.assert_violations(v, 'connect', ['%s:%d' % (host, port)])
        self.assert_violations(v, 'socketcall', 1)
        s1.close()

    def test_sock_tcp_ipv6(self):
        s1 = socket.socket(socket.AF_INET6)
        s1.listen(1)
        (host, port, _, _) = s1.getsockname()

        def run():
            s2 = socket.socket(socket.AF_INET6)
            s2.connect((host, port))
            s2.close()

        (code, v) = _catbox_it(run)
        self.assertEquals(0, code)
        self.assert_violations(v, 'connect', ['%s:%d' % (host, port)])
        self.assertTrue(len(v) in (2, 3))
        self.assert_violations(v, 'socketcall', len(v) - 1)
        s1.close()

    def test_sock_unix(self):
        path = os.path.abspath('./socket.sock')
        try:
            os.unlink(path)
        except OSError:
            if os.path.exists(path):
                raise

        s1 = socket.socket(socket.AF_UNIX)
        s1.bind(path)
        s1.listen(1)

        def run():
            s2 = socket.socket(socket.AF_UNIX)
            s2.connect(path)
            s2.close()

        (code, v) = _catbox_it(run)
        self.assertEquals(0, code)
        self.assertEquals(2, len(v))
        self.assert_violations(v, 'connect', [path])
        self.assert_violations(v, 'socketcall', 1)
        s1.close()

    def test_nosyscall(self):

        def run():
            pass

        (code, v) = _catbox_it(run)
        self.assertEquals(0, code)
        self.assertEquals([], v)