# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\tiles.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 63496 bytes
__doc__ = 'Tile map management and rendering.\n\nThis module provides an API for loading, saving and rendering a map\nconstructed of image tiles.\n'
from __future__ import division, print_function, unicode_literals
import six
__docformat__ = 'restructuredtext'
__version__ = '$Id: resource.py 1078 2007-08-01 03:43:38Z r1chardj0n3s $'
import os
from math import ceil, sqrt, floor
import struct, weakref
from xml.etree import ElementTree
import pyglet
from pyglet import gl
import pyglet.text.formats.html as p_html
import cocos
import cocos.director as director
from cocos.rect import Rect
unicode = six.text_type

class ResourceError(Exception):
    pass


class TilesPropertyWithoutName(Exception):
    pass


class TilesPropertyWithoutValue(Exception):
    pass


class TmxUnsupportedVariant(Exception):
    pass


class Resource(object):
    """Resource"""
    cache = {}

    def __init__(self, filename):
        self.filename = filename
        self.contents = {}
        self.requires = []
        self.path = self.find_file(filename)

    def find_file(self, filename):
        if os.path.isabs(filename):
            return filename
        if os.path.exists(filename):
            return filename
        path = pyglet.resource.location(filename).path
        return os.path.join(path, filename)

    @classmethod
    def register_factory(cls, name):

        def decorate(func):
            cls.factories[name] = func
            return func

        return decorate

    def handle(self, tag):
        ref = tag.get('ref')
        if not ref:
            return self.factories[tag.tag](self, tag)
        return self.get_resource(ref)

    def __contains__(self, ref):
        return ref in self.contents

    def __getitem__(self, ref):
        reqns = ''
        id = ref
        if ':' in ref:
            reqns, id = ref.split(':', 1)
        elif id in self.contents:
            return self.contents[id]
        for ns, res in self.requires:
            if ns != reqns:
                pass
            else:
                if id in res:
                    return res[id]
                raise KeyError(id)

    def find(self, cls):
        """Find all elements of the given class in this resource.
        """
        for k in self.contents:
            if isinstance(self.contents[k], cls):
                yield (
                 k, self.contents[k])

    def findall(self, cls, ns=''):
        """Find all elements of the given class in this resource and all
        <requires>'ed resources.
        """
        for k in self.contents:
            if isinstance(self.contents[k], cls):
                if ns:
                    yield (
                     ns + ':' + k, self.contents[k])
                else:
                    yield (
                     k, self.contents[k])
            for ns, res in self.requires:
                for item in res.findall(cls, ns):
                    yield item

    def add_resource(self, id, resource):
        self.contents[id] = resource

    def get_resource(self, ref):
        return self[ref]

    def save_xml(self, filename):
        """Save this resource's XML to the indicated file.
        """
        root = ElementTree.Element('resource')
        root.tail = '\n'
        for namespace, res in self.requires:
            r = ElementTree.SubElement(root, 'requires', file=(res.filename))
            r.tail = '\n'
            if namespace:
                r.set('namespace', namespace)
            for element in self.contents.values():
                element._as_xml(root)

            tree = ElementTree.ElementTree(root)
            tree.write(filename)

    def resource_factory(self, tag):
        for child in tag:
            self.handle(child)

    def requires_factory(self, tag):
        resource = load(tag.get('file'))
        self.requires.append((tag.get('namespace', ''), resource))

    factories = {'resource':resource_factory, 
     'requires':requires_factory}


_cache = weakref.WeakValueDictionary()

class _NOT_LOADED(object):
    pass


def load(filename):
    """Load resource(s) defined in the indicated XML file.
    """
    dirname = os.path.dirname(filename)
    if dirname:
        if dirname not in pyglet.resource.path:
            if os.sep == '\\':
                dirname = dirname.replace(os.sep, '/')
            pyglet.resource.path.append(dirname)
            pyglet.resource.reindex()
    elif filename in _cache:
        if _cache[filename] is _NOT_LOADED:
            raise ResourceError('Loop in tile map files loading "%s"' % filename)
        return _cache[filename]
        _cache[filename] = _NOT_LOADED
        if filename.endswith('.tmx'):
            obj = load_tmx(filename)
    else:
        obj = load_tiles(filename)
    _cache[filename] = obj
    return obj


def load_tiles(filename):
    """Load some tile mapping resources from an XML file.
    """
    resource = Resource(filename)
    tree = ElementTree.parse(resource.path)
    root = tree.getroot()
    if root.tag != 'resource':
        raise ResourceError('document is <%s> instead of <resource>' % root.name)
    resource.handle(root)
    return resource


def decode_base64(s):
    """returns a bytes object"""
    if six.PY2:
        return s.decode('base64')
    import base64
    b = s.encode('utf-8')
    return base64.b64decode(b)


def decompress_zlib(in_bytes):
    """decompress the input array of bytes to an array of bytes using zlib"""
    if six.PY2:
        out_bytes = in_bytes.decode('zlib')
    else:
        import zlib
        out_bytes = zlib.decompress(in_bytes)
    return out_bytes


def decompress_gzip(in_bytes):
    """decompress the input array of bytes to an array of bytes using gzip"""
    import gzip
    inp = six.BytesIO(in_bytes)
    f = gzip.GzipFile(fileobj=inp)
    out_bytes = f.read()
    f.close()
    inp.close()
    return out_bytes


