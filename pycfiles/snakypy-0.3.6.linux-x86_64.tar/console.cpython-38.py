# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/console.py
# Compiled at: 2020-04-04 05:33:11
# Size of source mod 2**32: 17814 bytes
from snakypy.utils import decorators
from snakypy.ansi import NONE, FG, BG, SGR

def attr_foreground_background_sgr(*args):
    """
    Checks if the attributes of the functions that the foreground
    and background parameters are in accordance with their respective class.

    Arguments:
        args {str} -- It receives a certain number of arguments with an ansi code value.
    """
    if args[0]:
        if args[0] not in FG.__dict__.values():
            msg = 'Attribute invalid in parameter "foreground". Must receive from FG class.'
            raise AttributeError(msg)
    else:
        if args[1]:
            if args[1] not in BG.__dict__.values():
                msg = 'Attribute invalid in parameter "background". Must receive from BG class.'
                raise AttributeError(msg)
        if args[2] and args[2] not in SGR.__dict__.values():
            msg = 'Attribute invalid in parameter "sgr". Must receive from SGR class.'
            raise AttributeError(msg)


@decorators.denying_os('nt')
def printer(*args, foreground='', background='', sgr='', sep=' ', end='\n', file=None, flush=False):
    """A function that allows you to print colored text on the terminal.

    >>> from snakypy import printer, FG, BG, SGR
    >>> printer('Hello, World!', foreground=FG.BLACK, background=BG.WHITE, sgr=SGR.UNDERLINE)
    >>> printer('Hello, World!', foreground=FG.MAGENTA, sgr=SGR.UNDERLINE)

    Keyword Arguments:
        **foreground {str}** -- This named argument should optionally receive                             an object of class "snakypy.ansi.FG" for the foreground                             color of the text. This object will be text with ansi code.                             (default: '')

        **background {str}** -- This named argument should optionally receive                             an object of class "snakypy.ansi.BG" for the background                             color of the text. This object will be text with ansi code.                             (default: '')

        **sgr {str}** -- This named argument should optionally receive                      an object of class "snakypy.ansi.SGR" for the effect                      of the text. This object will be text with ansi code.                      (default: '')

        **sep {str}** -- Separator between printer function objects. (default: {' '}) 
        **end {str}** -- Responsible for skipping a line after printing is finished.                          (default: '[bar]n')
    """
    attr_foreground_background_sgr(foreground, background, sgr)
    lst = []
    for i in range(len(args)):
        lst.append(args[i])
    else:
        text = ' '.join(map(str, lst))
        return print(f"{NONE}{sgr}{foreground}{background}{text}{NONE}",
          sep=sep,
          end=end,
          file=file,
          flush=flush)


@decorators.denying_os('nt')
def entry--- This code section failed: ---

 L. 117         0  LOAD_GLOBAL              attr_foreground_background_sgr
                2  LOAD_FAST                'foreground'
                4  LOAD_FAST                'background'
                6  LOAD_FAST                'sgr'
                8  CALL_FUNCTION_3       3  ''
               10  POP_TOP          

 L. 119        12  SETUP_FINALLY        52  'to 52'

 L. 120        14  LOAD_GLOBAL              input
               16  LOAD_GLOBAL              NONE
               18  FORMAT_VALUE          0  ''
               20  LOAD_FAST                'sgr'
               22  FORMAT_VALUE          0  ''
               24  LOAD_FAST                'foreground'
               26  FORMAT_VALUE          0  ''
               28  LOAD_FAST                'background'
               30  FORMAT_VALUE          0  ''
               32  LOAD_FAST                'text'
               34  FORMAT_VALUE          0  ''
               36  LOAD_FAST                'jump_line'
               38  FORMAT_VALUE          0  ''
               40  LOAD_GLOBAL              NONE
               42  FORMAT_VALUE          0  ''
               44  BUILD_STRING_7        7 
               46  CALL_FUNCTION_1       1  ''
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    12  '12'

 L. 121        52  DUP_TOP          
               54  LOAD_GLOBAL              KeyboardInterrupt
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    92  'to 92'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 122        66  LOAD_GLOBAL              print
               68  LOAD_STR                 '\n'
               70  LOAD_GLOBAL              FG
               72  LOAD_ATTR                WARNING
               74  FORMAT_VALUE          0  ''
               76  LOAD_STR                 ' Aborted by user.'
               78  LOAD_GLOBAL              NONE
               80  FORMAT_VALUE          0  ''
               82  BUILD_STRING_4        4 
               84  CALL_FUNCTION_1       1  ''
               86  POP_TOP          
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
             92_0  COME_FROM            58  '58'
               92  END_FINALLY      
             94_0  COME_FROM            90  '90'

