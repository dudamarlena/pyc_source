# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/other.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.other
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for other languages.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, this, do_insertions
from pygments.token import Error, Punctuation, Literal, Token, Text, Comment, Operator, Keyword, Name, String, Number, Generic
from pygments.util import shebang_matches
from pygments.lexers.web import HtmlLexer
__all__ = [
 'SqlLexer', 'MySqlLexer', 'SqliteConsoleLexer', 'BrainfuckLexer',
 'BashLexer', 'BatchLexer', 'BefungeLexer', 'RedcodeLexer',
 'MOOCodeLexer', 'SmalltalkLexer', 'TcshLexer', 'LogtalkLexer',
 'GnuplotLexer', 'PovrayLexer', 'AppleScriptLexer',
 'BashSessionLexer', 'ModelicaLexer', 'RebolLexer', 'ABAPLexer',
 'NewspeakLexer', 'GherkinLexer', 'AsymptoteLexer',
 'PostScriptLexer', 'AutohotkeyLexer', 'GoodDataCLLexer',
 'MaqlLexer', 'ProtoBufLexer', 'HybrisLexer']
line_re = re.compile('.*?\n')

class SqlLexer(RegexLexer):
    """
    Lexer for Structured Query Language. Currently, this lexer does
    not recognize any special syntax except ANSI SQL.
    """
    name = 'SQL'
    aliases = ['sql']
    filenames = ['*.sql']
    mimetypes = ['text/x-sql']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '--.*?\\n', Comment.Single),
              (
               '/\\*', Comment.Multiline, 'multiline-comments'),
              (
               '(ABORT|ABS|ABSOLUTE|ACCESS|ADA|ADD|ADMIN|AFTER|AGGREGATE|ALIAS|ALL|ALLOCATE|ALTER|ANALYSE|ANALYZE|AND|ANY|ARE|AS|ASC|ASENSITIVE|ASSERTION|ASSIGNMENT|ASYMMETRIC|AT|ATOMIC|AUTHORIZATION|AVG|BACKWARD|BEFORE|BEGIN|BETWEEN|BITVAR|BIT_LENGTH|BOTH|BREADTH|BY|C|CACHE|CALL|CALLED|CARDINALITY|CASCADE|CASCADED|CASE|CAST|CATALOG|CATALOG_NAME|CHAIN|CHARACTERISTICS|CHARACTER_LENGTH|CHARACTER_SET_CATALOG|CHARACTER_SET_NAME|CHARACTER_SET_SCHEMA|CHAR_LENGTH|CHECK|CHECKED|CHECKPOINT|CLASS|CLASS_ORIGIN|CLOB|CLOSE|CLUSTER|COALSECE|COBOL|COLLATE|COLLATION|COLLATION_CATALOG|COLLATION_NAME|COLLATION_SCHEMA|COLUMN|COLUMN_NAME|COMMAND_FUNCTION|COMMAND_FUNCTION_CODE|COMMENT|COMMIT|COMMITTED|COMPLETION|CONDITION_NUMBER|CONNECT|CONNECTION|CONNECTION_NAME|CONSTRAINT|CONSTRAINTS|CONSTRAINT_CATALOG|CONSTRAINT_NAME|CONSTRAINT_SCHEMA|CONSTRUCTOR|CONTAINS|CONTINUE|CONVERSION|CONVERT|COPY|CORRESPONTING|COUNT|CREATE|CREATEDB|CREATEUSER|CROSS|CUBE|CURRENT|CURRENT_DATE|CURRENT_PATH|CURRENT_ROLE|CURRENT_TIME|CURRENT_TIMESTAMP|CURRENT_USER|CURSOR|CURSOR_NAME|CYCLE|DATA|DATABASE|DATETIME_INTERVAL_CODE|DATETIME_INTERVAL_PRECISION|DAY|DEALLOCATE|DECLARE|DEFAULT|DEFAULTS|DEFERRABLE|DEFERRED|DEFINED|DEFINER|DELETE|DELIMITER|DELIMITERS|DEREF|DESC|DESCRIBE|DESCRIPTOR|DESTROY|DESTRUCTOR|DETERMINISTIC|DIAGNOSTICS|DICTIONARY|DISCONNECT|DISPATCH|DISTINCT|DO|DOMAIN|DROP|DYNAMIC|DYNAMIC_FUNCTION|DYNAMIC_FUNCTION_CODE|EACH|ELSE|ENCODING|ENCRYPTED|END|END-EXEC|EQUALS|ESCAPE|EVERY|EXCEPT|ESCEPTION|EXCLUDING|EXCLUSIVE|EXEC|EXECUTE|EXISTING|EXISTS|EXPLAIN|EXTERNAL|EXTRACT|FALSE|FETCH|FINAL|FIRST|FOR|FORCE|FOREIGN|FORTRAN|FORWARD|FOUND|FREE|FREEZE|FROM|FULL|FUNCTION|G|GENERAL|GENERATED|GET|GLOBAL|GO|GOTO|GRANT|GRANTED|GROUP|GROUPING|HANDLER|HAVING|HIERARCHY|HOLD|HOST|IDENTITY|IGNORE|ILIKE|IMMEDIATE|IMMUTABLE|IMPLEMENTATION|IMPLICIT|IN|INCLUDING|INCREMENT|INDEX|INDITCATOR|INFIX|INHERITS|INITIALIZE|INITIALLY|INNER|INOUT|INPUT|INSENSITIVE|INSERT|INSTANTIABLE|INSTEAD|INTERSECT|INTO|INVOKER|IS|ISNULL|ISOLATION|ITERATE|JOIN|KEY|KEY_MEMBER|KEY_TYPE|LANCOMPILER|LANGUAGE|LARGE|LAST|LATERAL|LEADING|LEFT|LENGTH|LESS|LEVEL|LIKE|LIMIT|LISTEN|LOAD|LOCAL|LOCALTIME|LOCALTIMESTAMP|LOCATION|LOCATOR|LOCK|LOWER|MAP|MATCH|MAX|MAXVALUE|MESSAGE_LENGTH|MESSAGE_OCTET_LENGTH|MESSAGE_TEXT|METHOD|MIN|MINUTE|MINVALUE|MOD|MODE|MODIFIES|MODIFY|MONTH|MORE|MOVE|MUMPS|NAMES|NATIONAL|NATURAL|NCHAR|NCLOB|NEW|NEXT|NO|NOCREATEDB|NOCREATEUSER|NONE|NOT|NOTHING|NOTIFY|NOTNULL|NULL|NULLABLE|NULLIF|OBJECT|OCTET_LENGTH|OF|OFF|OFFSET|OIDS|OLD|ON|ONLY|OPEN|OPERATION|OPERATOR|OPTION|OPTIONS|OR|ORDER|ORDINALITY|OUT|OUTER|OUTPUT|OVERLAPS|OVERLAY|OVERRIDING|OWNER|PAD|PARAMETER|PARAMETERS|PARAMETER_MODE|PARAMATER_NAME|PARAMATER_ORDINAL_POSITION|PARAMETER_SPECIFIC_CATALOG|PARAMETER_SPECIFIC_NAME|PARAMATER_SPECIFIC_SCHEMA|PARTIAL|PASCAL|PENDANT|PLACING|PLI|POSITION|POSTFIX|PRECISION|PREFIX|PREORDER|PREPARE|PRESERVE|PRIMARY|PRIOR|PRIVILEGES|PROCEDURAL|PROCEDURE|PUBLIC|READ|READS|RECHECK|RECURSIVE|REF|REFERENCES|REFERENCING|REINDEX|RELATIVE|RENAME|REPEATABLE|REPLACE|RESET|RESTART|RESTRICT|RESULT|RETURN|RETURNED_LENGTH|RETURNED_OCTET_LENGTH|RETURNED_SQLSTATE|RETURNS|REVOKE|RIGHT|ROLE|ROLLBACK|ROLLUP|ROUTINE|ROUTINE_CATALOG|ROUTINE_NAME|ROUTINE_SCHEMA|ROW|ROWS|ROW_COUNT|RULE|SAVE_POINT|SCALE|SCHEMA|SCHEMA_NAME|SCOPE|SCROLL|SEARCH|SECOND|SECURITY|SELECT|SELF|SENSITIVE|SERIALIZABLE|SERVER_NAME|SESSION|SESSION_USER|SET|SETOF|SETS|SHARE|SHOW|SIMILAR|SIMPLE|SIZE|SOME|SOURCE|SPACE|SPECIFIC|SPECIFICTYPE|SPECIFIC_NAME|SQL|SQLCODE|SQLERROR|SQLEXCEPTION|SQLSTATE|SQLWARNINIG|STABLE|START|STATE|STATEMENT|STATIC|STATISTICS|STDIN|STDOUT|STORAGE|STRICT|STRUCTURE|STYPE|SUBCLASS_ORIGIN|SUBLIST|SUBSTRING|SUM|SYMMETRIC|SYSID|SYSTEM|SYSTEM_USER|TABLE|TABLE_NAME| TEMP|TEMPLATE|TEMPORARY|TERMINATE|THAN|THEN|TIMESTAMP|TIMEZONE_HOUR|TIMEZONE_MINUTE|TO|TOAST|TRAILING|TRANSATION|TRANSACTIONS_COMMITTED|TRANSACTIONS_ROLLED_BACK|TRANSATION_ACTIVE|TRANSFORM|TRANSFORMS|TRANSLATE|TRANSLATION|TREAT|TRIGGER|TRIGGER_CATALOG|TRIGGER_NAME|TRIGGER_SCHEMA|TRIM|TRUE|TRUNCATE|TRUSTED|TYPE|UNCOMMITTED|UNDER|UNENCRYPTED|UNION|UNIQUE|UNKNOWN|UNLISTEN|UNNAMED|UNNEST|UNTIL|UPDATE|UPPER|USAGE|USER|USER_DEFINED_TYPE_CATALOG|USER_DEFINED_TYPE_NAME|USER_DEFINED_TYPE_SCHEMA|USING|VACUUM|VALID|VALIDATOR|VALUES|VARIABLE|VERBOSE|VERSION|VIEW|VOLATILE|WHEN|WHENEVER|WHERE|WITH|WITHOUT|WORK|WRITE|YEAR|ZONE)\\b',
               Keyword),
              (
               '(ARRAY|BIGINT|BINARY|BIT|BLOB|BOOLEAN|CHAR|CHARACTER|DATE|DEC|DECIMAL|FLOAT|INT|INTEGER|INTERVAL|NUMBER|NUMERIC|REAL|SERIAL|SMALLINT|VARCHAR|VARYING|INT8|SERIAL8|TEXT)\\b',
               Name.Builtin),
              (
               '[+*/<>=~!@#%^&|`?^-]', Operator),
              (
               '[0-9]+', Number.Integer),
              (
               "'(''|[^'])*'", String.Single),
              (
               '"(""|[^"])*"', String.Symbol),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Name),
              (
               '[;:()\\[\\],\\.]', Punctuation)], 
       'multiline-comments': [
                            (
                             '/\\*', Comment.Multiline, 'multiline-comments'),
                            (
                             '\\*/', Comment.Multiline, '#pop'),
                            (
                             '[^/\\*]+', Comment.Multiline),
                            (
                             '[/*]', Comment.Multiline)]}


class MySqlLexer(RegexLexer):
    """
    Special lexer for MySQL.
    """
    name = 'MySQL'
    aliases = ['mysql']
    mimetypes = ['text/x-mysql']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '(#|--\\s+).*?\\n', Comment.Single),
              (
               '/\\*', Comment.Multiline, 'multiline-comments'),
              (
               '[0-9]+', Number.Integer),
              (
               '[0-9]*\\.[0-9]+(e[+-][0-9]+)', Number.Float),
              (
               "'(''|[^'])*'", String.Single),
              (
               '"(""|[^"])*"', String.Double),
              (
               '`(``|[^`])*`', String.Symbol),
              (
               '[+*/<>=~!@#%^&|`?^-]', Operator),
              (
               '\\b(tinyint|smallint|mediumint|int|integer|bigint|date|datetime|time|bit|bool|tinytext|mediumtext|longtext|text|tinyblob|mediumblob|longblob|blob|float|double|double\\s+precision|real|numeric|dec|decimal|timestamp|year|char|varchar|varbinary|varcharacter|enum|set)(\\b\\s*)(\\()?',
               bygroups(Keyword.Type, Text, Punctuation)),
              (
               '\\b(add|all|alter|analyze|and|as|asc|asensitive|before|between|bigint|binary|blob|both|by|call|cascade|case|change|char|character|check|collate|column|condition|constraint|continue|convert|create|cross|current_date|current_time|current_timestamp|current_user|cursor|database|databases|day_hour|day_microsecond|day_minute|day_second|dec|decimal|declare|default|delayed|delete|desc|describe|deterministic|distinct|distinctrow|div|double|drop|dual|each|else|elseif|enclosed|escaped|exists|exit|explain|fetch|float|float4|float8|for|force|foreign|from|fulltext|grant|group|having|high_priority|hour_microsecond|hour_minute|hour_second|if|ignore|in|index|infile|inner|inout|insensitive|insert|int|int1|int2|int3|int4|int8|integer|interval|into|is|iterate|join|key|keys|kill|leading|leave|left|like|limit|lines|load|localtime|localtimestamp|lock|long|loop|low_priority|match|minute_microsecond|minute_second|mod|modifies|natural|no_write_to_binlog|not|numeric|on|optimize|option|optionally|or|order|out|outer|outfile|precision|primary|procedure|purge|raid0|read|reads|real|references|regexp|release|rename|repeat|replace|require|restrict|return|revoke|right|rlike|schema|schemas|second_microsecond|select|sensitive|separator|set|show|smallint|soname|spatial|specific|sql|sql_big_result|sql_calc_found_rows|sql_small_result|sqlexception|sqlstate|sqlwarning|ssl|starting|straight_join|table|terminated|then|to|trailing|trigger|undo|union|unique|unlock|unsigned|update|usage|use|using|utc_date|utc_time|utc_timestamp|values|varying|when|where|while|with|write|x509|xor|year_month|zerofill)\\b',
               Keyword),
              (
               '\\b(auto_increment|engine|charset|tables)\\b', Keyword.Pseudo),
              (
               '(true|false|null)', Name.Constant),
              (
               '([a-zA-Z_][a-zA-Z0-9_]*)(\\s*)(\\()',
               bygroups(Name.Function, Text, Punctuation)),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Name),
              (
               '@[A-Za-z0-9]*[._]*[A-Za-z0-9]*', Name.Variable),
              (
               '[;:()\\[\\],\\.]', Punctuation)], 
       'multiline-comments': [
                            (
                             '/\\*', Comment.Multiline, 'multiline-comments'),
                            (
                             '\\*/', Comment.Multiline, '#pop'),
                            (
                             '[^/\\*]+', Comment.Multiline),
                            (
                             '[/*]', Comment.Multiline)]}


class SqliteConsoleLexer(Lexer):
    """
    Lexer for example sessions using sqlite3.

    *New in Pygments 0.11.*
    """
    name = 'sqlite3con'
    aliases = ['sqlite3']
    filenames = ['*.sqlite3-console']
    mimetypes = ['text/x-sqlite3-console']

    def get_tokens_unprocessed(self, data):
        sql = SqlLexer(**self.options)
        curcode = ''
        insertions = []
        for match in line_re.finditer(data):
            line = match.group()
            if line.startswith('sqlite> ') or line.startswith('   ...> '):
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, line[:8])]))
                curcode += line[8:]
            else:
                if curcode:
                    for item in do_insertions(insertions, sql.get_tokens_unprocessed(curcode)):
                        yield item

                    curcode = ''
                    insertions = []
                if line.startswith('SQL error: '):
                    yield (
                     match.start(), Generic.Traceback, line)
                else:
                    yield (
                     match.start(), Generic.Output, line)

        if curcode:
            for item in do_insertions(insertions, sql.get_tokens_unprocessed(curcode)):
                yield item


