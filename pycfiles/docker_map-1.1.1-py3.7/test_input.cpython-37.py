# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_input.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 22212 bytes
from __future__ import absolute_import, unicode_literals
import unittest, six
from dockermap.functional import lazy_once
from dockermap.utils import merge_list
from dockermap.map.config.main import ContainerMap
from dockermap.map.config.utils import expand_groups, get_map_config_ids
from dockermap.map.input import is_path, read_only, get_list, ItemType, SharedHostVolumesList, SharedVolume, HostVolume, ContainerLinkList, ContainerLink, PortBindingList, PortBinding, ExecCommandList, ExecCommand, ExecPolicy, NetworkEndpointList, NetworkEndpoint, AttachedVolumeList, UsedVolume, InputConfigIdList, MapConfigId, InputConfigId, get_healthcheck, HealthCheck

class InputConversionTest(unittest.TestCase):

    def test_is_path(self):
        self.assertFalse(is_path(None))
        self.assertFalse(is_path(''))
        self.assertFalse(is_path('.'))
        self.assertFalse(is_path('test'))
        self.assertTrue(is_path('/'))
        self.assertTrue(is_path('/test'))
        self.assertTrue(is_path('./'))
        self.assertTrue(is_path('./test'))

    def test_read_only(self):
        self.assertFalse(read_only(None))
        self.assertFalse(read_only(''))
        self.assertFalse(read_only(0))
        self.assertFalse(read_only('rw'))
        self.assertTrue(read_only('ro'))
        self.assertTrue(read_only(1))
        self.assertTrue(read_only('test'))

    def test_get_list(self):
        self.assertEqual(get_list(()), [])
        self.assertEqual(get_list(None), [])
        self.assertEqual(get_list(lazy_once(lambda : 'test')), ['test'])
        self.assertEqual(get_list('test'), ['test'])

    def test_get_shared_host_volume(self):
        l = SharedHostVolumesList()
        assert_a = lambda a: self.assertEqual(l.get_type_item(a), SharedVolume('a', False))
        assert_b = lambda b: self.assertEqual(l.get_type_item(b), SharedVolume('b', True))
        assert_c = lambda c: self.assertEqual(l.get_type_item(c), HostVolume('c', 'ch', False))
        assert_d = lambda d: self.assertEqual(l.get_type_item(d), HostVolume('d', 'dh', True))
        assert_a('a')
        assert_a(('a', ))
        assert_a(['a', False])
        assert_b(SharedVolume('b', True))
        assert_b(('b', 'ro'))
        assert_b({'b': 'ro'})
        assert_c(('c', 'ch'))
        assert_c(('c', 'ch', False))
        assert_c(('c', ['ch']))
        assert_c(('c', ('ch', 'rw')))
        assert_c({'c': 'ch'})
        assert_c({'c': ('ch', )})
        assert_d(('d', 'dh', 'ro'))
        assert_d({'d': ('dh', True)})

    def test_get_shared_host_volumes(self):
        assert_a = lambda a: self.assertEqual(SharedHostVolumesList(a), [SharedVolume('a', False)])
        assert_b = lambda b: six.assertCountEqual(self, SharedHostVolumesList(b), [SharedVolume('a', False),
         SharedVolume('b', True),
         HostVolume('c', 'ch', False),
         HostVolume('d', 'dh', True)])
        assert_a('a')
        assert_a([('a', )])
        assert_a((['a', False],))
        assert_b([['a'], SharedVolume('b', True), ('c', 'ch'), ('d', 'dh', 'ro')])
        assert_b(['a', ('b', 'ro'), ('c', ['ch']), ('d', 'dh', True)])
        assert_b({'a':False,  'b':'ro',  'c':'ch',  'd':('dh', True)})

    def test_get_attached_volume(self):
        l = AttachedVolumeList()
        assert_a = lambda a: self.assertEqual(l.get_type_item(a), SharedVolume('a', False))
        assert_c = lambda c: self.assertEqual(l.get_type_item(c), UsedVolume('c', 'p1', False))
        assert_a(SharedVolume('a', False))
        assert_a('a')
        assert_a(('a', ))
        assert_a({'name': 'a'})
        assert_c(UsedVolume('c', 'p1'))
        assert_c(('c', 'p1'))
        assert_c({'c': 'p1'})
        assert_c({'name':'c',  'path':'p1'})

    def test_get_attached_volumes(self):
        assert_a = lambda a: self.assertEqual(AttachedVolumeList(a), [SharedVolume('a', False)])
        assert_b = lambda b: six.assertCountEqual(self, AttachedVolumeList(b), [SharedVolume('a', False),
         SharedVolume('b', False),
         UsedVolume('c', 'p1', False)])
        assert_a(SharedVolume('a', False))
        assert_a('a')
        assert_a(('a', ))
        assert_a([{'name': 'a'}])
        assert_b(['a', ('b', False), {'c': 'p1'}])
        assert_b({'a':False,  'b':None,  'c':'p1'})
        assert_b({'a':False,  'b':None,  'c':'p1'})
        assert_b((SharedVolume('a'), {'name':'b',  'readonly':False}, {'name':'c',  'path':'p1'}))

    def test_get_used_volume(self):
        pass

    def test_get_used_volumes(self):
        pass

    def test_get_container_link(self):
        l = ContainerLinkList()
        assert_a = lambda a: self.assertEqual(l.get_type_item(a), ContainerLink('a', None))
        assert_b = lambda b: self.assertEqual(l.get_type_item(b), ContainerLink('b', 'b_'))
        assert_a('a')
        assert_a(('a', ))
        assert_a({'container': 'a'})
        assert_a(['a', None])
        assert_b(('b', 'b_'))
        assert_b({'container':'b',  'alias':'b_'})

    def test_get_container_links(self):
        assert_a = lambda a: self.assertEqual(ContainerLinkList(a), [ContainerLink('a', None)])
        assert_b = lambda b: six.assertCountEqual(self, ContainerLinkList(b), [ContainerLink('a', None),
         ContainerLink('b', 'b_')])
        assert_a('a')
        assert_a((ContainerLink('a'),))
        assert_a({'a': None})
        assert_a(({'container': 'a'},))
        assert_a([('a', )])
        assert_b(('a', ('b', 'b_')))
        assert_b({'a':None,  'b':'b_'})
        assert_b([{'container': 'a'}, {'container':'b',  'alias':'b_'}])

    def test_get_port_binding(self):
        l = PortBindingList()
        assert_a = lambda a: self.assertEqual(l.get_type_item(a), PortBinding('1234'))
        assert_b = lambda b: self.assertEqual(l.get_type_item(b), PortBinding(1234, 1234))
        assert_c = lambda c: self.assertEqual(l.get_type_item(c), PortBinding(1234, 1234, '0.0.0.0'))
        assert_d = lambda d: self.assertEqual(l.get_type_item(d), PortBinding(1234, 1234, '0.0.0.0', True))
        assert_a('1234')
        assert_a(('1234', ))
        assert_a(['1234', None])
        assert_a({'exposed_port': '1234'})
        assert_b((1234, lazy_once(lambda : 1234)))
        assert_c((1234, 1234, '0.0.0.0'))
        assert_c((1234, [1234, '0.0.0.0']))
        assert_d((1234, 1234, '0.0.0.0', True))
        assert_d(dict(exposed_port=1234, host_port=1234, interface='0.0.0.0', ipv6=True))
        assert_d((1234, [1234, '0.0.0.0', True]))

    def test_get_port_bindings(self):
        assert_a = lambda a: self.assertEqual(PortBindingList(a), [PortBinding('1234')])
        assert_b = lambda b: six.assertCountEqual(self, PortBindingList(b), [PortBinding('1234'),
         PortBinding(1234, 1234),
         PortBinding(1235, 1235, '0.0.0.0', True)])
        assert_a('1234')
        assert_a(PortBinding('1234', None, None, False))
        assert_a((['1234'],))
        assert_b(['1234', (1234, 1234), (1235, 1235, '0.0.0.0', True)])
        assert_b([('1234', [None, None]), PortBinding(1234, 1234), (1235, [1235, '0.0.0.0', True])])
        assert_b({'1234':None,  1234:1234,  1235:(1235, '0.0.0.0', True)})
        assert_b({'1234':None,  1234:dict(host_port=1234),  1235:dict(host_port=1235, interface='0.0.0.0', ipv6=True)})

    def test_get_exec_command(self):
        l = ExecCommandList()
        assert_a = lambda a: self.assertEqual(l.get_type_item(a), ExecCommand('a b c', None, ExecPolicy.RESTART))
        assert_b = lambda b: self.assertEqual(l.get_type_item(b), ExecCommand(['a', 'b', 'c'], None, ExecPolicy.RESTART))
        assert_c = lambda c: self.assertEqual(l.get_type_item(c), ExecCommand('a b c', 'user', ExecPolicy.RESTART))
        assert_d = lambda d: self.assertEqual(l.get_type_item(d), ExecCommand(['a', 'b', 'c'], 'user', ExecPolicy.RESTART))
        assert_e = lambda e: self.assertEqual(l.get_type_item(e), ExecCommand('a b c', 'user', ExecPolicy.INITIAL))
        assert_f = lambda f: self.assertEqual(l.get_type_item(f), ExecCommand(['a', 'b', 'c'], 'user', ExecPolicy.INITIAL))
        assert_a('a b c')
        assert_a(('a b c', ))
        assert_a(['a b c', None])
        assert_a(lazy_once(lambda : 'a b c'))
        assert_b((['a', 'b', 'c'],))
        assert_b([['a', 'b', 'c'], None])
        assert_c(('a b c', 'user'))
        assert_c([lazy_once(lambda : 'a b c'), lazy_once(lambda : 'user')])
        assert_d((['a', 'b', 'c'], 'user'))
        assert_d([lazy_once(lambda : ['a', 'b', 'c']), lazy_once(lambda : 'user')])
        assert_e(('a b c', 'user', ExecPolicy.INITIAL))
        assert_e([lazy_once(lambda : 'a b c'), lazy_once(lambda : 'user'), ExecPolicy.INITIAL])
        assert_f((['a', 'b', 'c'], 'user', ExecPolicy.INITIAL))
        assert_f([lazy_once(lambda : ['a', 'b', 'c']), lazy_once(lambda : 'user'), ExecPolicy.INITIAL])
        assert_f({'cmd':['a', 'b', 'c'],  'user':'user',  'policy':ExecPolicy.INITIAL})

    def test_get_exec_commmands(self):
        assert_a = lambda a: self.assertEqual(ExecCommandList(a), [ExecCommand('a b c', None, ExecPolicy.RESTART)])
        assert_b = lambda b: six.assertCountEqual(self, ExecCommandList(b), [
         ExecCommand(['a', 'b', 'c'], None, ExecPolicy.RESTART),
         ExecCommand('a b c', 'user', ExecPolicy.RESTART),
         ExecCommand(['a', 'b', 'c'], 'root', ExecPolicy.INITIAL)])
        assert_a('a b c')
        assert_a([ExecCommand('a b c', None, ExecPolicy.RESTART)])
        assert_a(['a b c'])
        assert_a(({'cmd': 'a b c'},))
        assert_b([(['a', 'b', 'c'],), ('a b c', 'user'), [['a', 'b', 'c'], 'root', ExecPolicy.INITIAL]])
        assert_b([(['a', 'b', 'c'], None),
         {'cmd':'a b c', 
          'user':'user',  'policy':ExecPolicy.RESTART},
         [
          [
           'a', 'b', 'c'], 'root', ExecPolicy.INITIAL]])

    def test_get_network_endpoint(self):
        l = NetworkEndpointList()
        assert_e1 = lambda v: self.assertEqual(l.get_type_item(v), NetworkEndpoint('endpoint1'))
        assert_e2 = lambda v: self.assertEqual(l.get_type_item(v), NetworkEndpoint('endpoint2', ['alias1']))
        assert_e3 = lambda v: self.assertEqual(l.get_type_item(v), NetworkEndpoint('endpoint3', ['alias1'], ipv4_address='0.0.0.0'))
        assert_e1('endpoint1')
        assert_e1(['endpoint1'])
        assert_e1({'endpoint1': ''})
        assert_e1({'network_name': 'endpoint1'})
        assert_e2(['endpoint2', 'alias1'])
        assert_e2({'endpoint2': 'alias1'})
        assert_e2(['endpoint2', dict(aliases='alias1')])
        assert_e2(['endpoint2', ('alias1', )])
        assert_e2({'endpoint2': 'alias1'})
        assert_e2({'endpoint2': ('alias1', )})
        assert_e2({'endpoint2': dict(aliases='alias1')})
        assert_e2({'endpoint2': dict(aliases=('alias1', ))})
        assert_e2({'network_name':'endpoint2',  'aliases':'alias1'})
        assert_e2({'network_name':'endpoint2',  'aliases':('alias1', )})
        assert_e3(['endpoint3', 'alias1', None, '0.0.0.0'])
        assert_e3({'endpoint3': ('alias1', None, '0.0.0.0')})
        assert_e3(['endpoint3', dict(aliases='alias1', ipv4_address='0.0.0.0')])
        assert_e3({'endpoint3': dict(aliases='alias1', ipv4_address='0.0.0.0')})
        assert_e3(dict(network_name='endpoint3', aliases='alias1', ipv4_address='0.0.0.0'))

    def test_get_network_endpoints(self):
        assert_e1 = lambda v: self.assertEqual(NetworkEndpointList(v), [NetworkEndpoint('endpoint1')])
        assert_e2 = lambda v: six.assertCountEqual(self, NetworkEndpointList(v), [
         NetworkEndpoint('endpoint2', ['alias1']),
         NetworkEndpoint('endpoint3', ['alias1'], ipv4_address='0.0.0.0')])
        assert_e1('endpoint1')
        assert_e1(['endpoint1'])
        assert_e1({'endpoint1': None})
        assert_e1(({'network_name': 'endpoint1'},))
        assert_e2([
         ('endpoint2', 'alias1'),
         [
          'endpoint3', 'alias1', None, '0.0.0.0']])
        assert_e2([
         ('endpoint2', 'alias1'),
         [
          'endpoint3', 'alias1', None, '0.0.0.0']])
        assert_e2([
         (
          'endpoint2', dict(aliases='alias1')),
         [
          'endpoint3', dict(aliases=('alias1', ), ipv4_address='0.0.0.0')]])
        assert_e2([
         dict(network_name='endpoint2', aliases='alias1'),
         dict(network_name='endpoint3', aliases=('alias1', ), ipv4_address='0.0.0.0')])

    def test_get_healthcheck(self):
        assert_h1 = lambda v: self.assertEqual(get_healthcheck(v), HealthCheck(['CMD', 'test'], 10000, 1000000000, 3, 60000000000))
        assert_h2 = lambda v: self.assertEqual(get_healthcheck(v), HealthCheck(['CMD-SHELL', 'test2'], 10000, 1000000, 1))
        assert_h1([['test'], '10us', '1000 ms', 3, '1m'])
        assert_h1({'test':[
          'CMD', 'test'], 
         'interval':'10000 ns', 
         'timeout':'1000ms', 
         'retries':3, 
         'start_period':'1m'})
        assert_h2((['CMD-SHELL', 'test2'], '10 us', '1ms', 1))
        self.assertEqual(HealthCheck('NONE')._asdict(), {'test': None})

    def test_get_input_config_id--- This code section failed: ---

 L. 299         0  LOAD_GLOBAL              InputConfigIdList
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_DEREF              'l'

 L. 300         6  LOAD_CONST               (None, None)
                8  LOAD_CLOSURE             'l'
               10  LOAD_CLOSURE             'self'
               12  BUILD_TUPLE_2         2 
               14  LOAD_LAMBDA              '<code_object <lambda>>'
               16  LOAD_STR                 'InputConversionTest.test_get_input_config_id.<locals>.<lambda>'
               18  MAKE_FUNCTION_9          'default, closure'
               20  STORE_FAST               'assert_a'

 L. 302        22  LOAD_CONST               (None, None)
               24  LOAD_CLOSURE             'l'
               26  LOAD_CLOSURE             'self'
               28  BUILD_TUPLE_2         2 
               30  LOAD_LAMBDA              '<code_object <lambda>>'
               32  LOAD_STR                 'InputConversionTest.test_get_input_config_id.<locals>.<lambda>'
               34  MAKE_FUNCTION_9          'default, closure'
               36  STORE_FAST               'assert_b'

 L. 304        38  LOAD_CONST               (None, None)
               40  LOAD_CLOSURE             'l'
               42  LOAD_CLOSURE             'self'
               44  BUILD_TUPLE_2         2 
               46  LOAD_LAMBDA              '<code_object <lambda>>'
               48  LOAD_STR                 'InputConversionTest.test_get_input_config_id.<locals>.<lambda>'
               50  MAKE_FUNCTION_9          'default, closure'
               52  STORE_FAST               'assert_c'

 L. 306        54  LOAD_CONST               (None, None)
               56  LOAD_CLOSURE             'l'
               58  LOAD_CLOSURE             'self'
               60  BUILD_TUPLE_2         2 
               62  LOAD_LAMBDA              '<code_object <lambda>>'
               64  LOAD_STR                 'InputConversionTest.test_get_input_config_id.<locals>.<lambda>'
               66  MAKE_FUNCTION_9          'default, closure'
               68  STORE_FAST               'assert_d'

 L. 308        70  LOAD_FAST                'assert_a'
               72  LOAD_STR                 'm.c'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  POP_TOP          

 L. 309        78  LOAD_FAST                'assert_a'
               80  LOAD_STR                 'm.c'
               82  LOAD_STR                 'x'
               84  CALL_FUNCTION_2       2  '2 positional arguments'
               86  POP_TOP          

 L. 310        88  LOAD_FAST                'assert_a'
               90  LOAD_STR                 'm.c.'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  POP_TOP          

 L. 311        96  LOAD_FAST                'assert_a'
               98  LOAD_CONST               ('m', 'c', None)
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  POP_TOP          

 L. 312       104  LOAD_FAST                'assert_a'
              106  LOAD_STR                 'm'
              108  LOAD_STR                 'c'
              110  BUILD_LIST_2          2 
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  POP_TOP          

 L. 313       116  LOAD_FAST                'assert_a'
              118  LOAD_STR                 'm'
              120  LOAD_STR                 'c'
              122  BUILD_LIST_0          0 
              124  BUILD_LIST_3          3 
              126  LOAD_STR                 'x'
              128  CALL_FUNCTION_2       2  '2 positional arguments'
              130  POP_TOP          

 L. 314       132  LOAD_FAST                'assert_a'
              134  LOAD_STR                 'c'
              136  LOAD_STR                 'm'
              138  CALL_FUNCTION_2       2  '2 positional arguments'
              140  POP_TOP          

 L. 315       142  LOAD_FAST                'assert_a'
              144  LOAD_STR                 'c'
              146  BUILD_LIST_1          1 
              148  LOAD_STR                 'm'
              150  CALL_FUNCTION_2       2  '2 positional arguments'
              152  POP_TOP          

 L. 316       154  LOAD_FAST                'assert_a'
              156  LOAD_GLOBAL              dict
              158  LOAD_STR                 'c'
              160  LOAD_STR                 'm'
              162  LOAD_CONST               ('config_name', 'map_name')
              164  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              166  CALL_FUNCTION_1       1  '1 positional argument'
              168  POP_TOP          

 L. 317       170  LOAD_FAST                'assert_a'
              172  LOAD_GLOBAL              dict
              174  LOAD_STR                 'c'
              176  LOAD_CONST               ('config_name',)
              178  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              180  LOAD_STR                 'm'
              182  CALL_FUNCTION_2       2  '2 positional arguments'
              184  POP_TOP          

 L. 318       186  LOAD_FAST                'assert_b'
              188  LOAD_STR                 'm.c.i'
              190  CALL_FUNCTION_1       1  '1 positional argument'
              192  POP_TOP          

 L. 319       194  LOAD_FAST                'assert_b'
              196  LOAD_STR                 'm.c.i'
              198  LOAD_STR                 'x'
              200  LOAD_STR                 'j'
              202  CALL_FUNCTION_3       3  '3 positional arguments'
              204  POP_TOP          

 L. 320       206  LOAD_FAST                'assert_b'
              208  LOAD_CONST               ('m', 'c', 'i')
              210  CALL_FUNCTION_1       1  '1 positional argument'
              212  POP_TOP          

 L. 321       214  LOAD_FAST                'assert_b'
              216  LOAD_STR                 'm'
              218  LOAD_STR                 'c'
              220  LOAD_STR                 'i'
              222  BUILD_LIST_3          3 
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  POP_TOP          

 L. 322       228  LOAD_FAST                'assert_b'
              230  LOAD_STR                 'm'
              232  LOAD_STR                 'c'
              234  LOAD_CONST               ('i',)
              236  BUILD_LIST_3          3 
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  POP_TOP          

 L. 323       242  LOAD_FAST                'assert_b'
              244  LOAD_CONST               ('m', 'c', ('i',))
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  POP_TOP          

 L. 324       250  LOAD_FAST                'assert_b'
              252  LOAD_CONST               ('m', 'c')
              254  LOAD_CONST               ('i',)
              256  LOAD_CONST               ('i',)
              258  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              260  POP_TOP          

 L. 325       262  LOAD_FAST                'assert_b'
              264  LOAD_STR                 'c'
              266  LOAD_STR                 'm'
              268  LOAD_CONST               ('i',)
              270  CALL_FUNCTION_3       3  '3 positional arguments'
              272  POP_TOP          

 L. 326       274  LOAD_FAST                'assert_b'
              276  LOAD_CONST               ('c',)
              278  LOAD_STR                 'm'
              280  LOAD_CONST               ('i',)
              282  CALL_FUNCTION_3       3  '3 positional arguments'
              284  POP_TOP          

 L. 327       286  LOAD_FAST                'assert_b'
              288  LOAD_GLOBAL              dict
              290  LOAD_STR                 'c'
              292  LOAD_STR                 'm'
              294  LOAD_CONST               ('i',)
              296  LOAD_CONST               ('config_name', 'map_name', 'instance_names')
              298  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              300  CALL_FUNCTION_1       1  '1 positional argument'
              302  POP_TOP          

 L. 328       304  LOAD_FAST                'assert_c'
              306  LOAD_STR                 'm'
              308  LOAD_STR                 'c'
              310  LOAD_CONST               ('i', 'j')
              312  BUILD_LIST_3          3 
              314  CALL_FUNCTION_1       1  '1 positional argument'
              316  POP_TOP          

 L. 329       318  LOAD_FAST                'assert_c'
              320  LOAD_STR                 'm'
              322  LOAD_STR                 'c'
              324  LOAD_STR                 'i'
              326  LOAD_STR                 'j'
              328  BUILD_LIST_2          2 
              330  BUILD_TUPLE_3         3 
              332  CALL_FUNCTION_1       1  '1 positional argument'
              334  POP_TOP          

 L. 330       336  LOAD_FAST                'assert_c'
              338  LOAD_CONST               ('m', 'c')
              340  LOAD_CONST               ('i', 'j')
              342  LOAD_CONST               ('i',)
              344  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              346  POP_TOP          

 L. 331       348  LOAD_FAST                'assert_c'
              350  LOAD_STR                 'c'
              352  LOAD_STR                 'm'
              354  LOAD_CONST               ('i', 'j')
              356  CALL_FUNCTION_3       3  '3 positional arguments'
              358  POP_TOP          

 L. 332       360  LOAD_FAST                'assert_c'
              362  LOAD_CONST               ('c',)
              364  LOAD_STR                 'm'
              366  LOAD_CONST               ('i', 'j')
              368  CALL_FUNCTION_3       3  '3 positional arguments'
              370  POP_TOP          

 L. 333       372  LOAD_FAST                'assert_c'
              374  LOAD_GLOBAL              dict
              376  LOAD_STR                 'c'
              378  LOAD_STR                 'm'
              380  LOAD_CONST               ('i', 'j')
              382  LOAD_CONST               ('config_name', 'map_name', 'instance_names')
              384  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              386  CALL_FUNCTION_1       1  '1 positional argument'
              388  POP_TOP          

 L. 334       390  LOAD_FAST                'assert_c'
              392  LOAD_GLOBAL              dict
              394  LOAD_STR                 'c'
              396  LOAD_CONST               ('config_name',)
              398  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              400  LOAD_STR                 'm'
              402  LOAD_CONST               ('i', 'j')
              404  CALL_FUNCTION_3       3  '3 positional arguments'
              406  POP_TOP          

 L. 335       408  LOAD_FAST                'assert_d'
              410  LOAD_GLOBAL              dict
              412  LOAD_STR                 'network'
              414  LOAD_STR                 'n'
              416  LOAD_CONST               ('config_type', 'config_name')
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  LOAD_STR                 'm'
              422  CALL_FUNCTION_2       2  '2 positional arguments'
              424  POP_TOP          

