# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\outputs\speechd_client.py
# Compiled at: 2010-10-23 22:06:20
"""Python API to Speech Dispatcher

Basic Python client API to Speech Dispatcher is provided by the 'SSIPClient'
class.  This interface maps directly to available SSIP commands and logic.

A more convenient interface is provided by the 'Speaker' class.

"""
import socket, sys, os, subprocess, time
try:
    import spawn
except:
    spawn = None

try:
    import threading
except:
    import dummy_threading as threading

class CallbackType(object):
    """Constants describing the available types of callbacks"""
    INDEX_MARK = 'index_marks'
    BEGIN = 'begin'
    END = 'end'
    CANCEL = 'cancel'
    PAUSE = 'pause'
    RESUME = 'resume'


class SSIPError(Exception):
    """Common base class for exceptions during SSIP communication."""
    pass


class SSIPCommunicationError(SSIPError):
    """Exception raised when trying to operate on a closed connection."""
    pass


class SSIPResponseError(Exception):

    def __init__(self, code, msg, data):
        Exception.__init__(self, '%s: %s' % (code, msg))
        self._code = code
        self._msg = msg
        self._data = data

    def code(self):
        """Return the server response error code as integer number."""
        return self._code

    def msg(self):
        """Return server response error message as string."""
        return self._msg


class SSIPCommandError(SSIPResponseError):
    """Exception raised on error response after sending command."""

    def command(self):
        """Return the command string which resulted in this error."""
        return self._data


class SSIPDataError(SSIPResponseError):
    """Exception raised on error response after sending data."""

    def data(self):
        """Return the data which resulted in this error."""
        return self._data