class BrainfuckLexer(RegexLexer):
    """
    Lexer for the esoteric `BrainFuck <http://www.muppetlabs.com/~breadbox/bf/>`_
    language.
    """
    name = 'Brainfuck'
    aliases = ['brainfuck', 'bf']
    filenames = ['*.bf', '*.b']
    mimetypes = ['application/x-brainfuck']
    tokens = {'common': [
                (
                 '[.,]+', Name.Tag),
                (
                 '[+-]+', Name.Builtin),
                (
                 '[<>]+', Name.Variable),
                (
                 '[^.,+\\-<>\\[\\]]+', Comment)], 
       'root': [
              (
               '\\[', Keyword, 'loop'),
              (
               '\\]', Error),
              include('common')], 
       'loop': [
              (
               '\\[', Keyword, '#push'),
              (
               '\\]', Keyword, '#pop'),
              include('common')]}


class BefungeLexer(RegexLexer):
    """
    Lexer for the esoteric `Befunge <http://en.wikipedia.org/wiki/Befunge>`_
    language.

    *New in Pygments 0.7.*
    """
    name = 'Befunge'
    aliases = ['befunge']
    filenames = ['*.befunge']
    mimetypes = ['application/x-befunge']
    tokens = {'root': [
              (
               '[0-9a-f]', Number),
              (
               '[\\+\\*/%!`-]', Operator),
              (
               '[<>^v?\\[\\]rxjk]', Name.Variable),
              (
               '[:\\\\$.,n]', Name.Builtin),
              (
               '[|_mw]', Keyword),
              (
               '[{}]', Name.Tag),
              (
               '".*?"', String.Double),
              (
               "\\'.", String.Single),
              (
               '[#;]', Comment),
              (
               '[pg&~=@iotsy]', Keyword),
              (
               '[()A-Z]', Comment),
              (
               '\\s+', Text)]}


class BashLexer(RegexLexer):
    """
    Lexer for (ba|k|)sh shell scripts.

    *New in Pygments 0.6.*
    """
    name = 'Bash'
    aliases = ['bash', 'sh', 'ksh']
    filenames = ['*.sh', '*.ksh', '*.bash', '*.ebuild', '*.eclass']
    mimetypes = ['application/x-sh', 'application/x-shellscript']
    tokens = {'root': [
              include('basic'),
              (
               '\\$\\(\\(', Keyword, 'math'),
              (
               '\\$\\(', Keyword, 'paren'),
              (
               '\\${#?', Keyword, 'curly'),
              (
               '`', String.Backtick, 'backticks'),
              include('data')], 
       'basic': [
               (
                '\\b(if|fi|else|while|do|done|for|then|return|function|case|select|continue|until|esac|elif)\\s*\\b',
                Keyword),
               (
                '\\b(alias|bg|bind|break|builtin|caller|cd|command|compgen|complete|declare|dirs|disown|echo|enable|eval|exec|exit|export|false|fc|fg|getopts|hash|help|history|jobs|kill|let|local|logout|popd|printf|pushd|pwd|read|readonly|set|shift|shopt|source|suspend|test|time|times|trap|true|type|typeset|ulimit|umask|unalias|unset|wait)\\s*\\b(?!\\.)',
                Name.Builtin),
               (
                '#.*\\n', Comment),
               (
                '\\\\[\\w\\W]', String.Escape),
               (
                '(\\b\\w+)(\\s*)(=)', bygroups(Name.Variable, Text, Operator)),
               (
                '[\\[\\]{}()=]', Operator),
               (
                "<<-?\\s*(\\'?)\\\\?(\\w+)[\\w\\W]+?\\2", String),
               (
                '&&|\\|\\|', Operator)], 
       'data': [
              (
               '(?s)\\$?"(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\])*"', String.Double),
              (
               "(?s)\\$?'(\\\\\\\\|\\\\[0-7]+|\\\\.|[^'\\\\])*'", String.Single),
              (
               ';', Text),
              (
               '\\s+', Text),
              (
               '[^=\\s\\n\\[\\]{}()$"\\\'`\\\\<]+', Text),
              (
               '\\d+(?= |\\Z)', Number),
              (
               '\\$#?(\\w+|.)', Name.Variable),
              (
               '<', Text)], 
       'curly': [
               (
                '}', Keyword, '#pop'),
               (
                ':-', Keyword),
               (
                '[a-zA-Z0-9_]+', Name.Variable),
               (
                '[^}:"\\\'`$]+', Punctuation),
               (
                ':', Punctuation),
               include('root')], 
       'paren': [
               (
                '\\)', Keyword, '#pop'),
               include('root')], 
       'math': [
              (
               '\\)\\)', Keyword, '#pop'),
              (
               '[-+*/%^|&]|\\*\\*|\\|\\|', Operator),
              (
               '\\d+', Number),
              include('root')], 
       'backticks': [
                   (
                    '`', String.Backtick, '#pop'),
                   include('root')]}

    def analyse_text(text):
        return shebang_matches(text, '(ba|z|)sh')


class BashSessionLexer(Lexer):
    """
    Lexer for simplistic shell sessions.

    *New in Pygments 1.1.*
    """
    name = 'Bash Session'
    aliases = ['console']
    filenames = ['*.sh-session']
    mimetypes = ['application/x-shell-session']

    def get_tokens_unprocessed(self, text):
        bashlexer = BashLexer(**self.options)
        pos = 0
        curcode = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            m = re.match('^((?:|sh\\S*?|\\w+\\S+[@:]\\S+(?:\\s+\\S+)?|\\[\\S+[@:][^\\n]+\\].+)[$#%])(.*\\n?)', line)
            if m:
                if not insertions:
                    pos = match.start()
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, m.group(1))]))
                curcode += m.group(2)
            elif line.startswith('>'):
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, line[:1])]))
                curcode += line[1:]
            else:
                if insertions:
                    toks = bashlexer.get_tokens_unprocessed(curcode)
                    for (i, t, v) in do_insertions(insertions, toks):
                        yield (
                         pos + i, t, v)

                yield (
                 match.start(), Generic.Output, line)
                insertions = []
                curcode = ''

        if insertions:
            for (i, t, v) in do_insertions(insertions, bashlexer.get_tokens_unprocessed(curcode)):
                yield (
                 pos + i, t, v)


class BatchLexer(RegexLexer):
    """
    Lexer for the DOS/Windows Batch file format.

    *New in Pygments 0.7.*
    """
    name = 'Batchfile'
    aliases = ['bat']
    filenames = ['*.bat', '*.cmd']
    mimetypes = ['application/x-dos-batch']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [
              (
               '^\\s*@', Punctuation),
              (
               '^(\\s*)(rem\\s.*)$', bygroups(Text, Comment)),
              (
               '".*?"', String.Double),
              (
               "'.*?'", String.Single),
              (
               '%%?[~$:\\w]+%?', Name.Variable),
              (
               '::.*', Comment),
              (
               '(set)(\\s+)(\\w+)', bygroups(Keyword, Text, Name.Variable)),
              (
               '(call)(\\s+)(:\\w+)', bygroups(Keyword, Text, Name.Label)),
              (
               '(goto)(\\s+)(\\w+)', bygroups(Keyword, Text, Name.Label)),
              (
               '\\b(set|call|echo|on|off|endlocal|for|do|goto|if|pause|setlocal|shift|errorlevel|exist|defined|cmdextversion|errorlevel|else|cd|md|del|deltree|cls|choice)\\b',
               Keyword),
              (
               '\\b(equ|neq|lss|leq|gtr|geq)\\b', Operator),
              include('basic'),
              (
               '.', Text)], 
       'echo': [
              (
               '\\^\\^|\\^<|\\^>|\\^\\|', String.Escape),
              (
               '\\n', Text, '#pop'),
              include('basic'),
              (
               '[^\\\'"^]+', Text)], 
       'basic': [
               (
                '".*?"', String.Double),
               (
                "'.*?'", String.Single),
               (
                '`.*?`', String.Backtick),
               (
                '-?\\d+', Number),
               (
                ',', Punctuation),
               (
                '=', Operator),
               (
                '/\\S+', Name),
               (
                ':\\w+', Name.Label),
               (
                '\\w:\\w+', Text),
               (
                '([<>|])(\\s*)(\\w+)', bygroups(Punctuation, Text, Name))]}


class RedcodeLexer(RegexLexer):
    """
    A simple Redcode lexer based on ICWS'94.
    Contributed by Adam Blinkinsop <blinks@acm.org>.

    *New in Pygments 0.8.*
    """
    name = 'Redcode'
    aliases = ['redcode']
    filenames = ['*.cw']
    opcodes = [
     'DAT', 'MOV', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
     'JMP', 'JMZ', 'JMN', 'DJN', 'CMP', 'SLT', 'SPL',
     'ORG', 'EQU', 'END']
    modifiers = ['A', 'B', 'AB', 'BA', 'F', 'X', 'I']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               ';.*$', Comment.Single),
              (
               '\\b(%s)\\b' % ('|').join(opcodes), Name.Function),
              (
               '\\b(%s)\\b' % ('|').join(modifiers), Name.Decorator),
              (
               '[A-Za-z_][A-Za-z_0-9]+', Name),
              (
               '[-+*/%]', Operator),
              (
               '[#$@<>]', Operator),
              (
               '[.,]', Punctuation),
              (
               '[-+]?\\d+', Number.Integer)]}


class MOOCodeLexer(RegexLexer):
    """
    For `MOOCode <http://www.moo.mud.org/>`_ (the MOO scripting
    language).

    *New in Pygments 0.9.*
    """
    name = 'MOOCode'
    filenames = ['*.moo']
    aliases = ['moocode']
    mimetypes = ['text/x-moocode']
    tokens = {'root': [
              (
               '(0|[1-9][0-9_]*)', Number.Integer),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '(E_PERM|E_DIV)', Name.Exception),
              (
               '((#[-0-9]+)|(\\$[a-z_A-Z0-9]+))', Name.Entity),
              (
               '\\b(if|else|elseif|endif|for|endfor|fork|endfork|while|endwhile|break|continue|return|try|except|endtry|finally|in)\\b',
               Keyword),
              (
               '(random|length)', Name.Builtin),
              (
               '(player|caller|this|args)', Name.Variable.Instance),
              (
               '\\s+', Text),
              (
               '\\n', Text),
              (
               '([!;=,{}&\\|:\\.\\[\\]@\\(\\)\\<\\>\\?]+)', Operator),
              (
               '([a-z_A-Z0-9]+)(\\()', bygroups(Name.Function, Operator)),
              (
               '([a-zA-Z_0-9]+)', Text)]}


class SmalltalkLexer(RegexLexer):
    """
    For `Smalltalk <http://www.smalltalk.org/>`_ syntax.
    Contributed by Stefan Matthias Aust.
    Rewritten by Nils Winter.

    *New in Pygments 0.10.*
    """
    name = 'Smalltalk'
    filenames = ['*.st']
    aliases = ['smalltalk', 'squeak']
    mimetypes = ['text/x-smalltalk']
    tokens = {'root': [
              (
               '(<)(\\w+:)(.*?)(>)', bygroups(Text, Keyword, Text, Text)),
              include('squeak fileout'),
              include('whitespaces'),
              include('method definition'),
              (
               '(\\|)([\\w\\s]*)(\\|)', bygroups(Operator, Name.Variable, Operator)),
              include('objects'),
              (
               '\\^|\\:=|\\_', Operator),
              (
               '[\\]({}.;!]', Text)], 
       'method definition': [
                           (
                            '([a-zA-Z]+\\w*:)(\\s*)(\\w+)',
                            bygroups(Name.Function, Text, Name.Variable)),
                           (
                            '^(\\b[a-zA-Z]+\\w*\\b)(\\s*)$', bygroups(Name.Function, Text)),
                           (
                            '^([-+*/\\\\~<>=|&!?,@%]+)(\\s*)(\\w+)(\\s*)$',
                            bygroups(Name.Function, Text, Name.Variable, Text))], 
       'blockvariables': [
                        include('whitespaces'),
                        (
                         '(:)(\\s*)([A-Za-z\\w]+)',
                         bygroups(Operator, Text, Name.Variable)),
                        (
                         '\\|', Operator, '#pop'),
                        (
                         '', Text, '#pop')], 
       'literals': [
                  (
                   "\\'[^\\']*\\'", String, 'afterobject'),
                  (
                   '\\$.', String.Char, 'afterobject'),
                  (
                   '#\\(', String.Symbol, 'parenth'),
                  (
                   '\\)', Text, 'afterobject'),
                  (
                   '(\\d+r)?-?\\d+(\\.\\d+)?(e-?\\d+)?', Number, 'afterobject')], 
       '_parenth_helper': [
                         include('whitespaces'),
                         (
                          '(\\d+r)?-?\\d+(\\.\\d+)?(e-?\\d+)?', Number),
                         (
                          '[-+*/\\\\~<>=|&#!?,@%\\w+:]+', String.Symbol),
                         (
                          "\\'[^\\']*\\'", String),
                         (
                          '\\$.', String.Char),
                         (
                          '#*\\(', String.Symbol, 'inner_parenth')], 
       'parenth': [
                 (
                  '\\)', String.Symbol, ('root', 'afterobject')),
                 include('_parenth_helper')], 
       'inner_parenth': [
                       (
                        '\\)', String.Symbol, '#pop'),
                       include('_parenth_helper')], 
       'whitespaces': [
                     (
                      '\\s+', Text),
                     (
                      '"[^"]*"', Comment)], 
       'objects': [
                 (
                  '\\[', Text, 'blockvariables'),
                 (
                  '\\]', Text, 'afterobject'),
                 (
                  '\\b(self|super|true|false|nil|thisContext)\\b',
                  Name.Builtin.Pseudo, 'afterobject'),
                 (
                  '\\b[A-Z]\\w*(?!:)\\b', Name.Class, 'afterobject'),
                 (
                  '\\b[a-z]\\w*(?!:)\\b', Name.Variable, 'afterobject'),
                 (
                  '#("[^"]*"|[-+*/\\\\~<>=|&!?,@%]+|[\\w:]+)',
                  String.Symbol, 'afterobject'),
                 include('literals')], 
       'afterobject': [
                     (
                      '! !$', Keyword, '#pop'),
                     include('whitespaces'),
                     (
                      '\\b(ifTrue:|ifFalse:|whileTrue:|whileFalse:|timesRepeat:)',
                      Name.Builtin, '#pop'),
                     (
                      '\\b(new\\b(?!:))', Name.Builtin),
                     (
                      '\\:=|\\_', Operator, '#pop'),
                     (
                      '\\b[a-zA-Z]+\\w*:', Name.Function, '#pop'),
                     (
                      '\\b[a-zA-Z]+\\w*', Name.Function),
                     (
                      '\\w+:?|[-+*/\\\\~<>=|&!?,@%]+', Name.Function, '#pop'),
                     (
                      '\\.', Punctuation, '#pop'),
                     (
                      ';', Punctuation),
                     (
                      '[\\])}]', Text),
                     (
                      '[\\[({]', Text, '#pop')], 
       'squeak fileout': [
                        (
                         '^"[^"]*"!', Keyword),
                        (
                         "^'[^']*'!", Keyword),
                        (
                         '^(!)(\\w+)( commentStamp: )(.*?)( prior: .*?!\\n)(.*?)(!)',
                         bygroups(Keyword, Name.Class, Keyword, String, Keyword, Text, Keyword)),
                        (
                         "^(!)(\\w+(?: class)?)( methodsFor: )(\\'[^\\']*\\')(.*?!)",
                         bygroups(Keyword, Name.Class, Keyword, String, Keyword)),
                        (
                         '^(\\w+)( subclass: )(#\\w+)(\\s+instanceVariableNames: )(.*?)(\\s+classVariableNames: )(.*?)(\\s+poolDictionaries: )(.*?)(\\s+category: )(.*?)(!)',
                         bygroups(Name.Class, Keyword, String.Symbol, Keyword, String, Keyword, String, Keyword, String, Keyword, String, Keyword)),
                        (
                         '^(\\w+(?: class)?)(\\s+instanceVariableNames: )(.*?)(!)',
                         bygroups(Name.Class, Keyword, String, Keyword)),
                        (
                         '(!\\n)(\\].*)(! !)$', bygroups(Keyword, Text, Keyword)),
                        (
                         '! !$', Keyword)]}


