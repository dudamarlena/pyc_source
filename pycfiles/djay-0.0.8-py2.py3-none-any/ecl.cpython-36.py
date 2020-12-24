# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/ecl.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 5875 bytes
"""
    pygments.lexers.ecl
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the ECL language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
__all__ = [
 'ECLLexer']

class ECLLexer(RegexLexer):
    __doc__ = '\n    Lexer for the declarative big-data `ECL\n    <http://hpccsystems.com/community/docs/ecl-language-reference/html>`_\n    language.\n\n    .. versionadded:: 1.5\n    '
    name = 'ECL'
    aliases = ['ecl']
    filenames = ['*.ecl']
    mimetypes = ['application/x-ecl']
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root':[
      include('whitespace'),
      include('statements')], 
     'whitespace':[
      (
       '\\s+', Text),
      (
       '\\/\\/.*', Comment.Single),
      (
       '/(\\\\\\n)?\\*(.|\\n)*?\\*(\\\\\\n)?/', Comment.Multiline)], 
     'statements':[
      include('types'),
      include('keywords'),
      include('functions'),
      include('hash'),
      (
       '"', String, 'string'),
      (
       "\\'", String, 'string'),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)e[+-]?\\d+[lu]*', Number.Float),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+f)f?', Number.Float),
      (
       '0x[0-9a-f]+[lu]*', Number.Hex),
      (
       '0[0-7]+[lu]*', Number.Oct),
      (
       '\\d+[lu]*', Number.Integer),
      (
       '\\*/', Error),
      (
       '[~!%^&*+=|?:<>/-]+', Operator),
      (
       '[{}()\\[\\],.;]', Punctuation),
      (
       '[a-z_]\\w*', Name)], 
     'hash':[
      (
       '^#.*$', Comment.Preproc)], 
     'types':[
      (
       '(RECORD|END)\\D', Keyword.Declaration),
      (
       '((?:ASCII|BIG_ENDIAN|BOOLEAN|DATA|DECIMAL|EBCDIC|INTEGER|PATTERN|QSTRING|REAL|RECORD|RULE|SET OF|STRING|TOKEN|UDECIMAL|UNICODE|UNSIGNED|VARSTRING|VARUNICODE)\\d*)(\\s+)',
       bygroups(Keyword.Type, Text))], 
     'keywords':[
      (
       words(('APPLY', 'ASSERT', 'BUILD', 'BUILDINDEX', 'EVALUATE', 'FAIL', 'KEYDIFF', 'KEYPATCH',
       'LOADXML', 'NOTHOR', 'NOTIFY', 'OUTPUT', 'PARALLEL', 'SEQUENTIAL', 'SOAPCALL',
       'CHECKPOINT', 'DEPRECATED', 'FAILCODE', 'FAILMESSAGE', 'FAILURE', 'GLOBAL',
       'INDEPENDENT', 'ONWARNING', 'PERSIST', 'PRIORITY', 'RECOVERY', 'STORED', 'SUCCESS',
       'WAIT', 'WHEN'),
         suffix='\\b'),
       Keyword.Reserved),
      (
       words(('ALL', 'AND', 'ANY', 'AS', 'ATMOST', 'BEFORE', 'BEGINC++', 'BEST', 'BETWEEN',
       'CASE', 'CONST', 'COUNTER', 'CSV', 'DESCEND', 'ENCRYPT', 'ENDC++', 'ENDMACRO',
       'EXCEPT', 'EXCLUSIVE', 'EXPIRE', 'EXPORT', 'EXTEND', 'FALSE', 'FEW', 'FIRST',
       'FLAT', 'FULL', 'FUNCTION', 'GROUP', 'HEADER', 'HEADING', 'HOLE', 'IFBLOCK',
       'IMPORT', 'IN', 'JOINED', 'KEEP', 'KEYED', 'LAST', 'LEFT', 'LIMIT', 'LOAD',
       'LOCAL', 'LOCALE', 'LOOKUP', 'MACRO', 'MANY', 'MAXCOUNT', 'MAXLENGTH', 'MIN SKEW',
       'MODULE', 'INTERFACE', 'NAMED', 'NOCASE', 'NOROOT', 'NOSCAN', 'NOSORT', 'NOT',
       'OF', 'ONLY', 'OPT', 'OR', 'OUTER', 'OVERWRITE', 'PACKED', 'PARTITION', 'PENALTY',
       'PHYSICALLENGTH', 'PIPE', 'QUOTE', 'RELATIONSHIP', 'REPEAT', 'RETURN', 'RIGHT',
       'SCAN', 'SELF', 'SEPARATOR', 'SERVICE', 'SHARED', 'SKEW', 'SKIP', 'SQL', 'STORE',
       'TERMINATOR', 'THOR', 'THRESHOLD', 'TOKEN', 'TRANSFORM', 'TRIM', 'TRUE', 'TYPE',
       'UNICODEORDER', 'UNSORTED', 'VALIDATE', 'VIRTUAL', 'WHOLE', 'WILD', 'WITHIN',
       'XML', 'XPATH', '__COMPRESSED__'),
         suffix='\\b'),
       Keyword.Reserved)], 
     'functions':[
      (
       words(('ABS', 'ACOS', 'ALLNODES', 'ASCII', 'ASIN', 'ASSTRING', 'ATAN', 'ATAN2', 'AVE',
       'CASE', 'CHOOSE', 'CHOOSEN', 'CHOOSESETS', 'CLUSTERSIZE', 'COMBINE', 'CORRELATION',
       'COS', 'COSH', 'COUNT', 'COVARIANCE', 'CRON', 'DATASET', 'DEDUP', 'DEFINE',
       'DENORMALIZE', 'DISTRIBUTE', 'DISTRIBUTED', 'DISTRIBUTION', 'EBCDIC', 'ENTH',
       'ERROR', 'EVALUATE', 'EVENT', 'EVENTEXTRA', 'EVENTNAME', 'EXISTS', 'EXP',
       'FAILCODE', 'FAILMESSAGE', 'FETCH', 'FROMUNICODE', 'GETISVALID', 'GLOBAL',
       'GRAPH', 'GROUP', 'HASH', 'HASH32', 'HASH64', 'HASHCRC', 'HASHMD5', 'HAVING',
       'IF', 'INDEX', 'INTFORMAT', 'ISVALID', 'ITERATE', 'JOIN', 'KEYUNICODE', 'LENGTH',
       'LIBRARY', 'LIMIT', 'LN', 'LOCAL', 'LOG', 'LOOP', 'MAP', 'MATCHED', 'MATCHLENGTH',
       'MATCHPOSITION', 'MATCHTEXT', 'MATCHUNICODE', 'MAX', 'MERGE', 'MERGEJOIN',
       'MIN', 'NOLOCAL', 'NONEMPTY', 'NORMALIZE', 'PARSE', 'PIPE', 'POWER', 'PRELOAD',
       'PROCESS', 'PROJECT', 'PULL', 'RANDOM', 'RANGE', 'RANK', 'RANKED', 'REALFORMAT',
       'RECORDOF', 'REGEXFIND', 'REGEXREPLACE', 'REGROUP', 'REJECTED', 'ROLLUP',
       'ROUND', 'ROUNDUP', 'ROW', 'ROWDIFF', 'SAMPLE', 'SET', 'SIN', 'SINH', 'SIZEOF',
       'SOAPCALL', 'SORT', 'SORTED', 'SQRT', 'STEPPED', 'STORED', 'SUM', 'TABLE',
       'TAN', 'TANH', 'THISNODE', 'TOPN', 'TOUNICODE', 'TRANSFER', 'TRIM', 'TRUNCATE',
       'TYPEOF', 'UNGROUP', 'UNICODEORDER', 'VARIANCE', 'WHICH', 'WORKUNIT', 'XMLDECODE',
       'XMLENCODE', 'XMLTEXT', 'XMLUNICODE'),
         suffix='\\b'),
       Name.Function)], 
     'string':[
      (
       '"', String, '#pop'),
      (
       "\\'", String, '#pop'),
      (
       '[^"\\\']+', String)]}