class _SSIP_Connection():
    """Implemantation of low level SSIP communication."""
    _NEWLINE = '\r\n'
    _END_OF_DATA_MARKER = '.'
    _END_OF_DATA_MARKER_ESCAPED = '..'
    _END_OF_DATA = _NEWLINE + _END_OF_DATA_MARKER + _NEWLINE
    _END_OF_DATA_ESCAPED = _NEWLINE + _END_OF_DATA_MARKER_ESCAPED + _NEWLINE
    _CALLBACK_TYPE_MAP = {700: CallbackType.INDEX_MARK, 701: CallbackType.BEGIN, 
       702: CallbackType.END, 
       703: CallbackType.CANCEL, 
       704: CallbackType.PAUSE, 
       705: CallbackType.RESUME}
    if spawn:
        speechd_server_pid = ''

    def __init__(self, host, port):
        """Init connection: open the socket to server,
        initialize buffers, launch a communication handling
        thread."""
        if host == '127.0.0.1' and spawn:
            self.speechd_server_pid = self.speechd_server_spawn()
            time.sleep(0.5)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((socket.gethostbyname(host), port))
        self._buffer = ''
        self._com_buffer = []
        self._callback = None
        self._ssip_reply_semaphore = threading.Semaphore(0)
        self._communication_thread = threading.Thread(target=self._communication, kwargs={}, name='SSIP client communication thread')
        self._communication_thread.daemon = True
        self._communication_thread.start()
        return

    def close(self):
        """Close the server connection, destroy the communication thread."""
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass

        self._socket.close()
        self._communication_thread.join()

    def _communication(self):
        """Handle incomming socket communication.

        Listens for all incomming communication on the socket, dispatches
        events and puts all other replies into self._com_buffer list in the
        already parsed form as (code, msg, data).  Each time a new item is
        appended to the _com_buffer list, the corresponding semaphore
        'self._ssip_reply_semaphore' is incremented.

        This method is designed to run in a separate thread.  The thread can be
        interrupted by closing the socket on which it is listening for
        reading."""
        while True:
            try:
                code, msg, data = self._recv_message()
            except IOError:
                sys.exit()

            if code / 100 != 7:
                self._com_buffer.append((code, msg, data))
                self._ssip_reply_semaphore.release()
                continue
            if self._callback is not None:
                type = self._CALLBACK_TYPE_MAP[code]
                if type == CallbackType.INDEX_MARK:
                    kwargs = {'index_mark': data[2]}
                else:
                    kwargs = {}
                msg_id, client_id = map(int, data[:2])
                self._callback(msg_id, client_id, type, **kwargs)

        return

    def _readline(self):
        """Read one whole line from the socket.

        Blocks until the line delimiter ('_NEWLINE') is read.
        
        """
        pointer = self._buffer.find(self._NEWLINE)
        while pointer == -1:
            try:
                d = self._socket.recv(1024)
            except:
                raise IOError

            if len(d) == 0:
                raise IOError
            self._buffer += d
            pointer = self._buffer.find(self._NEWLINE)

        line = self._buffer[:pointer]
        self._buffer = self._buffer[pointer + len(self._NEWLINE):]
        return line

    def _recv_message--- This code section failed: ---

 L. 198         0  BUILD_LIST_0          0 
                3  STORE_FAST            1  'data'

 L. 199         6  LOAD_CONST               None
                9  STORE_FAST            2  'c'

 L. 200        12  SETUP_LOOP          194  'to 209'
               15  LOAD_GLOBAL           1  'True'
               18  POP_JUMP_IF_FALSE   208  'to 208'

 L. 201        21  LOAD_FAST             0  'self'
               24  LOAD_ATTR             2  '_readline'
               27  CALL_FUNCTION_0       0  None
               30  STORE_FAST            3  'line'

 L. 202        33  LOAD_GLOBAL           3  'len'
               36  LOAD_FAST             3  'line'
               39  CALL_FUNCTION_1       1  None
               42  LOAD_CONST               4
               45  COMPARE_OP            5  >=
               48  POP_JUMP_IF_TRUE     60  'to 60'
               51  LOAD_ASSERT              AssertionError
               54  LOAD_CONST               'Malformed data received from server!'
               57  RAISE_VARARGS_2       2  None

 L. 203        60  LOAD_FAST             3  'line'
               63  LOAD_CONST               3
               66  SLICE+2          
               67  LOAD_FAST             3  'line'
               70  LOAD_CONST               3
               73  BINARY_SUBSCR    
               74  LOAD_FAST             3  'line'
               77  LOAD_CONST               4
               80  SLICE+1          
               81  ROT_THREE        
               82  ROT_TWO          
               83  STORE_FAST            4  'code'
               86  STORE_FAST            5  'sep'
               89  STORE_FAST            6  'text'

 L. 204        92  LOAD_FAST             4  'code'
               95  LOAD_ATTR             5  'isalnum'
               98  CALL_FUNCTION_0       0  None
              101  POP_JUMP_IF_FALSE   140  'to 140'
              104  LOAD_FAST             2  'c'
              107  LOAD_CONST               None
              110  COMPARE_OP            8  is
              113  POP_JUMP_IF_TRUE    128  'to 128'
              116  LOAD_FAST             4  'code'
              119  LOAD_FAST             2  'c'
              122  COMPARE_OP            2  ==
            125_0  COME_FROM           113  '113'
              125  POP_JUMP_IF_FALSE   140  'to 140'

 L. 205       128  LOAD_FAST             5  'sep'
              131  LOAD_CONST               ('-', ' ')
              134  COMPARE_OP            6  in
            137_0  COME_FROM           125  '125'
            137_1  COME_FROM           101  '101'
              137  POP_JUMP_IF_TRUE    149  'to 149'
              140  LOAD_ASSERT              AssertionError
              143  LOAD_CONST               'Malformed data received from server!'
              146  RAISE_VARARGS_2       2  None

 L. 206       149  LOAD_FAST             5  'sep'
              152  LOAD_CONST               ' '
              155  COMPARE_OP            2  ==
              158  POP_JUMP_IF_FALSE   192  'to 192'

 L. 207       161  LOAD_FAST             6  'text'
              164  STORE_FAST            7  'msg'

 L. 208       167  LOAD_GLOBAL           6  'int'
              170  LOAD_FAST             4  'code'
              173  CALL_FUNCTION_1       1  None
              176  LOAD_FAST             7  'msg'
              179  LOAD_GLOBAL           7  'tuple'
              182  LOAD_FAST             1  'data'
              185  CALL_FUNCTION_1       1  None
              188  BUILD_TUPLE_3         3 
              191  RETURN_END_IF    
            192_0  COME_FROM           158  '158'

 L. 209       192  LOAD_FAST             1  'data'
              195  LOAD_ATTR             8  'append'
              198  LOAD_FAST             6  'text'
              201  CALL_FUNCTION_1       1  None
              204  POP_TOP          
              205  JUMP_BACK            15  'to 15'
              208  POP_BLOCK        
            209_0  COME_FROM            12  '12'
              209  LOAD_CONST               None
              212  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 208

    def _recv_response(self):
        """Read server response from the communication thread
        and return the triplet (code, msg, data)."""
        if not self._communication_thread.isAlive():
            raise SSIPCommunicationError
        self._ssip_reply_semaphore.acquire()
        response = self._com_buffer[0]
        del self._com_buffer[0]
        return response

    def send_command(self, command, *args):
        """Send SSIP command with given arguments and read server response.

        Arguments can be of any data type -- they are all stringified before
        being sent to the server.

        Returns a triplet (code, msg, data), where 'code' is a numeric SSIP
        response code as an integer, 'msg' is an SSIP rsponse message as string
        and 'data' is a tuple of strings (all lines of response data) when a
        response contains some data.
        
        'SSIPCommandError' is raised in case of non 2xx return code.  See SSIP
        documentation for more information about server responses and codes.

        'IOError' is raised when the socket was closed by the remote side.
        
        """
        assert command in ('SET', 'CANCEL', 'STOP') and (args[0] in (Scope.SELF, Scope.ALL) or isinstance(args[0], int))
        cmd = (' ').join((command,) + tuple(map(str, args)))
        try:
            self._socket.send(cmd + self._NEWLINE)
        except socket.error:
            raise SSIPCommunicationError('Speech Dispatcher connection lost.')

        code, msg, data = self._recv_response()
        if code / 100 != 2:
            raise SSIPCommandError(code, msg, cmd)
        return (
         code, msg, data)

    def send_data(self, data):
        """Send multiline data and read server response.

        Returned value is the same as for 'send_command()' method.

        'SSIPDataError' is raised in case of non 2xx return code. See SSIP
        documentation for more information about server responses and codes.
        
        'IOError' is raised when the socket was closed by the remote side.
        
        """
        if data.startswith(self._END_OF_DATA_MARKER + self._NEWLINE):
            l = len(self._END_OF_DATA_MARKER)
            data = self._END_OF_DATA_MARKER_ESCAPED + data[l:]
        else:
            if data == self._END_OF_DATA_MARKER:
                data = self._END_OF_DATA_MARKER_ESCAPED
            data = data.replace(self._END_OF_DATA, self._END_OF_DATA_ESCAPED)
            try:
                self._socket.send(data + self._END_OF_DATA)
            except socket.error:
                raise SSIPCommunicationError('Speech Dispatcher connection lost.')

        code, msg, response_data = self._recv_response()
        if code / 100 != 2:
            raise SSIPDataError(code, msg, data)
        return (
         code, msg, response_data)

    def set_callback(self, callback):
        """Register a callback function for handling asynchronous events.

        Arguments:
          callback -- a callable object (function) which will be called to
            handle asynchronous events (arguments described below).  Passing
            `None' results in removing the callback function and ignoring
            events.  Just one callback may be registered.  Attempts to register
            a second callback will result in the former callback being
            replaced.

        The callback function must accept three positional arguments
        ('message_id', 'client_id', 'event_type') and an optional keyword
        argument 'index_mark' (when INDEX_MARK events are turned on).

        Note, that setting the callback function doesn't turn the events on.
        The user is responsible to turn them on by sending the appropriate `SET
        NOTIFICATION' command.

        """
        self._callback = callback

    def speechd_server_spawn(self):
        """Attempts to spawn the speech-dispatcher server."""
        if os.path.exists(spawn.SPD_SPAWN_CMD):
            speechd_server = subprocess.Popen([spawn.SPD_SPAWN_CMD], stdin=None, stdout=subprocess.PIPE, stderr=None)
            return speechd_server.communicate()[0].rstrip('\n')
        else:
            return


