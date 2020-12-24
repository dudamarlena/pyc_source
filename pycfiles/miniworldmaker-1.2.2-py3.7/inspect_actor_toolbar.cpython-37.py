# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\containers\inspect_actor_toolbar.py
# Compiled at: 2019-07-02 05:25:55
# Size of source mod 2**32: 5002 bytes
from miniworldmaker.containers import toolbar
from miniworldmaker.containers.toolbar_widgets import *

class InspectActorToolbar(toolbar.Toolbar):

    def __init__(self, board):
        super().__init__()
        self.position = 'right'
        self.board = board
        self.actor = None
        self.registered_events.add('all')
        self.registered_events.add('debug')
        self.default_size = 280
        self.active_token = None
        self.direction_label = 0
        self.position_label = 0

    def set_active_token(self, token):
        self.active_token = token
        self.active_token.costume.info_overlay = True
        token.dirty = 1
        self.window.send_event_to_containers('active_token', token)
        return token

    def get_active_token_from_board_position(self, pos):
        tokens = self.board.get_tokens_by_pixel(pos)
        if tokens:
            i = 0
            while i < len(tokens):
                if self.active_token == tokens[i]:
                    if i < len(tokens) - 1:
                        return tokens[(i + 1)]
                    return tokens[0]
                i = i + 1

        else:
            return tokens or None
        if self.active_token not in tokens:
            return tokens[0]

    def _add_to_window(self, window, dock, size=None):
        super()._add_to_window(window, dock, size)
        for actor in self.window.board.tokens:
            self.add_widget(TokenButton(token=actor, toolbar=self))

    def handle_event--- This code section failed: ---

 L.  53         0  LOAD_FAST                'event'
                2  POP_JUMP_IF_FALSE    68  'to 68'
                4  LOAD_STR                 'mouse'
                6  LOAD_FAST                'event'
                8  COMPARE_OP               in
               10  POP_JUMP_IF_FALSE    68  'to 68'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                board
               16  LOAD_METHOD              get_mouse_position
               18  CALL_METHOD_0         0  '0 positional arguments'
               20  POP_JUMP_IF_FALSE    68  'to 68'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                board
               26  LOAD_METHOD              get_mouse_position
               28  CALL_METHOD_0         0  '0 positional arguments'
               30  LOAD_METHOD              is_on_board
               32  CALL_METHOD_0         0  '0 positional arguments'
               34  POP_JUMP_IF_FALSE    68  'to 68'

 L.  54        36  LOAD_FAST                'event'
               38  LOAD_STR                 'mouse_left'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    68  'to 68'

 L.  55        44  LOAD_FAST                'self'
               46  LOAD_METHOD              get_active_token_from_board_position
               48  LOAD_FAST                'data'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  STORE_FAST               'token'

 L.  56        54  LOAD_FAST                'token'
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L.  57        58  LOAD_FAST                'self'
               60  LOAD_METHOD              set_active_token
               62  LOAD_FAST                'token'
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          
             68_0  COME_FROM            56  '56'
             68_1  COME_FROM            42  '42'
             68_2  COME_FROM            34  '34'
             68_3  COME_FROM            20  '20'
             68_4  COME_FROM            10  '10'
             68_5  COME_FROM             2  '2'

 L.  58        68  LOAD_GLOBAL              super
               70  CALL_FUNCTION_0       0  '0 positional arguments'
               72  LOAD_METHOD              get_event
               74  LOAD_FAST                'event'
               76  LOAD_FAST                'data'
               78  CALL_METHOD_2         2  '2 positional arguments'
               80  POP_TOP          

 L.  59        82  LOAD_FAST                'event'
               84  LOAD_STR                 'active_token'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE    96  'to 96'

 L.  60        90  LOAD_FAST                'data'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               actor
             96_0  COME_FROM            88  '88'

 L.  61        96  LOAD_FAST                'self'
               98  LOAD_ATTR                actor
              100  LOAD_CONST               None
              102  COMPARE_OP               is-not
          104_106  POP_JUMP_IF_FALSE   474  'to 474'

 L.  62       108  LOAD_FAST                'event'
              110  LOAD_STR                 'active_token'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_TRUE    126  'to 126'
              116  LOAD_STR                 'token'
              118  LOAD_FAST                'event'
              120  COMPARE_OP               in
          122_124  POP_JUMP_IF_FALSE   360  'to 360'
            126_0  COME_FROM           114  '114'

 L.  63       126  LOAD_FAST                'data'
              128  LOAD_FAST                'self'
              130  STORE_ATTR               actor

 L.  64       132  LOAD_FAST                'self'
              134  LOAD_METHOD              remove_all_widgets
              136  CALL_METHOD_0         0  '0 positional arguments'
              138  POP_TOP          

 L.  65       140  LOAD_FAST                'self'
              142  LOAD_METHOD              add_widget
              144  LOAD_GLOBAL              ToolbarLabel
              146  LOAD_STR                 'Class: '
              148  LOAD_GLOBAL              str
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                actor
              154  LOAD_ATTR                __class__
              156  LOAD_ATTR                __name__
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  BINARY_ADD       
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  CALL_METHOD_1         1  '1 positional argument'
              166  POP_TOP          

 L.  66       168  LOAD_FAST                'self'
              170  LOAD_METHOD              add_widget
              172  LOAD_GLOBAL              ToolbarLabel
              174  LOAD_STR                 'ID: '
              176  LOAD_GLOBAL              str
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                actor
              182  LOAD_ATTR                token_id
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  BINARY_ADD       
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  CALL_METHOD_1         1  '1 positional argument'
              192  POP_TOP          

 L.  67       194  LOAD_FAST                'self'
              196  LOAD_METHOD              add_widget
              198  LOAD_GLOBAL              ToolbarLabel
              200  LOAD_STR                 'Direction: '
              202  LOAD_GLOBAL              str
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                actor
              208  LOAD_ATTR                direction
              210  CALL_FUNCTION_1       1  '1 positional argument'
              212  BINARY_ADD       
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  LOAD_FAST                'self'
              220  STORE_ATTR               direction_label

 L.  69       222  LOAD_STR                 'Position: ('
              224  LOAD_GLOBAL              str
              226  LOAD_GLOBAL              round
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                actor
              232  LOAD_ATTR                position
              234  LOAD_CONST               0
              236  BINARY_SUBSCR    
              238  LOAD_CONST               0
              240  CALL_FUNCTION_2       2  '2 positional arguments'
              242  CALL_FUNCTION_1       1  '1 positional argument'
              244  BINARY_ADD       
              246  LOAD_STR                 ','
              248  BINARY_ADD       
              250  LOAD_GLOBAL              str
              252  LOAD_GLOBAL              round
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                actor
              258  LOAD_ATTR                position
              260  LOAD_CONST               1
              262  BINARY_SUBSCR    
              264  LOAD_CONST               0
              266  CALL_FUNCTION_2       2  '2 positional arguments'
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  BINARY_ADD       
              272  LOAD_STR                 ')'
              274  BINARY_ADD       
              276  STORE_FAST               'rounded_position'

 L.  70       278  LOAD_FAST                'self'
              280  LOAD_METHOD              add_widget
              282  LOAD_GLOBAL              ToolbarLabel
              284  LOAD_FAST                'rounded_position'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  LOAD_FAST                'self'
              292  STORE_ATTR               position_label

 L.  71       294  LOAD_LISTCOMP            '<code_object <listcomp>>'
              296  LOAD_STR                 'InspectActorToolbar.handle_event.<locals>.<listcomp>'
              298  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                actor
              304  LOAD_ATTR                __class__
              306  LOAD_ATTR                __dict__
              308  GET_ITER         
              310  CALL_FUNCTION_1       1  '1 positional argument'
              312  STORE_FAST               'method_list'

 L.  73       314  SETUP_LOOP          472  'to 472'
              316  LOAD_FAST                'method_list'
              318  GET_ITER         
              320  FOR_ITER            356  'to 356'
              322  STORE_FAST               'method'

 L.  74       324  LOAD_FAST                'self'
              326  LOAD_METHOD              add_widget

 L.  75       328  LOAD_GLOBAL              MethodButton
              330  LOAD_STR                 '--> call method: {0}'
              332  LOAD_METHOD              format
              334  LOAD_FAST                'method'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                actor
              342  LOAD_FAST                'method'
              344  LOAD_CONST               ('text', 'actor', 'method')
              346  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              348  CALL_METHOD_1         1  '1 positional argument'
              350  POP_TOP          
          352_354  JUMP_BACK           320  'to 320'
              356  POP_BLOCK        
              358  JUMP_FORWARD        472  'to 472'
            360_0  COME_FROM           122  '122'

 L.  77       360  LOAD_FAST                'self'
              362  LOAD_ATTR                direction_label
          364_366  POP_JUMP_IF_FALSE   520  'to 520'
              368  LOAD_FAST                'self'
              370  LOAD_ATTR                position_label
          372_374  POP_JUMP_IF_FALSE   520  'to 520'

 L.  78       376  LOAD_FAST                'self'
              378  LOAD_ATTR                direction_label
              380  LOAD_METHOD              set_text
              382  LOAD_STR                 'Direction: '
              384  LOAD_GLOBAL              str
              386  LOAD_FAST                'self'
              388  LOAD_ATTR                actor
              390  LOAD_ATTR                direction
              392  CALL_FUNCTION_1       1  '1 positional argument'
              394  BINARY_ADD       
              396  CALL_METHOD_1         1  '1 positional argument'
              398  LOAD_FAST                'self'
              400  STORE_ATTR               direction_label

 L.  79       402  LOAD_STR                 'Position: ('
              404  LOAD_GLOBAL              str
              406  LOAD_GLOBAL              round
              408  LOAD_FAST                'self'
              410  LOAD_ATTR                actor
              412  LOAD_ATTR                position
              414  LOAD_CONST               0
              416  BINARY_SUBSCR    
              418  LOAD_CONST               0
              420  CALL_FUNCTION_2       2  '2 positional arguments'
              422  CALL_FUNCTION_1       1  '1 positional argument'
              424  BINARY_ADD       
              426  LOAD_STR                 ','
              428  BINARY_ADD       
              430  LOAD_GLOBAL              str
              432  LOAD_GLOBAL              round
              434  LOAD_FAST                'self'
              436  LOAD_ATTR                actor
              438  LOAD_ATTR                position
              440  LOAD_CONST               1
              442  BINARY_SUBSCR    
              444  LOAD_CONST               0
              446  CALL_FUNCTION_2       2  '2 positional arguments'
              448  CALL_FUNCTION_1       1  '1 positional argument'
              450  BINARY_ADD       
              452  LOAD_STR                 ')'
              454  BINARY_ADD       
              456  STORE_FAST               'rounded_position'

 L.  80       458  LOAD_FAST                'self'
              460  LOAD_ATTR                position_label
              462  LOAD_METHOD              set_text
              464  LOAD_FAST                'rounded_position'
              466  CALL_METHOD_1         1  '1 positional argument'
              468  LOAD_FAST                'self'
              470  STORE_ATTR               position_label
            472_0  COME_FROM           358  '358'
            472_1  COME_FROM_LOOP      314  '314'
              472  JUMP_FORWARD        520  'to 520'
            474_0  COME_FROM           104  '104'

 L.  84       474  SETUP_LOOP          520  'to 520'
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                window
              480  LOAD_ATTR                board
              482  LOAD_ATTR                tokens
              484  GET_ITER         
            486_0  COME_FROM           494  '494'
              486  FOR_ITER            518  'to 518'
              488  STORE_FAST               'an_actor'

 L.  85       490  LOAD_FAST                'self'
              492  LOAD_ATTR                actor
          494_496  POP_JUMP_IF_FALSE   486  'to 486'

 L.  86       498  LOAD_FAST                'self'
              500  LOAD_METHOD              add_widget
              502  LOAD_GLOBAL              TokenButton
              504  LOAD_FAST                'an_actor'
              506  LOAD_CONST               ('token',)
              508  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              510  CALL_METHOD_1         1  '1 positional argument'
              512  POP_TOP          
          514_516  JUMP_BACK           486  'to 486'
              518  POP_BLOCK        
            520_0  COME_FROM_LOOP      474  '474'
            520_1  COME_FROM           472  '472'
            520_2  COME_FROM           372  '372'
            520_3  COME_FROM           364  '364'

Parse error at or near `COME_FROM_LOOP' instruction at offset 472_1


class MethodButton(ToolbarButton):

    def __init__(self, text, actor, method):
        super().__init__(text=text)
        self.actor = actor
        self.method = method

    def get_event(self, event, data):
        if self.actor is not None:
            getattrself.actorstr(self.method)()

    def __str__(self):
        return 'MethodButton, {0}'.format(self.actor)


class TokenButton(ToolbarButton):

    def __init__(self, token, toolbar):
        super().__init__(text=(str(token.__class__.__name__) + ' at ' + str(token.position)))
        self.token = token
        if token.costume.image_paths:
            self._img_path = token.costume.image_paths[0]
        self.toolbar = toolbar
        self._text_padding = 30

    def get_event(self, event, data):
        if not self.toolbar.active_token == self.token:
            self.toolbar.set_active_token(token=(self.token))

    def __str__(self):
        return 'ActorButton, {0} at pos: {1}'.format(self.token, self.token.position)