# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/business.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 26706 bytes
"""
    pygments.lexers.business
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for "business-oriented" languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, words, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
from pygments.lexers._openedge_builtins import OPENEDGEKEYWORDS
__all__ = [
 'CobolLexer', 'CobolFreeformatLexer', 'ABAPLexer', 'OpenEdgeLexer',
 'GoodDataCLLexer', 'MaqlLexer']

class CobolLexer(RegexLexer):
    __doc__ = '\n    Lexer for OpenCOBOL code.\n\n    .. versionadded:: 1.6\n    '
    name = 'COBOL'
    aliases = ['cobol']
    filenames = ['*.cob', '*.COB', '*.cpy', '*.CPY']
    mimetypes = ['text/x-cobol']
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root': [
              include('comment'),
              include('strings'),
              include('core'),
              include('nums'),
              (
               '[a-z0-9]([\\w\\-]*[a-z0-9]+)?', Name.Variable),
              (
               '[ \\t]+', Text)], 
     
     'comment': [
                 (
                  '(^.{6}[*/].*\\n|^.{6}|\\*>.*\\n)', Comment)], 
     
     'core': [
              (
               '(^|(?<=[^0-9a-z_\\-]))(ALL\\s+)?((ZEROES)|(HIGH-VALUE|LOW-VALUE|QUOTE|SPACE|ZERO)(S)?)\\s*($|(?=[^0-9a-z_\\-]))',
               Name.Constant),
              (
               words(('ACCEPT', 'ADD', 'ALLOCATE', 'CALL', 'CANCEL', 'CLOSE', 'COMPUTE', 'CONFIGURATION',
       'CONTINUE', 'DATA', 'DELETE', 'DISPLAY', 'DIVIDE', 'DIVISION', 'ELSE', 'END',
       'END-ACCEPT', 'END-ADD', 'END-CALL', 'END-COMPUTE', 'END-DELETE', 'END-DISPLAY',
       'END-DIVIDE', 'END-EVALUATE', 'END-IF', 'END-MULTIPLY', 'END-OF-PAGE', 'END-PERFORM',
       'END-READ', 'END-RETURN', 'END-REWRITE', 'END-SEARCH', 'END-START', 'END-STRING',
       'END-SUBTRACT', 'END-UNSTRING', 'END-WRITE', 'ENVIRONMENT', 'EVALUATE', 'EXIT',
       'FD', 'FILE', 'FILE-CONTROL', 'FOREVER', 'FREE', 'GENERATE', 'GO', 'GOBACK',
       'IDENTIFICATION', 'IF', 'INITIALIZE', 'INITIATE', 'INPUT-OUTPUT', 'INSPECT',
       'INVOKE', 'I-O-CONTROL', 'LINKAGE', 'LOCAL-STORAGE', 'MERGE', 'MOVE', 'MULTIPLY',
       'OPEN', 'PERFORM', 'PROCEDURE', 'PROGRAM-ID', 'RAISE', 'READ', 'RELEASE',
       'RESUME', 'RETURN', 'REWRITE', 'SCREEN', 'SD', 'SEARCH', 'SECTION', 'SET',
       'SORT', 'START', 'STOP', 'STRING', 'SUBTRACT', 'SUPPRESS', 'TERMINATE', 'THEN',
       'UNLOCK', 'UNSTRING', 'USE', 'VALIDATE', 'WORKING-STORAGE', 'WRITE'), prefix='(^|(?<=[^0-9a-z_\\-]))', suffix='\\s*($|(?=[^0-9a-z_\\-]))'),
               Keyword.Reserved),
              (
               words(('ACCESS', 'ADDRESS', 'ADVANCING', 'AFTER', 'ALL', 'ALPHABET', 'ALPHABETIC',
       'ALPHABETIC-LOWER', 'ALPHABETIC-UPPER', 'ALPHANUMERIC', 'ALPHANUMERIC-EDITED',
       'ALSO', 'ALTER', 'ALTERNATEANY', 'ARE', 'AREA', 'AREAS', 'ARGUMENT-NUMBER',
       'ARGUMENT-VALUE', 'AS', 'ASCENDING', 'ASSIGN', 'AT', 'AUTO', 'AUTO-SKIP',
       'AUTOMATIC', 'AUTOTERMINATE', 'BACKGROUND-COLOR', 'BASED', 'BEEP', 'BEFORE',
       'BELL', 'BLANK', 'BLINK', 'BLOCK', 'BOTTOM', 'BY', 'BYTE-LENGTH', 'CHAINING',
       'CHARACTER', 'CHARACTERS', 'CLASS', 'CODE', 'CODE-SET', 'COL', 'COLLATING',
       'COLS', 'COLUMN', 'COLUMNS', 'COMMA', 'COMMAND-LINE', 'COMMIT', 'COMMON',
       'CONSTANT', 'CONTAINS', 'CONTENT', 'CONTROL', 'CONTROLS', 'CONVERTING', 'COPY',
       'CORR', 'CORRESPONDING', 'COUNT', 'CRT', 'CURRENCY', 'CURSOR', 'CYCLE', 'DATE',
       'DAY', 'DAY-OF-WEEK', 'DE', 'DEBUGGING', 'DECIMAL-POINT', 'DECLARATIVES',
       'DEFAULT', 'DELIMITED', 'DELIMITER', 'DEPENDING', 'DESCENDING', 'DETAIL',
       'DISK', 'DOWN', 'DUPLICATES', 'DYNAMIC', 'EBCDIC', 'ENTRY', 'ENVIRONMENT-NAME',
       'ENVIRONMENT-VALUE', 'EOL', 'EOP', 'EOS', 'ERASE', 'ERROR', 'ESCAPE', 'EXCEPTION',
       'EXCLUSIVE', 'EXTEND', 'EXTERNAL', 'FILE-ID', 'FILLER', 'FINAL', 'FIRST',
       'FIXED', 'FLOAT-LONG', 'FLOAT-SHORT', 'FOOTING', 'FOR', 'FOREGROUND-COLOR',
       'FORMAT', 'FROM', 'FULL', 'FUNCTION', 'FUNCTION-ID', 'GIVING', 'GLOBAL', 'GROUP',
       'HEADING', 'HIGHLIGHT', 'I-O', 'ID', 'IGNORE', 'IGNORING', 'IN', 'INDEX',
       'INDEXED', 'INDICATE', 'INITIAL', 'INITIALIZED', 'INPUT', 'INTO', 'INTRINSIC',
       'INVALID', 'IS', 'JUST', 'JUSTIFIED', 'KEY', 'LABEL', 'LAST', 'LEADING', 'LEFT',
       'LENGTH', 'LIMIT', 'LIMITS', 'LINAGE', 'LINAGE-COUNTER', 'LINE', 'LINES',
       'LOCALE', 'LOCK', 'LOWLIGHT', 'MANUAL', 'MEMORY', 'MINUS', 'MODE', 'MULTIPLE',
       'NATIONAL', 'NATIONAL-EDITED', 'NATIVE', 'NEGATIVE', 'NEXT', 'NO', 'NULL',
       'NULLS', 'NUMBER', 'NUMBERS', 'NUMERIC', 'NUMERIC-EDITED', 'OBJECT-COMPUTER',
       'OCCURS', 'OF', 'OFF', 'OMITTED', 'ON', 'ONLY', 'OPTIONAL', 'ORDER', 'ORGANIZATION',
       'OTHER', 'OUTPUT', 'OVERFLOW', 'OVERLINE', 'PACKED-DECIMAL', 'PADDING', 'PAGE',
       'PARAGRAPH', 'PLUS', 'POINTER', 'POSITION', 'POSITIVE', 'PRESENT', 'PREVIOUS',
       'PRINTER', 'PRINTING', 'PROCEDURE-POINTER', 'PROCEDURES', 'PROCEED', 'PROGRAM',
       'PROGRAM-POINTER', 'PROMPT', 'QUOTE', 'QUOTES', 'RANDOM', 'RD', 'RECORD',
       'RECORDING', 'RECORDS', 'RECURSIVE', 'REDEFINES', 'REEL', 'REFERENCE', 'RELATIVE',
       'REMAINDER', 'REMOVAL', 'RENAMES', 'REPLACING', 'REPORT', 'REPORTING', 'REPORTS',
       'REPOSITORY', 'REQUIRED', 'RESERVE', 'RETURNING', 'REVERSE-VIDEO', 'REWIND',
       'RIGHT', 'ROLLBACK', 'ROUNDED', 'RUN', 'SAME', 'SCROLL', 'SECURE', 'SEGMENT-LIMIT',
       'SELECT', 'SENTENCE', 'SEPARATE', 'SEQUENCE', 'SEQUENTIAL', 'SHARING', 'SIGN',
       'SIGNED', 'SIGNED-INT', 'SIGNED-LONG', 'SIGNED-SHORT', 'SIZE', 'SORT-MERGE',
       'SOURCE', 'SOURCE-COMPUTER', 'SPECIAL-NAMES', 'STANDARD', 'STANDARD-1', 'STANDARD-2',
       'STATUS', 'SUM', 'SYMBOLIC', 'SYNC', 'SYNCHRONIZED', 'TALLYING', 'TAPE', 'TEST',
       'THROUGH', 'THRU', 'TIME', 'TIMES', 'TO', 'TOP', 'TRAILING', 'TRANSFORM',
       'TYPE', 'UNDERLINE', 'UNIT', 'UNSIGNED', 'UNSIGNED-INT', 'UNSIGNED-LONG',
       'UNSIGNED-SHORT', 'UNTIL', 'UP', 'UPDATE', 'UPON', 'USAGE', 'USING', 'VALUE',
       'VALUES', 'VARYING', 'WAIT', 'WHEN', 'WITH', 'WORDS', 'YYYYDDD', 'YYYYMMDD'), prefix='(^|(?<=[^0-9a-z_\\-]))', suffix='\\s*($|(?=[^0-9a-z_\\-]))'),
               Keyword.Pseudo),
              (
               words(('ACTIVE-CLASS', 'ALIGNED', 'ANYCASE', 'ARITHMETIC', 'ATTRIBUTE', 'B-AND', 'B-NOT',
       'B-OR', 'B-XOR', 'BIT', 'BOOLEAN', 'CD', 'CENTER', 'CF', 'CH', 'CHAIN', 'CLASS-ID',
       'CLASSIFICATION', 'COMMUNICATION', 'CONDITION', 'DATA-POINTER', 'DESTINATION',
       'DISABLE', 'EC', 'EGI', 'EMI', 'ENABLE', 'END-RECEIVE', 'ENTRY-CONVENTION',
       'EO', 'ESI', 'EXCEPTION-OBJECT', 'EXPANDS', 'FACTORY', 'FLOAT-BINARY-16',
       'FLOAT-BINARY-34', 'FLOAT-BINARY-7', 'FLOAT-DECIMAL-16', 'FLOAT-DECIMAL-34',
       'FLOAT-EXTENDED', 'FORMAT', 'FUNCTION-POINTER', 'GET', 'GROUP-USAGE', 'IMPLEMENTS',
       'INFINITY', 'INHERITS', 'INTERFACE', 'INTERFACE-ID', 'INVOKE', 'LC_ALL', 'LC_COLLATE',
       'LC_CTYPE', 'LC_MESSAGES', 'LC_MONETARY', 'LC_NUMERIC', 'LC_TIME', 'LINE-COUNTER',
       'MESSAGE', 'METHOD', 'METHOD-ID', 'NESTED', 'NONE', 'NORMAL', 'OBJECT', 'OBJECT-REFERENCE',
       'OPTIONS', 'OVERRIDE', 'PAGE-COUNTER', 'PF', 'PH', 'PROPERTY', 'PROTOTYPE',
       'PURGE', 'QUEUE', 'RAISE', 'RAISING', 'RECEIVE', 'RELATION', 'REPLACE', 'REPRESENTS-NOT-A-NUMBER',
       'RESET', 'RESUME', 'RETRY', 'RF', 'RH', 'SECONDS', 'SEGMENT', 'SELF', 'SEND',
       'SOURCES', 'STATEMENT', 'STEP', 'STRONG', 'SUB-QUEUE-1', 'SUB-QUEUE-2', 'SUB-QUEUE-3',
       'SUPER', 'SYMBOL', 'SYSTEM-DEFAULT', 'TABLE', 'TERMINAL', 'TEXT', 'TYPEDEF',
       'UCS-4', 'UNIVERSAL', 'USER-DEFAULT', 'UTF-16', 'UTF-8', 'VAL-STATUS', 'VALID',
       'VALIDATE', 'VALIDATE-STATUS'), prefix='(^|(?<=[^0-9a-z_\\-]))', suffix='\\s*($|(?=[^0-9a-z_\\-]))'),
               Error),
              (
               '(^|(?<=[^0-9a-z_\\-]))(PIC\\s+.+?(?=(\\s|\\.\\s))|PICTURE\\s+.+?(?=(\\s|\\.\\s))|(COMPUTATIONAL)(-[1-5X])?|(COMP)(-[1-5X])?|BINARY-C-LONG|BINARY-CHAR|BINARY-DOUBLE|BINARY-LONG|BINARY-SHORT|BINARY)\\s*($|(?=[^0-9a-z_\\-]))',
               Keyword.Type),
              (
               '(\\*\\*|\\*|\\+|-|/|<=|>=|<|>|==|/=|=)', Operator),
              (
               '([(),;:&%.])', Punctuation),
              (
               '(^|(?<=[^0-9a-z_\\-]))(ABS|ACOS|ANNUITY|ASIN|ATAN|BYTE-LENGTH|CHAR|COMBINED-DATETIME|CONCATENATE|COS|CURRENT-DATE|DATE-OF-INTEGER|DATE-TO-YYYYMMDD|DAY-OF-INTEGER|DAY-TO-YYYYDDD|EXCEPTION-(?:FILE|LOCATION|STATEMENT|STATUS)|EXP10|EXP|E|FACTORIAL|FRACTION-PART|INTEGER-OF-(?:DATE|DAY|PART)|INTEGER|LENGTH|LOCALE-(?:DATE|TIME(?:-FROM-SECONDS)?)|LOG(?:10)?|LOWER-CASE|MAX|MEAN|MEDIAN|MIDRANGE|MIN|MOD|NUMVAL(?:-C)?|ORD(?:-MAX|-MIN)?|PI|PRESENT-VALUE|RANDOM|RANGE|REM|REVERSE|SECONDS-FROM-FORMATTED-TIME|SECONDS-PAST-MIDNIGHT|SIGN|SIN|SQRT|STANDARD-DEVIATION|STORED-CHAR-LENGTH|SUBSTITUTE(?:-CASE)?|SUM|TAN|TEST-DATE-YYYYMMDD|TEST-DAY-YYYYDDD|TRIM|UPPER-CASE|VARIANCE|WHEN-COMPILED|YEAR-TO-YYYY)\\s*($|(?=[^0-9a-z_\\-]))',
               Name.Function),
              (
               '(^|(?<=[^0-9a-z_\\-]))(true|false)\\s*($|(?=[^0-9a-z_\\-]))', Name.Builtin),
              (
               '(^|(?<=[^0-9a-z_\\-]))(equal|equals|ne|lt|le|gt|ge|greater|less|than|not|and|or)\\s*($|(?=[^0-9a-z_\\-]))',
               Operator.Word)], 
     
     'strings': [
                 (
                  '"[^"\\n]*("|\\n)', String.Double),
                 (
                  "'[^'\\n]*('|\\n)", String.Single)], 
     
     'nums': [
              (
               '\\d+(\\s*|\\.$|$)', Number.Integer),
              (
               '[+-]?\\d*\\.\\d+(E[-+]?\\d+)?', Number.Float),
              (
               '[+-]?\\d+\\.\\d*(E[-+]?\\d+)?', Number.Float)]}


class CobolFreeformatLexer(CobolLexer):
    __doc__ = '\n    Lexer for Free format OpenCOBOL code.\n\n    .. versionadded:: 1.6\n    '
    name = 'COBOLFree'
    aliases = ['cobolfree']
    filenames = ['*.cbl', '*.CBL']
    mimetypes = []
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'comment': [
                 (
                  '(\\*>.*\\n|^\\w*\\*.*$)', Comment)]}


class ABAPLexer(RegexLexer):
    __doc__ = "\n    Lexer for ABAP, SAP's integrated language.\n\n    .. versionadded:: 1.1\n    "
    name = 'ABAP'
    aliases = ['abap']
    filenames = ['*.abap', '*.ABAP']
    mimetypes = ['text/x-abap']
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'common': [
                (
                 '\\s+', Text),
                (
                 '^\\*.*$', Comment.Single),
                (
                 '\\".*?\\n', Comment.Single)], 
     
     'variable-names': [
                        (
                         '<\\S+>', Name.Variable),
                        (
                         '\\w[\\w~]*(?:(\\[\\])|->\\*)?', Name.Variable)], 
     
     'root': [
              include('common'),
              (
               "(CALL\\s+(?:BADI|CUSTOMER-FUNCTION|FUNCTION))(\\s+)(\\'?\\S+\\'?)",
               bygroups(Keyword, Text, Name.Function)),
              (
               '(CALL\\s+(?:DIALOG|SCREEN|SUBSCREEN|SELECTION-SCREEN|TRANSACTION|TRANSFORMATION))\\b',
               Keyword),
              (
               '(FORM|PERFORM)(\\s+)(\\w+)',
               bygroups(Keyword, Text, Name.Function)),
              (
               '(PERFORM)(\\s+)(\\()(\\w+)(\\))',
               bygroups(Keyword, Text, Punctuation, Name.Variable, Punctuation)),
              (
               '(MODULE)(\\s+)(\\S+)(\\s+)(INPUT|OUTPUT)',
               bygroups(Keyword, Text, Name.Function, Text, Keyword)),
              (
               '(METHOD)(\\s+)([\\w~]+)',
               bygroups(Keyword, Text, Name.Function)),
              (
               '(\\s+)([\\w\\-]+)([=\\-]>)([\\w\\-~]+)',
               bygroups(Text, Name.Variable, Operator, Name.Function)),
              (
               '(?<=(=|-)>)([\\w\\-~]+)(?=\\()', Name.Function),
              (
               '(ADD-CORRESPONDING|AUTHORITY-CHECK|CLASS-DATA|CLASS-EVENTS|CLASS-METHODS|CLASS-POOL|DELETE-ADJACENT|DIVIDE-CORRESPONDING|EDITOR-CALL|ENHANCEMENT-POINT|ENHANCEMENT-SECTION|EXIT-COMMAND|FIELD-GROUPS|FIELD-SYMBOLS|FUNCTION-POOL|INTERFACE-POOL|INVERTED-DATE|LOAD-OF-PROGRAM|LOG-POINT|MESSAGE-ID|MOVE-CORRESPONDING|MULTIPLY-CORRESPONDING|NEW-LINE|NEW-PAGE|NEW-SECTION|NO-EXTENSION|OUTPUT-LENGTH|PRINT-CONTROL|SELECT-OPTIONS|START-OF-SELECTION|SUBTRACT-CORRESPONDING|SYNTAX-CHECK|SYSTEM-EXCEPTIONS|TYPE-POOL|TYPE-POOLS)\\b',
               Keyword),
              (
               'CREATE\\s+(PUBLIC|PRIVATE|DATA|OBJECT)|((PUBLIC|PRIVATE|PROTECTED)\\s+SECTION|(TYPE|LIKE)(\\s+(LINE\\s+OF|REF\\s+TO|(SORTED|STANDARD|HASHED)\\s+TABLE\\s+OF))?|FROM\\s+(DATABASE|MEMORY)|CALL\\s+METHOD|(GROUP|ORDER) BY|HAVING|SEPARATED BY|GET\\s+(BADI|BIT|CURSOR|DATASET|LOCALE|PARAMETER|PF-STATUS|(PROPERTY|REFERENCE)\\s+OF|RUN\\s+TIME|TIME\\s+(STAMP)?)?|SET\\s+(BIT|BLANK\\s+LINES|COUNTRY|CURSOR|DATASET|EXTENDED\\s+CHECK|HANDLER|HOLD\\s+DATA|LANGUAGE|LEFT\\s+SCROLL-BOUNDARY|LOCALE|MARGIN|PARAMETER|PF-STATUS|PROPERTY\\s+OF|RUN\\s+TIME\\s+(ANALYZER|CLOCK\\s+RESOLUTION)|SCREEN|TITLEBAR|UPADTE\\s+TASK\\s+LOCAL|USER-COMMAND)|CONVERT\\s+((INVERTED-)?DATE|TIME|TIME\\s+STAMP|TEXT)|(CLOSE|OPEN)\\s+(DATASET|CURSOR)|(TO|FROM)\\s+(DATA BUFFER|INTERNAL TABLE|MEMORY ID|DATABASE|SHARED\\s+(MEMORY|BUFFER))|DESCRIBE\\s+(DISTANCE\\s+BETWEEN|FIELD|LIST|TABLE)|FREE\\s(MEMORY|OBJECT)?|PROCESS\\s+(BEFORE\\s+OUTPUT|AFTER\\s+INPUT|ON\\s+(VALUE-REQUEST|HELP-REQUEST))|AT\\s+(LINE-SELECTION|USER-COMMAND|END\\s+OF|NEW)|AT\\s+SELECTION-SCREEN(\\s+(ON(\\s+(BLOCK|(HELP|VALUE)-REQUEST\\s+FOR|END\\s+OF|RADIOBUTTON\\s+GROUP))?|OUTPUT))?|SELECTION-SCREEN:?\\s+((BEGIN|END)\\s+OF\\s+((TABBED\\s+)?BLOCK|LINE|SCREEN)|COMMENT|FUNCTION\\s+KEY|INCLUDE\\s+BLOCKS|POSITION|PUSHBUTTON|SKIP|ULINE)|LEAVE\\s+(LIST-PROCESSING|PROGRAM|SCREEN|TO LIST-PROCESSING|TO TRANSACTION)(ENDING|STARTING)\\s+AT|FORMAT\\s+(COLOR|INTENSIFIED|INVERSE|HOTSPOT|INPUT|FRAMES|RESET)|AS\\s+(CHECKBOX|SUBSCREEN|WINDOW)|WITH\\s+(((NON-)?UNIQUE)?\\s+KEY|FRAME)|(BEGIN|END)\\s+OF|DELETE(\\s+ADJACENT\\s+DUPLICATES\\sFROM)?|COMPARING(\\s+ALL\\s+FIELDS)?|INSERT(\\s+INITIAL\\s+LINE\\s+INTO|\\s+LINES\\s+OF)?|IN\\s+((BYTE|CHARACTER)\\s+MODE|PROGRAM)|END-OF-(DEFINITION|PAGE|SELECTION)|WITH\\s+FRAME(\\s+TITLE)|AND\\s+(MARK|RETURN)|CLIENT\\s+SPECIFIED|CORRESPONDING\\s+FIELDS\\s+OF|IF\\s+FOUND|FOR\\s+EVENT|INHERITING\\s+FROM|LEAVE\\s+TO\\s+SCREEN|LOOP\\s+AT\\s+(SCREEN)?|LOWER\\s+CASE|MATCHCODE\\s+OBJECT|MODIF\\s+ID|MODIFY\\s+SCREEN|NESTING\\s+LEVEL|NO\\s+INTERVALS|OF\\s+STRUCTURE|RADIOBUTTON\\s+GROUP|RANGE\\s+OF|REF\\s+TO|SUPPRESS DIALOG|TABLE\\s+OF|UPPER\\s+CASE|TRANSPORTING\\s+NO\\s+FIELDS|VALUE\\s+CHECK|VISIBLE\\s+LENGTH|HEADER\\s+LINE)\\b',
               Keyword),
              (
               '(^|(?<=(\\s|\\.)))(ABBREVIATED|ADD|ALIASES|APPEND|ASSERT|ASSIGN(ING)?|AT(\\s+FIRST)?|BACK|BLOCK|BREAK-POINT|CASE|CATCH|CHANGING|CHECK|CLASS|CLEAR|COLLECT|COLOR|COMMIT|CREATE|COMMUNICATION|COMPONENTS?|COMPUTE|CONCATENATE|CONDENSE|CONSTANTS|CONTEXTS|CONTINUE|CONTROLS|DATA|DECIMALS|DEFAULT|DEFINE|DEFINITION|DEFERRED|DEMAND|DETAIL|DIRECTORY|DIVIDE|DO|ELSE(IF)?|ENDAT|ENDCASE|ENDCLASS|ENDDO|ENDFORM|ENDFUNCTION|ENDIF|ENDLOOP|ENDMETHOD|ENDMODULE|ENDSELECT|ENDTRY|ENHANCEMENT|EVENTS|EXCEPTIONS|EXIT|EXPORT|EXPORTING|EXTRACT|FETCH|FIELDS?|FIND|FOR|FORM|FORMAT|FREE|FROM|HIDE|ID|IF|IMPORT|IMPLEMENTATION|IMPORTING|IN|INCLUDE|INCLUDING|INDEX|INFOTYPES|INITIALIZATION|INTERFACE|INTERFACES|INTO|LENGTH|LINES|LOAD|LOCAL|JOIN|KEY|MAXIMUM|MESSAGE|METHOD[S]?|MINIMUM|MODULE|MODIFY|MOVE|MULTIPLY|NODES|OBLIGATORY|OF|OFF|ON|OVERLAY|PACK|PARAMETERS|PERCENTAGE|POSITION|PROGRAM|PROVIDE|PUBLIC|PUT|RAISE|RAISING|RANGES|READ|RECEIVE|REFRESH|REJECT|REPORT|RESERVE|RESUME|RETRY|RETURN|RETURNING|RIGHT|ROLLBACK|SCROLL|SEARCH|SELECT|SHIFT|SINGLE|SKIP|SORT|SPLIT|STATICS|STOP|SUBMIT|SUBTRACT|SUM|SUMMARY|SUMMING|SUPPLY|TABLE|TABLES|TIMES|TITLE|TO|TOP-OF-PAGE|TRANSFER|TRANSLATE|TRY|TYPES|ULINE|UNDER|UNPACK|UPDATE|USING|VALUE|VALUES|VIA|WAIT|WHEN|WHERE|WHILE|WITH|WINDOW|WRITE)\\b',
               Keyword),
              (
               '(abs|acos|asin|atan|boolc|boolx|bit_set|char_off|charlen|ceil|cmax|cmin|condense|contains|contains_any_of|contains_any_not_of|concat_lines_of|cos|cosh|count|count_any_of|count_any_not_of|dbmaxlen|distance|escape|exp|find|find_end|find_any_of|find_any_not_of|floor|frac|from_mixed|insert|lines|log|log10|match|matches|nmax|nmin|numofchar|repeat|replace|rescale|reverse|round|segment|shift_left|shift_right|sign|sin|sinh|sqrt|strlen|substring|substring_after|substring_from|substring_before|substring_to|tan|tanh|to_upper|to_lower|to_mixed|translate|trunc|xstrlen)(\\()\\b',
               bygroups(Name.Builtin, Punctuation)),
              (
               '&[0-9]', Name),
              (
               '[0-9]+', Number.Integer),
              (
               '(?<=(\\s|.))(AND|EQ|NE|GT|LT|GE|LE|CO|CN|CA|NA|CS|NOT|NS|CP|NP|BYTE-CO|BYTE-CN|BYTE-CA|BYTE-NA|BYTE-CS|BYTE-NS|IS\\s+(NOT\\s+)?(INITIAL|ASSIGNED|REQUESTED|BOUND))\\b',
               Operator),
              include('variable-names'),
              (
               '[?*<>=\\-+]', Operator),
              (
               "'(''|[^'])*'", String.Single),
              (
               '`([^`])*`', String.Single),
              (
               '[/;:()\\[\\],.]', Punctuation)]}


class OpenEdgeLexer(RegexLexer):
    __doc__ = '\n    Lexer for `OpenEdge ABL (formerly Progress)\n    <http://web.progress.com/en/openedge/abl.html>`_ source code.\n\n    .. versionadded:: 1.5\n    '
    name = 'OpenEdge ABL'
    aliases = ['openedge', 'abl', 'progress']
    filenames = ['*.p', '*.cls']
    mimetypes = ['text/x-openedge', 'application/x-openedge']
    types = '(?i)(^|(?<=[^0-9a-z_\\-]))(CHARACTER|CHAR|CHARA|CHARAC|CHARACT|CHARACTE|COM-HANDLE|DATE|DATETIME|DATETIME-TZ|DECIMAL|DEC|DECI|DECIM|DECIMA|HANDLE|INT64|INTEGER|INT|INTE|INTEG|INTEGE|LOGICAL|LONGCHAR|MEMPTR|RAW|RECID|ROWID)\\s*($|(?=[^0-9a-z_\\-]))'
    keywords = words(OPENEDGEKEYWORDS, prefix='(?i)(^|(?<=[^0-9a-z_\\-]))', suffix='\\s*($|(?=[^0-9a-z_\\-]))')
    tokens = {'root': [
              (
               '/\\*', Comment.Multiline, 'comment'),
              (
               '\\{', Comment.Preproc, 'preprocessor'),
              (
               '\\s*&.*', Comment.Preproc),
              (
               '0[xX][0-9a-fA-F]+[LlUu]*', Number.Hex),
              (
               '(?i)(DEFINE|DEF|DEFI|DEFIN)\\b', Keyword.Declaration),
              (
               types, Keyword.Type),
              (
               keywords, Name.Builtin),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
              (
               "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
              (
               '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
              (
               '[0-9]+', Number.Integer),
              (
               '\\s+', Text),
              (
               '[+*/=-]', Operator),
              (
               '[.:()]', Punctuation),
              (
               '.', Name.Variable)], 
     
     'comment': [
                 (
                  '[^*/]', Comment.Multiline),
                 (
                  '/\\*', Comment.Multiline, '#push'),
                 (
                  '\\*/', Comment.Multiline, '#pop'),
                 (
                  '[*/]', Comment.Multiline)], 
     
     'preprocessor': [
                      (
                       '[^{}]', Comment.Preproc),
                      (
                       '\\{', Comment.Preproc, '#push'),
                      (
                       '\\}', Comment.Preproc, '#pop')]}


class GoodDataCLLexer(RegexLexer):
    __doc__ = '\n    Lexer for `GoodData-CL\n    <http://github.com/gooddata/GoodData-CL/raw/master/cli/src/main/resources/com/gooddata/processor/COMMANDS.txt>`_\n    script files.\n\n    .. versionadded:: 1.4\n    '
    name = 'GoodData-CL'
    aliases = ['gooddata-cl']
    filenames = ['*.gdc']
    mimetypes = ['text/x-gooddata-cl']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               '#.*', Comment.Single),
              (
               '[a-z]\\w*', Name.Function),
              (
               '\\(', Punctuation, 'args-list'),
              (
               ';', Punctuation),
              (
               '\\s+', Text)], 
     
     'args-list': [
                   (
                    '\\)', Punctuation, '#pop'),
                   (
                    ',', Punctuation),
                   (
                    '[a-z]\\w*', Name.Variable),
                   (
                    '=', Operator),
                   (
                    '"', String, 'string-literal'),
                   (
                    '[0-9]+(?:\\.[0-9]+)?(?:e[+-]?[0-9]{1,3})?', Number),
                   (
                    '\\s', Text)], 
     
     'string-literal': [
                        (
                         '\\\\[tnrfbae"\\\\]', String.Escape),
                        (
                         '"', String, '#pop'),
                        (
                         '[^\\\\"]+', String)]}


class MaqlLexer(RegexLexer):
    __doc__ = '\n    Lexer for `GoodData MAQL\n    <https://secure.gooddata.com/docs/html/advanced.metric.tutorial.html>`_\n    scripts.\n\n    .. versionadded:: 1.4\n    '
    name = 'MAQL'
    aliases = ['maql']
    filenames = ['*.maql']
    mimetypes = ['text/x-gooddata-maql', 'application/x-gooddata-maql']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               'IDENTIFIER\\b', Name.Builtin),
              (
               '\\{[^}]+\\}', Name.Variable),
              (
               '[0-9]+(?:\\.[0-9]+)?(?:e[+-]?[0-9]{1,3})?', Number),
              (
               '"', String, 'string-literal'),
              (
               '\\<\\>|\\!\\=', Operator),
              (
               '\\=|\\>\\=|\\>|\\<\\=|\\<', Operator),
              (
               '\\:\\=', Operator),
              (
               '\\[[^]]+\\]', Name.Variable.Class),
              (
               words(('DIMENSION', 'DIMENSIONS', 'BOTTOM', 'METRIC', 'COUNT', 'OTHER', 'FACT', 'WITH',
       'TOP', 'OR', 'ATTRIBUTE', 'CREATE', 'PARENT', 'FALSE', 'ROW', 'ROWS', 'FROM',
       'ALL', 'AS', 'PF', 'COLUMN', 'COLUMNS', 'DEFINE', 'REPORT', 'LIMIT', 'TABLE',
       'LIKE', 'AND', 'BY', 'BETWEEN', 'EXCEPT', 'SELECT', 'MATCH', 'WHERE', 'TRUE',
       'FOR', 'IN', 'WITHOUT', 'FILTER', 'ALIAS', 'WHEN', 'NOT', 'ON', 'KEYS', 'KEY',
       'FULLSET', 'PRIMARY', 'LABELS', 'LABEL', 'VISUAL', 'TITLE', 'DESCRIPTION',
       'FOLDER', 'ALTER', 'DROP', 'ADD', 'DATASET', 'DATATYPE', 'INT', 'BIGINT',
       'DOUBLE', 'DATE', 'VARCHAR', 'DECIMAL', 'SYNCHRONIZE', 'TYPE', 'DEFAULT',
       'ORDER', 'ASC', 'DESC', 'HYPERLINK', 'INCLUDE', 'TEMPLATE', 'MODIFY'), suffix='\\b'),
               Keyword),
              (
               '[a-z]\\w*\\b', Name.Function),
              (
               '#.*', Comment.Single),
              (
               '[,;()]', Punctuation),
              (
               '\\s+', Text)], 
     
     'string-literal': [
                        (
                         '\\\\[tnrfbae"\\\\]', String.Escape),
                        (
                         '"', String, '#pop'),
                        (
                         '[^\\\\"]+', String)]}