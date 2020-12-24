# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/dist-packages/uctp/cli.py
# Compiled at: 2020-05-12 13:39:36
# Size of source mod 2**32: 12949 bytes
import argparse, atexit, cmd, hashlib, json, os, random, readline, sys, textwrap
from datetime import datetime
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
connect.add_argument('-p', '--port', nargs='?', default=2604, type=int, help='Port of remote peer')
connect.add_argument('-k', '--key', nargs='?', type=argparse.FileType('r', encoding='utf8'), help='File with private RSA key. If not specified, key will be generated')
connect.add_argument('-r', '--raw', action='store_true', help='Print raw data of response')
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
    raw: bool

    def __init__(self, name, key_, ip, port, raw_output=False):
        self._peer = peer.Peer(name, key_, '0.0.0.0', 0, max_connections=0)
        self._peer.run()
        self._peer.connect(ip, port)
        self.raw = raw_output
        readline.set_history_length(100)
        self.prompt = '> '
        self.doc_header = 'Documented commands (type "help <command>" to see help):'
        self.nohelp = '- No help for this command "%s"'
        super().__init__()

    def _print(self, command: str, result) -> None:
        output = ''
        if (self.raw or command) == '_commands':
            commands_ = []
            for k, v in result.items():
                commands_.append('{0}({1}) -> {2}'.format(k, ', '.join([f"{i[0]}{: {i[1]} if i[1] != 'None' else ''}{ = {i[2]} if i[2] is not None else ''}" for i in v['args']] + (['*'] if v['kwargs'] else []) + [f"{i[0]}{: {i[1]} if i[1] != 'None' else ''}{ = {i[2]} if i[2] is not None else ''}" for i in v['kwargs']] + ([f"*{v['varargs']}"] if v['varargs'] else []) + ([f"**{v['varkw']}"] if v['varkw'] else [])), v['returns']))
            else:
                output = '\n'.join(commands_)

        else:
            if command == '_me':
                output = f"Name: {result['name']}\nAddress: {result['ip']}:{result['port']}\nConnected: {datetime.utcfromtimestamp(result['timestamp']).isoformat()}\nKey (SHA1): {result['key']}\nSession: {result['session']}"
            else:
                if command == '_peers':
                    output = '\n'.join([f"{i['name']} Key (SHA1): {i['key']}, Session: {i['session']}\n{'':>{len(i['name'])}} Address: {i['ip']}:{i['port']}, Connected: {datetime.utcfromtimestamp(i['timestamp']).isoformat()}{' (client)' if i['client'] else ''}" for i in result])
                else:
                    if command == '_trusted':
                        output = ', '.join(result)
                    else:
                        if command == '_aliases':
                            output = '\n'.join([f"{v}: {k}" for k, v in result.items()])
                        print(f"\n{output if output else result}\n")

    def connected--- This code section failed: ---

 L. 111         0  SETUP_FINALLY        24  'to 24'

 L. 112         2  LOAD_CONST               True
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

 L. 113        24  DUP_TOP          
               26  LOAD_GLOBAL              IndexError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 114        38  POP_EXCEPT       
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

 L. 151         0  LOAD_FAST                'self'
                2  LOAD_METHOD              check
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 152         8  LOAD_CONST               None
               10  SETUP_FINALLY        74  'to 74'

 L. 153        12  LOAD_FAST                'line'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  LOAD_STR                 '/'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    42  'to 42'

 L. 154        24  LOAD_STR                 'send '
               26  LOAD_FAST                'line'
               28  LOAD_CONST               1
               30  LOAD_CONST               None
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  BINARY_ADD       
               38  STORE_FAST               'line'
               40  JUMP_FORWARD         70  'to 70'
             42_0  COME_FROM            22  '22'

 L. 155        42  LOAD_FAST                'line'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_STR                 '!'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    70  'to 70'

 L. 156        54  LOAD_STR                 'fsend '
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

 L. 158        74  LOAD_FAST                'line'
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
                    status, result = self._peer.send(self.connected()[1], command, args)
                    if status == 1:
                        self._print(command, result)
                    else:
                        print(f"\n{result}\n")
                except Exception as e:
                    try:
                        print(f"\n{e.__class__.__name__}: {e.__str__()}\n")
                    finally:
                        e = None
                        del e

        except json.JSONDecodeError:
            print('Error while parsing arguments')

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
                status, result = self._peer.send((self.connected()[1]), command, kwargs=string)
            else:
                if isinstance(string, list):
                    status, result = self._peer.send(self.connected()[1], command, string)
                else:
                    status, result = self._peer.send(self.connected()[1], command, (string,))
            if status == 1:
                self._print(command, result)
            else:
                print(f"\n{result}\n")
        except json.JSONDecodeError:
            print('Error while parsing (JSON)')
        except Exception as e:
            try:
                print(f"\n{e.__class__.__name__}: {e.__str__()}\n")
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

 L. 245         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                platform
                4  LOAD_STR                 'linux'
                6  COMPARE_OP               ==
             8_10  POP_JUMP_IF_FALSE   868  'to 868'

 L. 246        12  LOAD_GLOBAL              atexit
               14  LOAD_METHOD              register
               16  LOAD_LAMBDA              '<code_object <lambda>>'
               18  LOAD_STR                 'main.<locals>.<lambda>'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L. 248        26  LOAD_GLOBAL              parser
               28  LOAD_METHOD              parse_args
               30  LOAD_GLOBAL              sys
               32  LOAD_ATTR                argv
               34  LOAD_CONST               1
               36  LOAD_CONST               None
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'args'

 L. 249        46  LOAD_STR                 'command'
               48  LOAD_FAST                'args'
               50  COMPARE_OP               in
            52_54  POP_JUMP_IF_FALSE   858  'to 858'

 L. 250        56  LOAD_FAST                'args'
               58  LOAD_ATTR                command
               60  LOAD_STR                 'connect'
               62  COMPARE_OP               ==
            64_66  POP_JUMP_IF_FALSE   282  'to 282'

 L. 251        68  SETUP_FINALLY       108  'to 108'

 L. 252        70  LOAD_FAST                'args'
               72  LOAD_ATTR                key
               74  POP_JUMP_IF_FALSE    94  'to 94'

 L. 253        76  LOAD_GLOBAL              RSA
               78  LOAD_METHOD              import_key
               80  LOAD_FAST                'args'
               82  LOAD_ATTR                key
               84  LOAD_METHOD              read
               86  CALL_METHOD_0         0  ''
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'key_'
               92  JUMP_FORWARD        104  'to 104'
             94_0  COME_FROM            74  '74'

 L. 255        94  LOAD_GLOBAL              RSA
               96  LOAD_METHOD              generate
               98  LOAD_CONST               2048
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'key_'
            104_0  COME_FROM            92  '92'
              104  POP_BLOCK        
              106  JUMP_FORWARD        136  'to 136'
            108_0  COME_FROM_FINALLY    68  '68'

 L. 256       108  DUP_TOP          
              110  LOAD_GLOBAL              ValueError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   134  'to 134'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 257       122  LOAD_GLOBAL              exit_
              124  LOAD_STR                 'File has no valid RSA'
              126  CALL_FUNCTION_1       1  ''
              128  POP_TOP          
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM           114  '114'
              134  END_FINALLY      
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM           106  '106'

 L. 258       136  SETUP_FINALLY       204  'to 204'

 L. 259       138  LOAD_FAST                'args'
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

 L. 260       168  LOAD_GLOBAL              Shell

 L. 261       170  LOAD_FAST                'name'

 L. 262       172  LOAD_FAST                'key_'

 L. 263       174  LOAD_FAST                'args'
              176  LOAD_ATTR                ip

 L. 264       178  LOAD_FAST                'args'
              180  LOAD_ATTR                port

 L. 265       182  LOAD_FAST                'args'
              184  LOAD_ATTR                raw

 L. 260       186  CALL_FUNCTION_5       5  ''
              188  LOAD_METHOD              start
              190  CALL_METHOD_0         0  ''
              192  POP_TOP          

 L. 267       194  LOAD_GLOBAL              exit
              196  CALL_FUNCTION_0       0  ''
              198  POP_TOP          
              200  POP_BLOCK        
              202  JUMP_FORWARD        858  'to 858'
            204_0  COME_FROM_FINALLY   136  '136'

 L. 268       204  DUP_TOP          
              206  LOAD_GLOBAL              Exception
              208  COMPARE_OP               exception-match
          210_212  POP_JUMP_IF_FALSE   276  'to 276'
              214  POP_TOP          
              216  STORE_FAST               'e'
              218  POP_TOP          
              220  SETUP_FINALLY       264  'to 264'

 L. 269       222  LOAD_FAST                'args'
              224  LOAD_ATTR                debug
              226  POP_JUMP_IF_FALSE   234  'to 234'

 L. 270       228  LOAD_FAST                'e'
              230  RAISE_VARARGS_1       1  'exception instance'
              232  JUMP_FORWARD        260  'to 260'
            234_0  COME_FROM           226  '226'

 L. 272       234  LOAD_GLOBAL              exit_
              236  LOAD_FAST                'e'
              238  LOAD_ATTR                __class__
              240  LOAD_ATTR                __name__
              242  FORMAT_VALUE          0  ''
              244  LOAD_STR                 ': '
              246  LOAD_FAST                'e'
              248  LOAD_METHOD              __str__
              250  CALL_METHOD_0         0  ''
              252  FORMAT_VALUE          0  ''
              254  BUILD_STRING_3        3 
              256  CALL_FUNCTION_1       1  ''
              258  POP_TOP          
            260_0  COME_FROM           232  '232'
              260  POP_BLOCK        
              262  BEGIN_FINALLY    
            264_0  COME_FROM_FINALLY   220  '220'
              264  LOAD_CONST               None
              266  STORE_FAST               'e'
              268  DELETE_FAST              'e'
              270  END_FINALLY      
              272  POP_EXCEPT       
              274  JUMP_FORWARD        858  'to 858'
            276_0  COME_FROM           210  '210'
              276  END_FINALLY      
          278_280  JUMP_FORWARD        858  'to 858'
            282_0  COME_FROM            64  '64'

 L. 273       282  LOAD_FAST                'args'
              284  LOAD_ATTR                command
              286  LOAD_STR                 'key'
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_FALSE   858  'to 858'

 L. 274       294  LOAD_FAST                'args'
              296  LOAD_ATTR                gen
          298_300  POP_JUMP_IF_FALSE   636  'to 636'

 L. 275       302  LOAD_FAST                'args'
              304  LOAD_ATTR                gen
              306  LOAD_CONST               1024
              308  COMPARE_OP               <
          310_312  POP_JUMP_IF_FALSE   326  'to 326'

 L. 276       314  LOAD_GLOBAL              exit_
              316  LOAD_STR                 "Key length can't be less than 1024 bits"
              318  CALL_FUNCTION_1       1  ''
              320  POP_TOP          
          322_324  JUMP_ABSOLUTE       858  'to 858'
            326_0  COME_FROM           310  '310'

 L. 278       326  SETUP_FINALLY       576  'to 576'

 L. 279       328  LOAD_GLOBAL              os
              330  LOAD_ATTR                path
              332  LOAD_METHOD              isfile
              334  LOAD_FAST                'args'
              336  LOAD_ATTR                file
              338  CALL_METHOD_1         1  ''
          340_342  POP_JUMP_IF_FALSE   436  'to 436'

 L. 280       344  LOAD_GLOBAL              range
              346  LOAD_CONST               3
              348  CALL_FUNCTION_1       1  ''
              350  GET_ITER         
              352  FOR_ITER            432  'to 432'
              354  STORE_FAST               'i'

 L. 281       356  LOAD_GLOBAL              input
              358  LOAD_STR                 'File "'
              360  LOAD_GLOBAL              os
              362  LOAD_ATTR                path
              364  LOAD_METHOD              abspath
              366  LOAD_FAST                'args'
              368  LOAD_ATTR                file
              370  CALL_METHOD_1         1  ''
              372  FORMAT_VALUE          0  ''
              374  LOAD_STR                 '" already exists. Overwrite (y/n): '
              376  BUILD_STRING_3        3 
              378  CALL_FUNCTION_1       1  ''
              380  LOAD_METHOD              lower
              382  CALL_METHOD_0         0  ''
              384  STORE_FAST               'prompt'

 L. 283       386  LOAD_FAST                'prompt'
              388  LOAD_STR                 'y'
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_FALSE   404  'to 404'

 L. 284       396  POP_TOP          
          398_400  BREAK_LOOP          436  'to 436'
              402  JUMP_BACK           352  'to 352'
            404_0  COME_FROM           392  '392'

 L. 285       404  LOAD_FAST                'prompt'
              406  LOAD_STR                 'n'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   420  'to 420'

 L. 286       414  LOAD_GLOBAL              KeyboardInterrupt
              416  RAISE_VARARGS_1       1  'exception instance'
              418  JUMP_BACK           352  'to 352'
            420_0  COME_FROM           410  '410'

 L. 288       420  LOAD_GLOBAL              print
              422  LOAD_STR                 'Y or N. Try again...'
              424  CALL_FUNCTION_1       1  ''
              426  POP_TOP          
          428_430  JUMP_BACK           352  'to 352'

 L. 290       432  LOAD_GLOBAL              KeyboardInterrupt
              434  RAISE_VARARGS_1       1  'exception instance'
            436_0  COME_FROM           340  '340'

 L. 291       436  LOAD_GLOBAL              open
              438  LOAD_FAST                'args'
              440  LOAD_ATTR                file
              442  LOAD_STR                 'wb+'
              444  CALL_FUNCTION_2       2  ''
              446  SETUP_WITH          566  'to 566'
              448  STORE_FAST               'f'

 L. 292       450  LOAD_GLOBAL              print
              452  LOAD_STR                 'Generating '
              454  LOAD_FAST                'args'
              456  LOAD_ATTR                gen
              458  FORMAT_VALUE          0  ''
              460  LOAD_STR                 '-bit RSA key'
              462  BUILD_STRING_3        3 
              464  CALL_FUNCTION_1       1  ''
              466  POP_TOP          

 L. 293       468  LOAD_GLOBAL              RSA
              470  LOAD_METHOD              generate
              472  LOAD_FAST                'args'
              474  LOAD_ATTR                gen
              476  CALL_METHOD_1         1  ''
              478  STORE_FAST               'key_'

 L. 294       480  LOAD_FAST                'f'
              482  LOAD_METHOD              write
              484  LOAD_FAST                'key_'
              486  LOAD_METHOD              export_key
              488  CALL_METHOD_0         0  ''
              490  CALL_METHOD_1         1  ''
              492  POP_TOP          

 L. 295       494  LOAD_GLOBAL              print
              496  LOAD_STR                 'Generating complete'
              498  CALL_FUNCTION_1       1  ''
              500  POP_TOP          

 L. 296       502  LOAD_GLOBAL              exit_
              504  LOAD_STR                 'Key fingerprint:\n\tSHA1: '
              506  LOAD_GLOBAL              hashlib
              508  LOAD_METHOD              sha1
              510  LOAD_FAST                'key_'
              512  LOAD_METHOD              publickey
              514  CALL_METHOD_0         0  ''
              516  LOAD_METHOD              export_key
              518  LOAD_STR                 'DER'
              520  CALL_METHOD_1         1  ''
              522  CALL_METHOD_1         1  ''
              524  LOAD_METHOD              hexdigest
              526  CALL_METHOD_0         0  ''
              528  FORMAT_VALUE          0  ''
              530  LOAD_STR                 '\n\tSHA256: '
              532  LOAD_GLOBAL              hashlib
              534  LOAD_METHOD              sha256
              536  LOAD_FAST                'key_'
              538  LOAD_METHOD              publickey
              540  CALL_METHOD_0         0  ''
              542  LOAD_METHOD              export_key
              544  LOAD_STR                 'DER'
              546  CALL_METHOD_1         1  ''
              548  CALL_METHOD_1         1  ''
              550  LOAD_METHOD              hexdigest
              552  CALL_METHOD_0         0  ''
              554  FORMAT_VALUE          0  ''
              556  BUILD_STRING_4        4 
              558  CALL_FUNCTION_1       1  ''
              560  POP_TOP          
              562  POP_BLOCK        
              564  BEGIN_FINALLY    
            566_0  COME_FROM_WITH      446  '446'
              566  WITH_CLEANUP_START
              568  WITH_CLEANUP_FINISH
              570  END_FINALLY      
              572  POP_BLOCK        
              574  JUMP_FORWARD        634  'to 634'
            576_0  COME_FROM_FINALLY   326  '326'

 L. 300       576  DUP_TOP          
              578  LOAD_GLOBAL              OSError
              580  COMPARE_OP               exception-match
          582_584  POP_JUMP_IF_FALSE   604  'to 604'
              586  POP_TOP          
              588  POP_TOP          
              590  POP_TOP          

 L. 301       592  LOAD_GLOBAL              exit_
              594  LOAD_STR                 'Wrong file path'
              596  CALL_FUNCTION_1       1  ''
              598  POP_TOP          
              600  POP_EXCEPT       
              602  JUMP_FORWARD        634  'to 634'
            604_0  COME_FROM           582  '582'

 L. 302       604  DUP_TOP          
              606  LOAD_GLOBAL              KeyboardInterrupt
              608  COMPARE_OP               exception-match
          610_612  POP_JUMP_IF_FALSE   632  'to 632'
              614  POP_TOP          
              616  POP_TOP          
              618  POP_TOP          

 L. 303       620  LOAD_GLOBAL              exit_
              622  LOAD_STR                 'Generation canceled'
              624  CALL_FUNCTION_1       1  ''
              626  POP_TOP          
              628  POP_EXCEPT       
              630  JUMP_FORWARD        634  'to 634'
            632_0  COME_FROM           610  '610'
              632  END_FINALLY      
            634_0  COME_FROM           630  '630'
            634_1  COME_FROM           602  '602'
            634_2  COME_FROM           574  '574'
              634  JUMP_FORWARD        858  'to 858'
            636_0  COME_FROM           298  '298'

 L. 304       636  LOAD_FAST                'args'
              638  LOAD_ATTR                check
          640_642  POP_JUMP_IF_FALSE   850  'to 850'

 L. 305       644  LOAD_GLOBAL              os
              646  LOAD_ATTR                path
              648  LOAD_METHOD              isfile
              650  LOAD_FAST                'args'
              652  LOAD_ATTR                file
              654  CALL_METHOD_1         1  ''
          656_658  POP_JUMP_IF_FALSE   840  'to 840'

 L. 306       660  SETUP_FINALLY       688  'to 688'

 L. 307       662  LOAD_GLOBAL              RSA
              664  LOAD_METHOD              import_key
              666  LOAD_GLOBAL              open
              668  LOAD_FAST                'args'
              670  LOAD_ATTR                file
              672  LOAD_STR                 'r'
              674  CALL_FUNCTION_2       2  ''
              676  LOAD_METHOD              read
              678  CALL_METHOD_0         0  ''
              680  CALL_METHOD_1         1  ''
              682  STORE_FAST               'key_'
              684  POP_BLOCK        
              686  JUMP_FORWARD        718  'to 718'
            688_0  COME_FROM_FINALLY   660  '660'

 L. 308       688  DUP_TOP          
              690  LOAD_GLOBAL              ValueError
              692  COMPARE_OP               exception-match
          694_696  POP_JUMP_IF_FALSE   716  'to 716'
              698  POP_TOP          
              700  POP_TOP          
              702  POP_TOP          

 L. 309       704  LOAD_GLOBAL              exit_
              706  LOAD_STR                 'File has no RSA key'
              708  CALL_FUNCTION_1       1  ''
              710  POP_TOP          
              712  POP_EXCEPT       
              714  JUMP_FORWARD        718  'to 718'
            716_0  COME_FROM           694  '694'
              716  END_FINALLY      
            718_0  COME_FROM           714  '714'
            718_1  COME_FROM           686  '686'

 L. 310       718  LOAD_GLOBAL              exit_
              720  LOAD_STR                 'RSA key type: '
              722  LOAD_FAST                'key_'
              724  LOAD_METHOD              has_private
              726  CALL_METHOD_0         0  ''
          728_730  POP_JUMP_IF_FALSE   736  'to 736'
              732  LOAD_STR                 'Public'
              734  JUMP_FORWARD        738  'to 738'
            736_0  COME_FROM           728  '728'
              736  LOAD_STR                 'Private'
            738_0  COME_FROM           734  '734'
              738  FORMAT_VALUE          0  ''
              740  LOAD_STR                 '\nRSA length: '
              742  LOAD_FAST                'key_'
              744  LOAD_METHOD              size_in_bits
              746  CALL_METHOD_0         0  ''
              748  FORMAT_VALUE          0  ''
              750  LOAD_STR                 '-bits ('
              752  LOAD_FAST                'key_'
              754  LOAD_METHOD              size_in_bytes
              756  CALL_METHOD_0         0  ''
              758  FORMAT_VALUE          0  ''
              760  LOAD_STR                 '-bytes)\nKey fingerprint:\n\tSHA1: '
              762  LOAD_GLOBAL              hashlib
              764  LOAD_METHOD              sha1
              766  LOAD_FAST                'key_'
              768  LOAD_METHOD              publickey
              770  CALL_METHOD_0         0  ''
              772  LOAD_METHOD              export_key
              774  LOAD_STR                 'DER'
              776  CALL_METHOD_1         1  ''
              778  CALL_METHOD_1         1  ''
            780_0  COME_FROM           202  '202'
              780  LOAD_METHOD              hexdigest
              782  CALL_METHOD_0         0  ''
              784  FORMAT_VALUE          0  ''
              786  LOAD_STR                 '\n\tSHA256: '
              788  LOAD_GLOBAL              hashlib
              790  LOAD_METHOD              sha256
              792  LOAD_FAST                'key_'
              794  LOAD_METHOD              publickey
              796  CALL_METHOD_0         0  ''
              798  LOAD_METHOD              export_key
              800  LOAD_STR                 'DER'
              802  CALL_METHOD_1         1  ''
              804  CALL_METHOD_1         1  ''
              806  LOAD_METHOD              hexdigest
              808  CALL_METHOD_0         0  ''
              810  FORMAT_VALUE          0  ''
              812  LOAD_STR                 '\nCan be used for uctp: '
              814  LOAD_FAST                'key_'
              816  LOAD_METHOD              has_private
              818  CALL_METHOD_0         0  ''
          820_822  POP_JUMP_IF_FALSE   828  'to 828'
              824  LOAD_STR                 'Yes'
              826  JUMP_FORWARD        830  'to 830'
            828_0  COME_FROM           820  '820'
              828  LOAD_STR                 'No'
            830_0  COME_FROM           826  '826'
              830  FORMAT_VALUE          0  ''
              832  BUILD_STRING_12      12 
              834  CALL_FUNCTION_1       1  ''
              836  POP_TOP          
              838  JUMP_FORWARD        848  'to 848'
            840_0  COME_FROM           656  '656'

 L. 317       840  LOAD_GLOBAL              exit_
              842  LOAD_STR                 "File doesn't exist"
              844  CALL_FUNCTION_1       1  ''
              846  POP_TOP          
            848_0  COME_FROM           838  '838'
              848  JUMP_FORWARD        858  'to 858'
            850_0  COME_FROM           640  '640'

 L. 319       850  LOAD_GLOBAL              key
            852_0  COME_FROM           274  '274'
              852  LOAD_METHOD              print_usage
              854  CALL_METHOD_0         0  ''
              856  POP_TOP          
            858_0  COME_FROM           848  '848'
            858_1  COME_FROM           634  '634'
            858_2  COME_FROM           290  '290'
            858_3  COME_FROM           278  '278'
            858_4  COME_FROM            52  '52'

 L. 320       858  LOAD_GLOBAL              parser
              860  LOAD_METHOD              print_usage
              862  CALL_METHOD_0         0  ''
              864  POP_TOP          
              866  JUMP_FORWARD        876  'to 876'
            868_0  COME_FROM             8  '8'

 L. 322       868  LOAD_GLOBAL              print
              870  LOAD_STR                 'uctp-cli supports only linux'
              872  CALL_FUNCTION_1       1  ''
              874  POP_TOP          
            876_0  COME_FROM           866  '866'

Parse error at or near `COME_FROM' instruction at offset 780_0