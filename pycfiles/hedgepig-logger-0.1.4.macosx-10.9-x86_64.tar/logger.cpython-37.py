# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/hedgepig_logger/logger.py
# Compiled at: 2019-12-31 15:14:18
# Size of source mod 2**32: 11188 bytes
import os, sys, time, codecs
from datetime import datetime
from collections import OrderedDict

class log:
    logfile_path = None
    logfile = sys.stdout
    stdout_also = True
    stopped = False
    tracker = None
    timer = None
    autoflush = True
    indent_level = 0

    @staticmethod
    def start(logfile=None, message=None, args=None, stdout_also=True):
        if logfile:
            if type(logfile) == type('a'):
                log.logfile_path = logfile
                log.logfile = open(logfile, 'w')
        if message:
            if type(message) == type(lambda x: x):
                if args:
                    message(args)
            else:
                message()
        elif message:
            if type(message) == type('str'):
                log.writeln(message)
        log.stdout_also = stdout_also
        log.indent_level = 0

    @staticmethod
    def stop(message=None, suppress=False):
        if message:
            log.writeln(message)
        if log.logfile != sys.stdout:
            if not suppress:
                if log.logfile_path:
                    log.writeln('\nLog output saved to %s' % log.logfile_path)
            log.logfile.close()
        log.stopped = True

    @staticmethod
    def getstream():
        return log.logfile

    @staticmethod
    def indent(by=2):
        log.indent_level += by

    @staticmethod
    def unindent(by=2):
        log.indent_level = max(0, log.indent_level - by)

    @staticmethod
    def write--- This code section failed: ---

 L.  63         0  LOAD_GLOBAL              log
                2  LOAD_ATTR                stopped
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L.  64         6  LOAD_GLOBAL              Exception
                8  LOAD_STR                 'Log has stopped!'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L.  65        14  LOAD_GLOBAL              log
               16  LOAD_ATTR                stdout_also
               18  POP_JUMP_IF_FALSE    60  'to 60'
               20  LOAD_GLOBAL              log
               22  LOAD_METHOD              getstream
               24  CALL_METHOD_0         0  '0 positional arguments'
               26  LOAD_GLOBAL              sys
               28  LOAD_ATTR                stdout
               30  COMPARE_OP               !=
               32  POP_JUMP_IF_FALSE    60  'to 60'
               34  LOAD_FAST                'quiet'
               36  POP_JUMP_IF_TRUE     60  'to 60'

 L.  66        38  LOAD_GLOBAL              sys
               40  LOAD_ATTR                stdout
               42  LOAD_METHOD              write
               44  LOAD_GLOBAL              log
               46  LOAD_ATTR                indent_level
               48  LOAD_STR                 ' '
               50  BINARY_MULTIPLY  
               52  LOAD_FAST                'message'
               54  BINARY_ADD       
               56  CALL_METHOD_1         1  '1 positional argument'
               58  POP_TOP          
             60_0  COME_FROM            36  '36'
             60_1  COME_FROM            32  '32'
             60_2  COME_FROM            18  '18'

 L.  68        60  LOAD_FAST                'stdoutOnly'
               62  POP_JUMP_IF_FALSE    78  'to 78'
               64  LOAD_GLOBAL              log
               66  LOAD_METHOD              getstream
               68  CALL_METHOD_0         0  '0 positional arguments'
               70  LOAD_GLOBAL              sys
               72  LOAD_ATTR                stdout
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_TRUE    122  'to 122'
             78_0  COME_FROM            62  '62'

 L.  69        78  LOAD_GLOBAL              log
               80  LOAD_ATTR                stdout_also
               82  POP_JUMP_IF_FALSE   102  'to 102'
               84  LOAD_GLOBAL              log
               86  LOAD_METHOD              getstream
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  LOAD_GLOBAL              sys
               92  LOAD_ATTR                stdout
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   102  'to 102'
               98  LOAD_FAST                'quiet'
              100  POP_JUMP_IF_TRUE    122  'to 122'
            102_0  COME_FROM            96  '96'
            102_1  COME_FROM            82  '82'

 L.  70       102  LOAD_GLOBAL              log
              104  LOAD_ATTR                stdout_also
              106  POP_JUMP_IF_TRUE    126  'to 126'
              108  LOAD_GLOBAL              log
              110  LOAD_METHOD              getstream
              112  CALL_METHOD_0         0  '0 positional arguments'
              114  LOAD_GLOBAL              sys
              116  LOAD_ATTR                stdout
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   126  'to 126'
            122_0  COME_FROM           100  '100'
            122_1  COME_FROM            76  '76'

 L.  72       122  LOAD_CONST               None
              124  RETURN_VALUE     
            126_0  COME_FROM           120  '120'
            126_1  COME_FROM           106  '106'

 L.  74       126  LOAD_GLOBAL              log
              128  LOAD_METHOD              getstream
              130  CALL_METHOD_0         0  '0 positional arguments'
              132  LOAD_METHOD              write
              134  LOAD_GLOBAL              log
              136  LOAD_ATTR                indent_level
              138  LOAD_STR                 ' '
              140  BINARY_MULTIPLY  
              142  LOAD_FAST                'message'
              144  BINARY_ADD       
              146  CALL_METHOD_1         1  '1 positional argument'
              148  POP_TOP          

 L.  75       150  LOAD_GLOBAL              log
              152  LOAD_ATTR                autoflush
              154  POP_JUMP_IF_FALSE   168  'to 168'

 L.  75       156  LOAD_GLOBAL              log
              158  LOAD_METHOD              getstream
              160  CALL_METHOD_0         0  '0 positional arguments'
              162  LOAD_METHOD              flush
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  POP_TOP          
            168_0  COME_FROM           154  '154'

