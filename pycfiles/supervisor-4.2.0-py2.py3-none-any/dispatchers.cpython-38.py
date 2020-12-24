# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/dispatchers.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 19087 bytes
import warnings, errno
from supervisor.medusa.asyncore_25 import compact_traceback
from supervisor.compat import as_string
from supervisor.events import notify
from supervisor.events import EventRejectedEvent
from supervisor.events import ProcessLogStderrEvent
from supervisor.events import ProcessLogStdoutEvent
from supervisor.states import EventListenerStates
from supervisor.states import getEventListenerStateDescription
from supervisor import loggers

def find_prefix_at_end(haystack, needle):
    l = len(needle) - 1
    while l:
        if not haystack.endswith(needle[:l]):
            l -= 1

    return l


class PDispatcher:
    __doc__ = ' Asyncore dispatcher for mainloop, representing a process channel\n    (stdin, stdout, or stderr).  This class is abstract. '
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
    __doc__ = '\n    A Process Output (stdout/stderr) dispatcher. Serves several purposes:\n\n    - capture output sent within <!--XSUPERVISOR:BEGIN--> and\n      <!--XSUPERVISOR:END--> tags and signal a ProcessCommunicationEvent\n      by calling notify(event).\n    - route the output to the appropriate log handlers as specified in the\n      config.\n    '
    capturemode = False
    mainlog = None
    capturelog = None
    childlog = None
    output_buffer = b''

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
            self.capturelog = loggers.handle_boundIO((self.process.config.options.getLogger()),
              fmt='%(message)s',
              maxbytes=capture_maxbytes)
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
            fmt = ' '.join((config.name, fmt))
        self.mainlog = loggers.handle_file((config.options.getLogger()),
          filename=logfile,
          fmt=fmt,
          rotating=(not not maxbytes),
          maxbytes=maxbytes,
          backups=backups)
        if getattr(config, '%s_syslog' % channel, False):
            fmt = config.name + ' %(message)s'
            loggers.handle_syslog(self.mainlog, fmt)

    def removelogs(self):
        for log in (self.mainlog, self.capturelog):
            if log is not None:
                for handler in log.handlers:
                    handler.remove()
                    handler.reopen()

    def reopenlogs(self):
        for log in (
         self.mainlog, self.capturelog):
            if log is not None:
                for handler in log.handlers:
                    handler.reopen()

    def _log(self, data):
        if data:
            config = self.process.config
            if config.options.strip_ansi:
                data = stripEscapes(data)
            if self.childlog:
                self.childlog.info(data)
            elif self.log_to_mainlog:
                text = isinstance(data, bytes) or data
            else:
                try:
                    text = data.decode('utf-8')
                except UnicodeDecodeError:
                    text = 'Undecodable: %r' % data
                else:
                    msg = '%(name)r %(channel)s output:\n%(data)s'
                    config.options.logger.log((self.mainlog_level),
                      msg, name=(config.name), channel=(self.channel),
                      data=text)
                if self.channel == 'stdout':
                    if self.stdout_events_enabled:
                        notify(ProcessLogStdoutEvent(self.process, self.process.pid, data))
                elif self.stderr_events_enabled:
                    notify(ProcessLogStderrEvent(self.process, self.process.pid, data))

    def record_output(self):
        if self.capturelog is None:
            data = self.output_buffer
            self.output_buffer = b''
            self._log(data)
            return
            if self.capturemode:
                token, tokenlen = self.endtoken_data
            else:
                token, tokenlen = self.begintoken_data
            if len(self.output_buffer) <= tokenlen:
                return
        else:
            data = self.output_buffer
            self.output_buffer = b''
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

    def toggle_capturemode(self):
        self.capturemode = not self.capturemode
        if self.capturelog is not None:
            if self.capturemode:
                self.childlog = self.capturelog
            else:
                for handler in self.capturelog.handlers:
                    handler.flush()
                else:
                    data = self.capturelog.getvalue()
                    channel = self.channel
                    procname = self.process.config.name
                    event = self.event_type(self.process, self.process.pid, data)
                    notify(event)
                    msg = '%(procname)r %(channel)s emitted a comm event'
                    self.process.config.options.logger.debug(msg, procname=procname,
                      channel=channel)
                    for handler in self.capturelog.handlers:
                        handler.remove()
                        handler.reopen()
                    else:
                        self.childlog = self.mainlog

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
    __doc__ = " An output dispatcher that monitors and changes a process'\n    listener_state "
    childlog = None
    state_buffer = b''
    READY_FOR_EVENTS_TOKEN = b'READY\n'
    RESULT_TOKEN_START = b'RESULT '
    READY_FOR_EVENTS_LEN = len(READY_FOR_EVENTS_TOKEN)
    RESULT_TOKEN_START_LEN = len(RESULT_TOKEN_START)

    def __init__(self, process, channel, fd):
        PDispatcher.__init__(self, process, channel, fd)
        self.process.listener_state = EventListenerStates.ACKNOWLEDGED
        self.process.event = None
        self.result = b''
        self.resultlen = None
        logfile = getattr(process.config, '%s_logfile' % channel)
        if logfile:
            maxbytes = getattr(process.config, '%s_logfile_maxbytes' % channel)
            backups = getattr(process.config, '%s_logfile_backups' % channel)
            self.childlog = loggers.handle_file((process.config.options.getLogger()),
              logfile,
              '%(message)s',
              rotating=(not not maxbytes),
              maxbytes=maxbytes,
              backups=backups)

    def removelogs(self):
        if self.childlog is not None:
            for handler in self.childlog.handlers:
                handler.remove()
                handler.reopen()

    def reopenlogs(self):
        if self.childlog is not None:
            for handler in self.childlog.handlers:
                handler.reopen()

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

    def handle_listener_state_change--- This code section failed: ---

 L. 352         0  LOAD_FAST                'self'
                2  LOAD_ATTR                state_buffer
                4  STORE_FAST               'data'

 L. 354         6  LOAD_FAST                'data'
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 355        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 357        14  LOAD_FAST                'self'
               16  LOAD_ATTR                process
               18  STORE_FAST               'process'

 L. 358        20  LOAD_FAST                'process'
               22  LOAD_ATTR                config
               24  LOAD_ATTR                name
               26  STORE_FAST               'procname'

 L. 359        28  LOAD_FAST                'process'
               30  LOAD_ATTR                listener_state
               32  STORE_FAST               'state'

 L. 361        34  LOAD_FAST                'state'
               36  LOAD_GLOBAL              EventListenerStates
               38  LOAD_ATTR                UNKNOWN
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L. 363        44  LOAD_CONST               b''
               46  LOAD_FAST                'self'
               48  STORE_ATTR               state_buffer

 L. 364        50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            42  '42'

 L. 366        54  LOAD_FAST                'state'
               56  LOAD_GLOBAL              EventListenerStates
               58  LOAD_ATTR                ACKNOWLEDGED
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE   184  'to 184'

 L. 367        64  LOAD_GLOBAL              len
               66  LOAD_FAST                'data'
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                READY_FOR_EVENTS_LEN
               74  COMPARE_OP               <
               76  POP_JUMP_IF_FALSE    82  'to 82'

 L. 369        78  LOAD_CONST               None
               80  RETURN_VALUE     
             82_0  COME_FROM            76  '76'

 L. 370        82  LOAD_FAST                'data'
               84  LOAD_METHOD              startswith
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                READY_FOR_EVENTS_TOKEN
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE   136  'to 136'

 L. 371        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _change_listener_state
               98  LOAD_GLOBAL              EventListenerStates
              100  LOAD_ATTR                READY
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 372       106  LOAD_FAST                'self'
              108  LOAD_ATTR                READY_FOR_EVENTS_LEN
              110  STORE_FAST               'tokenlen'

 L. 373       112  LOAD_FAST                'self'
              114  LOAD_ATTR                state_buffer
              116  LOAD_FAST                'tokenlen'
              118  LOAD_CONST               None
              120  BUILD_SLICE_2         2 
              122  BINARY_SUBSCR    
              124  LOAD_FAST                'self'
              126  STORE_ATTR               state_buffer

 L. 374       128  LOAD_CONST               None
              130  LOAD_FAST                'process'
              132  STORE_ATTR               event
              134  JUMP_FORWARD        160  'to 160'
            136_0  COME_FROM            92  '92'

 L. 376       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _change_listener_state
              140  LOAD_GLOBAL              EventListenerStates
              142  LOAD_ATTR                UNKNOWN
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

 L. 377       148  LOAD_CONST               b''
              150  LOAD_FAST                'self'
              152  STORE_ATTR               state_buffer

 L. 378       154  LOAD_CONST               None
              156  LOAD_FAST                'process'
              158  STORE_ATTR               event
            160_0  COME_FROM           134  '134'

 L. 379       160  LOAD_FAST                'self'
              162  LOAD_ATTR                state_buffer
              164  POP_JUMP_IF_FALSE   176  'to 176'

 L. 381       166  LOAD_FAST                'self'
              168  LOAD_METHOD              handle_listener_state_change
              170  CALL_METHOD_0         0  ''
              172  POP_TOP          
              174  JUMP_FORWARD        600  'to 600'
            176_0  COME_FROM           164  '164'

 L. 383       176  LOAD_CONST               None
              178  RETURN_VALUE     
          180_182  JUMP_FORWARD        600  'to 600'
            184_0  COME_FROM            62  '62'

 L. 385       184  LOAD_FAST                'state'
              186  LOAD_GLOBAL              EventListenerStates
              188  LOAD_ATTR                READY
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   222  'to 222'

 L. 387       194  LOAD_FAST                'self'
              196  LOAD_METHOD              _change_listener_state
              198  LOAD_GLOBAL              EventListenerStates
              200  LOAD_ATTR                UNKNOWN
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 388       206  LOAD_CONST               b''
              208  LOAD_FAST                'self'
              210  STORE_ATTR               state_buffer

 L. 389       212  LOAD_CONST               None
              214  LOAD_FAST                'process'
              216  STORE_ATTR               event

 L. 390       218  LOAD_CONST               None
              220  RETURN_VALUE     
            222_0  COME_FROM           192  '192'

 L. 392       222  LOAD_FAST                'state'
              224  LOAD_GLOBAL              EventListenerStates
              226  LOAD_ATTR                BUSY
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_FALSE   600  'to 600'

 L. 393       234  LOAD_FAST                'self'
              236  LOAD_ATTR                resultlen
              238  LOAD_CONST               None
              240  COMPARE_OP               is
          242_244  POP_JUMP_IF_FALSE   468  'to 468'

 L. 395       246  LOAD_FAST                'data'
              248  LOAD_METHOD              find
              250  LOAD_CONST               b'\n'
              252  CALL_METHOD_1         1  ''
              254  STORE_FAST               'pos'

 L. 396       256  LOAD_FAST                'pos'
              258  LOAD_CONST               -1
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   270  'to 270'

 L. 399       266  LOAD_CONST               None
              268  RETURN_VALUE     
            270_0  COME_FROM           262  '262'

 L. 401       270  LOAD_FAST                'self'
              272  LOAD_ATTR                state_buffer
              274  LOAD_CONST               None
              276  LOAD_FAST                'pos'
              278  BUILD_SLICE_2         2 
              280  BINARY_SUBSCR    
              282  STORE_FAST               'result_line'

 L. 402       284  LOAD_FAST                'self'
              286  LOAD_ATTR                state_buffer
              288  LOAD_FAST                'pos'
              290  LOAD_CONST               1
              292  BINARY_ADD       
              294  LOAD_CONST               None
              296  BUILD_SLICE_2         2 
              298  BINARY_SUBSCR    
              300  LOAD_FAST                'self'
              302  STORE_ATTR               state_buffer

 L. 403       304  LOAD_FAST                'result_line'
              306  LOAD_FAST                'self'
              308  LOAD_ATTR                RESULT_TOKEN_START_LEN
              310  LOAD_CONST               None
              312  BUILD_SLICE_2         2 
              314  BINARY_SUBSCR    
              316  STORE_FAST               'resultlen'

 L. 404       318  SETUP_FINALLY       334  'to 334'

 L. 405       320  LOAD_GLOBAL              int
              322  LOAD_FAST                'resultlen'
              324  CALL_FUNCTION_1       1  ''
              326  LOAD_FAST                'self'
              328  STORE_ATTR               resultlen
              330  POP_BLOCK        
              332  JUMP_FORWARD        466  'to 466'
            334_0  COME_FROM_FINALLY   318  '318'

 L. 406       334  DUP_TOP          
              336  LOAD_GLOBAL              ValueError
              338  COMPARE_OP               exception-match
          340_342  POP_JUMP_IF_FALSE   464  'to 464'
              344  POP_TOP          
              346  POP_TOP          
              348  POP_TOP          

 L. 407       350  SETUP_FINALLY       364  'to 364'

 L. 408       352  LOAD_GLOBAL              as_string
              354  LOAD_FAST                'result_line'
              356  CALL_FUNCTION_1       1  ''
              358  STORE_FAST               'result_line'
              360  POP_BLOCK        
              362  JUMP_FORWARD        394  'to 394'
            364_0  COME_FROM_FINALLY   350  '350'

 L. 409       364  DUP_TOP          
              366  LOAD_GLOBAL              UnicodeDecodeError
              368  COMPARE_OP               exception-match
          370_372  POP_JUMP_IF_FALSE   392  'to 392'
              374  POP_TOP          
              376  POP_TOP          
              378  POP_TOP          

 L. 410       380  LOAD_STR                 'Undecodable: %r'
              382  LOAD_FAST                'result_line'
              384  BINARY_MODULO    
              386  STORE_FAST               'result_line'
              388  POP_EXCEPT       
              390  JUMP_FORWARD        394  'to 394'
            392_0  COME_FROM           370  '370'
              392  END_FINALLY      
            394_0  COME_FROM           390  '390'
            394_1  COME_FROM           362  '362'

 L. 411       394  LOAD_FAST                'process'
              396  LOAD_ATTR                config
              398  LOAD_ATTR                options
              400  LOAD_ATTR                logger
              402  LOAD_METHOD              warn

 L. 412       404  LOAD_STR                 "%s: bad result line: '%s'"
              406  LOAD_FAST                'procname'
              408  LOAD_FAST                'result_line'
              410  BUILD_TUPLE_2         2 
              412  BINARY_MODULO    

 L. 411       414  CALL_METHOD_1         1  ''
              416  POP_TOP          

 L. 414       418  LOAD_FAST                'self'
              420  LOAD_METHOD              _change_listener_state
              422  LOAD_GLOBAL              EventListenerStates
              424  LOAD_ATTR                UNKNOWN
              426  CALL_METHOD_1         1  ''
              428  POP_TOP          

 L. 415       430  LOAD_CONST               b''
              432  LOAD_FAST                'self'
              434  STORE_ATTR               state_buffer

 L. 416       436  LOAD_GLOBAL              notify
              438  LOAD_GLOBAL              EventRejectedEvent
              440  LOAD_FAST                'process'
              442  LOAD_FAST                'process'
              444  LOAD_ATTR                event
              446  CALL_FUNCTION_2       2  ''
              448  CALL_FUNCTION_1       1  ''
              450  POP_TOP          

 L. 417       452  LOAD_CONST               None
              454  LOAD_FAST                'process'
              456  STORE_ATTR               event

 L. 418       458  POP_EXCEPT       
              460  LOAD_CONST               None
              462  RETURN_VALUE     
            464_0  COME_FROM           340  '340'
              464  END_FINALLY      
            466_0  COME_FROM           332  '332'
              466  JUMP_FORWARD        584  'to 584'
            468_0  COME_FROM           242  '242'

 L. 421       468  LOAD_FAST                'self'
              470  LOAD_ATTR                resultlen
              472  LOAD_GLOBAL              len
              474  LOAD_FAST                'self'
              476  LOAD_ATTR                result
              478  CALL_FUNCTION_1       1  ''
              480  BINARY_SUBTRACT  
              482  STORE_FAST               'needed'

 L. 423       484  LOAD_FAST                'needed'
          486_488  POP_JUMP_IF_FALSE   546  'to 546'

 L. 424       490  LOAD_FAST                'self'
              492  DUP_TOP          
              494  LOAD_ATTR                result
              496  LOAD_FAST                'self'
              498  LOAD_ATTR                state_buffer
              500  LOAD_CONST               None
              502  LOAD_FAST                'needed'
              504  BUILD_SLICE_2         2 
              506  BINARY_SUBSCR    
              508  INPLACE_ADD      
              510  ROT_TWO          
              512  STORE_ATTR               result

 L. 425       514  LOAD_FAST                'self'
              516  LOAD_ATTR                state_buffer
              518  LOAD_FAST                'needed'
              520  LOAD_CONST               None
              522  BUILD_SLICE_2         2 
              524  BINARY_SUBSCR    
              526  LOAD_FAST                'self'
              528  STORE_ATTR               state_buffer

 L. 426       530  LOAD_FAST                'self'
              532  LOAD_ATTR                resultlen
              534  LOAD_GLOBAL              len
              536  LOAD_FAST                'self'
              538  LOAD_ATTR                result
              540  CALL_FUNCTION_1       1  ''
              542  BINARY_SUBTRACT  
              544  STORE_FAST               'needed'
            546_0  COME_FROM           486  '486'

 L. 428       546  LOAD_FAST                'needed'
          548_550  POP_JUMP_IF_TRUE    584  'to 584'

 L. 429       552  LOAD_FAST                'self'
              554  LOAD_METHOD              handle_result
              556  LOAD_FAST                'self'
              558  LOAD_ATTR                result
              560  CALL_METHOD_1         1  ''
              562  POP_TOP          

 L. 430       564  LOAD_CONST               None
              566  LOAD_FAST                'self'
              568  LOAD_ATTR                process
              570  STORE_ATTR               event

 L. 431       572  LOAD_CONST               b''
              574  LOAD_FAST                'self'
              576  STORE_ATTR               result

 L. 432       578  LOAD_CONST               None
              580  LOAD_FAST                'self'
              582  STORE_ATTR               resultlen
            584_0  COME_FROM           548  '548'
            584_1  COME_FROM           466  '466'

 L. 434       584  LOAD_FAST                'self'
              586  LOAD_ATTR                state_buffer
          588_590  POP_JUMP_IF_FALSE   600  'to 600'
            592_0  COME_FROM           174  '174'

 L. 436       592  LOAD_FAST                'self'
              594  LOAD_METHOD              handle_listener_state_change
              596  CALL_METHOD_0         0  ''
              598  POP_TOP          
            600_0  COME_FROM           588  '588'
            600_1  COME_FROM           230  '230'
            600_2  COME_FROM           180  '180'

