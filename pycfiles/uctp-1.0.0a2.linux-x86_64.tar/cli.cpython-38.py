# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/dist-packages/uctp/cli.py
# Compiled at: 2020-04-30 12:36:17
# Size of source mod 2**32: 10484 bytes
import argparse, atexit, cmd, hashlib, json, os, random, readline, sys, textwrap
from typing import Union, Tuple
from Crypto.PublicKey import RSA
from . import __copyright__, __version__
from . import peer

def exit_(msg: str):
    print(msg)
    exit(0)


parser = argparse.ArgumentParser(prog='uctp',
  formatter_class=(argparse.RawDescriptionHelpFormatter),
  description=(textwrap.dedent(f"uctp v{__version__} (Command Line Interface)\n{__copyright__}")))
parser.add_argument('-v', '--version', action='version', version=f"uctp {__version__}")
parser.add_argument('-d', '--debug', action='store_true', help='Debug mode')
commands = parser.add_subparsers(title='commands', dest='command')
connect = commands.add_parser('connect', help='Connect to peer and open shell')
connect.add_argument('ip', help='ip of remote peer')
connect.add_argument('-n', '--name', type=str, help='Name for peer')
connect.add_argument('-p', '--port', nargs='?', default=2604, type=int, help='port of remote peer')
connect.add_argument('-k', '--key', nargs='?', type=argparse.FileType('r', encoding='utf8'), help='File with private RSA key. If not specified, key will be generated')
key = commands.add_parser('key', help='Key generator and validator')
key.add_argument('file', type=str, help='Path to file that stores RSA key')
key.add_argument('-c', '--check', action='store_true', help='Check key')
key.add_argument('-g', '--gen', nargs='?', const=4096, type=int, help='Generate new key to file with specified length (in bits)',
  metavar='LENGTH')

class Shell(cmd.Cmd):
    _key: RSA.RsaKey
    _peer: peer.Peer
    _history = os.path.expanduser('~/.uctp-cli-history')
    _history: str

    def __init__(self, name, key_, ip, port):
        self._peer = peer.Peer(name, key_, '0.0.0.0', 0, max_connections=0)
        self._peer.run()
        self._peer.connect(ip, port)
        readline.set_history_length(100)
        self.prompt = '> '
        self.doc_header = 'Documented commands (type "help <command>" to see help):'
        self.nohelp = '- No help for this command "%s"'
        super().__init__()

    def connected--- This code section failed: ---

 L.  69         0  SETUP_FINALLY        24  'to 24'

 L.  70         2  LOAD_CONST               True
                4  LOAD_GLOBAL              tuple
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _peer
               10  LOAD_ATTR                connections
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  BUILD_TUPLE_2         2 
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.  71        24  DUP_TOP          
               26  LOAD_GLOBAL              IndexError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  72        38  POP_EXCEPT       
               40  LOAD_CONST               (False, None)
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 34

    def check(self):
        if not self.connected()[0]:
            exit_('Connection with remote peer lost')

    def start(self):
        self.load_history()
        while True:
            try:
                remote = self._peer.connections[self.connected()[1]]
                self.cmdloop(f"Peer: {self._peer.name} ({hashlib.sha1(self._peer.key.publickey().export_key('DER')).hexdigest().upper()})\nRemote peer: {remote.name} ({hashlib.sha1(remote.key.export_key('DER')).hexdigest().upper()})")
                break
            except KeyboardInterrupt:
                readline.set_auto_history(False)
                prompt = input('\nYou really want to exit? (y/n): ').lower()
                if prompt == 'y':
                    break
                else:
                    readline.set_auto_history(True)

    @classmethod
    def load_history(cls):
        if not os.path.isfile(cls._history):
            open(cls._history, 'x')
        readline.read_history_file(cls._history)

    @classmethod
    def save_history(cls):
        if not os.path.isfile(cls._history):
            open(cls._history, 'x')
        readline.write_history_file(cls._history)

    def precmd--- This code section failed: ---

 L. 109         0  LOAD_FAST                'self'
                2  LOAD_METHOD              check
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 110         8  LOAD_CONST               None
               10  SETUP_FINALLY        74  'to 74'

 L. 111        12  LOAD_FAST                'line'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  LOAD_STR                 '/'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    42  'to 42'

 L. 112        24  LOAD_STR                 'send '
               26  LOAD_FAST                'line'
               28  LOAD_CONST               1
               30  LOAD_CONST               None
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  BINARY_ADD       
               38  STORE_FAST               'line'
               40  JUMP_FORWARD         70  'to 70'
             42_0  COME_FROM            22  '22'

 L. 113        42  LOAD_FAST                'line'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_STR                 '!'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    70  'to 70'

 L. 114        54  LOAD_STR                 'fsend '
               56  LOAD_FAST                'line'
               58  LOAD_CONST               1
               60  LOAD_CONST               None
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  BINARY_ADD       
               68  STORE_FAST               'line'
             70_0  COME_FROM            52  '52'
             70_1  COME_FROM            40  '40'
               70  POP_BLOCK        
               72  BEGIN_FINALLY    
             74_0  COME_FROM_FINALLY    10  '10'

 L. 116        74  LOAD_FAST                'line'
               76  POP_FINALLY           1  ''
               78  ROT_TWO          
               80  POP_TOP          
               82  RETURN_VALUE     
               84  END_FINALLY      
               86  POP_TOP          

