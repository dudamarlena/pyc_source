# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\dispatchers.py
# Compiled at: 2015-07-18 10:13:56
import warnings, errno
from supervisor.medusa.asyncore_25 import compact_traceback
from supervisor.events import notify
from supervisor.events import EventRejectedEvent
from supervisor.events import ProcessLogStderrEvent
from supervisor.events import ProcessLogStdoutEvent
from supervisor.states import EventListenerStates
from supervisor.states import getEventListenerStateDescription
from supervisor import loggers

def find_prefix_at_end(haystack, needle):
    l = len(needle) - 1
    while l and not haystack.endswith(needle[:l]):
        l -= 1

    return l


class PDispatcher:
    """ Asyncore dispatcher for mainloop, representing a process channel
    (stdin, stdout, or stderr).  This class is abstract. """
    closed = False

    def __init__(self, process, channel, fd):
        self.process = process
        self.channel = channel
        self.fd = fd
        self.closed = False

    def __repr__(self):
        return '<%s at %s for %s (%s)>' % (self.__class__.__name__,
         id(self),
         self.process,
         self.channel)

    def readable(self):
        raise NotImplementedError

    def writable(self):
        raise NotImplementedError

    def handle_read_event(self):
        raise NotImplementedError

    def handle_write_event(self):
        raise NotImplementedError

    def handle_error(self):
        nil, t, v, tbinfo = compact_traceback()
        self.process.config.options.logger.critical('uncaptured python exception, closing channel %s (%s:%s %s)' % (
         repr(self),
         t,
         v,
         tbinfo))
        self.close()

    def close(self):
        if not self.closed:
            self.process.config.options.logger.debug('fd %s closed, stopped monitoring %s' % (self.fd, self))
            self.closed = True

    def flush(self):
        pass


class POutputDispatcher(PDispatcher):
    """
    A Process Output (stdout/stderr) dispatcher. Serves several purposes:

    - capture output sent within <!--XSUPERVISOR:BEGIN--> and
      <!--XSUPERVISOR:END--> tags and signal a ProcessCommunicationEvent
      by calling notify(event).
    - route the output to the appropriate log handlers as specified in the
      config.
    """
    capturemode = False
    mainlog = None
    capturelog = None
    childlog = None
    output_buffer = ''

    def __init__(self, process, event_type, fd):
        """
        Initialize the dispatcher.

        `event_type` should be one of ProcessLogStdoutEvent or
        ProcessLogStderrEvent
        """
        self.process = process
        self.event_type = event_type
        self.fd = fd
        self.channel = channel = self.event_type.channel
        self._setup_logging(process.config, channel)
        capture_maxbytes = getattr(process.config, '%s_capture_maxbytes' % channel)
        if capture_maxbytes:
            self.capturelog = loggers.handle_boundIO(self.process.config.options.getLogger(), fmt='%(message)s', maxbytes=capture_maxbytes)
        self.childlog = self.mainlog
        begintoken = self.event_type.BEGIN_TOKEN
        endtoken = self.event_type.END_TOKEN
        self.begintoken_data = (begintoken, len(begintoken))
        self.endtoken_data = (endtoken, len(endtoken))
        self.mainlog_level = loggers.LevelsByName.DEBG
        config = self.process.config
        self.log_to_mainlog = config.options.loglevel <= self.mainlog_level
        self.stdout_events_enabled = config.stdout_events_enabled
        self.stderr_events_enabled = config.stderr_events_enabled

    def _setup_logging(self, config, channel):
        """
        Configure the main log according to the process' configuration and
        channel. Sets `mainlog` on self. Returns nothing.
        """
        logfile = getattr(config, '%s_logfile' % channel)
        if not logfile:
            return
        maxbytes = getattr(config, '%s_logfile_maxbytes' % channel)
        backups = getattr(config, '%s_logfile_backups' % channel)
        fmt = '%(message)s'
        if logfile == 'syslog':
            warnings.warn("Specifying 'syslog' for filename is deprecated. Use %s_syslog instead." % channel, DeprecationWarning)
            fmt = (' ').join((config.name, fmt))
        self.mainlog = loggers.handle_file(config.options.getLogger(), filename=logfile, fmt=fmt, rotating=not not maxbytes, maxbytes=maxbytes, backups=backups)
        if getattr(config, '%s_syslog' % channel, False):
            fmt = config.name + ' %(message)s'
            loggers.handle_syslog(self.mainlog, fmt)

    def removelogs(self):
        for log in (self.mainlog, self.capturelog):
            if log is not None:
                for handler in log.handlers:
                    handler.remove()
                    handler.reopen()

        return

    def reopenlogs(self):
        for log in (self.mainlog, self.capturelog):
            if log is not None:
                for handler in log.handlers:
                    handler.reopen()

        return

    def _log(self, data):
        if data:
            config = self.process.config
            if config.options.strip_ansi:
                data = stripEscapes(data)
            if self.childlog:
                self.childlog.info(data)
            if self.log_to_mainlog:
                msg = '%(name)r %(channel)s output:\n%(data)s'
                config.options.logger.log(self.mainlog_level, msg, name=config.name, channel=self.channel, data=data)
            if self.channel == 'stdout':
                if self.stdout_events_enabled:
                    notify(ProcessLogStdoutEvent(self.process, self.process.pid, data))
            elif self.stderr_events_enabled:
                notify(ProcessLogStderrEvent(self.process, self.process.pid, data))

    def record_output(self):
        if self.capturelog is None:
            data = self.output_buffer
            self.output_buffer = ''
            self._log(data)
            return
        else:
            if self.capturemode:
                token, tokenlen = self.endtoken_data
            else:
                token, tokenlen = self.begintoken_data
            if len(self.output_buffer) <= tokenlen:
                return
            data = self.output_buffer
            self.output_buffer = ''
            try:
                before, after = data.split(token, 1)
            except ValueError:
                after = None
                index = find_prefix_at_end(data, token)
                if index:
                    self.output_buffer = self.output_buffer + data[-index:]
                    data = data[:-index]
                self._log(data)
            else:
                self._log(before)
                self.toggle_capturemode()
                self.output_buffer = after

            if after:
                self.record_output()
            return

    def toggle_capturemode(self):
        self.capturemode = not self.capturemode
        if self.capturelog is not None:
            if self.capturemode:
                self.childlog = self.capturelog
            else:
                for handler in self.capturelog.handlers:
                    handler.flush()

                data = self.capturelog.getvalue()
                channel = self.channel
                procname = self.process.config.name
                event = self.event_type(self.process, self.process.pid, data)
                notify(event)
                msg = '%(procname)r %(channel)s emitted a comm event'
                self.process.config.options.logger.debug(msg, procname=procname, channel=channel)
                for handler in self.capturelog.handlers:
                    handler.remove()
                    handler.reopen()

                self.childlog = self.mainlog
        return

    def writable(self):
        return False

    def readable(self):
        if self.closed:
            return False
        return True

    def handle_read_event(self):
        data = self.process.config.options.readfd(self.fd)
        self.output_buffer += data
        self.record_output()
        if not data:
            self.close()


