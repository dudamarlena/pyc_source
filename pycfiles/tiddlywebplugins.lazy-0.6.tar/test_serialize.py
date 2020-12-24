# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/lazytiddlywebwiki/test/test_serialize.py
# Compiled at: 2011-04-19 11:42:11
from tiddlyweb.config import config
from tiddlywebwiki import init as twinit
from tiddlywebplugins.utils import get_store
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.serializer import Serializer

def setup_module(module):
    twinit(config)
    store = get_store(config)
    bag = Bag('test')
    store.put(bag)
    environ = {'tiddlyweb.config': config}
    tiddler = Tiddler('monkey', 'test')
    tiddler.text = 'I am uniquely999'
    store.put(tiddler)
    module.store = store
    module.lserializer = Serializer('tiddlywebplugins.lazy.serialization', environ)
    module.fserializer = Serializer('tiddlywebwiki.serialization', environ)


def test_lazy--- This code section failed: ---

 L.  32         0  LOAD_GENEXPR             '<code_object <genexpr>>'
                3  MAKE_FUNCTION_0       0  None
                6  LOAD_GLOBAL           0  'store'
                9  LOAD_ATTR             1  'list_bag_tiddlers'
               12  LOAD_GLOBAL           0  'store'
               15  LOAD_ATTR             2  'get'
               18  LOAD_GLOBAL           3  'Bag'
               21  LOAD_CONST               'test'
               24  CALL_FUNCTION_1       1  None
               27  CALL_FUNCTION_1       1  None
               30  CALL_FUNCTION_1       1  None
               33  GET_ITER         
               34  CALL_FUNCTION_1       1  None
               37  STORE_FAST            0  'tiddlers'

 L.  33        40  LOAD_CONST               ''
               43  LOAD_ATTR             4  'join'
               46  LOAD_GLOBAL           5  'lserializer'
               49  LOAD_ATTR             6  'list_tiddlers'
               52  LOAD_FAST             0  'tiddlers'
               55  CALL_FUNCTION_1       1  None
               58  CALL_FUNCTION_1       1  None
               61  STORE_FAST            1  'output'

 L.  34        64  LOAD_CONST               'I am uniquely999'
               67  LOAD_FAST             1  'output'
               70  COMPARE_OP            7  not-in
               73  POP_JUMP_IF_TRUE     82  'to 82'
               76  LOAD_ASSERT              AssertionError
               79  RAISE_VARARGS_1       1  None

 L.  36        82  LOAD_GENEXPR             '<code_object <genexpr>>'
               85  MAKE_FUNCTION_0       0  None
               88  LOAD_GLOBAL           0  'store'
               91  LOAD_ATTR             1  'list_bag_tiddlers'
               94  LOAD_GLOBAL           0  'store'
               97  LOAD_ATTR             2  'get'
              100  LOAD_GLOBAL           3  'Bag'
              103  LOAD_CONST               'test'
              106  CALL_FUNCTION_1       1  None
              109  CALL_FUNCTION_1       1  None
              112  CALL_FUNCTION_1       1  None
              115  GET_ITER         
              116  CALL_FUNCTION_1       1  None
              119  STORE_FAST            0  'tiddlers'

 L.  37       122  LOAD_CONST               ''
              125  LOAD_ATTR             4  'join'
              128  LOAD_GLOBAL           8  'fserializer'
              131  LOAD_ATTR             6  'list_tiddlers'
              134  LOAD_FAST             0  'tiddlers'
              137  CALL_FUNCTION_1       1  None
              140  CALL_FUNCTION_1       1  None
              143  STORE_FAST            1  'output'

 L.  38       146  LOAD_CONST               'I am uniquely999'
              149  LOAD_FAST             1  'output'
              152  COMPARE_OP            6  in
              155  POP_JUMP_IF_TRUE    167  'to 167'
              158  LOAD_ASSERT              AssertionError
              161  LOAD_FAST             1  'output'
              164  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 161