def load_tmx--- This code section failed: ---

 L. 271         0  LOAD_GLOBAL              Resource
                2  LOAD_FAST                'filename'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'resource'

 L. 273         8  LOAD_GLOBAL              ElementTree
               10  LOAD_METHOD              parse
               12  LOAD_FAST                'resource'
               14  LOAD_ATTR                path
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'tree'

 L. 274        20  LOAD_FAST                'tree'
               22  LOAD_METHOD              getroot
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'map'

 L. 275        28  LOAD_FAST                'map'
               30  LOAD_ATTR                tag
               32  LOAD_STR                 'map'
               34  COMPARE_OP               !=
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 276        38  LOAD_GLOBAL              ResourceError
               40  LOAD_STR                 'document is <%s> instead of <map>'
               42  LOAD_FAST                'map'
               44  LOAD_ATTR                name
               46  BINARY_MODULO    
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  ''
             52_0  COME_FROM            36  '36'

 L. 278        52  LOAD_GLOBAL              int
               54  LOAD_FAST                'map'
               56  LOAD_ATTR                attrib
               58  LOAD_STR                 'width'
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'width'

 L. 279        66  LOAD_GLOBAL              int
               68  LOAD_FAST                'map'
               70  LOAD_ATTR                attrib
               72  LOAD_STR                 'height'
               74  BINARY_SUBSCR    
               76  CALL_FUNCTION_1       1  ''
               78  STORE_DEREF              'height'

 L. 282        80  LOAD_GLOBAL              int
               82  LOAD_FAST                'map'
               84  LOAD_ATTR                attrib
               86  LOAD_STR                 'tilewidth'
               88  BINARY_SUBSCR    
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'tile_width'

 L. 283        94  LOAD_GLOBAL              int
               96  LOAD_FAST                'map'
               98  LOAD_ATTR                attrib
              100  LOAD_STR                 'tileheight'
              102  BINARY_SUBSCR    
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'tile_height'

 L. 285       108  LOAD_FAST                'map'
              110  LOAD_ATTR                attrib
              112  LOAD_STR                 'orientation'
              114  BINARY_SUBSCR    
              116  STORE_FAST               'tiling_style'

 L. 287       118  LOAD_FAST                'tiling_style'
              120  LOAD_STR                 'hexagonal'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   200  'to 200'

 L. 288       126  LOAD_GLOBAL              int
              128  LOAD_FAST                'map'
              130  LOAD_ATTR                attrib
              132  LOAD_STR                 'hexsidelength'
              134  BINARY_SUBSCR    
              136  CALL_FUNCTION_1       1  ''
              138  STORE_FAST               'hex_sidelenght'

 L. 291       140  LOAD_FAST                'map'
              142  LOAD_ATTR                attrib
              144  LOAD_STR                 'staggeraxis'
              146  BINARY_SUBSCR    
              148  STORE_FAST               's'

 L. 292       150  LOAD_STR                 'pointy_left'
              152  LOAD_STR                 'pointy_up'
              154  LOAD_CONST               ('x', 'y')
              156  BUILD_CONST_KEY_MAP_2     2 
              158  STORE_FAST               'hex_orientation'

 L. 294       160  LOAD_FAST                'map'
              162  LOAD_ATTR                attrib
              164  LOAD_STR                 'staggerindex'
              166  BINARY_SUBSCR    
              168  LOAD_STR                 'even'
              170  COMPARE_OP               ==
              172  STORE_FAST               'lowest_columns'

 L. 295       174  LOAD_GLOBAL              HexCell
              176  STORE_FAST               'cell_cls'

 L. 296       178  LOAD_GLOBAL              HexMapLayer
              180  STORE_FAST               'layer_cls'

 L. 297       182  LOAD_DEREF               'height'
              184  LOAD_FAST                'tile_height'
              186  BINARY_MULTIPLY  
              188  LOAD_FAST                'tile_height'
              190  LOAD_CONST               2
              192  BINARY_FLOOR_DIVIDE
              194  BINARY_ADD       
              196  STORE_FAST               'map_height_pixels'
              198  JUMP_FORWARD        234  'to 234'
            200_0  COME_FROM           124  '124'

 L. 299       200  LOAD_FAST                'tiling_style'
              202  LOAD_STR                 'orthogonal'
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   226  'to 226'

 L. 300       208  LOAD_GLOBAL              RectCell
              210  STORE_FAST               'cell_cls'

 L. 301       212  LOAD_GLOBAL              RectMapLayer
              214  STORE_FAST               'layer_cls'

 L. 302       216  LOAD_DEREF               'height'
              218  LOAD_FAST                'tile_height'
              220  BINARY_MULTIPLY  
              222  STORE_FAST               'map_height_pixels'
              224  JUMP_FORWARD        234  'to 234'
            226_0  COME_FROM           206  '206'

 L. 305       226  LOAD_GLOBAL              ValueError
              228  LOAD_STR                 "Unsuported tiling style, must be 'orthogonal' or 'hexagonal'"
              230  CALL_FUNCTION_1       1  ''
              232  RAISE_VARARGS_1       1  ''
            234_0  COME_FROM           224  '224'
            234_1  COME_FROM           198  '198'

 L. 308       234  BUILD_LIST_0          0 
              236  STORE_FAST               'tilesets'

 L. 309       238  LOAD_FAST                'map'
              240  LOAD_METHOD              findall
              242  LOAD_STR                 'tileset'
              244  CALL_METHOD_1         1  ''
              246  GET_ITER         
          248_250  FOR_ITER            634  'to 634'
              252  STORE_FAST               'tag'

 L. 310       254  LOAD_STR                 'source'
              256  LOAD_FAST                'tag'
              258  LOAD_ATTR                attrib
              260  COMPARE_OP               in
          262_264  POP_JUMP_IF_FALSE   332  'to 332'

 L. 311       266  LOAD_GLOBAL              int
              268  LOAD_FAST                'tag'
              270  LOAD_ATTR                attrib
              272  LOAD_STR                 'firstgid'
              274  BINARY_SUBSCR    
              276  CALL_FUNCTION_1       1  ''
              278  STORE_FAST               'firstgid'

 L. 312       280  LOAD_FAST                'resource'
              282  LOAD_METHOD              find_file
              284  LOAD_FAST                'tag'
              286  LOAD_ATTR                attrib
              288  LOAD_STR                 'source'
              290  BINARY_SUBSCR    
              292  CALL_METHOD_1         1  ''
              294  STORE_FAST               'path'

 L. 313       296  LOAD_GLOBAL              open
              298  LOAD_FAST                'path'
              300  CALL_FUNCTION_1       1  ''
              302  SETUP_WITH          324  'to 324'
              304  STORE_FAST               'f'

 L. 314       306  LOAD_GLOBAL              ElementTree
              308  LOAD_METHOD              fromstring
              310  LOAD_FAST                'f'
              312  LOAD_METHOD              read
              314  CALL_METHOD_0         0  ''
              316  CALL_METHOD_1         1  ''
              318  STORE_FAST               'tag'
              320  POP_BLOCK        
              322  BEGIN_FINALLY    
            324_0  COME_FROM_WITH      302  '302'
              324  WITH_CLEANUP_START
              326  WITH_CLEANUP_FINISH
              328  END_FINALLY      
              330  JUMP_FORWARD        346  'to 346'
            332_0  COME_FROM           262  '262'

 L. 316       332  LOAD_GLOBAL              int
              334  LOAD_FAST                'tag'
              336  LOAD_ATTR                attrib
              338  LOAD_STR                 'firstgid'
              340  BINARY_SUBSCR    
              342  CALL_FUNCTION_1       1  ''
              344  STORE_FAST               'firstgid'
            346_0  COME_FROM           330  '330'

 L. 318       346  LOAD_FAST                'tag'
              348  LOAD_ATTR                attrib
              350  LOAD_STR                 'name'
              352  BINARY_SUBSCR    
              354  STORE_FAST               'name'

 L. 320       356  LOAD_GLOBAL              int
              358  LOAD_FAST                'tag'
              360  LOAD_ATTR                attrib
              362  LOAD_METHOD              get
              364  LOAD_STR                 'spacing'
              366  LOAD_CONST               0
              368  CALL_METHOD_2         2  ''
              370  CALL_FUNCTION_1       1  ''
              372  STORE_FAST               'spacing'

 L. 321       374  LOAD_FAST                'tag'
              376  LOAD_METHOD              getchildren
              378  CALL_METHOD_0         0  ''
              380  GET_ITER         
            382_0  COME_FROM           506  '506'
              382  FOR_ITER            632  'to 632'
              384  STORE_FAST               'c'

 L. 322       386  LOAD_FAST                'c'
              388  LOAD_ATTR                tag
              390  LOAD_STR                 'image'
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_FALSE   498  'to 498'

 L. 324       398  LOAD_FAST                'resource'
              400  LOAD_METHOD              find_file
              402  LOAD_FAST                'c'
              404  LOAD_ATTR                attrib
              406  LOAD_STR                 'source'
              408  BINARY_SUBSCR    
              410  CALL_METHOD_1         1  ''
              412  STORE_FAST               'path'

 L. 325       414  LOAD_GLOBAL              int
              416  LOAD_FAST                'tag'
              418  LOAD_ATTR                attrib
              420  LOAD_METHOD              get
              422  LOAD_STR                 'tileheight'
              424  LOAD_FAST                'tile_height'
              426  CALL_METHOD_2         2  ''
              428  CALL_FUNCTION_1       1  ''
              430  STORE_FAST               'tileset_tile_height'

 L. 326       432  LOAD_GLOBAL              int
              434  LOAD_FAST                'tag'
              436  LOAD_ATTR                attrib
              438  LOAD_METHOD              get
              440  LOAD_STR                 'tilewidth'
              442  LOAD_FAST                'tile_width'
              444  CALL_METHOD_2         2  ''
              446  CALL_FUNCTION_1       1  ''
              448  STORE_FAST               'tileset_tile_width'

 L. 327       450  LOAD_GLOBAL              TileSet
              452  LOAD_ATTR                from_atlas
              454  LOAD_FAST                'name'
              456  LOAD_FAST                'firstgid'
              458  LOAD_FAST                'path'
              460  LOAD_FAST                'tileset_tile_width'

 L. 328       462  LOAD_FAST                'tileset_tile_height'

 L. 328       464  LOAD_FAST                'spacing'

 L. 329       466  LOAD_FAST                'spacing'

 L. 327       468  LOAD_CONST               ('row_padding', 'column_padding')
              470  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              472  STORE_FAST               'tileset'

 L. 331       474  LOAD_FAST                'tilesets'
              476  LOAD_METHOD              append
              478  LOAD_FAST                'tileset'
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          

 L. 332       484  LOAD_FAST                'resource'
              486  LOAD_METHOD              add_resource
              488  LOAD_FAST                'name'
              490  LOAD_FAST                'tileset'
              492  CALL_METHOD_2         2  ''
              494  POP_TOP          
              496  JUMP_BACK           382  'to 382'
            498_0  COME_FROM           394  '394'

 L. 333       498  LOAD_FAST                'c'
              500  LOAD_ATTR                tag
              502  LOAD_STR                 'tile'
              504  COMPARE_OP               ==
          506_508  POP_JUMP_IF_FALSE   382  'to 382'

 L. 335       510  LOAD_FAST                'tileset'
              512  LOAD_ATTR                firstgid
              514  LOAD_GLOBAL              int
              516  LOAD_FAST                'c'
              518  LOAD_ATTR                attrib
              520  LOAD_STR                 'id'
              522  BINARY_SUBSCR    
              524  CALL_FUNCTION_1       1  ''
              526  BINARY_ADD       
              528  STORE_FAST               'gid'

 L. 336       530  LOAD_FAST                'tileset'
              532  LOAD_FAST                'gid'
              534  BINARY_SUBSCR    
              536  STORE_FAST               'tile'

 L. 337       538  LOAD_FAST                'c'
              540  LOAD_METHOD              find
              542  LOAD_STR                 'properties'
              544  CALL_METHOD_1         1  ''
              546  STORE_FAST               'props'

 L. 338       548  LOAD_FAST                'props'
              550  LOAD_CONST               None
              552  COMPARE_OP               is
          554_556  POP_JUMP_IF_FALSE   562  'to 562'

 L. 339   558_560  JUMP_BACK           382  'to 382'
            562_0  COME_FROM           554  '554'

 L. 340       562  LOAD_FAST                'props'
              564  LOAD_METHOD              findall
              566  LOAD_STR                 'property'
              568  CALL_METHOD_1         1  ''
              570  GET_ITER         
              572  FOR_ITER            628  'to 628'
              574  STORE_FAST               'p'

 L. 342       576  LOAD_FAST                'p'
              578  LOAD_ATTR                attrib
              580  LOAD_STR                 'name'
              582  BINARY_SUBSCR    
              584  STORE_FAST               'name'

 L. 343       586  LOAD_FAST                'p'
              588  LOAD_ATTR                attrib
              590  LOAD_STR                 'value'
              592  BINARY_SUBSCR    
              594  STORE_FAST               'value'

 L. 345       596  LOAD_FAST                'value'
              598  LOAD_METHOD              isdigit
              600  CALL_METHOD_0         0  ''
          602_604  POP_JUMP_IF_FALSE   614  'to 614'

 L. 346       606  LOAD_GLOBAL              int
              608  LOAD_FAST                'value'
              610  CALL_FUNCTION_1       1  ''
              612  STORE_FAST               'value'
            614_0  COME_FROM           602  '602'

 L. 347       614  LOAD_FAST                'value'
              616  LOAD_FAST                'tile'
              618  LOAD_ATTR                properties
              620  LOAD_FAST                'name'
              622  STORE_SUBSCR     
          624_626  JUMP_BACK           572  'to 572'
          628_630  JUMP_BACK           382  'to 382'
              632  JUMP_BACK           248  'to 248'

 L. 350       634  LOAD_FAST                'map'
              636  LOAD_METHOD              findall
              638  LOAD_STR                 'layer'
              640  CALL_METHOD_1         1  ''
              642  GET_ITER         
          644_646  FOR_ITER           1144  'to 1144'
              648  STORE_FAST               'layer'

 L. 351       650  LOAD_FAST                'layer'
              652  LOAD_METHOD              find
              654  LOAD_STR                 'data'
              656  CALL_METHOD_1         1  ''
              658  STORE_FAST               'data'

 L. 352       660  LOAD_FAST                'data'
              662  LOAD_CONST               None
              664  COMPARE_OP               is
          666_668  POP_JUMP_IF_FALSE   684  'to 684'

 L. 353       670  LOAD_GLOBAL              ValueError
              672  LOAD_STR                 'layer %s does not contain <data>'
              674  LOAD_FAST                'layer'
              676  LOAD_ATTR                name
              678  BINARY_MODULO    
              680  CALL_FUNCTION_1       1  ''
              682  RAISE_VARARGS_1       1  ''
            684_0  COME_FROM           666  '666'

 L. 355       684  LOAD_FAST                'data'
              686  LOAD_ATTR                attrib
              688  LOAD_METHOD              get
              690  LOAD_STR                 'encoding'
              692  CALL_METHOD_1         1  ''
              694  STORE_FAST               'encoding'

 L. 356       696  LOAD_FAST                'data'
              698  LOAD_ATTR                attrib
              700  LOAD_METHOD              get
              702  LOAD_STR                 'compression'
              704  CALL_METHOD_1         1  ''
              706  STORE_FAST               'compression'

 L. 357       708  LOAD_FAST                'encoding'
              710  LOAD_CONST               None
              712  COMPARE_OP               is
          714_716  POP_JUMP_IF_FALSE   740  'to 740'

 L. 359       718  LOAD_LISTCOMP            '<code_object <listcomp>>'
              720  LOAD_STR                 'load_tmx.<locals>.<listcomp>'
              722  MAKE_FUNCTION_0          ''
              724  LOAD_FAST                'data'
              726  LOAD_METHOD              findall
              728  LOAD_STR                 'tile'
              730  CALL_METHOD_1         1  ''
              732  GET_ITER         
              734  CALL_FUNCTION_1       1  ''
              736  STORE_FAST               'data'
              738  JUMP_FORWARD        914  'to 914'
            740_0  COME_FROM           714  '714'

 L. 361       740  LOAD_FAST                'data'
              742  LOAD_ATTR                text
              744  LOAD_METHOD              strip
              746  CALL_METHOD_0         0  ''
              748  STORE_FAST               'data'

 L. 362       750  LOAD_FAST                'encoding'
              752  LOAD_STR                 'csv'
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_FALSE   794  'to 794'

 L. 363       760  LOAD_FAST                'data'
              762  LOAD_METHOD              replace
              764  LOAD_STR                 '\n'
              766  LOAD_STR                 ''
              768  CALL_METHOD_2         2  ''
              770  POP_TOP          

 L. 364       772  LOAD_LISTCOMP            '<code_object <listcomp>>'
              774  LOAD_STR                 'load_tmx.<locals>.<listcomp>'
              776  MAKE_FUNCTION_0          ''
              778  LOAD_FAST                'data'
              780  LOAD_METHOD              split
              782  LOAD_STR                 ','
              784  CALL_METHOD_1         1  ''
              786  GET_ITER         
              788  CALL_FUNCTION_1       1  ''
              790  STORE_FAST               'data'
              792  JUMP_FORWARD        914  'to 914'
            794_0  COME_FROM           756  '756'

 L. 365       794  LOAD_FAST                'encoding'
              796  LOAD_STR                 'base64'
              798  COMPARE_OP               ==
          800_802  POP_JUMP_IF_FALSE   906  'to 906'

 L. 366       804  LOAD_GLOBAL              decode_base64
              806  LOAD_FAST                'data'
              808  CALL_FUNCTION_1       1  ''
              810  STORE_FAST               'data'

 L. 367       812  LOAD_FAST                'compression'
              814  LOAD_STR                 'zlib'
              816  COMPARE_OP               ==
          818_820  POP_JUMP_IF_FALSE   832  'to 832'

 L. 368       822  LOAD_GLOBAL              decompress_zlib
              824  LOAD_FAST                'data'
              826  CALL_FUNCTION_1       1  ''
              828  STORE_FAST               'data'
              830  JUMP_FORWARD        876  'to 876'
            832_0  COME_FROM           818  '818'

 L. 369       832  LOAD_FAST                'compression'
              834  LOAD_STR                 'gzip'
              836  COMPARE_OP               ==
          838_840  POP_JUMP_IF_FALSE   852  'to 852'

 L. 370       842  LOAD_GLOBAL              decompress_gzip
              844  LOAD_FAST                'data'
              846  CALL_FUNCTION_1       1  ''
              848  STORE_FAST               'data'
              850  JUMP_FORWARD        876  'to 876'
            852_0  COME_FROM           838  '838'

 L. 371       852  LOAD_FAST                'compression'
              854  LOAD_CONST               None
              856  COMPARE_OP               is
          858_860  POP_JUMP_IF_FALSE   864  'to 864'

 L. 372       862  BREAK_LOOP          876  'to 876'
            864_0  COME_FROM           858  '858'

 L. 374       864  LOAD_GLOBAL              ResourceError
              866  LOAD_STR                 'Unknown compression method: %r'
              868  LOAD_FAST                'compression'
              870  BINARY_MODULO    
              872  CALL_FUNCTION_1       1  ''
              874  RAISE_VARARGS_1       1  ''
            876_0  COME_FROM           862  '862'
            876_1  COME_FROM           850  '850'
            876_2  COME_FROM           830  '830'

 L. 375       876  LOAD_GLOBAL              struct
              878  LOAD_METHOD              unpack
              880  LOAD_GLOBAL              str
              882  LOAD_STR                 '<%di'
              884  LOAD_GLOBAL              len
              886  LOAD_FAST                'data'
              888  CALL_FUNCTION_1       1  ''
              890  LOAD_CONST               4
              892  BINARY_FLOOR_DIVIDE
              894  BINARY_MODULO    
              896  CALL_FUNCTION_1       1  ''
              898  LOAD_FAST                'data'
              900  CALL_METHOD_2         2  ''
              902  STORE_FAST               'data'
              904  JUMP_FORWARD        914  'to 914'
            906_0  COME_FROM           800  '800'

 L. 377       906  LOAD_GLOBAL              TmxUnsupportedVariant
              908  LOAD_STR                 "Unsupported tiles layer format use 'csv', 'xml' or one of the 'base64'"
              910  CALL_FUNCTION_1       1  ''
              912  RAISE_VARARGS_1       1  ''
            914_0  COME_FROM           904  '904'
            914_1  COME_FROM           792  '792'
            914_2  COME_FROM           738  '738'

 L. 381       914  LOAD_GLOBAL              len
              916  LOAD_FAST                'data'
              918  CALL_FUNCTION_1       1  ''
              920  LOAD_FAST                'width'
              922  LOAD_DEREF               'height'
              924  BINARY_MULTIPLY  
              926  COMPARE_OP               ==
          928_930  POP_JUMP_IF_TRUE    936  'to 936'
              932  LOAD_ASSERT              AssertionError
              934  RAISE_VARARGS_1       1  ''
            936_0  COME_FROM           928  '928'

 L. 383       936  LOAD_CLOSURE             'height'
              938  BUILD_TUPLE_1         1 
              940  LOAD_LISTCOMP            '<code_object <listcomp>>'
              942  LOAD_STR                 'load_tmx.<locals>.<listcomp>'
              944  MAKE_FUNCTION_8          'closure'
              946  LOAD_GLOBAL              range
              948  LOAD_FAST                'width'
              950  CALL_FUNCTION_1       1  ''
              952  GET_ITER         
              954  CALL_FUNCTION_1       1  ''
              956  STORE_FAST               'cells'

 L. 384       958  LOAD_GLOBAL              enumerate
              960  LOAD_FAST                'data'
              962  CALL_FUNCTION_1       1  ''
              964  GET_ITER         
              966  FOR_ITER           1080  'to 1080'
              968  UNPACK_SEQUENCE_2     2 
              970  STORE_FAST               'n'
              972  STORE_FAST               'gid'

 L. 385       974  LOAD_FAST                'gid'
              976  LOAD_CONST               1
              978  COMPARE_OP               <
          980_982  POP_JUMP_IF_FALSE   990  'to 990'

 L. 386       984  LOAD_CONST               None
              986  STORE_FAST               'tile'
              988  JUMP_FORWARD       1026  'to 1026'
            990_0  COME_FROM           980  '980'

 L. 389       990  LOAD_FAST                'tilesets'
              992  GET_ITER         
            994_0  COME_FROM          1004  '1004'
              994  FOR_ITER           1026  'to 1026'
              996  STORE_FAST               'ts'

 L. 390       998  LOAD_FAST                'gid'
             1000  LOAD_FAST                'ts'
             1002  COMPARE_OP               in
         1004_1006  POP_JUMP_IF_FALSE   994  'to 994'

 L. 391      1008  LOAD_FAST                'ts'
             1010  LOAD_FAST                'gid'
             1012  BINARY_SUBSCR    
             1014  STORE_FAST               'tile'

 L. 392      1016  POP_TOP          
         1018_1020  BREAK_LOOP         1026  'to 1026'
         1022_1024  JUMP_BACK           994  'to 994'
           1026_0  COME_FROM           988  '988'

 L. 393      1026  LOAD_FAST                'n'
             1028  LOAD_FAST                'width'
             1030  BINARY_MODULO    
             1032  STORE_FAST               'i'

 L. 394      1034  LOAD_DEREF               'height'
             1036  LOAD_FAST                'n'
             1038  LOAD_FAST                'width'
             1040  BINARY_FLOOR_DIVIDE
             1042  LOAD_CONST               1
             1044  BINARY_ADD       
             1046  BINARY_SUBTRACT  
             1048  STORE_FAST               'j'

 L. 395      1050  LOAD_FAST                'cell_cls'
             1052  LOAD_FAST                'i'
             1054  LOAD_FAST                'j'
             1056  LOAD_FAST                'tile_width'
             1058  LOAD_FAST                'tile_height'
             1060  BUILD_MAP_0           0 
             1062  LOAD_FAST                'tile'
             1064  CALL_FUNCTION_6       6  ''
             1066  LOAD_FAST                'cells'
             1068  LOAD_FAST                'i'
             1070  BINARY_SUBSCR    
             1072  LOAD_FAST                'j'
             1074  STORE_SUBSCR     
         1076_1078  JUMP_BACK           966  'to 966'

 L. 397      1080  LOAD_FAST                'layer'
             1082  LOAD_ATTR                attrib
             1084  LOAD_STR                 'name'
             1086  BINARY_SUBSCR    
             1088  STORE_FAST               'id'

 L. 399      1090  LOAD_FAST                'layer_cls'
             1092  LOAD_FAST                'id'
             1094  LOAD_FAST                'tile_width'
             1096  LOAD_FAST                'tile_height'
             1098  LOAD_FAST                'cells'
             1100  LOAD_CONST               None
             1102  BUILD_MAP_0           0 
             1104  CALL_FUNCTION_6       6  ''
             1106  STORE_FAST               'm'

 L. 400      1108  LOAD_GLOBAL              int
             1110  LOAD_FAST                'layer'
             1112  LOAD_ATTR                attrib
             1114  LOAD_METHOD              get
             1116  LOAD_STR                 'visible'
             1118  LOAD_CONST               1
             1120  CALL_METHOD_2         2  ''
             1122  CALL_FUNCTION_1       1  ''
             1124  LOAD_FAST                'm'
             1126  STORE_ATTR               visible

 L. 402      1128  LOAD_FAST                'resource'
             1130  LOAD_METHOD              add_resource
             1132  LOAD_FAST                'id'
             1134  LOAD_FAST                'm'
             1136  CALL_METHOD_2         2  ''
             1138  POP_TOP          
         1140_1142  JUMP_BACK           644  'to 644'

 L. 405      1144  LOAD_FAST                'map'
             1146  LOAD_METHOD              findall
             1148  LOAD_STR                 'objectgroup'
             1150  CALL_METHOD_1         1  ''
             1152  GET_ITER         
             1154  FOR_ITER           1190  'to 1190'
             1156  STORE_FAST               'tag'

 L. 406      1158  LOAD_GLOBAL              TmxObjectLayer
             1160  LOAD_METHOD              fromxml
             1162  LOAD_FAST                'tag'
             1164  LOAD_FAST                'tilesets'
             1166  LOAD_FAST                'map_height_pixels'
             1168  CALL_METHOD_3         3  ''
             1170  STORE_FAST               'layer'

 L. 407      1172  LOAD_FAST                'resource'
             1174  LOAD_METHOD              add_resource
             1176  LOAD_FAST                'layer'
             1178  LOAD_ATTR                name
             1180  LOAD_FAST                'layer'
             1182  CALL_METHOD_2         2  ''
             1184  POP_TOP          
         1186_1188  JUMP_BACK          1154  'to 1154'

 L. 409      1190  LOAD_FAST                'resource'
             1192  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 322