class PEventListenerDispatcher(PDispatcher):
    """ An output dispatcher that monitors and changes a process'
    listener_state """
    childlog = None
    state_buffer = ''
    READY_FOR_EVENTS_TOKEN = 'READY\n'
    RESULT_TOKEN_START = 'RESULT '
    READY_FOR_EVENTS_LEN = len(READY_FOR_EVENTS_TOKEN)
    RESULT_TOKEN_START_LEN = len(RESULT_TOKEN_START)

    def __init__(self, process, channel, fd):
        PDispatcher.__init__(self, process, channel, fd)
        self.process.listener_state = EventListenerStates.ACKNOWLEDGED
        self.process.event = None
        self.result = ''
        self.resultlen = None
        logfile = getattr(process.config, '%s_logfile' % channel)
        if logfile:
            maxbytes = getattr(process.config, '%s_logfile_maxbytes' % channel)
            backups = getattr(process.config, '%s_logfile_backups' % channel)
            self.childlog = loggers.handle_file(process.config.options.getLogger(), logfile, '%(message)s', rotating=not not maxbytes, maxbytes=maxbytes, backups=backups)
        return

    def removelogs(self):
        if self.childlog is not None:
            for handler in self.childlog.handlers:
                handler.remove()
                handler.reopen()

        return

    def reopenlogs(self):
        if self.childlog is not None:
            for handler in self.childlog.handlers:
                handler.reopen()

        return

    def writable(self):
        return False

    def readable(self):
        if self.closed:
            return False
        return True

    def handle_read_event(self):
        data = self.process.config.options.readfd(self.fd)
        if data:
            self.state_buffer += data
            procname = self.process.config.name
            msg = '%r %s output:\n%s' % (procname, self.channel, data)
            self.process.config.options.logger.debug(msg)
            if self.childlog:
                if self.process.config.options.strip_ansi:
                    data = stripEscapes(data)
                self.childlog.info(data)
        else:
            self.close()
        self.handle_listener_state_change()

    def handle_listener_state_change(self):
        data = self.state_buffer
        if not data:
            return
        else:
            process = self.process
            procname = process.config.name
            state = process.listener_state
            if state == EventListenerStates.UNKNOWN:
                self.state_buffer = ''
                return
            if state == EventListenerStates.ACKNOWLEDGED:
                if len(data) < self.READY_FOR_EVENTS_LEN:
                    return
                if data.startswith(self.READY_FOR_EVENTS_TOKEN):
                    self._change_listener_state(EventListenerStates.READY)
                    tokenlen = self.READY_FOR_EVENTS_LEN
                    self.state_buffer = self.state_buffer[tokenlen:]
                    process.event = None
                else:
                    self._change_listener_state(EventListenerStates.UNKNOWN)
                    self.state_buffer = ''
                    process.event = None
                if self.state_buffer:
                    self.handle_listener_state_change()
                else:
                    return
            elif state == EventListenerStates.READY:
                self._change_listener_state(EventListenerStates.UNKNOWN)
                self.state_buffer = ''
                process.event = None
                return
            if state == EventListenerStates.BUSY:
                if self.resultlen is None:
                    pos = data.find('\n')
                    if pos == -1:
                        return
                    result_line = self.state_buffer[:pos]
                    self.state_buffer = self.state_buffer[pos + 1:]
                    resultlen = result_line[self.RESULT_TOKEN_START_LEN:]
                    try:
                        self.resultlen = int(resultlen)
                    except ValueError:
                        process.config.options.logger.warn('%s: bad result line: %r' % (procname, result_line))
                        self._change_listener_state(EventListenerStates.UNKNOWN)
                        self.state_buffer = ''
                        notify(EventRejectedEvent(process, process.event))
                        process.event = None
                        return

                else:
                    needed = self.resultlen - len(self.result)
                    if needed:
                        self.result += self.state_buffer[:needed]
                        self.state_buffer = self.state_buffer[needed:]
                        needed = self.resultlen - len(self.result)
                    if not needed:
                        self.handle_result(self.result)
                        self.process.event = None
                        self.result = ''
                        self.resultlen = None
                if self.state_buffer:
                    self.handle_listener_state_change()
            return

    def handle_result(self, result):
        process = self.process
        procname = process.config.name
        logger = process.config.options.logger
        try:
            self.process.group.config.result_handler(process.event, result)
            logger.debug('%s: event was processed' % procname)
            self._change_listener_state(EventListenerStates.ACKNOWLEDGED)
        except RejectEvent:
            logger.warn('%s: event was rejected' % procname)
            self._change_listener_state(EventListenerStates.ACKNOWLEDGED)
            notify(EventRejectedEvent(process, process.event))
        except:
            logger.warn('%s: event caused an error' % procname)
            self._change_listener_state(EventListenerStates.UNKNOWN)
            notify(EventRejectedEvent(process, process.event))

    def _change_listener_state(self, new_state):
        process = self.process
        procname = process.config.name
        old_state = process.listener_state
        msg = '%s: %s -> %s' % (
         procname,
         getEventListenerStateDescription(old_state),
         getEventListenerStateDescription(new_state))
        process.config.options.logger.debug(msg)
        process.listener_state = new_state
        if new_state == EventListenerStates.UNKNOWN:
            msg = '%s: has entered the UNKNOWN state and will no longer receive events, this usually indicates the process violated the eventlistener protocol' % procname
            process.config.options.logger.warn(msg)


