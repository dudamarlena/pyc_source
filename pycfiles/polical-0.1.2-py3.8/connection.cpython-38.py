# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/connection.py
# Compiled at: 2020-05-12 23:09:07
# Size of source mod 2**32: 2553 bytes
import trello, requests
from polical import configuration
import logging
logging.basicConfig(filename=(configuration.get_file_location('Running.log')), level=(logging.INFO), format='%(asctime)s:%(levelname)s:%(message)s')

class GTDException(Exception):
    __doc__ = 'single parameter indicates exit code for the interpreter, because\n    this exception typically results in a return of control to the terminal'

    def __init__(self, errno):
        self.errno = errno


class TrelloConnection:
    __doc__ = "this one handles connection, retry attempts, stuff like that so it doesn't bail out each\n    time we lose connection\n    creating a connection requires configuration to be parsed because we need the api keys- so this will need to be invoked\n    after the config parser is done doing its thing, with a parameter perhaps being the config\n\n    :param bool autoconnect: should we make a network connection to Trello immediately?\n    "

    def __init__(self, config, autoconnect=True):
        self.autoconnect = autoconnect
        self.config = config
        self.trello = self._TrelloConnection__connect(config) if autoconnect else None

    def __connect--- This code section failed: ---

 L.  29         0  LOAD_FAST                'self'
                2  LOAD_METHOD              initialize_trello
                4  LOAD_FAST                'config'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'trello_client'

 L.  30        10  SETUP_FINALLY        30  'to 30'

 L.  32        12  LOAD_FAST                'trello_client'
               14  LOAD_METHOD              fetch_json
               16  LOAD_STR                 '/members/me/boards/?filter=open'
               18  CALL_METHOD_1         1  ''
               20  LOAD_FAST                'self'
               22  STORE_ATTR               boards

 L.  33        24  LOAD_FAST                'trello_client'
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY    10  '10'

 L.  34        30  DUP_TOP          
               32  LOAD_GLOBAL              requests
               34  LOAD_ATTR                exceptions
               36  LOAD_ATTR                ConnectionError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    70  'to 70'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  35        48  LOAD_GLOBAL              logging
               50  LOAD_METHOD              critical
               52  LOAD_STR                 '[FATAL] Could not connect to the Trello API!'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.  36        58  LOAD_GLOBAL              GTDException
               60  LOAD_CONST               1
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
               66  POP_EXCEPT       
               68  JUMP_FORWARD        112  'to 112'
             70_0  COME_FROM            40  '40'

 L.  37        70  DUP_TOP          
               72  LOAD_GLOBAL              trello
               74  LOAD_ATTR                exceptions
               76  LOAD_ATTR                Unauthorized
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   110  'to 110'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L.  38        88  LOAD_GLOBAL              logging
               90  LOAD_METHOD              critical
               92  LOAD_STR                 '[FATAL] Trello API credentials are invalid'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L.  39        98  LOAD_GLOBAL              GTDException
              100  LOAD_CONST               1
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM            80  '80'
              110  END_FINALLY      
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            68  '68'

Parse error at or near `POP_TOP' instruction at offset 44

    def __repr__(self):
        c = 'disconnected' if self.trello is None else 'connected'
        return 'TrelloConnection {0} at {1}'.format(c, id(self))

    def __str__(self):
        return repr(self)

    def initialize_trello(self, config):
        """Initializes our connection to the trello API
        :param dict config: parsed configuration from the yaml file
        :returns: trello.TrelloClient client
        """
        trello_client = trello.TrelloClient(api_key=(config.api_key),
          api_secret=(config.api_secret),
          token=(config.oauth_token),
          token_secret=(config.oauth_token_secret))
        return trello_client