def text_to_4tuple_int(s):
    s = s.strip()
    s = s[1:-1]
    res = tuple([int(v) for v in s.split(',')])
    for e in res:
        assert 0 <= e <= 255
        return res


def color4_to_text(v):
    return repr(v)


_xml_to_python = dict(unicode=unicode,
  int=int,
  float=float,
  bool=(lambda value: value != 'False'),
  color4=text_to_4tuple_int)
_python_to_xml = {str: unicode, 
 unicode: unicode, 
 int: repr, 
 float: repr, 
 bool: repr, 
 'color4': color4_to_text}
_xml_type = {str: 'unicode', 
 unicode: 'unicode', 
 int: 'int', 
 float: 'float', 
 bool: 'bool', 
 'color4': 'color4'}

def _handle_properties(tag):
    """returns the properties dict reading from the etree node tag

    :Parameters:
        `tag` : xml.etree.ElementTree
            node from which the properties are obtained
    """
    properties = {}
    for node in tag.findall('./property'):
        name = node.get('name')
        type = node.get('type') or 
        value = node.get('value')
        if name is None:
            raise TilesPropertyWithoutName('\nnode:\n%s' % ElementTree.tostring(node))
        if value is None:
            raise TilesPropertyWithoutValue('\nnode:\n%s' % ElementTree.tostring(node))
        properties[name] = _xml_to_python[type](value)

    return properties