class PInputDispatcher(PDispatcher):
    """ Input (stdin) dispatcher """

    def __init__(self, process, channel, fd):
        PDispatcher.__init__(self, process, channel, fd)
        self.input_buffer = ''

    def writable(self):
        if self.input_buffer and not self.closed:
            return True
        return False

    def readable(self):
        return False

    def flush(self):
        sent = self.process.config.options.write(self.fd, self.input_buffer)
        self.input_buffer = self.input_buffer[sent:]

    def handle_write_event(self):
        if self.input_buffer:
            try:
                self.flush()
            except OSError as why:
                if why.args[0] == errno.EPIPE:
                    self.input_buffer = ''
                    self.close()
                else:
                    raise


ANSI_ESCAPE_BEGIN = '\x1b['
ANSI_TERMINATORS = ('H', 'f', 'A', 'B', 'C', 'D', 'R', 's', 'u', 'J', 'K', 'h', 'l',
                    'p', 'm')

def stripEscapes(s):
    """
    Remove all ANSI color escapes from the given string.
    """
    result = ''
    show = 1
    i = 0
    L = len(s)
    while i < L:
        if show == 0 and s[i] in ANSI_TERMINATORS:
            show = 1
        elif show:
            n = s.find(ANSI_ESCAPE_BEGIN, i)
            if n == -1:
                return result + s[i:]
            result = result + s[i:n]
            i = n
            show = 0
        i += 1

    return result


class RejectEvent(Exception):
    """ The exception type expected by a dispatcher when a handler wants
    to reject an event """
    pass


def default_handler(event, response):
    if response != 'OK':
        raise RejectEvent(response)