class Scope(object):
    """An enumeration of valid SSIP command scopes.

    The constants of this class should be used to specify the 'scope' argument
    for the 'Client' methods.

    """
    SELF = 'self'
    ALL = 'all'


class Priority(object):
    """An enumeration of valid SSIP message priorities.

    The constants of this class should be used to specify the 'priority'
    argument for the 'Client' methods.  For more information about message
    priorities and their interaction, see the SSIP documentation.
    
    """
    IMPORTANT = 'important'
    TEXT = 'text'
    MESSAGE = 'message'
    NOTIFICATION = 'notification'
    PROGRESS = 'progress'


class PunctuationMode(object):
    """Constants for selecting a punctuation mode.

    The mode determines which characters should be read.

    """
    ALL = 'all'
    NONE = 'none'
    SOME = 'some'


class SSIPClient(object):
    """Basic Speech Dispatcher client interface.

    This class provides a Python interface to Speech Dispatcher functionality
    over an SSIP connection.  The API maps directly to available SSIP commands.
    Each connection to Speech Dispatcher is represented by one instance of this
    class.
    
    Many commands take the 'scope' argument, thus it is shortly documented
    here.  It is either one of 'Scope' constants or a number of connection.  By
    specifying the connection number, you are applying the command to a
    particular connection.  This feature is only meant to be used by Speech
    Dispatcher control application, however.  More datails can be found in
    Speech Dispatcher documentation.

    """
    DEFAULT_SPEECHD_HOST = '127.0.0.1'
    DEFAULT_SPEECHD_PORT = 6560

    def __init__(self, name, component='default', user='unknown', host=None, port=None):
        """Initialize the instance and connect to the server.

        Arguments:
          name -- client identification string
          component -- connection identification string.  When one client opens
            multiple connections, this can be used to identify each of them.
          user -- user identification string (user name).  When multi-user
            acces is expected, this can be used to identify their connections.
          host -- server hostname or IP address as a string.  If None, the
            default value is taken from SPEECHD_HOST environment variable (if it
            exists) or from the DEFAULT_SPEECHD_HOST attribute of this class.
          port -- server port as number or None.  If None, the default value is
            taken from SPEECHD_PORT environment variable (if it exists) or from the
            DEFAULT_SPEECHD_PORT attribute of this class.
        
        For more information on client identification strings see Speech
        Dispatcher documentation.
          
        """
        if host is None:
            host = os.environ.get('SPEECHD_HOST', self.DEFAULT_SPEECHD_HOST)
        if port is None:
            try:
                port = int(os.environ.get('SPEECHD_PORT'))
            except (ValueError, TypeError):
                port = self.DEFAULT_SPEECHD_PORT

        self._conn = conn = _SSIP_Connection(host, port)
        full_name = '%s:%s:%s' % (user, name, component)
        conn.send_command('SET', Scope.SELF, 'CLIENT_NAME', full_name)
        code, msg, data = conn.send_command('HISTORY', 'GET', 'CLIENT_ID')
        self._client_id = int(data[0])
        self._lock = threading.Lock()
        self._callbacks = {}
        conn.set_callback(self._callback_handler)
        for event in (CallbackType.INDEX_MARK,
         CallbackType.BEGIN,
         CallbackType.END,
         CallbackType.CANCEL,
         CallbackType.PAUSE,
         CallbackType.RESUME):
            conn.send_command('SET', 'self', 'NOTIFICATION', event, 'on')

        return

    def __del__(self):
        """Close the connection"""
        self.close()

    def _callback_handler(self, msg_id, client_id, type, **kwargs):
        if client_id != self._client_id:
            return
        else:
            self._lock.acquire()
            try:
                try:
                    callback, event_types = self._callbacks[msg_id]
                except KeyError:
                    pass

                if event_types is None or type in event_types:
                    callback(type, **kwargs)
                if type in (CallbackType.END, CallbackType.CANCEL):
                    del self._callbacks[msg_id]
            finally:
                self._lock.release()

            return

    def set_priority--- This code section failed: ---

 L. 453         0  LOAD_FAST             1  'priority'
                3  LOAD_GLOBAL           0  'Priority'
                6  LOAD_ATTR             1  'IMPORTANT'
                9  LOAD_GLOBAL           0  'Priority'
               12  LOAD_ATTR             2  'MESSAGE'

 L. 454        15  LOAD_GLOBAL           0  'Priority'
               18  LOAD_ATTR             3  'TEXT'
               21  LOAD_GLOBAL           0  'Priority'
               24  LOAD_ATTR             4  'NOTIFICATION'

 L. 455        27  LOAD_GLOBAL           0  'Priority'
               30  LOAD_ATTR             5  'PROGRESS'
               33  BUILD_TUPLE_5         5 
               36  COMPARE_OP            6  in
               39  POP_JUMP_IF_TRUE     51  'to 51'
               42  LOAD_ASSERT              AssertionError
               45  LOAD_FAST             1  'priority'
               48  RAISE_VARARGS_2       2  None

 L. 456        51  LOAD_FAST             0  'self'
               54  LOAD_ATTR             7  '_conn'
               57  LOAD_ATTR             8  'send_command'
               60  LOAD_CONST               'SET'
               63  LOAD_GLOBAL           9  'Scope'
               66  LOAD_ATTR            10  'SELF'
               69  LOAD_CONST               'PRIORITY'
               72  LOAD_FAST             1  'priority'
               75  CALL_FUNCTION_4       4  None
               78  POP_TOP          

