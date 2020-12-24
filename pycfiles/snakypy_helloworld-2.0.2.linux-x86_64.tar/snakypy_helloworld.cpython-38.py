# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/files/github/repository/williamcanin/snakypy/snakypy-helloworld/venv/lib/python3.8/site-packages/snakypy_helloworld/snakypy_helloworld.py
# Compiled at: 2020-02-26 22:56:26
# Size of source mod 2**32: 3846 bytes
import json, os
from sys import exit
from snakypy_helloworld import __PKG_NAME__, __version__

class SnakypyHelloworld:
    __doc__ = '\n        PyHell class where everything will happen.\n    '
    config = {'appname':'Snakypy Helloworld', 
     'appexec':'helloworld.py', 
     'author':{'name':'Snakypy Org', 
      'email':'contact.snakypy@gmail.com', 
      'website':'https://snakypy.github.io', 
      'github':'snakypy'}}

    def __init__(self, NAME='World!'):
        """
            Constructor method, gets a parameter with default
            value "World!" case user does not specify parameter
            in optional arguments when executing program.
        """
        self.NAME = NAME

    def get_data(self):
        """
            This method is responsible for reading the program configuration
            JSON file. This file contains information that is used.
        """
        _path = os.path.dirname(os.path.realpath(__file__)) + '/'
        with open(os.path.join(_path, 'data/data.json'), 'r') as (f):
            data = json.load(f)
        return data

    def menu(self):
        "%s" % '\n            This method is responsible for passing an optional parameter\n            to display a custom message on the console. In addition, I also\n            displayed other functionality, such as showing help. To do this,\n            run helloworld.py --help" on the console.\n        '
        from argparse import ArgumentParser, RawTextHelpFormatter
        try:
            parser = ArgumentParser(prog=(self.config['appname']), usage=f"{self.config['appexec']} <optional arguments>",
              description='Snakypy Helloworld is a simple script with parameterized to show hello message.',
              formatter_class=RawTextHelpFormatter,
              epilog='See you later!!')
            parser.add_argument('--name', '-n', help='This option shows welcome to someone.')
            parser.add_argument('--version', '-v', action='store_true', default=False, help='Shows the current version.')
            args = parser.parse_args()
            return args
            except Exception as err:
            try:
                print('Error in passing arguments...', err)
            finally:
                err = None
                del err

    def message--- This code section failed: ---

 L.  74         0  SETUP_FINALLY       162  'to 162'

 L.  75         2  LOAD_FAST                'self'
                4  LOAD_METHOD              menu
                6  CALL_METHOD_0         0  ''
                8  LOAD_ATTR                version
               10  POP_JUMP_IF_FALSE    30  'to 30'

 L.  76        12  LOAD_GLOBAL              print
               14  LOAD_GLOBAL              __version__
               16  FORMAT_VALUE          0  ''
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          

 L.  77        22  LOAD_GLOBAL              exit
               24  LOAD_CONST               0
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          
             30_0  COME_FROM            10  '10'

 L.  78        30  LOAD_FAST                'self'
               32  LOAD_METHOD              menu
               34  CALL_METHOD_0         0  ''
               36  LOAD_ATTR                name
               38  LOAD_CONST               None
               40  COMPARE_OP               is
               42  POP_JUMP_IF_FALSE    60  'to 60'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                NAME
               48  LOAD_STR                 'World!'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    60  'to 60'

 L.  79        54  POP_BLOCK        
               56  LOAD_STR                 'Hello, World!'
               58  RETURN_VALUE     
             60_0  COME_FROM            52  '52'
             60_1  COME_FROM            42  '42'

 L.  81        60  LOAD_FAST                'self'
               62  LOAD_METHOD              menu
               64  CALL_METHOD_0         0  ''
               66  LOAD_ATTR                name
               68  LOAD_CONST               None
               70  COMPARE_OP               is-not
               72  POP_JUMP_IF_FALSE   108  'to 108'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                NAME
               78  LOAD_STR                 'World!'
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   108  'to 108'

 L.  82        84  LOAD_STR                 'Hello, Mr(s) '
               86  LOAD_FAST                'self'
               88  LOAD_METHOD              menu
               90  CALL_METHOD_0         0  ''
               92  LOAD_ATTR                name
               94  LOAD_METHOD              title
               96  CALL_METHOD_0         0  ''
               98  FORMAT_VALUE          0  ''
              100  LOAD_STR                 '!'
              102  BUILD_STRING_3        3 
              104  POP_BLOCK        
              106  RETURN_VALUE     
            108_0  COME_FROM            82  '82'
            108_1  COME_FROM            72  '72'

 L.  83       108  LOAD_FAST                'self'
              110  LOAD_METHOD              menu
              112  CALL_METHOD_0         0  ''
              114  LOAD_ATTR                name
              116  LOAD_CONST               None
              118  COMPARE_OP               is
              120  POP_JUMP_IF_FALSE   152  'to 152'
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                NAME
              126  LOAD_STR                 'World!'
              128  COMPARE_OP               !=
              130  POP_JUMP_IF_FALSE   152  'to 152'

 L.  84       132  LOAD_STR                 'Hello, Mr(s) '
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                NAME
              138  LOAD_METHOD              title
              140  CALL_METHOD_0         0  ''
              142  FORMAT_VALUE          0  ''
              144  LOAD_STR                 '!'
              146  BUILD_STRING_3        3 
              148  POP_BLOCK        
              150  RETURN_VALUE     
            152_0  COME_FROM           130  '130'
            152_1  COME_FROM           120  '120'

 L.  86       152  POP_BLOCK        
              154  LOAD_CONST               None
              156  RETURN_VALUE     
              158  POP_BLOCK        
              160  JUMP_FORWARD        206  'to 206'
            162_0  COME_FROM_FINALLY     0  '0'

 L.  87       162  DUP_TOP          
              164  LOAD_GLOBAL              Exception
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   204  'to 204'
              170  POP_TOP          
              172  STORE_FAST               'err'
              174  POP_TOP          
              176  SETUP_FINALLY       192  'to 192'

 L.  88       178  LOAD_GLOBAL              print
              180  LOAD_STR                 'There was some error in the parameterization.'
              182  LOAD_FAST                'err'
              184  CALL_FUNCTION_2       2  ''
              186  POP_TOP          
              188  POP_BLOCK        
              190  BEGIN_FINALLY    
            192_0  COME_FROM_FINALLY   176  '176'
              192  LOAD_CONST               None
              194  STORE_FAST               'err'
              196  DELETE_FAST              'err'
              198  END_FINALLY      
              200  POP_EXCEPT       
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           168  '168'
              204  END_FINALLY      
            206_0  COME_FROM           202  '202'
            206_1  COME_FROM           160  '160'

Parse error at or near `LOAD_STR' instruction at offset 56

    def __str__(self):
        """
            Python's special method for returning a Hello message when
            executing the Snakypy Helloworld class.
        """
        header = self.get_data()['head']
        body = self.message()
        footer = 'I was raised with Python. :)'
        return f"{header}\n{body}\n{footer}"


if __name__ == '__main__':
    print(SnakypyHelloworld())