Parse error at or near `POP_TOP' instruction at offset 62


def pick_options--- This code section failed: ---

 L. 129         0  LOAD_FAST                'colorful'
                2  POP_JUMP_IF_TRUE     40  'to 40'

 L. 130         4  LOAD_STR                 ''
                6  LOAD_GLOBAL              FG
                8  STORE_ATTR               QUESTION

 L. 131        10  LOAD_STR                 ''
               12  LOAD_GLOBAL              FG
               14  STORE_ATTR               GREEN

 L. 132        16  LOAD_STR                 ''
               18  LOAD_GLOBAL              FG
               20  STORE_ATTR               MAGENTA

 L. 133        22  LOAD_STR                 ''
               24  LOAD_GLOBAL              FG
               26  STORE_ATTR               CYAN

 L. 134        28  LOAD_STR                 ''
               30  LOAD_GLOBAL              FG
               32  STORE_ATTR               ERROR

 L. 135        34  LOAD_STR                 ''
               36  LOAD_GLOBAL              FG
               38  STORE_ATTR               WARNING
             40_0  COME_FROM             2  '2'

 L. 136        40  LOAD_FAST                'ctrl_c_message'
               42  POP_JUMP_IF_FALSE    48  'to 48'
               44  LOAD_STR                 '(Ctrl+C to Cancel)'
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            42  '42'
               48  LOAD_STR                 ''
             50_0  COME_FROM            46  '46'
               50  STORE_FAST               'ctrl_c'

 L. 137        52  LOAD_GLOBAL              printer
               54  LOAD_FAST                'title'
               56  LOAD_FAST                'ctrl_c'
               58  LOAD_GLOBAL              FG
               60  LOAD_ATTR                QUESTION
               62  LOAD_CONST               ('foreground',)
               64  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               66  POP_TOP          

 L. 138        68  LOAD_CONST               1
               70  STORE_FAST               'count'

 L. 139        72  LOAD_FAST                'options'
               74  GET_ITER         
               76  FOR_ITER            126  'to 126'
               78  STORE_FAST               'option'

 L. 140        80  LOAD_GLOBAL              print
               82  LOAD_GLOBAL              FG
               84  LOAD_ATTR                GREEN
               86  FORMAT_VALUE          0  ''
               88  LOAD_STR                 '['
               90  LOAD_FAST                'count'
               92  FORMAT_VALUE          0  ''
               94  LOAD_STR                 '] '
               96  LOAD_GLOBAL              FG
               98  LOAD_ATTR                MAGENTA
              100  FORMAT_VALUE          0  ''
              102  LOAD_FAST                'option'
              104  FORMAT_VALUE          0  ''
              106  LOAD_GLOBAL              NONE
              108  FORMAT_VALUE          0  ''
              110  BUILD_STRING_7        7 
              112  CALL_FUNCTION_1       1  ''
              114  POP_TOP          

 L. 141       116  LOAD_FAST                'count'
              118  LOAD_CONST               1
              120  INPLACE_ADD      
              122  STORE_FAST               'count'
              124  JUMP_BACK            76  'to 76'

 L. 142       126  SETUP_FINALLY       248  'to 248'

 L. 143       128  LOAD_GLOBAL              int
              130  LOAD_GLOBAL              input
              132  LOAD_GLOBAL              FG
              134  LOAD_ATTR                CYAN
              136  FORMAT_VALUE          0  ''
              138  LOAD_FAST                'answer'
              140  FORMAT_VALUE          0  ''
              142  LOAD_STR                 ' '
              144  LOAD_GLOBAL              NONE
              146  FORMAT_VALUE          0  ''
              148  BUILD_STRING_4        4 
              150  CALL_FUNCTION_1       1  ''
              152  CALL_FUNCTION_1       1  ''
              154  LOAD_CONST               1
              156  BINARY_SUBTRACT  
              158  STORE_FAST               'pos'

 L. 144       160  LOAD_FAST                'pos'
              162  LOAD_CONST               -1
              164  COMPARE_OP               >
              166  POP_JUMP_IF_TRUE    172  'to 172'
              168  LOAD_ASSERT              AssertionError
              170  RAISE_VARARGS_1       1  'exception instance'
            172_0  COME_FROM           166  '166'

 L. 145       172  LOAD_FAST                'index'
              174  POP_JUMP_IF_FALSE   198  'to 198'
              176  LOAD_FAST                'lowercase'
              178  POP_JUMP_IF_FALSE   198  'to 198'

 L. 146       180  LOAD_FAST                'pos'
              182  LOAD_FAST                'options'
              184  LOAD_FAST                'pos'
              186  BINARY_SUBSCR    
              188  LOAD_METHOD              lower
              190  CALL_METHOD_0         0  ''
              192  BUILD_TUPLE_2         2 
              194  POP_BLOCK        
              196  RETURN_VALUE     
            198_0  COME_FROM           178  '178'
            198_1  COME_FROM           174  '174'

 L. 147       198  LOAD_FAST                'index'
              200  POP_JUMP_IF_FALSE   220  'to 220'
              202  LOAD_FAST                'lowercase'
              204  POP_JUMP_IF_TRUE    220  'to 220'

 L. 148       206  LOAD_FAST                'pos'
              208  LOAD_FAST                'options'
              210  LOAD_FAST                'pos'
              212  BINARY_SUBSCR    
              214  BUILD_TUPLE_2         2 
              216  POP_BLOCK        
              218  RETURN_VALUE     
            220_0  COME_FROM           204  '204'
            220_1  COME_FROM           200  '200'

 L. 149       220  LOAD_FAST                'lowercase'
              222  POP_JUMP_IF_FALSE   238  'to 238'

 L. 150       224  LOAD_FAST                'options'
              226  LOAD_FAST                'pos'
              228  BINARY_SUBSCR    
              230  LOAD_METHOD              lower
              232  CALL_METHOD_0         0  ''
              234  POP_BLOCK        
              236  RETURN_VALUE     
            238_0  COME_FROM           222  '222'

 L. 151       238  LOAD_FAST                'options'
              240  LOAD_FAST                'pos'
              242  BINARY_SUBSCR    
              244  POP_BLOCK        
              246  RETURN_VALUE     
            248_0  COME_FROM_FINALLY   126  '126'

 L. 152       248  DUP_TOP          
              250  LOAD_GLOBAL              Exception
              252  COMPARE_OP               exception-match
          254_256  POP_JUMP_IF_FALSE   284  'to 284'
              258  POP_TOP          
              260  POP_TOP          
              262  POP_TOP          

 L. 153       264  LOAD_GLOBAL              printer
              266  LOAD_STR                 'Option invalid!'
              268  LOAD_GLOBAL              FG
              270  LOAD_ATTR                ERROR
              272  LOAD_CONST               ('foreground',)
              274  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              276  POP_TOP          

 L. 154       278  POP_EXCEPT       
              280  LOAD_CONST               False
              282  RETURN_VALUE     
            284_0  COME_FROM           254  '254'

 L. 155       284  DUP_TOP          
              286  LOAD_GLOBAL              KeyboardInterrupt
              288  COMPARE_OP               exception-match
          290_292  POP_JUMP_IF_FALSE   320  'to 320'
              294  POP_TOP          
              296  POP_TOP          
              298  POP_TOP          

 L. 156       300  LOAD_GLOBAL              printer
              302  LOAD_STR                 'Canceled by user.'
              304  LOAD_GLOBAL              FG
              306  LOAD_ATTR                WARNING
              308  LOAD_CONST               ('foreground',)
              310  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              312  POP_TOP          

 L. 157       314  POP_EXCEPT       
              316  LOAD_CONST               None
              318  RETURN_VALUE     
            320_0  COME_FROM           290  '290'
              320  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 260


def pick--- This code section failed: ---

 L. 218         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'options'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              list
                8  COMPARE_OP               is-not
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 219        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'You must enter a list in the argument: options'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 221        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'title'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_CONST               0
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L. 222        32  LOAD_GLOBAL              TypeError
               34  LOAD_STR                 'The title cannot contain an empty element. Approached.'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'

 L. 224        40  LOAD_FAST                'options'
               42  GET_ITER         
             44_0  COME_FROM            58  '58'
               44  FOR_ITER             70  'to 70'
               46  STORE_FAST               'option'

 L. 225        48  LOAD_GLOBAL              len
               50  LOAD_FAST                'option'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_CONST               0
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    44  'to 44'

 L. 226        60  LOAD_GLOBAL              TypeError
               62  LOAD_STR                 'The list cannot contain an empty element. Approached.'
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
               68  JUMP_BACK            44  'to 44'

 L. 228        70  SETUP_FINALLY       116  'to 116'
             72_0  COME_FROM           104  '104'

 L. 230        72  LOAD_GLOBAL              pick_options

 L. 231        74  LOAD_FAST                'title'

 L. 231        76  LOAD_FAST                'options'

 L. 231        78  LOAD_FAST                'answer'

 L. 231        80  LOAD_FAST                'index'

 L. 231        82  LOAD_FAST                'colorful'

 L. 232        84  LOAD_FAST                'lowercase'

 L. 232        86  LOAD_FAST                'ctrl_c_message'

 L. 230        88  LOAD_CONST               ('answer', 'index', 'colorful', 'lowercase', 'ctrl_c_message')
               90  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
               92  STORE_FAST               'option'

 L. 234        94  LOAD_FAST                'option'
               96  POP_JUMP_IF_TRUE    110  'to 110'
               98  LOAD_FAST                'option'
              100  LOAD_CONST               None
              102  COMPARE_OP               is
              104  POP_JUMP_IF_FALSE    72  'to 72'

 L. 235       106  BREAK_LOOP          110  'to 110'
              108  JUMP_BACK            72  'to 72'
            110_0  COME_FROM            96  '96'

 L. 236       110  LOAD_FAST                'option'
              112  POP_BLOCK        
              114  RETURN_VALUE     
            116_0  COME_FROM_FINALLY    70  '70'

 L. 237       116  DUP_TOP          
              118  LOAD_GLOBAL              Exception
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   142  'to 142'
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          

 L. 238       130  LOAD_GLOBAL              Exception
              132  LOAD_STR                 'An unexpected error occurs when using pick'
              134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  'exception instance'
              138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM           122  '122'
              142  END_FINALLY      
            144_0  COME_FROM           140  '140'

Parse error at or near `DUP_TOP' instruction at offset 116


