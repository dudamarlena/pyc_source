# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\test\gdb_test.py
# Compiled at: 2020-01-16 08:24:16
"""
Unit tests
Run from top level directory: ./tests/test_app.py
"""
import os, random, unittest, subprocess
from time import time
from distutils.spawn import find_executable
from pygdbmi.StringStream import StringStream
from pygdbmi.gdbmiparser import parse_response, assert_match
from pygdbmi.gdbcontroller import GdbController, NoGdbProcessError, GdbTimeoutError
USING_WINDOWS = os.name == 'nt'
if USING_WINDOWS:
    MAKE_CMD = 'mingw32-make.exe'
else:
    MAKE_CMD = 'make'

class TestPyGdbMi(unittest.TestCase):

    def test_parser(self):
        """Test that the parser returns dictionaries from gdb mi strings as expected"""
        assert_match(parse_response('^done'), {'type': 'result', 'payload': None, 'message': 'done', 'token': None})
        assert_match(parse_response('~"done"'), {'type': 'console', 'payload': 'done', 'message': None})
        assert_match(parse_response('@"done"'), {'type': 'target', 'payload': 'done', 'message': None})
        assert_match(parse_response('&"done"'), {'type': 'log', 'payload': 'done', 'message': None})
        assert_match(parse_response('done'), {'type': 'output', 'payload': 'done', 'message': None})
        assert_match(parse_response('~""'), {'type': 'console', 'payload': '', 'message': None})
        assert_match(parse_response('~"\x08\x0c\n\r\t""'), {'type': 'console', 'payload': '\x08\x0c\n\r\t"', 'message': None})
        assert_match(parse_response('@""'), {'type': 'target', 'payload': '', 'message': None})
        assert_match(parse_response('@"\x08\x0c\n\r\t""'), {'type': 'target', 'payload': '\x08\x0c\n\r\t"', 'message': None})
        assert_match(parse_response('&""'), {'type': 'log', 'payload': '', 'message': None})
        assert_match(parse_response('&"\x08\x0c\n\r\t""'), {'type': 'log', 'payload': '\x08\x0c\n\r\t"', 'message': None})
        assert_match(parse_response('&"\\"'), {'type': 'log', 'payload': '\\', 'message': None})
        assert_match(parse_response('^done,thread-ids={thread-id="3",thread-id="2",thread-id="1"}, current-thread-id="1",number-of-threads="3"'), {'type': 'result', 
           'payload': {'thread-ids': {'thread-id': ['3', '2', '1']}, 'current-thread-id': '1', 
                       'number-of-threads': '3'}, 
           'message': 'done', 
           'token': None})
        assert_match(parse_response('=breakpoint-modified,bkpt={number="1",empty_arr=[],type="breakpoint",disp="keep",enabled="y",addr="0x000000000040059c",func="main",file="hello.cpp",fullname="hello.cpp",line="9",thread-groups=["i1"],times="1",original-location="hello.cpp:7"}'), {'message': 'breakpoint-modified', 
           'payload': {'bkpt': {'addr': '0x000000000040059c', 
                                'disp': 'keep', 
                                'enabled': 'y', 
                                'file': 'hello.cpp', 
                                'fullname': 'hello.cpp', 
                                'func': 'main', 
                                'line': '7', 
                                'number': '1', 
                                'empty_arr': [], 'original-location': 'hello.cpp:7', 
                                'thread-groups': [
                                                'i1'], 
                                'times': '1', 
                                'type': 'breakpoint'}}, 
           'type': 'notify', 
           'token': None})
        assert_match(parse_response('1342^done'), {'type': 'result', 'payload': None, 'message': 'done', 'token': 1342})
        assert_match(parse_response('=event,name="gdb"discardme'), {'type': 'notify', 
           'payload': {'name': 'gdb'}, 'message': 'event', 
           'token': None})
        return

    def _get_c_program(self, makefile_target_name, binary_name):
        """build c program and return path to binary"""
        find_executable(MAKE_CMD)
        if not find_executable(MAKE_CMD):
            print 'Could not find executable "%s". Ensure it is installed and on your $PATH.' % MAKE_CMD
            exit(1)
        SAMPLE_C_CODE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hello.cpp')
        binary_path = os.path.join(SAMPLE_C_CODE_DIR, binary_name)
        subprocess.call(['rm', 'pygdbmi.a*'], cwd=SAMPLE_C_CODE_DIR)
        subprocess.check_output([
         MAKE_CMD, makefile_target_name, '-C', SAMPLE_C_CODE_DIR, '--quiet'])
        return binary_path

    def test_controller(self):
        """Build a simple C program, then run it with GdbController and verify the output is parsed
        as expected"""
        gdbmi = GdbController()
        c_hello_world_binary = self._get_c_program('hello', 'pygdbmiapp.a')
        if USING_WINDOWS:
            c_hello_world_binary = c_hello_world_binary.replace('\\', '/')
        responses = gdbmi.write('-file-exec-and-symbols %s' % c_hello_world_binary, timeout_sec=1)
        assert len(responses) != 0
        response = responses[0]
        assert set(response.keys()) == {'message', 'type', 'payload', 'stream', 'token'}
        assert response['message'] == 'thread-group-added'
        assert response['type'] == 'notify'
        assert response['payload'] == {'id': 'i1'}
        assert response['stream'] == 'stdout'
        assert response['token'] is None
        responses = gdbmi.write(['-file-list-exec-source-files', '-break-insert main'])
        assert len(responses) != 0
        responses = gdbmi.write(['-exec-run', '-exec-continue'], timeout_sec=3)
        found_match = False
        print responses
        for r in responses:
            if r.get('payload', '') == '  leading spaces should be preserved. So should trailing spaces.  ':
                found_match = True

        assert found_match is True
        got_timeout_exception = False
        try:
            gdbmi.get_gdb_response(timeout_sec=0)
        except GdbTimeoutError:
            got_timeout_exception = True

        if not got_timeout_exception is True:
            raise AssertionError
            USING_WINDOWS or gdbmi.send_signal_to_gdb('SIGINT')
            gdbmi.send_signal_to_gdb(2)
            gdbmi.interrupt_gdb()
        responses = gdbmi.exit()
        assert responses is None
        assert gdbmi.gdb_process is None
        got_no_process_exception = False
        try:
            responses = gdbmi.write('-file-exec-and-symbols %s' % c_hello_world_binary)
        except NoGdbProcessError:
            got_no_process_exception = True

        if not got_no_process_exception is True:
            raise AssertionError
            gdbmi.spawn_new_gdb_subprocess()
            responses = gdbmi.write('-file-exec-and-symbols %s' % c_hello_world_binary, timeout_sec=1)
            responses = gdbmi.write(['-break-insert main', '-exec-run'])
            if not USING_WINDOWS:
                gdbmi.interrupt_gdb()
                gdbmi.send_signal_to_gdb(2)
                gdbmi.send_signal_to_gdb('sigTeRm')
                try:
                    gdbmi.send_signal_to_gdb('sigterms')
                    assert False
                except ValueError:
                    assert True

            responses = gdbmi.write('-exec-run')
            USING_WINDOWS or gdbmi.send_signal_to_gdb('sigstop')
        return

    def test_controller_buffer(self):
        """test that a partial response gets successfully buffered
        by the controller, then fully read when more data arrives"""
        gdbmi = GdbController()
        to_be_buffered = '^done,BreakpointTable={nr_rows="1",nr_'
        stream = 'teststream'
        response = gdbmi._get_responses_list(to_be_buffered, stream)
        assert len(response) == 0
        assert gdbmi._incomplete_output[stream] == to_be_buffered
        remaining_gdb_output = 'cols="6"}\n(gdb) \n'
        response = gdbmi._get_responses_list(remaining_gdb_output, stream)
        assert len(response) == 1
        r = response[0]
        assert r['stream'] == 'teststream'
        assert r['type'] == 'result'
        assert r['payload'] == {'BreakpointTable': {'nr_cols': '6', 'nr_rows': '1'}}

    def test_controller_buffer_randomized(self):
        """
        The following code reads a sample gdb mi stream randomly to ensure partial
        output is read and that the buffer is working as expected on all streams.
        """
        test_directory = os.path.dirname(os.path.abspath(__file__))
        datafile_path = '%s/response_samples.txt' % test_directory
        gdbmi = GdbController()
        for stream in gdbmi._incomplete_output.keys():
            responses = []
            with open(datafile_path, 'rb') as (f):
                while True:
                    n = random.randint(1, 100)
                    gdb_mi_simulated_output = f.read(n)
                    if gdb_mi_simulated_output == '':
                        break
                    responses += gdbmi._get_responses_list(gdb_mi_simulated_output, stream)

            if not len(responses) == 141:
                raise AssertionError
                assert_match(responses[0], {'message': None, 
                   'type': 'console', 
                   'payload': '0x00007fe2c5c58920 in __nanosleep_nocancel () at ../sysdeps/unix/syscall-template.S:81\\n', 
                   'stream': stream})
                USING_WINDOWS or assert_match(responses[71], {'stream': stream, 
                   'message': 'done', 
                   'type': 'result', 
                   'payload': None, 
                   'token': None})
                assert_match(responses[82], {'message': None, 
                   'type': 'output', 
                   'payload': 'The inferior program printed this! Can you still parse it?', 
                   'stream': stream})
            assert_match(responses[137], {'stream': stream, 
               'message': 'thread-group-exited', 
               'type': 'notify', 
               'payload': {'exit-code': '0', 'id': 'i1'}, 'token': None})
            assert_match(responses[138], {'stream': stream, 
               'message': 'thread-group-started', 
               'type': 'notify', 
               'payload': {'pid': '48337', 'id': 'i1'}, 'token': None})
            assert_match(responses[139], {'stream': stream, 
               'message': 'tsv-created', 
               'type': 'notify', 
               'payload': {'name': 'trace_timestamp', 'initial': '0'}, 'token': None})
            assert_match(responses[140], {'stream': stream, 
               'message': 'tsv-created', 
               'type': 'notify', 
               'payload': {'name': 'trace_timestamp', 'initial': '0'}, 'token': None})
            for stream in gdbmi._incomplete_output.keys():
                assert gdbmi._incomplete_output[stream] is None

        return


