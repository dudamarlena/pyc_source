# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/deniz/My code/diclipy/diclipy/diclipy.py
# Compiled at: 2017-06-18 02:56:29
# Size of source mod 2**32: 32708 bytes
r"""### D* is for Diaspora* ###
This is a Diaspora* CLIent written using `diaspy` API.
Why? Cause — CLI rocks! \o

SYNTAX:
    diclipy [OPTIONS ...] [COMMAND [COMMAND OPTIONS ...]]

OPTIONS:
    -h, --help                  - Display this help.
    -v, --verbose               - Be verbose.
    -d, --debug                 - Print a lot of debug scrap
                                   (WARNING: password too!).
    -V, --version               - Display version information.
    -C, --component <str>       - Which component's version to display:
                                   ui, backend|diaspy, clap.
    -Q, --quiet                 - Be quiet.

   LOGIN OPTIONS:
    -H, --handle HANDLE         - Diaspora* handle (USER@POD) (overrides config)
                                   (not load saved password).
    -P, --password PASSWORD     - Specify password.
    -p, --proto <str>           - Protocol to use (default: 'https').
    -s, --save-auth             - Store auth data as plain json file
                                   (~/.diclipy/auth.json).
    -S, --set-default           - Set default handle (requires: --handle|-H)
                                   (~/.diclipy/defhandle.json).
    -L, --load-auth             - Load saved password associated with handle
                                   being used (default).
    -D, --use-default           - Use default handle (default)
                                   (if not set you'll be asked for login data).

   EXAMPLES:
    Save auth to file & set default handle:
     diclipy -sS [...]
     or:
     diclipy -sSH USER@POD [...]
     or:
     diclipy -sSH USER@POD -P PASSWORD [...]
     or save only password:
      diclipy -s [...]
     or only set default handle:
      diclipy -S [...]

    Load saved password & use default handle (default):
     diclipy -LD [...]

    Show version:
     diclipy -V -C ui
     diclipy -v -V -C backend
     diclipy -vVC clap

COMMAND:
    post                        - posts operations.
    notifs                      - notifications operations.

COMMAND OPTIONS:
   `post` command options:
        -m, --message "MESSAGE" - Send post with given message
                                   (conflicts: --read, --reshare)
                                   if "MESSAGE" = "-" then read data from stdin.
        -A, --aspect <str>      - Aspect id to send post to (default: "public")
                                   ("public", "all", or aspect id number)
                                   you can find aspect numeric value at your
                                   Diaspora contacts page in aspects links list
                                   e.g.: for 'https://POD/contacts?a_id=1234567'
                                   aspect id is: '1234567'.
        -i, --image "PATH"      - Attach image to post.
        -r, --read              - Read post of given id (conflicts: --message).
        -a, --also-comments     - Read also post comments (requires: --read).
        -R, --reshare           - Reshare post of given id
                                   (conflicts: --message).
        -c, --comment "COMMENT" - Comment the post of given id
                                   (conflicts: --message)
                                   if "COMMENT" = "-" read from stdin.
        -l, --like              - Like the post of given id
                                   (conflicts: --message).
        -I, --id <str>          - Supplies post id
                                   (for: --read, --reshare, --comment, --like).
        -s, --stdin             - Read data from --message|--comment arg
                                   and + system standart input
                                   (requires: --message|--comment).

   `notifs` (short for 'notifications') command options:
        -l, --last              - Check your unread notifications.
        -U, --unread-only       - Display only unread notifications.
        -r, --read              - Mark listed notifications as read
                                   (by default notifications are not marked).
        -p, --page N            - Print N-th page of notifications.
        -P, --per-page N        - Print N notifications per page.

    EXAMPLES:
     SEND THE POST:
        diclipy post -m "MESSAGE"
        diclipy -H USER@POD -P PASSWORD post -m "MESSAGE"
        diclipy post -A ASPECT_ID -m "MESSAGE"
        diclipy post -m "MESSAGE WITH
         LINE BREAKS,
         PIC & TAGS
         ![](PICTURE.JPG)
         #TAG1 #TAG2 #TAG3"

     SEND THE POST FROM SYSTEM STDIN:
        diclipy post -m -
         ... TYPE MESSAGE (multiline acceptably) & PRESS: Ctrl+d
        diclipy post -sm ''
         ... TYPE MESSAGE & PRESS: Ctrl+d
        echo "It's a post through pipe!" | diclipy post -m -
        diclipy post -m - <<<"It's a stdin post again! Whoo!"
        diclipy post -m - <<EOF
         It's a stdin post
         with line breaks!
         Yay!
         EOF

     READ THE POST OF GIVEN ID:
        diclipy post -rI ID

     READ THE POST OF GIVEN ID + COMMENTS:
        diclipy post -raI ID

     RESHARE THE POST OF GIVEN ID:
        diclipy post -RI ID

     LIKE THE POST OF GIVEN ID:
        diclipy post -lI ID

     COMMENTING POST OF GIVEN ID:
        diclipy post -I ID -c "COMMENT"
        diclipy post -I ID -c "COMMENT WITH
         LINE
         BREAKS"

     COMMENTING POST OF GIVEN ID FROM SYSTEM STDIN:
        diclipy post -I ID -c -
         ... TYPE COMMENT & PRESS: Ctrl+d
        diclipy post -I ID -sc ''
         ... TYPE COMMENT & PRESS: Ctrl+d
        echo "It's a comment through pipe!" | diclipy post -I ID -c -
      BE VERBOSE:
        diclipy -v post -I ID -c - <<<"It's stdin again!"
        diclipy -v post -I ID -c - <<EOF
         It's a
         multiline
         stdin
         comment!
         EOF

     READ YOUR UNREAD NOTIFICATIONS:
      READ LAST:
        diclipy notifs --last
        diclipy notifs -l
      READ LAST 20 PER PAGE:
        diclipy notifs --last --per-page 20
        diclipy notifs --page 2 --per-page 20
        diclipy notifs -p 2 -P 20

--
diacli: Copyright Marek Marecki (c) 2013 https://github.com/marekjm/diacli This is free software published under GNU GPL v3 license or any later version of this license.

diclipy: Copyleft uzver(at)protonmail.ch (ɔ) 2017
"""
import json, getpass, os, re, sys, pickle, diaspy, clap
__version__ = '0.1.3'
DEBUG = False
if DEBUG:
    import errno
    from pprint import pprint
verbose = False
debug = False
username, pod = ('', '')
password = ''
savedconn = {}
proto = 'https'
schemed = ''

def sure_path_exists(path, mode):
    os.makedirs(path, mode, exist_ok=True)


def get_authdb():
    if os.path.isfile(os.path.expanduser('~/.diclipy/auth.json')):
        ifstream = open(os.path.expanduser('~/.diclipy/auth.json'))
        try:
            try:
                authdb = json.loads(ifstream.read())
            except ValueError:
                authdb = {}
            except Exception as e:
                print('\ndiclipy: auth loading: error encountered: {0}'.format(e))

        finally:
            ifstream.close()

    else:
        authdb = {}
    return authdb


def set_default_handle(username, pod):
    sure_path_exists(os.path.expanduser('~/.diclipy'), mode=448)
    defhandlepath = os.path.expanduser('~/.diclipy/defhandle.json')
    ofstream = open(defhandlepath, 'w')
    ofstream.write(json.dumps({'username': username,  'pod': pod}))
    ofstream.close()
    os.chmod(defhandlepath, 384)


def get_default_handle():
    global debug
    if os.path.isfile(os.path.expanduser('~/.diclipy/defhandle.json')):
        defhandlepath = os.path.expanduser('~/.diclipy/defhandle.json')
        ifstream = open(defhandlepath)
        try:
            try:
                handle = json.loads(ifstream.read())
            except ValueError:
                handle = {'pod': '',  'username': ''}
            except Exception as e:
                print('\ndiclipy: handle extraction: error encountered: {0}'.format(e))

        finally:
            ifstream.close()

    else:
        handle = {'pod': '',  'username': ''}
    if debug:
        print('debug: Found default handle: {0}@{1}'.format(handle['username'], handle['pod']))
    return (
     handle['username'], handle['pod'])


def get_password():
    global pod
    global username
    passwd = getpass.getpass('Password for {0}@{1}: '.format(username, pod))
    return passwd


def get_user_input():
    txt = ''
    txtarr = sys.stdin.readlines()
    txtarr[-1] = txtarr[(-1)][:-1]
    for line in txtarr:
        txt += line

    return txt


def load_auth():
    global passkey
    global password
    global savedconn
    global verbose
    if verbose:
        print('Loading auth...')
    if not password:
        authdb = get_authdb()
        passkey = '{0}@{1}'.format(username, pod)
        if passkey in authdb:
            try:
                try:
                    password = authdb[passkey]
                except ValueError:
                    password = ''
                    print('\ndiclipy: password extraction: ValueError: {0}'.format(e))
                except Exception as e:
                    print('\ndiclipy: password extraction: error encountered: {0}'.format(e))

            finally:
                if not password:
                    print("Can't find password. Is it empty?")

        else:
            print("Can't load password. Was it saved?")
    connpath = os.path.expanduser('~/.diclipy/{}.connection'.format(passkey))
    if os.path.isfile(connpath):
        f = open(connpath, 'rb')
        try:
            try:
                success = False
                savedconn = pickle.load(f)
                if debug:
                    print("debug: savedconn._login_data['user[username]'] = username:")
                savedconn._login_data['user[username]'] = username
                if debug:
                    print("debug: savedconn._login_data['user[password]'] = password:")
                savedconn._login_data['user[password]'] = password
                if debug:
                    print("debug: savedconn._login_data['authenticity_token'] = savedconn._token:")
                savedconn._login_data['authenticity_token'] = savedconn._token
                success = True
            except pickle.UnpicklingError as e:
                print('\ndiclipy: pickle load: problems with the deserialization of the object was hapened: {}'.format(e))
                success = False
            except Exception as e:
                print('\ndiclipy: pickle load: error encountered: {0}'.format(e))
                success = False
            except ValueError:
                success = False

        finally:
            f.close()
            if verbose:
                if success:
                    print('Connection loaded.')
            else:
                print("Can't find saved connection. Will try to get new.")
                if debug:
                    print('debug: diclipy: load savedconn not success.\n')
                if debug:
                    print('debug: type of "savedconn" =', type(savedconn))
                    print('debug: savedconn._login_data =', savedconn._login_data)
                    print('\ndebug: dir(savedconn):')
                    print(dir(savedconn))
                    print('\ndebug: savedconn.__dict__:')
                    pprint(savedconn.__dict__, indent=2)
                    print('')

    else:
        if verbose:
            print('No saved connection. Will try to get new.')
        return (
         password, savedconn)


