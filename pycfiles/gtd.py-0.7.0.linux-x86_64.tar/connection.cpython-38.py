# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/delucks/.pyenv/versions/3.8.1/lib/python3.8/site-packages/todo/connection.py
# Compiled at: 2020-02-22 12:32:07
# Size of source mod 2**32: 4251 bytes
import trello, requests
from todo.exceptions import GTDException

class TrelloConnection:
    __doc__ = "this one handles connection, retry attempts, stuff like that so it doesn't bail out each\n    time we lose connection\n    creating a connection requires configuration to be parsed because we need the api keys- so this will need to be invoked\n    after the config parser is done doing its thing, with a parameter perhaps being the config\n    "

    def __init__(self, config):
        self.config = config
        self.trello = self._TrelloConnection__connect(config)
        self._main_board = None
        self._main_lists = None

    def __connect--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL              trello
                2  LOAD_ATTR                TrelloClient

 L.  23         4  LOAD_FAST                'config'
                6  LOAD_ATTR                api_key

 L.  24         8  LOAD_FAST                'config'
               10  LOAD_ATTR                api_secret

 L.  25        12  LOAD_FAST                'config'
               14  LOAD_ATTR                oauth_token

 L.  26        16  LOAD_FAST                'config'
               18  LOAD_ATTR                oauth_token_secret

 L.  22        20  LOAD_CONST               ('api_key', 'api_secret', 'token', 'token_secret')
               22  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               24  STORE_FAST               'trello_client'

 L.  28        26  SETUP_FINALLY        46  'to 46'

 L.  30        28  LOAD_FAST                'trello_client'
               30  LOAD_METHOD              fetch_json
               32  LOAD_STR                 '/members/me/boards/?filter=open'
               34  CALL_METHOD_1         1  ''
               36  LOAD_FAST                'self'
               38  STORE_ATTR               boards

 L.  31        40  LOAD_FAST                'trello_client'
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    26  '26'

 L.  32        46  DUP_TOP          
               48  LOAD_GLOBAL              requests
               50  LOAD_ATTR                exceptions
               52  LOAD_ATTR                ConnectionError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    84  'to 84'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  33        64  LOAD_GLOBAL              print
               66  LOAD_STR                 '[FATAL] Could not connect to the Trello API!'
               68  CALL_FUNCTION_1       1  ''
               70  POP_TOP          

 L.  34        72  LOAD_GLOBAL              GTDException
               74  LOAD_CONST               1
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  POP_EXCEPT       
               82  JUMP_FORWARD        124  'to 124'
             84_0  COME_FROM            56  '56'

 L.  35        84  DUP_TOP          
               86  LOAD_GLOBAL              trello
               88  LOAD_ATTR                exceptions
               90  LOAD_ATTR                Unauthorized
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   122  'to 122'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L.  36       102  LOAD_GLOBAL              print
              104  LOAD_STR                 '[FATAL] Trello API credentials are invalid'
              106  CALL_FUNCTION_1       1  ''
              108  POP_TOP          

 L.  37       110  LOAD_GLOBAL              GTDException
              112  LOAD_CONST               1
              114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM            94  '94'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            82  '82'

Parse error at or near `POP_TOP' instruction at offset 60

    def __repr__(self):
        c = 'disconnected' if self.trello is None else 'connected'
        return f"TrelloConnection {c} at {id(self)}"

    def __str__(self):
        return repr(self)

    def main_board(self):
        """use the configuration to get the main board & return it
        This function avoids py-trello's connection.list_boards() function as it produces O(N) network calls.
        This function is guaranteed to only produce 1 network call, in the trello.Board initialization below.
        """
        if self._main_board is not None:
            return self._main_board
        if self.config.board is None:
            board_json = self.boards[0]
        else:
            possible = [b for b in self.boards if b['name'] == self.config.board]
            if possible:
                board_json = possible[0]
            else:
                board_json = self.boards[0]
        board_object = trello.Board.from_json((self.trello), json_obj=board_json)
        self._main_board = board_object
        return board_object

    def boards_by_name(self):
        """Return a mapping of board names present in this account to their JSON contents.
        Useful to potentially avoid a network call when generating mappings for interactive
        completion, and allowing the boards to be turned into objects quickly with Board.from_json
        """
        return {b:b['name'] for b in self.boards}

    def main_lists(self, status_filter='open', force=False):
        """Load the JSON corresponding to all lists on the main board, to ease setup of CardView"""
        if self._main_lists is None:
            lists_json = self.trello.fetch_json(f"/boards/{self.main_board().id}/lists",
              query_params={'cards':'none', 
             'filter':status_filter,  'fields':'all'})
            self._main_lists = lists_json
        return self._main_lists

    def lists_by_id(self):
        """Return a mapping of list names to IDs on the main board, so that cards can have their
        lists shown without making a network call to retrieve the list names.
        """
        return {l['name']:l['id'] for l in self.main_lists(status_filter='all', force=True)}

    def inbox_list(self):
        """use the configuration to get the main board & list from
        Trello, return the list where new cards should go.
        """
        if getattr(self.config, 'inbox_list', False):
            return [l for l in self.main_board().open_lists() if l.name == self.config.inbox_list][0]
        return self.main_board().open_lists()[0]