class TcshLexer(RegexLexer):
    """
    Lexer for tcsh scripts.

    *New in Pygments 0.10.*
    """
    name = 'Tcsh'
    aliases = ['tcsh', 'csh']
    filenames = ['*.tcsh', '*.csh']
    mimetypes = ['application/x-csh']
    tokens = {'root': [
              include('basic'),
              (
               '\\$\\(', Keyword, 'paren'),
              (
               '\\${#?', Keyword, 'curly'),
              (
               '`', String.Backtick, 'backticks'),
              include('data')], 
       'basic': [
               (
                '\\b(if|endif|else|while|then|foreach|case|default|continue|goto|breaksw|end|switch|endsw)\\s*\\b',
                Keyword),
               (
                '\\b(alias|alloc|bg|bindkey|break|builtins|bye|caller|cd|chdir|complete|dirs|echo|echotc|eval|exec|exit|fg|filetest|getxvers|glob|getspath|hashstat|history|hup|inlib|jobs|kill|limit|log|login|logout|ls-F|migrate|newgrp|nice|nohup|notify|onintr|popd|printenv|pushd|rehash|repeat|rootnode|popd|pushd|set|shift|sched|setenv|setpath|settc|setty|setxvers|shift|source|stop|suspend|source|suspend|telltc|time|umask|unalias|uncomplete|unhash|universe|unlimit|unset|unsetenv|ver|wait|warp|watchlog|where|which)\\s*\\b',
                Name.Builtin),
               (
                '#.*\\n', Comment),
               (
                '\\\\[\\w\\W]', String.Escape),
               (
                '(\\b\\w+)(\\s*)(=)', bygroups(Name.Variable, Text, Operator)),
               (
                '[\\[\\]{}()=]+', Operator),
               (
                "<<\\s*(\\'?)\\\\?(\\w+)[\\w\\W]+?\\2", String)], 
       'data': [
              (
               '(?s)"(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\])*"', String.Double),
              (
               "(?s)'(\\\\\\\\|\\\\[0-7]+|\\\\.|[^'\\\\])*'", String.Single),
              (
               '\\s+', Text),
              (
               '[^=\\s\\n\\[\\]{}()$"\\\'`\\\\]+', Text),
              (
               '\\d+(?= |\\Z)', Number),
              (
               '\\$#?(\\w+|.)', Name.Variable)], 
       'curly': [
               (
                '}', Keyword, '#pop'),
               (
                ':-', Keyword),
               (
                '[a-zA-Z0-9_]+', Name.Variable),
               (
                '[^}:"\\\'`$]+', Punctuation),
               (
                ':', Punctuation),
               include('root')], 
       'paren': [
               (
                '\\)', Keyword, '#pop'),
               include('root')], 
       'backticks': [
                   (
                    '`', String.Backtick, '#pop'),
                   include('root')]}


class LogtalkLexer(RegexLexer):
    """
    For `Logtalk <http://logtalk.org/>`_ source code.

    *New in Pygments 0.10.*
    """
    name = 'Logtalk'
    aliases = ['logtalk']
    filenames = ['*.lgt']
    mimetypes = ['text/x-logtalk']
    tokens = {'root': [
              (
               '^\\s*:-\\s', Punctuation, 'directive'),
              (
               '%.*?\\n', Comment),
              (
               '/\\*(.|\\n)*?\\*/', Comment),
              (
               '\\n', Text),
              (
               '\\s+', Text),
              (
               "0'.", Number),
              (
               '0b[01]+', Number),
              (
               '0o[0-7]+', Number),
              (
               '0x[0-9a-fA-F]+', Number),
              (
               '\\d+\\.?\\d*((e|E)(\\+|-)?\\d+)?', Number),
              (
               '([A-Z_][a-zA-Z0-9_]*)', Name.Variable),
              (
               '(after|before)(?=[(])', Keyword),
              (
               '(parameter|this|se(lf|nder))(?=[(])', Keyword),
              (
               '(current_predicate|predicate_property)(?=[(])', Keyword),
              (
               '(expand_(goal|term)|(goal|term)_expansion|phrase)(?=[(])',
               Keyword),
              (
               '(abolish|c(reate|urrent))_(object|protocol|category)(?=[(])',
               Keyword),
              (
               '(object|protocol|category)_property(?=[(])', Keyword),
              (
               'complements_object(?=[(])', Keyword),
              (
               'extends_(object|protocol|category)(?=[(])', Keyword),
              (
               'imp(lements_protocol|orts_category)(?=[(])', Keyword),
              (
               '(instantiat|specializ)es_class(?=[(])', Keyword),
              (
               '(current_event|(abolish|define)_events)(?=[(])', Keyword),
              (
               '(current|set)_logtalk_flag(?=[(])', Keyword),
              (
               'logtalk_(compile|l(ibrary_path|oad))(?=[(])', Keyword),
              (
               '(clause|retract(all)?)(?=[(])', Keyword),
              (
               'a(bolish|ssert(a|z))(?=[(])', Keyword),
              (
               '(ca(ll|tch)|throw)(?=[(])', Keyword),
              (
               '(fail|true)\\b', Keyword),
              (
               '((bag|set)of|f(ind|or)all)(?=[(])', Keyword),
              (
               'threaded(_(call|once|ignore|exit|peek|wait|notify))?(?=[(])',
               Keyword),
              (
               'unify_with_occurs_check(?=[(])', Keyword),
              (
               '(functor|arg|copy_term)(?=[(])', Keyword),
              (
               '(rem|mod|abs|sign)(?=[(])', Keyword),
              (
               'float(_(integer|fractional)_part)?(?=[(])', Keyword),
              (
               '(floor|truncate|round|ceiling)(?=[(])', Keyword),
              (
               '(cos|atan|exp|log|s(in|qrt))(?=[(])', Keyword),
              (
               '(var|atom(ic)?|integer|float|compound|n(onvar|umber))(?=[(])',
               Keyword),
              (
               '(curren|se)t_(in|out)put(?=[(])', Keyword),
              (
               '(open|close)(?=[(])', Keyword),
              (
               'flush_output(?=[(])', Keyword),
              (
               '(at_end_of_stream|flush_output)\\b', Keyword),
              (
               '(stream_property|at_end_of_stream|set_stream_position)(?=[(])',
               Keyword),
              (
               '(nl|(get|peek|put)_(byte|c(har|ode)))(?=[(])', Keyword),
              (
               '\\bnl\\b', Keyword),
              (
               'read(_term)?(?=[(])', Keyword),
              (
               'write(q|_(canonical|term))?(?=[(])', Keyword),
              (
               '(current_)?op(?=[(])', Keyword),
              (
               '(current_)?char_conversion(?=[(])', Keyword),
              (
               'atom_(length|c(hars|o(ncat|des)))(?=[(])', Keyword),
              (
               '(char_code|sub_atom)(?=[(])', Keyword),
              (
               'number_c(har|ode)s(?=[(])', Keyword),
              (
               '(se|curren)t_prolog_flag(?=[(])', Keyword),
              (
               '\\bhalt\\b', Keyword),
              (
               'halt(?=[(])', Keyword),
              (
               '(::|:|\\^\\^)', Operator),
              (
               '[{}]', Keyword),
              (
               '\\bonce(?=[(])', Keyword),
              (
               '\\brepeat\\b', Keyword),
              (
               '(>>|<<|/\\\\|\\\\\\\\|\\\\)', Operator),
              (
               '\\bis\\b', Keyword),
              (
               '(=:=|=\\\\=|<|=<|>=|>)', Operator),
              (
               '=\\.\\.', Operator),
              (
               '(=|\\\\=)', Operator),
              (
               '(==|\\\\==|@=<|@<|@>=|@>)', Operator),
              (
               '(//|[-+*/])', Operator),
              (
               '\\b(mod|rem)\\b', Operator),
              (
               '\\b\\*\\*\\b', Operator),
              (
               '-->', Operator),
              (
               '([!;]|->)', Operator),
              (
               '\\\\+', Operator),
              (
               '[?@]', Operator),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '[()\\[\\],.|]', Text),
              (
               '[a-z][a-zA-Z0-9_]*', Text),
              (
               "[']", String, 'quoted_atom')], 
       'quoted_atom': [
                     (
                      "['][']", String),
                     (
                      "[']", String, '#pop'),
                     (
                      '\\\\([\\\\abfnrtv"\\\']|(x[a-fA-F0-9]+|[0-7]+)\\\\)', String.Escape),
                     (
                      "[^\\\\'\\n]+", String),
                     (
                      '\\\\', String)], 
       'directive': [
                   (
                    '(el)?if(?=[(])', Keyword, 'root'),
                   (
                    '(e(lse|ndif))[.]', Keyword, 'root'),
                   (
                    '(category|object|protocol)(?=[(])', Keyword, 'entityrelations'),
                   (
                    '(end_(category|object|protocol))[.]', Keyword, 'root'),
                   (
                    '(public|protected|private)(?=[(])', Keyword, 'root'),
                   (
                    'e(n(coding|sure_loaded)|xport)(?=[(])', Keyword, 'root'),
                   (
                    'in(fo|itialization)(?=[(])', Keyword, 'root'),
                   (
                    '(dynamic|synchronized|threaded)[.]', Keyword, 'root'),
                   (
                    '(alias|d(ynamic|iscontiguous)|m(eta_predicate|ode|ultifile)|s(et_(logtalk|prolog)_flag|ynchronized))(?=[(])',
                    Keyword, 'root'),
                   (
                    'op(?=[(])', Keyword, 'root'),
                   (
                    '(calls|reexport|use(s|_module))(?=[(])', Keyword, 'root'),
                   (
                    '[a-z][a-zA-Z0-9_]*(?=[(])', Text, 'root'),
                   (
                    '[a-z][a-zA-Z0-9_]*[.]', Text, 'root')], 
       'entityrelations': [
                         (
                          '(extends|i(nstantiates|mp(lements|orts))|specializes)(?=[(])',
                          Keyword),
                         (
                          "0'.", Number),
                         (
                          '0b[01]+', Number),
                         (
                          '0o[0-7]+', Number),
                         (
                          '0x[0-9a-fA-F]+', Number),
                         (
                          '\\d+\\.?\\d*((e|E)(\\+|-)?\\d+)?', Number),
                         (
                          '([A-Z_][a-zA-Z0-9_]*)', Name.Variable),
                         (
                          '[a-z][a-zA-Z0-9_]*', Text),
                         (
                          "[']", String, 'quoted_atom'),
                         (
                          '"(\\\\\\\\|\\\\"|[^"])*"', String),
                         (
                          '([)]\\.)', Text, 'root'),
                         (
                          '(::)', Operator),
                         (
                          '[()\\[\\],.|]', Text),
                         (
                          '%.*?\\n', Comment),
                         (
                          '/\\*(.|\\n)*?\\*/', Comment),
                         (
                          '\\n', Text),
                         (
                          '\\s+', Text)]}

    def analyse_text(text):
        if ':- object(' in text:
            return True
        if ':- protocol(' in text:
            return True
        if ':- category(' in text:
            return True
        return False


def _shortened(word):
    dpos = word.find('$')
    return ('|').join([ word[:dpos] + word[dpos + 1:i] + '\\b' for i in range(len(word), dpos, -1)
                      ])


def _shortened_many(*words):
    return ('|').join(map(_shortened, words))