def billboard(text, foreground='', background='', ret_text=False, justify='auto'):
    """
    Creates a Billboard in the terminal.

    >>> from snakypy.console import billboard
    >>> from snakypy import FG, BG
    >>> billboard('Hello, Snakypy!')
    >>> billboard('Hello, Snakypy!', foreground=FG.BLUE, background=BG.WHITE)

    Arguments:
        **text {str}** -- Any text must be informed.

    Keyword Arguments:
        **foreground {str}** -- This named argument should optionally receive                             an object of class "snakypy.ansi.FG" for the foreground                             color of the text. This object will be text with ansi code.                             (default: '')

        **background {str}** -- This named argument should optionally receive                             an object of class "snakypy.ansi.BG" for the background                             color of the text. This object will be text with ansi code.                             (default: '')

        **ret_text {bool}** -- Receives a Boolean value. If the value is True, it will only                                return the text. If the value is False, it will resume printing.

        **justify {str}** -- Justify the position of the text: auto | center | right.                              (default: 'auto')

    Returns:
        **[str]** -- The text informed in billboard form.
    """
    import pyfiglet, snakypy
    banner = pyfiglet.figlet_format(text, justify=justify)
    if ret_text:
        return banner
    return snakypy.printer(banner, foreground=foreground, background=background)


