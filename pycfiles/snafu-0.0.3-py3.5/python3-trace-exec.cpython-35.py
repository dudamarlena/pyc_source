# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/python3-trace-exec.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 6508 bytes
import sys, os, time, json, base64, pickle, psutil, datetime, uuid

class Context:

    def __init__(self):
        self.SnafuContext = self


frame_time_dict = {'frame': time.time()}
open_connections_old = []
open_connections = []
open_files_old = []
open_files = []
saved_variables = {'last_line': 0, 'last_time': -1}
proc = psutil.Process(os.getpid())
time_now = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d-%H%M')
short_uuid = uuid.uuid4().hex[0:8]
func_name = sys.argv[2]
file_to_print_to_name = 'trace_log-' + func_name + '-' + time_now + '-' + short_uuid + '.log'
file_to_print_to = open(file_to_print_to_name, 'w')
print('Printing trace to ' + file_to_print_to_name, file=sys.stderr)

def trace(frame, event, arg):
    line_no = frame.f_lineno
    funcname = frame.f_code.co_name
    filename = frame.f_code.co_filename
    function_string = str(filename) + '.' + str(funcname)
    interval = 10
    if saved_variables['last_time'] == -1:
        proc.cpu_percent()
        proc.memory_percent()
        saved_variables['last_time'] = time.time()
    if int(100 * (time.time() - saved_variables['last_time'])) > interval:
        print('performance -- CPU: ' + str(proc.cpu_percent()) + '% - Memory: ' + str(proc.memory_percent()) + '%', file=file_to_print_to)
        saved_variables['last_time'] = time.time()
    open_conections = proc.connections()
    for connection in open_connections_old:
        if connection not in open_conections:
            protocol = 'udp' if connection.status == psutil.CONN_NONE else 'tcp'
            print('Connection CLOSED by ' + function_string + ': ' + protocol + ' connection from ' + connection.laddr.ip + ':' + str(connection.laddr.port) + ' to ' + connection.raddr.ip + ':' + str(connection.laddr.port), file=file_to_print_to)
            open_connections_old.remove(connection)

    for connection in open_conections:
        if connection not in open_connections_old:
            protocol = 'udp' if connection.status == psutil.CONN_NONE else 'tcp'
            print('Connection OPENED by ' + function_string + ': ' + protocol + ' connection from ' + connection.laddr.ip + ':' + str(connection.laddr.port) + ' to ' + connection.raddr.ip + ':' + str(connection.laddr.port), file=file_to_print_to)
            open_connections_old.append(connection)

    open_files = proc.open_files()
    for open_file in open_files_old:
        if open_file not in open_files:
            acces_type = open_file.mode
            print('File CLOSED by ' + function_string + ' - Path: ' + open_file.path, file=file_to_print_to)
            open_files_old.remove(open_file)

    for open_file in open_files:
        if open_file not in open_files_old:
            acces_type = open_file.mode
            print('File OPENED by ' + function_string + " in mode '" + acces_type + "' - Path: " + open_file.path, file=file_to_print_to)
            open_files_old.append(open_file)

    has_caller = frame.f_back is not None
    caller_string = ''
    if has_caller:
        caller = frame.f_back
        caller_funcname = caller.f_code.co_name
        caller_filename = caller.f_code.co_filename
        caller_string = caller_filename + '.' + caller_funcname
    if event == 'call':
        frame_time_dict[frame] = time.time()
        print('call from \t' + caller_string + ' to ' + function_string, file=file_to_print_to)
    if event == 'return':
        time_elapsed_ms = round((time.time() - frame_time_dict[frame]) * 1000, 6)
        print('return from \t' + function_string + ' to ' + caller_string + ' - time elapsed: ' + str(time_elapsed_ms) + 'ms', file=file_to_print_to)
    if event == 'exception':
        print('exception in \t' + function_string + ' at line ' + str(saved_variables['last_line']) + ': ' + str(arg), file=file_to_print_to)
    if event == 'line':
        saved_variables['last_line'] = frame.f_lineno
    return trace


def execute(filename, func, funcargs, envvars):
    funcargs = json.loads(funcargs)
    envvars = json.loads(envvars)
    for i, funcarg in enumerate(funcargs):
        if type(funcarg) == str and funcarg.startswith('pickle:'):
            sys.modules['lib'] = Context()
            sys.modules['lib.snafu'] = Context()
            funcarg = None

    sys.path.append('.')
    os.chdir(os.path.dirname(filename))
    mod = __import__(os.path.basename(filename[:-3]))
    func = getattr(mod, func)
    for envvar in envvars:
        os.environ[envvar] = envvars[envvar]

    stime = time.time()
    try:
        sys.settrace(trace)
        res = func(*funcargs)
        sys.settrace(None)
        success = True
    except Exception as e:
        res = e
        success = False

    dtime = (time.time() - stime) * 1000
    return '{} {} {}'.format(dtime, success, '{}'.format(res).replace("'", '"'))


print(execute(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))