class GnuplotLexer(RegexLexer):
    """
    For `Gnuplot <http://gnuplot.info/>`_ plotting scripts.

    *New in Pygments 0.11.*
    """
    name = 'Gnuplot'
    aliases = ['gnuplot']
    filenames = ['*.plot', '*.plt']
    mimetypes = ['text/x-gnuplot']
    tokens = {'root': [
              include('whitespace'),
              (
               _shortened('bi$nd'), Keyword, 'bind'),
              (
               _shortened_many('ex$it', 'q$uit'), Keyword, 'quit'),
              (
               _shortened('f$it'), Keyword, 'fit'),
              (
               '(if)(\\s*)(\\()', bygroups(Keyword, Text, Punctuation), 'if'),
              (
               'else\\b', Keyword),
              (
               _shortened('pa$use'), Keyword, 'pause'),
              (
               _shortened_many('p$lot', 'rep$lot', 'sp$lot'), Keyword, 'plot'),
              (
               _shortened('sa$ve'), Keyword, 'save'),
              (
               _shortened('se$t'), Keyword, ('genericargs', 'optionarg')),
              (
               _shortened_many('sh$ow', 'uns$et'),
               Keyword, ('noargs', 'optionarg')),
              (
               _shortened_many('low$er', 'ra$ise', 'ca$ll', 'cd$', 'cl$ear', 'h$elp', '\\?$', 'hi$story', 'l$oad', 'pr$int', 'pwd$', 're$read', 'res$et', 'scr$eendump', 'she$ll', 'sy$stem', 'up$date'),
               Keyword, 'genericargs'),
              (
               _shortened_many('pwd$', 're$read', 'res$et', 'scr$eendump', 'she$ll', 'test$'),
               Keyword, 'noargs'),
              (
               '([a-zA-Z_][a-zA-Z0-9_]*)(\\s*)(=)',
               bygroups(Name.Variable, Text, Operator), 'genericargs'),
              (
               '([a-zA-Z_][a-zA-Z0-9_]*)(\\s*\\(.*?\\)\\s*)(=)',
               bygroups(Name.Function, Text, Operator), 'genericargs'),
              (
               '@[a-zA-Z_][a-zA-Z0-9_]*', Name.Constant),
              (
               ';', Keyword)], 
       'comment': [
                 (
                  '[^\\\\\\n]', Comment),
                 (
                  '\\\\\\n', Comment),
                 (
                  '\\\\', Comment),
                 (
                  '', Comment, '#pop')], 
       'whitespace': [
                    (
                     '#', Comment, 'comment'),
                    (
                     '[ \\t\\v\\f]+', Text)], 
       'noargs': [
                include('whitespace'),
                (
                 ';', Punctuation, '#pop'),
                (
                 '\\n', Text, '#pop')], 
       'dqstring': [
                  (
                   '"', String, '#pop'),
                  (
                   '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                  (
                   '[^\\\\"\\n]+', String),
                  (
                   '\\\\\\n', String),
                  (
                   '\\\\', String),
                  (
                   '\\n', String, '#pop')], 
       'sqstring': [
                  (
                   "''", String),
                  (
                   "'", String, '#pop'),
                  (
                   "[^\\\\'\\n]+", String),
                  (
                   '\\\\\\n', String),
                  (
                   '\\\\', String),
                  (
                   '\\n', String, '#pop')], 
       'genericargs': [
                     include('noargs'),
                     (
                      '"', String, 'dqstring'),
                     (
                      "'", String, 'sqstring'),
                     (
                      '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+', Number.Float),
                     (
                      '(\\d+\\.\\d*|\\.\\d+)', Number.Float),
                     (
                      '-?\\d+', Number.Integer),
                     (
                      '[,.~!%^&*+=|?:<>/-]', Operator),
                     (
                      '[{}()\\[\\]]', Punctuation),
                     (
                      '(eq|ne)\\b', Operator.Word),
                     (
                      '([a-zA-Z_][a-zA-Z0-9_]*)(\\s*)(\\()',
                      bygroups(Name.Function, Text, Punctuation)),
                     (
                      '[a-zA-Z_][a-zA-Z0-9_]*', Name),
                     (
                      '@[a-zA-Z_][a-zA-Z0-9_]*', Name.Constant),
                     (
                      '\\\\\\n', Text)], 
       'optionarg': [
                   include('whitespace'),
                   (
                    _shortened_many('a$ll', 'an$gles', 'ar$row', 'au$toscale', 'b$ars', 'bor$der', 'box$width', 'cl$abel', 'c$lip', 'cn$trparam', 'co$ntour', 'da$ta', 'data$file', 'dg$rid3d', 'du$mmy', 'enc$oding', 'dec$imalsign', 'fit$', 'font$path', 'fo$rmat', 'fu$nction', 'fu$nctions', 'g$rid', 'hid$den3d', 'his$torysize', 'is$osamples', 'k$ey', 'keyt$itle', 'la$bel', 'li$nestyle', 'ls$', 'loa$dpath', 'loc$ale', 'log$scale', 'mac$ros', 'map$ping', 'map$ping3d', 'mar$gin', 'lmar$gin', 'rmar$gin', 'tmar$gin', 'bmar$gin', 'mo$use', 'multi$plot', 'mxt$ics', 'nomxt$ics', 'mx2t$ics', 'nomx2t$ics', 'myt$ics', 'nomyt$ics', 'my2t$ics', 'nomy2t$ics', 'mzt$ics', 'nomzt$ics', 'mcbt$ics', 'nomcbt$ics', 'of$fsets', 'or$igin', 'o$utput', 'pa$rametric', 'pm$3d', 'pal$ette', 'colorb$ox', 'p$lot', 'poi$ntsize', 'pol$ar', 'pr$int', 'obj$ect', 'sa$mples', 'si$ze', 'st$yle', 'su$rface', 'table$', 't$erminal', 'termo$ptions', 'ti$cs', 'ticsc$ale', 'ticsl$evel', 'timef$mt', 'tim$estamp', 'tit$le', 'v$ariables', 've$rsion', 'vi$ew', 'xyp$lane', 'xda$ta', 'x2da$ta', 'yda$ta', 'y2da$ta', 'zda$ta', 'cbda$ta', 'xl$abel', 'x2l$abel', 'yl$abel', 'y2l$abel', 'zl$abel', 'cbl$abel', 'xti$cs', 'noxti$cs', 'x2ti$cs', 'nox2ti$cs', 'yti$cs', 'noyti$cs', 'y2ti$cs', 'noy2ti$cs', 'zti$cs', 'nozti$cs', 'cbti$cs', 'nocbti$cs', 'xdti$cs', 'noxdti$cs', 'x2dti$cs', 'nox2dti$cs', 'ydti$cs', 'noydti$cs', 'y2dti$cs', 'noy2dti$cs', 'zdti$cs', 'nozdti$cs', 'cbdti$cs', 'nocbdti$cs', 'xmti$cs', 'noxmti$cs', 'x2mti$cs', 'nox2mti$cs', 'ymti$cs', 'noymti$cs', 'y2mti$cs', 'noy2mti$cs', 'zmti$cs', 'nozmti$cs', 'cbmti$cs', 'nocbmti$cs', 'xr$ange', 'x2r$ange', 'yr$ange', 'y2r$ange', 'zr$ange', 'cbr$ange', 'rr$ange', 'tr$ange', 'ur$ange', 'vr$ange', 'xzeroa$xis', 'x2zeroa$xis', 'yzeroa$xis', 'y2zeroa$xis', 'zzeroa$xis', 'zeroa$xis', 'z$ero'), Name.Builtin, '#pop')], 
       'bind': [
              (
               '!', Keyword, '#pop'),
              (
               _shortened('all$windows'), Name.Builtin),
              include('genericargs')], 
       'quit': [
              (
               'gnuplot\\b', Keyword),
              include('noargs')], 
       'fit': [
             (
              'via\\b', Name.Builtin),
             include('plot')], 
       'if': [
            (
             '\\)', Punctuation, '#pop'),
            include('genericargs')], 
       'pause': [
               (
                '(mouse|any|button1|button2|button3)\\b', Name.Builtin),
               (
                _shortened('key$press'), Name.Builtin),
               include('genericargs')], 
       'plot': [
              (
               _shortened_many('ax$es', 'axi$s', 'bin$ary', 'ev$ery', 'i$ndex', 'mat$rix', 's$mooth', 'thru$', 't$itle', 'not$itle', 'u$sing', 'w$ith'),
               Name.Builtin),
              include('genericargs')], 
       'save': [
              (
               _shortened_many('f$unctions', 's$et', 't$erminal', 'v$ariables'),
               Name.Builtin),
              include('genericargs')]}


class PovrayLexer(RegexLexer):
    """
    For `Persistence of Vision Raytracer <http://www.povray.org/>`_ files.

    *New in Pygments 0.11.*
    """
    name = 'POVRay'
    aliases = ['pov']
    filenames = ['*.pov', '*.inc']
    mimetypes = ['text/x-povray']
    tokens = {'root': [
              (
               '/\\*[\\w\\W]*?\\*/', Comment.Multiline),
              (
               '//.*\\n', Comment.Single),
              (
               '(?s)"(?:\\\\.|[^"\\\\])+"', String.Double),
              (
               '#(debug|default|else|end|error|fclose|fopen|if|ifdef|ifndef|include|range|read|render|statistics|switch|undef|version|warning|while|write|define|macro|local|declare)',
               Comment.Preproc),
              (
               '\\b(aa_level|aa_threshold|abs|acos|acosh|adaptive|adc_bailout|agate|agate_turb|all|alpha|ambient|ambient_light|angle|aperture|arc_angle|area_light|asc|asin|asinh|assumed_gamma|atan|atan2|atanh|atmosphere|atmospheric_attenuation|attenuating|average|background|black_hole|blue|blur_samples|bounded_by|box_mapping|bozo|break|brick|brick_size|brightness|brilliance|bumps|bumpy1|bumpy2|bumpy3|bump_map|bump_size|case|caustics|ceil|checker|chr|clipped_by|clock|color|color_map|colour|colour_map|component|composite|concat|confidence|conic_sweep|constant|control0|control1|cos|cosh|count|crackle|crand|cube|cubic_spline|cylindrical_mapping|debug|declare|default|degrees|dents|diffuse|direction|distance|distance_maximum|div|dust|dust_type|eccentricity|else|emitting|end|error|error_bound|exp|exponent|fade_distance|fade_power|falloff|falloff_angle|false|file_exists|filter|finish|fisheye|flatness|flip|floor|focal_point|fog|fog_alt|fog_offset|fog_type|frequency|gif|global_settings|glowing|gradient|granite|gray_threshold|green|halo|hexagon|hf_gray_16|hierarchy|hollow|hypercomplex|if|ifdef|iff|image_map|incidence|include|int|interpolate|inverse|ior|irid|irid_wavelength|jitter|lambda|leopard|linear|linear_spline|linear_sweep|location|log|looks_like|look_at|low_error_factor|mandel|map_type|marble|material_map|matrix|max|max_intersections|max_iteration|max_trace_level|max_value|metallic|min|minimum_reuse|mod|mortar|nearest_count|no|normal|normal_map|no_shadow|number_of_waves|octaves|off|offset|omega|omnimax|on|once|onion|open|orthographic|panoramic|pattern1|pattern2|pattern3|perspective|pgm|phase|phong|phong_size|pi|pigment|pigment_map|planar_mapping|png|point_at|pot|pow|ppm|precision|pwr|quadratic_spline|quaternion|quick_color|quick_colour|quilted|radial|radians|radiosity|radius|rainbow|ramp_wave|rand|range|reciprocal|recursion_limit|red|reflection|refraction|render|repeat|rgb|rgbf|rgbft|rgbt|right|ripples|rotate|roughness|samples|scale|scallop_wave|scattering|seed|shadowless|sin|sine_wave|sinh|sky|sky_sphere|slice|slope_map|smooth|specular|spherical_mapping|spiral|spiral1|spiral2|spotlight|spotted|sqr|sqrt|statistics|str|strcmp|strength|strlen|strlwr|strupr|sturm|substr|switch|sys|t|tan|tanh|test_camera_1|test_camera_2|test_camera_3|test_camera_4|texture|texture_map|tga|thickness|threshold|tightness|tile2|tiles|track|transform|translate|transmit|triangle_wave|true|ttf|turbulence|turb_depth|type|ultra_wide_angle|up|use_color|use_colour|use_index|u_steps|val|variance|vaxis_rotate|vcross|vdot|version|vlength|vnormalize|volume_object|volume_rendered|vol_with_light|vrotate|v_steps|warning|warp|water_level|waves|while|width|wood|wrinkles|yes)\\b',
               Keyword),
              (
               'bicubic_patch|blob|box|camera|cone|cubic|cylinder|difference|disc|height_field|intersection|julia_fractal|lathe|light_source|merge|mesh|object|plane|poly|polygon|prism|quadric|quartic|smooth_triangle|sor|sphere|superellipsoid|text|torus|triangle|union',
               Name.Builtin),
              (
               '[\\[\\](){}<>;,]', Punctuation),
              (
               '[-+*/=]', Operator),
              (
               '\\b(x|y|z|u|v)\\b', Name.Builtin.Pseudo),
              (
               '[a-zA-Z_][a-zA-Z_0-9]*', Name),
              (
               '[0-9]+\\.[0-9]*', Number.Float),
              (
               '\\.[0-9]+', Number.Float),
              (
               '[0-9]+', Number.Integer),
              (
               '\\s+', Text)]}