Parse error at or near `COME_FROM' instruction at offset 126_1

    @staticmethod
    def writeln(message='', stdoutOnly=False, quiet=False):
        log.write(message, stdoutOnly=stdoutOnly, quiet=quiet)
        log.write('\n', stdoutOnly=stdoutOnly, quiet=quiet)

    @staticmethod
    def progress(current, total, numDots=0, stdoutOnly=False):
        line = str.format('\r{0}{1}%', numDots * '.', int(float(current) / total * 100))
        log.write(line, stdoutOnly=stdoutOnly)

    @staticmethod
    def yesno(bln):
        if bln:
            return 'Yes'
        return 'No'

    @staticmethod
    def redirect_stderr():
        """Redirect output from STDERR to the log
        """
        sys.stderr = log.getstream()

    @staticmethod
    def track(message='{0:,}', total=None, writeInterval=1, stdoutOnly=False):
        if type(message) == type('str'):
            msgFormat = message
            if total:
                message = lambda current, total, args: (str.format)(msgFormat, int(float(current) / total * 100), *args)
            else:
                message = lambda current, args: (str.format)(msgFormat, current, *args)
        elif total:
            onIncrement = lambda current, total, args: log.write((str.format('\r{0}{1}', log.indent_level * ' ', message(current, total, args))),
              stdoutOnly=True)
            onFlush = lambda current, total, args: log.write((str.format('\r{0}{1}', log.indent_level * ' ', message(current, total, args))),
              stdoutOnly=stdoutOnly)
        else:
            onIncrement = lambda current, args: log.write((str.format('\r{0}{1}', log.indent_level * ' ', message(current, args))),
              stdoutOnly=True)
            onFlush = lambda current, args: log.write((str.format('\r{0}{1}', log.indent_level * ' ', message(current, args))),
              stdoutOnly=stdoutOnly)
        log.tracker = ProgressTracker(total, onIncrement=onIncrement, onFlush=onFlush, writeInterval=writeInterval)

    @staticmethod
    def tick(*args):
        if log.tracker != None:
            if not log.tracker.total or log.tracker.current < log.tracker.total:
                (log.tracker.increment)(*args)
            else:
                raise Exception('Tracker is complete!')

    @staticmethod
    def flushTracker(*args, **kwargs):
        message = kwargs.get('message', '')
        newline = kwargs.get('newline', True)
        if log.tracker != None:
            (log.tracker.flush)(*args)
            if newline:
                log.writeln('\n%s' % message)
            else:
                log.writeln(message)

    @staticmethod
    def reset():
        if log.tracker != None:
            log.tracker.reset()

    @staticmethod
    def startTimer(message=None, newline=True):
        if message:
            if newline:
                log.writeln(message)
            else:
                log.write(message)
        log.timer = Timer()
        log.timer.start()
        return log.timer

    @staticmethod
    def stopTimer(timer=None, message='>>Completed in {0} sec.\n'):
        if timer or log.timer:
            if not timer:
                timer = log.timer
            timer.stop()
            elpsed = timer.elapsed()
            log.writeln(str.format(message, elpsed))
        else:
            raise Exception('No timer to stop!')

    @staticmethod
    def writeConfig(settings, title=None, start_time=None, end_time=None):
        """Write an experimental configuration to the log.

        Always writes the current date and time at the head of the file.

        The optional title argument is a string to write at the head of the file,
            before date and time.

        Settings should be passed in as a list, in the desired order for writing.
        To write the value of a single setting, pass it as (name, value) pair.
        To group several settings under a section, pass a (name, dict) pair, where
            the first element is the name of the section, and the second is a
            dict (or OrderedDict) of { setting: value } format.

        For example, the following call:
            log.writeConfig([
                ('Value 1', 3),
                ('Some other setting', True),
                ('Section 1', OrderedDict([
                    ('sub-value A', 12.4),
                    ('sub-value B', 'string')
                ]))
            ], title='My experimental configuration')
        will produce the following configuration log:
            
            My experimental configuration
            Run time: 1970-01-01 00:00:00

            Value 1: 3
            Some other setting: True

            ## Section 1 ##
            sub-value A: 12.4
            sub-value B: string

        Arguments:

            settings   :: (described above)
            title      :: optional string to write at start of config file
            start_time :: a datetime.datetime object indicating when the program started
                          execution; if not provided, defaults to datetime.now()
            end_time   :: a datetime.datetime object indicating when the program ended
                          execution; if provided, also writes elapsed execution time
                          between start_time and end_time
        """
        group_set = set([dict, OrderedDict, list, tuple])
        dict_set = set([dict, OrderedDict])
        if title:
            log.write('%s\n' % title)
        else:
            time_fmt = '%Y-%m-%d %H:%M:%S'
            if start_time is None:
                start_time = datetime.now()
                header = 'Run'
            else:
                header = 'Start'
        log.write('%s time: %s\n' % (header, start_time.strftime(time_fmt)))
        if end_time:
            log.write('End time: %s\n' % end_time.strftime(time_fmt))
            log.write('Execution time: %f seconds\n' % (end_time - start_time).total_seconds())
        try:
            script_path = os.path.abspath(sys.argv[0])
            log.write('Generating script: %s\n' % script_path)
        except:
            pass

        log.write('\n')
        for key, value in settings:
            if type(value) in group_set:
                log.write('\n## %s ##\n' % key)
                if type(value) in dict_set:
                    iterator = value.items()
                else:
                    iterator = iter(value)
                for sub_key, sub_value in iterator:
                    log.write('%s: %s\n' % (sub_key, str(sub_value)))

                log.write('\n')
            else:
                log.write('%s: %s\n' % (key, str(value)))

        log.write('\n')


class ProgressTracker:

    def __init__(self, total=None, onIncrement=None, onFlush=None, writeInterval=1):
        self.total = total
        self.current = 0
        self.sinceLastWrite = 0
        self.onIncrement = onIncrement
        self.onFlush = onFlush
        self.writeInterval = writeInterval

    def increment(self, *args):
        self.current += 1
        self.sinceLastWrite += 1
        if self.sinceLastWrite >= self.writeInterval:
            self.sinceLastWrite = 0
            (self.showProgress)(*args)

    def reset(self):
        self.current = 0
        self.sinceLastWrite = 0

    def showProgress(self, *args):
        if self.onIncrement:
            if self.total:
                self.onIncrement(self.current, self.total, args)
            else:
                self.onIncrement(self.current, args)

    def flush(self, *args):
        if self.onFlush:
            if self.total:
                self.onFlush(self.current, self.total, args)
            else:
                self.onFlush(self.current, args)


class Timer:

    def __init__(self):
        self.startTime = 0
        self.stopTime = 0
        self.started = False

    def start(self):
        if not self.started:
            self.startTime = time.time()
            self.started = True
        else:
            raise Exception('Timer already started!')

    def stop(self):
        if self.started:
            self.stopTime = time.time()
            self.started = False
        else:
            raise Exception('Timer already stopped!')

    def elapsed(self):
        if not self.started:
            return self.stopTime - self.startTime
        return time.time() - self.startTime