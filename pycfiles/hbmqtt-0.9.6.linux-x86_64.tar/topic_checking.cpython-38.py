# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/plugins/topic_checking.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 2834 bytes
import asyncio

class BaseTopicPlugin:

    def __init__(self, context):
        self.context = context
        try:
            self.topic_config = self.context.config['topic-check']
        except KeyError:
            self.context.logger.warning("'topic-check' section not found in context configuration")

    def topic_filtering(self, *args, **kwargs):
        if not self.topic_config:
            self.context.logger.warning("'auth' section not found in context configuration")
            return False
        return True


class TopicTabooPlugin(BaseTopicPlugin):

    def __init__(self, context):
        super().__init__(context)
        self._taboo = ['prohibited', 'top-secret', 'data/classified']

    @asyncio.coroutine
    def topic_filtering(self, *args, **kwargs):
        filter_result = (super().topic_filtering)(*args, **kwargs)
        if filter_result:
            session = kwargs.get('session', None)
            topic = kwargs.get('topic', None)
            if topic:
                if session.username != 'admin':
                    if topic in self._taboo:
                        return False
                return True
            return False
        return filter_result


class TopicAccessControlListPlugin(BaseTopicPlugin):

    def __init__(self, context):
        super().__init__(context)

    @staticmethod
    def topic_ac--- This code section failed: ---

 L.  46         0  LOAD_FAST                'topic_requested'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'req_split'

 L.  47        10  LOAD_FAST                'topic_allowed'
               12  LOAD_METHOD              split
               14  LOAD_STR                 '/'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'allowed_split'

 L.  48        20  LOAD_CONST               True
               22  STORE_FAST               'ret'

 L.  49        24  LOAD_GLOBAL              range
               26  LOAD_GLOBAL              max
               28  LOAD_GLOBAL              len
               30  LOAD_FAST                'req_split'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_GLOBAL              len
               36  LOAD_FAST                'allowed_split'
               38  CALL_FUNCTION_1       1  ''
               40  CALL_FUNCTION_2       2  ''
               42  CALL_FUNCTION_1       1  ''
               44  GET_ITER         
             46_0  COME_FROM           122  '122'
               46  FOR_ITER            146  'to 146'
               48  STORE_FAST               'i'

 L.  50        50  SETUP_FINALLY        72  'to 72'

 L.  51        52  LOAD_FAST                'req_split'
               54  LOAD_FAST                'i'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'a_aux'

 L.  52        60  LOAD_FAST                'allowed_split'
               62  LOAD_FAST                'i'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'b_aux'
               68  POP_BLOCK        
               70  JUMP_FORWARD        102  'to 102'
             72_0  COME_FROM_FINALLY    50  '50'

 L.  53        72  DUP_TOP          
               74  LOAD_GLOBAL              IndexError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   100  'to 100'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L.  54        86  LOAD_CONST               False
               88  STORE_FAST               'ret'

 L.  55        90  POP_EXCEPT       
               92  POP_TOP          
               94  BREAK_LOOP          146  'to 146'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            78  '78'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            70  '70'

 L.  56       102  LOAD_FAST                'b_aux'
              104  LOAD_STR                 '#'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   116  'to 116'

 L.  57       110  POP_TOP          
              112  BREAK_LOOP          146  'to 146'
              114  JUMP_BACK            46  'to 46'
            116_0  COME_FROM           108  '108'

 L.  58       116  LOAD_FAST                'b_aux'
              118  LOAD_STR                 '+'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_TRUE     46  'to 46'
              124  LOAD_FAST                'b_aux'
              126  LOAD_FAST                'a_aux'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   136  'to 136'

 L.  59       132  CONTINUE             46  'to 46'
              134  JUMP_BACK            46  'to 46'
            136_0  COME_FROM           130  '130'

 L.  61       136  LOAD_CONST               False
              138  STORE_FAST               'ret'

 L.  62       140  POP_TOP          
              142  BREAK_LOOP          146  'to 146'
              144  JUMP_BACK            46  'to 46'

 L.  63       146  LOAD_FAST                'ret'
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 92

    @asyncio.coroutine
    def topic_filtering(self, *args, **kwargs):
        filter_result = (super().topic_filtering)(*args, **kwargs)
        if filter_result:
            session = kwargs.get('session', None)
            req_topic = kwargs.get('topic', None)
            if req_topic:
                username = session.username
                if username is None:
                    username = 'anonymous'
                allowed_topics = self.topic_config['acl'].get(username, None)
                if allowed_topics:
                    for allowed_topic in allowed_topics:
                        if self.topic_ac(req_topic, allowed_topic):
                            return True
                        return False

                return False
            else:
                return False