class AppleScriptLexer(RegexLexer):
    """
    For `AppleScript source code
    <http://developer.apple.com/documentation/AppleScript/
    Conceptual/AppleScriptLangGuide>`_,
    including `AppleScript Studio
    <http://developer.apple.com/documentation/AppleScript/
    Reference/StudioReference>`_.
    Contributed by Andreas Amann <aamann@mac.com>.
    """
    name = 'AppleScript'
    aliases = ['applescript']
    filenames = ['*.applescript']
    flags = re.MULTILINE | re.DOTALL
    Identifiers = '[a-zA-Z]\\w*'
    Literals = ['AppleScript', 'current application', 'false', 'linefeed',
     'missing value', 'pi', 'quote', 'result', 'return', 'space',
     'tab', 'text item delimiters', 'true', 'version']
    Classes = ['alias ', 'application ', 'boolean ', 'class ', 'constant ',
     'date ', 'file ', 'integer ', 'list ', 'number ', 'POSIX file ',
     'real ', 'record ', 'reference ', 'RGB color ', 'script ',
     'text ', 'unit types', '(Unicode )?text', 'string']
    BuiltIn = ['attachment', 'attribute run', 'character', 'day', 'month',
     'paragraph', 'word', 'year']
    HandlerParams = ['about', 'above', 'against', 'apart from', 'around',
     'aside from', 'at', 'below', 'beneath', 'beside',
     'between', 'for', 'given', 'instead of', 'on', 'onto',
     'out of', 'over', 'since']
    Commands = ['ASCII (character|number)', 'activate', 'beep', 'choose URL',
     'choose application', 'choose color', 'choose file( name)?',
     'choose folder', 'choose from list',
     'choose remote application', 'clipboard info',
     'close( access)?', 'copy', 'count', 'current date', 'delay',
     'delete', 'display (alert|dialog)', 'do shell script',
     'duplicate', 'exists', 'get eof', 'get volume settings',
     'info for', 'launch', 'list (disks|folder)', 'load script',
     'log', 'make', 'mount volume', 'new', 'offset',
     'open( (for access|location))?', 'path to', 'print', 'quit',
     'random number', 'read', 'round', 'run( script)?',
     'say', 'scripting components',
     'set (eof|the clipboard to|volume)', 'store script',
     'summarize', 'system attribute', 'system info',
     'the clipboard', 'time to GMT', 'write', 'quoted form']
    References = ['(in )?back of', '(in )?front of', '[0-9]+(st|nd|rd|th)',
     'first', 'second', 'third', 'fourth', 'fifth', 'sixth',
     'seventh', 'eighth', 'ninth', 'tenth', 'after', 'back',
     'before', 'behind', 'every', 'front', 'index', 'last',
     'middle', 'some', 'that', 'through', 'thru', 'where', 'whose']
    Operators = ['and', 'or', 'is equal', 'equals', '(is )?equal to', 'is not',
     "isn't", "isn't equal( to)?", 'is not equal( to)?',
     "doesn't equal", 'does not equal', '(is )?greater than',
     'comes after', 'is not less than or equal( to)?',
     "isn't less than or equal( to)?", '(is )?less than',
     'comes before', 'is not greater than or equal( to)?',
     "isn't greater than or equal( to)?",
     '(is  )?greater than or equal( to)?', 'is not less than',
     "isn't less than", 'does not come before',
     "doesn't come before", '(is )?less than or equal( to)?',
     'is not greater than', "isn't greater than",
     'does not come after', "doesn't come after", 'starts? with',
     'begins? with', 'ends? with', 'contains?', 'does not contain',
     "doesn't contain", 'is in', 'is contained by', 'is not in',
     'is not contained by', "isn't contained by", 'div', 'mod',
     'not', '(a  )?(ref( to)?|reference to)', 'is', 'does']
    Control = ['considering', 'else', 'error', 'exit', 'from', 'if',
     'ignoring', 'in', 'repeat', 'tell', 'then', 'times', 'to',
     'try', 'until', 'using terms from', 'while', 'whith',
     'with timeout( of)?', 'with transaction', 'by', 'continue',
     'end', 'its?', 'me', 'my', 'return', 'of', 'as']
    Declarations = ['global', 'local', 'prop(erty)?', 'set', 'get']
    Reserved = ['but', 'put', 'returning', 'the']
    StudioClasses = ['action cell', 'alert reply', 'application', 'box',
     'browser( cell)?', 'bundle', 'button( cell)?', 'cell',
     'clip view', 'color well', 'color-panel',
     'combo box( item)?', 'control',
     'data( (cell|column|item|row|source))?', 'default entry',
     'dialog reply', 'document', 'drag info', 'drawer',
     'event', 'font(-panel)?', 'formatter',
     'image( (cell|view))?', 'matrix', 'menu( item)?', 'item',
     'movie( view)?', 'open-panel', 'outline view', 'panel',
     'pasteboard', 'plugin', 'popup button',
     'progress indicator', 'responder', 'save-panel',
     'scroll view', 'secure text field( cell)?', 'slider',
     'sound', 'split view', 'stepper', 'tab view( item)?',
     'table( (column|header cell|header view|view))',
     'text( (field( cell)?|view))?', 'toolbar( item)?',
     'user-defaults', 'view', 'window']
    StudioEvents = ['accept outline drop', 'accept table drop', 'action',
     'activated', 'alert ended', 'awake from nib', 'became key',
     'became main', 'begin editing', 'bounds changed',
     'cell value', 'cell value changed', 'change cell value',
     'change item value', 'changed', 'child of item',
     'choose menu item', 'clicked', 'clicked toolbar item',
     'closed', 'column clicked', 'column moved',
     'column resized', 'conclude drop', 'data representation',
     'deminiaturized', 'dialog ended', 'document nib name',
     'double clicked', 'drag( (entered|exited|updated))?',
     'drop', 'end editing', 'exposed', 'idle', 'item expandable',
     'item value', 'item value changed', 'items changed',
     'keyboard down', 'keyboard up', 'launched',
     'load data representation', 'miniaturized', 'mouse down',
     'mouse dragged', 'mouse entered', 'mouse exited',
     'mouse moved', 'mouse up', 'moved',
     'number of browser rows', 'number of items',
     'number of rows', 'open untitled', 'opened', 'panel ended',
     'parameters updated', 'plugin loaded', 'prepare drop',
     'prepare outline drag', 'prepare outline drop',
     'prepare table drag', 'prepare table drop',
     'read from file', 'resigned active', 'resigned key',
     'resigned main', 'resized( sub views)?',
     'right mouse down', 'right mouse dragged',
     'right mouse up', 'rows changed', 'scroll wheel',
     'selected tab view item', 'selection changed',
     'selection changing', 'should begin editing',
     'should close', 'should collapse item',
     'should end editing', 'should expand item',
     'should open( untitled)?',
     'should quit( after last window closed)?',
     'should select column', 'should select item',
     'should select row', 'should select tab view item',
     'should selection change', 'should zoom', 'shown',
     'update menu item', 'update parameters',
     'update toolbar item', 'was hidden', 'was miniaturized',
     'will become active', 'will close', 'will dismiss',
     'will display browser cell', 'will display cell',
     'will display item cell', 'will display outline cell',
     'will finish launching', 'will hide', 'will miniaturize',
     'will move', 'will open', 'will pop up', 'will quit',
     'will resign active', 'will resize( sub views)?',
     'will select tab view item', 'will show', 'will zoom',
     'write to file', 'zoomed']
    StudioCommands = ['animate', 'append', 'call method', 'center',
     'close drawer', 'close panel', 'display',
     'display alert', 'display dialog', 'display panel', 'go',
     'hide', 'highlight', 'increment', 'item for',
     'load image', 'load movie', 'load nib', 'load panel',
     'load sound', 'localized string', 'lock focus', 'log',
     'open drawer', 'path for', 'pause', 'perform action',
     'play', 'register', 'resume', 'scroll', 'select( all)?',
     'show', 'size to fit', 'start', 'step back',
     'step forward', 'stop', 'synchronize', 'unlock focus',
     'update']
    StudioProperties = ['accepts arrow key', 'action method', 'active',
     'alignment', 'allowed identifiers',
     'allows branch selection', 'allows column reordering',
     'allows column resizing', 'allows column selection',
     'allows customization',
     'allows editing text attributes',
     'allows empty selection', 'allows mixed state',
     'allows multiple selection', 'allows reordering',
     'allows undo', 'alpha( value)?', 'alternate image',
     'alternate increment value', 'alternate title',
     'animation delay', 'associated file name',
     'associated object', 'auto completes', 'auto display',
     'auto enables items', 'auto repeat',
     'auto resizes( outline column)?',
     'auto save expanded items', 'auto save name',
     'auto save table columns', 'auto saves configuration',
     'auto scroll', 'auto sizes all columns to fit',
     'auto sizes cells', 'background color', 'bezel state',
     'bezel style', 'bezeled', 'border rect', 'border type',
     'bordered', 'bounds( rotation)?', 'box type',
     'button returned', 'button type',
     'can choose directories', 'can choose files',
     'can draw', 'can hide',
     'cell( (background color|size|type))?', 'characters',
     'class', 'click count', 'clicked( data)? column',
     'clicked data item', 'clicked( data)? row',
     'closeable', 'collating', 'color( (mode|panel))',
     'command key down', 'configuration',
     'content(s| (size|view( margins)?))?', 'context',
     'continuous', 'control key down', 'control size',
     'control tint', 'control view',
     'controller visible', 'coordinate system',
     'copies( on scroll)?', 'corner view', 'current cell',
     'current column', 'current( field)?  editor',
     'current( menu)? item', 'current row',
     'current tab view item', 'data source',
     'default identifiers', 'delta (x|y|z)',
     'destination window', 'directory', 'display mode',
     'displayed cell', 'document( (edited|rect|view))?',
     'double value', 'dragged column', 'dragged distance',
     'dragged items', 'draws( cell)? background',
     'draws grid', 'dynamically scrolls', 'echos bullets',
     'edge', 'editable', 'edited( data)? column',
     'edited data item', 'edited( data)? row', 'enabled',
     'enclosing scroll view', 'ending page',
     'error handling', 'event number', 'event type',
     'excluded from windows menu', 'executable path',
     'expanded', 'fax number', 'field editor', 'file kind',
     'file name', 'file type', 'first responder',
     'first visible column', 'flipped', 'floating',
     'font( panel)?', 'formatter', 'frameworks path',
     'frontmost', 'gave up', 'grid color', 'has data items',
     'has horizontal ruler', 'has horizontal scroller',
     'has parent data item', 'has resize indicator',
     'has shadow', 'has sub menu', 'has vertical ruler',
     'has vertical scroller', 'header cell', 'header view',
     'hidden', 'hides when deactivated', 'highlights by',
     'horizontal line scroll', 'horizontal page scroll',
     'horizontal ruler view', 'horizontally resizable',
     'icon image', 'id', 'identifier',
     'ignores multiple clicks',
     'image( (alignment|dims when disabled|frame style|scaling))?',
     'imports graphics', 'increment value',
     'indentation per level', 'indeterminate', 'index',
     'integer value', 'intercell spacing', 'item height',
     'key( (code|equivalent( modifier)?|window))?',
     'knob thickness', 'label', 'last( visible)? column',
     'leading offset', 'leaf', 'level', 'line scroll',
     'loaded', 'localized sort', 'location', 'loop mode',
     'main( (bunde|menu|window))?', 'marker follows cell',
     'matrix mode', 'maximum( content)? size',
     'maximum visible columns',
     'menu( form representation)?', 'miniaturizable',
     'miniaturized', 'minimized image', 'minimized title',
     'minimum column width', 'minimum( content)? size',
     'modal', 'modified', 'mouse down state',
     'movie( (controller|file|rect))?', 'muted', 'name',
     'needs display', 'next state', 'next text',
     'number of tick marks', 'only tick mark values',
     'opaque', 'open panel', 'option key down',
     'outline table column', 'page scroll', 'pages across',
     'pages down', 'palette label', 'pane splitter',
     'parent data item', 'parent window', 'pasteboard',
     'path( (names|separator))?', 'playing',
     'plays every frame', 'plays selection only', 'position',
     'preferred edge', 'preferred type', 'pressure',
     'previous text', 'prompt', 'properties',
     'prototype cell', 'pulls down', 'rate',
     'released when closed', 'repeated',
     'requested print time', 'required file type',
     'resizable', 'resized column', 'resource path',
     'returns records', 'reuses columns', 'rich text',
     'roll over', 'row height', 'rulers visible',
     'save panel', 'scripts path', 'scrollable',
     'selectable( identifiers)?', 'selected cell',
     'selected( data)? columns?', 'selected data items?',
     'selected( data)? rows?', 'selected item identifier',
     'selection by rect', 'send action on arrow key',
     'sends action when done editing', 'separates columns',
     'separator item', 'sequence number', 'services menu',
     'shared frameworks path', 'shared support path',
     'sheet', 'shift key down', 'shows alpha',
     'shows state by', 'size( mode)?',
     'smart insert delete enabled', 'sort case sensitivity',
     'sort column', 'sort order', 'sort type',
     'sorted( data rows)?', 'sound', 'source( mask)?',
     'spell checking enabled', 'starting page', 'state',
     'string value', 'sub menu', 'super menu', 'super view',
     'tab key traverses cells', 'tab state', 'tab type',
     'tab view', 'table view', 'tag', 'target( printer)?',
     'text color', 'text container insert',
     'text container origin', 'text returned',
     'tick mark position', 'time stamp',
     'title(d| (cell|font|height|position|rect))?',
     'tool tip', 'toolbar', 'trailing offset', 'transparent',
     'treat packages as directories', 'truncated labels',
     'types', 'unmodified characters', 'update views',
     'use sort indicator', 'user defaults',
     'uses data source', 'uses ruler',
     'uses threaded animation',
     'uses title from previous column', 'value wraps',
     'version',
     'vertical( (line scroll|page scroll|ruler view))?',
     'vertically resizable', 'view',
     'visible( document rect)?', 'volume', 'width', 'window',
     'windows menu', 'wraps', 'zoomable', 'zoomed']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '¬\\n', String.Escape),
              (
               "'s\\s+", Text),
              (
               '(--|#).*?$', Comment),
              (
               '\\(\\*', Comment.Multiline, 'comment'),
              (
               '[\\(\\){}!,.:]', Punctuation),
              (
               '(«)([^»]+)(»)',
               bygroups(Text, Name.Builtin, Text)),
              (
               '\\b((?:considering|ignoring)\\s*)(application responses|case|diacriticals|hyphens|numeric strings|punctuation|white space)',
               bygroups(Keyword, Name.Builtin)),
              (
               '(-|\\*|\\+|&|≠|>=?|<=?|=|≥|≤|/|÷|\\^)', Operator),
              (
               '\\b(%s)\\b' % ('|').join(Operators), Operator.Word),
              (
               '^(\\s*(?:on|end)\\s+)(%s)' % ('|').join(StudioEvents),
               bygroups(Keyword, Name.Function)),
              (
               '^(\\s*)(in|on|script|to)(\\s+)', bygroups(Text, Keyword, Text)),
              (
               '\\b(as )(%s)\\b' % ('|').join(Classes),
               bygroups(Keyword, Name.Class)),
              (
               '\\b(%s)\\b' % ('|').join(Literals), Name.Constant),
              (
               '\\b(%s)\\b' % ('|').join(Commands), Name.Builtin),
              (
               '\\b(%s)\\b' % ('|').join(Control), Keyword),
              (
               '\\b(%s)\\b' % ('|').join(Declarations), Keyword),
              (
               '\\b(%s)\\b' % ('|').join(Reserved), Name.Builtin),
              (
               '\\b(%s)s?\\b' % ('|').join(BuiltIn), Name.Builtin),
              (
               '\\b(%s)\\b' % ('|').join(HandlerParams), Name.Builtin),
              (
               '\\b(%s)\\b' % ('|').join(StudioProperties), Name.Attribute),
              (
               '\\b(%s)s?\\b' % ('|').join(StudioClasses), Name.Builtin),
              (
               '\\b(%s)\\b' % ('|').join(StudioCommands), Name.Builtin),
              (
               '\\b(%s)\\b' % ('|').join(References), Name.Builtin),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
              (
               '\\b(%s)\\b' % Identifiers, Name.Variable),
              (
               '[-+]?(\\d+\\.\\d*|\\d*\\.\\d+)(E[-+][0-9]+)?', Number.Float),
              (
               '[-+]?\\d+', Number.Integer)], 
       'comment': [
                 (
                  '\\(\\*', Comment.Multiline, '#push'),
                 (
                  '\\*\\)', Comment.Multiline, '#pop'),
                 (
                  '[^*(]+', Comment.Multiline),
                 (
                  '[*(]', Comment.Multiline)]}


