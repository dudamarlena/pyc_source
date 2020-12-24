# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stephenmoore/Projects/utility/photons-interactor/photons_interactor/database/db_queue.py
# Compiled at: 2020-01-11 08:01:53
# Size of source mod 2**32: 3110 bytes
"""
A connector between a bunch of database connections in threads
and the asyncio event loop.

Usage is as follows:

    def some_action(db):
        # db is an instance of photons_interactor.database.connection.DatabaseConnection
        entry = db.create_entry(...)
        db.add(entry)
    await db_queue.request(some_action)

By requesting the function you are putting it onto a queue that will be
picked up by another thread. That thread will then create a database session
that is passed into the function.

The `request` function returns a future that is eventually fulfilled by that
worker and that's how we get the result from the different thread back into the
event loop.
"""
from photons_interactor.database.connection import DatabaseConnection
from photons_app.errors import PhotonsAppError
from photons_app import helpers as hp
from sqlalchemy.pool import StaticPool
import sqlalchemy, logging, sys
log = logging.getLogger('photosn_interactor.database.db_queue')

class DBQueue(hp.ThreadToAsyncQueue):
    __doc__ = 'Connect asyncio to threaded database connections'
    _merged_options_formattable = True

    def setup(self, database):
        self.database = database

    def create_args(self, thread_number, existing):
        """This is run when the queue starts and before every request"""
        if existing:
            return existing
        return (DatabaseConnection((self.database), poolclass=StaticPool),)

    def wrap_request(self, proc, args):
        """We create a new session for every database request"""

        def ret--- This code section failed: ---

 L.  53         0  LOAD_CONST               0
                2  STORE_FAST               'tries'

 L.  55         4  LOAD_DEREF               'args'
                6  UNPACK_SEQUENCE_1     1 
                8  STORE_FAST               'db'

 L.  58        10  LOAD_FAST                'db'
               12  LOAD_METHOD              new_session
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'database'

 L.  61     18_20  SETUP_FINALLY       322  'to 322'
               22  SETUP_FINALLY        52  'to 52'

 L.  62        24  LOAD_DEREF               'proc'
               26  LOAD_FAST                'database'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'res'

 L.  63        32  LOAD_FAST                'database'
               34  LOAD_METHOD              commit
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L.  64        40  LOAD_FAST                'res'
               42  POP_BLOCK        
               44  POP_BLOCK        
            46_48  CALL_FINALLY        322  'to 322'
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    22  '22'

 L.  66        52  DUP_TOP          
               54  LOAD_GLOBAL              sqlalchemy
               56  LOAD_ATTR                exc
               58  LOAD_ATTR                OperationalError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE   134  'to 134'
               64  POP_TOP          
               66  STORE_FAST               'error'
               68  POP_TOP          
               70  SETUP_FINALLY       122  'to 122'

 L.  67        72  LOAD_FAST                'database'
               74  LOAD_METHOD              rollback
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L.  68        80  LOAD_GLOBAL              log
               82  LOAD_METHOD              error

 L.  69        84  LOAD_GLOBAL              hp
               86  LOAD_ATTR                lc

 L.  70        88  LOAD_STR                 'Failed to use database, will rollback and maybe try again'

 L.  70        90  LOAD_FAST                'error'

 L.  69        92  LOAD_CONST               ('error',)
               94  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L.  68        96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L.  73       100  LOAD_FAST                'tries'
              102  LOAD_CONST               1
              104  INPLACE_ADD      
              106  STORE_FAST               'tries'

 L.  75       108  LOAD_FAST                'tries'
              110  LOAD_CONST               1
              112  COMPARE_OP               >
              114  POP_JUMP_IF_FALSE   118  'to 118'

 L.  76       116  RAISE_VARARGS_0       0  'reraise'
            118_0  COME_FROM           114  '114'
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM_FINALLY    70  '70'
              122  LOAD_CONST               None
              124  STORE_FAST               'error'
              126  DELETE_FAST              'error'
              128  END_FINALLY      
              130  POP_EXCEPT       
              132  JUMP_FORWARD        318  'to 318'
            134_0  COME_FROM            62  '62'

 L.  78       134  DUP_TOP          
              136  LOAD_GLOBAL              sqlalchemy
              138  LOAD_ATTR                exc
              140  LOAD_ATTR                InvalidRequestError
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   200  'to 200'
              146  POP_TOP          
              148  STORE_FAST               'error'
              150  POP_TOP          
              152  SETUP_FINALLY       188  'to 188'

 L.  79       154  LOAD_FAST                'database'
              156  LOAD_METHOD              rollback
              158  CALL_METHOD_0         0  ''
              160  POP_TOP          

 L.  80       162  LOAD_GLOBAL              log
              164  LOAD_METHOD              error
              166  LOAD_GLOBAL              hp
              168  LOAD_ATTR                lc
              170  LOAD_STR                 'Failed to perform database operation'
              172  LOAD_FAST                'error'
              174  LOAD_CONST               ('error',)
              176  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          

 L.  81       182  RAISE_VARARGS_0       0  'reraise'
              184  POP_BLOCK        
              186  BEGIN_FINALLY    
            188_0  COME_FROM_FINALLY   152  '152'
              188  LOAD_CONST               None
              190  STORE_FAST               'error'
              192  DELETE_FAST              'error'
              194  END_FINALLY      
              196  POP_EXCEPT       
              198  JUMP_FORWARD        318  'to 318'
            200_0  COME_FROM           144  '144'

 L.  83       200  DUP_TOP          
              202  LOAD_GLOBAL              PhotonsAppError
              204  COMPARE_OP               exception-match
          206_208  POP_JUMP_IF_FALSE   264  'to 264'
              210  POP_TOP          
              212  STORE_FAST               'error'
              214  POP_TOP          
              216  SETUP_FINALLY       252  'to 252'

 L.  84       218  LOAD_FAST                'database'
              220  LOAD_METHOD              rollback
              222  CALL_METHOD_0         0  ''
              224  POP_TOP          

 L.  85       226  LOAD_GLOBAL              log
              228  LOAD_METHOD              error
              230  LOAD_GLOBAL              hp
              232  LOAD_ATTR                lc
              234  LOAD_STR                 'Failed to use database'
              236  LOAD_FAST                'error'
              238  LOAD_CONST               ('error',)
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L.  86       246  RAISE_VARARGS_0       0  'reraise'
              248  POP_BLOCK        
              250  BEGIN_FINALLY    
            252_0  COME_FROM_FINALLY   216  '216'
              252  LOAD_CONST               None
              254  STORE_FAST               'error'
              256  DELETE_FAST              'error'
              258  END_FINALLY      
              260  POP_EXCEPT       
              262  JUMP_FORWARD        318  'to 318'
            264_0  COME_FROM           206  '206'

 L.  88       264  POP_TOP          
              266  POP_TOP          
              268  POP_TOP          

 L.  89       270  LOAD_FAST                'database'
              272  LOAD_METHOD              rollback
              274  CALL_METHOD_0         0  ''
              276  POP_TOP          

 L.  90       278  LOAD_GLOBAL              sys
              280  LOAD_METHOD              exc_info
              282  CALL_METHOD_0         0  ''
              284  STORE_FAST               'exc_info'

 L.  91       286  LOAD_GLOBAL              log
              288  LOAD_METHOD              exception

 L.  92       290  LOAD_GLOBAL              hp
              292  LOAD_ATTR                lc
              294  LOAD_STR                 'Unexpected failure when using database'
              296  LOAD_FAST                'exc_info'
              298  LOAD_CONST               1
              300  BINARY_SUBSCR    
              302  LOAD_CONST               ('error',)
              304  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L.  91       306  CALL_METHOD_1         1  ''
              308  POP_TOP          

 L.  94       310  RAISE_VARARGS_0       0  'reraise'
              312  POP_EXCEPT       
              314  JUMP_FORWARD        318  'to 318'
              316  END_FINALLY      
            318_0  COME_FROM           314  '314'
            318_1  COME_FROM           262  '262'
            318_2  COME_FROM           198  '198'
            318_3  COME_FROM           132  '132'
              318  POP_BLOCK        
              320  BEGIN_FINALLY    
            322_0  COME_FROM            46  '46'
            322_1  COME_FROM_FINALLY    18  '18'

 L.  97       322  LOAD_FAST                'database'
              324  LOAD_METHOD              close
              326  CALL_METHOD_0         0  ''
              328  POP_TOP          
              330  END_FINALLY      
              332  JUMP_BACK             4  'to 4'

Parse error at or near `POP_BLOCK' instruction at offset 44

        return ret