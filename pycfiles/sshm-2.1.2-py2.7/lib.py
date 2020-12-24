# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sshm/lib.py
# Compiled at: 2016-05-31 17:28:44
import re, subprocess, threading, zmq
from itertools import product
from traceback import format_exc
__all__ = [
 'sshm', 'uri_expansion']
disable_formatting = False
default_workers = 20
_match_ranges = re.compile('(?:(\\d+)(?:,|$))|(?:(\\d+-\\d+))')

def expand_ranges(to_expand):
    """
    Convert a comma-seperated range of integers into a list. Keep any zero
    padding the numbers may have.  If the provided string is just a -, then I
    will return an entire range.

        Example: "1,4,07-10" to ['1', '4', '07', '08', '09', '10']

    @param to_expand: Expand this string into a list of integers.
    @type to_expand: str
    """
    if to_expand == '-':
        for i in range(0, 256):
            yield str(i)

    for single, range_str in _match_ranges.findall(to_expand):
        if single:
            yield single
        if range_str:
            i, j = range_str.split('-')
            padding = '%' + '0.%d' % len(i) + 'd'
            for k in range(int(i), int(j) + 1):
                yield padding % k


def create_uri(user, target, port):
    """
    Create a valid URI from the provided parameters.
    """
    if user and port:
        return user + '@' + target + ':' + port
    else:
        if user:
            return user + '@' + target
        if port:
            return target + ':' + port
        return target


_parse_uri = re.compile('(?:(\\w+)@)?(?:(?:([a-zA-Z][\\w.-]+)(?:\\[([\\d,-]+)\\])?([\\w.]+)?)|((?:(?:(?:\\d+-\\d+)|(?:\\d+,\\d+)|(?:\\d+)|(?:-))+\\.){3}(?:(?:\\d+-\\d+)|(?:\\d+,\\d+)|(?:\\d+)|(?:-)))(?=,|$|:))(?::(\\d+))?,?')

def uri_expansion(input_str):
    """
    Expand a list of uris into invividual URLs/IPs and their respective
    ports and usernames. Preserve any zero-padding the range may contain.

    @param input_str: The uris to expand
    @type input_str: str
    """
    try:
        uris = _parse_uri.findall(input_str)
    except TypeError:
        raise ValueError('Unable to parse provided URIs')

    yielded_something = False
    for uri in uris:
        user, prefix, range_str, suffix, ip_addr, port = uri
        if (prefix or suffix) and range_str:
            i = product([prefix], expand_ranges(range_str), [suffix])
            i = [ ('').join(iter(j)) for j in i ]
            for k in i:
                yielded_something = True
                yield create_uri(user, k, port)

        elif ip_addr:
            if '-' in ip_addr or ',' in ip_addr:
                x = [ expand_ranges(i) for i in ip_addr.split('.') ]
                j = product(x[0], x[1], x[2], x[3])
                l = [ ('.').join(iter(k)) for k in j ]
                for i in l:
                    yielded_something = True
                    yield create_uri(user, i, port)

            else:
                yielded_something = True
                yield create_uri(user, ip_addr, port)
        else:
            yielded_something = True
            yield create_uri(user, prefix + suffix, port)

    if not yielded_something:
        raise ValueError(('No URIs found in "{}"').format(input_str))


def popen(cmd, stdin, stdout, stderr):
    """
    Separating Popen call from ssh command for testing.
    """
    proc = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
    return proc


SINK_URL = 'inproc://sink'
STDIN_URL = 'inproc://stdin'