Parse error at or near `LOAD_CONST' instruction at offset 460

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
    __doc__ = ' Input (stdin) dispatcher '

    def __init__(self, process, channel, fd):
        PDispatcher.__init__(self, process, channel, fd)
        self.input_buffer = b''

    def writable(self):
        if self.input_buffer:
            if not self.closed:
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
                try:
                    if why.args[0] == errno.EPIPE:
                        self.input_buffer = b''
                        self.close()
                    else:
                        raise
                finally:
                    why = None
                    del why


ANSI_ESCAPE_BEGIN = b'\x1b['
ANSI_TERMINATORS = (b'H', b'f', b'A', b'B', b'C', b'D', b'R', b's', b'u', b'J', b'K',
                    b'h', b'l', b'p', b'm')

def stripEscapes(s):
    """
    Remove all ANSI color escapes from the given string.
    """
    result = b''
    show = 1
    i = 0
    L = len(s)
    while i < L:
        if show == 0 and s[i:i + 1] in ANSI_TERMINATORS:
            show = 1
        else:
            if show:
                n = s.find(ANSI_ESCAPE_BEGIN, i)
                if n == -1:
                    return result + s[i:]
                result = result + s[i:n]
                i = n
                show = 0
        i += 1

    return result


class RejectEvent(Exception):
    __doc__ = ' The exception type expected by a dispatcher when a handler wants\n    to reject an event '


def default_handler(event, response):
    if response != b'OK':
        raise RejectEvent(response)