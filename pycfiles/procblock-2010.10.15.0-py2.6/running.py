# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/procblock/run/running.py
# Compiled at: 2010-10-14 14:04:21
"""
running

Running threads and shell commands, for procblock.
"""
import subprocess, threading, time, os, copy, pprint, logging, code_python, unidist
from unidist import error_info
from unidist.log import log
from unidist import sharedlock
from unidist import sharedstate
from unidist import sharedcounter
from unidist import timeseries
RUN_CACHE_DEFAULT_HISTORY_MAXIMUM = 100
RUN_CACHE_DEFAULT_INTERVAL = 5
COMMAND_CACHE_TIMEOUT_DEFAULT = 60

def Run(command, cache=False, cache_timeout=COMMAND_CACHE_TIMEOUT_DEFAULT):
    """Actually run the command on the local machine.  Blocks until complete.
  
  Args:
    command: string, command to execute
    cache: boolean (default False), cache this command [TBD: Add cache timeout...]
  
  TODO(g): Store commands and cache for internals viewing?
  """
    output_error = ''
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    status = pipe.wait()
    output = pipe.stdout.read()
    output_error = pipe.stderr.read()
    pipe.stderr.close()
    pipe.stdout.close()
    if status != 0:
        log('Non-Zero Exit Code: %s: %s: %s' % (status, command, output_error), logging.INFO)
    if not command.startswith('rrdtool'):
        sharedstate.Set('__internals.run', command, (time.time(), status, output, output_error))
    return (status, output, output_error)


def TimeSeriesCollection(run_item, result):
    """Collect time series information into timeseries data source."""
    collect_items = run_item['timeseries collect']
    for item in collect_items:
        TimeSeriesCollectionItem({'timeseries collect': item}, result)