@Resource.register_factory('image')
def image_factory(resource, tag):
    filename = resource.find_file(tag.get('file'))
    if not filename:
        raise ResourceError('No file= on <image> tag')
    image = pyglet.image.load(filename)
    image.properties = _handle_properties(tag)
    if tag.get('id'):
        image.id = tag.get('id')
        resource.add_resource(image.id, image)
    return image


@Resource.register_factory('imageatlas')
def imageatlas_factory(resource, tag):
    filename = resource.find_file(tag.get('file'))
    if not filename:
        raise ResourceError('No file= on <imageatlas> tag')
    else:
        atlas = pyglet.image.load(filename)
        atlas.properties = _handle_properties(tag)
        if tag.get('id'):
            atlas.id = tag.get('id')
            resource.add_resource(atlas.id, atlas)
        if tag.get('size'):
            d_width, d_height = map(int, tag.get('size').split('x'))
        else:
            d_width = d_height = None
    for child in tag:
        if child.tag != 'image':
            raise ValueError('invalid child')
        elif child.get('size'):
            width, height = map(int, child.get('size').split('x'))
        elif d_width is None:
            raise ValueError('atlas or subimage must specify size')
        else:
            width, height = d_width, d_height
        x, y = map(int, child.get('offset').split(','))
        image = atlas.get_region(x, y, width, height)
        tx = image.get_texture()
        gl.glBindTexture(tx.target, tx.id)
        gl.glTexParameteritx.targetgl.GL_TEXTURE_WRAP_Sgl.GL_CLAMP_TO_EDGE
        gl.glTexParameteritx.targetgl.GL_TEXTURE_WRAP_Tgl.GL_CLAMP_TO_EDGE
        id = child.get('id')
        resource.add_resource(id, image)
        image.properties = _handle_properties(child)

    return atlas


