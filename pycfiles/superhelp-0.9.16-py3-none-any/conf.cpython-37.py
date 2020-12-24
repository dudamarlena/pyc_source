# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/g/projects/superhelp/build/lib/superhelp/conf.py
# Compiled at: 2020-04-18 17:22:06
# Size of source mod 2**32: 7209 bytes
import datetime, logging
from pathlib import Path
DEV_MODE = False
if DEV_MODE:
    print('\n\n\n    In DEV_MODE\n\n\n\n    ')
LOG_LEVEL = logging.DEBUG if DEV_MODE else logging.INFO
EXAMPLE_SNIPPET = 'def sorted(my_list):\n    sorted_list = my_list.sort()\n    return sorted_list\n'
TEST_SNIPPET = 'nums = set([1, 2])\n'
DEMO_SNIPPET = 'import datetime\nfrom math import pi as π\nmixed_keys = {1: \'cat\', \'1\': \'dog\'}\nmixedTypes = [\n    datetime.datetime.strptime(\'2020-02-10\', \'%Y-%m-%d\'),\n    π, 5, 1.234, \'Noor\', False,\n]\nnames = [\'Noor\', \'Grant\', \'Hyeji\', \'Vicky\', \'Olek\', \'Marzena\', \'Jess\', \'Nicole\']\nnames_lower = [name.lower() for name in names]\nname_lengths = []\nfor name in [\'Noor\', \'Grant\', ]:\n    name_lengths.append(len(name))\nfullName = \'Guido van Rossum\'\nevens_squared = [x**2 for x in range(1, 6) if x % 2 == 0]\nempty = []\nmyint = 666\nmyfloat = 6.667\nmyscinot = 1.23E-7\nmy_tup = (\'alpha\', \'beta\')\ngreeting = f"Hi {names[0]}!"\ngreeting = "Hi " + names[0] + "!"\ndef powerMe(num, *, power=2):\n    poweredVal = num ** power\n    return poweredVal\ncoord = (\'lat\', \'lon\')\nlatitude = coord[0]\nlongitude = coord[1]\nx, y = coord\npeople = set([\'Sam\', \'Avi\', \'Terri\', \'Noor\'])\nno_email = set([\'Sam\', \'Terri\'])\npeople2email = people - no_email\nempty_set = set()\nlen_word = len(fullName)\nif len_word == 1:\n    status = \'single-letter\'\nelif len_word < 4:\n    status = \'short\'\nelif len_word > 12:\n    status = \'long\'\nelif len_word > 20:\n    status = \'very_long\'\n# else:\n#     status = \'typical\'\nif len(\'chicken\') > 2:\n    print(\'cluck!\')\nphrase = "His age is %i" % 21\n\nfruit = [\'banana\']\ntry:\n    lunch = fruit[100]\nexcept (IndexError, TypeError):\n    print("No lunch for you!")\nexcept Exception as e:\n    print(f"Unknown error - details: {e}")\n\ntry:\n    float(\'boat\')\nexcept ValueError:\n    print("You can\'t float a boat! Only a number of some sort!")\n\ntry:\n    names[100]\nexcept Exception:\n    print(names)\n\nsorted_names = sorted(names)\nfaulty_val = names.sort()\n\n## modified and given more problems and features, from https://stackoverflow.com/questions/61154079/sorting-using-list-built-in-method-and-user-defined-function-sorts-the-list-with\ndef sorted(*G, **kwargs):\n    for i in range(len(G)):\n        for j in range(1,len(G)):\n            if G[j-1]<G[j]:\n                G[j-1],G[j]=G[j],G[j-1]\nG = [[\'Ahmad\', 3.8], [\'Rizwan\', 3.68], [\'Bilal\', 3.9]]\nsorted(G)\nprint(G)\n\nfrom functools import wraps\ndef tweet(func):\n    @wraps(func)\n    def wrapper(message):\n        func(message)\n        print(f"I\'m tweeting the message {message}")\n    return wrapper\n\n@tweet\ndef say(message):\n    print(message)\n\nsay("sausage!")\n\ndef has_docstring():\n    \'\'\'\n    Hi\n    \'\'\'\n    pass\ndef lacks_proper_docstring():\n    # Not a doc string\n    pass\ndef lacks_any_docstring():\n    666\n    name = \'Grant\'\n    \'\'\'\n    Ho\n    \'\'\'\ndef random():\n    \'\'\'\n    This is line 1\n    Line 2\n    Line 3\n    \'\'\'\n    pass\ndef camelCase(a, b, c, d, f, *, g):\n    \'\'\'\n    This is line 1\n    Line 2\n    Line 3\n    \'\'\'\n    pass\n'
AST_OUTPUT_XML = Path(__file__).parent / 'ast_output.xml'
PYTHON_CODE_START = '__python_code_start__'
PYTHON_CODE_END = '__python_code_end__'
MD_PYTHON_CODE_START = '::python'
BRIEF = 'Brief'
MAIN = 'Main'
EXTRA = 'Extra'
MESSAGE_LEVELS = [BRIEF, MAIN, EXTRA]
ANON_NAME = 'Anonymous'
INT_TYPE = 'int'
FLOAT_TYPE = 'float'
STR_TYPE = 'str'
DATETIME_TYPE = 'datetime'
BOOLEAN_TYPE = 'bool'
LIST_TYPE = 'list'
DICT_TYPE = 'dict'
TUPLE_TYPE = 'tuple'
TYPE2NAME = {INT_TYPE: 'integer', 
 FLOAT_TYPE: 'float', 
 STR_TYPE: 'string', 
 DATETIME_TYPE: 'datetime object', 
 BOOLEAN_TYPE: 'boolean', 
 LIST_TYPE: 'list', 
 DICT_TYPE: 'dict', 
 TUPLE_TYPE: 'tuple'}
