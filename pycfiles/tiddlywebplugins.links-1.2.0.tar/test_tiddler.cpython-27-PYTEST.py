# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.links/test/test_tiddler.py
# Compiled at: 2014-05-12 13:18:04
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlywebplugins.links import init
from tiddlywebplugins.links.parser import process_tiddler
from tiddlywebplugins.links.linksmanager import LinksManager
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.utils import get_store
from tiddlyweb.config import config
from tiddlyweb.web import serve
import os
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2

def setup_module(module):
    module.store = get_store(config)
    try:
        os.unlink('links.db')
    except OSError:
        pass

    environ = {'tiddlyweb.config': config}
    module.links_manager = LinksManager(environ=environ)
    try:
        shutil.rmtree('store')
    except:
        pass

    def app():
        return serve.load_app()

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app)
    module.store.put(Bag('cdent_public'))
    recipe = Recipe('cdent_public')
    recipe.set_recipe([('cdent_public', '')])
    module.store.put(recipe)
    init(config)


def test_simple_tiddler():
    tiddler = Tiddler('hello', 'barney')
    tiddler.text = 'I am NotYou, you [[are|you]]!'
    links = process_tiddler(tiddler)
    @py_assert0 = links[0]
    @py_assert3 = ('NotYou', None)
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = links[1]
    @py_assert3 = ('you', None)
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_space_only():
    tiddler = Tiddler('cow', 'barn')
    tiddler.text = '@cdent'
    links_manager.delete_links(tiddler)
    links_manager.update_database(tiddler)
    frontlinks = links_manager.read_frontlinks(tiddler)
    @py_assert0 = '@cdent:'
    @py_assert2 = @py_assert0 in frontlinks
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, frontlinks)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frontlinks) if 'frontlinks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frontlinks) else 'frontlinks'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_store_tiddler():
    tiddler = Tiddler('hello', 'barney')
    tiddler.text = 'I am NotYou, you [[are|you]]!'
    links_manager.delete_links(tiddler)
    links_manager.update_database(tiddler)
    frontlinks = links_manager.read_frontlinks(tiddler)
    @py_assert0 = 'barney:you'
    @py_assert2 = @py_assert0 in frontlinks
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, frontlinks)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frontlinks) if 'frontlinks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frontlinks) else 'frontlinks'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'barney:NotYou'
    @py_assert2 = @py_assert0 in frontlinks
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, frontlinks)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frontlinks) if 'frontlinks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frontlinks) else 'frontlinks'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('you', 'barney')
    backlinks = links_manager.read_backlinks(tiddler)
    @py_assert0 = 'barney:hello'
    @py_assert2 = @py_assert0 in backlinks
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, backlinks)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(backlinks) if 'backlinks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backlinks) else 'backlinks'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_stored_with_space--- This code section failed: ---

 L.  92         0  LOAD_GLOBAL           0  'store'
                3  LOAD_ATTR             1  'put'
                6  LOAD_GLOBAL           2  'Bag'
                9  LOAD_CONST               'barney'
               12  CALL_FUNCTION_1       1  None
               15  CALL_FUNCTION_1       1  None
               18  POP_TOP          

 L.  93        19  LOAD_GLOBAL           3  'Tiddler'
               22  LOAD_CONST               'hello'
               25  LOAD_CONST               'barney'
               28  CALL_FUNCTION_2       2  None
               31  STORE_FAST            0  'tiddler'

 L.  94        34  LOAD_CONST               'I am NotYou@cdent, http://burningchrome.com/'
               37  LOAD_FAST             0  'tiddler'
               40  STORE_ATTR            4  'text'

 L.  96        43  LOAD_GLOBAL           0  'store'
               46  LOAD_ATTR             1  'put'
               49  LOAD_FAST             0  'tiddler'
               52  CALL_FUNCTION_1       1  None
               55  POP_TOP          

 L.  98        56  LOAD_GLOBAL           5  'links_manager'
               59  LOAD_ATTR             6  'read_frontlinks'
               62  LOAD_FAST             0  'tiddler'
               65  CALL_FUNCTION_1       1  None
               68  STORE_FAST            1  'frontlinks'

 L.  99        71  LOAD_GLOBAL           7  'len'
               74  LOAD_FAST             1  'frontlinks'
               77  CALL_FUNCTION_1       1  None
               80  LOAD_CONST               2
               83  COMPARE_OP            2  ==
               86  POP_JUMP_IF_TRUE     98  'to 98'
               89  LOAD_ASSERT              AssertionError
               92  LOAD_FAST             1  'frontlinks'
               95  RAISE_VARARGS_2       2  None

 L. 101        98  LOAD_GLOBAL           3  'Tiddler'
              101  LOAD_CONST               'NotYou'
              104  LOAD_CONST               'cdent_public'
              107  CALL_FUNCTION_2       2  None
              110  STORE_FAST            0  'tiddler'

 L. 102       113  LOAD_GLOBAL           5  'links_manager'
              116  LOAD_ATTR             9  'read_backlinks'
              119  LOAD_FAST             0  'tiddler'
              122  CALL_FUNCTION_1       1  None
              125  STORE_FAST            2  'backlinks'

 L. 103       128  LOAD_GLOBAL           7  'len'
              131  LOAD_FAST             2  'backlinks'
              134  CALL_FUNCTION_1       1  None
              137  LOAD_CONST               1
              140  COMPARE_OP            2  ==
              143  POP_JUMP_IF_TRUE    155  'to 155'
              146  LOAD_ASSERT              AssertionError
              149  LOAD_FAST             2  'backlinks'
              152  RAISE_VARARGS_2       2  None

 L. 104       155  LOAD_CONST               'barney:hello'
              158  STORE_FAST            3  '@py_assert0'
              161  LOAD_FAST             3  '@py_assert0'
              164  LOAD_FAST             2  'backlinks'
              167  COMPARE_OP            6  in
              170  STORE_FAST            4  '@py_assert2'
              173  LOAD_FAST             4  '@py_assert2'
              176  POP_JUMP_IF_TRUE    328  'to 328'
              179  LOAD_GLOBAL          10  '@pytest_ar'
              182  LOAD_ATTR            11  '_call_reprcompare'
              185  LOAD_CONST               ('in',)
              188  LOAD_FAST             4  '@py_assert2'
              191  BUILD_TUPLE_1         1 
              194  LOAD_CONST               ('%(py1)s in %(py3)s',)
              197  LOAD_FAST             3  '@py_assert0'
              200  LOAD_FAST             2  'backlinks'
              203  BUILD_TUPLE_2         2 
              206  CALL_FUNCTION_4       4  None
              209  BUILD_MAP_2           2  None
              212  LOAD_GLOBAL          10  '@pytest_ar'
              215  LOAD_ATTR            12  '_saferepr'
              218  LOAD_FAST             3  '@py_assert0'
              221  CALL_FUNCTION_1       1  None
              224  LOAD_CONST               'py1'
              227  STORE_MAP        
              228  LOAD_CONST               'backlinks'
              231  LOAD_GLOBAL          13  '@py_builtins'
              234  LOAD_ATTR            14  'locals'
              237  CALL_FUNCTION_0       0  None
              240  COMPARE_OP            6  in
              243  POP_JUMP_IF_TRUE    261  'to 261'
              246  LOAD_GLOBAL          10  '@pytest_ar'
              249  LOAD_ATTR            15  '_should_repr_global_name'
              252  LOAD_FAST             2  'backlinks'
              255  CALL_FUNCTION_1       1  None
            258_0  COME_FROM           243  '243'
              258  POP_JUMP_IF_FALSE   276  'to 276'
              261  LOAD_GLOBAL          10  '@pytest_ar'
              264  LOAD_ATTR            12  '_saferepr'
              267  LOAD_FAST             2  'backlinks'
              270  CALL_FUNCTION_1       1  None
              273  JUMP_FORWARD          3  'to 279'
              276  LOAD_CONST               'backlinks'
            279_0  COME_FROM           273  '273'
              279  LOAD_CONST               'py3'
              282  STORE_MAP        
              283  BINARY_MODULO    
              284  STORE_FAST            5  '@py_format4'
              287  LOAD_CONST               'assert %(py5)s'
              290  BUILD_MAP_1           1  None
              293  LOAD_FAST             5  '@py_format4'
              296  LOAD_CONST               'py5'
              299  STORE_MAP        
              300  BINARY_MODULO    
              301  STORE_FAST            6  '@py_format6'
              304  LOAD_GLOBAL           8  'AssertionError'
              307  LOAD_GLOBAL          10  '@pytest_ar'
              310  LOAD_ATTR            16  '_format_explanation'
              313  LOAD_FAST             6  '@py_format6'
              316  CALL_FUNCTION_1       1  None
              319  CALL_FUNCTION_1       1  None
              322  RAISE_VARARGS_1       1  None
              325  JUMP_FORWARD          0  'to 328'
            328_0  COME_FROM           325  '325'
              328  LOAD_CONST               None
              331  DUP_TOP          
              332  STORE_FAST            3  '@py_assert0'
              335  STORE_FAST            4  '@py_assert2'
              338  LOAD_CONST               None
              341  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 338