def cmd(command, *args, shell=True, universal_newlines=True, ret=False, verbose=False):
    """
    Function that uses the subprocess library with Popen.
    The function receives a command as an argument and shows
    execution in real time.

    >>> from snakypy.console import cmd
    >>> command = 'git clone https://github.com/snakypy/snakypy.git'
    >>> cmd(command, verbose=True)

    Arguments:
        **command {str}** -- Must inform the command to be executed.

    Keyword Arguments:
        **shell {bool}** -- Receives a Boolean value. If it has False, the command must be \xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0in list where the command space is split. \xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0**E.g:** ['ls', '/bin']. \xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0If the value is True, the command can be stored in a string \xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0normal. **E.g:** 'ls /bin'

        **ret {bool}** -- The default value is False, however if it is set to True it will                       return a code\xa0status of the command output, where the code 0 (zero),                       is output without errors. 
        **verbose {bool}** -- The default value is False, if you change it to True, the command                           will show\xa0in real time the exit at the terminal, if there is an exit.     """
    from subprocess import Popen, PIPE
    process = Popen(command,
      shell=shell, stdout=PIPE, universal_newlines=universal_newlines)
    if verbose:
        for line in iter(process.stdout.readline, ''):
            print(NONE, *args, *(line.rstrip(), NONE))

    if ret:
        r = process.poll()
        return r


