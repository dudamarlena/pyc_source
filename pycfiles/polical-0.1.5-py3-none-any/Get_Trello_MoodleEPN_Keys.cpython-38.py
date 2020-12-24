# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/Get_Trello_MoodleEPN_Keys.py
# Compiled at: 2020-05-13 11:55:58
# Size of source mod 2**32: 11069 bytes
import yaml, os, webbrowser, trello, sys
from polical import configuration
from polical import connectSQLite
from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenRequestDenied
import logging
logging.basicConfig(filename=(configuration.get_file_location('Running.log')), level=(logging.INFO), format='%(asctime)s:%(levelname)s:%(message)s')

class DevNullRedirect:
    """DevNullRedirect"""

    def __enter__(self):
        self.old_stderr = os.dup(2)
        self.old_stdout = os.dup(1)
        os.close(2)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)

    def __exit__(self, exc_type, exc_value, traceback):
        os.dup2(self.old_stderr, 2)
        os.dup2(self.old_stdout, 1)


def onboard--- This code section failed: ---

 L.  39         0  LOAD_STR                 ''
                2  STORE_FAST               'username'

 L.  40         4  LOAD_GLOBAL              configuration
                6  LOAD_METHOD              get_file_location
                8  LOAD_FAST                'output_path'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'output_file'

 L.  41        14  LOAD_STR                 'https://trello.com/app-key'
               16  STORE_FAST               'user_api_key_url'

 L.  42        18  LOAD_STR                 'https://trello.com/1/OAuthGetRequestToken'
               20  STORE_FAST               'request_token_url'

 L.  43        22  LOAD_STR                 'https://trello.com/1/OAuthAuthorizeToken'
               24  STORE_FAST               'authorize_url'

 L.  44        26  LOAD_STR                 'https://trello.com/1/OAuthGetAccessToken'
               28  STORE_FAST               'access_token_url'

 L.  45        30  LOAD_STR                 'https://educacionvirtual.epn.edu.ec/calendar/view.php?view=upcoming&course=1'
               32  STORE_FAST               'calendar_moodle_epn_url'

 L.  47        34  LOAD_GLOBAL              logging
               36  LOAD_METHOD              info
               38  LOAD_STR                 'Mostrando print-board al usuario'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L.  48        44  LOAD_GLOBAL              print
               46  LOAD_STR                 'Bienvenido a PoliCal! Recuerde que antes de iniciar el proceso de obtención de credenciales ud debe tener una cuenta en Trello y en el Aula Virtual, y deben estar iniciadas las sesiones en el navegador predeterminado'
               48  CALL_FUNCTION_1       1  ''
               50  POP_TOP          

 L.  49        52  LOAD_GLOBAL              print
               54  LOAD_STR                 '\n\n'
               56  CALL_FUNCTION_1       1  ''
               58  POP_TOP          

 L.  50        60  LOAD_GLOBAL              input
               62  LOAD_STR                 'Ingrese su nombre:'
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'username'

 L.  51        68  LOAD_GLOBAL              print
               70  LOAD_STR                 'PASO 1: Acceso a Trello'
               72  CALL_FUNCTION_1       1  ''
               74  POP_TOP          

 L.  52        76  LOAD_GLOBAL              print
               78  LOAD_STR                 'En su navegador web se cargará el siguiente URL:'
               80  CALL_FUNCTION_1       1  ''
               82  POP_TOP          

 L.  53        84  LOAD_GLOBAL              print
               86  LOAD_STR                 '  '
               88  LOAD_FAST                'user_api_key_url'
               90  BINARY_ADD       
               92  CALL_FUNCTION_1       1  ''
               94  POP_TOP          

 L.  54        96  LOAD_GLOBAL              print
               98  LOAD_STR                 'Cuando llegue a esa página, inicie sesión y copie la "Tecla" o "Key" que se muestra en un cuadro de texto.'
              100  CALL_FUNCTION_1       1  ''
              102  POP_TOP          

 L.  55       104  LOAD_GLOBAL              print
              106  LOAD_STR                 'Si es la primera vez que realiza este proceso debe aceptar los terminos y condiciones de Trello'
              108  CALL_FUNCTION_1       1  ''
              110  POP_TOP          

 L.  56       112  LOAD_GLOBAL              input
              114  LOAD_STR                 'Presione ENTER para ir al enlace'
              116  CALL_FUNCTION_1       1  ''
              118  POP_TOP          

 L.  57       120  LOAD_FAST                'no_open'
              122  POP_JUMP_IF_TRUE    152  'to 152'

 L.  58       124  LOAD_GLOBAL              DevNullRedirect
              126  CALL_FUNCTION_0       0  ''
              128  SETUP_WITH          146  'to 146'
              130  POP_TOP          

 L.  59       132  LOAD_GLOBAL              webbrowser
              134  LOAD_METHOD              open_new_tab
              136  LOAD_FAST                'user_api_key_url'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  POP_BLOCK        
              144  BEGIN_FINALLY    
            146_0  COME_FROM_WITH      128  '128'
              146  WITH_CLEANUP_START
              148  WITH_CLEANUP_FINISH
              150  END_FINALLY      
            152_0  COME_FROM           122  '122'

 L.  60       152  LOAD_GLOBAL              input
              154  LOAD_STR                 'Por favor, introduzca el valor de "Tecla" o "Key":'
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'api_key'

 L.  61       160  LOAD_GLOBAL              print
              162  LOAD_STR                 'Ahora desplácese hasta la parte inferior de la página y copie el "Secreto" o "Secret" que se muestra en un cuadro de texto.'
              164  CALL_FUNCTION_1       1  ''
              166  POP_TOP          

 L.  62       168  LOAD_GLOBAL              input
              170  LOAD_STR                 'Por favor, introduzca el valor de "Secret":'
              172  CALL_FUNCTION_1       1  ''
              174  STORE_FAST               'api_secret'

 L.  64       176  LOAD_GLOBAL              print
              178  LOAD_STR                 '\n\n'
              180  CALL_FUNCTION_1       1  ''
              182  POP_TOP          

 L.  65       184  LOAD_GLOBAL              print
              186  LOAD_STR                 'PASO 2: Permitir acceso de Polical a Trello'
              188  CALL_FUNCTION_1       1  ''
              190  POP_TOP          

 L.  66       192  LOAD_GLOBAL              print
              194  LOAD_STR                 'Ahora obtendremos las credenciales de OAuth necesarias para usar este programa...'
              196  CALL_FUNCTION_1       1  ''
              198  POP_TOP          

 L.  74       200  LOAD_GLOBAL              OAuth1Session
              202  LOAD_FAST                'api_key'
              204  LOAD_FAST                'api_secret'
              206  LOAD_CONST               ('client_key', 'client_secret')
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  STORE_FAST               'session'

 L.  75       212  SETUP_FINALLY       228  'to 228'

 L.  76       214  LOAD_FAST                'session'
              216  LOAD_METHOD              fetch_request_token
              218  LOAD_FAST                'request_token_url'
              220  CALL_METHOD_1         1  ''
              222  STORE_FAST               'response'
              224  POP_BLOCK        
              226  JUMP_FORWARD        276  'to 276'
            228_0  COME_FROM_FINALLY   212  '212'

 L.  77       228  DUP_TOP          
              230  LOAD_GLOBAL              TokenRequestDenied
              232  COMPARE_OP               exception-match
          234_236  POP_JUMP_IF_FALSE   274  'to 274'
              238  POP_TOP          
              240  POP_TOP          
              242  POP_TOP          

 L.  78       244  LOAD_GLOBAL              print

 L.  79       246  LOAD_STR                 'Invalid API key/secret provided: {0} / {1}'
              248  LOAD_METHOD              format
              250  LOAD_FAST                'api_key'
              252  LOAD_FAST                'api_secret'
              254  CALL_METHOD_2         2  ''

 L.  78       256  CALL_FUNCTION_1       1  ''
              258  POP_TOP          

 L.  80       260  LOAD_GLOBAL              sys
              262  LOAD_METHOD              exit
              264  LOAD_CONST               1
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          
              270  POP_EXCEPT       
              272  JUMP_FORWARD        276  'to 276'
            274_0  COME_FROM           234  '234'
              274  END_FINALLY      
            276_0  COME_FROM           272  '272'
            276_1  COME_FROM           226  '226'

 L.  81       276  LOAD_FAST                'response'
              278  LOAD_METHOD              get

 L.  82       280  LOAD_STR                 'oauth_token'

 L.  81       282  CALL_METHOD_1         1  ''

 L.  82       284  LOAD_FAST                'response'
              286  LOAD_METHOD              get
              288  LOAD_STR                 'oauth_token_secret'
              290  CALL_METHOD_1         1  ''

 L.  81       292  ROT_TWO          
              294  STORE_FAST               'resource_owner_key'
              296  STORE_FAST               'resource_owner_secret'

 L.  86       298  LOAD_STR                 '{authorize_url}?oauth_token={oauth_token}&scope={scope}&expiration={expiration}&name={name}'
              300  LOAD_ATTR                format

 L.  87       302  LOAD_FAST                'authorize_url'

 L.  88       304  LOAD_FAST                'resource_owner_key'

 L.  89       306  LOAD_STR                 'never'

 L.  90       308  LOAD_STR                 'read,write'

 L.  91       310  LOAD_STR                 'PoliCal'

 L.  86       312  LOAD_CONST               ('authorize_url', 'oauth_token', 'expiration', 'scope', 'name')
              314  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              316  STORE_FAST               'user_confirmation_url'

 L.  93       318  LOAD_GLOBAL              print
              320  LOAD_STR                 'Visite la siguiente URL en su navegador web para autorizar a PoliCal acceso a su cuenta:'
              322  CALL_FUNCTION_1       1  ''
              324  POP_TOP          

 L.  94       326  LOAD_GLOBAL              print
              328  LOAD_STR                 '  '
              330  LOAD_FAST                'user_confirmation_url'
              332  BINARY_ADD       
              334  CALL_FUNCTION_1       1  ''
              336  POP_TOP          

 L.  95       338  LOAD_GLOBAL              print
              340  LOAD_STR                 'Concedale los permisos a PoliCal para acceder a sus datos de Trello, estas credenciales se mantendran de manera local'
              342  CALL_FUNCTION_1       1  ''
              344  POP_TOP          

 L.  96       346  LOAD_GLOBAL              input
              348  LOAD_STR                 'Presione ENTER para ir al enlace'
              350  CALL_FUNCTION_1       1  ''
              352  POP_TOP          

 L.  97       354  LOAD_FAST                'no_open'
          356_358  POP_JUMP_IF_TRUE    388  'to 388'

 L.  98       360  LOAD_GLOBAL              DevNullRedirect
              362  CALL_FUNCTION_0       0  ''
              364  SETUP_WITH          382  'to 382'
              366  POP_TOP          

 L.  99       368  LOAD_GLOBAL              webbrowser
              370  LOAD_METHOD              open_new_tab
              372  LOAD_FAST                'user_confirmation_url'
              374  CALL_METHOD_1         1  ''
              376  POP_TOP          
              378  POP_BLOCK        
              380  BEGIN_FINALLY    
            382_0  COME_FROM_WITH      364  '364'
              382  WITH_CLEANUP_START
              384  WITH_CLEANUP_FINISH
              386  END_FINALLY      
            388_0  COME_FROM           356  '356'

 L. 103       388  LOAD_GLOBAL              input

 L. 104       390  LOAD_STR                 '¿Has autorizado a PoliCal? Escriba n para no y S para si:'

 L. 103       392  CALL_FUNCTION_1       1  ''
              394  STORE_FAST               'confirmation'

 L. 105       396  LOAD_FAST                'confirmation'
              398  LOAD_STR                 'n'
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   418  'to 418'

 L. 106       406  LOAD_GLOBAL              input

 L. 107       408  LOAD_STR                 '¿Has autorizado a PoliCal? Escriba n para no y S para si:'

 L. 106       410  CALL_FUNCTION_1       1  ''
              412  STORE_FAST               'confirmation'
          414_416  JUMP_BACK           396  'to 396'
            418_0  COME_FROM           402  '402'

 L. 109       418  LOAD_GLOBAL              input
              420  LOAD_STR                 '¿Cuál es el código de verificación?:'
              422  CALL_FUNCTION_1       1  ''
              424  LOAD_METHOD              strip
              426  CALL_METHOD_0         0  ''
              428  STORE_FAST               'oauth_verifier'

 L. 115       430  LOAD_GLOBAL              OAuth1Session

 L. 116       432  LOAD_FAST                'api_key'

 L. 117       434  LOAD_FAST                'api_secret'

 L. 118       436  LOAD_FAST                'resource_owner_key'

 L. 119       438  LOAD_FAST                'resource_owner_secret'

 L. 120       440  LOAD_FAST                'oauth_verifier'

 L. 115       442  LOAD_CONST               ('client_key', 'client_secret', 'resource_owner_key', 'resource_owner_secret', 'verifier')
              444  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              446  STORE_FAST               'session'

 L. 122       448  LOAD_FAST                'session'
              450  LOAD_METHOD              fetch_access_token
              452  LOAD_FAST                'access_token_url'
              454  CALL_METHOD_1         1  ''
              456  STORE_FAST               'access_token'

 L. 126       458  LOAD_GLOBAL              print
              460  LOAD_STR                 '\n\n'
              462  CALL_FUNCTION_1       1  ''
              464  POP_TOP          

 L. 127       466  LOAD_GLOBAL              print
              468  LOAD_STR                 'PASO 3: Obtención del calendario del Aula Virtual'
              470  CALL_FUNCTION_1       1  ''
              472  POP_TOP          

 L. 128       474  LOAD_GLOBAL              print
              476  LOAD_STR                 'A continuación se abrirá un link hacia el Aula Virtual EPN, en proximos eventos para: elija Todos los cursos'
              478  CALL_FUNCTION_1       1  ''
              480  POP_TOP          

 L. 129       482  LOAD_GLOBAL              print
              484  LOAD_STR                 'y a continuación desplácese a la parte más inferior de la página y de clic en el botón Exportar Calendario'
              486  CALL_FUNCTION_1       1  ''
              488  POP_TOP          

 L. 130       490  LOAD_GLOBAL              print
              492  LOAD_STR                 'Luego, en la opción Exportar seleccione todos los eventos y después en "para" seleccione los 60 días recientes y próximos'
              494  CALL_FUNCTION_1       1  ''
              496  POP_TOP          

 L. 131       498  LOAD_GLOBAL              print
              500  LOAD_STR                 'Finalmente de clic en el boton Obtener URL del calendario'
              502  CALL_FUNCTION_1       1  ''
              504  POP_TOP          

 L. 132       506  LOAD_GLOBAL              print
              508  LOAD_STR                 'Visite la siguiente URL en su navegador web para obtener el calendario del aula virtual EPN:'
              510  CALL_FUNCTION_1       1  ''
              512  POP_TOP          

 L. 133       514  LOAD_GLOBAL              print
              516  LOAD_STR                 '  '
              518  LOAD_FAST                'calendar_moodle_epn_url'
              520  BINARY_ADD       
              522  CALL_FUNCTION_1       1  ''
              524  POP_TOP          

 L. 134       526  LOAD_GLOBAL              input
              528  LOAD_STR                 'Presione ENTER para ir al enlace e iniciar el proceso, no olvide verificar si su sesión del Aula Virtual se encuentra activa'
              530  CALL_FUNCTION_1       1  ''
              532  POP_TOP          

 L. 135       534  LOAD_FAST                'no_open'
          536_538  POP_JUMP_IF_TRUE    568  'to 568'

 L. 136       540  LOAD_GLOBAL              DevNullRedirect
              542  CALL_FUNCTION_0       0  ''
              544  SETUP_WITH          562  'to 562'
              546  POP_TOP          

 L. 137       548  LOAD_GLOBAL              webbrowser
              550  LOAD_METHOD              open_new_tab
              552  LOAD_FAST                'calendar_moodle_epn_url'
              554  CALL_METHOD_1         1  ''
              556  POP_TOP          
              558  POP_BLOCK        
              560  BEGIN_FINALLY    
            562_0  COME_FROM_WITH      544  '544'
              562  WITH_CLEANUP_START
              564  WITH_CLEANUP_FINISH
              566  END_FINALLY      
            568_0  COME_FROM           536  '536'

 L. 138       568  LOAD_FAST                'calendar_moodle_epn_url'
              570  STORE_FAST               'calendar_url'

 L. 139       572  LOAD_GLOBAL              configuration
              574  LOAD_METHOD              check_for_url
              576  LOAD_FAST                'calendar_url'
              578  CALL_METHOD_1         1  ''
          580_582  POP_JUMP_IF_TRUE    596  'to 596'

 L. 140       584  LOAD_GLOBAL              input

 L. 141       586  LOAD_STR                 'Por favor, introduzca el url generado por el Aula Virtual, si este es erróneo se volverá a solicitar:'

 L. 140       588  CALL_FUNCTION_1       1  ''
              590  STORE_FAST               'calendar_url'
          592_594  JUMP_BACK           572  'to 572'
            596_0  COME_FROM           580  '580'

 L. 143       596  LOAD_FAST                'access_token'
              598  LOAD_STR                 'oauth_token'
              600  BINARY_SUBSCR    

 L. 144       602  LOAD_FAST                'access_token'
              604  LOAD_STR                 'oauth_token_secret'
              606  BINARY_SUBSCR    

 L. 145       608  LOAD_FAST                'api_key'

 L. 146       610  LOAD_FAST                'api_secret'

 L. 147       612  LOAD_FAST                'calendar_url'

 L. 142       614  LOAD_CONST               ('oauth_token', 'oauth_token_secret', 'api_key', 'api_secret', 'calendar_url')
              616  BUILD_CONST_KEY_MAP_5     5 
              618  STORE_FAST               'final_output_data'

 L. 149       620  LOAD_GLOBAL              print
              622  LOAD_STR                 '\n\n'
              624  CALL_FUNCTION_1       1  ''
              626  POP_TOP          

 L. 158       628  LOAD_GLOBAL              get_working_board_id

 L. 159       630  LOAD_FAST                'api_key'

 L. 159       632  LOAD_FAST                'api_secret'

 L. 159       634  LOAD_FAST                'access_token'
              636  LOAD_STR                 'oauth_token'
              638  BINARY_SUBSCR    

 L. 159       640  LOAD_FAST                'access_token'
              642  LOAD_STR                 'oauth_token_secret'
              644  BINARY_SUBSCR    

 L. 158       646  CALL_FUNCTION_4       4  ''
              648  UNPACK_SEQUENCE_2     2 
              650  STORE_FAST               'board_id'
              652  STORE_FAST               'owner_id'

 L. 160       654  LOAD_FAST                'board_id'
              656  LOAD_FAST                'final_output_data'
              658  LOAD_STR                 'board_id'
              660  STORE_SUBSCR     

 L. 161       662  LOAD_FAST                'owner_id'
              664  LOAD_FAST                'final_output_data'
              666  LOAD_STR                 'owner_id'
              668  STORE_SUBSCR     

 L. 162       670  LOAD_GLOBAL              check_file_existence
              672  LOAD_FAST                'output_file'
              674  CALL_FUNCTION_1       1  ''
          676_678  POP_JUMP_IF_FALSE   752  'to 752'

 L. 163       680  LOAD_GLOBAL              check_user_on_file
              682  LOAD_FAST                'output_file'
              684  LOAD_FAST                'username'
              686  LOAD_FAST                'owner_id'
              688  BINARY_ADD       
              690  CALL_FUNCTION_2       2  ''
              692  POP_TOP          

 L. 164       694  LOAD_GLOBAL              open
              696  LOAD_FAST                'output_file'
              698  CALL_FUNCTION_1       1  ''
              700  SETUP_WITH          744  'to 744'
              702  STORE_FAST               'file'

 L. 166       704  LOAD_GLOBAL              yaml
              706  LOAD_METHOD              safe_load
              708  LOAD_FAST                'file'
              710  CALL_METHOD_1         1  ''
              712  STORE_FAST               'super_final'

 L. 167       714  LOAD_FAST                'final_output_data'
              716  LOAD_FAST                'super_final'
              718  LOAD_FAST                'username'
              720  LOAD_FAST                'owner_id'
              722  BINARY_ADD       
              724  STORE_SUBSCR     

 L. 168       726  LOAD_GLOBAL              connectSQLite
              728  LOAD_METHOD              saveUser
              730  LOAD_FAST                'username'
              732  LOAD_FAST                'owner_id'
              734  BINARY_ADD       
              736  CALL_METHOD_1         1  ''
              738  POP_TOP          
              740  POP_BLOCK        
              742  BEGIN_FINALLY    
            744_0  COME_FROM_WITH      700  '700'
              744  WITH_CLEANUP_START
              746  WITH_CLEANUP_FINISH
              748  END_FINALLY      
              750  JUMP_FORWARD        778  'to 778'
            752_0  COME_FROM           676  '676'

 L. 171       752  LOAD_FAST                'username'
              754  LOAD_FAST                'owner_id'
              756  BINARY_ADD       

 L. 171       758  LOAD_FAST                'final_output_data'

 L. 170       760  BUILD_MAP_1           1 
              762  STORE_FAST               'super_final'

 L. 173       764  LOAD_GLOBAL              connectSQLite
              766  LOAD_METHOD              saveUser
              768  LOAD_FAST                'username'
              770  LOAD_FAST                'owner_id'
              772  BINARY_ADD       
              774  CALL_METHOD_1         1  ''
              776  POP_TOP          
            778_0  COME_FROM           750  '750'

 L. 174       778  LOAD_GLOBAL              open
              780  LOAD_FAST                'output_file'
              782  LOAD_STR                 'w'
              784  CALL_FUNCTION_2       2  ''
              786  SETUP_WITH          814  'to 814'
              788  STORE_FAST               'f'

 L. 175       790  LOAD_FAST                'f'
              792  LOAD_METHOD              write
              794  LOAD_GLOBAL              yaml
              796  LOAD_ATTR                safe_dump
              798  LOAD_FAST                'super_final'
              800  LOAD_CONST               False
              802  LOAD_CONST               ('default_flow_style',)
              804  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              806  CALL_METHOD_1         1  ''
              808  POP_TOP          
              810  POP_BLOCK        
              812  BEGIN_FINALLY    
            814_0  COME_FROM_WITH      786  '786'
              814  WITH_CLEANUP_START
              816  WITH_CLEANUP_FINISH
              818  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 742


