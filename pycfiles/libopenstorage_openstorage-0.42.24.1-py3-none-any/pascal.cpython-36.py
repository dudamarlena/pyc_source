# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/pascal.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 32621 bytes
"""
    pygments.lexers.pascal
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Pascal family languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, include, bygroups, words, using, this, default
from pygments.util import get_bool_opt, get_list_opt
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
from pygments.scanner import Scanner
from pygments.lexers.modula2 import Modula2Lexer
__all__ = [
 'DelphiLexer', 'AdaLexer']

class DelphiLexer(Lexer):
    __doc__ = '\n    For `Delphi <http://www.borland.com/delphi/>`_ (Borland Object Pascal),\n    Turbo Pascal and Free Pascal source code.\n\n    Additional options accepted:\n\n    `turbopascal`\n        Highlight Turbo Pascal specific keywords (default: ``True``).\n    `delphi`\n        Highlight Borland Delphi specific keywords (default: ``True``).\n    `freepascal`\n        Highlight Free Pascal specific keywords (default: ``True``).\n    `units`\n        A list of units that should be considered builtin, supported are\n        ``System``, ``SysUtils``, ``Classes`` and ``Math``.\n        Default is to consider all of them builtin.\n    '
    name = 'Delphi'
    aliases = ['delphi', 'pas', 'pascal', 'objectpascal']
    filenames = ['*.pas', '*.dpr']
    mimetypes = ['text/x-pascal']
    TURBO_PASCAL_KEYWORDS = ('absolute', 'and', 'array', 'asm', 'begin', 'break', 'case',
                             'const', 'constructor', 'continue', 'destructor', 'div',
                             'do', 'downto', 'else', 'end', 'file', 'for', 'function',
                             'goto', 'if', 'implementation', 'in', 'inherited', 'inline',
                             'interface', 'label', 'mod', 'nil', 'not', 'object',
                             'of', 'on', 'operator', 'or', 'packed', 'procedure',
                             'program', 'record', 'reintroduce', 'repeat', 'self',
                             'set', 'shl', 'shr', 'string', 'then', 'to', 'type',
                             'unit', 'until', 'uses', 'var', 'while', 'with', 'xor')
    DELPHI_KEYWORDS = ('as', 'class', 'except', 'exports', 'finalization', 'finally',
                       'initialization', 'is', 'library', 'on', 'property', 'raise',
                       'threadvar', 'try')
    FREE_PASCAL_KEYWORDS = ('dispose', 'exit', 'false', 'new', 'true')
    BLOCK_KEYWORDS = {
     'begin', 'class', 'const', 'constructor', 'destructor', 'end',
     'finalization', 'function', 'implementation', 'initialization',
     'label', 'library', 'operator', 'procedure', 'program', 'property',
     'record', 'threadvar', 'type', 'unit', 'uses', 'var'}
    FUNCTION_MODIFIERS = {
     'alias', 'cdecl', 'export', 'inline', 'interrupt', 'nostackframe',
     'pascal', 'register', 'safecall', 'softfloat', 'stdcall',
     'varargs', 'name', 'dynamic', 'near', 'virtual', 'external',
     'override', 'assembler'}
    DIRECTIVES = {
     'absolute', 'abstract', 'assembler', 'cppdecl', 'default', 'far',
     'far16', 'forward', 'index', 'oldfpccall', 'private', 'protected',
     'published', 'public'}
    BUILTIN_TYPES = {
     'ansichar', 'ansistring', 'bool', 'boolean', 'byte', 'bytebool',
     'cardinal', 'char', 'comp', 'currency', 'double', 'dword',
     'extended', 'int64', 'integer', 'iunknown', 'longbool', 'longint',
     'longword', 'pansichar', 'pansistring', 'pbool', 'pboolean',
     'pbyte', 'pbytearray', 'pcardinal', 'pchar', 'pcomp', 'pcurrency',
     'pdate', 'pdatetime', 'pdouble', 'pdword', 'pextended', 'phandle',
     'pint64', 'pinteger', 'plongint', 'plongword', 'pointer',
     'ppointer', 'pshortint', 'pshortstring', 'psingle', 'psmallint',
     'pstring', 'pvariant', 'pwidechar', 'pwidestring', 'pword',
     'pwordarray', 'pwordbool', 'real', 'real48', 'shortint',
     'shortstring', 'single', 'smallint', 'string', 'tclass', 'tdate',
     'tdatetime', 'textfile', 'thandle', 'tobject', 'ttime', 'variant',
     'widechar', 'widestring', 'word', 'wordbool'}
    BUILTIN_UNITS = {'System':('abs', 'acquireexceptionobject', 'addr', 'ansitoutf8', 'append', 'arctan', 'assert',
 'assigned', 'assignfile', 'beginthread', 'blockread', 'blockwrite', 'break', 'chdir',
 'chr', 'close', 'closefile', 'comptocurrency', 'comptodouble', 'concat', 'continue',
 'copy', 'cos', 'dec', 'delete', 'dispose', 'doubletocomp', 'endthread', 'enummodules',
 'enumresourcemodules', 'eof', 'eoln', 'erase', 'exceptaddr', 'exceptobject', 'exclude',
 'exit', 'exp', 'filepos', 'filesize', 'fillchar', 'finalize', 'findclasshinstance',
 'findhinstance', 'findresourcehinstance', 'flush', 'frac', 'freemem', 'get8087cw',
 'getdir', 'getlasterror', 'getmem', 'getmemorymanager', 'getmodulefilename', 'getvariantmanager',
 'halt', 'hi', 'high', 'inc', 'include', 'initialize', 'insert', 'int', 'ioresult',
 'ismemorymanagerset', 'isvariantmanagerset', 'length', 'ln', 'lo', 'low', 'mkdir',
 'move', 'new', 'odd', 'olestrtostring', 'olestrtostrvar', 'ord', 'paramcount', 'paramstr',
 'pi', 'pos', 'pred', 'ptr', 'pucs4chars', 'random', 'randomize', 'read', 'readln',
 'reallocmem', 'releaseexceptionobject', 'rename', 'reset', 'rewrite', 'rmdir', 'round',
 'runerror', 'seek', 'seekeof', 'seekeoln', 'set8087cw', 'setlength', 'setlinebreakstyle',
 'setmemorymanager', 'setstring', 'settextbuf', 'setvariantmanager', 'sin', 'sizeof',
 'slice', 'sqr', 'sqrt', 'str', 'stringofchar', 'stringtoolestr', 'stringtowidechar',
 'succ', 'swap', 'trunc', 'truncate', 'typeinfo', 'ucs4stringtowidestring', 'unicodetoutf8',
 'uniquestring', 'upcase', 'utf8decode', 'utf8encode', 'utf8toansi', 'utf8tounicode',
 'val', 'vararrayredim', 'varclear', 'widecharlentostring', 'widecharlentostrvar',
 'widechartostring', 'widechartostrvar', 'widestringtoucs4string', 'write', 'writeln'), 
     'SysUtils':('abort', 'addexitproc', 'addterminateproc', 'adjustlinebreaks', 'allocmem', 'ansicomparefilename',
 'ansicomparestr', 'ansicomparetext', 'ansidequotedstr', 'ansiextractquotedstr',
 'ansilastchar', 'ansilowercase', 'ansilowercasefilename', 'ansipos', 'ansiquotedstr',
 'ansisamestr', 'ansisametext', 'ansistrcomp', 'ansistricomp', 'ansistrlastchar',
 'ansistrlcomp', 'ansistrlicomp', 'ansistrlower', 'ansistrpos', 'ansistrrscan', 'ansistrscan',
 'ansistrupper', 'ansiuppercase', 'ansiuppercasefilename', 'appendstr', 'assignstr',
 'beep', 'booltostr', 'bytetocharindex', 'bytetocharlen', 'bytetype', 'callterminateprocs',
 'changefileext', 'charlength', 'chartobyteindex', 'chartobytelen', 'comparemem',
 'comparestr', 'comparetext', 'createdir', 'createguid', 'currentyear', 'currtostr',
 'currtostrf', 'date', 'datetimetofiledate', 'datetimetostr', 'datetimetostring',
 'datetimetosystemtime', 'datetimetotimestamp', 'datetostr', 'dayofweek', 'decodedate',
 'decodedatefully', 'decodetime', 'deletefile', 'directoryexists', 'diskfree', 'disksize',
 'disposestr', 'encodedate', 'encodetime', 'exceptionerrormessage', 'excludetrailingbackslash',
 'excludetrailingpathdelimiter', 'expandfilename', 'expandfilenamecase', 'expanduncfilename',
 'extractfiledir', 'extractfiledrive', 'extractfileext', 'extractfilename', 'extractfilepath',
 'extractrelativepath', 'extractshortpathname', 'fileage', 'fileclose', 'filecreate',
 'filedatetodatetime', 'fileexists', 'filegetattr', 'filegetdate', 'fileisreadonly',
 'fileopen', 'fileread', 'filesearch', 'fileseek', 'filesetattr', 'filesetdate',
 'filesetreadonly', 'filewrite', 'finalizepackage', 'findclose', 'findcmdlineswitch',
 'findfirst', 'findnext', 'floattocurr', 'floattodatetime', 'floattodecimal', 'floattostr',
 'floattostrf', 'floattotext', 'floattotextfmt', 'fmtloadstr', 'fmtstr', 'forcedirectories',
 'format', 'formatbuf', 'formatcurr', 'formatdatetime', 'formatfloat', 'freeandnil',
 'getcurrentdir', 'getenvironmentvariable', 'getfileversion', 'getformatsettings',
 'getlocaleformatsettings', 'getmodulename', 'getpackagedescription', 'getpackageinfo',
 'gettime', 'guidtostring', 'incamonth', 'includetrailingbackslash', 'includetrailingpathdelimiter',
 'incmonth', 'initializepackage', 'interlockeddecrement', 'interlockedexchange',
 'interlockedexchangeadd', 'interlockedincrement', 'inttohex', 'inttostr', 'isdelimiter',
 'isequalguid', 'isleapyear', 'ispathdelimiter', 'isvalidident', 'languages', 'lastdelimiter',
 'loadpackage', 'loadstr', 'lowercase', 'msecstotimestamp', 'newstr', 'nextcharindex',
 'now', 'outofmemoryerror', 'quotedstr', 'raiselastoserror', 'raiselastwin32error',
 'removedir', 'renamefile', 'replacedate', 'replacetime', 'safeloadlibrary', 'samefilename',
 'sametext', 'setcurrentdir', 'showexception', 'sleep', 'stralloc', 'strbufsize',
 'strbytetype', 'strcat', 'strcharlength', 'strcomp', 'strcopy', 'strdispose', 'strecopy',
 'strend', 'strfmt', 'stricomp', 'stringreplace', 'stringtoguid', 'strlcat', 'strlcomp',
 'strlcopy', 'strlen', 'strlfmt', 'strlicomp', 'strlower', 'strmove', 'strnew', 'strnextchar',
 'strpas', 'strpcopy', 'strplcopy', 'strpos', 'strrscan', 'strscan', 'strtobool',
 'strtobooldef', 'strtocurr', 'strtocurrdef', 'strtodate', 'strtodatedef', 'strtodatetime',
 'strtodatetimedef', 'strtofloat', 'strtofloatdef', 'strtoint', 'strtoint64', 'strtoint64def',
 'strtointdef', 'strtotime', 'strtotimedef', 'strupper', 'supports', 'syserrormessage',
 'systemtimetodatetime', 'texttofloat', 'time', 'timestamptodatetime', 'timestamptomsecs',
 'timetostr', 'trim', 'trimleft', 'trimright', 'tryencodedate', 'tryencodetime',
 'tryfloattocurr', 'tryfloattodatetime', 'trystrtobool', 'trystrtocurr', 'trystrtodate',
 'trystrtodatetime', 'trystrtofloat', 'trystrtoint', 'trystrtoint64', 'trystrtotime',
 'unloadpackage', 'uppercase', 'widecomparestr', 'widecomparetext', 'widefmtstr',
 'wideformat', 'wideformatbuf', 'widelowercase', 'widesamestr', 'widesametext', 'wideuppercase',
 'win32check', 'wraptext'), 
     'Classes':('activateclassgroup', 'allocatehwnd', 'bintohex', 'checksynchronize', 'collectionsequal',
 'countgenerations', 'deallocatehwnd', 'equalrect', 'extractstrings', 'findclass',
 'findglobalcomponent', 'getclass', 'groupdescendantswith', 'hextobin', 'identtoint',
 'initinheritedcomponent', 'inttoident', 'invalidpoint', 'isuniqueglobalcomponentname',
 'linestart', 'objectbinarytotext', 'objectresourcetotext', 'objecttexttobinary',
 'objecttexttoresource', 'pointsequal', 'readcomponentres', 'readcomponentresex',
 'readcomponentresfile', 'rect', 'registerclass', 'registerclassalias', 'registerclasses',
 'registercomponents', 'registerintegerconsts', 'registernoicon', 'registernonactivex',
 'smallpoint', 'startclassgroup', 'teststreamformat', 'unregisterclass', 'unregisterclasses',
 'unregisterintegerconsts', 'unregistermoduleclasses', 'writecomponentresfile'), 
     'Math':('arccos', 'arccosh', 'arccot', 'arccoth', 'arccsc', 'arccsch', 'arcsec', 'arcsech',
 'arcsin', 'arcsinh', 'arctan2', 'arctanh', 'ceil', 'comparevalue', 'cosecant', 'cosh',
 'cot', 'cotan', 'coth', 'csc', 'csch', 'cycletodeg', 'cycletograd', 'cycletorad',
 'degtocycle', 'degtograd', 'degtorad', 'divmod', 'doubledecliningbalance', 'ensurerange',
 'floor', 'frexp', 'futurevalue', 'getexceptionmask', 'getprecisionmode', 'getroundmode',
 'gradtocycle', 'gradtodeg', 'gradtorad', 'hypot', 'inrange', 'interestpayment',
 'interestrate', 'internalrateofreturn', 'intpower', 'isinfinite', 'isnan', 'iszero',
 'ldexp', 'lnxp1', 'log10', 'log2', 'logn', 'max', 'maxintvalue', 'maxvalue', 'mean',
 'meanandstddev', 'min', 'minintvalue', 'minvalue', 'momentskewkurtosis', 'netpresentvalue',
 'norm', 'numberofperiods', 'payment', 'periodpayment', 'poly', 'popnstddev', 'popnvariance',
 'power', 'presentvalue', 'radtocycle', 'radtodeg', 'radtograd', 'randg', 'randomrange',
 'roundto', 'samevalue', 'sec', 'secant', 'sech', 'setexceptionmask', 'setprecisionmode',
 'setroundmode', 'sign', 'simpleroundto', 'sincos', 'sinh', 'slndepreciation', 'stddev',
 'sum', 'sumint', 'sumofsquares', 'sumsandsquares', 'syddepreciation', 'tan', 'tanh',
 'totalvariance', 'variance')}
    ASM_REGISTERS = {
     'ah', 'al', 'ax', 'bh', 'bl', 'bp', 'bx', 'ch', 'cl', 'cr0',
     'cr1', 'cr2', 'cr3', 'cr4', 'cs', 'cx', 'dh', 'di', 'dl', 'dr0',
     'dr1', 'dr2', 'dr3', 'dr4', 'dr5', 'dr6', 'dr7', 'ds', 'dx',
     'eax', 'ebp', 'ebx', 'ecx', 'edi', 'edx', 'es', 'esi', 'esp',
     'fs', 'gs', 'mm0', 'mm1', 'mm2', 'mm3', 'mm4', 'mm5', 'mm6',
     'mm7', 'si', 'sp', 'ss', 'st0', 'st1', 'st2', 'st3', 'st4', 'st5',
     'st6', 'st7', 'xmm0', 'xmm1', 'xmm2', 'xmm3', 'xmm4', 'xmm5',
     'xmm6', 'xmm7'}
    ASM_INSTRUCTIONS = {
     'aaa', 'aad', 'aam', 'aas', 'adc', 'add', 'and', 'arpl', 'bound',
     'bsf', 'bsr', 'bswap', 'bt', 'btc', 'btr', 'bts', 'call', 'cbw',
     'cdq', 'clc', 'cld', 'cli', 'clts', 'cmc', 'cmova', 'cmovae',
     'cmovb', 'cmovbe', 'cmovc', 'cmovcxz', 'cmove', 'cmovg',
     'cmovge', 'cmovl', 'cmovle', 'cmovna', 'cmovnae', 'cmovnb',
     'cmovnbe', 'cmovnc', 'cmovne', 'cmovng', 'cmovnge', 'cmovnl',
     'cmovnle', 'cmovno', 'cmovnp', 'cmovns', 'cmovnz', 'cmovo',
     'cmovp', 'cmovpe', 'cmovpo', 'cmovs', 'cmovz', 'cmp', 'cmpsb',
     'cmpsd', 'cmpsw', 'cmpxchg', 'cmpxchg486', 'cmpxchg8b', 'cpuid',
     'cwd', 'cwde', 'daa', 'das', 'dec', 'div', 'emms', 'enter', 'hlt',
     'ibts', 'icebp', 'idiv', 'imul', 'in', 'inc', 'insb', 'insd',
     'insw', 'int', 'int01', 'int03', 'int1', 'int3', 'into', 'invd',
     'invlpg', 'iret', 'iretd', 'iretw', 'ja', 'jae', 'jb', 'jbe',
     'jc', 'jcxz', 'jcxz', 'je', 'jecxz', 'jg', 'jge', 'jl', 'jle',
     'jmp', 'jna', 'jnae', 'jnb', 'jnbe', 'jnc', 'jne', 'jng', 'jnge',
     'jnl', 'jnle', 'jno', 'jnp', 'jns', 'jnz', 'jo', 'jp', 'jpe',
     'jpo', 'js', 'jz', 'lahf', 'lar', 'lcall', 'lds', 'lea', 'leave',
     'les', 'lfs', 'lgdt', 'lgs', 'lidt', 'ljmp', 'lldt', 'lmsw',
     'loadall', 'loadall286', 'lock', 'lodsb', 'lodsd', 'lodsw',
     'loop', 'loope', 'loopne', 'loopnz', 'loopz', 'lsl', 'lss', 'ltr',
     'mov', 'movd', 'movq', 'movsb', 'movsd', 'movsw', 'movsx',
     'movzx', 'mul', 'neg', 'nop', 'not', 'or', 'out', 'outsb', 'outsd',
     'outsw', 'pop', 'popa', 'popad', 'popaw', 'popf', 'popfd', 'popfw',
     'push', 'pusha', 'pushad', 'pushaw', 'pushf', 'pushfd', 'pushfw',
     'rcl', 'rcr', 'rdmsr', 'rdpmc', 'rdshr', 'rdtsc', 'rep', 'repe',
     'repne', 'repnz', 'repz', 'ret', 'retf', 'retn', 'rol', 'ror',
     'rsdc', 'rsldt', 'rsm', 'sahf', 'sal', 'salc', 'sar', 'sbb',
     'scasb', 'scasd', 'scasw', 'seta', 'setae', 'setb', 'setbe',
     'setc', 'setcxz', 'sete', 'setg', 'setge', 'setl', 'setle',
     'setna', 'setnae', 'setnb', 'setnbe', 'setnc', 'setne', 'setng',
     'setnge', 'setnl', 'setnle', 'setno', 'setnp', 'setns', 'setnz',
     'seto', 'setp', 'setpe', 'setpo', 'sets', 'setz', 'sgdt', 'shl',
     'shld', 'shr', 'shrd', 'sidt', 'sldt', 'smi', 'smint', 'smintold',
     'smsw', 'stc', 'std', 'sti', 'stosb', 'stosd', 'stosw', 'str',
     'sub', 'svdc', 'svldt', 'svts', 'syscall', 'sysenter', 'sysexit',
     'sysret', 'test', 'ud1', 'ud2', 'umov', 'verr', 'verw', 'wait',
     'wbinvd', 'wrmsr', 'wrshr', 'xadd', 'xbts', 'xchg', 'xlat',
     'xlatb', 'xor'}

    def __init__(self, **options):
        (Lexer.__init__)(self, **options)
        self.keywords = set()
        if get_bool_opt(options, 'turbopascal', True):
            self.keywords.update(self.TURBO_PASCAL_KEYWORDS)
        if get_bool_opt(options, 'delphi', True):
            self.keywords.update(self.DELPHI_KEYWORDS)
        if get_bool_opt(options, 'freepascal', True):
            self.keywords.update(self.FREE_PASCAL_KEYWORDS)
        self.builtins = set()
        for unit in get_list_opt(options, 'units', list(self.BUILTIN_UNITS)):
            self.builtins.update(self.BUILTIN_UNITS[unit])

    def get_tokens_unprocessed--- This code section failed: ---

 L. 315         0  LOAD_GLOBAL              Scanner
                2  LOAD_FAST                'text'
                4  LOAD_GLOBAL              re
                6  LOAD_ATTR                DOTALL
                8  LOAD_GLOBAL              re
               10  LOAD_ATTR                MULTILINE
               12  BINARY_OR        
               14  LOAD_GLOBAL              re
               16  LOAD_ATTR                IGNORECASE
               18  BINARY_OR        
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  STORE_FAST               'scanner'

 L. 316        24  LOAD_STR                 'initial'
               26  BUILD_LIST_1          1 
               28  STORE_FAST               'stack'

 L. 317        30  LOAD_CONST               False
               32  STORE_FAST               'in_function_block'

 L. 318        34  LOAD_CONST               False
               36  STORE_FAST               'in_property_block'

 L. 319        38  LOAD_CONST               False
               40  STORE_FAST               'was_dot'

 L. 320        42  LOAD_CONST               False
               44  STORE_FAST               'next_token_is_function'

 L. 321        46  LOAD_CONST               False
               48  STORE_FAST               'next_token_is_property'

 L. 322        50  LOAD_CONST               False
               52  STORE_FAST               'collect_labels'

 L. 323        54  LOAD_GLOBAL              set
               56  CALL_FUNCTION_0       0  '0 positional arguments'
               58  STORE_FAST               'block_labels'

 L. 324        60  LOAD_CONST               0
               62  LOAD_CONST               0
               64  BUILD_LIST_2          2 
               66  STORE_FAST               'brace_balance'

 L. 326        68  SETUP_LOOP         1446  'to 1446'
               72  LOAD_FAST                'scanner'
               74  LOAD_ATTR                eos
               76  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 327        80  LOAD_GLOBAL              Error
               82  STORE_FAST               'token'

 L. 329        84  LOAD_FAST                'stack'
               86  LOAD_CONST               -1
               88  BINARY_SUBSCR    
               90  LOAD_STR                 'initial'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   950  'to 950'

 L. 330        98  LOAD_FAST                'scanner'
              100  LOAD_ATTR                scan
              102  LOAD_STR                 '\\s+'
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  POP_JUMP_IF_FALSE   116  'to 116'

 L. 331       108  LOAD_GLOBAL              Text
              110  STORE_FAST               'token'
              112  JUMP_ABSOLUTE      1398  'to 1398'
              116  ELSE                     '948'

 L. 332       116  LOAD_FAST                'scanner'
              118  LOAD_ATTR                scan
              120  LOAD_STR                 '\\{.*?\\}|\\(\\*.*?\\*\\)'
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  POP_JUMP_IF_FALSE   156  'to 156'

 L. 333       126  LOAD_FAST                'scanner'
              128  LOAD_ATTR                match
              130  LOAD_ATTR                startswith
              132  LOAD_STR                 '$'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  POP_JUMP_IF_FALSE   146  'to 146'

 L. 334       138  LOAD_GLOBAL              Comment
              140  LOAD_ATTR                Preproc
              142  STORE_FAST               'token'
              144  JUMP_FORWARD        152  'to 152'
              146  ELSE                     '152'

 L. 336       146  LOAD_GLOBAL              Comment
              148  LOAD_ATTR                Multiline
              150  STORE_FAST               'token'
            152_0  COME_FROM           144  '144'
              152  JUMP_ABSOLUTE      1398  'to 1398'
              156  ELSE                     '948'

 L. 337       156  LOAD_FAST                'scanner'
              158  LOAD_ATTR                scan
              160  LOAD_STR                 '//.*?$'
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  POP_JUMP_IF_FALSE   176  'to 176'

 L. 338       166  LOAD_GLOBAL              Comment
              168  LOAD_ATTR                Single
              170  STORE_FAST               'token'
              172  JUMP_ABSOLUTE      1398  'to 1398'
              176  ELSE                     '948'

 L. 339       176  LOAD_FAST                'scanner'
              178  LOAD_ATTR                scan
              180  LOAD_STR                 '[-+*\\/=<>:;,.@\\^]'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  POP_JUMP_IF_FALSE   212  'to 212'

 L. 340       186  LOAD_GLOBAL              Operator
              188  STORE_FAST               'token'

 L. 342       190  LOAD_FAST                'collect_labels'
              192  POP_JUMP_IF_FALSE   208  'to 208'
              194  LOAD_FAST                'scanner'
              196  LOAD_ATTR                match
              198  LOAD_STR                 ';'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   208  'to 208'

 L. 343       204  LOAD_CONST               False
              206  STORE_FAST               'collect_labels'
            208_0  COME_FROM           202  '202'
            208_1  COME_FROM           192  '192'
              208  JUMP_ABSOLUTE      1398  'to 1398'
              212  ELSE                     '948'

 L. 344       212  LOAD_FAST                'scanner'
              214  LOAD_ATTR                scan
              216  LOAD_STR                 '[\\(\\)\\[\\]]+'
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  POP_JUMP_IF_FALSE   364  'to 364'

 L. 345       224  LOAD_GLOBAL              Punctuation
              226  STORE_FAST               'token'

 L. 347       228  LOAD_CONST               False
              230  STORE_FAST               'next_token_is_function'

 L. 351       232  LOAD_FAST                'in_function_block'
              234  POP_JUMP_IF_TRUE    242  'to 242'
              236  LOAD_FAST                'in_property_block'
            238_0  COME_FROM           234  '234'
              238  POP_JUMP_IF_FALSE   946  'to 946'

 L. 352       242  LOAD_FAST                'scanner'
              244  LOAD_ATTR                match
              246  LOAD_STR                 '('
              248  COMPARE_OP               ==
              250  POP_JUMP_IF_FALSE   272  'to 272'

 L. 353       254  LOAD_FAST                'brace_balance'
              256  LOAD_CONST               0
              258  DUP_TOP_TWO      
              260  BINARY_SUBSCR    
              262  LOAD_CONST               1
              264  INPLACE_ADD      
              266  ROT_THREE        
              268  STORE_SUBSCR     
              270  JUMP_FORWARD        360  'to 360'
              272  ELSE                     '360'

 L. 354       272  LOAD_FAST                'scanner'
              274  LOAD_ATTR                match
              276  LOAD_STR                 ')'
              278  COMPARE_OP               ==
              280  POP_JUMP_IF_FALSE   302  'to 302'

 L. 355       284  LOAD_FAST                'brace_balance'
              286  LOAD_CONST               0
              288  DUP_TOP_TWO      
              290  BINARY_SUBSCR    
              292  LOAD_CONST               1
              294  INPLACE_SUBTRACT 
              296  ROT_THREE        
              298  STORE_SUBSCR     
              300  JUMP_FORWARD        360  'to 360'
              302  ELSE                     '360'

 L. 356       302  LOAD_FAST                'scanner'
              304  LOAD_ATTR                match
              306  LOAD_STR                 '['
              308  COMPARE_OP               ==
              310  POP_JUMP_IF_FALSE   332  'to 332'

 L. 357       314  LOAD_FAST                'brace_balance'
              316  LOAD_CONST               1
              318  DUP_TOP_TWO      
              320  BINARY_SUBSCR    
              322  LOAD_CONST               1
              324  INPLACE_ADD      
              326  ROT_THREE        
              328  STORE_SUBSCR     
              330  JUMP_FORWARD        360  'to 360'
              332  ELSE                     '360'

 L. 358       332  LOAD_FAST                'scanner'
              334  LOAD_ATTR                match
              336  LOAD_STR                 ']'
              338  COMPARE_OP               ==
              340  POP_JUMP_IF_FALSE   946  'to 946'

 L. 359       344  LOAD_FAST                'brace_balance'
              346  LOAD_CONST               1
              348  DUP_TOP_TWO      
              350  BINARY_SUBSCR    
              352  LOAD_CONST               1
              354  INPLACE_SUBTRACT 
              356  ROT_THREE        
              358  STORE_SUBSCR     
            360_0  COME_FROM           330  '330'
            360_1  COME_FROM           300  '300'
            360_2  COME_FROM           270  '270'
              360  JUMP_ABSOLUTE      1398  'to 1398'
              364  ELSE                     '948'

 L. 360       364  LOAD_FAST                'scanner'
              366  LOAD_ATTR                scan
              368  LOAD_STR                 '[A-Za-z_][A-Za-z_0-9]*'
              370  CALL_FUNCTION_1       1  '1 positional argument'
              372  POP_JUMP_IF_FALSE   808  'to 808'

 L. 361       376  LOAD_FAST                'scanner'
              378  LOAD_ATTR                match
              380  LOAD_ATTR                lower
              382  CALL_FUNCTION_0       0  '0 positional arguments'
              384  STORE_FAST               'lowercase_name'

 L. 362       386  LOAD_FAST                'lowercase_name'
              388  LOAD_STR                 'result'
              390  COMPARE_OP               ==
              392  POP_JUMP_IF_FALSE   408  'to 408'

 L. 363       396  LOAD_GLOBAL              Name
              398  LOAD_ATTR                Builtin
              400  LOAD_ATTR                Pseudo
              402  STORE_FAST               'token'
              404  JUMP_ABSOLUTE       946  'to 946'
              408  ELSE                     '806'

 L. 364       408  LOAD_FAST                'lowercase_name'
              410  LOAD_FAST                'self'
              412  LOAD_ATTR                keywords
              414  COMPARE_OP               in
              416  POP_JUMP_IF_FALSE   576  'to 576'

 L. 365       420  LOAD_GLOBAL              Keyword
              422  STORE_FAST               'token'

 L. 369       424  LOAD_FAST                'in_function_block'
              426  POP_JUMP_IF_TRUE    436  'to 436'
              430  LOAD_FAST                'in_property_block'
            432_0  COME_FROM           426  '426'
              432  POP_JUMP_IF_FALSE   498  'to 498'

 L. 370       436  LOAD_FAST                'lowercase_name'
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                BLOCK_KEYWORDS
              442  COMPARE_OP               in
              444  POP_JUMP_IF_FALSE   498  'to 498'

 L. 371       448  LOAD_FAST                'brace_balance'
              450  LOAD_CONST               0
              452  BINARY_SUBSCR    
              454  LOAD_CONST               0
              456  COMPARE_OP               <=
              458  POP_JUMP_IF_FALSE   498  'to 498'

 L. 372       462  LOAD_FAST                'brace_balance'
              464  LOAD_CONST               1
              466  BINARY_SUBSCR    
              468  LOAD_CONST               0
              470  COMPARE_OP               <=
              472  POP_JUMP_IF_FALSE   498  'to 498'

 L. 373       476  LOAD_CONST               False
              478  STORE_FAST               'in_function_block'

 L. 374       480  LOAD_CONST               False
              482  STORE_FAST               'in_property_block'

 L. 375       484  LOAD_CONST               0
              486  LOAD_CONST               0
              488  BUILD_LIST_2          2 
              490  STORE_FAST               'brace_balance'

 L. 376       492  LOAD_GLOBAL              set
              494  CALL_FUNCTION_0       0  '0 positional arguments'
              496  STORE_FAST               'block_labels'
            498_0  COME_FROM           472  '472'
            498_1  COME_FROM           458  '458'
            498_2  COME_FROM           444  '444'
            498_3  COME_FROM           432  '432'

 L. 377       498  LOAD_FAST                'lowercase_name'
              500  LOAD_CONST               ('label', 'goto')
              502  COMPARE_OP               in
              504  POP_JUMP_IF_FALSE   514  'to 514'

 L. 378       508  LOAD_CONST               True
              510  STORE_FAST               'collect_labels'
              512  JUMP_FORWARD        574  'to 574'
              514  ELSE                     '574'

 L. 379       514  LOAD_FAST                'lowercase_name'
              516  LOAD_STR                 'asm'
              518  COMPARE_OP               ==
              520  POP_JUMP_IF_FALSE   536  'to 536'

 L. 380       524  LOAD_FAST                'stack'
              526  LOAD_ATTR                append
              528  LOAD_STR                 'asm'
              530  CALL_FUNCTION_1       1  '1 positional argument'
              532  POP_TOP          
              534  JUMP_FORWARD        574  'to 574'
              536  ELSE                     '574'

 L. 381       536  LOAD_FAST                'lowercase_name'
              538  LOAD_STR                 'property'
              540  COMPARE_OP               ==
              542  POP_JUMP_IF_FALSE   556  'to 556'

 L. 382       546  LOAD_CONST               True
              548  STORE_FAST               'in_property_block'

 L. 383       550  LOAD_CONST               True
              552  STORE_FAST               'next_token_is_property'
              554  JUMP_FORWARD        574  'to 574'
              556  ELSE                     '574'

 L. 384       556  LOAD_FAST                'lowercase_name'

 L. 386       558  LOAD_CONST               ('procedure', 'operator', 'function', 'constructor', 'destructor')
              560  COMPARE_OP               in
              562  POP_JUMP_IF_FALSE   806  'to 806'

 L. 387       566  LOAD_CONST               True
              568  STORE_FAST               'in_function_block'

 L. 388       570  LOAD_CONST               True
              572  STORE_FAST               'next_token_is_function'
            574_0  COME_FROM           554  '554'
            574_1  COME_FROM           534  '534'
            574_2  COME_FROM           512  '512'
              574  JUMP_FORWARD        806  'to 806'
              576  ELSE                     '806'

 L. 392       576  LOAD_FAST                'in_function_block'
              578  POP_JUMP_IF_FALSE   602  'to 602'

 L. 393       582  LOAD_FAST                'lowercase_name'
              584  LOAD_FAST                'self'
              586  LOAD_ATTR                FUNCTION_MODIFIERS
              588  COMPARE_OP               in
              590  POP_JUMP_IF_FALSE   602  'to 602'

 L. 394       594  LOAD_GLOBAL              Keyword
              596  LOAD_ATTR                Pseudo
              598  STORE_FAST               'token'
              600  JUMP_FORWARD        806  'to 806'
            602_0  COME_FROM           578  '578'

 L. 397       602  LOAD_FAST                'in_property_block'
              604  POP_JUMP_IF_FALSE   630  'to 630'

 L. 398       608  LOAD_FAST                'lowercase_name'
              610  LOAD_CONST               ('read', 'write')
              612  COMPARE_OP               in
              614  POP_JUMP_IF_FALSE   630  'to 630'

 L. 399       618  LOAD_GLOBAL              Keyword
              620  LOAD_ATTR                Pseudo
              622  STORE_FAST               'token'

 L. 400       624  LOAD_CONST               True
              626  STORE_FAST               'next_token_is_function'
              628  JUMP_FORWARD        806  'to 806'
            630_0  COME_FROM           604  '604'

 L. 404       630  LOAD_FAST                'next_token_is_function'
              632  POP_JUMP_IF_FALSE   668  'to 668'

 L. 408       636  LOAD_FAST                'scanner'
              638  LOAD_ATTR                test
              640  LOAD_STR                 '\\s*\\.\\s*'
              642  CALL_FUNCTION_1       1  '1 positional argument'
              644  POP_JUMP_IF_FALSE   656  'to 656'

 L. 409       648  LOAD_GLOBAL              Name
              650  LOAD_ATTR                Class
              652  STORE_FAST               'token'
              654  JUMP_FORWARD        666  'to 666'
              656  ELSE                     '666'

 L. 412       656  LOAD_GLOBAL              Name
              658  LOAD_ATTR                Function
              660  STORE_FAST               'token'

 L. 413       662  LOAD_CONST               False
              664  STORE_FAST               'next_token_is_function'
            666_0  COME_FROM           654  '654'
              666  JUMP_FORWARD        806  'to 806'
              668  ELSE                     '806'

 L. 415       668  LOAD_FAST                'next_token_is_property'
              670  POP_JUMP_IF_FALSE   686  'to 686'

 L. 416       674  LOAD_GLOBAL              Name
              676  LOAD_ATTR                Property
              678  STORE_FAST               'token'

 L. 417       680  LOAD_CONST               False
              682  STORE_FAST               'next_token_is_property'
              684  JUMP_FORWARD        806  'to 806'
              686  ELSE                     '806'

 L. 420       686  LOAD_FAST                'collect_labels'
              688  POP_JUMP_IF_FALSE   716  'to 716'

 L. 421       692  LOAD_GLOBAL              Name
              694  LOAD_ATTR                Label
              696  STORE_FAST               'token'

 L. 422       698  LOAD_FAST                'block_labels'
              700  LOAD_ATTR                add
              702  LOAD_FAST                'scanner'
              704  LOAD_ATTR                match
              706  LOAD_ATTR                lower
              708  CALL_FUNCTION_0       0  '0 positional arguments'
              710  CALL_FUNCTION_1       1  '1 positional argument'
              712  POP_TOP          
              714  JUMP_FORWARD        806  'to 806'
              716  ELSE                     '806'

 L. 424       716  LOAD_FAST                'lowercase_name'
              718  LOAD_FAST                'block_labels'
              720  COMPARE_OP               in
              722  POP_JUMP_IF_FALSE   734  'to 734'

 L. 425       726  LOAD_GLOBAL              Name
              728  LOAD_ATTR                Label
              730  STORE_FAST               'token'
              732  JUMP_FORWARD        806  'to 806'
              734  ELSE                     '806'

 L. 426       734  LOAD_FAST                'lowercase_name'
              736  LOAD_FAST                'self'
              738  LOAD_ATTR                BUILTIN_TYPES
              740  COMPARE_OP               in
              742  POP_JUMP_IF_FALSE   754  'to 754'

 L. 427       746  LOAD_GLOBAL              Keyword
              748  LOAD_ATTR                Type
              750  STORE_FAST               'token'
              752  JUMP_FORWARD        806  'to 806'
              754  ELSE                     '806'

 L. 428       754  LOAD_FAST                'lowercase_name'
              756  LOAD_FAST                'self'
              758  LOAD_ATTR                DIRECTIVES
              760  COMPARE_OP               in
              762  POP_JUMP_IF_FALSE   774  'to 774'

 L. 429       766  LOAD_GLOBAL              Keyword
              768  LOAD_ATTR                Pseudo
              770  STORE_FAST               'token'
              772  JUMP_FORWARD        806  'to 806'
              774  ELSE                     '806'

 L. 432       774  LOAD_FAST                'was_dot'
              776  UNARY_NOT        
              778  POP_JUMP_IF_FALSE   802  'to 802'
              782  LOAD_FAST                'lowercase_name'
              784  LOAD_FAST                'self'
              786  LOAD_ATTR                builtins
              788  COMPARE_OP               in
              790  POP_JUMP_IF_FALSE   802  'to 802'

 L. 433       794  LOAD_GLOBAL              Name
              796  LOAD_ATTR                Builtin
              798  STORE_FAST               'token'
              800  JUMP_FORWARD        806  'to 806'
            802_0  COME_FROM           778  '778'

 L. 435       802  LOAD_GLOBAL              Name
              804  STORE_FAST               'token'
            806_0  COME_FROM           800  '800'
            806_1  COME_FROM           772  '772'
            806_2  COME_FROM           752  '752'
            806_3  COME_FROM           732  '732'
            806_4  COME_FROM           714  '714'
            806_5  COME_FROM           684  '684'
            806_6  COME_FROM           666  '666'
            806_7  COME_FROM           628  '628'
            806_8  COME_FROM           600  '600'
            806_9  COME_FROM           574  '574'
           806_10  COME_FROM           562  '562'
              806  JUMP_FORWARD        946  'to 946'
              808  ELSE                     '946'

 L. 436       808  LOAD_FAST                'scanner'
              810  LOAD_ATTR                scan
              812  LOAD_STR                 "'"
              814  CALL_FUNCTION_1       1  '1 positional argument'
              816  POP_JUMP_IF_FALSE   836  'to 836'

 L. 437       820  LOAD_GLOBAL              String
              822  STORE_FAST               'token'

 L. 438       824  LOAD_FAST                'stack'
              826  LOAD_ATTR                append
              828  LOAD_STR                 'string'
              830  CALL_FUNCTION_1       1  '1 positional argument'
              832  POP_TOP          
              834  JUMP_FORWARD        946  'to 946'
              836  ELSE                     '946'

 L. 439       836  LOAD_FAST                'scanner'
              838  LOAD_ATTR                scan
              840  LOAD_STR                 '\\#(\\d+|\\$[0-9A-Fa-f]+)'
              842  CALL_FUNCTION_1       1  '1 positional argument'
              844  POP_JUMP_IF_FALSE   856  'to 856'

 L. 440       848  LOAD_GLOBAL              String
              850  LOAD_ATTR                Char
              852  STORE_FAST               'token'
              854  JUMP_FORWARD        946  'to 946'
              856  ELSE                     '946'

 L. 441       856  LOAD_FAST                'scanner'
              858  LOAD_ATTR                scan
              860  LOAD_STR                 '\\$[0-9A-Fa-f]+'
              862  CALL_FUNCTION_1       1  '1 positional argument'
              864  POP_JUMP_IF_FALSE   876  'to 876'

 L. 442       868  LOAD_GLOBAL              Number
              870  LOAD_ATTR                Hex
              872  STORE_FAST               'token'
              874  JUMP_FORWARD        946  'to 946'
              876  ELSE                     '946'

 L. 443       876  LOAD_FAST                'scanner'
              878  LOAD_ATTR                scan
              880  LOAD_STR                 '\\d+(?![eE]|\\.[^.])'
              882  CALL_FUNCTION_1       1  '1 positional argument'
              884  POP_JUMP_IF_FALSE   896  'to 896'

 L. 444       888  LOAD_GLOBAL              Number
              890  LOAD_ATTR                Integer
              892  STORE_FAST               'token'
              894  JUMP_FORWARD        946  'to 946'
              896  ELSE                     '946'

 L. 445       896  LOAD_FAST                'scanner'
              898  LOAD_ATTR                scan
              900  LOAD_STR                 '\\d+(\\.\\d+([eE][+-]?\\d+)?|[eE][+-]?\\d+)'
              902  CALL_FUNCTION_1       1  '1 positional argument'
              904  POP_JUMP_IF_FALSE   916  'to 916'

 L. 446       908  LOAD_GLOBAL              Number
              910  LOAD_ATTR                Float
              912  STORE_FAST               'token'
              914  JUMP_FORWARD        946  'to 946'
              916  ELSE                     '946'

 L. 449       916  LOAD_GLOBAL              len
              918  LOAD_FAST                'stack'
              920  CALL_FUNCTION_1       1  '1 positional argument'
              922  LOAD_CONST               1
              924  COMPARE_OP               >
              926  POP_JUMP_IF_FALSE   938  'to 938'

 L. 450       930  LOAD_FAST                'stack'
              932  LOAD_ATTR                pop
              934  CALL_FUNCTION_0       0  '0 positional arguments'
              936  POP_TOP          
            938_0  COME_FROM           926  '926'

 L. 451       938  LOAD_FAST                'scanner'
              940  LOAD_ATTR                get_char
              942  CALL_FUNCTION_0       0  '0 positional arguments'
              944  POP_TOP          
            946_0  COME_FROM           914  '914'
            946_1  COME_FROM           894  '894'
            946_2  COME_FROM           874  '874'
            946_3  COME_FROM           854  '854'
            946_4  COME_FROM           834  '834'
            946_5  COME_FROM           806  '806'
            946_6  COME_FROM           340  '340'
            946_7  COME_FROM           238  '238'
              946  JUMP_FORWARD       1398  'to 1398'
              950  ELSE                     '1398'

 L. 453       950  LOAD_FAST                'stack'
              952  LOAD_CONST               -1
              954  BINARY_SUBSCR    
              956  LOAD_STR                 'string'
              958  COMPARE_OP               ==
              960  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 454       964  LOAD_FAST                'scanner'
              966  LOAD_ATTR                scan
              968  LOAD_STR                 "''"
              970  CALL_FUNCTION_1       1  '1 positional argument'
              972  POP_JUMP_IF_FALSE   984  'to 984'

 L. 455       976  LOAD_GLOBAL              String
              978  LOAD_ATTR                Escape
              980  STORE_FAST               'token'
              982  JUMP_FORWARD       1044  'to 1044'
              984  ELSE                     '1044'

 L. 456       984  LOAD_FAST                'scanner'
              986  LOAD_ATTR                scan
              988  LOAD_STR                 "'"
              990  CALL_FUNCTION_1       1  '1 positional argument'
              992  POP_JUMP_IF_FALSE  1010  'to 1010'

 L. 457       996  LOAD_GLOBAL              String
              998  STORE_FAST               'token'

 L. 458      1000  LOAD_FAST                'stack'
             1002  LOAD_ATTR                pop
             1004  CALL_FUNCTION_0       0  '0 positional arguments'
             1006  POP_TOP          
             1008  JUMP_FORWARD       1044  'to 1044'
             1010  ELSE                     '1044'

 L. 459      1010  LOAD_FAST                'scanner'
             1012  LOAD_ATTR                scan
             1014  LOAD_STR                 "[^']*"
             1016  CALL_FUNCTION_1       1  '1 positional argument'
             1018  POP_JUMP_IF_FALSE  1028  'to 1028'

 L. 460      1022  LOAD_GLOBAL              String
             1024  STORE_FAST               'token'
             1026  JUMP_FORWARD       1044  'to 1044'
             1028  ELSE                     '1044'

 L. 462      1028  LOAD_FAST                'scanner'
             1030  LOAD_ATTR                get_char
             1032  CALL_FUNCTION_0       0  '0 positional arguments'
             1034  POP_TOP          

 L. 463      1036  LOAD_FAST                'stack'
             1038  LOAD_ATTR                pop
             1040  CALL_FUNCTION_0       0  '0 positional arguments'
             1042  POP_TOP          
           1044_0  COME_FROM          1026  '1026'
           1044_1  COME_FROM          1008  '1008'
           1044_2  COME_FROM           982  '982'
             1044  JUMP_FORWARD       1398  'to 1398'
             1048  ELSE                     '1398'

 L. 465      1048  LOAD_FAST                'stack'
             1050  LOAD_CONST               -1
             1052  BINARY_SUBSCR    
             1054  LOAD_STR                 'asm'
             1056  COMPARE_OP               ==
             1058  POP_JUMP_IF_FALSE  1398  'to 1398'

 L. 466      1062  LOAD_FAST                'scanner'
             1064  LOAD_ATTR                scan
             1066  LOAD_STR                 '\\s+'
             1068  CALL_FUNCTION_1       1  '1 positional argument'
             1070  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 467      1074  LOAD_GLOBAL              Text
             1076  STORE_FAST               'token'
             1078  JUMP_FORWARD       1398  'to 1398'
             1082  ELSE                     '1398'

 L. 468      1082  LOAD_FAST                'scanner'
             1084  LOAD_ATTR                scan
             1086  LOAD_STR                 'end'
             1088  CALL_FUNCTION_1       1  '1 positional argument'
             1090  POP_JUMP_IF_FALSE  1110  'to 1110'

 L. 469      1094  LOAD_GLOBAL              Keyword
             1096  STORE_FAST               'token'

 L. 470      1098  LOAD_FAST                'stack'
             1100  LOAD_ATTR                pop
             1102  CALL_FUNCTION_0       0  '0 positional arguments'
             1104  POP_TOP          
             1106  JUMP_FORWARD       1398  'to 1398'
             1110  ELSE                     '1398'

 L. 471      1110  LOAD_FAST                'scanner'
             1112  LOAD_ATTR                scan
             1114  LOAD_STR                 '\\{.*?\\}|\\(\\*.*?\\*\\)'
             1116  CALL_FUNCTION_1       1  '1 positional argument'
             1118  POP_JUMP_IF_FALSE  1152  'to 1152'

 L. 472      1122  LOAD_FAST                'scanner'
             1124  LOAD_ATTR                match
             1126  LOAD_ATTR                startswith
             1128  LOAD_STR                 '$'
             1130  CALL_FUNCTION_1       1  '1 positional argument'
             1132  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 473      1136  LOAD_GLOBAL              Comment
             1138  LOAD_ATTR                Preproc
             1140  STORE_FAST               'token'
             1142  JUMP_FORWARD       1150  'to 1150'
             1144  ELSE                     '1150'

 L. 475      1144  LOAD_GLOBAL              Comment
             1146  LOAD_ATTR                Multiline
             1148  STORE_FAST               'token'
           1150_0  COME_FROM          1142  '1142'
             1150  JUMP_FORWARD       1398  'to 1398'
             1152  ELSE                     '1398'

 L. 476      1152  LOAD_FAST                'scanner'
             1154  LOAD_ATTR                scan
             1156  LOAD_STR                 '//.*?$'
             1158  CALL_FUNCTION_1       1  '1 positional argument'
             1160  POP_JUMP_IF_FALSE  1172  'to 1172'

 L. 477      1164  LOAD_GLOBAL              Comment
             1166  LOAD_ATTR                Single
             1168  STORE_FAST               'token'
             1170  JUMP_FORWARD       1398  'to 1398'
             1172  ELSE                     '1398'

 L. 478      1172  LOAD_FAST                'scanner'
             1174  LOAD_ATTR                scan
             1176  LOAD_STR                 "'"
             1178  CALL_FUNCTION_1       1  '1 positional argument'
             1180  POP_JUMP_IF_FALSE  1200  'to 1200'

 L. 479      1184  LOAD_GLOBAL              String
             1186  STORE_FAST               'token'

 L. 480      1188  LOAD_FAST                'stack'
             1190  LOAD_ATTR                append
             1192  LOAD_STR                 'string'
             1194  CALL_FUNCTION_1       1  '1 positional argument'
             1196  POP_TOP          
             1198  JUMP_FORWARD       1398  'to 1398'
             1200  ELSE                     '1398'

 L. 481      1200  LOAD_FAST                'scanner'
             1202  LOAD_ATTR                scan
             1204  LOAD_STR                 '@@[A-Za-z_][A-Za-z_0-9]*'
             1206  CALL_FUNCTION_1       1  '1 positional argument'
             1208  POP_JUMP_IF_FALSE  1220  'to 1220'

 L. 482      1212  LOAD_GLOBAL              Name
             1214  LOAD_ATTR                Label
             1216  STORE_FAST               'token'
             1218  JUMP_FORWARD       1398  'to 1398'
             1220  ELSE                     '1398'

 L. 483      1220  LOAD_FAST                'scanner'
             1222  LOAD_ATTR                scan
             1224  LOAD_STR                 '[A-Za-z_][A-Za-z_0-9]*'
             1226  CALL_FUNCTION_1       1  '1 positional argument'
             1228  POP_JUMP_IF_FALSE  1286  'to 1286'

 L. 484      1232  LOAD_FAST                'scanner'
             1234  LOAD_ATTR                match
             1236  LOAD_ATTR                lower
             1238  CALL_FUNCTION_0       0  '0 positional arguments'
             1240  STORE_FAST               'lowercase_name'

 L. 485      1242  LOAD_FAST                'lowercase_name'
             1244  LOAD_FAST                'self'
             1246  LOAD_ATTR                ASM_INSTRUCTIONS
             1248  COMPARE_OP               in
             1250  POP_JUMP_IF_FALSE  1260  'to 1260'

 L. 486      1254  LOAD_GLOBAL              Keyword
             1256  STORE_FAST               'token'
             1258  JUMP_FORWARD       1284  'to 1284'
             1260  ELSE                     '1284'

 L. 487      1260  LOAD_FAST                'lowercase_name'
             1262  LOAD_FAST                'self'
             1264  LOAD_ATTR                ASM_REGISTERS
             1266  COMPARE_OP               in
             1268  POP_JUMP_IF_FALSE  1280  'to 1280'

 L. 488      1272  LOAD_GLOBAL              Name
             1274  LOAD_ATTR                Builtin
             1276  STORE_FAST               'token'
             1278  JUMP_FORWARD       1284  'to 1284'
             1280  ELSE                     '1284'

 L. 490      1280  LOAD_GLOBAL              Name
             1282  STORE_FAST               'token'
           1284_0  COME_FROM          1278  '1278'
           1284_1  COME_FROM          1258  '1258'
             1284  JUMP_FORWARD       1398  'to 1398'
             1286  ELSE                     '1398'

 L. 491      1286  LOAD_FAST                'scanner'
             1288  LOAD_ATTR                scan
             1290  LOAD_STR                 '[-+*\\/=<>:;,.@\\^]+'
             1292  CALL_FUNCTION_1       1  '1 positional argument'
             1294  POP_JUMP_IF_FALSE  1304  'to 1304'

 L. 492      1298  LOAD_GLOBAL              Operator
             1300  STORE_FAST               'token'
             1302  JUMP_FORWARD       1398  'to 1398'
             1304  ELSE                     '1398'

 L. 493      1304  LOAD_FAST                'scanner'
             1306  LOAD_ATTR                scan
             1308  LOAD_STR                 '[\\(\\)\\[\\]]+'
             1310  CALL_FUNCTION_1       1  '1 positional argument'
             1312  POP_JUMP_IF_FALSE  1322  'to 1322'

 L. 494      1316  LOAD_GLOBAL              Punctuation
             1318  STORE_FAST               'token'
             1320  JUMP_FORWARD       1398  'to 1398'
             1322  ELSE                     '1398'

 L. 495      1322  LOAD_FAST                'scanner'
             1324  LOAD_ATTR                scan
             1326  LOAD_STR                 '\\$[0-9A-Fa-f]+'
             1328  CALL_FUNCTION_1       1  '1 positional argument'
             1330  POP_JUMP_IF_FALSE  1342  'to 1342'

 L. 496      1334  LOAD_GLOBAL              Number
             1336  LOAD_ATTR                Hex
             1338  STORE_FAST               'token'
             1340  JUMP_FORWARD       1398  'to 1398'
             1342  ELSE                     '1398'

 L. 497      1342  LOAD_FAST                'scanner'
             1344  LOAD_ATTR                scan
             1346  LOAD_STR                 '\\d+(?![eE]|\\.[^.])'
             1348  CALL_FUNCTION_1       1  '1 positional argument'
             1350  POP_JUMP_IF_FALSE  1362  'to 1362'

 L. 498      1354  LOAD_GLOBAL              Number
             1356  LOAD_ATTR                Integer
             1358  STORE_FAST               'token'
             1360  JUMP_FORWARD       1398  'to 1398'
             1362  ELSE                     '1398'

 L. 499      1362  LOAD_FAST                'scanner'
             1364  LOAD_ATTR                scan
             1366  LOAD_STR                 '\\d+(\\.\\d+([eE][+-]?\\d+)?|[eE][+-]?\\d+)'
             1368  CALL_FUNCTION_1       1  '1 positional argument'
             1370  POP_JUMP_IF_FALSE  1382  'to 1382'

 L. 500      1374  LOAD_GLOBAL              Number
             1376  LOAD_ATTR                Float
             1378  STORE_FAST               'token'
             1380  JUMP_FORWARD       1398  'to 1398'
             1382  ELSE                     '1398'

 L. 502      1382  LOAD_FAST                'scanner'
             1384  LOAD_ATTR                get_char
             1386  CALL_FUNCTION_0       0  '0 positional arguments'
             1388  POP_TOP          

 L. 503      1390  LOAD_FAST                'stack'
             1392  LOAD_ATTR                pop
             1394  CALL_FUNCTION_0       0  '0 positional arguments'
             1396  POP_TOP          
           1398_0  COME_FROM          1380  '1380'
           1398_1  COME_FROM          1360  '1360'
           1398_2  COME_FROM          1340  '1340'
           1398_3  COME_FROM          1320  '1320'
           1398_4  COME_FROM          1302  '1302'
           1398_5  COME_FROM          1284  '1284'
           1398_6  COME_FROM          1218  '1218'
           1398_7  COME_FROM          1198  '1198'
           1398_8  COME_FROM          1170  '1170'
           1398_9  COME_FROM          1150  '1150'
          1398_10  COME_FROM          1106  '1106'
          1398_11  COME_FROM          1078  '1078'
          1398_12  COME_FROM          1058  '1058'
          1398_13  COME_FROM          1044  '1044'
          1398_14  COME_FROM           946  '946'

 L. 506      1398  LOAD_FAST                'scanner'
             1400  LOAD_ATTR                match
             1402  LOAD_ATTR                strip
             1404  CALL_FUNCTION_0       0  '0 positional arguments'
             1406  POP_JUMP_IF_FALSE  1420  'to 1420'

 L. 507      1410  LOAD_FAST                'scanner'
             1412  LOAD_ATTR                match
             1414  LOAD_STR                 '.'
             1416  COMPARE_OP               ==
             1418  STORE_FAST               'was_dot'
           1420_0  COME_FROM          1406  '1406'

 L. 508      1420  LOAD_FAST                'scanner'
             1422  LOAD_ATTR                start_pos
             1424  LOAD_FAST                'token'
             1426  LOAD_FAST                'scanner'
             1428  LOAD_ATTR                match
             1430  JUMP_IF_TRUE_OR_POP  1436  'to 1436'
             1434  LOAD_STR                 ''
           1436_0  COME_FROM          1430  '1430'
             1436  BUILD_TUPLE_3         3 
             1438  YIELD_VALUE      
             1440  POP_TOP          
             1442  JUMP_BACK            72  'to 72'
           1444_0  COME_FROM            76  '76'
             1444  POP_BLOCK        
           1446_0  COME_FROM_LOOP       68  '68'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 360


class AdaLexer(RegexLexer):
    __doc__ = '\n    For Ada source code.\n\n    .. versionadded:: 1.3\n    '
    name = 'Ada'
    aliases = ['ada', 'ada95', 'ada2005']
    filenames = ['*.adb', '*.ads', '*.ada']
    mimetypes = ['text/x-ada']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root':[
      (
       '[^\\S\\n]+', Text),
      (
       '--.*?\\n', Comment.Single),
      (
       '[^\\S\\n]+', Text),
      (
       'function|procedure|entry', Keyword.Declaration, 'subprogram'),
      (
       '(subtype|type)(\\s+)(\\w+)',
       bygroups(Keyword.Declaration, Text, Keyword.Type), 'type_def'),
      (
       'task|protected', Keyword.Declaration),
      (
       '(subtype)(\\s+)', bygroupsKeyword.DeclarationText),
      (
       '(end)(\\s+)', bygroupsKeyword.ReservedText, 'end'),
      (
       '(pragma)(\\s+)(\\w+)',
       bygroups(Keyword.Reserved, Text, Comment.Preproc)),
      (
       '(true|false|null)\\b', Keyword.Constant),
      (
       words(('Address', 'Byte', 'Boolean', 'Character', 'Controlled', 'Count', 'Cursor',
       'Duration', 'File_Mode', 'File_Type', 'Float', 'Generator', 'Integer', 'Long_Float',
       'Long_Integer', 'Long_Long_Float', 'Long_Long_Integer', 'Natural', 'Positive',
       'Reference_Type', 'Short_Float', 'Short_Integer', 'Short_Short_Float', 'Short_Short_Integer',
       'String', 'Wide_Character', 'Wide_String'),
         suffix='\\b'),
       Keyword.Type),
      (
       '(and(\\s+then)?|in|mod|not|or(\\s+else)|rem)\\b', Operator.Word),
      (
       'generic|private', Keyword.Declaration),
      (
       'package', Keyword.Declaration, 'package'),
      (
       'array\\b', Keyword.Reserved, 'array_def'),
      (
       '(with|use)(\\s+)', bygroupsKeyword.NamespaceText, 'import'),
      (
       '(\\w+)(\\s*)(:)(\\s*)(constant)',
       bygroups(Name.Constant, Text, Punctuation, Text, Keyword.Reserved)),
      (
       '<<\\w+>>', Name.Label),
      (
       '(\\w+)(\\s*)(:)(\\s*)(declare|begin|loop|for|while)',
       bygroups(Name.Label, Text, Punctuation, Text, Keyword.Reserved)),
      (
       words(('abort', 'abs', 'abstract', 'accept', 'access', 'aliased', 'all', 'array', 'at',
       'begin', 'body', 'case', 'constant', 'declare', 'delay', 'delta', 'digits',
       'do', 'else', 'elsif', 'end', 'entry', 'exception', 'exit', 'interface', 'for',
       'goto', 'if', 'is', 'limited', 'loop', 'new', 'null', 'of', 'or', 'others',
       'out', 'overriding', 'pragma', 'protected', 'raise', 'range', 'record', 'renames',
       'requeue', 'return', 'reverse', 'select', 'separate', 'subtype', 'synchronized',
       'task', 'tagged', 'terminate', 'then', 'type', 'until', 'when', 'while', 'xor'),
         prefix='\\b', suffix='\\b'),
       Keyword.Reserved),
      (
       '"[^"]*"', String),
      include('attribute'),
      include('numbers'),
      (
       "'[^']'", String.Character),
      (
       '(\\w+)(\\s*|[(,])', bygroupsNameusing(this)),
      (
       "(<>|=>|:=|[()|:;,.'])", Punctuation),
      (
       '[*<>+=/&-]', Operator),
      (
       '\\n+', Text)], 
     'numbers':[
      (
       '[0-9_]+#[0-9a-f]+#', Number.Hex),
      (
       '[0-9_]+\\.[0-9_]*', Number.Float),
      (
       '[0-9_]+', Number.Integer)], 
     'attribute':[
      (
       "(')(\\w+)", bygroupsPunctuationName.Attribute)], 
     'subprogram':[
      (
       '\\(', Punctuation, ('#pop', 'formal_part')),
      (
       ';', Punctuation, '#pop'),
      (
       'is\\b', Keyword.Reserved, '#pop'),
      (
       '"[^"]+"|\\w+', Name.Function),
      include('root')], 
     'end':[
      (
       '(if|case|record|loop|select)', Keyword.Reserved),
      (
       '"[^"]+"|[\\w.]+', Name.Function),
      (
       '\\s+', Text),
      (
       ';', Punctuation, '#pop')], 
     'type_def':[
      (
       ';', Punctuation, '#pop'),
      (
       '\\(', Punctuation, 'formal_part'),
      (
       'with|and|use', Keyword.Reserved),
      (
       'array\\b', Keyword.Reserved, ('#pop', 'array_def')),
      (
       'record\\b', Keyword.Reserved, 'record_def'),
      (
       '(null record)(;)', bygroupsKeyword.ReservedPunctuation, '#pop'),
      include('root')], 
     'array_def':[
      (
       ';', Punctuation, '#pop'),
      (
       '(\\w+)(\\s+)(range)', bygroups(Keyword.Type, Text, Keyword.Reserved)),
      include('root')], 
     'record_def':[
      (
       'end record', Keyword.Reserved, '#pop'),
      include('root')], 
     'import':[
      (
       '[\\w.]+', Name.Namespace, '#pop'),
      default('#pop')], 
     'formal_part':[
      (
       '\\)', Punctuation, '#pop'),
      (
       '\\w+', Name.Variable),
      (
       ',|:[^=]', Punctuation),
      (
       '(in|not|null|out|access)\\b', Keyword.Reserved),
      include('root')], 
     'package':[
      (
       'body', Keyword.Declaration),
      (
       'is\\s+new|renames', Keyword.Reserved),
      (
       'is', Keyword.Reserved, '#pop'),
      (
       ';', Punctuation, '#pop'),
      (
       '\\(', Punctuation, 'package_instantiation'),
      (
       '([\\w.]+)', Name.Class),
      include('root')], 
     'package_instantiation':[
      (
       '("[^"]+"|\\w+)(\\s+)(=>)', bygroups(Name.Variable, Text, Punctuation)),
      (
       '[\\w.\\\'"]', Text),
      (
       '\\)', Punctuation, '#pop'),
      include('root')]}