def credence(app_name, app_version, app_url, data: dict, foreground='', column: int=80):
    """
    Print project development credits.

    >>> from snakypy.console import credence
    >>> data = {
        "credence": [
            {
                "my_name": "William Canin",
                "email": "example@domain.com",
                "website": "http://williamcanin.me",
                "locale": "Brazil - SP"
            },
            {
                "my_name": "Maria Canin",
                "email": "example@domain.com",
                "locale": "Brazil - SP"
            }
        ]
    }
    >>> credence('Snakypy', '0.1.0', 'https://github.com/snakypy/snakypy', data)

    **output:**

    .. code-block:: shell

        ---------------------------------------------------------
                       Snakypy - Version 0.1.0
        ---------------------------------------------------------

                              Credence:

                        My Name: William Canin
                      Email: example@domain.com
                   Website: http://williamcanin.me
                         Locale: Brazil - SP

                         My Name: Maria Canin
                      Email: example@domain.com
                         Locale: Brazil - SP

        ---------------------------------------------------------
                    Snakypy © 2020 - All Right Reserved.
                Home: https://github.com/snakypy/snakypy
        ---------------------------------------------------------

    Arguments:
        app_name {str} -- Put application name.

        app_version {str} -- Application version.

        app_url {str} -- Application or website url.

        data {dict} -- You must receive a dictionary containing a key called "credence".
                       E.g: data = {'credence': []}

    Keyword Arguments:
        **foreground {str}** -- This named argument should optionally receive                             an object of class "snakypy.ansi.FG" for the foreground                             color of the text. This object will be text with ansi code.                             (default: '')

        **column {int}** -- Justify the position of the credits through the columns                           using an integer. (default: 80)
    """
    from datetime import date
    try:
        if type(data) is not dict:
            msg = f'>>> The function "{credence.__name__}" must take a dictionary as an argument.'
            raise Exception(msg)
        printer(((f"{'---------------------------------------------------------'}").center(column)), foreground=foreground)
        printer((f"{app_name} - Version {app_version}".center(column)), foreground=foreground)
        printer((f"{'---------------------------------------------------------'}\n".center(column)), foreground=foreground)
        printer(('Credence:\n'.center(column)), foreground=foreground)
        for item in data['credence']:
            for key, value in item.items():
                printer((f"{key.title().replace('_', ' ')}: {value}".center(column)),
                  foreground=foreground)
            else:
                print()

        else:
            printer(((f"{'---------------------------------------------------------'}").center(column)), foreground=foreground)
            printer((f"{app_name} © {date.today().year} - All Right Reserved.".center(column)),
              foreground=foreground)
            printer((f"Home: {app_url}".center(column)), foreground=foreground)
            printer(((f"{'---------------------------------------------------------'}").center(column)), foreground=foreground)

    except KeyError:
        msg = "The 'credence' key was not found.Enter a dictionary containing a 'credits' key."
        raise KeyError(msg)