def get_working_board_id(api_key, api_secret, oauth_token, oauth_token_secret):
    client = trello.TrelloClient(api_key=api_key,
      api_secret=api_secret,
      token=oauth_token,
      token_secret=oauth_token_secret)
    board_id = ''
    all_boards = client.list_boards
    for board in all_boards:
        if board.name == 'TareasPoli':
            board_id = board.id
        if board_id == '':
            logging.error('No se encontró el board "TareasPoli", será creado ahora')
            print('No se encontró el board "TareasPoli", será creado ahora')
            client.add_board('TareasPoli')
            all_boards = client.list_boards
            for board in all_boards:
                if board.name == 'TareasPoli':
                    board_id = board.id

        else:
            return (
             board_id, board.all_members[(-1)].id)


def check_user_on_file--- This code section failed: ---

 L. 205         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_FAST                'output_file'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_FALSE    84  'to 84'

 L. 206        12  LOAD_GLOBAL              open
               14  LOAD_FAST                'output_file'
               16  CALL_FUNCTION_1       1  ''
               18  SETUP_WITH           78  'to 78'
               20  STORE_FAST               'file'

 L. 208        22  LOAD_GLOBAL              yaml
               24  LOAD_METHOD              safe_load
               26  LOAD_FAST                'file'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'users'

 L. 209        32  LOAD_FAST                'username'
               34  LOAD_FAST                'users'
               36  LOAD_METHOD              keys
               38  CALL_METHOD_0         0  ''
               40  COMPARE_OP               in
               42  POP_JUMP_IF_FALSE    74  'to 74'

 L. 210        44  LOAD_GLOBAL              input

 L. 211        46  LOAD_STR                 'El nombre de usuario actualmente ya existe, sobreescribir? s/N:'

 L. 210        48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'overwrite'

 L. 212        52  LOAD_FAST                'overwrite'
               54  LOAD_STR                 'N'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    74  'to 74'

 L. 213        60  POP_BLOCK        
               62  BEGIN_FINALLY    
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  POP_FINALLY           0  ''
               70  LOAD_CONST               None
               72  RETURN_VALUE     
             74_0  COME_FROM            58  '58'
             74_1  COME_FROM            42  '42'
               74  POP_BLOCK        
               76  BEGIN_FINALLY    
             78_0  COME_FROM_WITH       18  '18'
               78  WITH_CLEANUP_START
               80  WITH_CLEANUP_FINISH
               82  END_FINALLY      
             84_0  COME_FROM            10  '10'

