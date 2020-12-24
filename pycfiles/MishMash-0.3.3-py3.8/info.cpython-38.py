# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/commands/info.py
# Compiled at: 2019-12-04 00:39:07
# Size of source mod 2**32: 3567 bytes
import sys
from nicfit.console.ansi import Fg, Style
from pyfiglet import figlet_format
from sqlalchemy.exc import ProgrammingError, OperationalError
from .. import version
from ..core import Command
from ..util import safeDbUrl
from ..orm import Track, Artist, Album, Meta, Tag, Library

class DisplayList:

    def __init__(self):
        self._rows = []

    def add(self, key, val):
        self._rows.append(tuple((key, val)))

    def print(self, _format, clear=False, **kwargs):
        k_width = max([len(k) for k, v in self._rows if k])
        for k, v in self._rows:
            if k:
                print((_format.format)(k=k.ljust(k_width), v=v, **kwargs))
        else:
            if clear:
                self.clear()

    def clear(self):
        self._rows.clear()


@Command.register
class Info(Command):
    NAME = 'info'
    HELP = 'Show information about the database and configuration.'
    _library_arg_nargs = '*'

    def _initArgParser(self, parser):
        super()._initArgParser(parser)
        parser.add_argument('--artists', dest='show_artists', action='store_true',
          help='List all artists, per library.')

    def lib_query(self, OrgType, lib):
        if isinstance(lib, int):
            lid = lib
        else:
            lid = lib.id
        return self.db_session.query(OrgType).filter_by(lib_id=lid)

    def _displayMetaInfo--- This code section failed: ---

 L.  56         0  LOAD_GLOBAL              DisplayList
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'display_list'

 L.  58         6  LOAD_CODE                <code_object mkkey>
                8  LOAD_STR                 'Info._displayMetaInfo.<locals>.mkkey'
               10  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               12  STORE_FAST               'mkkey'

 L.  61        14  LOAD_CODE                <code_object mkval>
               16  LOAD_STR                 'Info._displayMetaInfo.<locals>.mkval'
               18  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               20  STORE_FAST               'mkval'

 L.  64        22  LOAD_FAST                'display_list'
               24  LOAD_METHOD              add
               26  LOAD_FAST                'mkkey'
               28  LOAD_STR                 'Version'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_FAST                'mkval'
               34  LOAD_GLOBAL              version
               36  CALL_FUNCTION_1       1  ''
               38  CALL_METHOD_2         2  ''
               40  POP_TOP          

 L.  65        42  LOAD_FAST                'display_list'
               44  LOAD_METHOD              add
               46  LOAD_FAST                'mkkey'
               48  LOAD_STR                 'Database URL'
               50  CALL_FUNCTION_1       1  ''

 L.  66        52  LOAD_FAST                'mkval'
               54  LOAD_GLOBAL              safeDbUrl
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                config
               60  LOAD_ATTR                db_url
               62  CALL_FUNCTION_1       1  ''
               64  CALL_FUNCTION_1       1  ''

 L.  65        66  CALL_METHOD_2         2  ''
               68  POP_TOP          

 L.  67        70  SETUP_FINALLY        92  'to 92'

 L.  68        72  LOAD_FAST                'self'
               74  LOAD_ATTR                db_session
               76  LOAD_METHOD              query
               78  LOAD_GLOBAL              Meta
               80  CALL_METHOD_1         1  ''
               82  LOAD_METHOD              one
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'meta'
               88  POP_BLOCK        
               90  JUMP_FORWARD        158  'to 158'
             92_0  COME_FROM_FINALLY    70  '70'

 L.  69        92  DUP_TOP          
               94  LOAD_GLOBAL              ProgrammingError
               96  LOAD_GLOBAL              OperationalError
               98  BUILD_TUPLE_2         2 
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   156  'to 156'
              104  POP_TOP          
              106  STORE_FAST               'ex'
              108  POP_TOP          
              110  SETUP_FINALLY       144  'to 144'

 L.  70       112  LOAD_GLOBAL              print
              114  LOAD_STR                 '\nError querying metadata. Database may not be initialized: %s'

 L.  71       116  LOAD_GLOBAL              str
              118  LOAD_FAST                'ex'
              120  CALL_FUNCTION_1       1  ''

 L.  70       122  BINARY_MODULO    

 L.  71       124  LOAD_GLOBAL              sys
              126  LOAD_ATTR                stderr

 L.  70       128  LOAD_CONST               ('file',)
              130  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              132  POP_TOP          

 L.  72       134  POP_BLOCK        
              136  POP_EXCEPT       
              138  CALL_FINALLY        144  'to 144'
              140  LOAD_CONST               1
              142  RETURN_VALUE     
            144_0  COME_FROM           138  '138'
            144_1  COME_FROM_FINALLY   110  '110'
              144  LOAD_CONST               None
              146  STORE_FAST               'ex'
              148  DELETE_FAST              'ex'
              150  END_FINALLY      
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM           102  '102'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM            90  '90'

 L.  74       158  LOAD_FAST                'display_list'
              160  LOAD_METHOD              add
              162  LOAD_FAST                'mkkey'
              164  LOAD_STR                 'Database version'
              166  CALL_FUNCTION_1       1  ''
              168  LOAD_FAST                'mkval'
              170  LOAD_FAST                'meta'
              172  LOAD_ATTR                version
              174  CALL_FUNCTION_1       1  ''
              176  CALL_METHOD_2         2  ''
              178  POP_TOP          

 L.  75       180  LOAD_FAST                'display_list'
              182  LOAD_METHOD              add
              184  LOAD_FAST                'mkkey'
              186  LOAD_STR                 'Last sync'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_FAST                'mkval'
              192  LOAD_FAST                'meta'
              194  LOAD_ATTR                last_sync
              196  JUMP_IF_TRUE_OR_POP   200  'to 200'
              198  LOAD_STR                 'Never'
            200_0  COME_FROM           196  '196'
              200  CALL_FUNCTION_1       1  ''
              202  CALL_METHOD_2         2  ''
              204  POP_TOP          

 L.  76       206  LOAD_FAST                'display_list'
              208  LOAD_METHOD              add
              210  LOAD_FAST                'mkkey'
              212  LOAD_STR                 'Configuration files '
              214  CALL_FUNCTION_1       1  ''

 L.  77       216  LOAD_FAST                'mkval'
              218  LOAD_STR                 ', '
              220  LOAD_METHOD              join
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                args
              226  LOAD_ATTR                config
              228  LOAD_ATTR                input_filenames
              230  CALL_METHOD_1         1  ''
              232  CALL_FUNCTION_1       1  ''

 L.  76       234  CALL_METHOD_2         2  ''
              236  POP_TOP          

 L.  78       238  LOAD_FAST                'display_list'
              240  LOAD_ATTR                print
              242  LOAD_STR                 '{k} {delim} {v}'
              244  LOAD_GLOBAL              Style
              246  LOAD_METHOD              bright
              248  LOAD_STR                 ':'
              250  CALL_METHOD_1         1  ''
              252  LOAD_CONST               ('delim',)
              254  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              256  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 138

    def _displayLibraryInfo(self, lib):

        def mkkey(k):
            return Style.bright(str(k))

        display_list = DisplayList()
        for name, orm_type in (('tracks', Track), ('artists', Artist),
         (
          'albums', Album), ('tags', Tag)):
            count = self.lib_queryorm_typelib.count()
            display_list.addmkkey(count)name
        else:
            display_list.print('{k} music {v}', clear=True)

    def _displayArtists(self, lib):
        for a in self.lib_queryArtistlib.order_by(Artist.sort_name).all():
            print(a.name)

    def _run(self):
        logo = figlet_format('``MishMash``', font='graffiti')
        print(Fg.greenlogoStyle.BRIGHT)
        self._displayMetaInfo()
        for lib in Library.iterall((self.db_session), names=(self.args.libs)):
            if self.args.show_artists:
                print(Fg.green(f"\n=== {lib.name} library artists ==="))
                self._displayArtists(lib)
            else:
                print(Fg.green(f"\n=== {lib.name} library ==="))
                self._displayLibraryInfo(lib)