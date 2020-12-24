# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/QueueCatalog/CatalogEventQueue.py
# Compiled at: 2008-05-13 06:37:54
__doc__ = '\n$Id: CatalogEventQueue.py 86691 2008-05-13 10:37:50Z andreasjung $\n'
import logging
from Persistence import Persistent
from ZODB.POSException import ConflictError
logger = logging.getLogger('event.QueueCatalog')
SAFE_POLICY = 0
ALTERNATIVE_POLICY = 1
REMOVED = 0
ADDED = 1
CHANGED = 2
CHANGED_ADDED = 3
EVENT_TYPES = (REMOVED, CHANGED, ADDED, CHANGED_ADDED)
antiEvent = {REMOVED: ADDED, ADDED: REMOVED, CHANGED: CHANGED, CHANGED_ADDED: CHANGED_ADDED}.get
ADDED_EVENTS = (
 CHANGED, ADDED, CHANGED_ADDED)

class CatalogEventQueue(Persistent):
    """Event queue for catalog events

    This is a rather odd queue. It organizes events by object, where
    objects are identified by uids, which happen to be string paths.

    One way that this queue is extremely odd is that it really only
    keeps track of the last event for an object. This is because we
    really only *care* about the last event for an object.

    There are three types of events:

    ADDED         -- An object was added to the catalog

    CHANGED       -- An object was changed

    REMOVED       -- An object was removed from the catalog

    CHANGED_ADDED -- Add object was added and subsequently changed.
                     This event is a consequence of the queue implementation.
                     
    Note that, although we only keep track of the most recent
    event. there are rules for how the most recent event can be
    updated:

    - It is illegal to update an ADDED, CHANGED, or CHANGED_ADDED
      event with an ADDED event or

    - to update a REMOVED event with a CHANGED event.

    We have a problem because applications don't really indicate
    whether they are are adding, or just updating.  We deduce add
    events by examining the catalog and event queue states.

    Also note that, when events are applied to the catalog, events may
    have no effect.

    - If an object is in the catalog, ADDED events are equivalent to
      CHANGED events.

    - If an object is not in the catalog, REMOVED and CHANGED events
      have no effect.

    If we undo a transaction, we generate an anti-event. The anti
    event of ADDED id REMOVED, of REMOVED is ADDED, and of CHANGED is
    CHANGED. 

    Note that these rules represent heuristics that attempt to provide
    efficient and sensible behavior for most cases. They are not "correct" in
    that they handle cases that may not seem handleable. For example,
    consider a sequence of transactions:

      T1 adds an object
      T2 removes the object
      T3 adds the object
      T4 processes the queue
      T5 undoes T1

    It's not clear what should be done in this case? We decide to
    generate a remove event, even though a later transaction added the
    object again. Is this correct? It's hard to say. The decision we
    make is not horrible and it allows us to provide a very efficient
    implementation.  See the unit tests for other scenarios. Feel
    free to think of cases for which our decisions are unacceptably
    wrong and write unit tests for these cases.

    There are two kinds of transactions that affect the queue:

    - Application transactions always add or modify events. They never
      remove events.

    - Queue processing transactions always remove events.
    
    """
    __module__ = __name__
    _conflict_policy = SAFE_POLICY

    def __init__(self, conflict_policy=SAFE_POLICY):
        self._data = {}
        self._conflict_policy = conflict_policy

    def __nonzero__(self):
        return not not self._data

    def __len__(self):
        return len(self._data)

    def update(self, uid, etype):
        assert etype in EVENT_TYPES
        data = self._data
        current = data.get(uid)
        if current is not None:
            (generation, current) = current
            if current in ADDED_EVENTS and etype is ADDED:
                raise TypeError('Attempt to add an object that is already in the catalog')
            if current is REMOVED and etype is CHANGED:
                raise TypeError('Attempt to change an object that has been removed')
            if (current is ADDED or current is CHANGED_ADDED) and etype is CHANGED:
                etype = CHANGED_ADDED
        else:
            generation = 0
        data[uid] = (generation + 1, etype)
        self._p_changed = 1
        return

    def getEvent(self, uid):
        state = self._data.get(uid)
        if state is not None:
            state = state[1]
        return state

    def process(self, limit=None):
        """Removes and returns events from this queue.

        If limit is specified, at most (limit) events are removed.
        """
        data = self._data
        if not limit or len(data) <= limit:
            self._data = {}
            return data
        else:
            self._p_changed = 1
            res = {}
            keys = data.keys()[:limit]
            for key in keys:
                res[key] = data[key]
                del data[key]

            return res

    def _p_resolveConflict--- This code section failed: ---

 L. 189         0  LOAD_FAST             3  'newstate'
                3  LOAD_CONST               '_conflict_policy'
                6  BINARY_SUBSCR    
                7  STORE_FAST            9  'policy'

 L. 192        10  LOAD_FAST             1  'oldstate'
               13  LOAD_CONST               '_data'
               16  BINARY_SUBSCR    
               17  STORE_FAST           11  'oldstate_data'

 L. 193        20  LOAD_FAST             2  'committed'
               23  LOAD_CONST               '_data'
               26  BINARY_SUBSCR    
               27  STORE_FAST            8  'committed_data'

 L. 194        30  LOAD_FAST             3  'newstate'
               33  LOAD_CONST               '_data'
               36  BINARY_SUBSCR    
               37  STORE_FAST           10  'newstate_data'

 L. 197        40  SETUP_LOOP          500  'to 543'
               43  LOAD_FAST            10  'newstate_data'
               46  LOAD_ATTR             7  'items'
               49  CALL_FUNCTION_0       0  None
               52  GET_ITER         
               53  FOR_ITER            486  'to 542'
               56  UNPACK_SEQUENCE_2     2 
               59  STORE_FAST            5  'uid'
               62  STORE_FAST            6  'new'

 L. 200        65  LOAD_FAST            11  'oldstate_data'
               68  LOAD_ATTR            10  'get'
               71  LOAD_FAST             5  'uid'
               74  CALL_FUNCTION_1       1  None
               77  STORE_FAST            4  'old'

 L. 201        80  LOAD_FAST             8  'committed_data'
               83  LOAD_ATTR            10  'get'
               86  LOAD_FAST             5  'uid'
               89  CALL_FUNCTION_1       1  None
               92  STORE_FAST            7  'current'

 L. 203        95  LOAD_FAST             6  'new'
               98  LOAD_FAST             4  'old'
              101  COMPARE_OP            3  !=
              104  JUMP_IF_FALSE       431  'to 538'
            107_0  THEN                     539
              107  POP_TOP          

 L. 206       108  LOAD_FAST             4  'old'
              111  LOAD_CONST               None
              114  COMPARE_OP            9  is-not
              117  JUMP_IF_FALSE       173  'to 293'
            120_0  THEN                     294
              120  POP_TOP          

 L. 208       121  LOAD_FAST             6  'new'
              124  LOAD_CONST               0
              127  BINARY_SUBSCR    
              128  LOAD_FAST             4  'old'
              131  LOAD_CONST               0
              134  BINARY_SUBSCR    
              135  COMPARE_OP            0  <
              138  JUMP_IF_FALSE        26  'to 167'
              141  POP_TOP          

 L. 212       142  LOAD_CONST               0
              145  LOAD_GLOBAL          14  'antiEvent'
              148  LOAD_FAST             4  'old'
              151  LOAD_CONST               1
              154  BINARY_SUBSCR    
              155  CALL_FUNCTION_1       1  None
              158  BUILD_TUPLE_2         2 
              161  STORE_FAST            6  'new'
              164  JUMP_FORWARD        116  'to 283'
            167_0  COME_FROM           138  '138'
              167  POP_TOP          

 L. 213       168  LOAD_FAST             6  'new'
              171  LOAD_CONST               1
              174  BINARY_SUBSCR    
              175  LOAD_GLOBAL          15  'ADDED'
              178  COMPARE_OP            8  is
              181  JUMP_IF_FALSE        98  'to 282'
            184_0  THEN                     283
              184  POP_TOP          

 L. 214       185  LOAD_FAST             9  'policy'
              188  LOAD_GLOBAL          16  'SAFE_POLICY'
              191  COMPARE_OP            2  ==
              194  JUMP_IF_FALSE        27  'to 224'
            197_0  THEN                     279
              197  POP_TOP          

 L. 215       198  LOAD_GLOBAL          17  'logger'
              201  LOAD_ATTR            18  'error'
              204  LOAD_CONST               'Queue conflict on %s: ADDED on existing item'
              207  LOAD_FAST             5  'uid'
              210  BINARY_MODULO    
              211  CALL_FUNCTION_1       1  None
              214  POP_TOP          

 L. 216       215  LOAD_GLOBAL          19  'ConflictError'
              218  RAISE_VARARGS_1       1  None
              221  JUMP_ABSOLUTE       283  'to 283'
            224_0  COME_FROM           194  '194'
              224  POP_TOP          

 L. 218       225  LOAD_FAST             7  'current'
              228  JUMP_IF_FALSE        27  'to 258'
              231  POP_TOP          
              232  LOAD_FAST             7  'current'
              235  LOAD_CONST               1
              238  BINARY_SUBSCR    
              239  LOAD_GLOBAL          20  'REMOVED'
              242  COMPARE_OP            2  ==
              245  JUMP_IF_FALSE        10  'to 258'
            248_0  THEN                     279
              248  POP_TOP          

 L. 219       249  LOAD_FAST             7  'current'
              252  STORE_FAST            6  'new'
              255  JUMP_ABSOLUTE       283  'to 283'
            258_0  COME_FROM           245  '245'
            258_1  COME_FROM           228  '228'
              258  POP_TOP          

 L. 221       259  LOAD_FAST             7  'current'
              262  LOAD_CONST               0
              265  BINARY_SUBSCR    
              266  LOAD_CONST               1
              269  BINARY_ADD       
              270  LOAD_GLOBAL          21  'CHANGED_ADDED'
              273  BUILD_TUPLE_2         2 
              276  STORE_FAST            6  'new'
              279  JUMP_FORWARD          1  'to 283'
            282_0  COME_FROM           181  '181'
              282  POP_TOP          
            283_0  COME_FROM           279  '279'
            283_1  COME_FROM           164  '164'

 L. 226       283  LOAD_FAST            11  'oldstate_data'
              286  LOAD_FAST             5  'uid'
              289  DELETE_SUBSCR    
              290  JUMP_FORWARD          1  'to 294'
            293_0  COME_FROM           117  '117'
              293  POP_TOP          
            294_0  COME_FROM           290  '290'

 L. 231       294  LOAD_FAST             7  'current'
              297  LOAD_CONST               None
              300  COMPARE_OP            9  is-not
              303  JUMP_IF_FALSE       218  'to 524'
            306_0  THEN                     525
              306  POP_TOP          

 L. 232       307  LOAD_FAST             7  'current'
              310  LOAD_CONST               1
              313  BINARY_SUBSCR    
              314  LOAD_FAST             6  'new'
              317  LOAD_CONST               1
              320  BINARY_SUBSCR    
              321  COMPARE_OP            3  !=
              324  JUMP_IF_FALSE       190  'to 517'
              327  POP_TOP          

 L. 233       328  LOAD_FAST             9  'policy'
              331  LOAD_GLOBAL          16  'SAFE_POLICY'
              334  COMPARE_OP            2  ==
              337  JUMP_IF_FALSE        27  'to 367'
              340  POP_TOP          

 L. 235       341  LOAD_GLOBAL          17  'logger'
              344  LOAD_ATTR            18  'error'
              347  LOAD_CONST               'Queue conflict on %s'
              350  LOAD_FAST             5  'uid'
              353  BINARY_MODULO    
              354  CALL_FUNCTION_1       1  None
              357  POP_TOP          

 L. 236       358  LOAD_GLOBAL          19  'ConflictError'
              361  RAISE_VARARGS_1       1  None
              364  JUMP_FORWARD        114  'to 481'
            367_0  COME_FROM           337  '337'
              367  POP_TOP          

 L. 237       368  LOAD_GLOBAL          20  'REMOVED'
              371  LOAD_FAST             6  'new'
              374  LOAD_CONST               1
              377  BINARY_SUBSCR    
              378  LOAD_FAST             7  'current'
              381  LOAD_CONST               1
              384  BINARY_SUBSCR    
              385  BUILD_TUPLE_2         2 
              388  COMPARE_OP            7  not-in
              391  JUMP_IF_FALSE        34  'to 428'
              394  POP_TOP          

 L. 238       395  LOAD_FAST             7  'current'
              398  LOAD_CONST               0
              401  BINARY_SUBSCR    
              402  LOAD_CONST               1
              405  BINARY_ADD       
              406  LOAD_GLOBAL          21  'CHANGED_ADDED'
              409  BUILD_TUPLE_2         2 
              412  STORE_FAST            6  'new'

 L. 239       415  LOAD_FAST             6  'new'
              418  LOAD_FAST             8  'committed_data'
              421  LOAD_FAST             5  'uid'
              424  STORE_SUBSCR     
              425  JUMP_FORWARD         53  'to 481'
            428_0  COME_FROM           391  '391'
              428  POP_TOP          

 L. 240       429  LOAD_FAST             7  'current'
              432  LOAD_CONST               0
              435  BINARY_SUBSCR    
              436  LOAD_FAST             6  'new'
              439  LOAD_CONST               0
              442  BINARY_SUBSCR    
              443  COMPARE_OP            0  <
              446  JUMP_IF_FALSE        31  'to 480'
              449  POP_TOP          
              450  LOAD_FAST             6  'new'
              453  LOAD_CONST               1
              456  BINARY_SUBSCR    
              457  LOAD_GLOBAL          20  'REMOVED'
              460  COMPARE_OP            2  ==
              463  JUMP_IF_FALSE        14  'to 480'
            466_0  THEN                     481
              466  POP_TOP          

 L. 242       467  LOAD_FAST             6  'new'
              470  LOAD_FAST             8  'committed_data'
              473  LOAD_FAST             5  'uid'
              476  STORE_SUBSCR     
              477  JUMP_FORWARD          1  'to 481'
            480_0  COME_FROM           463  '463'
            480_1  COME_FROM           446  '446'
              480  POP_TOP          
            481_0  COME_FROM           477  '477'
            481_1  COME_FROM           425  '425'
            481_2  COME_FROM           364  '364'

 L. 246       481  LOAD_FAST            11  'oldstate_data'
              484  LOAD_ATTR            10  'get'
              487  LOAD_FAST             5  'uid'
              490  CALL_FUNCTION_1       1  None
              493  LOAD_CONST               None
              496  COMPARE_OP            9  is-not
              499  JUMP_IF_FALSE        11  'to 513'
              502  POP_TOP          

 L. 247       503  LOAD_FAST            11  'oldstate_data'
              506  LOAD_FAST             5  'uid'
              509  DELETE_SUBSCR    
              510  JUMP_ABSOLUTE       518  'to 518'
            513_0  COME_FROM           499  '499'
              513  POP_TOP          
              514  JUMP_BACK            53  'to 53'
            517_0  COME_FROM           324  '324'
              517  POP_TOP          

 L. 250       518  CONTINUE             53  'to 53'
              521  JUMP_FORWARD          1  'to 525'
            524_0  COME_FROM           303  '303'
              524  POP_TOP          
            525_0  COME_FROM           521  '521'

 L. 252       525  LOAD_FAST             6  'new'
              528  LOAD_FAST             8  'committed_data'
              531  LOAD_FAST             5  'uid'
              534  STORE_SUBSCR     
              535  JUMP_BACK            53  'to 53'
            538_0  COME_FROM           104  '104'
              538  POP_TOP          
              539  JUMP_BACK            53  'to 53'
              542  POP_BLOCK        
            543_0  COME_FROM            40  '40'

 L. 256       543  SETUP_LOOP          141  'to 687'
              546  LOAD_FAST            11  'oldstate_data'
              549  LOAD_ATTR             7  'items'
              552  CALL_FUNCTION_0       0  None
              555  GET_ITER         
              556  FOR_ITER            127  'to 686'
              559  UNPACK_SEQUENCE_2     2 
              562  STORE_FAST            5  'uid'
              565  STORE_FAST            4  'old'

 L. 257       568  LOAD_CONST               0
              571  LOAD_GLOBAL          14  'antiEvent'
              574  LOAD_FAST             4  'old'
              577  LOAD_CONST               1
              580  BINARY_SUBSCR    
              581  CALL_FUNCTION_1       1  None
              584  BUILD_TUPLE_2         2 
              587  STORE_FAST            6  'new'

 L. 260       590  LOAD_FAST             8  'committed_data'
              593  LOAD_ATTR            10  'get'
              596  LOAD_FAST             5  'uid'
              599  CALL_FUNCTION_1       1  None
              602  STORE_FAST            7  'current'

 L. 261       605  LOAD_FAST             7  'current'
              608  LOAD_CONST               None
              611  COMPARE_OP            9  is-not
              614  JUMP_IF_FALSE        55  'to 672'
            617_0  THEN                     673
              617  POP_TOP          

 L. 262       618  LOAD_FAST             7  'current'
              621  LOAD_CONST               1
              624  BINARY_SUBSCR    
              625  LOAD_FAST             6  'new'
              628  LOAD_CONST               1
              631  BINARY_SUBSCR    
              632  COMPARE_OP            3  !=
              635  JUMP_IF_FALSE        27  'to 665'
              638  POP_TOP          

 L. 264       639  LOAD_GLOBAL          17  'logger'
              642  LOAD_ATTR            18  'error'
              645  LOAD_CONST               'Queue conflict on %s processing undos'
              648  LOAD_FAST             5  'uid'
              651  BINARY_MODULO    
              652  CALL_FUNCTION_1       1  None
              655  POP_TOP          

 L. 265       656  LOAD_GLOBAL          19  'ConflictError'
              659  RAISE_VARARGS_1       1  None
              662  JUMP_BACK           556  'to 556'
            665_0  COME_FROM           635  '635'
              665  POP_TOP          

 L. 267       666  CONTINUE            556  'to 556'
              669  JUMP_FORWARD          1  'to 673'
            672_0  COME_FROM           614  '614'
              672  POP_TOP          
            673_0  COME_FROM           669  '669'

 L. 269       673  LOAD_FAST             6  'new'
              676  LOAD_FAST             8  'committed_data'
              679  LOAD_FAST             5  'uid'
              682  STORE_SUBSCR     
              683  JUMP_BACK           556  'to 556'
              686  POP_BLOCK        
            687_0  COME_FROM           543  '543'

 L. 271       687  BUILD_MAP             0 
              690  DUP_TOP          
              691  LOAD_CONST               '_data'
              694  LOAD_FAST             8  'committed_data'
              697  ROT_THREE        
              698  STORE_SUBSCR     
              699  DUP_TOP          
              700  LOAD_CONST               '_conflict_policy'
              703  LOAD_FAST             9  'policy'
              706  ROT_THREE        
              707  STORE_SUBSCR     
              708  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 542


__doc__ = CatalogEventQueue.__doc__ + __doc__