EXAMPLES_OF_TYPES = {INT_TYPE: [123, 9, 17, 20, 100, 2020, 16], 
 FLOAT_TYPE: [1.2345, 0.667, 0.1, 0.001, 10.0], 
 STR_TYPE: ['apple', 'banana', 'kiwifruit', 'Auckland, New Zealand'], 
 DATETIME_TYPE: [
                 datetime.date(2020, 4, 4),
                 datetime.date(1066, 10, 14),
                 datetime.datetime.today()], 
 
 BOOLEAN_TYPE: [True, False], 
 LIST_TYPE: [[10, 2], [-3, 20], [44, -180]], 
 DICT_TYPE: [{'x':10,  'y':2}, {'x':-3,  'y':20}, {'x':44,  'y':-180}], 
 TUPLE_TYPE: [(10, 2), (-3, 20), (44, -180)]}
MAX_BRIEF_FUNC_LOC = 35
MAX_BRIEF_FUNC_ARGS = 6
MIN_BRIEF_DOCSTRING = 3
NO_ADVICE_MESSAGE = "No advice to give - looks fine :-). But if you think there should have been some advice given, contact grant@p-s.co.nz with the subject line 'Advice' and explain. Include a snippet to test as well."
SYSTEM_MESSAGE = 'System message'
LINE_FEED = '&#10;'
STD_LIBS = [
 '__future__', '__main__', '_dummy_thread', '_thread', 'aifc',
 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit',
 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2',
 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop',
 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser',
 'contextlib', 'contextvars', 'copy', 'copyreg', 'cProfile', 'crypt', 'csv',
 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib',
 'dis', 'distutils', 'doctest', 'dummy_threading', 'email', 'encodings',
 'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput',
 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools', 'gc', 'getopt',
 'getpass', 'gettext', 'glob', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html',
 'http', 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io', 'ipaddress',
 'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging',
 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap',
 'modulefinder', 'msilib', 'msvcrt', 'multiprocessing', 'netrc', 'nis',
 'nntplib', 'numbers', 'operator', 'optparse', 'os', 'ossaudiodev', 'parser',
 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform',
 'plistlib', 'poplib', 'posix', 'pprint', 'profile', 'pstats', 'pty', 'pwd',
 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 're', 'readline',
 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select',
 'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib',
 'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat',
 'statistics', 'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symbol',
 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib',
 'tempfile', 'termios', 'test', 'textwrap', 'threading', 'time', 'timeit',
 'tkinter', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty',
 'turtle', 'turtledemo', 'types', 'typing', 'unicodedata', 'unittest', 'urllib',
 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg',
 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile',
 'zipimport', 'zlib']