def main--- This code section failed: ---

 L. 335         0  BUILD_MAP_0           0  ''
                3  STORE_FAST               'model'

 L. 338         6  LOAD_GLOBAL              list
                9  LOAD_GLOBAL              clap
               12  LOAD_ATTR                formatter
               15  LOAD_ATTR                Formatter
               18  LOAD_GLOBAL              sys
               21  LOAD_ATTR                argv
               24  LOAD_CONST               1
               27  LOAD_CONST               None
               30  BUILD_SLICE_2         2 
               33  BINARY_SUBSCR    
               34  CALL_FUNCTION_1       1  '1 positional, 0 named'
               37  LOAD_ATTR                format
               40  CALL_FUNCTION_0       0  '0 positional, 0 named'
               43  CALL_FUNCTION_1       1  '1 positional, 0 named'
               46  STORE_FAST               'args'

 L. 340        49  LOAD_STR                 ''
               52  STORE_FAST               'uilocation'

 L. 342        55  SETUP_LOOP          236  'to 236'
               58  LOAD_STR                 '.'
               61  LOAD_STR                 ''
               64  LOAD_GLOBAL              os
               67  LOAD_ATTR                getcwd
               70  CALL_FUNCTION_0       0  '0 positional, 0 named'
               73  BUILD_TUPLE_2         2 
               76  LOAD_STR                 ''
               79  LOAD_GLOBAL              os
               82  LOAD_ATTR                path
               85  LOAD_ATTR                dirname
               88  LOAD_GLOBAL              __file__
               91  CALL_FUNCTION_1       1  '1 positional, 0 named'
               94  BUILD_TUPLE_2         2 
               97  LOAD_GLOBAL              os
              100  LOAD_ATTR                path
              103  LOAD_ATTR                expanduser
              106  LOAD_STR                 '~'
              109  CALL_FUNCTION_1       1  '1 positional, 0 named'
              112  LOAD_STR                 '.diclipy'
              115  BUILD_TUPLE_2         2 
              118  LOAD_CONST               ('', '/usr', 'share', 'diclipy')
              121  BUILD_LIST_5          5 
              124  GET_ITER         
              125  FOR_ITER            235  'to 235'
              128  STORE_FAST               'path'

 L. 343       131  LOAD_GLOBAL              os
              134  LOAD_ATTR                path
              137  LOAD_ATTR                join
              140  LOAD_FAST                'path'
              143  CALL_FUNCTION_VAR_0     0  '0 positional, 0 named'
              146  STORE_FAST               'path'

 L. 344       149  LOAD_GLOBAL              os
              152  LOAD_ATTR                path
              155  LOAD_ATTR                abspath
              158  LOAD_GLOBAL              os
              161  LOAD_ATTR                path
              164  LOAD_ATTR                join
              167  LOAD_FAST                'path'
              170  LOAD_STR                 'ui.json'
              173  CALL_FUNCTION_2       2  '2 positional, 0 named'
              176  CALL_FUNCTION_1       1  '1 positional, 0 named'
              179  STORE_FAST               'path'

 L. 345       182  LOAD_GLOBAL              DEBUG
              185  POP_JUMP_IF_FALSE   204  'to 204'

 L. 345       188  LOAD_GLOBAL              print
              191  LOAD_STR                 'debug: ui.json path ='
              194  LOAD_FAST                'path'
              197  CALL_FUNCTION_2       2  '2 positional, 0 named'
              200  POP_TOP          
              201  JUMP_FORWARD        204  'to 204'
            204_0  COME_FROM           201  '201'

 L. 346       204  LOAD_GLOBAL              os
              207  LOAD_ATTR                path
              210  LOAD_ATTR                isfile
              213  LOAD_FAST                'path'
              216  CALL_FUNCTION_1       1  '1 positional, 0 named'
              219  POP_JUMP_IF_FALSE   125  'to 125'

 L. 347       222  LOAD_FAST                'path'
              225  STORE_FAST               'uilocation'

 L. 348       228  BREAK_LOOP       
              232  JUMP_BACK           125  'to 125'
              235  POP_BLOCK        
            236_0  COME_FROM_LOOP       55  '55'

 L. 349       236  LOAD_FAST                'uilocation'
              239  POP_JUMP_IF_FALSE   290  'to 290'

 L. 350       242  LOAD_GLOBAL              open
              245  LOAD_FAST                'uilocation'
              248  LOAD_STR                 'r'
              251  CALL_FUNCTION_2       2  '2 positional, 0 named'
              254  SETUP_WITH          285  'to 285'
              257  STORE_FAST               'ifstream'

 L. 350       260  LOAD_GLOBAL              json
              263  LOAD_ATTR                loads
              266  LOAD_FAST                'ifstream'
              269  LOAD_ATTR                read
              272  CALL_FUNCTION_0       0  '0 positional, 0 named'
              275  CALL_FUNCTION_1       1  '1 positional, 0 named'
              278  STORE_FAST               'model'
              281  POP_BLOCK        
              282  LOAD_CONST               None
            285_0  COME_FROM_WITH      254  '254'
              285  WITH_CLEANUP     
              286  END_FINALLY      
              287  JUMP_FORWARD        310  'to 310'

 L. 352       290  LOAD_GLOBAL              print
              293  LOAD_STR                 'diclipy: fatal: cannot find ui.json file'
              296  CALL_FUNCTION_1       1  '1 positional, 0 named'
              299  POP_TOP          

 L. 353       300  LOAD_GLOBAL              exit
              303  LOAD_CONST               1
              306  CALL_FUNCTION_1       1  '1 positional, 0 named'
              309  POP_TOP          
            310_0  COME_FROM           287  '287'

 L. 360       310  LOAD_GLOBAL              clap
              313  LOAD_ATTR                builder
              316  LOAD_ATTR                Builder
              319  LOAD_FAST                'model'
              322  CALL_FUNCTION_1       1  '1 positional, 0 named'
              325  LOAD_ATTR                build
              328  CALL_FUNCTION_0       0  '0 positional, 0 named'
              331  LOAD_ATTR                get
              334  CALL_FUNCTION_0       0  '0 positional, 0 named'
              337  STORE_FAST               'options'

 L. 363       340  LOAD_GLOBAL              clap
              343  LOAD_ATTR                parser
              346  LOAD_ATTR                Parser
              349  LOAD_FAST                'options'
              352  CALL_FUNCTION_1       1  '1 positional, 0 named'
              355  LOAD_ATTR                feed
              358  LOAD_FAST                'args'
              361  CALL_FUNCTION_1       1  '1 positional, 0 named'
              364  STORE_FAST               'parser'

 L. 365       367  LOAD_GLOBAL              clap
              370  LOAD_ATTR                checker
              373  LOAD_ATTR                RedChecker
              376  LOAD_FAST                'parser'
              379  CALL_FUNCTION_1       1  '1 positional, 0 named'
              382  STORE_FAST               'checker'

 L. 366       385  SETUP_FINALLY      1034  'to 1034'
              388  SETUP_EXCEPT        529  'to 529'

 L. 367       391  LOAD_CONST               False
              394  STORE_FAST               'success'

 L. 369       397  LOAD_FAST                'checker'
              400  LOAD_ATTR                check
              403  CALL_FUNCTION_0       0  '0 positional, 0 named'
              406  POP_TOP          

 L. 370       407  LOAD_CONST               True
              410  STORE_FAST               'success'

 L. 371       413  LOAD_GLOBAL              DEBUG
              416  POP_JUMP_IF_FALSE   441  'to 441'

 L. 371       419  LOAD_GLOBAL              print
              422  LOAD_STR                 'debug: options check success ='
              425  LOAD_GLOBAL              str
              428  LOAD_FAST                'success'
              431  CALL_FUNCTION_1       1  '1 positional, 0 named'
              434  CALL_FUNCTION_2       2  '2 positional, 0 named'
              437  POP_TOP          
              438  JUMP_FORWARD        441  'to 441'
            441_0  COME_FROM           438  '438'

 L. 372       441  LOAD_GLOBAL              DEBUG
              444  POP_JUMP_IF_FALSE   469  'to 469'

 L. 372       447  LOAD_GLOBAL              print
              450  LOAD_STR                 'debug: options parser ='
              453  LOAD_GLOBAL              str
              456  LOAD_FAST                'parser'
              459  CALL_FUNCTION_1       1  '1 positional, 0 named'
              462  CALL_FUNCTION_2       2  '2 positional, 0 named'
              465  POP_TOP          
              466  JUMP_FORWARD        469  'to 469'
            469_0  COME_FROM           466  '466'

 L. 373       469  LOAD_GLOBAL              DEBUG
              472  POP_JUMP_IF_FALSE   497  'to 497'

 L. 373       475  LOAD_GLOBAL              print
              478  LOAD_STR                 'debug: options checker ='
              481  LOAD_GLOBAL              str
              484  LOAD_FAST                'checker'
              487  CALL_FUNCTION_1       1  '1 positional, 0 named'
              490  CALL_FUNCTION_2       2  '2 positional, 0 named'
              493  POP_TOP          
              494  JUMP_FORWARD        497  'to 497'
            497_0  COME_FROM           494  '494'

 L. 374       497  LOAD_GLOBAL              DEBUG
              500  POP_JUMP_IF_FALSE   525  'to 525'

 L. 374       503  LOAD_GLOBAL              print
              506  LOAD_STR                 'debug: options model ='
              509  LOAD_GLOBAL              str
              512  LOAD_FAST                'model'
              515  CALL_FUNCTION_1       1  '1 positional, 0 named'
              518  CALL_FUNCTION_2       2  '2 positional, 0 named'
              521  POP_TOP          
              522  JUMP_FORWARD        525  'to 525'
            525_0  COME_FROM           522  '522'
              525  POP_BLOCK        
              526  JUMP_FORWARD       1030  'to 1030'
            529_0  COME_FROM_EXCEPT    388  '388'

 L. 375       529  DUP_TOP          
              530  LOAD_GLOBAL              clap
              533  LOAD_ATTR                errors
              536  LOAD_ATTR                UnrecognizedModeError
              539  COMPARE_OP               exception-match
              542  POP_JUMP_IF_FALSE   590  'to 590'
              545  POP_TOP          
              546  STORE_FAST               'e'
              549  POP_TOP          
              550  SETUP_FINALLY       577  'to 577'

 L. 376       553  LOAD_GLOBAL              print
              556  LOAD_STR                 'diclipy: fatal: unrecognized mode: {0}'
              559  LOAD_ATTR                format
              562  LOAD_FAST                'e'
              565  CALL_FUNCTION_1       1  '1 positional, 0 named'
              568  CALL_FUNCTION_1       1  '1 positional, 0 named'
              571  POP_TOP          
              572  POP_BLOCK        
              573  POP_EXCEPT       
              574  LOAD_CONST               None
            577_0  COME_FROM_FINALLY   550  '550'
              577  LOAD_CONST               None
              580  STORE_FAST               'e'
              583  DELETE_FAST              'e'
              586  END_FINALLY      
              587  JUMP_FORWARD       1030  'to 1030'

 L. 378       590  DUP_TOP          
              591  LOAD_GLOBAL              clap
              594  LOAD_ATTR                errors
              597  LOAD_ATTR                UnrecognizedOptionError
              600  COMPARE_OP               exception-match
              603  POP_JUMP_IF_FALSE   651  'to 651'
              606  POP_TOP          
              607  STORE_FAST               'e'
              610  POP_TOP          
              611  SETUP_FINALLY       638  'to 638'

 L. 379       614  LOAD_GLOBAL              print
              617  LOAD_STR                 'diclipy: fatal: unrecognized option found: {0}'
              620  LOAD_ATTR                format
              623  LOAD_FAST                'e'
              626  CALL_FUNCTION_1       1  '1 positional, 0 named'
              629  CALL_FUNCTION_1       1  '1 positional, 0 named'
              632  POP_TOP          
              633  POP_BLOCK        
              634  POP_EXCEPT       
              635  LOAD_CONST               None
            638_0  COME_FROM_FINALLY   611  '611'
              638  LOAD_CONST               None
              641  STORE_FAST               'e'
              644  DELETE_FAST              'e'
              647  END_FINALLY      
              648  JUMP_FORWARD       1030  'to 1030'

 L. 380       651  DUP_TOP          
              652  LOAD_GLOBAL              clap
              655  LOAD_ATTR                errors
              658  LOAD_ATTR                UIDesignError
              661  COMPARE_OP               exception-match
              664  POP_JUMP_IF_FALSE   712  'to 712'
              667  POP_TOP          
              668  STORE_FAST               'e'
              671  POP_TOP          
              672  SETUP_FINALLY       699  'to 699'

 L. 381       675  LOAD_GLOBAL              print
              678  LOAD_STR                 'diclipy: fatal: misdesigned interface: {0}'
              681  LOAD_ATTR                format
              684  LOAD_FAST                'e'
              687  CALL_FUNCTION_1       1  '1 positional, 0 named'
              690  CALL_FUNCTION_1       1  '1 positional, 0 named'
              693  POP_TOP          
              694  POP_BLOCK        
              695  POP_EXCEPT       
              696  LOAD_CONST               None
            699_0  COME_FROM_FINALLY   672  '672'
              699  LOAD_CONST               None
              702  STORE_FAST               'e'
              705  DELETE_FAST              'e'
              708  END_FINALLY      
              709  JUMP_FORWARD       1030  'to 1030'

 L. 383       712  DUP_TOP          
              713  LOAD_GLOBAL              clap
              716  LOAD_ATTR                errors
              719  LOAD_ATTR                RequiredOptionNotFoundError
              722  COMPARE_OP               exception-match
              725  POP_JUMP_IF_FALSE   773  'to 773'
              728  POP_TOP          
              729  STORE_FAST               'e'
              732  POP_TOP          
              733  SETUP_FINALLY       760  'to 760'

 L. 384       736  LOAD_GLOBAL              print
              739  LOAD_STR                 'diclipy: fatal: required option was not found: {0}'
              742  LOAD_ATTR                format
              745  LOAD_FAST                'e'
              748  CALL_FUNCTION_1       1  '1 positional, 0 named'
              751  CALL_FUNCTION_1       1  '1 positional, 0 named'
              754  POP_TOP          
              755  POP_BLOCK        
              756  POP_EXCEPT       
              757  LOAD_CONST               None
            760_0  COME_FROM_FINALLY   733  '733'
              760  LOAD_CONST               None
              763  STORE_FAST               'e'
              766  DELETE_FAST              'e'
              769  END_FINALLY      
              770  JUMP_FORWARD       1030  'to 1030'

 L. 385       773  DUP_TOP          
              774  LOAD_GLOBAL              clap
              777  LOAD_ATTR                errors
              780  LOAD_ATTR                NeededOptionNotFoundError
              783  COMPARE_OP               exception-match
              786  POP_JUMP_IF_FALSE   834  'to 834'
              789  POP_TOP          
              790  STORE_FAST               'e'
              793  POP_TOP          
              794  SETUP_FINALLY       821  'to 821'

 L. 386       797  LOAD_GLOBAL              print
              800  LOAD_STR                 'diclipy: fatal: at least one of needed options must be passed: {0}'
              803  LOAD_ATTR                format
              806  LOAD_FAST                'e'
              809  CALL_FUNCTION_1       1  '1 positional, 0 named'
              812  CALL_FUNCTION_1       1  '1 positional, 0 named'
              815  POP_TOP          
              816  POP_BLOCK        
              817  POP_EXCEPT       
              818  LOAD_CONST               None
            821_0  COME_FROM_FINALLY   794  '794'
              821  LOAD_CONST               None
              824  STORE_FAST               'e'
              827  DELETE_FAST              'e'
              830  END_FINALLY      
              831  JUMP_FORWARD       1030  'to 1030'

 L. 387       834  DUP_TOP          
              835  LOAD_GLOBAL              clap
              838  LOAD_ATTR                errors
              841  LOAD_ATTR                MissingArgumentError
              844  COMPARE_OP               exception-match
              847  POP_JUMP_IF_FALSE   895  'to 895'
              850  POP_TOP          
              851  STORE_FAST               'e'
              854  POP_TOP          
              855  SETUP_FINALLY       882  'to 882'

 L. 388       858  LOAD_GLOBAL              print
              861  LOAD_STR                 'diclipy: fatal: missing argument for option: {0}'
              864  LOAD_ATTR                format
              867  LOAD_FAST                'e'
              870  CALL_FUNCTION_1       1  '1 positional, 0 named'
              873  CALL_FUNCTION_1       1  '1 positional, 0 named'
              876  POP_TOP          
              877  POP_BLOCK        
              878  POP_EXCEPT       
              879  LOAD_CONST               None
            882_0  COME_FROM_FINALLY   855  '855'
              882  LOAD_CONST               None
              885  STORE_FAST               'e'
              888  DELETE_FAST              'e'
              891  END_FINALLY      
              892  JUMP_FORWARD       1030  'to 1030'

 L. 389       895  DUP_TOP          
              896  LOAD_GLOBAL              clap
              899  LOAD_ATTR                errors
              902  LOAD_ATTR                InvalidArgumentTypeError
              905  LOAD_GLOBAL              diaspy
              908  LOAD_ATTR                errors
              911  LOAD_ATTR                UserError
              914  BUILD_TUPLE_2         2 
              917  COMPARE_OP               exception-match
              920  POP_JUMP_IF_FALSE   968  'to 968'
              923  POP_TOP          
              924  STORE_FAST               'e'
              927  POP_TOP          
              928  SETUP_FINALLY       955  'to 955'

 L. 390       931  LOAD_GLOBAL              print
              934  LOAD_STR                 'diclipy: fatal: invalid argument for option: {0}'
              937  LOAD_ATTR                format
              940  LOAD_FAST                'e'
              943  CALL_FUNCTION_1       1  '1 positional, 0 named'
              946  CALL_FUNCTION_1       1  '1 positional, 0 named'
              949  POP_TOP          
              950  POP_BLOCK        
              951  POP_EXCEPT       
              952  LOAD_CONST               None
            955_0  COME_FROM_FINALLY   928  '928'
              955  LOAD_CONST               None
              958  STORE_FAST               'e'
              961  DELETE_FAST              'e'
              964  END_FINALLY      
              965  JUMP_FORWARD       1030  'to 1030'

 L. 391       968  DUP_TOP          
              969  LOAD_GLOBAL              clap
              972  LOAD_ATTR                errors
              975  LOAD_ATTR                ConflictingOptionsError
              978  COMPARE_OP               exception-match
              981  POP_JUMP_IF_FALSE  1029  'to 1029'
              984  POP_TOP          
              985  STORE_FAST               'e'
              988  POP_TOP          
              989  SETUP_FINALLY      1016  'to 1016'

 L. 392       992  LOAD_GLOBAL              print
              995  LOAD_STR                 'diclipy: fatal: conflicting options: {0}'
              998  LOAD_ATTR                format
             1001  LOAD_FAST                'e'
             1004  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1007  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1010  POP_TOP          
             1011  POP_BLOCK        
             1012  POP_EXCEPT       
             1013  LOAD_CONST               None
           1016_0  COME_FROM_FINALLY   989  '989'
             1016  LOAD_CONST               None
             1019  STORE_FAST               'e'
             1022  DELETE_FAST              'e'
             1025  END_FINALLY      
             1026  JUMP_FORWARD       1030  'to 1030'
             1029  END_FINALLY      
           1030_0  COME_FROM          1026  '1026'
           1030_1  COME_FROM           965  '965'
           1030_2  COME_FROM           892  '892'
           1030_3  COME_FROM           831  '831'
           1030_4  COME_FROM           770  '770'
           1030_5  COME_FROM           709  '709'
           1030_6  COME_FROM           648  '648'
           1030_7  COME_FROM           587  '587'
           1030_8  COME_FROM           526  '526'
             1030  POP_BLOCK        
             1031  LOAD_CONST               None
           1034_0  COME_FROM_FINALLY   385  '385'

 L. 394      1034  LOAD_FAST                'success'
             1037  POP_JUMP_IF_TRUE   1278  'to 1278'

 L. 395      1040  LOAD_GLOBAL              print
             1043  LOAD_STR                 "Wrong options or arguments. Run with '-h' for help. Exit."
             1046  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1049  POP_TOP          

 L. 396      1050  LOAD_GLOBAL              DEBUG
             1053  POP_JUMP_IF_FALSE  1072  'to 1072'

 L. 396      1056  LOAD_GLOBAL              print
             1059  LOAD_STR                 'debug: options check success ='
             1062  LOAD_FAST                'success'
             1065  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1068  POP_TOP          
             1069  JUMP_FORWARD       1072  'to 1072'
           1072_0  COME_FROM          1069  '1069'

 L. 397      1072  LOAD_FAST                'parser'
             1075  LOAD_ATTR                parse
             1078  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1081  LOAD_ATTR                ui
             1084  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1087  LOAD_ATTR                finalise
             1090  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1093  STORE_FAST               'optsui'

 L. 398      1096  LOAD_GLOBAL              DEBUG
             1099  POP_JUMP_IF_FALSE  1124  'to 1124'

 L. 398      1102  LOAD_GLOBAL              print
             1105  LOAD_STR                 'debug: options parser ='
             1108  LOAD_GLOBAL              str
             1111  LOAD_FAST                'parser'
             1114  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1117  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1120  POP_TOP          
             1121  JUMP_FORWARD       1124  'to 1124'
           1124_0  COME_FROM          1121  '1121'

 L. 399      1124  LOAD_GLOBAL              DEBUG
             1127  POP_JUMP_IF_FALSE  1152  'to 1152'

 L. 399      1130  LOAD_GLOBAL              print
             1133  LOAD_STR                 'debug: options checker ='
             1136  LOAD_GLOBAL              str
             1139  LOAD_FAST                'checker'
             1142  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1145  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1148  POP_TOP          
             1149  JUMP_FORWARD       1152  'to 1152'
           1152_0  COME_FROM          1149  '1149'

 L. 400      1152  LOAD_GLOBAL              DEBUG
             1155  POP_JUMP_IF_FALSE  1180  'to 1180'

 L. 400      1158  LOAD_GLOBAL              print
             1161  LOAD_STR                 'debug: options model ='
             1164  LOAD_GLOBAL              str
             1167  LOAD_FAST                'model'
             1170  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1173  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1176  POP_TOP          
             1177  JUMP_FORWARD       1180  'to 1180'
           1180_0  COME_FROM          1177  '1177'

 L. 401      1180  LOAD_GLOBAL              DEBUG
             1183  POP_JUMP_IF_FALSE  1208  'to 1208'

 L. 401      1186  LOAD_GLOBAL              print
             1189  LOAD_STR                 'debug: options ='
             1192  LOAD_GLOBAL              str
             1195  LOAD_FAST                'options'
             1198  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1201  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1204  POP_TOP          
             1205  JUMP_FORWARD       1208  'to 1208'
           1208_0  COME_FROM          1205  '1205'

 L. 402      1208  LOAD_GLOBAL              DEBUG
             1211  POP_JUMP_IF_FALSE  1243  'to 1243'

 L. 402      1214  LOAD_GLOBAL              print
             1217  LOAD_STR                 'debug: passed args ='
             1220  LOAD_GLOBAL              sys
             1223  LOAD_ATTR                argv
             1226  LOAD_CONST               1
             1229  LOAD_CONST               None
             1232  BUILD_SLICE_2         2 
             1235  BINARY_SUBSCR    
             1236  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1239  POP_TOP          
             1240  JUMP_FORWARD       1243  'to 1243'
           1243_0  COME_FROM          1240  '1240'

 L. 403      1243  LOAD_GLOBAL              DEBUG
             1246  POP_JUMP_IF_FALSE  1265  'to 1265'

 L. 403      1249  LOAD_GLOBAL              print
             1252  LOAD_STR                 'debug: formatted args ='
             1255  LOAD_FAST                'args'
             1258  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1261  POP_TOP          
             1262  JUMP_FORWARD       1265  'to 1265'
           1265_0  COME_FROM          1262  '1262'

 L. 404      1265  LOAD_GLOBAL              exit
             1268  LOAD_CONST               1
             1271  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1274  POP_TOP          
             1275  JUMP_FORWARD       1278  'to 1278'
           1278_0  COME_FROM          1275  '1275'

 L. 405      1278  LOAD_FAST                'parser'
             1281  LOAD_ATTR                parse
             1284  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1287  LOAD_ATTR                ui
             1290  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1293  LOAD_ATTR                finalise
             1296  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1299  STORE_FAST               'optsui'
             1302  END_FINALLY      

 L. 406      1303  LOAD_STR                 '--verbose'
             1306  LOAD_FAST                'optsui'
             1309  COMPARE_OP               in
             1312  POP_JUMP_IF_FALSE  1324  'to 1324'

 L. 407      1315  LOAD_CONST               True
             1318  STORE_GLOBAL             verbose
             1321  JUMP_FORWARD       1324  'to 1324'
           1324_0  COME_FROM          1321  '1321'

 L. 408      1324  LOAD_STR                 '--debug'
             1327  LOAD_FAST                'optsui'
             1330  COMPARE_OP               in
             1333  POP_JUMP_IF_FALSE  1379  'to 1379'

 L. 410      1336  LOAD_CONST               True
             1339  STORE_GLOBAL             verbose

 L. 411      1342  LOAD_CONST               True
             1345  STORE_GLOBAL             debug

 L. 412      1348  LOAD_CONST               0
             1351  LOAD_CONST               None
             1354  IMPORT_NAME              errno
             1357  STORE_FAST               'errno'

 L. 413      1360  LOAD_CONST               0
             1363  LOAD_CONST               ('pprint',)
             1366  IMPORT_NAME              pprint
             1369  IMPORT_FROM              pprint
             1372  STORE_FAST               'pprint'
             1375  POP_TOP          
             1376  JUMP_FORWARD       1379  'to 1379'
           1379_0  COME_FROM          1376  '1376'

 L. 414      1379  LOAD_STR                 '--version'
             1382  LOAD_FAST                'optsui'
             1385  COMPARE_OP               in
             1388  POP_JUMP_IF_FALSE  1615  'to 1615'

 L. 425      1391  LOAD_GLOBAL              verbose
             1394  POP_JUMP_IF_FALSE  1421  'to 1421'

 L. 425      1397  LOAD_STR                 'diclipy version: {0} (diaspy backend: {1})'
             1400  LOAD_ATTR                format
             1403  LOAD_GLOBAL              __version__
             1406  LOAD_GLOBAL              diaspy
             1409  LOAD_ATTR                __version__
             1412  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1415  STORE_FAST               'V'
             1418  JUMP_FORWARD       1427  'to 1427'
             1421  ELSE                     '1427'

 L. 426      1421  LOAD_GLOBAL              __version__
             1424  STORE_FAST               'V'
           1427_0  COME_FROM          1418  '1418'

 L. 427      1427  LOAD_STR                 '--component'
             1430  LOAD_FAST                'optsui'
             1433  COMPARE_OP               in
             1436  POP_JUMP_IF_FALSE  1592  'to 1592'

 L. 428      1439  LOAD_FAST                'optsui'
             1442  LOAD_ATTR                get
             1445  LOAD_STR                 '--component'
             1448  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1451  STORE_FAST               'component'

 L. 429      1454  LOAD_FAST                'component'
             1457  LOAD_STR                 'ui'
             1460  COMPARE_OP               ==
             1463  POP_JUMP_IF_FALSE  1475  'to 1475'

 L. 430      1466  LOAD_GLOBAL              __version__
             1469  STORE_FAST               'V'
             1472  JUMP_FORWARD       1544  'to 1544'
             1475  ELSE                     '1544'

 L. 431      1475  LOAD_FAST                'component'
             1478  LOAD_CONST               ('diaspy', 'backend')
             1481  COMPARE_OP               in
             1484  POP_JUMP_IF_FALSE  1505  'to 1505'

 L. 432      1487  LOAD_STR                 'diaspy'
             1490  STORE_FAST               'component'

 L. 433      1493  LOAD_GLOBAL              diaspy
             1496  LOAD_ATTR                __version__
             1499  STORE_FAST               'V'
             1502  JUMP_FORWARD       1544  'to 1544'
             1505  ELSE                     '1544'

 L. 434      1505  LOAD_FAST                'component'
             1508  LOAD_STR                 'clap'
             1511  COMPARE_OP               ==
             1514  POP_JUMP_IF_FALSE  1529  'to 1529'

 L. 435      1517  LOAD_GLOBAL              clap
             1520  LOAD_ATTR                __version__
             1523  STORE_FAST               'V'
             1526  JUMP_FORWARD       1544  'to 1544'
             1529  ELSE                     '1544'

 L. 436      1529  LOAD_STR                 "diclipy: fatal: there is no '{0}' component"
             1532  LOAD_ATTR                format
             1535  LOAD_FAST                'component'
             1538  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1541  STORE_FAST               'V'
           1544_0  COME_FROM          1526  '1526'
           1544_1  COME_FROM          1502  '1502'
           1544_2  COME_FROM          1472  '1472'

 L. 437      1544  LOAD_STR                 '--verbose'
             1547  LOAD_FAST                'optsui'
             1550  COMPARE_OP               in
             1553  POP_JUMP_IF_FALSE  1592  'to 1592'
             1556  LOAD_STR                 'fatal:'
             1559  LOAD_FAST                'V'
             1562  COMPARE_OP               not-in
             1565  POP_JUMP_IF_FALSE  1592  'to 1592'

 L. 438      1568  LOAD_STR                 '{0} version: {1}'
             1571  LOAD_ATTR                format
             1574  LOAD_FAST                'component'
             1577  LOAD_FAST                'V'
             1580  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1583  STORE_FAST               'V'
           1586_0  COME_FROM          1565  '1565'
             1586  JUMP_ABSOLUTE      1592  'to 1592'
             1589  JUMP_FORWARD       1592  'to 1592'
           1592_0  COME_FROM          1589  '1589'

 L. 439      1592  LOAD_GLOBAL              print
             1595  LOAD_FAST                'V'
             1598  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1601  POP_TOP          

 L. 440      1602  LOAD_GLOBAL              exit
             1605  LOAD_CONST               0
             1608  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1611  POP_TOP          
             1612  JUMP_FORWARD       1615  'to 1615'
           1615_0  COME_FROM          1612  '1612'

 L. 441      1615  LOAD_STR                 '--help'
             1618  LOAD_FAST                'optsui'
             1621  COMPARE_OP               in
             1624  POP_JUMP_IF_FALSE  1650  'to 1650'

 L. 443      1627  LOAD_GLOBAL              print
             1630  LOAD_GLOBAL              __doc__
             1633  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1636  POP_TOP          

 L. 444      1637  LOAD_GLOBAL              exit
             1640  LOAD_CONST               0
             1643  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1646  POP_TOP          
             1647  JUMP_FORWARD       1650  'to 1650'
           1650_0  COME_FROM          1647  '1647'

 L. 445      1650  LOAD_STR                 '--handle'
             1653  LOAD_FAST                'optsui'
             1656  COMPARE_OP               in
             1659  POP_JUMP_IF_FALSE  1773  'to 1773'

 L. 446      1662  LOAD_FAST                'optsui'
             1665  LOAD_ATTR                get
             1668  LOAD_STR                 '--handle'
             1671  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1674  LOAD_ATTR                split
             1677  LOAD_STR                 '@'
             1680  LOAD_CONST               2
             1683  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1686  UNPACK_SEQUENCE_2     2 
             1689  STORE_GLOBAL             username
             1692  STORE_GLOBAL             pod

 L. 447      1695  LOAD_GLOBAL              debug
             1698  POP_JUMP_IF_FALSE  1726  'to 1726'

 L. 447      1701  LOAD_GLOBAL              print
             1704  LOAD_STR                 'debug: handle ='
             1707  LOAD_FAST                'optsui'
             1710  LOAD_ATTR                get
             1713  LOAD_STR                 '--handle'
             1716  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1719  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1722  POP_TOP          
             1723  JUMP_FORWARD       1726  'to 1726'
           1726_0  COME_FROM          1723  '1723'

 L. 448      1726  LOAD_GLOBAL              debug
             1729  POP_JUMP_IF_FALSE  1748  'to 1748'

 L. 448      1732  LOAD_GLOBAL              print
             1735  LOAD_STR                 'debug: username ='
             1738  LOAD_GLOBAL              username
             1741  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1744  POP_TOP          
             1745  JUMP_FORWARD       1748  'to 1748'
           1748_0  COME_FROM          1745  '1745'

 L. 449      1748  LOAD_GLOBAL              debug
             1751  POP_JUMP_IF_FALSE  1818  'to 1818'

 L. 449      1754  LOAD_GLOBAL              print
             1757  LOAD_STR                 'debug: pod ='
             1760  LOAD_GLOBAL              pod
             1763  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1766  POP_TOP          
             1767  JUMP_ABSOLUTE      1818  'to 1818'
             1770  JUMP_FORWARD       1818  'to 1818'
             1773  ELSE                     '1818'

 L. 450      1773  LOAD_STR                 '--use-default'
             1776  LOAD_FAST                'optsui'
             1779  COMPARE_OP               in
             1782  POP_JUMP_IF_FALSE  1803  'to 1803'

 L. 450      1785  LOAD_GLOBAL              get_default_handle
             1788  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1791  UNPACK_SEQUENCE_2     2 
             1794  STORE_GLOBAL             username
             1797  STORE_GLOBAL             pod
             1800  JUMP_FORWARD       1818  'to 1818'
             1803  ELSE                     '1818'

 L. 451      1803  LOAD_GLOBAL              get_default_handle
             1806  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1809  UNPACK_SEQUENCE_2     2 
             1812  STORE_GLOBAL             username
             1815  STORE_GLOBAL             pod
           1818_0  COME_FROM          1800  '1800'
           1818_1  COME_FROM          1770  '1770'

 L. 452      1818  SETUP_FINALLY      2523  'to 2523'
             1821  SETUP_EXCEPT       2411  'to 2411'

 L. 453      1824  LOAD_CONST               False
             1827  STORE_FAST               'KeyInrt'

 L. 454      1830  LOAD_CONST               True
             1833  STORE_FAST               'fail'

 L. 455      1836  LOAD_GLOBAL              username
             1839  POP_JUMP_IF_TRUE   1857  'to 1857'

 L. 455      1842  LOAD_GLOBAL              input
             1845  LOAD_STR                 'D* username: '
             1848  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1851  STORE_GLOBAL             username
             1854  JUMP_FORWARD       1857  'to 1857'
           1857_0  COME_FROM          1854  '1854'

 L. 456      1857  LOAD_GLOBAL              pod
             1860  POP_JUMP_IF_TRUE   1878  'to 1878'

 L. 456      1863  LOAD_GLOBAL              input
             1866  LOAD_STR                 'D* pod: '
             1869  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1872  STORE_GLOBAL             pod
             1875  JUMP_FORWARD       1878  'to 1878'
           1878_0  COME_FROM          1875  '1875'

 L. 457      1878  LOAD_STR                 '--password'
             1881  LOAD_FAST                'optsui'
             1884  COMPARE_OP               in
             1887  POP_JUMP_IF_FALSE  1908  'to 1908'

 L. 457      1890  LOAD_FAST                'optsui'
             1893  LOAD_ATTR                get
             1896  LOAD_STR                 '--password'
             1899  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1902  STORE_GLOBAL             password
             1905  JUMP_FORWARD       1908  'to 1908'
           1908_0  COME_FROM          1905  '1905'

 L. 459      1908  LOAD_STR                 '--save-auth'
             1911  LOAD_FAST                'optsui'
             1914  COMPARE_OP               in
             1917  POP_JUMP_IF_TRUE   1980  'to 1980'
             1920  LOAD_STR                 '--handle'
             1923  LOAD_FAST                'optsui'
             1926  COMPARE_OP               in
           1929_0  COME_FROM          1917  '1917'
             1929  POP_JUMP_IF_FALSE  1935  'to 1935'

 L. 459      1932  JUMP_FORWARD       1980  'to 1980'
             1935  ELSE                     '1980'

 L. 460      1935  LOAD_STR                 '--load-auth'
             1938  LOAD_FAST                'optsui'
             1941  COMPARE_OP               in
             1944  POP_JUMP_IF_FALSE  1965  'to 1965'

 L. 460      1947  LOAD_GLOBAL              load_auth
             1950  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1953  UNPACK_SEQUENCE_2     2 
             1956  STORE_GLOBAL             password
             1959  STORE_GLOBAL             savedconn
             1962  JUMP_FORWARD       1980  'to 1980'
             1965  ELSE                     '1980'

 L. 461      1965  LOAD_GLOBAL              load_auth
             1968  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1971  UNPACK_SEQUENCE_2     2 
             1974  STORE_GLOBAL             password
             1977  STORE_GLOBAL             savedconn
           1980_0  COME_FROM          1962  '1962'
           1980_1  COME_FROM          1932  '1932'

 L. 462      1980  LOAD_GLOBAL              password
             1983  POP_JUMP_IF_TRUE   1998  'to 1998'

 L. 462      1986  LOAD_GLOBAL              get_password
             1989  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1992  STORE_GLOBAL             password
             1995  JUMP_FORWARD       1998  'to 1998'
           1998_0  COME_FROM          1995  '1995'

 L. 466      1998  LOAD_STR                 '--proto'
             2001  LOAD_FAST                'optsui'
             2004  COMPARE_OP               in
             2007  POP_JUMP_IF_FALSE  2028  'to 2028'

 L. 466      2010  LOAD_FAST                'optsui'
             2013  LOAD_ATTR                get
             2016  LOAD_STR                 '--proto'
             2019  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2022  STORE_GLOBAL             proto
             2025  JUMP_FORWARD       2028  'to 2028'
           2028_0  COME_FROM          2025  '2025'

 L. 468      2028  LOAD_GLOBAL              re
             2031  LOAD_ATTR                compile
             2034  LOAD_STR                 '^[a-z]://.*'
             2037  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2040  LOAD_ATTR                match
             2043  LOAD_GLOBAL              pod
             2046  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2049  POP_JUMP_IF_TRUE   2073  'to 2073'

 L. 468      2052  LOAD_STR                 '{0}://{1}'
             2055  LOAD_ATTR                format
             2058  LOAD_GLOBAL              proto
             2061  LOAD_GLOBAL              pod
             2064  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2067  STORE_GLOBAL             schemed
             2070  JUMP_FORWARD       2079  'to 2079'
             2073  ELSE                     '2079'

 L. 469      2073  LOAD_GLOBAL              pod
             2076  STORE_GLOBAL             schemed
           2079_0  COME_FROM          2070  '2070'

 L. 470      2079  LOAD_GLOBAL              debug
             2082  POP_JUMP_IF_FALSE  2101  'to 2101'

 L. 470      2085  LOAD_GLOBAL              print
             2088  LOAD_STR                 'debug: pod url ='
             2091  LOAD_GLOBAL              schemed
             2094  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2097  POP_TOP          
             2098  JUMP_FORWARD       2101  'to 2101'
           2101_0  COME_FROM          2098  '2098'

 L. 472      2101  LOAD_GLOBAL              savedconn
             2104  POP_JUMP_IF_TRUE   2162  'to 2162'

 L. 473      2107  LOAD_GLOBAL              verbose
             2110  POP_JUMP_IF_FALSE  2126  'to 2126'

 L. 473      2113  LOAD_GLOBAL              print
             2116  LOAD_STR                 'Trying to get new connection...'
             2119  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2122  POP_TOP          
             2123  JUMP_FORWARD       2126  'to 2126'
           2126_0  COME_FROM          2123  '2123'

 L. 474      2126  LOAD_GLOBAL              diaspy
             2129  LOAD_ATTR                connection
             2132  LOAD_ATTR                Connection
             2135  LOAD_STR                 'pod'
             2138  LOAD_GLOBAL              schemed
             2141  LOAD_STR                 'username'
             2144  LOAD_GLOBAL              username
             2147  LOAD_STR                 'password'
             2150  LOAD_GLOBAL              password
             2153  CALL_FUNCTION_768   768  '0 positional, 3 named'
             2156  STORE_FAST               'connection'
             2159  JUMP_FORWARD       2187  'to 2187'
             2162  ELSE                     '2187'

 L. 476      2162  LOAD_GLOBAL              savedconn
             2165  STORE_FAST               'connection'

 L. 477      2168  LOAD_GLOBAL              verbose
             2171  POP_JUMP_IF_FALSE  2187  'to 2187'

 L. 477      2174  LOAD_GLOBAL              print
             2177  LOAD_STR                 'Reusing saved connection.'
             2180  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2183  POP_TOP          
             2184  JUMP_FORWARD       2187  'to 2187'
           2187_0  COME_FROM          2184  '2184'
           2187_1  COME_FROM          2159  '2159'

 L. 478      2187  LOAD_GLOBAL              debug
             2190  POP_JUMP_IF_FALSE  2296  'to 2296'

 L. 479      2193  LOAD_GLOBAL              print
             2196  LOAD_STR                 'debug: type of "connection" ='
             2199  LOAD_GLOBAL              type
             2202  LOAD_FAST                'connection'
             2205  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2208  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2211  POP_TOP          

 L. 480      2212  LOAD_GLOBAL              print
             2215  LOAD_STR                 'debug: connection._login_data ='
             2218  LOAD_FAST                'connection'
             2221  LOAD_ATTR                _login_data
             2224  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2227  POP_TOP          

 L. 481      2228  LOAD_GLOBAL              print
             2231  LOAD_STR                 '\ndebug: dir(connection):'
             2234  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2237  POP_TOP          

 L. 482      2238  LOAD_GLOBAL              print
             2241  LOAD_GLOBAL              dir
             2244  LOAD_FAST                'connection'
             2247  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2250  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2253  POP_TOP          

 L. 483      2254  LOAD_GLOBAL              print
             2257  LOAD_STR                 '\ndebug: connection.__dict__:'
             2260  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2263  POP_TOP          

 L. 484      2264  LOAD_FAST                'pprint'
             2267  LOAD_FAST                'connection'
             2270  LOAD_ATTR                __dict__
             2273  LOAD_STR                 'indent'
             2276  LOAD_CONST               2
             2279  CALL_FUNCTION_257   257  '1 positional, 1 named'
             2282  POP_TOP          

 L. 485      2283  LOAD_GLOBAL              print
             2286  LOAD_STR                 ''
             2289  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2292  POP_TOP          
             2293  JUMP_FORWARD       2296  'to 2296'
           2296_0  COME_FROM          2293  '2293'

 L. 487      2296  LOAD_FAST                'connection'
             2299  LOAD_ATTR                login
             2302  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2305  STORE_FAST               'login'

 L. 491      2308  LOAD_GLOBAL              debug
             2311  POP_JUMP_IF_FALSE  2401  'to 2401'

 L. 492      2314  LOAD_GLOBAL              print
             2317  LOAD_STR                 'debug: type of "login" ='
             2320  LOAD_GLOBAL              type
             2323  LOAD_FAST                'login'
             2326  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2329  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2332  POP_TOP          

 L. 493      2333  LOAD_GLOBAL              print
             2336  LOAD_STR                 '\ndebug: dir(login):'
             2339  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2342  POP_TOP          

 L. 494      2343  LOAD_GLOBAL              print
             2346  LOAD_GLOBAL              dir
             2349  LOAD_FAST                'login'
             2352  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2355  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2358  POP_TOP          

 L. 495      2359  LOAD_GLOBAL              print
             2362  LOAD_STR                 '\ndebug: login.__dict__:'
             2365  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2368  POP_TOP          

 L. 496      2369  LOAD_FAST                'pprint'
             2372  LOAD_FAST                'login'
             2375  LOAD_ATTR                __dict__
             2378  LOAD_STR                 'indent'
             2381  LOAD_CONST               2
             2384  CALL_FUNCTION_257   257  '1 positional, 1 named'
             2387  POP_TOP          

 L. 497      2388  LOAD_GLOBAL              print
             2391  LOAD_STR                 ''
             2394  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2397  POP_TOP          
             2398  JUMP_FORWARD       2401  'to 2401'
           2401_0  COME_FROM          2398  '2398'

 L. 498      2401  LOAD_CONST               False
             2404  STORE_FAST               'fail'
             2407  POP_BLOCK        
             2408  JUMP_FORWARD       2519  'to 2519'
           2411_0  COME_FROM_EXCEPT   1821  '1821'

 L. 499      2411  DUP_TOP          
             2412  LOAD_GLOBAL              KeyboardInterrupt
             2415  LOAD_GLOBAL              EOFError
             2418  BUILD_TUPLE_2         2 
             2421  COMPARE_OP               exception-match
             2424  POP_JUMP_IF_FALSE  2457  'to 2457'
             2427  POP_TOP          
             2428  POP_TOP          
             2429  POP_TOP          

 L. 501      2430  LOAD_CONST               True
             2433  STORE_FAST               'KeyInrt'

 L. 502      2436  LOAD_GLOBAL              print
             2439  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2442  POP_TOP          

 L. 503      2443  LOAD_GLOBAL              print
             2446  LOAD_STR                 'Keyboard Interrupt. Exit.'
             2449  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2452  POP_TOP          
             2453  POP_EXCEPT       
             2454  JUMP_FORWARD       2519  'to 2519'

 L. 504      2457  DUP_TOP          
             2458  LOAD_GLOBAL              Exception
             2461  COMPARE_OP               exception-match
             2464  POP_JUMP_IF_FALSE  2518  'to 2518'
             2467  POP_TOP          
             2468  STORE_FAST               'e'
             2471  POP_TOP          
             2472  SETUP_FINALLY      2505  'to 2505'

 L. 505      2475  LOAD_CONST               True
             2478  STORE_FAST               'fail'

 L. 506      2481  LOAD_GLOBAL              print
             2484  LOAD_STR                 'diclipy: connection: error encountered: {0}'
             2487  LOAD_ATTR                format
             2490  LOAD_FAST                'e'
             2493  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2496  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2499  POP_TOP          
             2500  POP_BLOCK        
             2501  POP_EXCEPT       
             2502  LOAD_CONST               None
           2505_0  COME_FROM_FINALLY  2472  '2472'
             2505  LOAD_CONST               None
             2508  STORE_FAST               'e'
             2511  DELETE_FAST              'e'
             2514  END_FINALLY      
             2515  JUMP_FORWARD       2519  'to 2519'
             2518  END_FINALLY      
           2519_0  COME_FROM          2515  '2515'
           2519_1  COME_FROM          2454  '2454'
           2519_2  COME_FROM          2408  '2408'
             2519  POP_BLOCK        
             2520  LOAD_CONST               None
           2523_0  COME_FROM_FINALLY  1818  '1818'

 L. 508      2523  LOAD_FAST                'KeyInrt'
             2526  POP_JUMP_IF_FALSE  2542  'to 2542'

 L. 510      2529  LOAD_GLOBAL              exit
             2532  LOAD_CONST               0
             2535  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2538  POP_TOP          
             2539  JUMP_FORWARD       2542  'to 2542'
           2542_0  COME_FROM          2539  '2539'

 L. 511      2542  LOAD_FAST                'fail'
             2545  POP_JUMP_IF_FALSE  2708  'to 2708'

 L. 513      2548  SETUP_FINALLY      2673  'to 2673'
             2551  SETUP_EXCEPT       2607  'to 2607'

 L. 514      2554  LOAD_GLOBAL              print
             2557  LOAD_STR                 'Retrying to get connection...'
             2560  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2563  POP_TOP          

 L. 515      2564  LOAD_GLOBAL              diaspy
             2567  LOAD_ATTR                connection
             2570  LOAD_ATTR                Connection
             2573  LOAD_STR                 'pod'
             2576  LOAD_GLOBAL              schemed
             2579  LOAD_STR                 'username'
             2582  LOAD_GLOBAL              username
             2585  LOAD_STR                 'password'
             2588  LOAD_GLOBAL              password
             2591  CALL_FUNCTION_768   768  '0 positional, 3 named'
             2594  STORE_FAST               'connection'

 L. 516      2597  LOAD_CONST               False
             2600  STORE_FAST               'fail'
             2603  POP_BLOCK        
             2604  JUMP_FORWARD       2669  'to 2669'
           2607_0  COME_FROM_EXCEPT   2551  '2551'

 L. 517      2607  DUP_TOP          
             2608  LOAD_GLOBAL              Exception
             2611  COMPARE_OP               exception-match
             2614  POP_JUMP_IF_FALSE  2668  'to 2668'
             2617  POP_TOP          
             2618  STORE_FAST               'e'
             2621  POP_TOP          
             2622  SETUP_FINALLY      2655  'to 2655'

 L. 518      2625  LOAD_CONST               True
             2628  STORE_FAST               'fail'

 L. 519      2631  LOAD_GLOBAL              print
             2634  LOAD_STR                 'diclipy: connection: error encountered: {0}'
             2637  LOAD_ATTR                format
             2640  LOAD_FAST                'e'
             2643  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2646  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2649  POP_TOP          
             2650  POP_BLOCK        
             2651  POP_EXCEPT       
             2652  LOAD_CONST               None
           2655_0  COME_FROM_FINALLY  2622  '2622'
             2655  LOAD_CONST               None
             2658  STORE_FAST               'e'
             2661  DELETE_FAST              'e'
             2664  END_FINALLY      
             2665  JUMP_FORWARD       2669  'to 2669'
             2668  END_FINALLY      
           2669_0  COME_FROM          2665  '2665'
           2669_1  COME_FROM          2604  '2604'
             2669  POP_BLOCK        
             2670  LOAD_CONST               None
           2673_0  COME_FROM_FINALLY  2548  '2548'

 L. 521      2673  LOAD_FAST                'fail'
             2676  POP_JUMP_IF_FALSE  2692  'to 2692'

 L. 522      2679  LOAD_GLOBAL              exit
             2682  LOAD_CONST               1
             2685  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2688  POP_TOP          
             2689  JUMP_FORWARD       2692  'to 2692'
           2692_0  COME_FROM          2689  '2689'

 L. 524      2692  LOAD_FAST                'connection'
             2695  LOAD_ATTR                login
             2698  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2701  STORE_FAST               'login'
             2704  END_FINALLY      
             2705  JUMP_FORWARD       2708  'to 2708'
           2708_0  COME_FROM          2705  '2705'

 L. 525      2708  LOAD_STR                 '--set-default'
             2711  LOAD_FAST                'optsui'
             2714  COMPARE_OP               in
             2717  POP_JUMP_IF_FALSE  2806  'to 2806'

 L. 526      2720  LOAD_GLOBAL              set_default_handle
             2723  LOAD_GLOBAL              username
             2726  LOAD_GLOBAL              pod
             2729  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2732  POP_TOP          

 L. 527      2733  LOAD_GLOBAL              verbose
             2736  POP_JUMP_IF_FALSE  2806  'to 2806'

 L. 528      2739  LOAD_GLOBAL              os
             2742  LOAD_ATTR                path
             2745  LOAD_ATTR                expanduser
             2748  LOAD_STR                 '~/.diclipy/defhandle.json'
             2751  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2754  STORE_FAST               'defhandlepath'

 L. 529      2757  LOAD_GLOBAL              os
             2760  LOAD_ATTR                path
             2763  LOAD_ATTR                isfile
             2766  LOAD_FAST                'defhandlepath'
             2769  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2772  POP_JUMP_IF_FALSE  2803  'to 2803'

 L. 530      2775  LOAD_GLOBAL              print
             2778  LOAD_STR                 'Default handle setted to: {0}@{1}'
             2781  LOAD_ATTR                format
             2784  LOAD_GLOBAL              username
             2787  LOAD_GLOBAL              pod
             2790  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2793  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2796  POP_TOP          
             2797  JUMP_ABSOLUTE      2803  'to 2803'
             2800  JUMP_ABSOLUTE      2806  'to 2806'
             2803  JUMP_FORWARD       2806  'to 2806'
           2806_0  COME_FROM          2803  '2803'

 L. 531      2806  LOAD_STR                 '--save-auth'
             2809  LOAD_FAST                'optsui'
             2812  COMPARE_OP               in
             2815  POP_JUMP_IF_FALSE  3298  'to 3298'

 L. 533      2818  LOAD_GLOBAL              get_authdb
             2821  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2824  STORE_FAST               'authdb'

 L. 534      2827  LOAD_STR                 '{0}@{1}'
             2830  LOAD_ATTR                format
             2833  LOAD_GLOBAL              username
             2836  LOAD_GLOBAL              pod
             2839  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2842  STORE_GLOBAL             passkey

 L. 535      2845  LOAD_GLOBAL              password
             2848  LOAD_FAST                'authdb'
             2851  LOAD_GLOBAL              passkey
             2854  STORE_SUBSCR     

 L. 536      2855  LOAD_GLOBAL              sure_path_exists
             2858  LOAD_GLOBAL              os
             2861  LOAD_ATTR                path
             2864  LOAD_ATTR                expanduser
             2867  LOAD_STR                 '~/.diclipy'
             2870  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2873  LOAD_STR                 'mode'
             2876  LOAD_CONST               448
             2879  CALL_FUNCTION_257   257  '1 positional, 1 named'
             2882  POP_TOP          

 L. 539      2883  LOAD_GLOBAL              os
             2886  LOAD_ATTR                path
             2889  LOAD_ATTR                expanduser
             2892  LOAD_STR                 '~/.diclipy/{}.connection'
             2895  LOAD_ATTR                format
             2898  LOAD_GLOBAL              passkey
             2901  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2904  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2907  STORE_FAST               'connpath'

 L. 540      2910  LOAD_GLOBAL              open
             2913  LOAD_FAST                'connpath'
             2916  LOAD_STR                 'wb'
             2919  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2922  STORE_FAST               'f'

 L. 541      2925  SETUP_FINALLY      3096  'to 3096'
             2928  SETUP_EXCEPT       2966  'to 2966'

 L. 542      2931  LOAD_CONST               False
             2934  STORE_FAST               'success'

 L. 543      2937  LOAD_GLOBAL              pickle
             2940  LOAD_ATTR                dump
             2943  LOAD_FAST                'connection'
             2946  LOAD_FAST                'f'
             2949  LOAD_CONST               3
             2952  CALL_FUNCTION_3       3  '3 positional, 0 named'
             2955  POP_TOP          

 L. 544      2956  LOAD_CONST               True
             2959  STORE_FAST               'success'
             2962  POP_BLOCK        
             2963  JUMP_FORWARD       3092  'to 3092'
           2966_0  COME_FROM_EXCEPT   2928  '2928'

 L. 545      2966  DUP_TOP          
             2967  LOAD_GLOBAL              pickle
             2970  LOAD_ATTR                PicklingError
             2973  COMPARE_OP               exception-match
             2976  POP_JUMP_IF_FALSE  3030  'to 3030'
             2979  POP_TOP          
             2980  STORE_FAST               'e'
             2983  POP_TOP          
             2984  SETUP_FINALLY      3017  'to 3017'

 L. 546      2987  LOAD_GLOBAL              print
             2990  LOAD_STR                 '\ndiclipy: pickle dump: problems with the serialization of the object was hapened: {}'
             2993  LOAD_ATTR                format
             2996  LOAD_FAST                'e'
             2999  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3002  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3005  POP_TOP          

 L. 547      3006  LOAD_CONST               False
             3009  STORE_FAST               'success'
             3012  POP_BLOCK        
             3013  POP_EXCEPT       
             3014  LOAD_CONST               None
           3017_0  COME_FROM_FINALLY  2984  '2984'
             3017  LOAD_CONST               None
             3020  STORE_FAST               'e'
             3023  DELETE_FAST              'e'
             3026  END_FINALLY      
             3027  JUMP_FORWARD       3092  'to 3092'

 L. 548      3030  DUP_TOP          
             3031  LOAD_GLOBAL              Exception
             3034  COMPARE_OP               exception-match
             3037  POP_JUMP_IF_FALSE  3091  'to 3091'
             3040  POP_TOP          
             3041  STORE_FAST               'e'
             3044  POP_TOP          
             3045  SETUP_FINALLY      3078  'to 3078'

 L. 549      3048  LOAD_GLOBAL              print
             3051  LOAD_STR                 '\ndiclipy: pickle dump: error encountered: {0}'
             3054  LOAD_ATTR                format
             3057  LOAD_FAST                'e'
             3060  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3063  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3066  POP_TOP          

 L. 550      3067  LOAD_CONST               False
             3070  STORE_FAST               'success'
             3073  POP_BLOCK        
             3074  POP_EXCEPT       
             3075  LOAD_CONST               None
           3078_0  COME_FROM_FINALLY  3045  '3045'
             3078  LOAD_CONST               None
             3081  STORE_FAST               'e'
             3084  DELETE_FAST              'e'
             3087  END_FINALLY      
             3088  JUMP_FORWARD       3092  'to 3092'
             3091  END_FINALLY      
           3092_0  COME_FROM          3088  '3088'
           3092_1  COME_FROM          3027  '3027'
           3092_2  COME_FROM          2963  '2963'
             3092  POP_BLOCK        
             3093  LOAD_CONST               None
           3096_0  COME_FROM_FINALLY  2925  '2925'

 L. 552      3096  LOAD_FAST                'f'
             3099  LOAD_ATTR                close
             3102  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3105  POP_TOP          

 L. 553      3106  LOAD_FAST                'success'
             3109  POP_JUMP_IF_FALSE  3171  'to 3171'

 L. 554      3112  LOAD_GLOBAL              os
             3115  LOAD_ATTR                chmod
             3118  LOAD_FAST                'connpath'
             3121  LOAD_CONST               384
             3124  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3127  POP_TOP          

 L. 555      3128  LOAD_GLOBAL              verbose
             3131  POP_JUMP_IF_FALSE  3171  'to 3171'

 L. 556      3134  LOAD_GLOBAL              os
             3137  LOAD_ATTR                path
             3140  LOAD_ATTR                isfile
             3143  LOAD_FAST                'connpath'
             3146  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3149  POP_JUMP_IF_FALSE  3168  'to 3168'

 L. 556      3152  LOAD_GLOBAL              print
             3155  LOAD_STR                 'Connection saved.'
             3158  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3161  POP_TOP          
             3162  JUMP_ABSOLUTE      3168  'to 3168'
             3165  JUMP_ABSOLUTE      3171  'to 3171'
             3168  JUMP_FORWARD       3171  'to 3171'
           3171_0  COME_FROM          3168  '3168'
             3171  END_FINALLY      

 L. 557      3172  LOAD_GLOBAL              os
             3175  LOAD_ATTR                path
             3178  LOAD_ATTR                expanduser
             3181  LOAD_STR                 '~/.diclipy/auth.json'
             3184  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3187  STORE_FAST               'authdbpath'

 L. 558      3190  LOAD_GLOBAL              open
             3193  LOAD_FAST                'authdbpath'
             3196  LOAD_STR                 'w'
             3199  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3202  STORE_FAST               'ofstream'

 L. 559      3205  LOAD_FAST                'ofstream'
             3208  LOAD_ATTR                write
             3211  LOAD_GLOBAL              json
             3214  LOAD_ATTR                dumps
             3217  LOAD_FAST                'authdb'
             3220  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3223  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3226  STORE_FAST               'authdb'

 L. 560      3229  LOAD_FAST                'ofstream'
             3232  LOAD_ATTR                close
             3235  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3238  POP_TOP          

 L. 561      3239  LOAD_GLOBAL              os
             3242  LOAD_ATTR                chmod
             3245  LOAD_FAST                'authdbpath'
             3248  LOAD_CONST               384
             3251  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3254  POP_TOP          

 L. 562      3255  LOAD_GLOBAL              verbose
             3258  POP_JUMP_IF_FALSE  3298  'to 3298'

 L. 563      3261  LOAD_GLOBAL              os
             3264  LOAD_ATTR                path
             3267  LOAD_ATTR                isfile
             3270  LOAD_FAST                'authdbpath'
             3273  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3276  POP_JUMP_IF_FALSE  3295  'to 3295'

 L. 563      3279  LOAD_GLOBAL              print
             3282  LOAD_STR                 'Auth saved.'
             3285  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3288  POP_TOP          
             3289  JUMP_ABSOLUTE      3295  'to 3295'
             3292  JUMP_ABSOLUTE      3298  'to 3298'
             3295  JUMP_FORWARD       3298  'to 3298'
           3298_0  COME_FROM          3295  '3295'
             3298  END_FINALLY      

 L. 567      3299  LOAD_FAST                'optsui'
             3302  LOAD_ATTR                down
             3305  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3308  STORE_FAST               'optsui'

 L. 569      3311  LOAD_GLOBAL              str
             3314  LOAD_FAST                'optsui'
             3317  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3320  LOAD_STR                 ''
             3323  COMPARE_OP               ==
             3326  POP_JUMP_IF_FALSE  3417  'to 3417'

 L. 570      3329  LOAD_GLOBAL              verbose
             3332  POP_JUMP_IF_FALSE  3348  'to 3348'

 L. 570      3335  LOAD_GLOBAL              print
             3338  LOAD_STR                 'No command was given. Exit.'
             3341  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3344  POP_TOP          
             3345  JUMP_FORWARD       3348  'to 3348'
           3348_0  COME_FROM          3345  '3345'

 L. 571      3348  LOAD_GLOBAL              debug
             3351  POP_JUMP_IF_FALSE  3376  'to 3376'

 L. 571      3354  LOAD_GLOBAL              print
             3357  LOAD_STR                 'debug: options ='
             3360  LOAD_GLOBAL              str
             3363  LOAD_FAST                'options'
             3366  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3369  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3372  POP_TOP          
             3373  JUMP_FORWARD       3376  'to 3376'
           3376_0  COME_FROM          3373  '3373'

 L. 572      3376  LOAD_GLOBAL              debug
             3379  POP_JUMP_IF_FALSE  3404  'to 3404'

 L. 572      3382  LOAD_GLOBAL              print
             3385  LOAD_STR                 'debug: optsui ='
             3388  LOAD_GLOBAL              str
             3391  LOAD_FAST                'optsui'
             3394  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3397  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3400  POP_TOP          
             3401  JUMP_FORWARD       3404  'to 3404'
           3404_0  COME_FROM          3401  '3401'

 L. 574      3404  LOAD_GLOBAL              exit
             3407  LOAD_CONST               0
             3410  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3413  POP_TOP          
             3414  JUMP_FORWARD       3417  'to 3417'
           3417_0  COME_FROM          3414  '3414'

 L. 575      3417  LOAD_STR                 ''
             3420  STORE_FAST               'message'

 L. 576      3423  LOAD_GLOBAL              str
             3426  LOAD_FAST                'optsui'
             3429  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3432  LOAD_STR                 'post'
             3435  COMPARE_OP               ==
             3438  POP_JUMP_IF_FALSE  4948  'to 4948'

 L. 580      3441  LOAD_STR                 '--message'
             3444  LOAD_FAST                'optsui'
             3447  COMPARE_OP               in
             3450  POP_JUMP_IF_FALSE  3963  'to 3963'

 L. 582      3453  LOAD_STR                 '--image'
             3456  LOAD_FAST                'optsui'
             3459  COMPARE_OP               in
             3462  POP_JUMP_IF_FALSE  3483  'to 3483'

 L. 584      3465  LOAD_FAST                'optsui'
             3468  LOAD_ATTR                get
             3471  LOAD_STR                 '--image'
             3474  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3477  STORE_FAST               'photo'
             3480  JUMP_FORWARD       3489  'to 3489'
             3483  ELSE                     '3489'

 L. 585      3483  LOAD_STR                 ''
             3486  STORE_FAST               'photo'
           3489_0  COME_FROM          3480  '3480'

 L. 590      3489  LOAD_STR                 '{}'
             3492  LOAD_ATTR                format
             3495  LOAD_FAST                'optsui'
             3498  LOAD_ATTR                get
             3501  LOAD_STR                 '--message'
             3504  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3507  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3510  LOAD_ATTR                replace
             3513  LOAD_STR                 '\\n'
             3516  LOAD_STR                 '\n'
             3519  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3522  STORE_FAST               'text'

 L. 592      3525  LOAD_STR                 '--stdin'
             3528  LOAD_FAST                'optsui'
             3531  COMPARE_OP               in
             3534  POP_JUMP_IF_FALSE  3562  'to 3562'

 L. 593      3537  LOAD_FAST                'text'
             3540  LOAD_STR                 '{}'
             3543  LOAD_ATTR                format
             3546  LOAD_GLOBAL              get_user_input
             3549  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3552  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3555  INPLACE_ADD      
             3556  STORE_FAST               'text'
             3559  JUMP_FORWARD       3641  'to 3641'
             3562  ELSE                     '3641'

 L. 594      3562  LOAD_FAST                'optsui'
             3565  LOAD_ATTR                get
             3568  LOAD_STR                 '--message'
             3571  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3574  LOAD_STR                 '-'
             3577  COMPARE_OP               ==
             3580  POP_JUMP_IF_FALSE  3641  'to 3641'

 L. 599      3583  LOAD_STR                 '{}'
             3586  LOAD_ATTR                format
             3589  LOAD_GLOBAL              get_user_input
             3592  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3595  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3598  STORE_FAST               'text'

 L. 600      3601  LOAD_STR                 '--stdin'
             3604  LOAD_FAST                'optsui'
             3607  COMPARE_OP               in
             3610  POP_JUMP_IF_FALSE  3641  'to 3641'

 L. 601      3613  LOAD_FAST                'text'
             3616  LOAD_STR                 '{}'
             3619  LOAD_ATTR                format
             3622  LOAD_GLOBAL              get_user_input
             3625  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3628  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3631  INPLACE_ADD      
             3632  STORE_FAST               'text'
             3635  JUMP_ABSOLUTE      3641  'to 3641'
             3638  JUMP_FORWARD       3641  'to 3641'
           3641_0  COME_FROM          3638  '3638'
           3641_1  COME_FROM          3559  '3559'

 L. 602      3641  LOAD_FAST                'optsui'
             3644  LOAD_ATTR                get
             3647  LOAD_STR                 '--aspect'
             3650  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3653  STORE_FAST               'aspect_ids'

 L. 603      3656  LOAD_FAST                'aspect_ids'
             3659  POP_JUMP_IF_FALSE  3671  'to 3671'

 L. 604      3662  LOAD_FAST                'aspect_ids'
             3665  STORE_FAST               'aspect'
             3668  JUMP_FORWARD       3677  'to 3677'
             3671  ELSE                     '3677'

 L. 607      3671  LOAD_STR                 'pubic'
             3674  STORE_FAST               'aspect'
           3677_0  COME_FROM          3668  '3668'

 L. 608      3677  LOAD_GLOBAL              debug
             3680  POP_JUMP_IF_FALSE  3699  'to 3699'

 L. 608      3683  LOAD_GLOBAL              print
             3686  LOAD_STR                 'aspect ='
             3689  LOAD_FAST                'aspect'
             3692  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3695  POP_TOP          
             3696  JUMP_FORWARD       3699  'to 3699'
           3699_0  COME_FROM          3696  '3696'

 L. 610      3699  LOAD_FAST                'text'
             3702  POP_JUMP_IF_TRUE   3711  'to 3711'
             3705  LOAD_FAST                'photo'
           3708_0  COME_FROM          3702  '3702'
             3708  POP_JUMP_IF_FALSE  3954  'to 3954'

 L. 612      3711  LOAD_GLOBAL              verbose
             3714  POP_JUMP_IF_FALSE  3730  'to 3730'

 L. 612      3717  LOAD_GLOBAL              print
             3720  LOAD_STR                 'Posting ...'
             3723  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3726  POP_TOP          
             3727  JUMP_FORWARD       3730  'to 3730'
           3730_0  COME_FROM          3727  '3727'

 L. 613      3730  LOAD_GLOBAL              diaspy
             3733  LOAD_ATTR                streams
             3736  LOAD_ATTR                Activity
             3739  LOAD_FAST                'connection'
             3742  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3745  LOAD_ATTR                post
             3748  LOAD_STR                 'text'
             3751  LOAD_FAST                'text'
             3754  LOAD_STR                 'aspect_ids'
             3757  LOAD_FAST                'aspect'
             3760  LOAD_STR                 'photo'
             3763  LOAD_FAST                'photo'
             3766  CALL_FUNCTION_768   768  '0 positional, 3 named'
             3769  STORE_FAST               'post'

 L. 614      3772  LOAD_GLOBAL              debug
             3775  POP_JUMP_IF_FALSE  3859  'to 3859'

 L. 615      3778  LOAD_GLOBAL              print
             3781  LOAD_STR                 'debug: post:'
             3784  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3787  POP_TOP          

 L. 616      3788  LOAD_FAST                'pprint'
             3791  LOAD_FAST                'post'
             3794  LOAD_ATTR                __dict__
             3797  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3800  LOAD_STR                 'indent'
             3803  LOAD_CONST               2
             3806  CALL_FUNCTION_257   257  '1 positional, 1 named'
             3809  POP_TOP          

 L. 617      3810  LOAD_GLOBAL              print
             3813  LOAD_STR                 '\ndebug: post.id:'
             3816  LOAD_FAST                'post'
             3819  LOAD_STR                 'id'
             3822  BINARY_SUBSCR    
             3823  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3826  POP_TOP          

 L. 618      3827  LOAD_GLOBAL              print
             3830  LOAD_STR                 'debug: post.guid:'
             3833  LOAD_FAST                'post'
             3836  LOAD_STR                 'guid'
             3839  BINARY_SUBSCR    
             3840  LOAD_ATTR                replace
             3843  LOAD_STR                 "'"
             3846  LOAD_STR                 ''
             3849  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3852  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3855  POP_TOP          
             3856  JUMP_FORWARD       3859  'to 3859'
           3859_0  COME_FROM          3856  '3856'

 L. 619      3859  LOAD_GLOBAL              len
             3862  LOAD_FAST                'post'
             3865  LOAD_STR                 'guid'
             3868  BINARY_SUBSCR    
             3869  LOAD_ATTR                replace
             3872  LOAD_STR                 "'"
             3875  LOAD_STR                 ''
             3878  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3881  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3884  LOAD_CONST               2
             3887  COMPARE_OP               >
             3890  POP_JUMP_IF_FALSE  3918  'to 3918'

 L. 620      3893  LOAD_FAST                'post'
             3896  LOAD_STR                 'guid'
             3899  BINARY_SUBSCR    
             3900  LOAD_ATTR                replace
             3903  LOAD_STR                 "'"
             3906  LOAD_STR                 ''
             3909  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3912  STORE_FAST               'pid'
             3915  JUMP_FORWARD       3933  'to 3933'
             3918  ELSE                     '3933'

 L. 621      3918  LOAD_GLOBAL              repr
             3921  LOAD_FAST                'post'
             3924  LOAD_ATTR                id
             3927  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3930  STORE_FAST               'pid'
           3933_0  COME_FROM          3915  '3915'

 L. 622      3933  LOAD_STR                 '** post url: {0}/posts/{1}'
             3936  LOAD_ATTR                format
             3939  LOAD_GLOBAL              schemed
             3942  LOAD_FAST                'pid'
             3945  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3948  STORE_FAST               'message'
             3951  JUMP_ABSOLUTE      3963  'to 3963'
             3954  ELSE                     '3960'

 L. 623      3954  LOAD_STR                 'diclipy: fatal: nothing to post'
             3957  STORE_FAST               'message'
             3960  JUMP_FORWARD       3963  'to 3963'
           3963_0  COME_FROM          3960  '3960'

 L. 624      3963  LOAD_STR                 '--read'
             3966  LOAD_FAST                'optsui'
             3969  COMPARE_OP               in
             3972  POP_JUMP_IF_FALSE  4314  'to 4314'

 L. 626      3975  LOAD_STR                 '--id'
             3978  LOAD_FAST                'optsui'
             3981  COMPARE_OP               in
             3984  POP_JUMP_IF_FALSE  4005  'to 4005'

 L. 626      3987  LOAD_FAST                'optsui'
             3990  LOAD_ATTR                get
             3993  LOAD_STR                 '--id'
             3996  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3999  STORE_FAST               'pid'
             4002  JUMP_FORWARD       4005  'to 4005'
           4005_0  COME_FROM          4002  '4002'

 L. 628      4005  LOAD_GLOBAL              verbose
             4008  POP_JUMP_IF_FALSE  4168  'to 4168'

 L. 629      4011  LOAD_GLOBAL              print
             4014  LOAD_STR                 'Loading {} ...'
             4017  LOAD_ATTR                format
             4020  LOAD_FAST                'pid'
             4023  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4026  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4029  POP_TOP          

 L. 630      4030  LOAD_GLOBAL              diaspy
             4033  LOAD_ATTR                models
             4036  LOAD_ATTR                Post
             4039  LOAD_FAST                'connection'
             4042  LOAD_FAST                'pid'
             4045  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4048  STORE_FAST               'post'

 L. 632      4051  LOAD_GLOBAL              len
             4054  LOAD_FAST                'post'
             4057  LOAD_STR                 'guid'
             4060  BINARY_SUBSCR    
             4061  LOAD_ATTR                replace
             4064  LOAD_STR                 "'"
             4067  LOAD_STR                 ''
             4070  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4073  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4076  LOAD_CONST               2
             4079  COMPARE_OP               >
             4082  POP_JUMP_IF_FALSE  4110  'to 4110'

 L. 633      4085  LOAD_FAST                'post'
             4088  LOAD_STR                 'guid'
             4091  BINARY_SUBSCR    
             4092  LOAD_ATTR                replace
             4095  LOAD_STR                 "'"
             4098  LOAD_STR                 ''
             4101  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4104  STORE_FAST               'pid'
             4107  JUMP_FORWARD       4120  'to 4120'
             4110  ELSE                     '4120'

 L. 634      4110  LOAD_FAST                'post'
             4113  LOAD_STR                 'id'
             4116  BINARY_SUBSCR    
             4117  STORE_FAST               'pid'
           4120_0  COME_FROM          4107  '4107'

 L. 635      4120  LOAD_STR                 '** {0} ({1}):\n\n{2}\n\n** post url: {3}/posts/{4}'
             4123  LOAD_ATTR                format
             4126  LOAD_FAST                'post'
             4129  LOAD_ATTR                author
             4132  LOAD_STR                 'diaspora_id'
             4135  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4138  LOAD_FAST                'post'
             4141  LOAD_ATTR                author
             4144  LOAD_STR                 'guid'
             4147  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4150  LOAD_FAST                'post'
             4153  LOAD_GLOBAL              schemed
             4156  LOAD_FAST                'pid'
             4159  CALL_FUNCTION_5       5  '5 positional, 0 named'
             4162  STORE_FAST               'output'
             4165  JUMP_FORWARD       4216  'to 4216'
             4168  ELSE                     '4216'

 L. 637      4168  LOAD_GLOBAL              diaspy
             4171  LOAD_ATTR                models
             4174  LOAD_ATTR                Post
             4177  LOAD_FAST                'connection'
             4180  LOAD_FAST                'pid'
             4183  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4186  STORE_FAST               'post'

 L. 639      4189  LOAD_STR                 '** {0}:\n\n{1}'
             4192  LOAD_ATTR                format
             4195  LOAD_FAST                'post'
             4198  LOAD_ATTR                author
             4201  LOAD_STR                 'name'
             4204  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4207  LOAD_FAST                'post'
             4210  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4213  STORE_FAST               'output'
           4216_0  COME_FROM          4165  '4165'

 L. 640      4216  LOAD_GLOBAL              print
             4219  LOAD_FAST                'output'
             4222  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4225  POP_TOP          

 L. 641      4226  LOAD_STR                 '--also-comments'
             4229  LOAD_FAST                'optsui'
             4232  COMPARE_OP               in
             4235  POP_JUMP_IF_FALSE  4314  'to 4314'
             4238  LOAD_GLOBAL              len
             4241  LOAD_FAST                'post'
             4244  LOAD_ATTR                comments
             4247  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4250  POP_JUMP_IF_FALSE  4314  'to 4314'

 L. 645      4253  LOAD_GLOBAL              print
             4256  LOAD_STR                 '\n** Comments for this post:\n'
             4259  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4262  POP_TOP          

 L. 646      4263  SETUP_LOOP         4311  'to 4311'
             4266  LOAD_FAST                'post'
             4269  LOAD_ATTR                comments
             4272  GET_ITER         
             4273  FOR_ITER           4307  'to 4307'
             4276  STORE_FAST               'c'

 L. 646      4279  LOAD_GLOBAL              print
             4282  LOAD_STR                 '** {0}\n'
             4285  LOAD_ATTR                format
             4288  LOAD_GLOBAL              repr
             4291  LOAD_FAST                'c'
             4294  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4297  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4300  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4303  POP_TOP          
             4304  JUMP_BACK          4273  'to 4273'
             4307  POP_BLOCK        
           4308_0  COME_FROM_LOOP     4263  '4263'
           4308_1  COME_FROM          4250  '4250'
             4308  JUMP_ABSOLUTE      4314  'to 4314'
             4311  JUMP_FORWARD       4314  'to 4314'
           4314_0  COME_FROM          4311  '4311'

 L. 647      4314  LOAD_STR                 '--reshare'
             4317  LOAD_FAST                'optsui'
             4320  COMPARE_OP               in
             4323  POP_JUMP_IF_FALSE  4423  'to 4423'

 L. 649      4326  LOAD_STR                 '--id'
             4329  LOAD_FAST                'optsui'
             4332  COMPARE_OP               in
             4335  POP_JUMP_IF_FALSE  4356  'to 4356'

 L. 649      4338  LOAD_FAST                'optsui'
             4341  LOAD_ATTR                get
             4344  LOAD_STR                 '--id'
             4347  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4350  STORE_FAST               'pid'
             4353  JUMP_FORWARD       4356  'to 4356'
           4356_0  COME_FROM          4353  '4353'

 L. 650      4356  LOAD_GLOBAL              diaspy
             4359  LOAD_ATTR                models
             4362  LOAD_ATTR                Post
             4365  LOAD_FAST                'connection'
             4368  LOAD_FAST                'pid'
             4371  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4374  STORE_FAST               'post'

 L. 651      4377  LOAD_FAST                'post'
             4380  LOAD_ATTR                reshare
             4383  CALL_FUNCTION_0       0  '0 positional, 0 named'
             4386  POP_TOP          

 L. 652      4387  LOAD_GLOBAL              verbose
             4390  POP_JUMP_IF_FALSE  4423  'to 4423'

 L. 652      4393  LOAD_STR                 "diclipy: You reshared {0}'s post!"
             4396  LOAD_ATTR                format
             4399  LOAD_FAST                'post'
             4402  LOAD_ATTR                author
             4405  LOAD_STR                 'name'
             4408  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4411  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4414  STORE_FAST               'message'
             4417  JUMP_ABSOLUTE      4423  'to 4423'
             4420  JUMP_FORWARD       4423  'to 4423'
           4423_0  COME_FROM          4420  '4420'

 L. 653      4423  LOAD_STR                 '--comment'
             4426  LOAD_FAST                'optsui'
             4429  COMPARE_OP               in
             4432  POP_JUMP_IF_FALSE  4836  'to 4836'

 L. 654      4435  LOAD_STR                 '--image'
             4438  LOAD_FAST                'optsui'
             4441  COMPARE_OP               in
             4444  POP_JUMP_IF_FALSE  4465  'to 4465'

 L. 655      4447  LOAD_FAST                'optsui'
             4450  LOAD_ATTR                get
             4453  LOAD_STR                 '--image'
             4456  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4459  STORE_FAST               'photo'
             4462  JUMP_FORWARD       4471  'to 4471'
             4465  ELSE                     '4471'

 L. 656      4465  LOAD_STR                 ''
             4468  STORE_FAST               'photo'
           4471_0  COME_FROM          4462  '4462'

 L. 657      4471  LOAD_STR                 '{}'
             4474  LOAD_ATTR                format
             4477  LOAD_FAST                'optsui'
             4480  LOAD_ATTR                get
             4483  LOAD_STR                 '--comment'
             4486  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4489  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4492  LOAD_ATTR                replace
             4495  LOAD_STR                 '\\n'
             4498  LOAD_STR                 '\n'
             4501  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4504  STORE_FAST               'text'

 L. 658      4507  LOAD_STR                 '--stdin'
             4510  LOAD_FAST                'optsui'
             4513  COMPARE_OP               in
             4516  POP_JUMP_IF_FALSE  4544  'to 4544'

 L. 659      4519  LOAD_FAST                'text'
             4522  LOAD_STR                 '{}'
             4525  LOAD_ATTR                format
             4528  LOAD_GLOBAL              get_user_input
             4531  CALL_FUNCTION_0       0  '0 positional, 0 named'
             4534  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4537  INPLACE_ADD      
             4538  STORE_FAST               'text'
             4541  JUMP_FORWARD       4623  'to 4623'
             4544  ELSE                     '4623'

 L. 660      4544  LOAD_FAST                'optsui'
             4547  LOAD_ATTR                get
             4550  LOAD_STR                 '--comment'
             4553  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4556  LOAD_STR                 '-'
             4559  COMPARE_OP               ==
             4562  POP_JUMP_IF_FALSE  4623  'to 4623'

 L. 661      4565  LOAD_STR                 '{}'
             4568  LOAD_ATTR                format
             4571  LOAD_GLOBAL              get_user_input
             4574  CALL_FUNCTION_0       0  '0 positional, 0 named'
             4577  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4580  STORE_FAST               'text'

 L. 662      4583  LOAD_STR                 '--stdin'
             4586  LOAD_FAST                'optsui'
             4589  COMPARE_OP               in
             4592  POP_JUMP_IF_FALSE  4623  'to 4623'

 L. 663      4595  LOAD_FAST                'text'
             4598  LOAD_STR                 '{}'
             4601  LOAD_ATTR                format
             4604  LOAD_GLOBAL              get_user_input
             4607  CALL_FUNCTION_0       0  '0 positional, 0 named'
             4610  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4613  INPLACE_ADD      
             4614  STORE_FAST               'text'
             4617  JUMP_ABSOLUTE      4623  'to 4623'
             4620  JUMP_FORWARD       4623  'to 4623'
           4623_0  COME_FROM          4620  '4620'
           4623_1  COME_FROM          4541  '4541'

 L. 665      4623  LOAD_FAST                'text'
             4626  POP_JUMP_IF_TRUE   4635  'to 4635'
             4629  LOAD_FAST                'photo'
           4632_0  COME_FROM          4626  '4626'
             4632  POP_JUMP_IF_FALSE  4827  'to 4827'

 L. 666      4635  LOAD_STR                 '--id'
             4638  LOAD_FAST                'optsui'
             4641  COMPARE_OP               in
             4644  POP_JUMP_IF_FALSE  4665  'to 4665'

 L. 666      4647  LOAD_FAST                'optsui'
             4650  LOAD_ATTR                get
             4653  LOAD_STR                 '--id'
             4656  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4659  STORE_FAST               'pid'
             4662  JUMP_FORWARD       4665  'to 4665'
           4665_0  COME_FROM          4662  '4662'

 L. 667      4665  LOAD_GLOBAL              diaspy
             4668  LOAD_ATTR                models
             4671  LOAD_ATTR                Post
             4674  LOAD_FAST                'connection'
             4677  LOAD_FAST                'pid'
             4680  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4683  STORE_FAST               'post'

 L. 668      4686  LOAD_GLOBAL              verbose
             4689  POP_JUMP_IF_FALSE  4705  'to 4705'

 L. 668      4692  LOAD_GLOBAL              print
             4695  LOAD_STR                 'Commenting ...'
             4698  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4701  POP_TOP          
             4702  JUMP_FORWARD       4705  'to 4705'
           4705_0  COME_FROM          4702  '4702'

 L. 669      4705  LOAD_FAST                'post'
             4708  LOAD_ATTR                comment
             4711  LOAD_FAST                'text'
             4714  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4717  STORE_FAST               'comment'

 L. 670      4720  LOAD_GLOBAL              verbose
             4723  POP_JUMP_IF_FALSE  4802  'to 4802'

 L. 671      4726  LOAD_STR                 "diclipy: You commented on {0}'s post!\n"
             4729  LOAD_ATTR                format
             4732  LOAD_FAST                'post'
             4735  LOAD_ATTR                author
             4738  LOAD_STR                 'name'
             4741  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4744  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4747  STORE_FAST               'message'

 L. 672      4750  LOAD_FAST                'message'
             4753  LOAD_STR                 '** {0} ({1})\n'
             4756  LOAD_ATTR                format
             4759  LOAD_FAST                'post'
             4762  LOAD_ATTR                author
             4765  LOAD_STR                 'diaspora_id'
             4768  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4771  LOAD_FAST                'post'
             4774  LOAD_ATTR                author
             4777  LOAD_STR                 'guid'
             4780  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4783  LOAD_FAST                'post'
             4786  LOAD_GLOBAL              schemed
             4789  LOAD_FAST                'pid'
             4792  CALL_FUNCTION_5       5  '5 positional, 0 named'
             4795  INPLACE_ADD      
             4796  STORE_FAST               'message'
             4799  JUMP_FORWARD       4802  'to 4802'
           4802_0  COME_FROM          4799  '4799'

 L. 673      4802  LOAD_FAST                'message'
             4805  LOAD_STR                 '** post url: {0}/posts/{1}'
             4808  LOAD_ATTR                format
             4811  LOAD_GLOBAL              schemed
             4814  LOAD_FAST                'pid'
             4817  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4820  INPLACE_ADD      
             4821  STORE_FAST               'message'
             4824  JUMP_ABSOLUTE      4836  'to 4836'
             4827  ELSE                     '4833'

 L. 674      4827  LOAD_STR                 'diclipy: fatal: Nothing to send'
             4830  STORE_FAST               'message'
             4833  JUMP_FORWARD       4836  'to 4836'
           4836_0  COME_FROM          4833  '4833'

 L. 675      4836  LOAD_STR                 '--like'
             4839  LOAD_FAST                'optsui'
             4842  COMPARE_OP               in
             4845  POP_JUMP_IF_FALSE  5598  'to 5598'

 L. 677      4848  LOAD_STR                 '--id'
             4851  LOAD_FAST                'optsui'
             4854  COMPARE_OP               in
             4857  POP_JUMP_IF_FALSE  4878  'to 4878'

 L. 677      4860  LOAD_FAST                'optsui'
             4863  LOAD_ATTR                get
             4866  LOAD_STR                 '--id'
             4869  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4872  STORE_FAST               'pid'
             4875  JUMP_FORWARD       4878  'to 4878'
           4878_0  COME_FROM          4875  '4875'

 L. 678      4878  LOAD_GLOBAL              diaspy
             4881  LOAD_ATTR                models
             4884  LOAD_ATTR                Post
             4887  LOAD_FAST                'connection'
             4890  LOAD_FAST                'pid'
             4893  CALL_FUNCTION_2       2  '2 positional, 0 named'
             4896  STORE_FAST               'post'

 L. 679      4899  LOAD_FAST                'post'
             4902  LOAD_ATTR                like
             4905  CALL_FUNCTION_0       0  '0 positional, 0 named'
             4908  POP_TOP          

 L. 680      4909  LOAD_GLOBAL              verbose
             4912  POP_JUMP_IF_FALSE  4945  'to 4945'

 L. 680      4915  LOAD_STR                 "diclipy: You liked {0}'s post!"
             4918  LOAD_ATTR                format
             4921  LOAD_FAST                'post'
             4924  LOAD_ATTR                author
             4927  LOAD_STR                 'name'
             4930  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4933  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4936  STORE_FAST               'message'
             4939  JUMP_ABSOLUTE      4945  'to 4945'
             4942  JUMP_ABSOLUTE      5598  'to 5598'
             4945  JUMP_FORWARD       5598  'to 5598'
             4948  ELSE                     '5598'

 L. 681      4948  LOAD_GLOBAL              str
             4951  LOAD_FAST                'optsui'
             4954  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4957  LOAD_STR                 'notifs'
             4960  COMPARE_OP               ==
             4963  POP_JUMP_IF_FALSE  5577  'to 5577'

 L. 686      4966  LOAD_GLOBAL              str
             4969  LOAD_FAST                'optsui'
             4972  CALL_FUNCTION_1       1  '1 positional, 0 named'
             4975  LOAD_STR                 'notifs'
             4978  COMPARE_OP               ==
             4981  POP_JUMP_IF_FALSE  5598  'to 5598'

 L. 687      4984  BUILD_MAP_0           0  ''
             4987  STORE_FAST               'notifications'

 L. 688      4990  SETUP_FINALLY      5084  'to 5084'
             4993  SETUP_EXCEPT       5018  'to 5018'

 L. 689      4996  LOAD_GLOBAL              diaspy
             4999  LOAD_ATTR                notifications
             5002  LOAD_ATTR                Notifications
             5005  LOAD_FAST                'connection'
             5008  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5011  STORE_FAST               'notifications'
             5014  POP_BLOCK        
             5015  JUMP_FORWARD       5080  'to 5080'
           5018_0  COME_FROM_EXCEPT   4993  '4993'

 L. 690      5018  DUP_TOP          
             5019  LOAD_GLOBAL              Exception
             5022  COMPARE_OP               exception-match
             5025  POP_JUMP_IF_FALSE  5079  'to 5079'
             5028  POP_TOP          
             5029  STORE_FAST               'e'
             5032  POP_TOP          
             5033  SETUP_FINALLY      5066  'to 5066'

 L. 691      5036  LOAD_GLOBAL              print
             5039  LOAD_STR                 '\ndiclipy: notifications: error encountered: {0}'
             5042  LOAD_ATTR                format
             5045  LOAD_FAST                'e'
             5048  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5051  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5054  POP_TOP          

 L. 692      5055  LOAD_FAST                'e'
             5058  RAISE_VARARGS_1       1  'exception'
             5061  POP_BLOCK        
             5062  POP_EXCEPT       
             5063  LOAD_CONST               None
           5066_0  COME_FROM_FINALLY  5033  '5033'
             5066  LOAD_CONST               None
             5069  STORE_FAST               'e'
             5072  DELETE_FAST              'e'
             5075  END_FINALLY      
             5076  JUMP_FORWARD       5080  'to 5080'
             5079  END_FINALLY      
           5080_0  COME_FROM          5076  '5076'
           5080_1  COME_FROM          5015  '5015'
             5080  POP_BLOCK        
             5081  LOAD_CONST               None
           5084_0  COME_FROM_FINALLY  4990  '4990'

 L. 695      5084  LOAD_GLOBAL              debug
             5087  POP_JUMP_IF_FALSE  5142  'to 5142'

 L. 696      5090  LOAD_GLOBAL              print
             5093  LOAD_STR                 'debug: notifications:'
             5096  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5099  POP_TOP          

 L. 697      5100  SETUP_LOOP         5142  'to 5142'
             5103  LOAD_FAST                'notifications'
             5106  GET_ITER         
             5107  FOR_ITER           5138  'to 5138'
             5110  STORE_FAST               'i'

 L. 698      5113  LOAD_FAST                'pprint'
             5116  LOAD_GLOBAL              str
             5119  LOAD_FAST                'i'
             5122  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5125  LOAD_STR                 'indent'
             5128  LOAD_CONST               2
             5131  CALL_FUNCTION_257   257  '1 positional, 1 named'
             5134  POP_TOP          
             5135  JUMP_BACK          5107  'to 5107'
             5138  POP_BLOCK        
           5139_0  COME_FROM_LOOP     5100  '5100'
             5139  JUMP_FORWARD       5142  'to 5142'
           5142_0  COME_FROM          5139  '5139'
             5142  END_FINALLY      

 L. 699      5143  LOAD_STR                 '--page'
             5146  LOAD_FAST                'optsui'
             5149  COMPARE_OP               in
             5152  POP_JUMP_IF_FALSE  5233  'to 5233'

 L. 702      5155  LOAD_FAST                'optsui'
             5158  LOAD_ATTR                get
             5161  LOAD_STR                 '--page'
             5164  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5167  STORE_FAST               'page'

 L. 703      5170  LOAD_STR                 '--per-page'
             5173  LOAD_FAST                'optsui'
             5176  COMPARE_OP               in
             5179  POP_JUMP_IF_FALSE  5200  'to 5200'

 L. 706      5182  LOAD_FAST                'optsui'
             5185  LOAD_ATTR                get
             5188  LOAD_STR                 '--per-page'
             5191  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5194  STORE_FAST               'per_page'
             5197  JUMP_FORWARD       5206  'to 5206'
             5200  ELSE                     '5206'

 L. 709      5200  LOAD_CONST               5
             5203  STORE_FAST               'per_page'
           5206_0  COME_FROM          5197  '5197'

 L. 711      5206  LOAD_FAST                'notifications'
             5209  LOAD_ATTR                get
             5212  LOAD_STR                 'per_page'
             5215  LOAD_FAST                'per_page'
             5218  LOAD_STR                 'page'
             5221  LOAD_FAST                'page'
             5224  CALL_FUNCTION_512   512  '0 positional, 2 named'
             5227  STORE_FAST               'notifs'
             5230  JUMP_FORWARD       5404  'to 5404'
             5233  ELSE                     '5404'

 L. 712      5233  LOAD_STR                 '--last'
             5236  LOAD_FAST                'optsui'
             5239  COMPARE_OP               in
             5242  POP_JUMP_IF_FALSE  5398  'to 5398'

 L. 714      5245  LOAD_STR                 '--per-page'
             5248  LOAD_FAST                'optsui'
             5251  COMPARE_OP               in
             5254  POP_JUMP_IF_FALSE  5338  'to 5338'

 L. 715      5257  LOAD_FAST                'notifications'
             5260  LOAD_ATTR                get
             5263  LOAD_STR                 'per_page'
             5266  LOAD_FAST                'optsui'
             5269  LOAD_ATTR                get
             5272  LOAD_STR                 '--per-page'
             5275  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5278  LOAD_STR                 'page'
             5281  LOAD_CONST               1
             5284  CALL_FUNCTION_512   512  '0 positional, 2 named'
             5287  STORE_FAST               'notifs'

 L. 716      5290  LOAD_GLOBAL              debug
             5293  POP_JUMP_IF_FALSE  5395  'to 5395'

 L. 717      5296  SETUP_LOOP         5335  'to 5335'
             5299  LOAD_FAST                'notifs'
             5302  GET_ITER         
             5303  FOR_ITER           5331  'to 5331'
             5306  STORE_FAST               'i'

 L. 718      5309  LOAD_GLOBAL              print
             5312  LOAD_STR                 'debug: --last --per-page notifs ='
             5315  LOAD_GLOBAL              str
             5318  LOAD_FAST                'i'
             5321  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5324  CALL_FUNCTION_2       2  '2 positional, 0 named'
             5327  POP_TOP          
             5328  JUMP_BACK          5303  'to 5303'
             5331  POP_BLOCK        
           5332_0  COME_FROM_LOOP     5296  '5296'
             5332  JUMP_ABSOLUTE      5395  'to 5395'
             5335  JUMP_ABSOLUTE      5404  'to 5404'
             5338  ELSE                     '5395'

 L. 720      5338  LOAD_FAST                'notifications'
             5341  LOAD_ATTR                last
             5344  CALL_FUNCTION_0       0  '0 positional, 0 named'
             5347  STORE_FAST               'notifs'

 L. 721      5350  LOAD_GLOBAL              debug
             5353  POP_JUMP_IF_FALSE  5404  'to 5404'

 L. 722      5356  SETUP_LOOP         5395  'to 5395'
             5359  LOAD_FAST                'notifs'
             5362  GET_ITER         
             5363  FOR_ITER           5391  'to 5391'
             5366  STORE_FAST               'i'

 L. 723      5369  LOAD_GLOBAL              print
             5372  LOAD_STR                 'debug: --last notifs ='
             5375  LOAD_GLOBAL              str
             5378  LOAD_FAST                'i'
             5381  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5384  CALL_FUNCTION_2       2  '2 positional, 0 named'
             5387  POP_TOP          
             5388  JUMP_BACK          5363  'to 5363'
             5391  POP_BLOCK        
           5392_0  COME_FROM_LOOP     5356  '5356'
             5392  JUMP_ABSOLUTE      5404  'to 5404'
             5395  JUMP_FORWARD       5404  'to 5404'
             5398  ELSE                     '5404'

 L. 726      5398  BUILD_LIST_0          0 
             5401  STORE_FAST               'notifs'
           5404_0  COME_FROM          5395  '5395'
           5404_1  COME_FROM          5230  '5230'

 L. 727      5404  SETUP_LOOP         5574  'to 5574'
             5407  LOAD_FAST                'notifs'
             5410  GET_ITER         
             5411  FOR_ITER           5570  'to 5570'
             5414  STORE_FAST               'n'

 L. 728      5417  LOAD_FAST                'n'
             5420  LOAD_ATTR                unread
             5423  UNARY_NOT        
             5424  POP_JUMP_IF_FALSE  5445  'to 5445'
             5427  LOAD_STR                 '--unread-only'
             5430  LOAD_FAST                'optsui'
             5433  COMPARE_OP               in
             5436  POP_JUMP_IF_FALSE  5445  'to 5445'

 L. 728      5439  CONTINUE           5411  'to 5411'
             5442  JUMP_FORWARD       5445  'to 5445'
           5445_0  COME_FROM          5442  '5442'

 L. 731      5445  LOAD_GLOBAL              str
             5448  LOAD_FAST                'n'
             5451  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5454  STORE_FAST               'text'

 L. 732      5457  LOAD_FAST                'n'
             5460  LOAD_ATTR                about
             5463  CALL_FUNCTION_0       0  '0 positional, 0 named'
             5466  STORE_FAST               'about'

 L. 735      5469  LOAD_GLOBAL              type
             5472  LOAD_FAST                'about'
             5475  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5478  LOAD_GLOBAL              int
             5481  COMPARE_OP               ==
             5484  POP_JUMP_IF_FALSE  5508  'to 5508'

 L. 735      5487  LOAD_STR                 '{0}/posts/{1}'
             5490  LOAD_ATTR                format
             5493  LOAD_GLOBAL              schemed
             5496  LOAD_FAST                'about'
             5499  CALL_FUNCTION_2       2  '2 positional, 0 named'
             5502  STORE_FAST               'about'
             5505  JUMP_FORWARD       5514  'to 5514'
             5508  ELSE                     '5514'

 L. 736      5508  LOAD_STR                 ''
             5511  STORE_FAST               'about'
           5514_0  COME_FROM          5505  '5505'

 L. 737      5514  LOAD_GLOBAL              print
             5517  LOAD_STR                 '** {0} {1}\n'
             5520  LOAD_ATTR                format
             5523  LOAD_FAST                'text'
             5526  LOAD_FAST                'about'
             5529  CALL_FUNCTION_2       2  '2 positional, 0 named'
             5532  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5535  POP_TOP          

 L. 738      5536  LOAD_STR                 '--read'
             5539  LOAD_FAST                'optsui'
             5542  COMPARE_OP               in
             5545  POP_JUMP_IF_FALSE  5411  'to 5411'

 L. 740      5548  LOAD_FAST                'n'
             5551  LOAD_ATTR                mark
             5554  LOAD_STR                 'read'
             5557  LOAD_CONST               True
             5560  CALL_FUNCTION_256   256  '0 positional, 1 named'
             5563  POP_TOP          
             5564  CONTINUE           5411  'to 5411'
             5567  JUMP_BACK          5411  'to 5411'
             5570  POP_BLOCK        
           5571_0  COME_FROM_LOOP     5404  '5404'
             5571  JUMP_ABSOLUTE      5598  'to 5598'
             5574  JUMP_FORWARD       5598  'to 5598'
             5577  ELSE                     '5598'

 L. 743      5577  LOAD_STR                 "diclipy: fatal: '{0}' command not implemented"
             5580  LOAD_ATTR                format
             5583  LOAD_GLOBAL              str
             5586  LOAD_FAST                'optsui'
             5589  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5592  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5595  STORE_FAST               'message'
           5598_0  COME_FROM          5574  '5574'
           5598_1  COME_FROM          4945  '4945'

 L. 744      5598  LOAD_FAST                'message'
             5601  POP_JUMP_IF_FALSE  5673  'to 5673'

 L. 745      5604  LOAD_GLOBAL              print
             5607  LOAD_FAST                'message'
             5610  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5613  POP_TOP          

 L. 746      5614  LOAD_GLOBAL              debug
             5617  POP_JUMP_IF_FALSE  5642  'to 5642'

 L. 746      5620  LOAD_GLOBAL              print
             5623  LOAD_STR                 'debug: options ='
             5626  LOAD_GLOBAL              str
             5629  LOAD_FAST                'options'
             5632  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5635  CALL_FUNCTION_2       2  '2 positional, 0 named'
             5638  POP_TOP          
             5639  JUMP_FORWARD       5642  'to 5642'
           5642_0  COME_FROM          5639  '5639'

 L. 747      5642  LOAD_GLOBAL              debug
             5645  POP_JUMP_IF_FALSE  5673  'to 5673'

 L. 747      5648  LOAD_GLOBAL              print
             5651  LOAD_STR                 'debug: optsui ='
             5654  LOAD_GLOBAL              str
             5657  LOAD_FAST                'optsui'
             5660  CALL_FUNCTION_1       1  '1 positional, 0 named'
             5663  CALL_FUNCTION_2       2  '2 positional, 0 named'
             5666  POP_TOP          
             5667  JUMP_ABSOLUTE      5673  'to 5673'
             5670  JUMP_FORWARD       5673  'to 5673'
           5673_0  COME_FROM          5670  '5670'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 1929


if __name__ == '__main__':
    main()
# global proto ## Warning: Unused global
# global schemed ## Warning: Unused global