@Resource.register_factory('tileset')
def tileset_factory(resource, tag):
    id = tag.get('id')
    properties = _handle_properties(tag)
    tileset = TileSet(id, properties)
    resource.add_resource(tileset.id, tileset)
    for child in tag:
        id = child.get('id')
        offset = child.get('offset')
        if offset:
            offset = map(int, offset.split(','))
        else:
            offset = None
        properties = _handle_properties(child)
        image = child.find('image')
        if image is not None:
            image = resource.handle(image)
        tile = Tile(id, properties, image, offset)
        resource.add_resource(id, tile)
        tileset[id] = tile

    return tileset


class Tile(object):
    """Tile"""

    def __init__(self, id, properties, image, offset=None):
        self.id = id
        self.properties = properties
        self.image = image
        self.offset = offset

    def __repr__(self):
        return '<%s object at 0x%x id=%r offset=%r properties=%r>' % (
         self.__class__.__name__, id(self), self.id, self.offset, self.properties)


class TileSet(dict):
    """TileSet"""

    def __init__(self, id, properties):
        self.id = id
        self.properties = properties

    tile_id = 0

    @classmethod
    def generate_id(cls):
        cls.tile_id += 1
        return str(cls.tile_id)

    def add(self, properties, image, id=None):
        """Add a new Tile to this TileSet, generating a unique id if
        necessary.

        Returns the Tile instance.
        """
        if id is None:
            id = self.generate_id()
        self[id] = Tile(id, properties, image)
        return self[id]

    @classmethod
    def from_atlas(cls, name, firstgid, file, tile_width, tile_height, row_padding=0, column_padding=0):
        image = pyglet.image.load(file)
        rows = (image.height + row_padding) // (tile_height + row_padding)
        columns = (image.width + column_padding) // (tile_width + column_padding)
        image_grid = pyglet.image.ImageGrid(image, rows, columns, row_padding=row_padding,
          column_padding=column_padding)
        atlas = pyglet.image.TextureGrid(image_grid)
        id = firstgid
        ts = cls(name, {})
        ts.firstgid = firstgid
        for j in range(rows - 1, -1, -1):
            for i in range(columns):
                tile_image = image.get_region(atlas[(j, i)].x, atlas[(j, i)].y, atlas[(j, i)].width, atlas[(j, i)].height)
                tx = tile_image.get_texture()
                gl.glBindTexture(tx.target, tx.id)
                gl.glTexParameteritx.targetgl.GL_TEXTURE_WRAP_Sgl.GL_CLAMP_TO_EDGE
                gl.glTexParameteritx.targetgl.GL_TEXTURE_WRAP_Tgl.GL_CLAMP_TO_EDGE
                ts[id] = Tile(id, {}, tile_image)
                id += 1

            return ts


@Resource.register_factory('rectmap')
def rectmap_factory(resource, tag):
    width, height = map(int, tag.get('tile_size').split('x'))
    origin = tag.get('origin')
    if origin:
        origin = map(int, tag.get('origin').split(','))
    id = tag.get('id')
    cells = []
    for i, column in enumerate(tag.getiterator('column')):
        c = []
        cells.append(c)
        for j, cell in enumerate(column.getiterator('cell')):
            tile = cell.get('tile')
            if tile:
                tile = resource.get_resource(tile)
            else:
                tile = None
            properties = _handle_properties(cell)
            c.append(RectCellijwidthheightpropertiestile)

        properties = _handle_properties(tag)
        m = RectMapLayeridwidthheightcellsoriginproperties
        resource.add_resource(id, m)
        return m


@Resource.register_factory('hexmap')
def hexmap_factory(resource, tag):
    height = int(tag.get('tile_height'))
    width = hex_width(height)
    origin = tag.get('origin')
    if origin:
        origin = map(int, tag.get('origin').split(','))
    id = tag.get('id')
    cells = []
    for i, column in enumerate(tag.getiterator('column')):
        c = []
        cells.append(c)
        for j, cell in enumerate(column.getiterator('cell')):
            tile = cell.get('tile')
            if tile:
                tile = resource.get_resource(tile)
            else:
                tile = None
            properties = _handle_properties(cell)
            c.append(HexCellijNoneheightpropertiestile)

        properties = _handle_properties(tag)
        m = HexMapLayeridNoneheightcellsoriginproperties
        resource.add_resource(id, m)
        return m


def hex_width(height):
    """Determine a regular hexagon's width given its height.
    """
    return int(height / sqrt(3) * 2)


class MapLayer(cocos.layer.ScrollableLayer):
    """MapLayer"""

    def __init__(self, properties):
        self._sprites = {}
        self.properties = properties
        super(MapLayer, self).__init__()

    def __contains__(self, key):
        return key in self.properties

    def __getitem__(self, key):
        if key in self.properties:
            return self.properties[key]
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.properties[key] = value

    def get(self, key, default=None):
        return self.properties.get(key, default)

    def set_dirty(self):
        self._sprites.clear()
        self._update_sprite_set()

    def set_view(self, x, y, w, h, viewport_x=0, viewport_y=0):
        super(MapLayer, self).set_view(x, y, w, h, viewport_x, viewport_y)
        self._update_sprite_set()

    def get_visible_cells(self):
        """Given the current view in map-space pixels, transform it based
        on the current screen-space transform and figure the region of
        map-space pixels currently visible.

        Pass to get_in_region to return a list of Cell instances.
        """
        x, y = self.view_x, self.view_y
        w, h = self.view_w, self.view_h
        return self.get_in_region(x, y, x + w, y + h)

    def is_visible(self, rect):
        """Determine whether the indicated rect (with .x, .y, .width and
        .height attributes) located in this Layer is visible.
        """
        x, y = rect.x, rect.y
        if x + rect.width < self.view_x:
            return False
        if y + rect.height < self.view_y:
            return False
        if x > self.view_x + self.view_w:
            return False
        if y > self.view_y + self.view_h:
            return False
        return True

    debug = False

    def set_debug(self, debug):
        self.debug = debug
        self._update_sprite_set()

    def set_cell_opacity(self, i, j, opacity):
        cell = self.get_cell(i, j)
        if cell is None:
            return
        elif 'color4' in cell.properties:
            r, g, b, a = cell.properties['color4']
        else:
            r, g, b = (0, 0, 0)
        cell.properties['color4'] = (
         r, g, b, opacity)
        key = cell.origin[:2]
        if key in self._sprites:
            self._sprites[key].opacity = opacity

    def set_cell_color(self, i, j, color):
        cell = self.get_cell(i, j)
        if cell is None:
            return
        elif 'color4' in cell.properties:
            a = cell.properties['color4'][3]
            r, g, b = color
        else:
            a = 255
            r, g, b = color
        cell.properties['color4'] = (
         r, g, b, a)
        key = cell.origin[:2]
        if key in self._sprites:
            self._sprites[key].color = color

    def _update_sprite_set(self):
        keep = set()
        for cell in self.get_visible_cells():
            cx, cy = key = cell.origin[:2]
            keep.add(key)
            if cell.tile is None:
                pass
            else:
                if key in self._sprites:
                    s = self._sprites[key]
                else:
                    s = pyglet.sprite.Sprite((cell.tile.image), x=cx,
                      y=cy,
                      batch=(self.batch))
                    if 'color4' in cell.properties:
                        r, g, b, a = cell.properties['color4']
                        s.color = (r, g, b)
                        s.opacity = a
                    self._sprites[key] = s
                if self.debug:
                    if getattr(s, '_label', None):
                        pass
                    else:
                        label = [
                         'cell=%d,%d' % (cell.i, cell.j),
                         'origin=%d,%d px' % (cx, cy)]
                        for p in cell.properties:
                            label.append('%s=%r' % (p, cell.properties[p]))

                        if cell.tile is not None:
                            for p in cell.tile.properties:
                                label.append('%s=%r' % (p, cell.tile.properties[p]))

                        else:
                            lx, ly = cell.topleft
                            s._label = pyglet.text.Label(('\n'.join(label)),
                              multiline=True, x=lx, y=ly, bold=True,
                              font_size=8,
                              width=(cell.width),
                              batch=(self.batch))
                else:
                    s._label = None

        for k in list(self._sprites):
            if k not in keep and k in self._sprites:
                self._sprites[k]._label = None
                del self._sprites[k]

    def find_cells(self, **requirements):
        """Find all cells that match the properties specified.

        For example:

           map.find_cells(player_start=True)

        Return a list of Cell instances.
        """
        r = []
        for col in self.cells:
            for cell in col:
                for k in requirements:
                    if cell.get(k) != requirements[k]:
                        continue

                r.append(cell)

            return r