def loading--- This code section failed: ---

 L. 457         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              time
                6  STORE_FAST               'time'

 L. 458         8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              sys
               14  STORE_FAST               'sys'

 L. 461        16  LOAD_GLOBAL              printer
               18  LOAD_FAST                'header'
               20  LOAD_FAST                'foreground'
               22  LOAD_CONST               ('foreground',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  POP_TOP          

 L. 462        28  SETUP_FINALLY       242  'to 242'

 L. 463        30  LOAD_FAST                'bar'
               32  POP_JUMP_IF_FALSE   146  'to 146'

 L. 464        34  LOAD_GLOBAL              range
               36  LOAD_CONST               0
               38  LOAD_CONST               100
               40  CALL_FUNCTION_2       2  ''
               42  GET_ITER         
               44  FOR_ITER            134  'to 134'
               46  STORE_FAST               'i'

 L. 465        48  LOAD_FAST                'time'
               50  LOAD_METHOD              sleep
               52  LOAD_FAST                'set_time'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 466        58  LOAD_FAST                'i'
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  LOAD_CONST               4
               66  BINARY_TRUE_DIVIDE
               68  STORE_FAST               'width'

 L. 467        70  LOAD_STR                 '['
               72  LOAD_STR                 '#'
               74  LOAD_GLOBAL              int
               76  LOAD_FAST                'width'
               78  CALL_FUNCTION_1       1  ''
               80  BINARY_MULTIPLY  
               82  FORMAT_VALUE          0  ''
               84  LOAD_STR                 ' '
               86  LOAD_CONST               25
               88  LOAD_GLOBAL              int
               90  LOAD_FAST                'width'
               92  CALL_FUNCTION_1       1  ''
               94  BINARY_SUBTRACT  
               96  BINARY_MULTIPLY  
               98  FORMAT_VALUE          0  ''
              100  LOAD_STR                 ']'
              102  BUILD_STRING_4        4 
              104  STORE_FAST               'bar'

 L. 468       106  LOAD_FAST                'sys'
              108  LOAD_ATTR                stdout
              110  LOAD_METHOD              write
              112  LOAD_STR                 '\x1b[1000D'
              114  LOAD_FAST                'bar'
              116  BINARY_ADD       
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 469       122  LOAD_FAST                'sys'
              124  LOAD_ATTR                stdout
              126  LOAD_METHOD              flush
              128  CALL_METHOD_0         0  ''
              130  POP_TOP          
              132  JUMP_BACK            44  'to 44'

 L. 470       134  LOAD_GLOBAL              print
              136  CALL_FUNCTION_0       0  ''
              138  POP_TOP          

 L. 471       140  POP_BLOCK        
              142  LOAD_CONST               None
              144  RETURN_VALUE     
            146_0  COME_FROM            32  '32'

 L. 472       146  LOAD_GLOBAL              range
              148  LOAD_CONST               0
              150  LOAD_CONST               100
              152  CALL_FUNCTION_2       2  ''
              154  GET_ITER         
              156  FOR_ITER            230  'to 230'
              158  STORE_FAST               'i'

 L. 473       160  LOAD_FAST                'time'
              162  LOAD_METHOD              sleep
              164  LOAD_FAST                'set_time'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 474       170  LOAD_FAST                'sys'
              172  LOAD_ATTR                stdout
              174  LOAD_METHOD              write
              176  LOAD_STR                 '\x1b[1000D'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          

 L. 475       182  LOAD_FAST                'sys'
              184  LOAD_ATTR                stdout
              186  LOAD_METHOD              flush
              188  CALL_METHOD_0         0  ''
              190  POP_TOP          

 L. 477       192  LOAD_FAST                'sys'
              194  LOAD_ATTR                stdout
              196  LOAD_METHOD              write
              198  LOAD_GLOBAL              str
              200  LOAD_FAST                'i'
              202  LOAD_CONST               1
              204  BINARY_ADD       
              206  CALL_FUNCTION_1       1  ''
              208  FORMAT_VALUE          0  ''
              210  LOAD_STR                 '%'
              212  BUILD_STRING_2        2 
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          

 L. 478       218  LOAD_FAST                'sys'
              220  LOAD_ATTR                stdout
              222  LOAD_METHOD              flush
              224  CALL_METHOD_0         0  ''
              226  POP_TOP          
              228  JUMP_BACK           156  'to 156'

 L. 479       230  LOAD_GLOBAL              print
              232  CALL_FUNCTION_0       0  ''
              234  POP_TOP          

 L. 480       236  POP_BLOCK        
              238  LOAD_CONST               None
              240  RETURN_VALUE     
            242_0  COME_FROM_FINALLY    28  '28'

 L. 481       242  DUP_TOP          
              244  LOAD_GLOBAL              KeyboardInterrupt
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   278  'to 278'
              252  POP_TOP          
              254  POP_TOP          
              256  POP_TOP          

 L. 482       258  LOAD_GLOBAL              printer
              260  LOAD_STR                 '\nCanceled by user.'
              262  LOAD_GLOBAL              FG
              264  LOAD_ATTR                WARNING
              266  LOAD_CONST               ('foreground',)
              268  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              270  POP_TOP          

 L. 483       272  POP_EXCEPT       
              274  LOAD_CONST               None
              276  RETURN_VALUE     
            278_0  COME_FROM           248  '248'
              278  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 142


__all__ = [
 'pick', 'entry', 'printer', 'billboard', 'cmd', 'credence', 'loading']