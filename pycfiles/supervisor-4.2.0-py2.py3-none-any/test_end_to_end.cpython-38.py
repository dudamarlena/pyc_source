# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/tests/test_end_to_end.py
# Compiled at: 2019-05-28 13:56:42
# Size of source mod 2**32: 10018 bytes
from __future__ import unicode_literals
import os, sys, signal, unittest, pkg_resources
from supervisor.compat import xmlrpclib
from supervisor.xmlrpc import SupervisorTransport
if 'END_TO_END' in os.environ:
    import pexpect
    BaseTestCase = unittest.TestCase
else:
    BaseTestCase = object

class EndToEndTests(BaseTestCase):

    def test_issue_565(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-565.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        supervisord.expect_exact('success: hello entered RUNNING state')
        args = [
         '-m', 'supervisor.supervisorctl', '-c', filename, 'tail', '-f', 'hello']
        supervisorctl = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisorctl.kill, signal.SIGINT)
        for i in range(1, 4):
            line = 'The Øresund bridge ends in Malmö - %d' % i
            supervisorctl.expect_exact(line, timeout=30)

    def test_issue_638(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-638.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        is_py2 = sys.version_info[0] < 3
        if is_py2:
            b_prefix = ''
        else:
            b_prefix = 'b'
        supervisord.expect_exact(("Undecodable: %s'\\x88\\n'" % b_prefix), timeout=30)
        supervisord.expect('received SIGCH?LD indicating a child quit', timeout=30)
        if is_py2:
            supervisord.expect_exact('gave up: produce-unicode-error entered FATAL state, too many start retries too quickly', timeout=60)

    def test_issue_663(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-663.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        for i in range(2):
            supervisord.expect_exact('OKREADY', timeout=60)
            supervisord.expect_exact('BUSY -> ACKNOWLEDGED', timeout=30)

    def test_issue_664(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-664.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        supervisord.expect_exact('test_öäü entered RUNNING state', timeout=60)
        args = ['-m', 'supervisor.supervisorctl', '-c', filename, 'status']
        supervisorctl = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisorctl.kill, signal.SIGINT)
        try:
            supervisorctl.expect('test_öäü\\s+RUNNING', timeout=30)
            seen = True
        except pexpect.ExceptionPexpect:
            seen = False
        else:
            self.assertTrue(seen)

    def test_issue_835(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-835.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        supervisord.expect_exact('cat entered RUNNING state', timeout=60)
        transport = SupervisorTransport('', '', 'unix:///tmp/issue-835.sock')
        server = xmlrpclib.ServerProxy('http://anything/RPC2', transport)
        try:
            for s in ('The Øresund bridge ends in Malmö', 'hello'):
                result = server.supervisor.sendProcessStdin('cat', s)
                self.assertTrue(result)
                supervisord.expect_exact(s, timeout=30)

        finally:
            transport.connection.close()

    def test_issue_836(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-836.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        supervisord.expect_exact('cat entered RUNNING state', timeout=60)
        args = ['-m', 'supervisor.supervisorctl', '-c', filename, 'fg', 'cat']
        supervisorctl = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisorctl.kill, signal.SIGINT)
        try:
            for s in ('Hi', 'Hello', 'The Øresund bridge ends in Malmö'):
                supervisorctl.sendline(s)
                supervisord.expect_exact(s, timeout=60)
                supervisorctl.expect_exact(s)
                supervisorctl.expect_exact(s)
            else:
                seen = True

        except pexpect.ExceptionPexpect:
            seen = False
        else:
            self.assertTrue(seen)

    def test_issue_1054(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-1054.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        supervisord.expect_exact('cat entered RUNNING state', timeout=60)
        args = ['-m', 'supervisor.supervisorctl', '-c', filename, 'avail']
        supervisorctl = pexpect.spawn((sys.executable), args, encoding='utf-8')
        try:
            supervisorctl.expect('cat\\s+in use\\s+auto', timeout=30)
            seen = True
        except pexpect.ExceptionPexpect:
            seen = False
        else:
            self.assertTrue(seen)

    def test_issue_1224(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-1224.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        supervisord.expect_exact('cat entered RUNNING state', timeout=60)

    def test_issue_1231a(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-1231.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        supervisord.expect_exact('success: hello entered RUNNING state')
        args = [
         '-m', 'supervisor.supervisorctl', '-c', filename, 'tail', '-f', 'hello']
        supervisorctl = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisorctl.kill, signal.SIGINT)
        for i in range(1, 4):
            line = '%d - hash=57d94b…381088' % i
            supervisorctl.expect_exact(line, timeout=30)

    def test_issue_1231b--- This code section failed: ---

 L. 156         0  LOAD_GLOBAL              pkg_resources
                2  LOAD_METHOD              resource_filename
                4  LOAD_GLOBAL              __name__
                6  LOAD_STR                 'fixtures/issue-1231.conf'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'filename'

 L. 157        12  LOAD_STR                 '-m'
               14  LOAD_STR                 'supervisor.supervisord'
               16  LOAD_STR                 '-c'
               18  LOAD_FAST                'filename'
               20  BUILD_LIST_4          4 
               22  STORE_FAST               'args'

 L. 158        24  LOAD_GLOBAL              pexpect
               26  LOAD_ATTR                spawn
               28  LOAD_GLOBAL              sys
               30  LOAD_ATTR                executable
               32  LOAD_FAST                'args'
               34  LOAD_STR                 'utf-8'
               36  LOAD_CONST               ('encoding',)
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  STORE_FAST               'supervisord'

 L. 159        42  LOAD_FAST                'self'
               44  LOAD_METHOD              addCleanup
               46  LOAD_FAST                'supervisord'
               48  LOAD_ATTR                kill
               50  LOAD_GLOBAL              signal
               52  LOAD_ATTR                SIGINT
               54  CALL_METHOD_2         2  ''
               56  POP_TOP          

 L. 160        58  LOAD_FAST                'supervisord'
               60  LOAD_METHOD              expect_exact
               62  LOAD_STR                 'success: hello entered RUNNING state'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L. 162        68  LOAD_STR                 '-m'
               70  LOAD_STR                 'supervisor.supervisorctl'
               72  LOAD_STR                 '-c'
               74  LOAD_FAST                'filename'
               76  LOAD_STR                 'tail'
               78  LOAD_STR                 '-f'
               80  LOAD_STR                 'hello'
               82  BUILD_LIST_7          7 
               84  STORE_FAST               'args'

 L. 163        86  LOAD_GLOBAL              os
               88  LOAD_ATTR                environ
               90  LOAD_METHOD              copy
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'env'

 L. 164        96  LOAD_STR                 'oops'
               98  LOAD_FAST                'env'
              100  LOAD_STR                 'LANG'
              102  STORE_SUBSCR     

 L. 165       104  LOAD_GLOBAL              pexpect
              106  LOAD_ATTR                spawn
              108  LOAD_GLOBAL              sys
              110  LOAD_ATTR                executable
              112  LOAD_FAST                'args'
              114  LOAD_STR                 'utf-8'

 L. 166       116  LOAD_FAST                'env'

 L. 165       118  LOAD_CONST               ('encoding', 'env')
              120  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              122  STORE_FAST               'supervisorctl'

 L. 167       124  LOAD_FAST                'self'
              126  LOAD_METHOD              addCleanup
              128  LOAD_FAST                'supervisorctl'
              130  LOAD_ATTR                kill
              132  LOAD_GLOBAL              signal
              134  LOAD_ATTR                SIGINT
              136  CALL_METHOD_2         2  ''
              138  POP_TOP          

 L. 172       140  LOAD_GLOBAL              sys
              142  LOAD_ATTR                version_info
              144  LOAD_CONST               None
              146  LOAD_CONST               2
              148  BUILD_SLICE_2         2 
              150  BINARY_SUBSCR    
              152  LOAD_CONST               (3, 7)
              154  COMPARE_OP               <
              156  POP_JUMP_IF_FALSE   186  'to 186'

 L. 173       158  LOAD_FAST                'supervisorctl'
              160  LOAD_ATTR                expect
              162  LOAD_STR                 'Warning: sys.stdout.encoding is set to '

 L. 174       164  LOAD_CONST               30

 L. 173       166  LOAD_CONST               ('timeout',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 175       172  LOAD_FAST                'supervisorctl'
              174  LOAD_ATTR                expect
              176  LOAD_STR                 'Unicode output may fail.'
              178  LOAD_CONST               30
              180  LOAD_CONST               ('timeout',)
              182  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              184  POP_TOP          
            186_0  COME_FROM           156  '156'

 L. 177       186  LOAD_GLOBAL              range
              188  LOAD_CONST               1
              190  LOAD_CONST               4
              192  CALL_FUNCTION_2       2  ''
              194  GET_ITER         
              196  FOR_ITER            278  'to 278'
              198  STORE_FAST               'i'

 L. 178       200  LOAD_STR                 '%d - hash=57d94b…381088'
              202  LOAD_FAST                'i'
              204  BINARY_MODULO    
              206  STORE_FAST               'line'

 L. 179       208  SETUP_FINALLY       228  'to 228'

 L. 180       210  LOAD_FAST                'supervisorctl'
              212  LOAD_ATTR                expect_exact
              214  LOAD_FAST                'line'
              216  LOAD_CONST               30
              218  LOAD_CONST               ('timeout',)
              220  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              222  POP_TOP          
              224  POP_BLOCK        
              226  JUMP_BACK           196  'to 196'
            228_0  COME_FROM_FINALLY   208  '208'

 L. 181       228  DUP_TOP          
              230  LOAD_GLOBAL              pexpect
              232  LOAD_ATTR                exceptions
              234  LOAD_ATTR                EOF
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   274  'to 274'
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 182       248  LOAD_FAST                'self'
              250  LOAD_METHOD              assertIn
              252  LOAD_STR                 'Unable to write Unicode to stdout because it has encoding '

 L. 184       254  LOAD_FAST                'supervisorctl'
              256  LOAD_ATTR                before

 L. 182       258  CALL_METHOD_2         2  ''
              260  POP_TOP          

 L. 185       262  POP_EXCEPT       
              264  POP_TOP          
          266_268  BREAK_LOOP          278  'to 278'
              270  POP_EXCEPT       
              272  JUMP_BACK           196  'to 196'
            274_0  COME_FROM           238  '238'
              274  END_FINALLY      
              276  JUMP_BACK           196  'to 196'

Parse error at or near `POP_TOP' instruction at offset 264

    def test_issue_1231c(self):
        filename = pkg_resources.resource_filename(__name__, 'fixtures/issue-1231.conf')
        args = ['-m', 'supervisor.supervisord', '-c', filename]
        supervisord = pexpect.spawn((sys.executable), args, encoding='utf-8')
        self.addCleanup(supervisord.kill, signal.SIGINT)
        supervisord.expect_exact('success: hello entered RUNNING state')
        args = [
         '-m', 'supervisor.supervisorctl', '-c', filename, 'tail', 'hello']
        env = os.environ.copy()
        env['LANG'] = 'oops'
        supervisorctl = pexpect.spawn((sys.executable), args, encoding='utf-8', env=env)
        self.addCleanup(supervisorctl.kill, signal.SIGINT)
        if sys.version_info[:2] < (3, 7):
            supervisorctl.expect('Warning: sys.stdout.encoding is set to ', timeout=30)
            supervisorctl.expect('Unicode output may fail.', timeout=30)


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')