class RegularTesselationMap(object):
    """RegularTesselationMap"""

    def get_cell--- This code section failed: ---

 L. 903         0  LOAD_FAST                'i'
                2  LOAD_CONST               0
                4  COMPARE_OP               <
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_FAST                'j'
               10  LOAD_CONST               0
               12  COMPARE_OP               <
               14  POP_JUMP_IF_FALSE    20  'to 20'
             16_0  COME_FROM             6  '6'

 L. 904        16  LOAD_CONST               None
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 905        20  SETUP_FINALLY        38  'to 38'

 L. 906        22  LOAD_FAST                'self'
               24  LOAD_ATTR                cells
               26  LOAD_FAST                'i'
               28  BINARY_SUBSCR    
               30  LOAD_FAST                'j'
               32  BINARY_SUBSCR    
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    20  '20'

 L. 907        38  DUP_TOP          
               40  LOAD_GLOBAL              IndexError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    58  'to 58'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 908        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            44  '44'
               58  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 38


class RectMap(RegularTesselationMap):
    """RectMap"""

    def __init__(self, id, tw, th, cells, origin=None, properties=None):
        """
        :Parameters:
            `id` : xml id
                node id
            `tw` : int
                number of colums in cells
            `th` : int
                number of rows in cells
            `cells` : container that supports cells[i][j]
                elements are stored in column-major order with y increasing up
            `origin` : (int, int, int)
                cell block offset x,y,z ; default is (0,0,0)
            `properties` : dict
                arbitrary properties
                if saving to XML, keys must be unicode or 8-bit ASCII strings
        """
        self.properties = properties or 
        self.id = id
        self.tw, self.th = tw, th
        if origin is None:
            origin = (0, 0, 0)
        self.origin_x, self.origin_y, self.origin_z = origin
        self.cells = cells
        self.px_width = len(cells) * tw
        self.px_height = len(cells[0]) * th

    def get_in_region(self, left, bottom, right, top):
        """Return cells that intersects the rectangle left, bottom, right, top
        in an area greater than zero

        (left, bottom) and (right, top) are the lower left and upper right
        corners respectively, in map's coordinate space, unmodified by screen,
        layer or view transformations

        Return a list of Cell instances.

        When the rectangle has area zero results are a bit inconsistent:
            A rectangle which is a point intersects no cell
            A rectangle which is a segment and overlaps the cell boundaries
            intersects no cells
            A rectangle which is a segment and don't overlaps the cell
            boundaries intersects some cells: the ones that the open segment
            intersects
        """
        ox = self.origin_x
        oy = self.origin_y
        left = max(0, (left - ox) // self.tw)
        bottom = max(0, (bottom - oy) // self.th)
        right = min(len(self.cells), ceil(float(right - ox) / self.tw))
        top = min(len(self.cells[0]), ceil(float(top - oy) / self.th))
        return [self.cells[i][j] for i in range(int(left), int(right)) for j in range(int(bottom), int(top))]

    def get_key_at_pixel(self, x, y):
        """returns the grid coordinates for the hex that covers the point (x, y)"""
        return (
         int((x - self.origin_x) // self.tw),
         int((y - self.origin_y) // self.th))

    def get_at_pixel(self, x, y):
        """ Return Cell at pixel px=(x,y) on the map.

        The pixel coordinate passed in is in the map's coordinate space,
        unmodified by screen, layer or view transformations.

        Return None if out of bounds.
        """
        return (self.get_cell)(*self.get_key_at_pixel(x, y))

    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def get_neighbor(self, cell, direction):
        """Get the neighbor Cell in the given direction (dx, dy) which
        is one of self.UP, self.DOWN, self.LEFT or self.RIGHT.

        Returns None if out of bounds.
        """
        dx, dy = direction
        return self.get_cell(cell.i + dx, cell.j + dy)

    def get_neighbors(self, cell, diagonals=False):
        """Get all cells touching the sides of the nominated cell.

        If "diagonals" is True then return the cells touching the corners
        of this cell too.

        Return a dict with the directions (self.UP, self.DOWN, etc) as keys
        and neighbor cells as values.
        """
        r = {}
        if diagonals:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx or dy:
                        direction = (
                         dx, dy)
                        r[direction] = self.get_cell(cell.i + dx, cell.j + dy)

        else:
            for direction in (
             self.UP, self.RIGHT, self.LEFT, self.DOWN):
                dx, dy = direction
                r[direction] = self.get_cell(cell.i + dx, cell.j + dy)

        return r

    def _as_xml(self, root):
        """stores a XML representation of itself as child of root with type rectmap

        """
        m = ElementTree.SubElement(root, 'rectmap', id=(self.id), tile_size=('%dx%d' % (self.tw, self.th)),
          origin=('%s,%s,%s' % (self.origin_x, self.origin_y, self.origin_z)))
        m.tail = '\n'
        for k in self.properties:
            v = self.properties[k]
            t = type(v)
            v = _python_to_xml[t](v)
            p = ElementTree.SubElement(m, 'property', name=k, value=v, type=(_xml_type[t]))
            p.tail = '\n'

        for column in self.cells:
            c = ElementTree.SubElement(m, 'column')
            c.tail = '\n'
            for cell in column:
                cell._as_xml(c)


class RectMapLayer(RectMap, MapLayer):
    """RectMapLayer"""

    def __init__(self, id, tw, th, cells, origin=None, properties=None):
        RectMap.__init__(self, id, tw, th, cells, origin, properties)
        MapLayer.__init__(self, properties)


class Cell(object):
    """Cell"""

    def __init__(self, i, j, width, height, properties, tile):
        self.width, self.height = width, height
        self.i, self.j = i, j
        self.properties = properties
        self.tile = tile

    @property
    def position(self):
        return (
         self.i, self.j)

    def _as_xml(self, parent):
        c = ElementTree.SubElement(parent, 'cell')
        c.tail = '\n'
        if self.tile:
            c.set('tile', self.tile.id)
        for k in self.properties:
            v = self.properties[k]
            if k == 'color4':
                t = 'color4'
            else:
                t = type(v)
            v = _python_to_xml[t](v)
            ElementTree.SubElement(c, 'property', name=k, value=v, type=(_xml_type[t]))

    def __contains__(self, key):
        if key in self.properties:
            return True
        return key in self.tile.properties

    def __getitem__(self, key):
        if key in self.properties:
            return self.properties[key]
        if self.tile is not None:
            if key in self.tile.properties:
                return self.tile.properties[key]
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.properties[key] = value

    def get(self, key, default=None):
        if key in self.properties:
            return self.properties[key]
        if self.tile is None:
            return default
        return self.tile.properties.get(key, default)

    def __repr__(self):
        return '<%s object at 0x%x (%g, %g) properties=%r tile=%r>' % (
         self.__class__.__name__, id(self), self.i, self.j, self.properties, self.tile)


class RectCell(Rect, Cell):
    """RectCell"""

    def __init__(self, i, j, width, height, properties, tile):
        Rect.__init__(self, i * width, j * height, width, height)
        Cell.__init__(self, i, j, width, height, properties, tile)

    origin = property(Rect.get_origin)
    top = property(Rect.get_top)
    bottom = property(Rect.get_bottom)
    center = property(Rect.get_center)
    midtop = property(Rect.get_midtop)
    midbottom = property(Rect.get_midbottom)
    left = property(Rect.get_left)
    right = property(Rect.get_right)
    topleft = property(Rect.get_topleft)
    topright = property(Rect.get_topright)
    bottomleft = property(Rect.get_bottomleft)
    bottomright = property(Rect.get_bottomright)
    midleft = property(Rect.get_midleft)
    midright = property(Rect.get_midright)


class HexMap(RegularTesselationMap):
    """HexMap"""

    def __init__(self, id, th, cells, origin=None, properties=None):
        properties = properties or 
        self.id = id
        self.th = th
        if origin is None:
            origin = (0, 0, 0)
        self.origin_x, self.origin_y, self.origin_z = origin
        self.cells = cells
        s = self.edge_length = int(th / sqrt(3))
        self.tw = self.edge_length * 2
        width = len(cells)
        height = len(cells[0])
        self.px_width = self.tw + (width - 1) * (s + s // 2)
        self.px_height = height * self.th
        if not width % 2:
            self.px_height += th // 2

    def get_in_region(self, left, bottom, right, top):
        """Return cells (in [column][row]) that are within the pixel bounds
        specified by the bottom-left (left, bottom) and top-right (right, top) corners.
        """
        ox = self.origin_x
        oy = self.origin_y
        col_width = self.tw // 2 + self.tw // 4
        left = max(0, (left - ox) // col_width - self.tw // 4)
        bottom = max(0, (bottom - oy) // self.th - 1)
        right = min(len(self.cells), right // col_width + 1)
        top = min(len(self.cells[0]), top // self.th + 1)
        return [self.cells[i][j] for i in range(int(left), int(right)) for j in range(int(bottom), int(top))]

    def get_key_at_pixel(self, x, y):
        """returns the grid coordinates for the hex that covers the point (x, y)

        Reference:
            Hexagonal grid math, by Ruslan Shestopalyuk
            http://blog.ruslans.com/2011/02/hexagonal-grid-math.html
        """
        radius = self.edge_length
        side = self.tw * 3 // 4
        height = self.th
        ci = int(floor(x / side))
        cx = int(x - side * ci)
        ty = int(y - ci % 2 * height / 2.0)
        cj = int(floor(1.0 * ty / height))
        cy = ty - height * cj
        if cx <= abs(radius / 2.0 - radius * cy / height):
            cj = cj + ci % 2 - (1 if cy < height / 2.0 else 0)
            ci = ci - 1
        return (ci, cj)

    def get_at_pixel(self, x, y):
        """Get the Cell at pixel (x,y).

        Return None if out of bounds."""
        return (self.get_cell)(*self.get_key_at_pixel(x, y))

    UP = 'up'
    DOWN = 'down'
    UP_LEFT = 'up left'
    UP_RIGHT = 'up right'
    DOWN_LEFT = 'down left'
    DOWN_RIGHT = 'down right'

    def get_neighbor(self, cell, direction):
        """Get the neighbor HexCell in the given direction which
        is one of self.UP, self.DOWN, self.UP_LEFT, self.UP_RIGHT,
        self.DOWN_LEFT or self.DOWN_RIGHT.

        Return None if out of bounds.
        """
        if direction is self.UP:
            return self.get_cell(cell.i, cell.j + 1)
            if direction is self.DOWN:
                return self.get_cell(cell.i, cell.j - 1)
            if direction is self.UP_LEFT:
                if cell.i % 2:
                    return self.get_cell(cell.i - 1, cell.j + 1)
                return self.get_cell(cell.i - 1, cell.j)
        elif direction is self.UP_RIGHT:
            if cell.i % 2:
                return self.get_cell(cell.i + 1, cell.j + 1)
            return self.get_cell(cell.i + 1, cell.j)
        elif direction is self.DOWN_LEFT:
            if cell.i % 2:
                return self.get_cell(cell.i - 1, cell.j)
            return self.get_cell(cell.i - 1, cell.j - 1)
        elif direction is self.DOWN_RIGHT:
            if cell.i % 2:
                return self.get_cell(cell.i + 1, cell.j)
            return self.get_cell(cell.i + 1, cell.j - 1)
        else:
            raise ValueError('Unknown direction %r' % direction)

    def get_neighbors(self, cell):
        """Get all neighbor cells for the nominated cell.

        Return a dict with the directions (self.UP, self.DOWN, etc) as keys
        and neighbor cells as values.
        """
        r = {}
        for direction in (
         self.UP_LEFT, self.UP, self.UP_RIGHT,
         self.DOWN_LEFT, self.DOWN, self.DOWN_RIGHT):
            dx, dy = direction
            r[direction] = self.get_cell(cell.i + dx, cell.j + dy)

        return r


class HexMapLayer(HexMap, MapLayer):
    """HexMapLayer"""

    def __init__(self, id, ignored, th, cells, origin=None, properties=None):
        HexMap.__init__(self, id, th, cells, origin, properties)
        MapLayer.__init__(self, properties)


class HexCell(Cell):
    """HexCell"""

    def __init__(self, i, j, ignored, height, properties, tile):
        width = hex_width(height)
        Cell.__init__(self, i, j, width, height, properties, tile)

    def get_origin(self):
        x = self.i * (self.width // 2 + self.width // 4)
        y = self.j * self.height
        if self.i % 2:
            y += self.height // 2
        return (x, y)

    origin = property(get_origin)

    def get_top(self):
        y = self.get_origin()[1]
        return y + self.height

    top = property(get_top)

    def get_bottom(self):
        return self.get_origin()[1]

    bottom = property(get_bottom)

    def get_center(self):
        x, y = self.get_origin()
        return (
         x + self.width // 2, y + self.height // 2)

    center = property(get_center)

    def get_midtop(self):
        x, y = self.get_origin()
        return (
         x + self.width // 2, y + self.height)

    midtop = property(get_midtop)

    def get_midbottom(self):
        x, y = self.get_origin()
        return (
         x + self.width // 2, y)

    midbottom = property(get_midbottom)

    def get_left(self):
        x, y = self.get_origin()
        return (
         x, y + self.height // 2)

    left = property(get_left)

    def get_right(self):
        x, y = self.get_origin()
        return (
         x + self.width, y + self.height // 2)

    right = property(get_right)

    def get_topleft(self):
        x, y = self.get_origin()
        return (
         x + self.width // 4, y + self.height)

    topleft = property(get_topleft)

    def get_topright(self):
        x, y = self.get_origin()
        return (
         x + self.width // 2 + self.width // 4, y + self.height)

    topright = property(get_topright)

    def get_bottomleft(self):
        x, y = self.get_origin()
        return (
         x + self.width // 4, y)

    bottomleft = property(get_bottomleft)

    def get_bottomright(self):
        x, y = self.get_origin()
        return (
         x + self.width // 2 + self.width // 4, y)

    bottomright = property(get_bottomright)

    def get_midtopleft(self):
        x, y = self.get_origin()
        return (
         x + self.width // 8, y + self.height // 2 + self.height // 4)

    midtopleft = property(get_midtopleft)

    def get_midtopright(self):
        x, y = self.get_origin()
        return (
         x + self.width // 2 + self.width // 4 + self.width // 8,
         y + self.height // 2 + self.height // 4)

    midtopright = property(get_midtopright)

    def get_midbottomleft(self):
        x, y = self.get_origin()
        return (
         x + self.width // 8, y + self.height // 4)

    midbottomleft = property(get_midbottomleft)

    def get_midbottomright(self):
        x, y = self.get_origin()
        return (
         x + self.width // 2 + self.width // 4 + self.width // 8,
         y + self.height // 4)

    midbottomright = property(get_midbottomright)


def parse_tmx_points(tag, obj_x, obj_y):
    """parses tmx tag points into left, bottom, right, top, points

    :Parameters:
        `tag` : xml tag
            assumed an object tag
        `obj_x` :
            object x position in gl coordinates
        `obj_y` :
            object y position in gl coordinates

    :Returns: tuple (left, bottom, width, height, points)
        left: leftmost x-position in points, gl coordinates system
        bottom: bottommost y-position in points, gl coordinates system
        width: width of point's enclosing box
        height: height of point's enclosing box
        points: list of points in a gl coordinates system relative to (left, bottom)
    """
    points_string = tag.attrib['points']
    points_parts = points_string.split(' ')
    pa = []
    for pair in points_parts:
        coords = pair.split(',')
        pa.append((float(coords[0]) + obj_x, -float(coords[1]) + obj_y))

    left = min([x for x, y in pa])
    bottom = min([y for x, y in pa])
    right = max([x for x, y in pa])
    top = max([y for x, y in pa])
    width = right - left + 1
    height = top - bottom + 1
    points = [(
     x - left, y - bottom) for x, y in pa]
    return (
     left, bottom, width, height, points)


def tmx_coords_to_gl(x, y, map_height):
    return (
     x, map_height - y)


class TmxObject(Rect):
    """TmxObject"""

    def __init__(self, tmxtype, usertype, x, y, width=0, height=0, name=None, gid=None, tile=None, visible=1, points=None):
        if tile:
            width = tile.image.width
            height = tile.image.height
        super(TmxObject, self).__init__(x, y, width, height)
        self.tmxtype = tmxtype
        self.px = x
        self.py = y
        self.usertype = usertype
        self.name = name
        self.gid = gid
        self.tile = tile
        self.visible = visible
        self.points = points
        self.properties = {}
        self._added_properties = {}
        self._deleted_properties = set()

    def __repr__(self):
        if self.tile:
            return '<TmxObject %s,%s %s,%s tile=%d>' % (self.px, self.py, self.width, self.height, self.gid)
        return '<TmxObject %s,%s %s,%s>' % (self.px, self.py, self.width, self.height)

    def __contains__(self, key):
        if key in self._deleted_properties:
            return False
        if key in self._added_properties:
            return True
        if key in self.properties:
            return True
        return self.tile and key in self.tile.properties

    def __getitem__(self, key):
        if key in self._deleted_properties:
            raise KeyError(key)
        else:
            if key in self._added_properties:
                return self._added_properties[key]
            if key in self.properties:
                return self.properties[key]
            if self.tile and key in self.tile.properties:
                return self.tile.properties[key]
        raise KeyError(key)

    def __setitem__(self, key, value):
        self._added_properties[key] = value

    def __delitem__(self, key):
        self._deleted_properties.add(key)

    def get--- This code section failed: ---

 L.1642         0  SETUP_FINALLY        12  'to 12'

 L.1643         2  LOAD_FAST                'self'
                4  LOAD_FAST                'key'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.1644        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    34  'to 34'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.1645        26  LOAD_FAST                'default'
               28  ROT_FOUR         
               30  POP_EXCEPT       
               32  RETURN_VALUE     
             34_0  COME_FROM            18  '18'
               34  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 12

    @classmethod
    def fromxml(cls, tag, tilesets, map_height):
        """
        :Parameters:
            `tag` : xml tag
                assumed an object tag
            `tileset` : enumerable giving tilesets
                only the tilesets used used by an object tile are needed, can be []
            `map_height` : int
                map height in pixels, needed to change coords from tmx to gl

        :Returns: a TmxObject instance
            attributes in the instance will store the info parsed from the class
        """
        left = float(tag.attrib['x'])
        top = map_height - float(tag.attrib['y'])
        bottom = None
        points = None
        if 'gid' in tag.attrib:
            tmxtype = 'tile'
            gid = int(tag.attrib['gid'])
            for ts in tilesets:
                if gid in ts:
                    tile = ts[gid]
                    break
                w = tile.image.width
                h = tile.image.height

        else:
            gid = None
            tile = None
            w = float(tag.attrib.get('width', 0))
            h = float(tag.attrib.get('height', 0))
            subtags = {}
            for c in tag.getchildren():
                subtags[c.tag] = c

            if 'ellipse' in subtags:
                tmxtype = 'ellipse'
            elif 'polygon' in subtags:
                tmxtype = 'polygon'
                left, bottom, w, h, points = parse_tmx_points(subtags['polygon'], left, top)
            elif 'polyline' in subtags:
                tmxtype = 'polyline'
                left, bottom, w, h, points = parse_tmx_points(subtags['polyline'], left, top)
            else:
                tmxtype = 'rect'
        if bottom is None:
            if tmxtype == 'tile':
                bottom = top
            else:
                bottom = top - h
        o = cls(tmxtype, tag.attrib.get('type'), left, bottom, w, h, tag.attrib.get('name'), gid, tile, int(tag.attrib.get('visible', 1)), points)
        props = tag.find('properties')
        if props is None:
            return o
        for c in props.findall('property'):
            name = c.attrib['name']
            value = c.attrib['value']
            if value.isdigit():
                value = int(value)
            o.properties[name] = value

        return o


class TmxObjectLayer(MapLayer):
    """TmxObjectLayer"""

    def __init__(self, name, color, objects, opacity=1, visible=1, position=(0, 0)):
        MapLayer.__init__(self, {})
        self.name = name
        self.color = color
        self.objects = objects
        self.opacity = opacity
        self.visible = visible
        self.position = position

    def __repr__(self):
        return '<TmxObjectLayer "%s" at 0x%x>' % (self.name, id(self))

    @classmethod
    def fromxml(cls, tag, tilesets, map_height):
        color = tag.attrib.get('color')
        if color:
            color = p_html._parse_color(color)
        layer = cls(tag.attrib['name'], color, [], float(tag.attrib.get('opacity', 1)), int(tag.attrib.get('visible', 1)))
        for obj in tag.findall('object'):
            layer.objects.append(TmxObject.fromxmlobjtilesetsmap_height)

        for c in tag.findall('property'):
            name = c.attrib['name']
            value = c.attrib['value']
            if value.isdigit():
                value = int(value)
            layer.properties[name] = value

        return layer

    def update(self, dt, *args):
        pass

    def find_cells(self, **requirements):
        """Find all objects with the given properties set.

        Called "find_cells" for compatibility with existing cocos tile API.
        """
        r = []
        for propname in requirements:
            for obj in self.objects:
                if obj:
                    if propname in obj or :
                        r.append(obj)

            return r

    def match(self, **properties):
        """Find all objects with the given properties set to the given values.
        """
        r = []
        for propname in properties:
            for obj in self.objects:
                if propname in obj:
                    val = obj[propname]
                else:
                    if propname in self.properties:
                        val = self.properties[propname]
                        break
                if properties[propname] == val:
                    r.append(obj)

            return r

    def collide(self, rect, propname):
        """Find all objects the rect is touching that have the indicated
        property name set.
        """
        r = []
        for obj in self.get_in_region(rect.left, rect.bottom, rect.right, rect.top):
            if propname in obj or propname in self.properties:
                r.append(obj)
            return r

    def get_in_region(self, left, bottom, right, top):
        """Return objects that overlaps any interior point of the rect with
        bottom-left (left, bottom) and top-right (right, top) corners.

        Return a list of TmxObject instances.
        """
        region = Rect(left, bottom, right - left, top - bottom)
        return [obj for obj in self.objects if obj.intersects(region)]

    def get_at(self, x, y):
        """Return the first object found at the nominated (x, y) coordinate.

        Return an TmxObject instance or None.
        """
        for obj in self.objects:
            if obj.contains(x, y):
                return obj

    def _update_sprite_set(self):
        self._sprites = {}
        color = self.color
        if color is None:
            color = [
             255] * 3
        color = tuple(color[:3] + [128])
        color_image = pyglet.image.SolidColorImagePattern(color)
        for cell in self.get_visible_cells():
            cx, cy = cell.origin[:2]
            if cell.tile:
                image = cell.tile.image
            else:
                image = color_image.create_image(int(cell.width), int(cell.height))
            if cell not in self._sprites:
                self._sprites[cell] = pyglet.sprite.Sprite(image, x=(int(cx)), y=(int(cy)), batch=(self.batch))


class RectMapCollider(object):
    """RectMapCollider"""

    def __init__(self):
        import warnings
        warnings.warn('RectMapCollider been has moved to cocos.mapcolliders and changed behavior', DeprecationWarning,
          stacklevel=2)
        import cocos.mapcolliders
        cocos.mapcolliders.RectMapWithPropsCollider()