def test_at_means_bag():
    store.put(Bag('spam'))
    tiddler = Tiddler('foo', 'spam')
    tiddler.text = 'I am AtCar@cdent, http://burningchrome.com/'
    config['links.at_means_bag'] = True
    store.put(tiddler)
    frontlinks = links_manager.read_frontlinks(tiddler)
    if not len(frontlinks) == 2:
        raise AssertionError, frontlinks
        @py_assert0 = 'cdent:AtCar'
        @py_assert2 = @py_assert0 in frontlinks
        @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, frontlinks)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frontlinks) if 'frontlinks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frontlinks) else 'frontlinks'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler.text = 'I am [[front man]]@[[back bag]], you know?'
    store.put(tiddler)
    frontlinks = links_manager.read_frontlinks(tiddler)
    if not len(frontlinks) == 1:
        raise AssertionError, frontlinks
        @py_assert0 = 'back bag:front man'
        @py_assert2 = @py_assert0 in frontlinks
        @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, frontlinks)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frontlinks) if 'frontlinks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frontlinks) else 'frontlinks'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    del config['links.at_means_bag']
    return


def test_web_front():
    bag = Bag('bagone')
    store.put(bag)
    tiddler = Tiddler('tiddlerone', 'bagone')
    tiddler.text = 'I am NotYou@cdent, http://burningchrome.com/'
    store.put(tiddler)
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/bags/bagone/tiddlers/tiddlerone/frontlinks.html')
    if not response['status'] == '200':
        raise AssertionError, content
        if not '<a href="/recipes/cdent_public/tiddlers/NotYou">NotYou</a>' in content:
            raise AssertionError, content
            bag = Bag('cdent_public')
            store.put(bag)
            tiddler = Tiddler('NotYou', 'cdent_public')
            tiddler.text = 'as BigPoo is'
            store.put(tiddler)
            response, content = http.request('http://0.0.0.0:8080/bags/cdent_public/tiddlers/NotYou/frontlinks')
            if not '<a href="/bags/cdent_public/tiddlers/BigPoo">BigPoo</a>' in content:
                raise AssertionError, content
                response, content = http.request('http://0.0.0.0:8080/bags/cdent_public/tiddlers/NotYou/backlinks')
                @py_assert0 = '<a href="/bags/barney/tiddlers/hello">hello</a>'
                @py_assert2 = @py_assert0 in content
                if not @py_assert2:
                    @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert0 = @py_assert2 = None
                @py_assert0 = '<a href="/bags/bagone/tiddlers/tiddlerone">tiddlerone</a>'
                @py_assert2 = @py_assert0 in content
                @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            response, content = http.request('http://0.0.0.0:8080/bags/barney/tiddlers/hello', method='DELETE')
            @py_assert0 = response['status']
            @py_assert3 = '204'
            @py_assert2 = @py_assert0 == @py_assert3
            @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        response, content = http.request('http://0.0.0.0:8080/bags/cdent_public/tiddlers/NotYou/backlinks')
        @py_assert0 = '<a href="/bags/barney/tiddlers/hello">hello</a>'
        @py_assert2 = @py_assert0 not in content
        @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_web_serialized--- This code section failed: ---

 L. 163         0  LOAD_GLOBAL           0  'httplib2'
                3  LOAD_ATTR             1  'Http'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            0  'http'

 L. 164        12  LOAD_FAST             0  'http'
               15  LOAD_ATTR             2  'request'
               18  LOAD_CONST               'http://0.0.0.0:8080/bags/cdent_public/tiddlers/NotYou/backlinks.json'
               21  CALL_FUNCTION_1       1  None
               24  UNPACK_SEQUENCE_2     2 
               27  STORE_FAST            1  'response'
               30  STORE_FAST            2  'content'

 L. 166        33  LOAD_FAST             1  'response'
               36  LOAD_CONST               'status'
               39  BINARY_SUBSCR    
               40  LOAD_CONST               '200'
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_TRUE     58  'to 58'
               49  LOAD_ASSERT              AssertionError
               52  LOAD_FAST             2  'content'
               55  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 52


def test_markdown():
    tiddler = Tiddler('hi', 'barney')
    tiddler.text = 'Hi\n==\n\nThis WikiWord and this [[Freelink|freelink]] and this BigOne@cdent in markdown\n'
    store.put(tiddler)
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/bags/barney/tiddlers/hi/frontlinks')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'href="/bags/barney/tiddlers/WikiWord">WikiWord</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'href="/bags/barney/tiddlers/freelink">freelink</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'href="/recipes/cdent_public/tiddlers/BigOne">BigOne</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return