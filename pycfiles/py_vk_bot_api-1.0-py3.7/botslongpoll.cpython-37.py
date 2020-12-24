# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_vk_bot_api\botslongpoll.py
# Compiled at: 2019-05-13 16:48:43
# Size of source mod 2**32: 3144 bytes
from .api import api
from .session import session as ses
from .exceptions import *
from requests import post
from threading import Thread
eventTypes = [
 'message_new',
 'message_reply',
 'message_edit',
 'message_allow',
 'message_deny',
 'photo_new',
 'photo_comment_new',
 'photo_comment_edit',
 'photo_comment_restore',
 'photo_comment_delete',
 'audio_new',
 'video_new',
 'video_comment_new',
 'video_comment_edit',
 'video_comment_restore',
 'video_comment_delete',
 'wall_post_new',
 'wall_repost',
 'wall_reply_new',
 'wall_reply_edit',
 'wall_reply_restore',
 'wall_reply_delete',
 'board_post_new',
 'board_post_edit',
 'board_post_restore',
 'board_post_delete',
 'market_comment_new',
 'market_comment_edit',
 'market_comment_restore',
 'market_comment_delete',
 'group_leave',
 'group_join',
 'user_block',
 'user_unblock',
 'poll_vote_new',
 'group_officers_edit',
 'group_change_settings',
 'group_change_photo',
 'vkpay_transaction']

class worker(Thread):

    def __init__(self, func, arg=None):
        Thread.__init__(self)
        self.func = func
        self.funcarg = arg

    def run(self):
        self.func(self.funcarg)


class botsLongPoll(object):
    polling = {}

    def __init__(self, session):
        if not isinstance(session, ses):
            raise mySword('invalid session')
        self.vk = api(session)
        self.group = self.vk.call('groups.getById')
        if 'error' in self.group or len(self.group) == 0:
            raise mySword('this method is available only with group auth')
        self.group = self.group[0]

    def get(self):
        try:
            lp = post((self.server), data={'act':'a_check',  'key':self.key,  'ts':self.ts,  'wait':25}).json()
            self.ts = lp['ts']
            if len(lp['updates']) != 0:
                return lp['updates']
            raise mySword
        except:
            poll = self.vk.call('groups.getLongPollServer', {'group_id': self.group['id']})
            self.poll = poll
            self.server = poll['server']
            self.key = poll['key']
            self.ts = poll['ts']
            return self.get()

    def on(self, func):
        if func.__name__ in eventTypes:
            self.polling = {**{func.__name__: func}, **(self.polling)}
            return
        raise TypeError('unknown event type')

    def __startPolling--- This code section failed: ---

 L.  93         0  SETUP_LOOP          118  'to 118'

 L.  94         2  LOAD_DEREF               'self'
                4  LOAD_ATTR                stop
                6  POP_JUMP_IF_FALSE    10  'to 10'

 L.  95         8  BREAK_LOOP       
             10_0  COME_FROM             6  '6'

 L.  96        10  SETUP_LOOP          114  'to 114'
               12  LOAD_DEREF               'self'
               14  LOAD_METHOD              get
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  GET_ITER         
               20  FOR_ITER            112  'to 112'
               22  STORE_DEREF              'event'

 L.  97        24  LOAD_DEREF               'event'
               26  LOAD_STR                 'type'
               28  BINARY_SUBSCR    
               30  LOAD_DEREF               'self'
               32  LOAD_ATTR                polling
               34  COMPARE_OP               not-in
               36  POP_JUMP_IF_FALSE    40  'to 40'

 L.  98        38  CONTINUE             20  'to 20'
             40_0  COME_FROM            36  '36'

 L.  99        40  LOAD_DEREF               'event'
               42  LOAD_STR                 'type'
               44  BINARY_SUBSCR    
               46  LOAD_STR                 'message_new'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    78  'to 78'

 L. 100        52  BUILD_MAP_0           0 
               54  BUILD_TUPLE_1         1 
               56  LOAD_CLOSURE             'event'
               58  LOAD_CLOSURE             'self'
               60  BUILD_TUPLE_2         2 
               62  LOAD_LAMBDA              '<code_object <lambda>>'
               64  LOAD_STR                 'botsLongPoll.__startPolling.<locals>.<lambda>'
               66  MAKE_FUNCTION_9          'default, closure'
               68  LOAD_DEREF               'event'
               70  LOAD_STR                 'object'
               72  BINARY_SUBSCR    
               74  LOAD_STR                 'send'
               76  STORE_SUBSCR     
             78_0  COME_FROM            50  '50'

 L. 101        78  LOAD_GLOBAL              worker
               80  LOAD_DEREF               'self'
               82  LOAD_ATTR                polling
               84  LOAD_DEREF               'event'
               86  LOAD_STR                 'type'
               88  BINARY_SUBSCR    
               90  BINARY_SUBSCR    
               92  LOAD_DEREF               'event'
               94  LOAD_STR                 'object'
               96  BINARY_SUBSCR    
               98  CALL_FUNCTION_2       2  '2 positional arguments'
              100  STORE_FAST               'work'

 L. 102       102  LOAD_FAST                'work'
              104  LOAD_METHOD              start
              106  CALL_METHOD_0         0  '0 positional arguments'
              108  POP_TOP          
              110  JUMP_BACK            20  'to 20'
              112  POP_BLOCK        
            114_0  COME_FROM_LOOP       10  '10'
              114  JUMP_BACK             2  'to 2'
              116  POP_BLOCK        
            118_0  COME_FROM_LOOP        0  '0'

Parse error at or near `LOAD_LAMBDA' instruction at offset 62

    def startPolling(self):
        self.stop = False
        poll = worker(self._botsLongPoll__startPolling)
        poll.start()

    def stopPolling(self):
        self.stop = True