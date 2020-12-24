# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/lamson/spam.py
# Compiled at: 2011-05-21 19:39:14
"""
Uses the SpamBayes system to perform filtering and classification
of email.  It's designed so that you attach a single decorator
to the state functions you need to be "spam free", and then use the
lamson.spam.Filter code to do training.

SpamBayes comes with extensive command line tools for processing
maildir and mbox for spam.  A good way to train SpamBayes is to 
take mail that you know is spam and stuff it into a maildir, then
periodically use the SpamBayes tools to train from that.
"""
from functools import wraps
from lamson import queue
from spambayes import hammie, Options, storage
import os, logging

class Filter(object):
    """
    This code implements simple filtering and is taken from the
    SpamBayes documentation.
    """

    def __init__--- This code section failed: ---

 L.  25         0  LOAD_GLOBAL           0  'Options'
                3  LOAD_ATTR             1  'options'
                6  STORE_FAST            3  'options'

 L.  26         9  LOAD_FAST             1  'storage_file'
               12  LOAD_FAST             3  'options'
               15  LOAD_CONST               ('Storage', 'persistent_storage_file')
               18  STORE_SUBSCR     

 L.  27        19  LOAD_FAST             3  'options'
               22  LOAD_ATTR             2  'merge_files'
               25  LOAD_CONST               '/etc/hammierc'
               28  LOAD_GLOBAL           3  'os'
               31  LOAD_ATTR             4  'path'
               34  LOAD_ATTR             5  'expanduser'
               37  LOAD_FAST             2  'config'
               40  CALL_FUNCTION_1       1  None
               43  BUILD_LIST_2          2 
               46  CALL_FUNCTION_1       1  None
               49  POP_TOP          

 L.  29        50  LOAD_GLOBAL           0  'Options'
               53  LOAD_ATTR             1  'options'
               56  LOAD_CONST               ('Headers', 'include_trained')
               59  BINARY_SUBSCR    
               60  LOAD_FAST             0  'self'
               63  STORE_ATTR            6  'include_trained'

 L.  30        66  LOAD_GLOBAL           7  'storage'
               69  LOAD_ATTR             8  'database_type'
               72  BUILD_LIST_0          0 
               75  CALL_FUNCTION_1       1  None
               78  UNPACK_SEQUENCE_2     2 
               81  LOAD_FAST             0  'self'
               84  STORE_ATTR            9  'dbname'
               87  LOAD_FAST             0  'self'
               90  STORE_ATTR           10  'usedb'

 L.  32        93  LOAD_CONST               None
               96  LOAD_FAST             0  'self'
               99  STORE_ATTR           12  'mode'

 L.  33       102  LOAD_CONST               None
              105  LOAD_FAST             0  'self'
              108  STORE_ATTR           13  'h'

 L.  35       111  LOAD_GLOBAL           0  'Options'
              114  LOAD_ATTR             1  'options'
              117  LOAD_CONST               ('Hammie', 'train_on_filter')
              120  BINARY_SUBSCR    
              121  UNARY_NOT        
              122  POP_JUMP_IF_TRUE    134  'to 134'
              125  LOAD_ASSERT              AssertionError
              128  LOAD_CONST               'Cannot train_on_filter.'
              131  RAISE_VARARGS_2       2  None
              134  LOAD_CONST               None
              137  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 134

    def open--- This code section failed: ---

 L.  38         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'h'
                6  UNARY_NOT        
                7  POP_JUMP_IF_TRUE     19  'to 19'
               10  LOAD_ASSERT              AssertionError
               13  LOAD_CONST               'Cannot reopen, close first.'
               16  RAISE_VARARGS_2       2  None

 L.  39        19  LOAD_FAST             0  'self'
               22  LOAD_ATTR             2  'mode'
               25  UNARY_NOT        
               26  POP_JUMP_IF_TRUE     38  'to 38'
               29  LOAD_ASSERT              AssertionError
               32  LOAD_CONST               'Mode should be None on open, bad state.'
               35  RAISE_VARARGS_2       2  None

 L.  40        38  LOAD_FAST             1  'mode'
               41  LOAD_CONST               ('r', 'c')
               44  COMPARE_OP            6  in
               47  POP_JUMP_IF_TRUE     59  'to 59'
               50  LOAD_ASSERT              AssertionError
               53  LOAD_CONST               'Must give a valid mode: r, c.'
               56  RAISE_VARARGS_2       2  None

 L.  42        59  LOAD_FAST             1  'mode'
               62  LOAD_FAST             0  'self'
               65  STORE_ATTR            2  'mode'

 L.  43        68  LOAD_GLOBAL           3  'hammie'
               71  LOAD_ATTR             4  'open'
               74  LOAD_FAST             0  'self'
               77  LOAD_ATTR             5  'dbname'
               80  LOAD_FAST             0  'self'
               83  LOAD_ATTR             6  'usedb'
               86  LOAD_FAST             0  'self'
               89  LOAD_ATTR             2  'mode'
               92  CALL_FUNCTION_3       3  None
               95  LOAD_FAST             0  'self'
               98  STORE_ATTR            0  'h'