class ModelicaLexer(RegexLexer):
    """
    For `Modelica <http://www.modelica.org/>`_ source code.

    *New in Pygments 1.1.*
    """
    name = 'Modelica'
    aliases = ['modelica']
    filenames = ['*.mo']
    mimetypes = ['text/x-modelica']
    flags = re.IGNORECASE | re.DOTALL
    tokens = {'whitespace': [
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     '\\\\\\n', Text),
                    (
                     '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment),
                    (
                     '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment)], 
       'statements': [
                    (
                     '"', String, 'string'),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+|\\d.)[eE][+-]?\\d+[lL]?', Number.Float),
                    (
                     '(\\d+\\.\\d*|\\.\\d+)', Number.Float),
                    (
                     '\\d+[Ll]?', Number.Integer),
                    (
                     '[~!%^&*+=|?:<>/-]', Operator),
                    (
                     '[()\\[\\]{},.;]', Punctuation),
                    (
                     '(true|false|NULL|Real|Integer|Boolean)\\b', Name.Builtin),
                    (
                     "([a-zA-Z_][\\w]*|'[a-zA-Z_\\+\\-\\*\\/\\^][\\w]*')(\\.([a-zA-Z_][\\w]*|'[a-zA-Z_\\+\\-\\*\\/\\^][\\w]*'))+",
                     Name.Class),
                    (
                     "('[\\w\\+\\-\\*\\/\\^]+'|\\w+)", Name)], 
       'root': [
              include('whitespace'),
              include('keywords'),
              include('functions'),
              include('operators'),
              include('classes'),
              (
               '("<html>|<html>)', Name.Tag, 'html-content'),
              include('statements')], 
       'keywords': [
                  (
                   '(algorithm|annotation|break|connect|constant|constrainedby|discrete|each|else|elseif|elsewhen|encapsulated|enumeration|end|equation|exit|expandable|extends|external|false|final|flow|for|if|import|in|inner|input|loop|nondiscrete|outer|output|parameter|partial|protected|public|redeclare|replaceable|stream|time|then|true|when|while|within)\\b',
                   Keyword)], 
       'functions': [
                   (
                    '(abs|acos|acosh|asin|asinh|atan|atan2|atan3|ceil|cos|cosh|cross|div|exp|floor|log|log10|mod|rem|sign|sin|sinh|size|sqrt|tan|tanh|zeros)\\b',
                    Name.Function)], 
       'operators': [
                   (
                    '(and|assert|cardinality|change|delay|der|edge|initial|noEvent|not|or|pre|reinit|return|sample|smooth|terminal|terminate)\\b',
                    Name.Builtin)], 
       'classes': [
                 (
                  '(block|class|connector|function|model|package|record|type)\\b',
                  Name.Class)], 
       'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})',
                 String.Escape),
                (
                 '[^\\\\"\\n]+', String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\', String)], 
       'html-content': [
                      (
                       '<\\s*/\\s*html\\s*>', Name.Tag, '#pop'),
                      (
                       '.+?(?=<\\s*/\\s*html\\s*>)', using(HtmlLexer))]}


class RebolLexer(RegexLexer):
    """
    A `REBOL <http://www.rebol.com/>`_ lexer.

    *New in Pygments 1.1.*
    """
    name = 'REBOL'
    aliases = ['rebol']
    filenames = ['*.r', '*.r3']
    mimetypes = ['text/x-rebol']
    flags = re.IGNORECASE | re.MULTILINE
    re.IGNORECASE
    escape_re = '(?:\\^\\([0-9a-fA-F]{1,4}\\)*)'

    def word_callback(lexer, match):
        word = match.group()
        if re.match('.*:$', word):
            yield (
             match.start(), Generic.Subheading, word)
        elif re.match('(native|alias|all|any|as-string|as-binary|bind|bound\\?|case|catch|checksum|comment|debase|dehex|exclude|difference|disarm|either|else|enbase|foreach|remove-each|form|free|get|get-env|if|in|intersect|loop|minimum-of|maximum-of|mold|new-line|new-line\\?|not|now|prin|print|reduce|compose|construct|repeat|reverse|save|script\\?|set|shift|switch|throw|to-hex|trace|try|type\\?|union|unique|unless|unprotect|unset|until|use|value\\?|while|compress|decompress|secure|open|close|read|read-io|write-io|write|update|query|wait|input\\?|exp|log-10|log-2|log-e|square-root|cosine|sine|tangent|arccosine|arcsine|arctangent|protect|lowercase|uppercase|entab|detab|connected\\?|browse|launch|stats|get-modes|set-modes|to-local-file|to-rebol-file|encloak|decloak|create-link|do-browser|bind\\?|hide|draw|show|size-text|textinfo|offset-to-caret|caret-to-offset|local-request-file|rgb-to-hsv|hsv-to-rgb|crypt-strength\\?|dh-make-key|dh-generate-key|dh-compute-key|dsa-make-key|dsa-generate-key|dsa-make-signature|dsa-verify-signature|rsa-make-key|rsa-generate-key|rsa-encrypt)$', word):
            yield (
             match.start(), Name.Builtin, word)
        elif re.match('(add|subtract|multiply|divide|remainder|power|and~|or~|xor~|minimum|maximum|negate|complement|absolute|random|head|tail|next|back|skip|at|pick|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|last|path|find|select|make|to|copy\\*|insert|remove|change|poke|clear|trim|sort|min|max|abs|cp|copy)$', word):
            yield (
             match.start(), Name.Function, word)
        elif re.match('(error|source|input|license|help|install|echo|Usage|with|func|throw-on-error|function|does|has|context|probe|\\?\\?|as-pair|mod|modulo|round|repend|about|set-net|append|join|rejoin|reform|remold|charset|array|replace|move|extract|forskip|forall|alter|first+|also|take|for|forever|dispatch|attempt|what-dir|change-dir|clean-path|list-dir|dirize|rename|split-path|delete|make-dir|delete-dir|in-dir|confirm|dump-obj|upgrade|what|build-tag|process-source|build-markup|decode-cgi|read-cgi|write-user|save-user|set-user-name|protect-system|parse-xml|cvs-date|cvs-version|do-boot|get-net-info|desktop|layout|scroll-para|get-face|alert|set-face|uninstall|unfocus|request-dir|center-face|do-events|net-error|decode-url|parse-header|parse-header-date|parse-email-addrs|import-email|send|build-attach-body|resend|show-popup|hide-popup|open-events|find-key-face|do-face|viewtop|confine|find-window|insert-event-func|remove-event-func|inform|dump-pane|dump-face|flag-face|deflag-face|clear-fields|read-net|vbug|path-thru|read-thru|load-thru|do-thru|launch-thru|load-image|request-download|do-face-alt|set-font|set-para|get-style|set-style|make-face|stylize|choose|hilight-text|hilight-all|unlight-text|focus|scroll-drag|clear-face|reset-face|scroll-face|resize-face|load-stock|load-stock-block|notify|request|flash|request-color|request-pass|request-text|request-list|request-date|request-file|dbug|editor|link-relative-path|emailer|parse-error)$', word):
            yield (
             match.start(), Keyword.Namespace, word)
        elif re.match('(halt|quit|do|load|q|recycle|call|run|ask|parse|view|unview|return|exit|break)$', word):
            yield (
             match.start(), Name.Exception, word)
        elif re.match('REBOL$', word):
            yield (
             match.start(), Generic.Heading, word)
        elif re.match('to-.*', word):
            yield (
             match.start(), Keyword, word)
        elif re.match('(\\+|-|\\*|/|//|\\*\\*|and|or|xor|=\\?|=|==|<>|<|>|<=|>=)$', word):
            yield (
             match.start(), Operator, word)
        elif re.match('.*\\?$', word):
            yield (
             match.start(), Keyword, word)
        elif re.match('.*\\!$', word):
            yield (
             match.start(), Keyword.Type, word)
        elif re.match("'.*", word):
            yield (
             match.start(), Name.Variable.Instance, word)
        elif re.match('#.*', word):
            yield (
             match.start(), Name.Label, word)
        elif re.match('%.*', word):
            yield (
             match.start(), Name.Decorator, word)
        else:
            yield (
             match.start(), Name.Variable, word)

    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '#"', String.Char, 'char'),
              (
               '#{[0-9a-fA-F]*}', Number.Hex),
              (
               '2#{', Number.Hex, 'bin2'),
              (
               '64#{[0-9a-zA-Z+/=\\s]*}', Number.Hex),
              (
               '"', String, 'string'),
              (
               '{', String, 'string2'),
              (
               ';#+.*\\n', Comment.Special),
              (
               ';\\*+.*\\n', Comment.Preproc),
              (
               ';.*\\n', Comment),
              (
               '%"', Name.Decorator, 'stringFile'),
              (
               '%[^(\\^{^")\\s\\[\\]]+', Name.Decorator),
              (
               '<[a-zA-Z0-9:._-]*>', Name.Tag),
              (
               '<[^(<>\\s")]+', Name.Tag, 'tag'),
              (
               '[+-]?([a-zA-Z]{1,3})?\\$\\d+(\\.\\d+)?', Number.Float),
              (
               '[+-]?\\d+\\:\\d+(\\:\\d+)?(\\.\\d+)?', String.Other),
              (
               '\\d+\\-[0-9a-zA-Z]+\\-\\d+(\\/\\d+\\:\\d+(\\:\\d+)?([\\.\\d+]?([+-]?\\d+:\\d+)?)?)?',
               String.Other),
              (
               '\\d+(\\.\\d+)+\\.\\d+', Keyword.Constant),
              (
               '\\d+[xX]\\d+', Keyword.Constant),
              (
               "[+-]?\\d+(\\'\\d+)?([\\.,]\\d*)?[eE][+-]?\\d+", Number.Float),
              (
               "[+-]?\\d+(\\'\\d+)?[\\.,]\\d*", Number.Float),
              (
               "[+-]?\\d+(\\'\\d+)?", Number),
              (
               '[\\[\\]\\(\\)]', Generic.Strong),
              (
               '[a-zA-Z]+[^(\\^{"\\s:)]*://[^(\\^{"\\s)]*', Name.Decorator),
              (
               'mailto:[^(\\^{"@\\s)]+@[^(\\^{"@\\s)]+', Name.Decorator),
              (
               '[^(\\^{"@\\s)]+@[^(\\^{"@\\s)]+', Name.Decorator),
              (
               'comment\\s', Comment, 'comment'),
              (
               '/[^(\\^{^")\\s/[\\]]*', Name.Attribute),
              (
               '([^(\\^{^")\\s/[\\]]+)(?=[:({"\\s/\\[\\]])', word_callback),
              (
               '([^(\\^{^")\\s]+)', Text)], 
       'string': [
                (
                 '[^(\\^")]+', String),
                (
                 escape_re, String.Escape),
                (
                 '[\\(|\\)]+', String),
                (
                 '\\^.', String.Escape),
                (
                 '"', String, '#pop')], 
       'string2': [
                 (
                  '[^(\\^{^})]+', String),
                 (
                  escape_re, String.Escape),
                 (
                  '[\\(|\\)]+', String),
                 (
                  '\\^.', String.Escape),
                 (
                  '{', String, '#push'),
                 (
                  '}', String, '#pop')], 
       'stringFile': [
                    (
                     '[^(\\^")]+', Name.Decorator),
                    (
                     escape_re, Name.Decorator),
                    (
                     '\\^.', Name.Decorator),
                    (
                     '"', Name.Decorator, '#pop')], 
       'char': [
              (
               escape_re + '"', String.Char, '#pop'),
              (
               '\\^."', String.Char, '#pop'),
              (
               '."', String.Char, '#pop')], 
       'tag': [
             (
              escape_re, Name.Tag),
             (
              '"', Name.Tag, 'tagString'),
             (
              '[^(<>\\r\\n")]+', Name.Tag),
             (
              '>', Name.Tag, '#pop')], 
       'tagString': [
                   (
                    '[^(\\^")]+', Name.Tag),
                   (
                    escape_re, Name.Tag),
                   (
                    '[\\(|\\)]+', Name.Tag),
                   (
                    '\\^.', Name.Tag),
                   (
                    '"', Name.Tag, '#pop')], 
       'tuple': [
               (
                '(\\d+\\.)+', Keyword.Constant),
               (
                '\\d+', Keyword.Constant, '#pop')], 
       'bin2': [
              (
               '\\s+', Number.Hex),
              (
               '([0-1]\\s*){8}', Number.Hex),
              (
               '}', Number.Hex, '#pop')], 
       'comment': [
                 (
                  '"', Comment, 'commentString1'),
                 (
                  '{', Comment, 'commentString2'),
                 (
                  '\\[', Comment, 'commentBlock'),
                 (
                  '[^(\\s{\\"\\[]+', Comment, '#pop')], 
       'commentString1': [
                        (
                         '[^(\\^")]+', Comment),
                        (
                         escape_re, Comment),
                        (
                         '[\\(|\\)]+', Comment),
                        (
                         '\\^.', Comment),
                        (
                         '"', Comment, '#pop')], 
       'commentString2': [
                        (
                         '[^(\\^{^})]+', Comment),
                        (
                         escape_re, Comment),
                        (
                         '[\\(|\\)]+', Comment),
                        (
                         '\\^.', Comment),
                        (
                         '{', Comment, '#push'),
                        (
                         '}', Comment, '#pop')], 
       'commentBlock': [
                      (
                       '\\[', Comment, '#push'),
                      (
                       '\\]', Comment, '#pop'),
                      (
                       '[^(\\[\\])]*', Comment)]}


class ABAPLexer(RegexLexer):
    """
    Lexer for ABAP, SAP's integrated language.

    *New in Pygments 1.1.*
    """
    name = 'ABAP'
    aliases = ['abap']
    filenames = ['*.abap']
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
                         '<[\\S_]+>', Name.Variable),
                        (
                         '[\\w][\\w_~]*(?:(\\[\\])|->\\*)?', Name.Variable)], 
       'root': [
              include('common'),
              (
               "(CALL\\s+(?:BADI|CUSTOMER-FUNCTION|FUNCTION))(\\s+)(\\'?\\S+\\'?)",
               bygroups(Keyword, Text, Name.Function)),
              (
               '(CALL\\s+(?:DIALOG|SCREEN|SUBSCREEN|SELECTION-SCREEN|TRANSACTION|TRANSFORMATION))\\b',
               Keyword),
              (
               '(FORM|PERFORM)(\\s+)([\\w_]+)',
               bygroups(Keyword, Text, Name.Function)),
              (
               '(PERFORM)(\\s+)(\\()([\\w_]+)(\\))',
               bygroups(Keyword, Text, Punctuation, Name.Variable, Punctuation)),
              (
               '(MODULE)(\\s+)(\\S+)(\\s+)(INPUT|OUTPUT)',
               bygroups(Keyword, Text, Name.Function, Text, Keyword)),
              (
               '(METHOD)(\\s+)([\\w_~]+)',
               bygroups(Keyword, Text, Name.Function)),
              (
               '(\\s+)([\\w_\\-]+)([=\\-]>)([\\w_\\-~]+)',
               bygroups(Text, Name.Variable, Operator, Name.Function)),
              (
               '(?<=(=|-)>)([\\w_\\-~]+)(?=\\()', Name.Function),
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
               '[/;:()\\[\\],\\.]', Punctuation)]}