Parse error at or near `CALL_FUNCTION_4' instruction at offset 75

    def speak(self, text, callback=None, event_types=None):
        """Say given message.

        Arguments:
          text -- message text to be spoken.  This may be either a UTF-8
            encoded byte string or a Python unicode string.
          callback -- a callback handler for asynchronous event notifications.
            A callable object (function) which accepts one positional argument
            `type' and one keyword argument `index_mark'.  See below for more
            details.
          event_types -- a tuple of event types for which the callback should
            be called.  Each item must be one of `CallbackType' constants.
            None (the default value) means to handle all event types.  This
            argument is irrelevant when `callback' is not used.

        The callback function will be called whenever one of the events occurs.
        The event type will be passed as argument.  Its value is one of the
        `CallbackType' constants.  In case of an index mark event, additional
        keyword argument `index_mark' will be passed and will contain the index
        mark identifier as specified within the text.

        The callback function should not perform anything complicated and is
        not allowed to issue any further SSIP client commands.  An attempt to
        do so would lead to a deadlock in SSIP communication.

        This method is non-blocking;  it just sends the command, given
        message is queued on the server and the method returns immediately.

        """
        self._conn.send_command('SPEAK')
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        result = self._conn.send_data(text)
        if callback:
            msg_id = int(result[2][0])
            self._lock.acquire()
            try:
                self._callbacks[msg_id] = (
                 callback, event_types)
            finally:
                self._lock.release()

        return result

    def char(self, char):
        """Say given character.

        Arguments:
          char -- a character to be spoken.  Either a Python unicode string or
            a UTF-8 encoded byte string.

        This method is non-blocking;  it just sends the command, given
        message is queued on the server and the method returns immediately.

        """
        if isinstance(char, unicode):
            char = char.encode('utf-8')
        self._conn.send_command('CHAR', char.replace(' ', 'space'))

    def key(self, key):
        """Say given key name.

        Arguments:
          key -- the key name (as defined in SSIP); string.

        This method is non-blocking;  it just sends the command, given
        message is queued on the server and the method returns immediately.

        """
        self._conn.send_command('KEY', key)

    def sound_icon(self, sound_icon):
        """Output given sound_icon.

        Arguments:
          sound_icon -- the name of the sound icon as defined by SSIP; string.

        This method is non-blocking; it just sends the command, given message
        is queued on the server and the method returns immediately.

        """
        self._conn.send_command('SOUND_ICON', sound_icon)

    def cancel(self, scope=Scope.SELF):
        """Immediately stop speaking and discard messages in queues.

        Arguments:
          scope -- see the documentaion of this class.
            
        """
        self._conn.send_command('CANCEL', scope)

    def stop(self, scope=Scope.SELF):
        """Immediately stop speaking the currently spoken message.

        Arguments:
          scope -- see the documentaion of this class.
        
        """
        self._conn.send_command('STOP', scope)

    def pause(self, scope=Scope.SELF):
        """Pause speaking and postpone other messages until resume.

        This method is non-blocking.  However, speaking can continue for a
        short while even after it's called (typically to the end of the
        sentence).

        Arguments:
          scope -- see the documentaion of this class.
        
        """
        self._conn.send_command('PAUSE', scope)

    def resume(self, scope=Scope.SELF):
        """Resume speaking of the currently paused messages.

        This method is non-blocking.  However, speaking can continue for a
        short while even after it's called (typically to the end of the
        sentence).

        Arguments:
          scope -- see the documentaion of this class.
        
        """
        self._conn.send_command('RESUME', scope)

    def list_output_modules(self):
        """Return names of all active output modules as a tuple of strings."""
        code, msg, data = self._conn.send_command('LIST', 'OUTPUT_MODULES')
        return data

    def list_synthesis_voices(self):
        """Return names of all available voices for the current output module.

        Returns a tuple of tripplets (name, language, dialect).

        'name' is a string, 'language' is an ISO 639-1 Alpha-2 language code
        and 'dialect' is a string.  Language and dialect may be None.

        """
        try:
            code, msg, data = self._conn.send_command('LIST', 'SYNTHESIS_VOICES')
        except SSIPCommandError:
            return ()

        def split(item):
            name, lang, dialect = tuple(item.rsplit(' ', 3))
            return (name, lang or None, dialect or None)

        return tuple([ split(item) for item in data ])

    def set_language(self, language, scope=Scope.SELF):
        """Switch to a particular language for further speech commands.

        Arguments:
          language -- two letter language code according to RFC 1776 as string.
          scope -- see the documentaion of this class.
            
        """
        assert isinstance(language, str) and len(language) == 2
        self._conn.send_command('SET', scope, 'LANGUAGE', language)

    def set_output_module(self, name, scope=Scope.SELF):
        """Switch to a particular output module.

        Arguments:
          name -- module (string) as returned by 'list_output_modules()'.
          scope -- see the documentaion of this class.
        
        """
        self._conn.send_command('SET', scope, 'OUTPUT_MODULE', name)

    def set_pitch--- This code section failed: ---

 L. 642         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             1  'value'
                6  LOAD_GLOBAL           1  'int'
                9  CALL_FUNCTION_2       2  None
               12  POP_JUMP_IF_FALSE    43  'to 43'
               15  LOAD_CONST               -100
               18  LOAD_FAST             1  'value'
               21  DUP_TOP          
               22  ROT_THREE        
               23  COMPARE_OP            1  <=
               26  JUMP_IF_FALSE_OR_POP    38  'to 38'
               29  LOAD_CONST               100
               32  COMPARE_OP            1  <=
               35  JUMP_FORWARD          2  'to 40'
             38_0  COME_FROM            26  '26'
               38  ROT_TWO          
               39  POP_TOP          
             40_0  COME_FROM            35  '35'
             40_1  COME_FROM            12  '12'
               40  POP_JUMP_IF_TRUE     52  'to 52'
               43  LOAD_ASSERT              AssertionError
               46  LOAD_FAST             1  'value'
               49  RAISE_VARARGS_2       2  None

 L. 643        52  LOAD_FAST             0  'self'
               55  LOAD_ATTR             3  '_conn'
               58  LOAD_ATTR             4  'send_command'
               61  LOAD_CONST               'SET'
               64  LOAD_FAST             2  'scope'
               67  LOAD_CONST               'PITCH'
               70  LOAD_FAST             1  'value'
               73  CALL_FUNCTION_4       4  None
               76  POP_TOP          

Parse error at or near `CALL_FUNCTION_4' instruction at offset 73

    def set_rate(self, value, scope=Scope.SELF):
        """Set the speech rate (speed) for further speech commands.

        Arguments:
          value -- integer value within the range from -100 to 100, with 0
            corresponding to the default speech rate of the current speech
            synthesis output module, lower values meaning slower speech and
            higher values meaning faster speech.
          scope -- see the documentaion of this class.
            
        """
        assert isinstance(value, int) and -100 <= value <= 100
        self._conn.send_command('SET', scope, 'RATE', value)

    def set_volume(self, value, scope=Scope.SELF):
        """Set the speech volume for further speech commands.

        Arguments:
          value -- integer value within the range from -100 to 100, with 100
            corresponding to the default speech volume of the current speech
            synthesis output module, lower values meaning softer speech.
          scope -- see the documentaion of this class.
            
        """
        assert isinstance(value, int) and -100 <= value <= 100
        self._conn.send_command('SET', scope, 'VOLUME', value)

    def set_punctuation--- This code section failed: ---

 L. 680         0  LOAD_FAST             1  'value'
                3  LOAD_GLOBAL           0  'PunctuationMode'
                6  LOAD_ATTR             1  'ALL'
                9  LOAD_GLOBAL           0  'PunctuationMode'
               12  LOAD_ATTR             2  'SOME'

 L. 681        15  LOAD_GLOBAL           0  'PunctuationMode'
               18  LOAD_ATTR             3  'NONE'
               21  BUILD_TUPLE_3         3 
               24  COMPARE_OP            6  in
               27  POP_JUMP_IF_TRUE     39  'to 39'
               30  LOAD_ASSERT              AssertionError
               33  LOAD_FAST             1  'value'
               36  RAISE_VARARGS_2       2  None

 L. 682        39  LOAD_FAST             0  'self'
               42  LOAD_ATTR             5  '_conn'
               45  LOAD_ATTR             6  'send_command'
               48  LOAD_CONST               'SET'
               51  LOAD_FAST             2  'scope'
               54  LOAD_CONST               'PUNCTUATION'
               57  LOAD_FAST             1  'value'
               60  CALL_FUNCTION_4       4  None
               63  POP_TOP          

Parse error at or near `CALL_FUNCTION_4' instruction at offset 60

    def set_spelling(self, value, scope=Scope.SELF):
        """Toogle the spelling mode or on off.

        Arguments:
          value -- if 'True', all incomming messages will be spelled
            instead of being read as normal words. 'False' switches
            this behavior off.
          scope -- see the documentaion of this class.
            
        """
        assert value in [True, False]
        if value == True:
            self._conn.send_command('SET', scope, 'SPELLING', 'on')
        else:
            self._conn.send_command('SET', scope, 'SPELLING', 'off')

    def set_cap_let_recogn(self, value, scope=Scope.SELF):
        """Set capital letter recognition mode.

        Arguments:
          value -- one of 'none', 'spell', 'icon'. None means no signalization
            of capital letters, 'spell' means capital letters will be spelled
            with a syntetic voice and 'icon' means that the capital-letter icon
            will be prepended before each capital letter.
          scope -- see the documentaion of this class.
            
        """
        assert value in ('none', 'spell', 'icon')
        self._conn.send_command('SET', scope, 'CAP_LET_RECOGN', value)

    def set_voice(self, value, scope=Scope.SELF):
        """Set voice by a symbolic name.

        Arguments:
          value -- one of the SSIP symbolic voice names: 'MALE1' .. 'MALE3',
            'FEMALE1' ... 'FEMALE3', 'CHILD_MALE', 'CHILD_FEMALE'
          scope -- see the documentaion of this class.

        Symbolic voice names are mapped to real synthesizer voices in the
        configuration of the output module.  Use the method
        'set_synthesis_voice()' if you want to work with real voices.
            
        """
        assert isinstance(value, str) and value.lower() in ('male1', 'male2', 'male3',
                                                            'female1', 'female2',
                                                            'female3', 'child_male',
                                                            'child_female')
        self._conn.send_command('SET', scope, 'VOICE', value)

    def set_synthesis_voice(self, value, scope=Scope.SELF):
        """Set voice by its real name.

        Arguments:
          value -- voice name as returned by 'list_synthesis_voices()'
          scope -- see the documentaion of this class.
            
        """
        self._conn.send_command('SET', scope, 'SYNTHESIS_VOICE', value)

    def set_pause_context(self, value, scope=Scope.SELF):
        """Set the amount of context when resuming a paused message.

        Arguments:
          value -- a positive or negative value meaning how many chunks of data
            after or before the pause should be read when resume() is executed.
          scope -- see the documentaion of this class.
            
        """
        assert isinstance(value, int)
        self._conn.send_command('SET', scope, 'PAUSE_CONTEXT', value)

    def set_debug(self, val):
        """Switch debugging on and off. When switched on,
        debugging files will be created in the chosen destination
        (see set_debug_destination()) for Speech Dispatcher and all
        its running modules. All logging information will then be
        written into these files with maximal verbosity until switched
        off. You should always first call set_debug_destination.

        The intended use of this functionality is to switch debuging
        on for a period of time while the user will repeat the behavior
        and then send the logs to the appropriate bug-reporting place.

        Arguments:
          val -- a boolean value determining whether debugging
                 is switched on or off
          scope -- see the documentaion of this class.
        
        """
        assert isinstance(val, bool)
        if val == True:
            ssip_val = 'ON'
        else:
            ssip_val = 'OFF'
        self._conn.send_command('SET', scope.ALL, 'DEBUG', ssip_val)

    def set_debug_destination(self, path):
        """Set debug destination.

        Arguments:
          path -- path (string) to the directory where debuging
                  files will be created
          scope -- see the documentaion of this class.
        
        """
        assert isinstance(val, string)
        self._conn.send_command('SET', scope.ALL, 'DEBUG_DESTINATION', val)

    def block_begin(self):
        """Begin an SSIP block.

        See SSIP documentation for more details about blocks.

        """
        self._conn.send_command('BLOCK', 'BEGIN')

    def block_end(self):
        """Close an SSIP block.

        See SSIP documentation for more details about blocks.

        """
        self._conn.send_command('BLOCK', 'END')

    def close(self):
        """Close the connection to Speech Dispatcher."""
        if hasattr(self, '_conn'):
            self._conn.close()


class Client(SSIPClient):
    """A DEPRECATED backwards-compatible API.

    This Class is provided only for backwards compatibility with the prevoius
    unofficial API.  It will be removed in future versions.  Please use either
    'SSIPClient' or 'Speaker' interface instead.  As deprecated, the API is no
    longer documented.

    """

    def __init__(self, name=None, client=None, **kwargs):
        name = name or client or 'python'
        super(Client, self).__init__(name, **kwargs)

    def say(self, text, priority=Priority.MESSAGE):
        self.set_priority(priority)
        self.speak(text)

    def char(self, char, priority=Priority.TEXT):
        self.set_priority(priority)
        super(Client, self).char(char)

    def key(self, key, priority=Priority.TEXT):
        self.set_priority(priority)
        super(Client, self).key(key)

    def sound_icon(self, sound_icon, priority=Priority.TEXT):
        self.set_priority(priority)
        super(Client, self).sound_icon(sound_icon)


class Speaker(SSIPClient):
    """Extended Speech Dispatcher Interface.

    This class provides an extended intercace to Speech Dispatcher
    functionality and tries to hide most of the lower level details of SSIP
    (such as a more sophisticated handling of blocks and priorities and
    advanced event notifications) under a more convenient API.
    
    Please note that the API is not yet stabilized and thus is subject to
    change!  Please contact the authors if you plan using it and/or if you have
    any suggestions.

    Well, in fact this class is currently not implemented at all.  It is just a
    draft.  The intention is to hide the SSIP details and provide a generic
    interface practical for screen readers.
    
    """
    pass