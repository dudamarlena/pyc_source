# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rc/test/test_run.py
# Compiled at: 2020-04-22 01:34:45
# Size of source mod 2**32: 3345 bytes
from rc import run, running, run_stream, handle_stream, STDERR, STDOUT, EXIT, print_stream, save_stream_to_file, gcloud
import contextlib
from io import StringIO
import time

def test_run_sh_syntax():
    assert run(['ls', '~']).returncode == 0
    assert run('ls ~').returncode == 0
    assert run(['cat', '"~"']) == run('cat "~"')


def test_run_multiple_line():
    assert run('cat', input='hello world\naaa').stdout == 'hello world\naaa'
    assert run('bash', input='date\nls /\necho hello world\n').stdout.strip().split('\n')[(-1)] == 'hello world'
    assert run('python', input="\nprint('hello world')\nprint('aaa')\n").stdout.strip() == 'hello world\naaa'


def test_run_stream():
    q, _ = run_stream('python', input='\nimport sys\nimport time\nsys.stdout.write(\'to stdout\\n\')\nsys.stdout.flush()\ntime.sleep(1) # sleep to make stdout happens earlier than stderr for sure\nsys.stderr.write("to stderr\\n")\nsys.stderr.flush()\ntime.sleep(1)\nsys.stdout.write(\'hello world\\n\')\nsys.stdout.flush()\nexit(1)\n    ')
    t = q.get()
    assert t == (STDOUT, 'to stdout\n')
    q.task_done()
    t = q.get()
    assert t == (STDERR, 'to stderr\n')
    q.task_done()
    t = q.get()
    assert t == (STDOUT, 'hello world\n')
    q.task_done()
    t = q.get()
    assert t == (EXIT, 1)
    q.task_done()
    assert q.empty()


def test_handle_stream():
    q, _ = run_stream('sh', input='\n    echo to stdout\n    echo 1>&2 to stderr\n    echo hello world\n    exit 1\n    ')
    stdout = []
    stderr = []
    exitcode = []
    handle_stream(q, stdout_handler=(lambda line: stdout.append(line)),
      stderr_handler=(lambda line: stderr.append(line)),
      exit_handler=(lambda x: exitcode.append(x)))
    assert stdout == ['to stdout\n', 'hello world\n']
    assert stderr == ['to stderr\n']
    assert exitcode == [1]


def test_print_stream():
    q, _ = run_stream('sh', input='\n    echo to stdout\n    echo 1>&2 to stderr\n    echo hello world\n    exit 1\n    ')
    temp_stdout = StringIO()
    with contextlib.redirect_stdout(temp_stdout):
        print_stream(q, prefix='node1')
    output = temp_stdout.getvalue().split('\n')
    assert output[(-1)] == 'node1 EXIT CODE | 1'
    assert output.sort() == 'node1 STDERR | to stderr\nnode1 STDOUT | to stdout\nnode1 STDOUT | hello world\nnode1 EXIT CODE | 1'.split('\n').sort()


def save_stream_to_file():
    q, _ = run_stream('sh', input='\n    echo to stdout\n    echo 1>&2 to stderr\n    echo hello world\n    exit 1\n    ')
    save_stream_to_file(path='/tmp', name='node1')
    assert open('/tmp/node1.stdout').read() == 'node1 STDOUT | to stdout\nnode1 STDOUT | hello world'
    assert open('/tmp/node1.stderr').read() == 'node1 STDERR | to stderr\n'
    assert open('/tmp/node1.exitcode').read() == 'node1 EXIT CODE | 1'


def test_tmux():
    machine = gcloud.create(name='test-rc-node', machine_type='n1-standard-1', disk_size='20G', image_project='ubuntu-os-cloud', image_family='ubuntu-1804-lts', zone='us-west2-a',
      preemptible=False,
      firewall_allows=['tcp:8080'])
    machine = gcloud.get('test-rc-node')
    machine.run('sudo apt install tmux')
    machine.run_detach_tmux('while true; do echo aaaaaa; sleep 10; done')
    machine.kill_detach_tmux()
    assert machine.run('cat /tmp/python-rc.log').stdout == 'aaaaaa\n'
    machine.delete()