class TestPerformance(unittest.TestCase):

    def get_test_input(self, n_repetitions):
        data = (', ').join([ '"/a/path/to/parse/' + str(i) + '"' for i in range(n_repetitions) ])
        return '=test-message,test-data=[' + data + ']'

    def get_avg_time_to_parse(self, input_str, num_runs):
        avg_time = 0
        for _ in range(num_runs):
            t0 = time()
            parse_response(input_str)
            t1 = time()
            time_to_run = t1 - t0
            avg_time += time_to_run / num_runs

        return avg_time

    def test_big_o(self):
        num_runs = 2
        large_input_len = 100000
        single_input = self.get_test_input(1)
        large_input = self.get_test_input(large_input_len)
        t_small = self.get_avg_time_to_parse(single_input, num_runs) or 0.0001
        t_large = self.get_avg_time_to_parse(large_input, num_runs)
        bigo_n = t_large / large_input_len / t_small
        assert bigo_n < 1


class TestStringStream(unittest.TestCase):

    def test_api(self):
        raw_text = 'abc- "d" ""ef"" g'
        stream = StringStream(raw_text)
        assert stream.index == 0
        assert stream.len == len(raw_text)
        buf = stream.read(1)
        assert_match(buf, 'a')
        assert stream.index == 1
        stream.seek(-1)
        assert stream.index == 0
        buf = stream.advance_past_chars(['"'])
        buf = stream.advance_past_string_with_gdb_escapes()
        assert_match(buf, 'd')
        buf = stream.advance_past_chars(['"'])
        buf = stream.advance_past_chars(['"'])
        buf = stream.advance_past_string_with_gdb_escapes()
        assert_match(buf, 'ef')
        buf = stream.read(50)
        assert_match(buf, '" g')


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    num_failures = len(result.errors) + len(result.failures)
    return num_failures


if __name__ == '__main__':
    exit(main())