Parse error at or near `LOAD_FAST' instruction at offset 74

    def default(self, line: str):
        self.stdout.write(f'Unknown command "{line}"\nTry "help" to see all commands\n')

    @staticmethod
    def do_clear(args: str):
        """
        Clear screen
        """
        os.system('clear')

    def do_send(self, line: str):
        """
        Send command to remote peer
        Syntax: send <command> [args]
        * Instead of "send" you can use "/"
        """
        command = line.split(' ')[0]
        args = []
        buffer = []
        try:
            for i in line.split(' ')[1:]:
                if buffer:
                    if i.endswith(("'", '"')):
                        buffer.append(i[:-1])
                        args.append(json.loads(''.join(buffer)))
                        buffer.clear()
                    else:
                        buffer.append(i)
                elif i.startswith(("'", '"')):
                    if i.endswith(("'", '"')):
                        args.append(json.loads(i[1:-1]))
                    else:
                        buffer.append(i[1:])
                else:
                    args.append(i)
            else:
                try:
                    print(f"\n{self._peer.send(self.connected()[1], command, args)[1]}\n")
                except Exception as e:
                    try:
                        print(f"{e.__class__.__name__}: {e.__str__()}")
                    finally:
                        e = None
                        del e

        except json.JSONDecodeError as e:
            try:
                print('Error while parsing arguments')
                raise e
            finally:
                e = None
                del e

    def do_fsend(self, line: str):
        """
        Send command to remote peer
        Syntax: send <command> string
        * string will be parsed as JSON (if string will be dict, it will be sent as kwargs)
        """
        command, sep, string = line.partition(' ')
        try:
            string = json.loads(string)
            if isinstance(string, dict):
                result = self._peer.send((self.connected()[1]), command, kwargs=string)[1]
            else:
                if isinstance(string, list):
                    result = self._peer.send(self.connected()[1], command, string)[1]
                else:
                    result = self._peer.send(self.connected()[1], command, (string,))[1]
            print(f"\n{result}\n")
        except json.JSONDecodeError:
            print('Error while parsing (JSON)')
        except Exception as e:
            try:
                print(f"{e.__class__.__name__}: {e.__str__()}")
            finally:
                e = None
                del e

    @staticmethod
    def do_exit(args: str):
        """
        Close connection with remote peer and exit
        """
        return True


def main--- This code section failed: ---

 L. 196         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                platform
                4  LOAD_STR                 'linux'
                6  COMPARE_OP               ==
             8_10  POP_JUMP_IF_FALSE   864  'to 864'

 L. 197        12  LOAD_GLOBAL              atexit
               14  LOAD_METHOD              register
               16  LOAD_LAMBDA              '<code_object <lambda>>'
               18  LOAD_STR                 'main.<locals>.<lambda>'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L. 199        26  LOAD_GLOBAL              parser
               28  LOAD_METHOD              parse_args
               30  LOAD_GLOBAL              sys
               32  LOAD_ATTR                argv
               34  LOAD_CONST               1
               36  LOAD_CONST               None
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'args'

 L. 200        46  LOAD_STR                 'command'
               48  LOAD_FAST                'args'
               50  COMPARE_OP               in
            52_54  POP_JUMP_IF_FALSE   854  'to 854'

 L. 201        56  LOAD_FAST                'args'
               58  LOAD_ATTR                command
               60  LOAD_STR                 'connect'
               62  COMPARE_OP               ==
            64_66  POP_JUMP_IF_FALSE   278  'to 278'

 L. 202        68  SETUP_FINALLY       108  'to 108'

 L. 203        70  LOAD_FAST                'args'
               72  LOAD_ATTR                key
               74  POP_JUMP_IF_FALSE    94  'to 94'

 L. 204        76  LOAD_GLOBAL              RSA
               78  LOAD_METHOD              import_key
               80  LOAD_FAST                'args'
               82  LOAD_ATTR                key
               84  LOAD_METHOD              read
               86  CALL_METHOD_0         0  ''
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'key_'
               92  JUMP_FORWARD        104  'to 104'
             94_0  COME_FROM            74  '74'

 L. 206        94  LOAD_GLOBAL              RSA
               96  LOAD_METHOD              generate
               98  LOAD_CONST               2048
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'key_'
            104_0  COME_FROM            92  '92'
              104  POP_BLOCK        
              106  JUMP_FORWARD        136  'to 136'
            108_0  COME_FROM_FINALLY    68  '68'

 L. 207       108  DUP_TOP          
              110  LOAD_GLOBAL              ValueError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   134  'to 134'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 208       122  LOAD_GLOBAL              exit_
              124  LOAD_STR                 'File has no valid RSA'
              126  CALL_FUNCTION_1       1  ''
              128  POP_TOP          
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM           114  '114'
              134  END_FINALLY      
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM           106  '106'

 L. 209       136  SETUP_FINALLY       200  'to 200'

 L. 210       138  LOAD_FAST                'args'
              140  LOAD_ATTR                name
              142  POP_JUMP_IF_FALSE   150  'to 150'
              144  LOAD_FAST                'args'
              146  LOAD_ATTR                name
              148  JUMP_FORWARD        166  'to 166'
            150_0  COME_FROM           142  '142'
              150  LOAD_STR                 'uctp-cli-'
              152  LOAD_GLOBAL              random
              154  LOAD_METHOD              randint
              156  LOAD_CONST               1000
              158  LOAD_CONST               9999
              160  CALL_METHOD_2         2  ''
              162  FORMAT_VALUE          0  ''
              164  BUILD_STRING_2        2 
            166_0  COME_FROM           148  '148'
              166  STORE_FAST               'name'

 L. 211       168  LOAD_GLOBAL              Shell

 L. 212       170  LOAD_FAST                'name'

 L. 213       172  LOAD_FAST                'key_'

 L. 214       174  LOAD_FAST                'args'
              176  LOAD_ATTR                ip

 L. 215       178  LOAD_FAST                'args'
              180  LOAD_ATTR                port

 L. 211       182  CALL_FUNCTION_4       4  ''
              184  LOAD_METHOD              start
              186  CALL_METHOD_0         0  ''
              188  POP_TOP          

 L. 217       190  LOAD_GLOBAL              exit
              192  CALL_FUNCTION_0       0  ''
              194  POP_TOP          
              196  POP_BLOCK        
              198  JUMP_FORWARD        854  'to 854'
            200_0  COME_FROM_FINALLY   136  '136'

 L. 218       200  DUP_TOP          
              202  LOAD_GLOBAL              Exception
              204  COMPARE_OP               exception-match
          206_208  POP_JUMP_IF_FALSE   272  'to 272'
              210  POP_TOP          
              212  STORE_FAST               'e'
              214  POP_TOP          
              216  SETUP_FINALLY       260  'to 260'

 L. 219       218  LOAD_FAST                'args'
              220  LOAD_ATTR                debug
              222  POP_JUMP_IF_FALSE   230  'to 230'

 L. 220       224  LOAD_FAST                'e'
              226  RAISE_VARARGS_1       1  'exception instance'
              228  JUMP_FORWARD        256  'to 256'
            230_0  COME_FROM           222  '222'

 L. 222       230  LOAD_GLOBAL              exit_
              232  LOAD_FAST                'e'
              234  LOAD_ATTR                __class__
              236  LOAD_ATTR                __name__
              238  FORMAT_VALUE          0  ''
              240  LOAD_STR                 ': '
              242  LOAD_FAST                'e'
              244  LOAD_METHOD              __str__
              246  CALL_METHOD_0         0  ''
              248  FORMAT_VALUE          0  ''
              250  BUILD_STRING_3        3 
              252  CALL_FUNCTION_1       1  ''
              254  POP_TOP          
            256_0  COME_FROM           228  '228'
              256  POP_BLOCK        
              258  BEGIN_FINALLY    
            260_0  COME_FROM_FINALLY   216  '216'
              260  LOAD_CONST               None
              262  STORE_FAST               'e'
              264  DELETE_FAST              'e'
              266  END_FINALLY      
              268  POP_EXCEPT       
              270  JUMP_FORWARD        854  'to 854'
            272_0  COME_FROM           206  '206'
              272  END_FINALLY      
          274_276  JUMP_FORWARD        854  'to 854'
            278_0  COME_FROM            64  '64'

 L. 223       278  LOAD_FAST                'args'
              280  LOAD_ATTR                command
              282  LOAD_STR                 'key'
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   854  'to 854'

 L. 224       290  LOAD_FAST                'args'
              292  LOAD_ATTR                gen
          294_296  POP_JUMP_IF_FALSE   632  'to 632'

 L. 225       298  LOAD_FAST                'args'
              300  LOAD_ATTR                gen
              302  LOAD_CONST               1024
              304  COMPARE_OP               <
          306_308  POP_JUMP_IF_FALSE   322  'to 322'

 L. 226       310  LOAD_GLOBAL              exit_
              312  LOAD_STR                 "Key length can't be less than 1024 bits"
              314  CALL_FUNCTION_1       1  ''
              316  POP_TOP          
          318_320  JUMP_ABSOLUTE       854  'to 854'
            322_0  COME_FROM           306  '306'

 L. 228       322  SETUP_FINALLY       572  'to 572'

 L. 229       324  LOAD_GLOBAL              os
              326  LOAD_ATTR                path
              328  LOAD_METHOD              isfile
              330  LOAD_FAST                'args'
              332  LOAD_ATTR                file
              334  CALL_METHOD_1         1  ''
          336_338  POP_JUMP_IF_FALSE   432  'to 432'

 L. 230       340  LOAD_GLOBAL              range
              342  LOAD_CONST               3
              344  CALL_FUNCTION_1       1  ''
              346  GET_ITER         
              348  FOR_ITER            428  'to 428'
              350  STORE_FAST               'i'

 L. 231       352  LOAD_GLOBAL              input
              354  LOAD_STR                 'File "'
              356  LOAD_GLOBAL              os
              358  LOAD_ATTR                path
              360  LOAD_METHOD              abspath
              362  LOAD_FAST                'args'
              364  LOAD_ATTR                file
              366  CALL_METHOD_1         1  ''
              368  FORMAT_VALUE          0  ''
              370  LOAD_STR                 '" already exists. Overwrite (y/n): '
              372  BUILD_STRING_3        3 
              374  CALL_FUNCTION_1       1  ''
              376  LOAD_METHOD              lower
              378  CALL_METHOD_0         0  ''
              380  STORE_FAST               'prompt'

 L. 233       382  LOAD_FAST                'prompt'
              384  LOAD_STR                 'y'
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   400  'to 400'

 L. 234       392  POP_TOP          
          394_396  BREAK_LOOP          432  'to 432'
              398  JUMP_BACK           348  'to 348'
            400_0  COME_FROM           388  '388'

 L. 235       400  LOAD_FAST                'prompt'
              402  LOAD_STR                 'n'
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   416  'to 416'

 L. 236       410  LOAD_GLOBAL              KeyboardInterrupt
              412  RAISE_VARARGS_1       1  'exception instance'
              414  JUMP_BACK           348  'to 348'
            416_0  COME_FROM           406  '406'

 L. 238       416  LOAD_GLOBAL              print
              418  LOAD_STR                 'Y or N. Try again...'
              420  CALL_FUNCTION_1       1  ''
              422  POP_TOP          
          424_426  JUMP_BACK           348  'to 348'

 L. 240       428  LOAD_GLOBAL              KeyboardInterrupt
              430  RAISE_VARARGS_1       1  'exception instance'
            432_0  COME_FROM           336  '336'

 L. 241       432  LOAD_GLOBAL              open
              434  LOAD_FAST                'args'
              436  LOAD_ATTR                file
              438  LOAD_STR                 'wb+'
              440  CALL_FUNCTION_2       2  ''
              442  SETUP_WITH          562  'to 562'
              444  STORE_FAST               'f'

 L. 242       446  LOAD_GLOBAL              print
              448  LOAD_STR                 'Generating '
              450  LOAD_FAST                'args'
              452  LOAD_ATTR                gen
              454  FORMAT_VALUE          0  ''
              456  LOAD_STR                 '-bit RSA key'
              458  BUILD_STRING_3        3 
              460  CALL_FUNCTION_1       1  ''
              462  POP_TOP          

 L. 243       464  LOAD_GLOBAL              RSA
              466  LOAD_METHOD              generate
              468  LOAD_FAST                'args'
              470  LOAD_ATTR                gen
              472  CALL_METHOD_1         1  ''
              474  STORE_FAST               'key_'

 L. 244       476  LOAD_FAST                'f'
              478  LOAD_METHOD              write
              480  LOAD_FAST                'key_'
              482  LOAD_METHOD              export_key
              484  CALL_METHOD_0         0  ''
              486  CALL_METHOD_1         1  ''
              488  POP_TOP          

 L. 245       490  LOAD_GLOBAL              print
              492  LOAD_STR                 'Generating complete'
              494  CALL_FUNCTION_1       1  ''
              496  POP_TOP          

 L. 246       498  LOAD_GLOBAL              exit_
              500  LOAD_STR                 'Key fingerprint:\n\tSHA1: '
              502  LOAD_GLOBAL              hashlib
              504  LOAD_METHOD              sha1
              506  LOAD_FAST                'key_'
              508  LOAD_METHOD              publickey
              510  CALL_METHOD_0         0  ''
              512  LOAD_METHOD              export_key
              514  LOAD_STR                 'DER'
              516  CALL_METHOD_1         1  ''
              518  CALL_METHOD_1         1  ''
              520  LOAD_METHOD              hexdigest
              522  CALL_METHOD_0         0  ''
              524  FORMAT_VALUE          0  ''
              526  LOAD_STR                 '\n\tSHA256: '
              528  LOAD_GLOBAL              hashlib
              530  LOAD_METHOD              sha256
              532  LOAD_FAST                'key_'
              534  LOAD_METHOD              publickey
              536  CALL_METHOD_0         0  ''
              538  LOAD_METHOD              export_key
              540  LOAD_STR                 'DER'
              542  CALL_METHOD_1         1  ''
              544  CALL_METHOD_1         1  ''
              546  LOAD_METHOD              hexdigest
              548  CALL_METHOD_0         0  ''
              550  FORMAT_VALUE          0  ''
              552  BUILD_STRING_4        4 
              554  CALL_FUNCTION_1       1  ''
              556  POP_TOP          
              558  POP_BLOCK        
              560  BEGIN_FINALLY    
            562_0  COME_FROM_WITH      442  '442'
              562  WITH_CLEANUP_START
              564  WITH_CLEANUP_FINISH
              566  END_FINALLY      
              568  POP_BLOCK        
              570  JUMP_FORWARD        630  'to 630'
            572_0  COME_FROM_FINALLY   322  '322'

 L. 250       572  DUP_TOP          
              574  LOAD_GLOBAL              OSError
              576  COMPARE_OP               exception-match
          578_580  POP_JUMP_IF_FALSE   600  'to 600'
              582  POP_TOP          
              584  POP_TOP          
              586  POP_TOP          

 L. 251       588  LOAD_GLOBAL              exit_
              590  LOAD_STR                 'Wrong file path'
              592  CALL_FUNCTION_1       1  ''
              594  POP_TOP          
              596  POP_EXCEPT       
              598  JUMP_FORWARD        630  'to 630'
            600_0  COME_FROM           578  '578'

 L. 252       600  DUP_TOP          
              602  LOAD_GLOBAL              KeyboardInterrupt
              604  COMPARE_OP               exception-match
          606_608  POP_JUMP_IF_FALSE   628  'to 628'
              610  POP_TOP          
              612  POP_TOP          
              614  POP_TOP          

 L. 253       616  LOAD_GLOBAL              exit_
              618  LOAD_STR                 'Generation canceled'
              620  CALL_FUNCTION_1       1  ''
              622  POP_TOP          
              624  POP_EXCEPT       
              626  JUMP_FORWARD        630  'to 630'
            628_0  COME_FROM           606  '606'
              628  END_FINALLY      
            630_0  COME_FROM           626  '626'
            630_1  COME_FROM           598  '598'
            630_2  COME_FROM           570  '570'
              630  JUMP_FORWARD        854  'to 854'
            632_0  COME_FROM           294  '294'

 L. 254       632  LOAD_FAST                'args'
              634  LOAD_ATTR                check
          636_638  POP_JUMP_IF_FALSE   846  'to 846'

 L. 255       640  LOAD_GLOBAL              os
              642  LOAD_ATTR                path
              644  LOAD_METHOD              isfile
              646  LOAD_FAST                'args'
              648  LOAD_ATTR                file
              650  CALL_METHOD_1         1  ''
          652_654  POP_JUMP_IF_FALSE   836  'to 836'

 L. 256       656  SETUP_FINALLY       684  'to 684'

 L. 257       658  LOAD_GLOBAL              RSA
              660  LOAD_METHOD              import_key
              662  LOAD_GLOBAL              open
              664  LOAD_FAST                'args'
              666  LOAD_ATTR                file
              668  LOAD_STR                 'r'
              670  CALL_FUNCTION_2       2  ''
              672  LOAD_METHOD              read
              674  CALL_METHOD_0         0  ''
              676  CALL_METHOD_1         1  ''
              678  STORE_FAST               'key_'
              680  POP_BLOCK        
              682  JUMP_FORWARD        714  'to 714'
            684_0  COME_FROM_FINALLY   656  '656'

 L. 258       684  DUP_TOP          
              686  LOAD_GLOBAL              ValueError
              688  COMPARE_OP               exception-match
          690_692  POP_JUMP_IF_FALSE   712  'to 712'
              694  POP_TOP          
              696  POP_TOP          
              698  POP_TOP          

 L. 259       700  LOAD_GLOBAL              exit_
              702  LOAD_STR                 'File has no RSA key'
              704  CALL_FUNCTION_1       1  ''
              706  POP_TOP          
              708  POP_EXCEPT       
              710  JUMP_FORWARD        714  'to 714'
            712_0  COME_FROM           690  '690'
              712  END_FINALLY      
            714_0  COME_FROM           710  '710'
            714_1  COME_FROM           682  '682'

 L. 260       714  LOAD_GLOBAL              exit_
              716  LOAD_STR                 'RSA key type: '
              718  LOAD_FAST                'key_'
              720  LOAD_METHOD              has_private
              722  CALL_METHOD_0         0  ''
          724_726  POP_JUMP_IF_FALSE   732  'to 732'
              728  LOAD_STR                 'Public'
              730  JUMP_FORWARD        734  'to 734'
            732_0  COME_FROM           724  '724'
              732  LOAD_STR                 'Private'
            734_0  COME_FROM           730  '730'
              734  FORMAT_VALUE          0  ''
              736  LOAD_STR                 '\nRSA length: '
              738  LOAD_FAST                'key_'
              740  LOAD_METHOD              size_in_bits
              742  CALL_METHOD_0         0  ''
              744  FORMAT_VALUE          0  ''
              746  LOAD_STR                 '-bits ('
              748  LOAD_FAST                'key_'
              750  LOAD_METHOD              size_in_bytes
              752  CALL_METHOD_0         0  ''
              754  FORMAT_VALUE          0  ''
              756  LOAD_STR                 '-bytes)\nKey fingerprint:\n\tSHA1: '
              758  LOAD_GLOBAL              hashlib
              760  LOAD_METHOD              sha1
              762  LOAD_FAST                'key_'
              764  LOAD_METHOD              publickey
              766  CALL_METHOD_0         0  ''
              768  LOAD_METHOD              export_key
              770  LOAD_STR                 'DER'
              772  CALL_METHOD_1         1  ''
              774  CALL_METHOD_1         1  ''
            776_0  COME_FROM           198  '198'
              776  LOAD_METHOD              hexdigest
              778  CALL_METHOD_0         0  ''
              780  FORMAT_VALUE          0  ''
              782  LOAD_STR                 '\n\tSHA256: '
              784  LOAD_GLOBAL              hashlib
              786  LOAD_METHOD              sha256
              788  LOAD_FAST                'key_'
              790  LOAD_METHOD              publickey
              792  CALL_METHOD_0         0  ''
              794  LOAD_METHOD              export_key
              796  LOAD_STR                 'DER'
              798  CALL_METHOD_1         1  ''
              800  CALL_METHOD_1         1  ''
              802  LOAD_METHOD              hexdigest
              804  CALL_METHOD_0         0  ''
              806  FORMAT_VALUE          0  ''
              808  LOAD_STR                 '\nCan be used for uctp: '
              810  LOAD_FAST                'key_'
              812  LOAD_METHOD              has_private
              814  CALL_METHOD_0         0  ''
          816_818  POP_JUMP_IF_FALSE   824  'to 824'
              820  LOAD_STR                 'Yes'
              822  JUMP_FORWARD        826  'to 826'
            824_0  COME_FROM           816  '816'
              824  LOAD_STR                 'No'
            826_0  COME_FROM           822  '822'
              826  FORMAT_VALUE          0  ''
              828  BUILD_STRING_12      12 
              830  CALL_FUNCTION_1       1  ''
              832  POP_TOP          
              834  JUMP_FORWARD        844  'to 844'
            836_0  COME_FROM           652  '652'

 L. 267       836  LOAD_GLOBAL              exit_
              838  LOAD_STR                 "File doesn't exist"
              840  CALL_FUNCTION_1       1  ''
              842  POP_TOP          
            844_0  COME_FROM           834  '834'
              844  JUMP_FORWARD        854  'to 854'
            846_0  COME_FROM           636  '636'

 L. 269       846  LOAD_GLOBAL              key
            848_0  COME_FROM           270  '270'
              848  LOAD_METHOD              print_usage
              850  CALL_METHOD_0         0  ''
              852  POP_TOP          
            854_0  COME_FROM           844  '844'
            854_1  COME_FROM           630  '630'
            854_2  COME_FROM           286  '286'
            854_3  COME_FROM           274  '274'
            854_4  COME_FROM            52  '52'

 L. 270       854  LOAD_GLOBAL              parser
              856  LOAD_METHOD              print_usage
              858  CALL_METHOD_0         0  ''
              860  POP_TOP          
              862  JUMP_FORWARD        872  'to 872'
            864_0  COME_FROM             8  '8'

 L. 272       864  LOAD_GLOBAL              print
              866  LOAD_STR                 'uctp-cli supports only linux'
              868  CALL_FUNCTION_1       1  ''
              870  POP_TOP          
            872_0  COME_FROM           862  '862'

Parse error at or near `COME_FROM' instruction at offset 776_0