class NewspeakLexer(RegexLexer):
    """
    For `Newspeak <http://newspeaklanguage.org/>` syntax.
    """
    name = 'Newspeak'
    filenames = ['*.ns2']
    aliases = ['newspeak']
    mimetypes = ['text/x-newspeak']
    tokens = {'root': [
              (
               '\\b(Newsqueak2)\\b', Keyword.Declaration),
              (
               "'[^']*'", String),
              (
               '\\b(class)(\\s+)([a-zA-Z0-9_]+)(\\s*)',
               bygroups(Keyword.Declaration, Text, Name.Class, Text)),
              (
               '\\b(mixin|self|super|private|public|protected|nil|true|false)\\b',
               Keyword),
              (
               '([a-zA-Z0-9_]+\\:)(\\s*)([a-zA-Z_]\\w+)',
               bygroups(Name.Function, Text, Name.Variable)),
              (
               '([a-zA-Z0-9_]+)(\\s*)(=)',
               bygroups(Name.Attribute, Text, Operator)),
              (
               '<[a-zA-Z0-9_]+>', Comment.Special),
              include('expressionstat'),
              include('whitespace')], 
       'expressionstat': [
                        (
                         '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
                        (
                         '\\d+', Number.Integer),
                        (
                         ':\\w+', Name.Variable),
                        (
                         '(\\w+)(::)', bygroups(Name.Variable, Operator)),
                        (
                         '\\w+:', Name.Function),
                        (
                         '\\w+', Name.Variable),
                        (
                         '\\(|\\)', Punctuation),
                        (
                         '\\[|\\]', Punctuation),
                        (
                         '\\{|\\}', Punctuation),
                        (
                         '(\\^|\\+|\\/|~|\\*|<|>|=|@|%|\\||&|\\?|!|,|-|:)', Operator),
                        (
                         '\\.|;', Punctuation),
                        include('whitespace'),
                        include('literals')], 
       'literals': [
                  (
                   '\\$.', String),
                  (
                   "'[^']*'", String),
                  (
                   "#'[^']*'", String.Symbol),
                  (
                   '#\\w+:?', String.Symbol),
                  (
                   '#(\\+|\\/|~|\\*|<|>|=|@|%|\\||&|\\?|!|,|-)+', String.Symbol)], 
       'whitespace': [
                    (
                     '\\s+', Text),
                    (
                     '"[^"]*"', Comment)]}


class GherkinLexer(RegexLexer):
    """
    For `Gherkin <http://github.com/aslakhellesoy/gherkin/>` syntax.

    *New in Pygments 1.2.*
    """
    name = 'Gherkin'
    aliases = ['Cucumber', 'cucumber', 'Gherkin', 'gherkin']
    filenames = ['*.feature']
    mimetypes = ['text/x-gherkin']
    feature_keywords = '^(기능|機能|功能|フィーチャ|خاصية|תכונה|Функціонал|Функционалност|Функционал|Фича|Особина|Могућност|Özellik|Właściwość|Tính năng|Trajto|Savybė|Požiadavka|Požadavek|Osobina|Ominaisuus|Omadus|OH HAI|Mogućnost|Mogucnost|Jellemző|Fīča|Funzionalità|Funktionalität|Funkcionalnost|Funkcionalitāte|Funcționalitate|Functionaliteit|Functionalitate|Funcionalitat|Funcionalidade|Fonctionnalité|Fitur|Feature|Egenskap|Egenskab|Crikey|Característica|Arwedd)(:)(.*)$'
    feature_element_keywords = "^(\\s*)(시나리오 개요|시나리오|배경|背景|場景大綱|場景|场景大纲|场景|劇本大綱|劇本|テンプレ|シナリオテンプレート|シナリオテンプレ|シナリオアウトライン|シナリオ|سيناريو مخطط|سيناريو|الخلفية|תרחיש|תבנית תרחיש|רקע|Тарих|Сценарій|Сценарио|Сценарий структураси|Сценарий|Структура сценарію|Структура сценарија|Структура сценария|Скица|Рамка на сценарий|Пример|Предыстория|Предистория|Позадина|Передумова|Основа|Концепт|Контекст|Założenia|Wharrimean is|Tình huống|The thing of it is|Tausta|Taust|Tapausaihio|Tapaus|Szenariogrundriss|Szenario|Szablon scenariusza|Stsenaarium|Struktura scenarija|Skica|Skenario konsep|Skenario|Situācija|Senaryo taslağı|Senaryo|Scénář|Scénario|Schema dello scenario|Scenārijs pēc parauga|Scenārijs|Scenár|Scenaro|Scenariusz|Scenariul de şablon|Scenariul de sablon|Scenariu|Scenario Outline|Scenario Amlinellol|Scenario|Scenarijus|Scenarijaus šablonas|Scenarij|Scenarie|Rerefons|Raamstsenaarium|Primer|Pozadí|Pozadina|Pozadie|Plan du scénario|Plan du Scénario|Osnova scénáře|Osnova|Náčrt Scénáře|Náčrt Scenáru|Mate|MISHUN SRSLY|MISHUN|Kịch bản|Konturo de la scenaro|Kontext|Konteksts|Kontekstas|Kontekst|Koncept|Khung tình huống|Khung kịch bản|Háttér|Grundlage|Geçmiş|Forgatókönyv vázlat|Forgatókönyv|Fono|Esquema do Cenário|Esquema do Cenario|Esquema del escenario|Esquema de l\\'escenari|Escenario|Escenari|Dis is what went down|Dasar|Contexto|Contexte|Contesto|Condiţii|Conditii|Cenário|Cenario|Cefndir|Bối cảnh|Blokes|Bakgrunn|Bakgrund|Baggrund|Background|B4|Antecedents|Antecedentes|All y\\'all|Achtergrond|Abstrakt Scenario|Abstract Scenario)(:)(.*)$"
    examples_keywords = '^(\\s*)(예|例子|例|サンプル|امثلة|דוגמאות|Сценарији|Примери|Приклади|Мисоллар|Значения|Örnekler|Voorbeelden|Variantai|Tapaukset|Scenarios|Scenariji|Scenarijai|Příklady|Példák|Príklady|Przykłady|Primjeri|Primeri|Piemēri|Pavyzdžiai|Paraugs|Juhtumid|Exemplos|Exemples|Exemplele|Exempel|Examples|Esempi|Enghreifftiau|Ekzemploj|Eksempler|Ejemplos|EXAMPLZ|Dữ liệu|Contoh|Cobber|Beispiele)(:)(.*)$'
    step_keywords = "^(\\s*)(하지만|조건|먼저|만일|만약|단|그리고|그러면|那麼|那么|而且|當|当|前提|假設|假如|但是|但し|並且|もし|ならば|ただし|しかし|かつ|و |متى |لكن |عندما |ثم |بفرض |اذاً |כאשר |וגם |בהינתן |אזי |אז |אבל |Якщо |Унда |То |Припустимо, що |Припустимо |Онда |Но |Нехай |Лекин |Когато |Када |Кад |К тому же |И |Задато |Задати |Задате |Если |Допустим |Дадено |Ва |Бирок |Аммо |Али |Але |Агар |А |І |Și |És |Zatati |Zakładając |Zadato |Zadate |Zadano |Zadani |Zadan |Youse know when youse got |Youse know like when |Yna |Ya know how |Ya gotta |Y |Wun |Wtedy |When y\\'all |When |Wenn |WEN |Và |Ve |Und |Un |Thì |Then y\\'all |Then |Tapi |Tak |Tada |Tad |Så |Stel |Soit |Siis |Si |Sed |Se |Quando |Quand |Quan |Pryd |Pokud |Pokiaľ |Però |Pero |Pak |Oraz |Onda |Ond |Oletetaan |Og |Och |O zaman |Når |När |Niin |Nhưng |N |Mutta |Men |Mas |Maka |Majd |Mais |Maar |Ma |Lorsque |Lorsqu\\'|Kun |Kuid |Kui |Khi |Keď |Ketika |Když |Kaj |Kai |Kada |Kad |Jeżeli |Ja |Ir |I CAN HAZ |I |Ha |Givun |Givet |Given y\\'all |Given |Gitt |Gegeven |Gegeben sei |Fakat |Eğer ki |Etant donné |Et |Então |Entonces |Entao |En |Eeldades |E |Duota |Dun |Donitaĵo |Donat |Donada |Do |Diyelim ki |Dengan |Den youse gotta |De |Dato |Dar |Dann |Dan |Dado |Dacă |Daca |DEN |Când |Cuando |Cho |Cept |Cand |Cal |But y\\'all |But |Buh |Biết |Bet |BUT |Atès |Atunci |Atesa |Anrhegedig a |Angenommen |And y\\'all |And |An |Ama |Als |Alors |Allora |Ali |Aleshores |Ale |Akkor |Aber |AN |A také |A |\\* )"
    tokens = {'comments': [
                  (
                   '#.*$', Comment)], 
       'feature_elements': [
                          (
                           step_keywords, Keyword, 'step_content_stack'),
                          include('comments'),
                          (
                           '(\\s|.)', Name.Function)], 
       'feature_elements_on_stack': [
                                   (
                                    step_keywords, Keyword, '#pop:2'),
                                   include('comments'),
                                   (
                                    '(\\s|.)', Name.Function)], 
       'examples_table': [
                        (
                         '\\s+\\|', Keyword, 'examples_table_header'),
                        include('comments'),
                        (
                         '(\\s|.)', Name.Function)], 
       'examples_table_header': [
                               (
                                '\\s+\\|\\s*$', Keyword, '#pop:2'),
                               include('comments'),
                               (
                                '\\s*\\|', Keyword),
                               (
                                '[^\\|]', Name.Variable)], 
       'scenario_sections_on_stack': [
                                    (
                                     feature_element_keywords, bygroups(Name.Function, Keyword, Keyword, Name.Function), 'feature_elements_on_stack')], 
       'narrative': [
                   include('scenario_sections_on_stack'),
                   (
                    '(\\s|.)', Name.Function)], 
       'table_vars': [
                    (
                     '(<[^>]+>)', Name.Variable)], 
       'numbers': [
                 (
                  '(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', String)], 
       'string': [
                include('table_vars'),
                (
                 '(\\s|.)', String)], 
       'py_string': [
                   (
                    '"""', Keyword, '#pop'),
                   include('string')], 
       'step_content_root': [
                           (
                            '$', Keyword, '#pop'),
                           include('step_content')], 
       'step_content_stack': [
                            (
                             '$', Keyword, '#pop:2'),
                            include('step_content')], 
       'step_content': [
                      (
                       '"', Name.Function, 'double_string'),
                      include('table_vars'),
                      include('numbers'),
                      include('comments'),
                      (
                       '(\\s|.)', Name.Function)], 
       'table_content': [
                       (
                        '\\s+\\|\\s*$', Keyword, '#pop'),
                       include('comments'),
                       (
                        '\\s*\\|', Keyword),
                       include('string')], 
       'double_string': [
                       (
                        '"', Name.Function, '#pop'),
                       include('string')], 
       'root': [
              (
               '\\n', Name.Function),
              include('comments'),
              (
               '"""', Keyword, 'py_string'),
              (
               '\\s+\\|', Keyword, 'table_content'),
              (
               '"', Name.Function, 'double_string'),
              include('table_vars'),
              include('numbers'),
              (
               '(\\s*)(@[^@\\r\\n\\t ]+)', bygroups(Name.Function, Name.Tag)),
              (
               step_keywords, bygroups(Name.Function, Keyword), 'step_content_root'),
              (
               feature_keywords, bygroups(Keyword, Keyword, Name.Function), 'narrative'),
              (
               feature_element_keywords, bygroups(Name.Function, Keyword, Keyword, Name.Function), 'feature_elements'),
              (
               examples_keywords, bygroups(Name.Function, Keyword, Keyword, Name.Function), 'examples_table'),
              (
               '(\\s|.)', Name.Function)]}


class AsymptoteLexer(RegexLexer):
    """
    For `Asymptote <http://asymptote.sf.net/>`_ source code.

    *New in Pygments 1.2.*
    """
    name = 'Asymptote'
    aliases = ['asy', 'asymptote']
    filenames = ['*.asy']
    mimetypes = ['text/x-asymptote']
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'whitespace': [
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     '\\\\\\n', Text),
                    (
                     '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment),
                    (
                     '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment)], 
       'statements': [
                    (
                     '"(\\\\\\\\|\\\\"|[^"])*"', String),
                    (
                     "'", String, 'string'),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[lL]?', Number.Float),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
                    (
                     '0x[0-9a-fA-F]+[Ll]?', Number.Hex),
                    (
                     '0[0-7]+[Ll]?', Number.Oct),
                    (
                     '\\d+[Ll]?', Number.Integer),
                    (
                     '[~!%^&*+=|?:<>/-]', Operator),
                    (
                     '[()\\[\\],.]', Punctuation),
                    (
                     '\\b(case)(.+?)(:)', bygroups(Keyword, using(this), Text)),
                    (
                     '(and|controls|tension|atleast|curl|if|else|while|for|do|return|break|continue|struct|typedef|new|access|import|unravel|from|include|quote|static|public|private|restricted|this|explicit|true|false|null|cycle|newframe|operator)\\b',
                     Keyword),
                    (
                     '(Braid|FitResult|Label|Legend|TreeNode|abscissa|arc|arrowhead|binarytree|binarytreeNode|block|bool|bool3|bounds|bqe|circle|conic|coord|coordsys|cputime|ellipse|file|filltype|frame|grid3|guide|horner|hsv|hyperbola|indexedTransform|int|inversion|key|light|line|linefit|marginT|marker|mass|object|pair|parabola|path|path3|pen|picture|point|position|projection|real|revolution|scaleT|scientific|segment|side|slice|splitface|string|surface|tensionSpecifier|ticklocate|ticksgridT|tickvalues|transform|transformation|tree|triangle|trilinear|triple|vector|vertex|void)(?=([ ]{1,}[a-zA-Z]))',
                     Keyword.Type),
                    (
                     '(Braid|FitResult|TreeNode|abscissa|arrowhead|block|bool|bool3|bounds|coord|frame|guide|horner|int|linefit|marginT|pair|pen|picture|position|real|revolution|slice|splitface|ticksgridT|tickvalues|tree|triple|vertex|void)\\b',
                     Keyword.Type),
                    (
                     '[a-zA-Z_][a-zA-Z0-9_]*:(?!:)', Name.Label),
                    (
                     '[a-zA-Z_][a-zA-Z0-9_]*', Name)], 
       'root': [
              include('whitespace'),
              (
               '((?:[a-zA-Z0-9_*\\s])+?(?:\\s|[*]))([a-zA-Z_][a-zA-Z0-9_]*)(\\s*\\([^;]*?\\))(' + _ws + ')({)',
               bygroups(using(this), Name.Function, using(this), using(this), Punctuation),
               'function'),
              (
               '((?:[a-zA-Z0-9_*\\s])+?(?:\\s|[*]))([a-zA-Z_][a-zA-Z0-9_]*)(\\s*\\([^;]*?\\))(' + _ws + ')(;)',
               bygroups(using(this), Name.Function, using(this), using(this), Punctuation)),
              (
               '', Text, 'statement')], 
       'statement': [
                   include('whitespace'),
                   include('statements'),
                   (
                    '[{}]', Punctuation),
                   (
                    ';', Punctuation, '#pop')], 
       'function': [
                  include('whitespace'),
                  include('statements'),
                  (
                   ';', Punctuation),
                  (
                   '{', Punctuation, '#push'),
                  (
                   '}', Punctuation, '#pop')], 
       'string': [
                (
                 "'", String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\'?]|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                (
                 '\\n', String),
                (
                 "[^\\\\'\\n]+", String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\n', String),
                (
                 '\\\\', String)]}

    def get_tokens_unprocessed(self, text):
        from pygments.lexers._asybuiltins import ASYFUNCNAME, ASYVARNAME
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in ASYFUNCNAME:
                token = Name.Function
            elif token is Name and value in ASYVARNAME:
                token = Name.Variable
            yield (
             index, token, value)


class PostScriptLexer(RegexLexer):
    """
    Lexer for PostScript files.

    The PostScript Language Reference published by Adobe at
    <http://partners.adobe.com/public/developer/en/ps/PLRM.pdf>
    is the authority for this.

    *New in Pygments 1.4.*
    """
    name = 'PostScript'
    aliases = ['postscript']
    filenames = ['*.ps', '*.eps']
    mimetypes = ['application/postscript']
    delimiter = '\\(\\)\\<\\>\\[\\]\\{\\}\\/\\%\\s'
    delimiter_end = '(?=[%s])' % delimiter
    valid_name_chars = '[^%s]' % delimiter
    valid_name = '%s+%s' % (valid_name_chars, delimiter_end)
    tokens = {'root': [
              (
               '^%!.+\\n', Comment.Preproc),
              (
               '%%.*\\n', Comment.Special),
              (
               '(^%.*\\n){2,}', Comment.Multiline),
              (
               '%.*\\n', Comment.Single),
              (
               '\\(', String, 'stringliteral'),
              (
               '[\\{\\}(\\<\\<)(\\>\\>)\\[\\]]', Punctuation),
              (
               '<[0-9A-Fa-f]+>' + delimiter_end, Number.Hex),
              (
               '[0-9]+\\#(\\-|\\+)?([0-9]+\\.?|[0-9]*\\.[0-9]+|[0-9]+\\.[0-9]*)((e|E)[0-9]+)?' + delimiter_end, Number.Oct),
              (
               '(\\-|\\+)?([0-9]+\\.?|[0-9]*\\.[0-9]+|[0-9]+\\.[0-9]*)((e|E)[0-9]+)?' + delimiter_end, Number.Float),
              (
               '(\\-|\\+)?[0-9]+' + delimiter_end, Number.Integer),
              (
               '\\/%s' % valid_name, Name.Variable),
              (
               valid_name, Name.Function),
              (
               '(false|true)' + delimiter_end, Keyword.Constant),
              (
               '(eq|ne|ge|gt|le|lt|and|or|not|if|ifelse|for|forall)' + delimiter_end, Keyword.Reserved),
              (
               '(abs|add|aload|arc|arcn|array|atan|begin|bind|ceiling|charpath|clip|closepath|concat|concatmatrix|copy|cos|currentlinewidth|currentmatrix|currentpoint|curveto|cvi|cvs|def|defaultmatrix|dict|dictstackoverflow|div|dtransform|dup|end|exch|exec|exit|exp|fill|findfont|floor|get|getinterval|grestore|gsave|gt|identmatrix|idiv|idtransform|index|invertmatrix|itransform|length|lineto|ln|load|log|loop|matrix|mod|moveto|mul|neg|newpath|pathforall|pathbbox|pop|print|pstack|put|quit|rand|rangecheck|rcurveto|repeat|restore|rlineto|rmoveto|roll|rotate|round|run|save|scale|scalefont|setdash|setfont|setgray|setlinecap|setlinejoin|setlinewidth|setmatrix|setrgbcolor|shfill|show|showpage|sin|sqrt|stack|stringwidth|stroke|strokepath|sub|syntaxerror|transform|translate|truncate|typecheck|undefined|undefinedfilename|undefinedresult)' + delimiter_end,
               Name.Builtin),
              (
               '\\s+', Text)], 
       'stringliteral': [
                       (
                        '[^\\(\\)\\\\]+', String),
                       (
                        '\\\\', String.Escape, 'escape'),
                       (
                        '\\(', String, '#push'),
                       (
                        '\\)', String, '#pop')], 
       'escape': [
                (
                 '([0-8]{3}|n|r|t|b|f|\\\\|\\(|\\)|)', String.Escape, '#pop')]}


class AutohotkeyLexer(RegexLexer):
    """
    For `autohotkey <http://www.autohotkey.com/>`_ source code.

    *New in Pygments 1.4.*
    """
    name = 'autohotkey'
    aliases = ['ahk']
    filenames = ['*.ahk', '*.ahkl']
    mimetypes = ['text/x-autohotkey']
    flags = re.IGNORECASE | re.DOTALL | re.MULTILINE
    tokens = {'root': [
              include('whitespace'),
              (
               '^\\(', String, 'continuation'),
              include('comments'),
              (
               '(^\\s*)(\\w+)(\\s*)(=)',
               bygroups(Text.Whitespace, Name, Text.Whitespace, Operator),
               'command'),
              (
               '([\\w#@$?\\[\\]]+)(\\s*)(\\()',
               bygroups(Name.Function, Text.Whitespace, Punctuation),
               'parameters'),
              include('directives'),
              include('labels'),
              include('commands'),
              include('expressions'),
              include('numbers'),
              include('literals'),
              include('keynames'),
              include('keywords')], 
       'command': [
                 include('comments'),
                 include('whitespace'),
                 (
                  '^\\(', String, 'continuation'),
                 (
                  '[^\\n]*?(?=;*|$)', String, '#pop'),
                 include('numbers'),
                 include('literals')], 
       'expressions': [
                     include('comments'),
                     include('whitespace'),
                     include('numbers'),
                     include('literals'),
                     (
                      '([]\\w#@$?[]+)(\\s*)(\\()',
                      bygroups(Name.Function, Text.Whitespace, Punctuation),
                      'parameters'),
                     (
                      'A_\\w+', Name.Builtin),
                     (
                      '%[]\\w#@$?[]+?%', Name.Variable),
                     (
                      '{', Punctuation, 'block')], 
       'literals': [
                  (
                   '"', String, 'string'),
                  (
                   'A_\\w+', Name.Builtin),
                  (
                   '%[]\\w#@$?[]+?%', Name.Variable),
                  (
                   '[-~!%^&*+|?:<>/=]=?', Operator, 'expressions'),
                  (
                   '==', Operator, 'expressions'),
                  (
                   '[{()},.%#`;]', Punctuation),
                  (
                   '\\\\', Punctuation),
                  include('keywords'),
                  (
                   '\\w+', Text)], 
       'string': [
                (
                 '"', String, '#pop'),
                (
                 '""|`.', String.Escape),
                (
                 '[^\\`"\\n]+', String)], 
       'block': [
               include('root'),
               (
                '{', Punctuation, '#push'),
               (
                '}', Punctuation, '#pop')], 
       'parameters': [
                    (
                     '\\)', Punctuation, '#pop'),
                    (
                     '\\(', Punctuation, '#push'),
                    include('numbers'),
                    include('literals'),
                    include('whitespace')], 
       'keywords': [
                  (
                   '(static|global|local)\\b', Keyword.Type),
                  (
                   '(if|else|and|or)\\b', Keyword.Reserved)], 
       'directives': [
                    (
                     '#\\w+?\\s', Keyword)], 
       'labels': [
                (
                 '(^\\s*)([^:\\s]+?:{1,2})', bygroups(Text.Whitespace, Name.Label)),
                (
                 '(^\\s*)(::[]\\w#@$?[]+?::)', bygroups(Text.Whitespace, Name.Label))], 
       'comments': [
                  (
                   '^;+.*?$', Comment.Single),
                  (
                   '(?<=\\s);+.*?$', Comment.Single),
                  (
                   '^/\\*.*?\\n\\*/', Comment.Multiline),
                  (
                   '(?<!\\n)/\\*.*?\\n\\*/', Error)], 
       'whitespace': [
                    (
                     '[ \\t]+', Text.Whitespace)], 
       'numbers': [
                 (
                  '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
                 (
                  '\\d+[eE][+-]?[0-9]+', Number.Float),
                 (
                  '0[0-7]+', Number.Oct),
                 (
                  '0[xX][a-fA-F0-9]+', Number.Hex),
                 (
                  '\\d+L', Number.Integer.Long),
                 (
                  '\\d+', Number.Integer)], 
       'continuation': [
                      (
                       '\\n\\)', Punctuation, '#pop'),
                      (
                       '\\s[^\\n\\)]+', String)], 
       'keynames': [
                  (
                   '\\[[^\\]]+\\]', Keyword, 'keynames')], 
       'commands': [
                  (
                   '(autotrim|blockinput|break|click|clipwait|continue|control|controlclick|controlfocus|controlget|controlgetfocus|controlgetpos|controlgettext|controlmove|controlsend|controlsendraw|controlsettext|coordmode|critical|detecthiddentext|detecthiddenwindows|dllcall|drive|driveget|drivespacefree|else|envadd|envdiv|envget|envmult|envset|envsub|envupdate|exit|exitapp|fileappend|filecopy|filecopydir|filecreatedir|filecreateshortcut|filedelete|filegetattrib|filegetshortcut|filegetsize|filegettime|filegetversion|fileinstall|filemove|filemovedir|fileread|filereadline|filerecycle|filerecycleempty|fileremovedir|fileselectfile|fileselectfolder|filesetattrib|filesettime|formattime|gosub|goto|groupactivate|groupadd|groupclose|groupdeactivate|gui|guicontrol|guicontrolget|hotkey|ifexist|ifgreater|ifgreaterorequal|ifinstring|ifless|iflessorequal|ifmsgbox|ifnotequal|ifnotexist|ifnotinstring|ifwinactive|ifwinexist|ifwinnotactive|ifwinnotexist|imagesearch|inidelete|iniread|iniwrite|input|inputbox|keyhistory|keywait|listhotkeys|listlines|listvars|loop|menu|mouseclick|mouseclickdrag|mousegetpos|mousemove|msgbox|onmessage|onexit|outputdebug|pixelgetcolor|pixelsearch|postmessage|process|progress|random|regexmatch|regexreplace|registercallback|regdelete|regread|regwrite|reload|repeat|return|run|runas|runwait|send|sendevent|sendinput|sendmessage|sendmode|sendplay|sendraw|setbatchlines|setcapslockstate|setcontroldelay|setdefaultmousespeed|setenv|setformat|setkeydelay|setmousedelay|setnumlockstate|setscrolllockstate|setstorecapslockmode|settimer|settitlematchmode|setwindelay|setworkingdir|shutdown|sleep|sort|soundbeep|soundget|soundgetwavevolume|soundplay|soundset|soundsetwavevolume|splashimage|splashtextoff|splashtexton|splitpath|statusbargettext|statusbarwait|stringcasesense|stringgetpos|stringleft|stringlen|stringlower|stringmid|stringreplace|stringright|stringsplit|stringtrimleft|stringtrimright|stringupper|suspend|sysget|thread|tooltip|transform|traytip|urldownloadtofile|while|varsetcapacity|winactivate|winactivatebottom|winclose|winget|wingetactivestats|wingetactivetitle|wingetclass|wingetpos|wingettext|wingettitle|winhide|winkill|winmaximize|winmenuselectitem|winminimize|winminimizeall|winminimizeallundo|winmove|winrestore|winset|winsettitle|winshow|winwait|winwaitactive|winwaitclose|winwaitnotactivetrue|false|NULL)\\b',
                   Keyword, 'command')]}


class MaqlLexer(RegexLexer):
    """
    Lexer for `GoodData MAQL <https://secure.gooddata.com/docs/html/advanced.metric.tutorial.html>`_
    scripts.

    *New in Pygments 1.4.*
    """
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
               '[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]{1,3})?', Literal.Number),
              (
               '"', Literal.String, 'string-literal'),
              (
               '\\<\\>|\\!\\=', Operator),
              (
               '\\=|\\>\\=|\\>|\\<\\=|\\<', Operator),
              (
               '\\:\\=', Operator),
              (
               '\\[[^]]+\\]', Name.Variable.Class),
              (
               '(DIMENSIONS?|BOTTOM|METRIC|COUNT|OTHER|FACT|WITH|TOP|OR|ATTRIBUTE|CREATE|PARENT|FALSE|ROWS?|FROM|ALL|AS|PF|COLUMNS?|DEFINE|REPORT|LIMIT|TABLE|LIKE|AND|BY|BETWEEN|EXCEPT|SELECT|MATCH|WHERE|TRUE|FOR|IN|WITHOUT|FILTER|ALIAS|ORDER|FACT|WHEN|NOT|ON|KEYS|KEY|FULLSET|PRIMARY|LABELS|LABEL|VISUAL|TITLE|DESCRIPTION|FOLDER|ALTER|DROP|ADD|DATASET|DATATYPE|INT|BIGINT|DOUBLE|DATE|VARCHAR|DECIMAL|SYNCHRONIZE|TYPE|DEFAULT|ORDER|ASC|DESC|HYPERLINK|INCLUDE|TEMPLATE|MODIFY)\\b',
               Keyword),
              (
               '[a-zA-Z]\\w*\\b', Name.Function),
              (
               '#.*', Comment.Single),
              (
               '[,;\\(\\)]', Token.Punctuation),
              (
               '\\s+', Text)], 
       'string-literal': [
                        (
                         '\\\\[tnrfbae"\\\\]', String.Escape),
                        (
                         '"', Literal.String, '#pop'),
                        (
                         '[^\\\\"]+', Literal.String)]}


class GoodDataCLLexer(RegexLexer):
    """
    Lexer for `GoodData-CL <http://github.com/gooddata/GoodData-CL/raw/master/cli/src/main/resources/com/gooddata/processor/COMMANDS.txt>`_
    script files.

    *New in Pygments 1.4.*
    """
    name = 'GoodData-CL'
    aliases = ['gooddata-cl']
    filenames = ['*.gdc']
    mimetypes = ['text/x-gooddata-cl']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               '#.*', Comment.Single),
              (
               '[a-zA-Z]\\w*', Name.Function),
              (
               '\\(', Token.Punctuation, 'args-list'),
              (
               ';', Token.Punctuation),
              (
               '\\s+', Text)], 
       'args-list': [
                   (
                    '\\)', Token.Punctuation, '#pop'),
                   (
                    ',', Token.Punctuation),
                   (
                    '[a-zA-Z]\\w*', Name.Variable),
                   (
                    '=', Operator),
                   (
                    '"', Literal.String, 'string-literal'),
                   (
                    '[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]{1,3})?', Literal.Number),
                   (
                    '\\s', Text)], 
       'string-literal': [
                        (
                         '\\\\[tnrfbae"\\\\]', String.Escape),
                        (
                         '"', Literal.String, '#pop'),
                        (
                         '[^\\\\"]+', Literal.String)]}