Parse error at or near `MAKE_FUNCTION_9' instruction at offset 18

    def test_get_input_config_ids(self):
        map_m = ContainerMap('m', c=dict(instances=['i']), d=dict(instances=['i']), groups=dict(default=['c.i', 'd.i']))
        map_n = ContainerMap('n', e={}, networks=dict(nn1={}), groups=dict(default=['e']))
        maps = {'m':map_m,  'n':map_n}

        def assert_a(v, m=None, i=None):
            self.assertEqual(InputConfigIdList(v, map_name=m, instances=i), [
             InputConfigId(ItemType.CONTAINER, 'm', 'c')])
            self.assertEqual(get_map_config_ids(v, maps, default_map_name=m, default_instances=i), [
             MapConfigId(ItemType.CONTAINER, 'm', 'c', 'i')])

        def assert_b(v, m=None, i=None):
            six.assertCountEqual(self, InputConfigIdList(v, map_name=m, instances=i), [
             InputConfigId(ItemType.CONTAINER, 'm', 'c', ('i', )),
             InputConfigId(ItemType.CONTAINER, 'm', 'd', ('i', )),
             InputConfigId(ItemType.CONTAINER, 'n', 'e', ('i', 'j'))])
            six.assertCountEqual(self, get_map_config_ids(v, maps, default_map_name=m, default_instances=i), [
             MapConfigId(ItemType.CONTAINER, 'm', 'c', 'i'),
             MapConfigId(ItemType.CONTAINER, 'm', 'd', 'i'),
             MapConfigId(ItemType.CONTAINER, 'n', 'e', 'i'),
             MapConfigId(ItemType.CONTAINER, 'n', 'e', 'j')])

        def assert_c(v, m=None, i=None):
            six.assertCountEqual(self, expand_groups(InputConfigIdList(v, map_name=m, instances=i), maps), [
             InputConfigId(ItemType.CONTAINER, 'm', 'c', ('i', )),
             InputConfigId(ItemType.CONTAINER, 'm', 'd', ('i', )),
             InputConfigId(ItemType.CONTAINER, 'n', 'e', ('i', )),
             InputConfigId(ItemType.CONTAINER, 'n', 'e', ('j', ))])
            six.assertCountEqual(self, get_map_config_ids(v, maps, default_map_name=m, default_instances=i), [
             MapConfigId(ItemType.CONTAINER, 'm', 'c', 'i'),
             MapConfigId(ItemType.CONTAINER, 'm', 'd', 'i'),
             MapConfigId(ItemType.CONTAINER, 'n', 'e', 'i'),
             MapConfigId(ItemType.CONTAINER, 'n', 'e', 'j')])

        def assert_d(v, m=None, i=None):
            six.assertCountEqual(self, expand_groups(InputConfigIdList(v, map_name=m, instances=i), maps), [
             InputConfigId(ItemType.NETWORK, 'n', 'nn1')])
            six.assertCountEqual(self, get_map_config_ids(v, maps, default_map_name=m, default_instances=i), [
             MapConfigId(ItemType.NETWORK, 'n', 'nn1')])

        assert_a('m.c')
        assert_a('c', 'm')
        assert_a('c', 'm', [])
        assert_a([['m', 'c']])
        assert_b(['m.c.',
         'd',
         (
          'n', 'e', ['i', 'j'])], 'm', 'i')
        assert_b([[None, 'c'],
         ('d', ),
         [
          'n', 'e', ('i', 'j')]], 'm', ('i', ))
        assert_c(['m.default', 'n.default', 'n.e.j'], None, ('i', ))
        assert_d([dict(config_type='network', config_name='nn1', map_name='n')])
        assert_d([dict(config_type='network', config_name='nn1')], 'n')

    def test_get_map_config_ids_all_alias(self):
        map_m = ContainerMap('m', c1=(dict()), c2=(dict()), c3=(dict()), groups=dict(default=['c3']))
        map_n = ContainerMap('n', c1=(dict()), c3=(dict()), groups=dict(default=['c3']))
        maps = {'m':map_m,  'n':map_n}
        six.assertCountEqual(self, get_map_config_ids('m.__all__', maps), [
         MapConfigId(ItemType.CONTAINER, 'm', 'c1'),
         MapConfigId(ItemType.CONTAINER, 'm', 'c2'),
         MapConfigId(ItemType.CONTAINER, 'm', 'c3')])
        six.assertCountEqual(self, get_map_config_ids('__all__.__all__', maps), [
         MapConfigId(ItemType.CONTAINER, 'm', 'c1'),
         MapConfigId(ItemType.CONTAINER, 'm', 'c2'),
         MapConfigId(ItemType.CONTAINER, 'm', 'c3'),
         MapConfigId(ItemType.CONTAINER, 'n', 'c1'),
         MapConfigId(ItemType.CONTAINER, 'n', 'c3')])
        six.assertCountEqual(self, get_map_config_ids('__all__.c1', maps), [
         MapConfigId(ItemType.CONTAINER, 'm', 'c1'),
         MapConfigId(ItemType.CONTAINER, 'n', 'c1')])
        six.assertCountEqual(self, get_map_config_ids('__all__.default', maps), [
         MapConfigId(ItemType.CONTAINER, 'm', 'c3'),
         MapConfigId(ItemType.CONTAINER, 'n', 'c3')])

    def test_merge_list(self):
        list1 = [
         'a', 'b', 'c']
        merge_list(list1, ['d'])
        self.assertListEqual(list1, ['a', 'b', 'c', 'd'])
        merge_list(list1, ['c', 'c'])
        self.assertListEqual(list1, ['a', 'b', 'c', 'd'])