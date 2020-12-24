# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sql/magic.py
# Compiled at: 2020-05-02 10:55:33
# Size of source mod 2**32: 10050 bytes
import json, re
from string import Formatter
from IPython.core.magic import Magics, cell_magic, line_magic, magics_class, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display_javascript
from sqlalchemy.exc import OperationalError, ProgrammingError
import sql.connection, sql.parse, sql.run
try:
    from traitlets.config.configurable import Configurable
    from traitlets import Bool, Int, Unicode
except ImportError:
    from IPython.config.configurable import Configurable
    from IPython.utils.traitlets import Bool, Int, Unicode
else:
    try:
        from pandas.core.frame import DataFrame, Series
    except ImportError:
        DataFrame = None
        Series = None
    else:

        @magics_class
        class SqlMagic(Magics, Configurable):
            __doc__ = 'Runs SQL statement on a database, specified by SQLAlchemy connect string.\n\n    Provides the %%sql magic.'
            displaycon = Bool(True, config=True, help='Show connection string after execute')
            autolimit = Int(0,
              config=True,
              allow_none=True,
              help='Automatically limit the size of the returned result sets')
            style = Unicode('DEFAULT',
              config=True,
              help="Set the table printing style to any of prettytable's defined styles (currently DEFAULT, MSWORD_FRIENDLY, PLAIN_COLUMNS, RANDOM)")
            short_errors = Bool(True,
              config=True,
              help="Don't display the full traceback on SQL Programming Error")
            displaylimit = Int(None,
              config=True,
              allow_none=True,
              help='Automatically limit the number of rows displayed (full result set is still stored)')
            autopandas = Bool(False,
              config=True,
              help='Return Pandas DataFrames instead of regular result sets')
            column_local_vars = Bool(False,
              config=True, help='Return data into local variables from column names')
            feedback = Bool(True, config=True, help='Print number of rows affected by DML')
            dsn_filename = Unicode('odbc.ini',
              config=True,
              help='Path to DSN file. When the first argument is of the form [section], a sqlalchemy connection string is formed from the matching section in the DSN file.')
            autocommit = Bool(True, config=True, help='Set autocommit mode')

            def __init__(self, shell):
                Configurable.__init__(self, config=(shell.config))
                Magics.__init__(self, shell=shell)
                self.shell.configurables.append(self)

            @needs_local_scope
            @line_magic('sql')
            @cell_magic('sql')
            @magic_arguments()
            @argument('line', default='', nargs='*', type=str, help='sql')
            @argument('-l',
              '--connections', action='store_true', help='list active connections')
            @argument('-x', '--close', type=str, help='close a session by name')
            @argument('-c',
              '--creator', type=str, help='specify creator function for new connection')
            @argument('-s',
              '--section',
              type=str,
              help='section of dsn_file to be used for generating a connection string')
            @argument('-p',
              '--persist',
              action='store_true',
              help='create a table name in the database from the named DataFrame')
            @argument('--append',
              action='store_true',
              help='create, or append to, a table name in the database from the named DataFrame')
            @argument('-a',
              '--connection_arguments',
              type=str,
              help='specify dictionary of connection arguments to pass to SQL driver')
            @argument('-f', '--file', type=str, help='Run SQL from file at this path')
            def execute--- This code section failed: ---

 L. 146         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'SqlMagic.execute.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 147         6  LOAD_GLOBAL              Formatter
                8  CALL_FUNCTION_0       0  ''
               10  LOAD_METHOD              parse
               12  LOAD_FAST                'cell'
               14  CALL_METHOD_1         1  ''

 L. 146        16  GET_ITER         
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'cell_variables'

 L. 149        22  BUILD_MAP_0           0 
               24  STORE_FAST               'cell_params'

 L. 150        26  LOAD_FAST                'cell_variables'
               28  GET_ITER         
               30  FOR_ITER             48  'to 48'
               32  STORE_FAST               'variable'

 L. 151        34  LOAD_FAST                'local_ns'
               36  LOAD_FAST                'variable'
               38  BINARY_SUBSCR    
               40  LOAD_FAST                'cell_params'
               42  LOAD_FAST                'variable'
               44  STORE_SUBSCR     
               46  JUMP_BACK            30  'to 30'

 L. 152        48  LOAD_FAST                'cell'
               50  LOAD_ATTR                format
               52  BUILD_TUPLE_0         0 
               54  LOAD_FAST                'cell_params'
               56  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               58  STORE_FAST               'cell'

 L. 154        60  LOAD_GLOBAL              parse_argstring
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                execute
               66  LOAD_FAST                'line'
               68  CALL_FUNCTION_2       2  ''
               70  STORE_FAST               'args'

 L. 155        72  LOAD_FAST                'args'
               74  LOAD_ATTR                connections
               76  POP_JUMP_IF_FALSE    88  'to 88'

 L. 156        78  LOAD_GLOBAL              sql
               80  LOAD_ATTR                connection
               82  LOAD_ATTR                Connection
               84  LOAD_ATTR                connections
               86  RETURN_VALUE     
             88_0  COME_FROM            76  '76'

 L. 157        88  LOAD_FAST                'args'
               90  LOAD_ATTR                close
               92  POP_JUMP_IF_FALSE   110  'to 110'

 L. 158        94  LOAD_GLOBAL              sql
               96  LOAD_ATTR                connection
               98  LOAD_ATTR                Connection
              100  LOAD_METHOD              _close
              102  LOAD_FAST                'args'
              104  LOAD_ATTR                close
              106  CALL_METHOD_1         1  ''
              108  RETURN_VALUE     
            110_0  COME_FROM            92  '92'

 L. 161       110  LOAD_FAST                'self'
              112  LOAD_ATTR                shell
              114  LOAD_ATTR                user_ns
              116  LOAD_METHOD              copy
              118  CALL_METHOD_0         0  ''
              120  STORE_FAST               'user_ns'

 L. 162       122  LOAD_FAST                'user_ns'
              124  LOAD_METHOD              update
              126  LOAD_FAST                'local_ns'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L. 164       132  LOAD_STR                 ' '
              134  LOAD_METHOD              join
              136  LOAD_FAST                'args'
              138  LOAD_ATTR                line
              140  CALL_METHOD_1         1  ''
              142  LOAD_STR                 '\n'
              144  BINARY_ADD       
              146  LOAD_FAST                'cell'
              148  BINARY_ADD       
              150  STORE_FAST               'command_text'

 L. 166       152  LOAD_FAST                'args'
              154  LOAD_ATTR                file
              156  POP_JUMP_IF_FALSE   198  'to 198'

 L. 167       158  LOAD_GLOBAL              open
              160  LOAD_FAST                'args'
              162  LOAD_ATTR                file
              164  LOAD_STR                 'r'
              166  CALL_FUNCTION_2       2  ''
              168  SETUP_WITH          192  'to 192'
              170  STORE_FAST               'infile'

 L. 168       172  LOAD_FAST                'infile'
              174  LOAD_METHOD              read
              176  CALL_METHOD_0         0  ''
              178  LOAD_STR                 '\n'
              180  BINARY_ADD       
              182  LOAD_FAST                'command_text'
              184  BINARY_ADD       
              186  STORE_FAST               'command_text'
              188  POP_BLOCK        
              190  BEGIN_FINALLY    
            192_0  COME_FROM_WITH      168  '168'
              192  WITH_CLEANUP_START
              194  WITH_CLEANUP_FINISH
              196  END_FINALLY      
            198_0  COME_FROM           156  '156'

 L. 170       198  LOAD_GLOBAL              sql
              200  LOAD_ATTR                parse
              202  LOAD_METHOD              parse
              204  LOAD_FAST                'command_text'
              206  LOAD_FAST                'self'
              208  CALL_METHOD_2         2  ''
              210  STORE_FAST               'parsed'

 L. 172       212  LOAD_FAST                'parsed'
              214  LOAD_STR                 'connection'
              216  BINARY_SUBSCR    
              218  STORE_FAST               'connect_str'

 L. 173       220  LOAD_FAST                'args'
              222  LOAD_ATTR                section
              224  POP_JUMP_IF_FALSE   242  'to 242'

 L. 174       226  LOAD_GLOBAL              sql
              228  LOAD_ATTR                parse
              230  LOAD_METHOD              connection_from_dsn_section
              232  LOAD_FAST                'args'
              234  LOAD_ATTR                section
              236  LOAD_FAST                'self'
              238  CALL_METHOD_2         2  ''
              240  STORE_FAST               'connect_str'
            242_0  COME_FROM           224  '224'

 L. 176       242  LOAD_FAST                'args'
              244  LOAD_ATTR                connection_arguments
          246_248  POP_JUMP_IF_FALSE   394  'to 394'

 L. 177       250  SETUP_FINALLY       344  'to 344'

 L. 179       252  LOAD_FAST                'args'
              254  LOAD_ATTR                connection_arguments
              256  STORE_FAST               'raw_args'

 L. 180       258  LOAD_GLOBAL              len
              260  LOAD_FAST                'raw_args'
              262  CALL_FUNCTION_1       1  ''
              264  LOAD_CONST               1
              266  COMPARE_OP               >
          268_270  POP_JUMP_IF_FALSE   328  'to 328'

 L. 181       272  LOAD_STR                 '"'
              274  LOAD_STR                 "'"
              276  BUILD_LIST_2          2 
              278  STORE_FAST               'targets'

 L. 182       280  LOAD_FAST                'raw_args'
              282  LOAD_CONST               0
              284  BINARY_SUBSCR    
              286  STORE_FAST               'head'

 L. 183       288  LOAD_FAST                'raw_args'
              290  LOAD_CONST               -1
              292  BINARY_SUBSCR    
              294  STORE_FAST               'tail'

 L. 184       296  LOAD_FAST                'head'
              298  LOAD_FAST                'targets'
              300  COMPARE_OP               in
          302_304  POP_JUMP_IF_FALSE   328  'to 328'
              306  LOAD_FAST                'head'
              308  LOAD_FAST                'tail'
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   328  'to 328'

 L. 185       316  LOAD_FAST                'raw_args'
              318  LOAD_CONST               1
              320  LOAD_CONST               -1
              322  BUILD_SLICE_2         2 
              324  BINARY_SUBSCR    
              326  STORE_FAST               'raw_args'
            328_0  COME_FROM           312  '312'
            328_1  COME_FROM           302  '302'
            328_2  COME_FROM           268  '268'

 L. 186       328  LOAD_GLOBAL              json
              330  LOAD_METHOD              loads
              332  LOAD_FAST                'raw_args'
              334  CALL_METHOD_1         1  ''
              336  LOAD_FAST                'args'
              338  STORE_ATTR               connection_arguments
              340  POP_BLOCK        
              342  JUMP_FORWARD        392  'to 392'
            344_0  COME_FROM_FINALLY   250  '250'

 L. 187       344  DUP_TOP          
              346  LOAD_GLOBAL              Exception
              348  COMPARE_OP               exception-match
          350_352  POP_JUMP_IF_FALSE   390  'to 390'
              354  POP_TOP          
              356  STORE_FAST               'e'
              358  POP_TOP          
              360  SETUP_FINALLY       378  'to 378'

 L. 188       362  LOAD_GLOBAL              print
              364  LOAD_FAST                'e'
              366  CALL_FUNCTION_1       1  ''
              368  POP_TOP          

 L. 189       370  LOAD_FAST                'e'
              372  RAISE_VARARGS_1       1  'exception instance'
              374  POP_BLOCK        
              376  BEGIN_FINALLY    
            378_0  COME_FROM_FINALLY   360  '360'
              378  LOAD_CONST               None
              380  STORE_FAST               'e'
              382  DELETE_FAST              'e'
              384  END_FINALLY      
              386  POP_EXCEPT       
              388  JUMP_FORWARD        392  'to 392'
            390_0  COME_FROM           350  '350'
              390  END_FINALLY      
            392_0  COME_FROM           388  '388'
            392_1  COME_FROM           342  '342'
              392  JUMP_FORWARD        400  'to 400'
            394_0  COME_FROM           246  '246'

 L. 191       394  BUILD_MAP_0           0 
              396  LOAD_FAST                'args'
              398  STORE_ATTR               connection_arguments
            400_0  COME_FROM           392  '392'

 L. 192       400  LOAD_FAST                'args'
              402  LOAD_ATTR                creator
          404_406  POP_JUMP_IF_FALSE   420  'to 420'

 L. 193       408  LOAD_FAST                'user_ns'
              410  LOAD_FAST                'args'
              412  LOAD_ATTR                creator
              414  BINARY_SUBSCR    
              416  LOAD_FAST                'args'
              418  STORE_ATTR               creator
            420_0  COME_FROM           404  '404'

 L. 195       420  SETUP_FINALLY       458  'to 458'

 L. 196       422  LOAD_GLOBAL              sql
              424  LOAD_ATTR                connection
              426  LOAD_ATTR                Connection
              428  LOAD_ATTR                set

 L. 197       430  LOAD_FAST                'parsed'
              432  LOAD_STR                 'connection'
              434  BINARY_SUBSCR    

 L. 198       436  LOAD_FAST                'self'
              438  LOAD_ATTR                displaycon

 L. 199       440  LOAD_FAST                'args'
              442  LOAD_ATTR                connection_arguments

 L. 200       444  LOAD_FAST                'args'
              446  LOAD_ATTR                creator

 L. 196       448  LOAD_CONST               ('displaycon', 'connect_args', 'creator')
              450  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              452  STORE_FAST               'conn'
              454  POP_BLOCK        
              456  JUMP_FORWARD        524  'to 524'
            458_0  COME_FROM_FINALLY   420  '420'

 L. 202       458  DUP_TOP          
              460  LOAD_GLOBAL              Exception
              462  COMPARE_OP               exception-match
          464_466  POP_JUMP_IF_FALSE   522  'to 522'
              468  POP_TOP          
              470  STORE_FAST               'e'
              472  POP_TOP          
              474  SETUP_FINALLY       510  'to 510'

 L. 203       476  LOAD_GLOBAL              print
              478  LOAD_FAST                'e'
              480  CALL_FUNCTION_1       1  ''
              482  POP_TOP          

 L. 204       484  LOAD_GLOBAL              print
              486  LOAD_GLOBAL              sql
              488  LOAD_ATTR                connection
              490  LOAD_ATTR                Connection
              492  LOAD_METHOD              tell_format
              494  CALL_METHOD_0         0  ''
              496  CALL_FUNCTION_1       1  ''
              498  POP_TOP          

 L. 205       500  POP_BLOCK        
              502  POP_EXCEPT       
              504  CALL_FINALLY        510  'to 510'
              506  LOAD_CONST               None
              508  RETURN_VALUE     
            510_0  COME_FROM           504  '504'
            510_1  COME_FROM_FINALLY   474  '474'
              510  LOAD_CONST               None
              512  STORE_FAST               'e'
              514  DELETE_FAST              'e'
              516  END_FINALLY      
              518  POP_EXCEPT       
              520  JUMP_FORWARD        524  'to 524'
            522_0  COME_FROM           464  '464'
              522  END_FINALLY      
            524_0  COME_FROM           520  '520'
            524_1  COME_FROM           456  '456'

 L. 207       524  LOAD_FAST                'args'
              526  LOAD_ATTR                persist
          528_530  POP_JUMP_IF_FALSE   554  'to 554'

 L. 208       532  LOAD_FAST                'self'
              534  LOAD_ATTR                _persist_dataframe
              536  LOAD_FAST                'parsed'
              538  LOAD_STR                 'sql'
              540  BINARY_SUBSCR    
              542  LOAD_FAST                'conn'
              544  LOAD_FAST                'user_ns'
              546  LOAD_CONST               False
              548  LOAD_CONST               ('append',)
              550  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              552  RETURN_VALUE     
            554_0  COME_FROM           528  '528'

 L. 210       554  LOAD_FAST                'args'
              556  LOAD_ATTR                append
          558_560  POP_JUMP_IF_FALSE   584  'to 584'

 L. 211       562  LOAD_FAST                'self'
              564  LOAD_ATTR                _persist_dataframe
              566  LOAD_FAST                'parsed'
              568  LOAD_STR                 'sql'
              570  BINARY_SUBSCR    
              572  LOAD_FAST                'conn'
              574  LOAD_FAST                'user_ns'
              576  LOAD_CONST               True
              578  LOAD_CONST               ('append',)
              580  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              582  RETURN_VALUE     
            584_0  COME_FROM           558  '558'

 L. 213       584  LOAD_FAST                'parsed'
              586  LOAD_STR                 'sql'
              588  BINARY_SUBSCR    
          590_592  POP_JUMP_IF_TRUE    598  'to 598'

 L. 214       594  LOAD_CONST               None
              596  RETURN_VALUE     
            598_0  COME_FROM           590  '590'

 L. 216       598  SETUP_FINALLY       798  'to 798'

 L. 217       600  LOAD_GLOBAL              sql
              602  LOAD_ATTR                run
              604  LOAD_METHOD              run
              606  LOAD_FAST                'conn'
              608  LOAD_FAST                'parsed'
              610  LOAD_STR                 'sql'
              612  BINARY_SUBSCR    
              614  LOAD_FAST                'self'
              616  LOAD_FAST                'user_ns'
              618  CALL_METHOD_4         4  ''
              620  STORE_FAST               'result'

 L. 220       622  LOAD_FAST                'result'
              624  LOAD_CONST               None
              626  COMPARE_OP               is-not

 L. 219   628_630  POP_JUMP_IF_FALSE   732  'to 732'

 L. 221       632  LOAD_GLOBAL              isinstance
              634  LOAD_FAST                'result'
              636  LOAD_GLOBAL              str
              638  CALL_FUNCTION_2       2  ''

 L. 219   640_642  POP_JUMP_IF_TRUE    732  'to 732'

 L. 222       644  LOAD_FAST                'self'
              646  LOAD_ATTR                column_local_vars

 L. 219   648_650  POP_JUMP_IF_FALSE   732  'to 732'

 L. 227       652  LOAD_FAST                'self'
              654  LOAD_ATTR                autopandas
          656_658  POP_JUMP_IF_FALSE   670  'to 670'

 L. 228       660  LOAD_FAST                'result'
              662  LOAD_METHOD              keys
              664  CALL_METHOD_0         0  ''
              666  STORE_FAST               'keys'
              668  JUMP_FORWARD        684  'to 684'
            670_0  COME_FROM           656  '656'

 L. 230       670  LOAD_FAST                'result'
              672  LOAD_ATTR                keys
              674  STORE_FAST               'keys'

 L. 231       676  LOAD_FAST                'result'
              678  LOAD_METHOD              dict
              680  CALL_METHOD_0         0  ''
              682  STORE_FAST               'result'
            684_0  COME_FROM           668  '668'

 L. 233       684  LOAD_FAST                'self'
              686  LOAD_ATTR                feedback
          688_690  POP_JUMP_IF_FALSE   712  'to 712'

 L. 234       692  LOAD_GLOBAL              print

 L. 235       694  LOAD_STR                 'Returning data to local variables [{}]'
              696  LOAD_METHOD              format
              698  LOAD_STR                 ', '
              700  LOAD_METHOD              join
              702  LOAD_FAST                'keys'
              704  CALL_METHOD_1         1  ''
              706  CALL_METHOD_1         1  ''

 L. 234       708  CALL_FUNCTION_1       1  ''
              710  POP_TOP          
            712_0  COME_FROM           688  '688'

 L. 238       712  LOAD_FAST                'self'
              714  LOAD_ATTR                shell
              716  LOAD_ATTR                user_ns
              718  LOAD_METHOD              update
              720  LOAD_FAST                'result'
              722  CALL_METHOD_1         1  ''
              724  POP_TOP          

 L. 240       726  POP_BLOCK        
              728  LOAD_CONST               None
              730  RETURN_VALUE     
            732_0  COME_FROM           648  '648'
            732_1  COME_FROM           640  '640'
            732_2  COME_FROM           628  '628'

 L. 243       732  LOAD_FAST                'parsed'
              734  LOAD_STR                 'result_var'
              736  BINARY_SUBSCR    
          738_740  POP_JUMP_IF_FALSE   788  'to 788'

 L. 244       742  LOAD_FAST                'parsed'
              744  LOAD_STR                 'result_var'
              746  BINARY_SUBSCR    
              748  STORE_FAST               'result_var'

 L. 245       750  LOAD_GLOBAL              print
              752  LOAD_STR                 'Returning data to local variable {}'
              754  LOAD_METHOD              format
              756  LOAD_FAST                'result_var'
              758  CALL_METHOD_1         1  ''
              760  CALL_FUNCTION_1       1  ''
              762  POP_TOP          

 L. 246       764  LOAD_FAST                'self'
              766  LOAD_ATTR                shell
              768  LOAD_ATTR                user_ns
              770  LOAD_METHOD              update
              772  LOAD_FAST                'result_var'
              774  LOAD_FAST                'result'
              776  BUILD_MAP_1           1 
              778  CALL_METHOD_1         1  ''
              780  POP_TOP          

 L. 247       782  POP_BLOCK        
              784  LOAD_CONST               None
              786  RETURN_VALUE     
            788_0  COME_FROM           738  '738'

 L. 250       788  LOAD_FAST                'result'
              790  POP_BLOCK        
              792  RETURN_VALUE     
              794  POP_BLOCK        
              796  JUMP_FORWARD        858  'to 858'
            798_0  COME_FROM_FINALLY   598  '598'

 L. 252       798  DUP_TOP          
              800  LOAD_GLOBAL              ProgrammingError
              802  LOAD_GLOBAL              OperationalError
              804  BUILD_TUPLE_2         2 
              806  COMPARE_OP               exception-match
          808_810  POP_JUMP_IF_FALSE   856  'to 856'
              812  POP_TOP          
              814  STORE_FAST               'e'
              816  POP_TOP          
              818  SETUP_FINALLY       844  'to 844'

 L. 254       820  LOAD_FAST                'self'
              822  LOAD_ATTR                short_errors
          824_826  POP_JUMP_IF_FALSE   838  'to 838'

 L. 255       828  LOAD_GLOBAL              print
              830  LOAD_FAST                'e'
              832  CALL_FUNCTION_1       1  ''
              834  POP_TOP          
              836  JUMP_FORWARD        840  'to 840'
            838_0  COME_FROM           824  '824'

 L. 257       838  RAISE_VARARGS_0       0  'reraise'
            840_0  COME_FROM           836  '836'
              840  POP_BLOCK        
              842  BEGIN_FINALLY    
            844_0  COME_FROM_FINALLY   818  '818'
              844  LOAD_CONST               None
              846  STORE_FAST               'e'
              848  DELETE_FAST              'e'
              850  END_FINALLY      
              852  POP_EXCEPT       
              854  JUMP_FORWARD        858  'to 858'
            856_0  COME_FROM           808  '808'
              856  END_FINALLY      
            858_0  COME_FROM           854  '854'
            858_1  COME_FROM           796  '796'

Parse error at or near `CALL_FINALLY' instruction at offset 504

            legal_sql_identifier = re.compile('^[A-Za-z0-9#_$]+')

            def _persist_dataframe(self, raw, conn, user_ns, append=False):
                """Implements PERSIST, which writes a DataFrame to the RDBMS"""
                if not DataFrame:
                    raise ImportError('Must `pip install pandas` to use DataFrames')
                else:
                    frame_name = raw.strip(';')
                    if not frame_name:
                        raise SyntaxError('Syntax: %sql PERSIST <name_of_data_frame>')
                    frame = evalframe_nameuser_ns
                    if not (isinstanceframeDataFrame or isinstanceframeSeries):
                        raise TypeError('%s is not a Pandas DataFrame or Series' % frame_name)
                table_name = frame_name.lower
                table_name = self.legal_sql_identifier.search(table_name).group(0)
                if_exists = 'append' if append else 'fail'
                frame.to_sql(table_name, (conn.session.engine), if_exists=if_exists)
                return 'Persisted %s' % table_name


        def load_ipython_extension(ip):
            """Load the extension in IPython."""
            ip.register_magics(SqlMagic)