def ssh(thread_num, context, uri, command, extra_arguments, if_stdin=False):
    """
    Create an SSH connection to 'uri'.  Execute 'command' and
    pass any stdin to this ssh session.  Return the results via ZMQ (SINK_URL).

    @param context: Create all ZMQ sockets using this context.
    @type context: zmq.Context

    @param uri: user@example.com:22
    @type uri: str

    @param commmand: Execute this command on 'uri'.
    @type command: str

    @param extra_arguments: Pass these extra arguments to the ssh call.
    @type extra_arguments: list

    @param if_stdin: If this is True, this function will request stdin and
        write it to proc's stdin.
    @type if_stdin: bool

    @returns: None
    """
    global disable_formatting
    result = {'thread_num': thread_num, 
       'uri': uri}
    sink = context.socket(zmq.PUSH)
    sink.connect(SINK_URL)
    stdin_sock = context.socket(zmq.REQ)
    stdin_sock.connect(STDIN_URL)
    formatting_dict = {'uri': uri, 
       'fqdn': uri.split(':')[0], 
       'subdomain': uri.split('.')[0], 
       'num': thread_num}
    try:
        cmd = [
         'ssh']
        cmd.extend(extra_arguments or [])
        if not disable_formatting:
            command = command.format(**formatting_dict)
        try:
            user_url, port = uri.split(':')
            cmd.extend([user_url, '-p', port, command])
        except ValueError:
            cmd.extend([uri, command])

        proc = popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while if_stdin:
            stdin_sock.send_pyobj(thread_num)
            chunk = stdin_sock.recv_pyobj()
            if chunk == None:
                break
            while proc.poll() == None:
                try:
                    proc.stdin.write(chunk)
                    break
                except IOError:
                    pass

        stdout, stderr = proc.communicate()
        proc.stdin.close()
        if 'decode' in dir(stdout):
            stdout = stdout.decode()
        if 'decode' in dir(stderr):
            stderr = stderr.decode()
        result.update({'return_code': proc.returncode, 'stdout': stdout, 
           'stderr': stderr})
    except:
        result.update({'traceback': format_exc()})

    result.update({'cmd': cmd})
    sink.send_pyobj(result)
    sink.close()
    return


CHUNK_SIZE = 65536

def sshm(servers, command, extra_arguments=None, stdin=None, disable_formatting_var=False, workers=default_workers):
    """
    SSH into multiple servers and execute "command". Pass stdin to these ssh
    handles.

    This is a generator to facilitate using the results of each ssh command as
    they become available.

    @param servers: A list of strings or a string containing the servers to
    execute "command" on via
        SSH.
        Examples:
            ['example.com']
            ['example[1-3].com']
            ['mail[1,3,8].example.com', 'example.com']
    @type servers: str

    @param command: A string containing the command to execute.
    @type command: str

    @param extra_arguments: These arguments will be passed directly to each SSH
        subprocess instance.
    @type extra_arguments: list

    @param stdin: A file object that will be passed to each subproccess
        instance.
    @type stdin: file

    @param workers: The max amount of concurrent SSH connections.
    @type workers: int

    @returns: A list containing (success, handle, message) from each method
        call.
    """
    global disable_formatting
    if type(servers) == str:
        servers = [
         servers]
    disable_formatting = disable_formatting_var
    context = zmq.Context()
    sink = context.socket(zmq.PULL)
    sink.bind(SINK_URL)
    stdin_sock = context.socket(zmq.REP)
    stdin_sock.bind(STDIN_URL)
    if 'buffer' in dir(stdin):
        stdin = stdin.buffer
    if_stdin = True if stdin else False
    poller = zmq.Poller()
    poller.register(sink, zmq.POLLIN)
    poller.register(stdin_sock, zmq.POLLIN)
    stdin_queue = {}
    stdin_chunks = {}
    chunk_count = 1
    threads = {}
    thread_num = 0
    uri_gen = uri_expansion(servers.pop(0))
    next_uri = next(uri_gen)
    while next_uri or threads:
        while next_uri and len(threads) < workers:
            thread = threading.Thread(target=ssh, args=(thread_num, context,
             next_uri, command, extra_arguments, if_stdin))
            thread.start()
            threads[thread_num] = thread
            thread_num += 1
            try:
                next_uri = next(uri_gen)
            except StopIteration:
                try:
                    uri_gen = uri_expansion(servers.pop(0))
                    next_uri = next(uri_gen)
                except IndexError:
                    next_uri = None

        socks = dict(poller.poll())
        if socks.get(sink) == zmq.POLLIN:
            results = sink.recv_pyobj()
            yield results
            threads[results['thread_num']].join()
            del threads[results['thread_num']]
        elif socks.get(stdin_sock) == zmq.POLLIN:
            thread_num = stdin_sock.recv_pyobj()
            if thread_num not in stdin_queue:
                stdin_queue[thread_num] = 1
            if stdin_queue[thread_num] not in stdin_chunks:
                chunk = stdin.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    chunk = None
                stdin_chunks[chunk_count] = chunk
                chunk_count += 1
            chunk = stdin_chunks[stdin_queue[thread_num]]
            stdin_sock.send_pyobj(chunk)
            stdin_queue[thread_num] += 1

    sink.close()
    stdin_sock.close()
    context.term()
    return