Parse error at or near `BEGIN_FINALLY' instruction at offset 62


def check_file_existence--- This code section failed: ---

 L. 217         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_FAST                'output_file'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_FALSE    88  'to 88'

 L. 218        12  LOAD_GLOBAL              open
               14  LOAD_FAST                'output_file'
               16  CALL_FUNCTION_1       1  ''
               18  SETUP_WITH           80  'to 80'
               20  STORE_FAST               'file'

 L. 220        22  LOAD_GLOBAL              yaml
               24  LOAD_METHOD              safe_load
               26  LOAD_FAST                'file'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'users'

 L. 221        32  LOAD_GLOBAL              len
               34  LOAD_FAST                'users'
               36  LOAD_METHOD              keys
               38  CALL_METHOD_0         0  ''
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_CONST               0
               44  COMPARE_OP               >
               46  POP_JUMP_IF_FALSE    62  'to 62'

 L. 222        48  POP_BLOCK        
               50  BEGIN_FINALLY    
               52  WITH_CLEANUP_START
               54  WITH_CLEANUP_FINISH
               56  POP_FINALLY           0  ''
               58  LOAD_CONST               True
               60  RETURN_VALUE     
             62_0  COME_FROM            46  '46'

 L. 224        62  POP_BLOCK        
               64  BEGIN_FINALLY    
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  POP_FINALLY           0  ''
               72  LOAD_CONST               False
               74  RETURN_VALUE     
               76  POP_BLOCK        
               78  BEGIN_FINALLY    
             80_0  COME_FROM_WITH       18  '18'
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  END_FINALLY      
               86  JUMP_FORWARD         92  'to 92'
             88_0  COME_FROM            10  '10'

 L. 226        88  LOAD_CONST               False
               90  RETURN_VALUE     
             92_0  COME_FROM            86  '86'

Parse error at or near `BEGIN_FINALLY' instruction at offset 50