def TimeSeriesCollectionItem(run_item, result):
    """Collect time series information into timeseries data source."""
    collect = run_item['timeseries collect']
    graph = collect.get('graph', None)
    key_series = collect.get('key', None)
    filename = collect['path']
    filename_template = filename
    interval = collect['interval']
    occurred = time.time()
    if key_series:
        if key_series not in result:
            Exception('Key series key not found in result: %s: %s: %s' % (filename, key_series, result))
        items = {}
        for key in result[key_series]:
            items[key] = result[key_series]

    else:
        items = [
         None]
    create_fields = collect['fields']
    if not create_fields:
        log('No field data returned: %s ')
        return
    else:
        for key_series_item in items:
            if key_series_item != None:
                key_str = key_series_item.replace('/', 'slash').replace(' ', 'space')
                filename = filename_template.replace('%(key)', key_str)
            if '%(node)s' in filename:
                node_name = unidist.node.GetNamePathReady()
                filename = filename.replace('%(node)s', node_name)
            if not os.path.isdir(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except Exception, e:
                    pass

            if not os.path.exists(filename):
                timeseries.Create(filename, interval, create_fields)
            fields = {}
            if key_series_item == None:
                for key in create_fields:
                    if key in result:
                        fields[key] = result[key]
                    else:
                        fields[key] = 'NaN'

            else:
                for key in create_fields:
                    if key_series in result and key_series_item in result[key_series] and key in result[key_series][key_series_item]:
                        fields[key] = result[key_series][key_series_item][key]
                    else:
                        print 'Couldnt find field: %s: %s: %s: %s' % (key_series, key_series_item, key, filename)
                        fields[key] = 'NaN'

                timeseries.Store(filename, interval, occurred, fields)
                sharedstate.Set('__internals.timeseries', filename, (occurred, collect, fields))
            if 0 and graph:
                for graph_item in graph:
                    method = graph_item.get('method', 'STACK')
                    node_name = unidist.node.GetNamePathReady()
                    if key_series_item:
                        title = str(graph_item.get('title', 'title')).replace('%(key)s', key_series_item).replace('%(node)s', node_name)
                        graph_path = graph_item['path'].replace('%(key)s', key_series_item.replace('/', 'slash').replace(' ', 'space')).replace('%(node)s', node_name)
                    else:
                        title = graph_item.get('title', 'title')
                        graph_path = graph_item['path'].replace('%(node)s', node_name)
                    label_vertical = graph_item.get('vertical label', 'vertical label')
                    if not os.path.isdir(os.path.dirname(graph_path)):
                        os.makedirs(os.path.dirname(graph_path))
                    timeseries.Graph(filename, graph_path, create_fields, graph_item['fields'], method, title, label_vertical)

        return


def ExecuteScript(python_script, pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Execute the specified script.  This will ensure it is imported, and
  re-imported if the code changes on the disk.
  
  TODO(g): Implement in-memory cache of md5-sums from the Manager, specifying
      the md5-sum of each script, and do not import if it is not the same.
      Instead, alert on a locally changed script.
  """
    script_module = code_python.GetPythonScriptModule(python_script)
    if script_module == None:
        log('Failed to find python script: %s' % os.path.abspath(python_script), logging.ERROR)
        return
    else:
        try:
            result = script_module.ProcessBlock(pipe_data, block, request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block_parent)
            sharedstate.Set('__internals.execute', python_script, (time.time(), result))
        except Exception, e:
            log('Exception in script: %s: %s' % (python_script, e))
            raise

        return result


class RunScriptFailedCondition(Exception):
    """Failed to pass all "if" conditions."""
    pass


class RunThreadHandler:

    def __init__(self):
        self.run_thread_id_next = 0
        self.run_thread_id_lock = threading.Lock()
        self.run_thread_objects = {}

    def GetNextRunThreadId(self):
        """Returns the next action_id, for a new RunThread."""
        self.run_thread_id_lock.acquire()
        next_id = self.run_thread_id_next
        self.run_thread_id_next += 1
        self.run_thread_id_lock.release()
        return next_id

    def Add(self, run_thread_object):
        """Adds this run_thread_object.  Get() by run_thread_object.id"""
        self.run_thread_objects[str(run_thread_object.id)] = run_thread_object

    def Get(self, run_thread_id):
        """Returns run_threadObject specified, or None if not found."""
        if run_thread_id in self.run_thread_objects:
            return self.run_thread_objects[str(run_thread_id)]
        else:
            return
            return


class RunThread(threading.Thread):

    def __init__(self, run_thread_id, pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
        self.id = run_thread_id
        self.run_block_data = copy.deepcopy(block)
        self.pipe_data = pipe_data
        self.request_state = request_state
        if type(input_data) in (dict,):
            self.input_data = dict(input_data)
        else:
            self.input_data = None
        self.tag = tag
        self.cwd = cwd
        self.env = env
        self.block_parent = block_parent
        self.output = None
        self.pipe_data['run_thread.%s' % self.id] = self
        self.create_time = time.time()
        self.has_started = False
        self.is_running = False
        self.status = None
        self.success = None
        self.run_start = None
        self.run_finish = None
        self.error = None
        self.stages = []
        sharedstate.Set('__internals.threads', run_thread_id, self)
        threading.Thread.__init__(self)
        return

    def __repr__(self):
        scripts = []
        if type(self.run_block_data) == dict:
            if 'script' in self.run_block_data:
                scripts.append(self.run_block_data['script'])
        elif type(self.run_block_data) == list:
            for item in self.run_block_data:
                if 'script' in item:
                    scripts.append(item['script'])

        if self.is_running:
            output = '<span style="color:green;">%s</span>: <b>Is Running:</b> %s  <b>Scripts:</b> %s' % (self.id, self.is_running, scripts)
        else:
            output = '<span style="color:red;">%s</span>: <b>Is Running:</b> %s  <b>Scripts:</b> %s' % (self.id, self.is_running, scripts)
        return output

    def HtmlDescription(self):
        output = '<h2>Thread %s:</h2>\n<br>' % self.id
        output += '<b>Tag:</b> %s<br>\n' % self.tag
        output += '\n<b>Created:</b> %s<br>\n' % unidist.html.PrintTime(self.create_time)
        output += '<b>Has Started:</b> %s<br>\n' % self.has_started
        if self.is_running:
            output += '<font color="green"><b>Is Running:</b> %s</font><br>\n' % self.is_running
        else:
            output += '<font color="red"><b>Is Running:</b> %s</font><br>\n' % self.is_running
        output += '<b>Started:</b> %s<br>\n' % unidist.html.PrintTime(self.run_start)
        output += '<b>Finished:</b> %s<br>\n' % unidist.html.PrintTime(self.run_finish)
        if self.run_finish:
            output += '<b>Duration:</b> %0.1f seconds<br>\n' % (self.run_finish - self.run_start)
        output += '<br><b>Input Data:</b><br>\n<pre><code>%s</code></pre><br>\n' % pprint.pformat(self.input_data)
        output += '<br><b>Run Block:</b><br>\n<pre><code>%s</code></pre><br>\n' % pprint.pformat(self.run_block_data)
        output += '<br><b>Pipe Data:</b><br>\n<pre><code>%s</code></pre><br>\n' % pprint.pformat(self.pipe_data)
        output += '<br><b>Output:</b><br>\n<pre><code>%s</code></pre><br>\n' % pprint.pformat(self.output)
        output += '<br><b>Block Parent:</b><br>\n<pre><code>%s</code></pre><br>\n' % pprint.pformat(self.block_parent)
        return output

    def StageBegin(self, name, message):
        """Logging Stages: Begin a new stage"""
        data = {'type': 'begin', 'time': time.time(), 'name': name, 'message': message}
        self.stages.append(data)

    def StageUpdate(self, name, message):
        """Logging Stages: Begin a new stage"""
        data = {'type': 'update', 'time': time.time(), 'name': name, 'message': message}
        self.stages.append(data)

    def StageEnd(self, name, message, status):
        """Logging Stages: Begin a new stage"""
        data = {'type': 'end', 'time': time.time(), 'name': name, 'message': message, 'status': status}
        self.stages.append(data)

    def StageError(self, name, message):
        """Logging Stages: Begin a new stage"""
        data = {'type': 'error', 'time': time.time(), 'name': name, 'message': message}
        self.stages.append(data)

    def Log(self, name, message):
        """Logging:  Regular old logging."""
        data = {'type': 'log', 'time': time.time(), 'name': name, 'message': message}
        self.stages.append(data)

    def GetOutput(self):
        """For the base class, just return the output, whatever it is."""
        return self.output

    def run(self):
        self.has_started = True
        self.run_start = time.time()
        self.is_running = True
        try:
            self.output = RunScriptBlock(self.pipe_data, self.run_block_data, self.request_state, self.input_data, tag='run', cwd=self.cwd, env=self.env, block_parent=self.block_parent)
        except Exception, e:
            details = error_info.GetExceptionDetails()
            self.error = details
            log(details, logging.ERROR)

        self.is_running = False
        self.run_finish = time.time()

    def Render(self):
        """Render all the interesting information about the state and our Stages."""
        if self.error:
            output = '<h4 style="color: red">ERROR: %s</h4>\n' % self.error
        elif self.run_finish:
            output = '<h4>Completed: Duration %0.1f seconds</h4>\n' % (self.run_finish - self.run_start)
            if 'output' in self.output:
                output += '<br>%s<br><br>' % self.output['output']
        elif self.is_running:
            output = '<h4>Running... %0.1f seconds</h4>\n' % (time.time() - self.run_start)
        else:
            output = '<h4>Not yet running...</h4>\n'
        stages = list(self.stages)
        stages.reverse()
        output += '<table border="1" cellspacing="0">\n'
        for stage in stages:
            output += '<tr>'
            output += '  <td valign="top"><b>%s</b></td>\n' % stage['name']
            output += '  <td valign="top" width="10%%">%0.1fs</td>\n' % (stage['time'] - self.run_start)
            output += '  <td valign="top">%s</td>\n' % stage['type'].upper()
            output += '  <td valign="top">%s</td>\n' % stage['message']
            if 'status' in stage:
                if stage['status']:
                    output += '  <td valign="top" style="color: green">Success</td>\n'
                else:
                    output += '  <td valign="top" style="color: red">Failure</td>\n'
            else:
                output += '  <td valign="top">&nbsp;</td>\n'
            output += '</tr>\n'

        output += '</table>\n'
        self.output = output
        return output


class RunThread_IntervalCache(RunThread):
    """This run thread will run a block at a specified interval until a timer
  has expired or a lock is released.
  """

    def __init__(self, run_thread_id, pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None, interval=None, run_lock='__running', duration=None, history_maximum=None):
        """Creates a RunThread with extra parameters to cache the content, and
    repeat the run every interval-seconds, until either a run_lock is released
    or the duration (if specified) is over.
    """
        RunThread.__init__(self, run_thread_id, pipe_data, block, request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block_parent)
        self.mutex = 'mutex.thread.%s' % self.id
        if interval != None:
            self.interval = interval
        else:
            self.interval = RUN_CACHE_DEFAULT_INTERVAL
        self.run_lock = run_lock
        self.duration = duration
        if history_maximum != None:
            self.history_maximum = history_maximum
        else:
            self.history_maximum = RUN_CACHE_DEFAULT_HISTORY_MAXIMUM
        self.history = []
        self.last_run = None
        self.last_finished = None
        return

    def GetOutput(self):
        """For running in an interval, return the last output, unless it hasnt
    finishing running once then, then stall until it finishes running."""
        while self.last_finished == None:
            time.sleep(0.1)

        return self.output

    def run(self):
        log('Running Thread: Starting: %s' % self.id)
        self.has_started = True
        self.run_start = time.time()
        self.is_running = True
        while self.run_lock and sharedlock.IsLocked(self.run_lock) or self.duration and self.create_time + self.duration < time.time():
            if not sharedlock.IsLocked('__running'):
                break
            try:
                self.last_run = time.time()
                if sharedlock.Acquire(self.mutex):
                    input_data = dict(self.input_data)
                    input_data['__nocache'] = True
                    self.output = ExecuteScript(self.run_block_data['script'], self.pipe_data, self.run_block_data, self.request_state, self.input_data, tag='run', cwd=self.cwd, env=self.env, block_parent=self.block_parent)
                    self.history.append(self.output)
                    if len(self.history) > self.history_maximum:
                        self.history = self.history[-self.history_maximum:]
                    self.last_finished = time.time()
                    if 'timeseries collect' in self.run_block_data:
                        TimeSeriesCollection(self.run_block_data, self.output)
                    sharedlock.Release(self.mutex)
                    time.sleep(self.interval)
            except Exception, e:
                details = error_info.GetExceptionDetails()
                self.error = details
                log(details, logging.ERROR)

        self.is_running = False
        self.run_finish = time.time()
        log('Running Thread: Quitting: %s' % self.id)


def RunScriptBlock(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    if block_parent:
        script_path_prefix = block_parent.get('script_path_prefix', None)
    else:
        script_path_prefix = None
    start_time = time.time()
    for item in block:
        if 'script' in item:
            if 'cache' in item and '__nocache' not in input_data:
                if 'thread_id' not in item:
                    thread_id = sharedcounter.GetIncrement('run_thread')
                    raise Exception('thread_id not found: This will keep creating them forever, fix!')
                else:
                    thread_id = item['thread_id']
                try:
                    run_thread = sharedstate.Get('threads', thread_id)
                except Exception, e:
                    run_thread = None
                else:
                    if run_thread == None:
                        log('Creating interval thread: %s: %s' % (thread_id, item))
                        run_item = item
                        run_thread = RunThread_IntervalCache(thread_id, pipe_data, run_item, request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block_parent, interval=item.get('interval', None), duration=item.get('duration', None), history_maximum=item.get('history', None))
                        sharedstate.Set('threads', thread_id, run_thread)
                        run_thread.start()
                    result = run_thread.GetOutput()
                    if type(result) == dict:
                        pipe_data.update(result)
                        if 'timeseries collect' in item:
                            TimeSeriesCollection(item, result)
                    else:
                        python_script = item['script']
                        log('Python Script Execute did not return dict: %s: %s' % (python_script, result), logging.ERROR)
            else:
                python_script = item['script']
                if script_path_prefix and not python_script.startswith('/'):
                    python_script = '%s/%s' % (script_path_prefix, python_script)
                result = ExecuteScript(python_script, pipe_data, block, request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block_parent)
                if type(result) == dict:
                    pipe_data.update(result)
                    if 'timeseries collect' in item:
                        TimeSeriesCollection(item, result)
                else:
                    log('Python Script Execute did not return dict: %s: %s' % (
                     python_script, result), logging.ERROR)
        elif 'set' in item:
            for (key, value) in item['set'].items():
                pipe_data[key] = value

        elif 'cd' in item:
            dir = item['cd']
            found = False
            for key in pipe_data:
                if '%%(%s)' % key in dir:
                    found = True
                    break

            if found:
                dir = dir % data
            log('Changing working directory: %s' % dir)
            os.chdir(dir)
        elif 'shell' in item:
            cmd = item['shell']
            log('Executing shell command: %s' % cmd)
            (status, output, output_error) = Run(cmd)
            if 'status' not in pipe_data:
                pipe_data['status'] = []
            if 'output' not in pipe_data:
                pipe_data['output'] = ''
            if 'output_error' not in pipe_data:
                pipe_data['output_error'] = ''
            pipe_data['status'].append(status)
            pipe_data['output'] += output
            pipe_data['output_error'] += output_error
        elif 'call' in item:
            log('ERROR: Not yet implemented.  This will call another script, but its name.  invoked=True', logging.CRITICAL)
        elif 'except' in item:
            log('ERROR: Not yet implemented.  This will deal with any exceptions in any of the preceding items.', logging.ERROR)
        else:
            raise Exception('Unknown type of script: %s' % item)

    duration = time.time() - start_time
    if 'duration' not in pipe_data:
        pipe_data['__duration'] = duration
    pipe_data['__start_time'] = start_time
    return pipe_data