class ProtoBufLexer(RegexLexer):
    """
    Lexer for `Protocol Buffer <http://code.google.com/p/protobuf/>`_
    definition files.

    *New in Pygments 1.4.*
    """
    name = 'Protocol Buffer'
    aliases = ['protobuf']
    filenames = ['*.proto']
    tokens = {'root': [
              (
               '[ \\t]+', Text),
              (
               '[,;{}\\[\\]\\(\\)]', Punctuation),
              (
               '/(\\\\\\n)?/(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
              (
               '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
              (
               '\\b(import|option|optional|required|repeated|default|packed|ctype|extensions|to|max|rpc|returns)\\b',
               Keyword),
              (
               '(int32|int64|uint32|uint64|sint32|sint64|fixed32|fixed64|sfixed32|sfixed64|float|double|bool|string|bytes)\\b',
               Keyword.Type),
              (
               '(true|false)\\b', Keyword.Constant),
              (
               '(package)(\\s+)', bygroups(Keyword.Namespace, Text), 'package'),
              (
               '(message|extend)(\\s+)',
               bygroups(Keyword.Declaration, Text), 'message'),
              (
               '(enum|group|service)(\\s+)',
               bygroups(Keyword.Declaration, Text), 'type'),
              (
               '\\".*\\"', String),
              (
               '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[LlUu]*', Number.Float),
              (
               '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
              (
               '(\\-?(inf|nan))', Number.Float),
              (
               '0x[0-9a-fA-F]+[LlUu]*', Number.Hex),
              (
               '0[0-7]+[LlUu]*', Number.Oct),
              (
               '\\d+[LlUu]*', Number.Integer),
              (
               '[+-=]', Operator),
              (
               '([a-zA-Z_][a-zA-Z0-9_\\.]*)([ \\t]*)(=)',
               bygroups(Name.Attribute, Text, Operator)),
              (
               '[a-zA-Z_][a-zA-Z0-9_\\.]*', Name)], 
       'package': [
                 (
                  '[a-zA-Z_][a-zA-Z0-9_]*', Name.Namespace, '#pop')], 
       'message': [
                 (
                  '[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop')], 
       'type': [
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Name, '#pop')]}


class HybrisLexer(RegexLexer):
    """
    For `Hybris <http://www.hybris-lang.org>`_ source code.

    *New in Pygments 1.4.*
    """
    name = 'Hybris'
    aliases = ['hybris', 'hy']
    filenames = ['*.hy', '*.hyb']
    mimetypes = ['text/x-hybris', 'application/x-hybris']
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [
              (
               '^(\\s*(?:function|method|operator\\s+)+?)([a-zA-Z_][a-zA-Z0-9_]*)(\\s*)(\\()',
               bygroups(Name.Function, Text, Operator)),
              (
               '[^\\S\\n]+', Text),
              (
               '//.*?\\n', Comment.Single),
              (
               '/\\*.*?\\*/', Comment.Multiline),
              (
               '@[a-zA-Z_][a-zA-Z0-9_\\.]*', Name.Decorator),
              (
               '(break|case|catch|next|default|do|else|finally|for|foreach|of|unless|if|new|return|switch|me|throw|try|while)\\b',
               Keyword),
              (
               '(extends|private|protected|public|static|throws|function|method|operator)\\b',
               Keyword.Declaration),
              (
               '(true|false|null|__FILE__|__LINE__|__VERSION__|__LIB_PATH__|__INC_PATH__)\\b',
               Keyword.Constant),
              (
               '(class|struct)(\\s+)',
               bygroups(Keyword.Declaration, Text), 'class'),
              (
               '(import|include)(\\s+)',
               bygroups(Keyword.Namespace, Text), 'import'),
              (
               '(gc_collect|gc_mm_items|gc_mm_usage|gc_collect_threshold|urlencode|urldecode|base64encode|base64decode|sha1|crc32|sha2|md5|md5_file|acos|asin|atan|atan2|ceil|cos|cosh|exp|fabs|floor|fmod|log|log10|pow|sin|sinh|sqrt|tan|tanh|isint|isfloat|ischar|isstring|isarray|ismap|isalias|typeof|sizeof|toint|tostring|fromxml|toxml|binary|pack|load|eval|var_names|var_values|user_functions|dyn_functions|methods|call|call_method|mknod|mkfifo|mount|umount2|umount|ticks|usleep|sleep|time|strtime|strdate|dllopen|dlllink|dllcall|dllcall_argv|dllclose|env|exec|fork|getpid|wait|popen|pclose|exit|kill|pthread_create|pthread_create_argv|pthread_exit|pthread_join|pthread_kill|smtp_send|http_get|http_post|http_download|socket|bind|listen|accept|getsockname|getpeername|settimeout|connect|server|recv|send|close|print|println|printf|input|readline|serial_open|serial_fcntl|serial_get_attr|serial_get_ispeed|serial_get_ospeed|serial_set_attr|serial_set_ispeed|serial_set_ospeed|serial_write|serial_read|serial_close|xml_load|xml_parse|fopen|fseek|ftell|fsize|fread|fwrite|fgets|fclose|file|readdir|pcre_replace|size|pop|unmap|has|keys|values|length|find|substr|replace|split|trim|remove|contains|join)\\b',
               Name.Builtin),
              (
               '(MethodReference|Runner|Dll|Thread|Pipe|Process|Runnable|CGI|ClientSocket|Socket|ServerSocket|File|Console|Directory|Exception)\\b',
               Keyword.Type),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               "'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-f]{4}'", String.Char),
              (
               '(\\.)([a-zA-Z_][a-zA-Z0-9_]*)',
               bygroups(Operator, Name.Attribute)),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*:', Name.Label),
              (
               '[a-zA-Z_\\$][a-zA-Z0-9_]*', Name),
              (
               '[~\\^\\*!%&\\[\\]\\(\\)\\{\\}<>\\|+=:;,./?\\-@]+', Operator),
              (
               '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
              (
               '0x[0-9a-f]+', Number.Hex),
              (
               '[0-9]+L?', Number.Integer),
              (
               '\\n', Text)], 
       'class': [
               (
                '[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop')], 
       'import': [
                (
                 '[a-zA-Z0-9_.]+\\*?', Name.Namespace, '#pop')]}