# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = 'Temporarily eat stdout/stderr to allow no output.\n    This is used to suppress browser messages in webbrowser.open'

    def __enter__(self):
        self.old_stderr = os.dup(2)
        self.old_stdout = os.dup(1)
        os.close(2)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)

    def __exit__(self, exc_type, exc_value, traceback):
        os.dup2(self.old_stderr, 2)
        os.dup2(self.old_stdout, 1)


def onboard(no_open, output_path='polical.yaml'):
    """Obtain Trello API credentials and put them into your config file.
    This is invoked automatically the first time you attempt to do an operation which requires authentication.
    The configuration file is put in an appropriate place for your operating system. If you want to change it later,
    you can use `gtd config -e` to open it in $EDITOR.
    """
    username = ''
    output_file = configuration.get_file_location(output_path)
    user_api_key_url = 'https://trello.com/app-key'
    request_token_url = 'https://trello.com/1/OAuthGetRequestToken'
    authorize_url = 'https://trello.com/1/OAuthAuthorizeToken'
    access_token_url = 'https://trello.com/1/OAuthGetAccessToken'
    calendar_moodle_epn_url = 'https://educacionvirtual.epn.edu.ec/calendar/view.php?view=upcoming&course=1'
    logging.info('Mostrando print-board al usuario')
    print('Bienvenido a PoliCal! Recuerde que antes de iniciar el proceso de obtención de credenciales ud debe tener una cuenta en Trello y en el Aula Virtual, y deben estar iniciadas las sesiones en el navegador predeterminado')
    print('\n\n')
    username = input('Ingrese su nombre:')
    print('PASO 1: Acceso a Trello')
    print('En su navegador web se cargará el siguiente URL:')
    print('  ' + user_api_key_url)
    print('Cuando llegue a esa página, inicie sesión y copie la "Tecla" o "Key" que se muestra en un cuadro de texto.')
    print('Si es la primera vez que realiza este proceso debe aceptar los terminos y condiciones de Trello')
    input('Presione ENTER para ir al enlace')
    if not no_open:
        with DevNullRedirect():
            webbrowser.open_new_tab(user_api_key_url)
    api_key = input('Por favor, introduzca el valor de "Tecla" o "Key":')
    print('Ahora desplácese hasta la parte inferior de la página y copie el "Secreto" o "Secret" que se muestra en un cuadro de texto.')
    api_secret = input('Por favor, introduzca el valor de "Secret":')
    print('\n\n')
    print('PASO 2: Permitir acceso de Polical a Trello')
    print('Ahora obtendremos las credenciales de OAuth necesarias para usar este programa...')
    session = OAuth1Session(client_key=api_key, client_secret=api_secret)
    try:
        response = session.fetch_request_token(request_token_url)
    except TokenRequestDenied:
        print('Invalid API key/secret provided: {0} / {1}'.format(api_key, api_secret))
        sys.exit(1)
    else:
        resource_owner_key, resource_owner_secret = response.get('oauth_token'), response.get('oauth_token_secret')
        user_confirmation_url = '{authorize_url}?oauth_token={oauth_token}&scope={scope}&expiration={expiration}&name={name}'.format(authorize_url=authorize_url,
          oauth_token=resource_owner_key,
          expiration='never',
          scope='read,write',
          name='PoliCal')
        print('Visite la siguiente URL en su navegador web para autorizar a PoliCal acceso a su cuenta:')
        print('  ' + user_confirmation_url)
        print('Concedale los permisos a PoliCal para acceder a sus datos de Trello, estas credenciales se mantendran de manera local')
        input('Presione ENTER para ir al enlace')
        if not no_open:
            with DevNullRedirect():
                webbrowser.open_new_tab(user_confirmation_url)
        confirmation = input('¿Has autorizado a PoliCal? Escriba n para no y S para si:')
        if confirmation == 'n':
            confirmation = input('¿Has autorizado a PoliCal? Escriba n para no y S para si:')
        else:
            oauth_verifier = input('¿Cuál es el código de verificación?:').strip()
            session = OAuth1Session(client_key=api_key,
              client_secret=api_secret,
              resource_owner_key=resource_owner_key,
              resource_owner_secret=resource_owner_secret,
              verifier=oauth_verifier)
            access_token = session.fetch_access_token(access_token_url)
            print('\n\n')
            print('PASO 3: Obtención del calendario del Aula Virtual')
            print('A continuación se abrirá un link hacia el Aula Virtual EPN, en proximos eventos para: elija Todos los cursos')
            print('y a continuación desplácese a la parte más inferior de la página y de clic en el botón Exportar Calendario')
            print('Luego, en la opción Exportar seleccione todos los eventos y después en "para" seleccione los 60 días recientes y próximos')
            print('Finalmente de clic en el boton Obtener URL del calendario')
            print('Visite la siguiente URL en su navegador web para obtener el calendario del aula virtual EPN:')
            print('  ' + calendar_moodle_epn_url)
            input('Presione ENTER para ir al enlace e iniciar el proceso, no olvide verificar si su sesión del Aula Virtual se encuentra activa')
            if not no_open:
                with DevNullRedirect():
                    webbrowser.open_new_tab(calendar_moodle_epn_url)
            calendar_url = calendar_moodle_epn_url
            if not configuration.check_for_url(calendar_url):
                calendar_url = input('Por favor, introduzca el url generado por el Aula Virtual, si este es erróneo se volverá a solicitar:')
            else:
                final_output_data = {'oauth_token':access_token['oauth_token'], 
                 'oauth_token_secret':access_token['oauth_token_secret'], 
                 'api_key':api_key, 
                 'api_secret':api_secret, 
                 'calendar_url':calendar_url}
                print('\n\n')
                board_id, owner_id = get_working_board_id(api_key, api_secret, access_token['oauth_token'], access_token['oauth_token_secret'])
                final_output_data['board_id'] = board_id
                final_output_data['owner_id'] = owner_id
                if check_file_existence(output_file):
                    check_user_on_file(output_file, username + owner_id)
                    with open(output_file) as (file):
                        super_final = yaml.safe_load(file)
                        super_final[username + owner_id] = final_output_data
                        connectSQLite.saveUser(username + owner_id)
                else:
                    super_final = {username + owner_id: final_output_data}
                    connectSQLite.saveUser(username + owner_id)
                with open(output_file, 'w') as (f):
                    f.write(yaml.safe_dump(super_final, default_flow_style=False))


def get_working_board_id(api_key, api_secret, oauth_token, oauth_token_secret):
    client = trello.TrelloClient(api_key=api_key,
      api_secret=api_secret,
      token=oauth_token,
      token_secret=oauth_token_secret)
    board_id = ''
    all_boards = client.list_boards()
    for board in all_boards:
        if board.name == 'TareasPoli':
            board_id = board.id
        if board_id == '':
            logging.error('No se encontró el board "TareasPoli", será creado ahora')
            print('No se encontró el board "TareasPoli", será creado ahora')
            client.add_board('TareasPoli')
            all_boards = client.list_boards()
            for board in all_boards:
                if board.name == 'TareasPoli':
                    board_id = board.id

        else:
            return (
             board_id, board.all_members()[(-1)].id)


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