Parse error at or near `LOAD_FAST' instruction at offset 95

    def close--- This code section failed: ---

 L.  46         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'h'
                6  POP_JUMP_IF_TRUE     13  'to 13'
                9  LOAD_CONST               None
               12  RETURN_END_IF    
             13_0  COME_FROM             6  '6'

 L.  48        13  LOAD_FAST             0  'self'
               16  LOAD_ATTR             1  'mode'
               19  POP_JUMP_IF_TRUE     31  'to 31'
               22  LOAD_ASSERT              AssertionError
               25  LOAD_CONST               'Mode was not set.'
               28  RAISE_VARARGS_2       2  None

 L.  49        31  LOAD_FAST             0  'self'
               34  LOAD_ATTR             1  'mode'
               37  LOAD_CONST               ('r', 'c')
               40  COMPARE_OP            6  in
               43  POP_JUMP_IF_TRUE     55  'to 55'
               46  LOAD_ASSERT              AssertionError
               49  LOAD_CONST               'self.mode was not r or c. Bad state.'
               52  RAISE_VARARGS_2       2  None

 L.  51        55  LOAD_FAST             0  'self'
               58  LOAD_ATTR             1  'mode'
               61  LOAD_CONST               'c'
               64  COMPARE_OP            2  ==
               67  POP_JUMP_IF_FALSE    99  'to 99'

 L.  52        70  LOAD_FAST             0  'self'
               73  LOAD_ATTR             0  'h'
               76  LOAD_ATTR             3  'store'
               79  CALL_FUNCTION_0       0  None
               82  POP_TOP          

 L.  53        83  LOAD_FAST             0  'self'
               86  LOAD_ATTR             0  'h'
               89  LOAD_ATTR             4  'close'
               92  CALL_FUNCTION_0       0  None
               95  POP_TOP          
               96  JUMP_FORWARD          0  'to 99'
             99_0  COME_FROM            96  '96'

 L.  55        99  LOAD_CONST               None
              102  LOAD_FAST             0  'self'
              105  STORE_ATTR            0  'h'

 L.  56       108  LOAD_CONST               None
              111  LOAD_FAST             0  'self'
              114  STORE_ATTR            1  'mode'
              117  LOAD_CONST               None
              120  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 117

    def filter(self, msg):
        self.open('r')
        result = self.h.filter(msg)
        self.close()
        return result

    def train_ham(self, msg):
        self.open('c')
        self.h.train_ham(msg, self.include_trained)
        self.close()

    def train_spam(self, msg):
        self.open('c')
        self.h.train_spam(msg, self.include_trained)
        self.close()

    def untrain_ham(self, msg):
        self.open('c')
        self.h.untrain_ham(msg)
        self.close()

    def untrain_spam(self, msg):
        self.open('c')
        self.h.untrain_spam(msg)
        self.close()


class spam_filter(object):
    """
    This is a decorator you attach to states that should be protected from spam.
    You use it by doing:

        @spam_filter(ham_db, rcfile, spam_dump_queue, next_state=SPAMMING)

    Where ham_db is the path to your hamdb configuration, rcfile is the 
    SpamBayes config, and spam_dump_queue is where this filter should
    dump spam it detects.

    The next_state argument is optional, defaulting to None, but if you use
    it then Lamson will transition that user into that state.  Use it to mark
    that address as a spammer and to ignore their emails or do something
    fancy with them.
    """

    def __init__(self, storage, config, spam_queue, next_state=None):
        self.storage = storage
        self.config = config
        self.spam_queue = spam_queue
        self.next_state = next_state
        if not self.next_state:
            raise AssertionError, 'You must give next_state function.'
            os.path.exists(self.storage) or logging.warn("SPAM filter for %r does not have a valid storage path, it'll still run but won't do anything.", (
             self.storage, self.config, self.spam_queue,
             self.next_state.__name__))
            self.functioning = False
        else:
            self.functioning = True

    def __call__(self, fn):

        @wraps(fn)
        def category_wrapper(message, *args, **kw):
            if self.functioning:
                if self.spam(message.to_message()):
                    self.enqueue_as_spam(message.to_message())
                    return self.next_state
                else:
                    return fn(message, *args, **kw)

            else:
                return fn(message, *args, **kw)

        return category_wrapper

    def spam(self, message):
        """Determines if the message is spam or not."""
        spfilter = Filter(self.storage, self.config)
        spfilter.filter(message)
        if 'X-Spambayes-Classification' in message:
            return message['X-Spambayes-Classification'].startswith('spam')
        else:
            return False

    def enqueue_as_spam(self, message):
        """Drops the message into the configured spam queue."""
        outq = queue.Queue(self.spam_queue)
        outq.push(str(message))