# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.sqlalchemy/test/test_cascade.py
# Compiled at: 2012-12-31 08:56:35
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, py.test
from tiddlyweb.config import config
from tiddlyweb.store import Store, NoBagError, NoUserError, NoRecipeError, NoTiddlerError
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.sqlalchemy3.model import Base, sText, sTag, sTiddler, sRevision, sField

def setup_module(module):
    module.store = Store(config['server_store'][0], config['server_store'][1], {'tiddlyweb.config': config})
    Base.metadata.drop_all()
    Base.metadata.create_all()


def test_cascade():
    bag = Bag('holder')
    store.put(bag)
    tiddler = Tiddler('one', 'holder')
    tiddler.text = 'text'
    tiddler.tags = ['tag']
    tiddler.fields = {'fieldone': 'valueone'}
    store.put(tiddler)

    def count_em--- This code section failed: ---

 L.  35         0  LOAD_GLOBAL           0  'store'
                3  LOAD_ATTR             1  'storage'
                6  LOAD_ATTR             2  'session'
                9  LOAD_ATTR             3  'query'
               12  LOAD_GLOBAL           4  'sText'
               15  CALL_FUNCTION_1       1  None
               18  LOAD_ATTR             5  'count'
               21  CALL_FUNCTION_0       0  None
               24  STORE_FAST            2  'text_count'

 L.  36        27  LOAD_GLOBAL           0  'store'
               30  LOAD_ATTR             1  'storage'
               33  LOAD_ATTR             2  'session'
               36  LOAD_ATTR             3  'query'
               39  LOAD_GLOBAL           6  'sTag'
               42  CALL_FUNCTION_1       1  None
               45  LOAD_ATTR             5  'count'
               48  CALL_FUNCTION_0       0  None
               51  STORE_FAST            3  'tag_count'

 L.  37        54  LOAD_GLOBAL           0  'store'
               57  LOAD_ATTR             1  'storage'
               60  LOAD_ATTR             2  'session'
               63  LOAD_ATTR             3  'query'
               66  LOAD_GLOBAL           7  'sTiddler'
               69  CALL_FUNCTION_1       1  None
               72  LOAD_ATTR             5  'count'
               75  CALL_FUNCTION_0       0  None
               78  STORE_FAST            4  'tiddler_count'

 L.  38        81  LOAD_GLOBAL           0  'store'
               84  LOAD_ATTR             1  'storage'
               87  LOAD_ATTR             2  'session'
               90  LOAD_ATTR             3  'query'
               93  LOAD_GLOBAL           8  'sRevision'
               96  CALL_FUNCTION_1       1  None
               99  LOAD_ATTR             5  'count'
              102  CALL_FUNCTION_0       0  None
              105  STORE_FAST            5  'revision_count'

 L.  39       108  LOAD_GLOBAL           0  'store'
              111  LOAD_ATTR             1  'storage'
              114  LOAD_ATTR             2  'session'
              117  LOAD_ATTR             3  'query'
              120  LOAD_GLOBAL           9  'sField'
              123  CALL_FUNCTION_1       1  None
              126  LOAD_ATTR             5  'count'
              129  CALL_FUNCTION_0       0  None
              132  STORE_FAST            6  'field_count'

 L.  40       135  LOAD_GLOBAL           0  'store'
              138  LOAD_ATTR             1  'storage'
              141  LOAD_ATTR             2  'session'
              144  LOAD_ATTR            10  'commit'
              147  CALL_FUNCTION_0       0  None
              150  POP_TOP          

 L.  42       151  LOAD_CONST               '%s, but got: text: %s, tag: %s, tiddler: %s, revision: %s, field: %s'

 L.  43       154  LOAD_FAST             1  'message'
              157  LOAD_FAST             2  'text_count'
              160  LOAD_FAST             3  'tag_count'

 L.  44       163  LOAD_FAST             4  'tiddler_count'
              166  LOAD_FAST             5  'revision_count'
              169  LOAD_FAST             6  'field_count'
              172  BUILD_TUPLE_6         6 
              175  BINARY_MODULO    
              176  STORE_FAST            1  'message'

 L.  46       179  LOAD_FAST             2  'text_count'
              182  LOAD_FAST             3  'tag_count'
              185  DUP_TOP          
              186  ROT_THREE        
              187  COMPARE_OP            2  ==
              190  JUMP_IF_FALSE_OR_POP   235  'to 235'
              193  LOAD_FAST             4  'tiddler_count'
              196  DUP_TOP          
              197  ROT_THREE        
              198  COMPARE_OP            2  ==
              201  JUMP_IF_FALSE_OR_POP   235  'to 235'

 L.  47       204  LOAD_FAST             5  'revision_count'
              207  DUP_TOP          
              208  ROT_THREE        
              209  COMPARE_OP            2  ==
              212  JUMP_IF_FALSE_OR_POP   235  'to 235'
              215  LOAD_FAST             6  'field_count'
              218  DUP_TOP          
              219  ROT_THREE        
              220  COMPARE_OP            2  ==
              223  JUMP_IF_FALSE_OR_POP   235  'to 235'
              226  LOAD_FAST             0  'count'
              229  COMPARE_OP            2  ==
              232  JUMP_FORWARD          2  'to 237'
            235_0  COME_FROM           223  '223'
            235_1  COME_FROM           212  '212'
            235_2  COME_FROM           201  '201'
            235_3  COME_FROM           190  '190'
              235  ROT_TWO          
              236  POP_TOP          
            237_0  COME_FROM           232  '232'
              237  POP_JUMP_IF_TRUE    249  'to 249'
              240  LOAD_ASSERT              AssertionError
              243  LOAD_FAST             1  'message'
              246  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 243

    count_em(1, '1 row for the tiddler everywhere')
    store.delete(tiddler)
    count_em(0, '0 rows for the tiddler everywhere')