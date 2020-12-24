# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/julia.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 14179 bytes
"""
    pygments.lexers.julia
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Julia language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, words, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic
from pygments.util import shebang_matches, unirange
__all__ = [
 'JuliaLexer', 'JuliaConsoleLexer']
allowed_variable = '(?:[a-zA-Z_¡-\uffff]|%s)(?:[a-zA-Z_0-9¡-\uffff]|%s)*!*' % ((
 unirange(65536, 1114111),) * 2)

class JuliaLexer(RegexLexer):
    __doc__ = '\n    For `Julia <http://julialang.org/>`_ source code.\n\n    .. versionadded:: 1.6\n    '
    name = 'Julia'
    aliases = ['julia', 'jl']
    filenames = ['*.jl']
    mimetypes = ['text/x-julia', 'application/x-julia']
    flags = re.MULTILINE | re.UNICODE
    tokens = {'root':[
      (
       '\\n', Text),
      (
       '[^\\S\\n]+', Text),
      (
       '#=', Comment.Multiline, 'blockcomment'),
      (
       '#.*$', Comment),
      (
       '[\\[\\]{}(),;]', Punctuation),
      (
       'in\\b', Keyword.Pseudo),
      (
       'isa\\b', Keyword.Pseudo),
      (
       '(true|false)\\b', Keyword.Constant),
      (
       '(local|global|const)\\b', Keyword.Declaration),
      (
       words([
        'function', 'type', 'typealias', 'abstract', 'immutable',
        'baremodule', 'begin', 'bitstype', 'break', 'catch', 'ccall',
        'continue', 'do', 'else', 'elseif', 'end', 'export', 'finally',
        'for', 'if', 'import', 'importall', 'let', 'macro', 'module',
        'mutable', 'primitive', 'quote', 'return', 'struct', 'try',
        'using', 'while'],
         suffix='\\b'), Keyword),
      (
       words([
        'ANY', 'ASCIIString', 'AbstractArray', 'AbstractChannel',
        'AbstractFloat', 'AbstractMatrix', 'AbstractRNG',
        'AbstractSparseArray', 'AbstractSparseMatrix',
        'AbstractSparseVector', 'AbstractString', 'AbstractVecOrMat',
        'AbstractVector', 'Any', 'ArgumentError', 'Array',
        'AssertionError', 'Associative', 'Base64DecodePipe',
        'Base64EncodePipe', 'Bidiagonal', 'BigFloat', 'BigInt',
        'BitArray', 'BitMatrix', 'BitVector', 'Bool', 'BoundsError',
        'Box', 'BufferStream', 'CapturedException', 'CartesianIndex',
        'CartesianRange', 'Cchar', 'Cdouble', 'Cfloat', 'Channel',
        'Char', 'Cint', 'Cintmax_t', 'Clong', 'Clonglong',
        'ClusterManager', 'Cmd', 'Coff_t', 'Colon', 'Complex',
        'Complex128', 'Complex32', 'Complex64', 'CompositeException',
        'Condition', 'Cptrdiff_t', 'Cshort', 'Csize_t', 'Cssize_t',
        'Cstring', 'Cuchar', 'Cuint', 'Cuintmax_t', 'Culong',
        'Culonglong', 'Cushort', 'Cwchar_t', 'Cwstring', 'DataType',
        'Date', 'DateTime', 'DenseArray', 'DenseMatrix',
        'DenseVecOrMat', 'DenseVector', 'Diagonal', 'Dict',
        'DimensionMismatch', 'Dims', 'DirectIndexString', 'Display',
        'DivideError', 'DomainError', 'EOFError', 'EachLine', 'Enum',
        'Enumerate', 'ErrorException', 'Exception', 'Expr',
        'Factorization', 'FileMonitor', 'FileOffset', 'Filter',
        'Float16', 'Float32', 'Float64', 'FloatRange', 'Function',
        'GenSym', 'GlobalRef', 'GotoNode', 'HTML', 'Hermitian', 'IO',
        'IOBuffer', 'IOStream', 'IPv4', 'IPv6', 'InexactError',
        'InitError', 'Int', 'Int128', 'Int16', 'Int32', 'Int64', 'Int8',
        'IntSet', 'Integer', 'InterruptException', 'IntrinsicFunction',
        'InvalidStateException', 'Irrational', 'KeyError', 'LabelNode',
        'LambdaStaticData', 'LinSpace', 'LineNumberNode', 'LoadError',
        'LocalProcess', 'LowerTriangular', 'MIME', 'Matrix',
        'MersenneTwister', 'Method', 'MethodError', 'MethodTable',
        'Module', 'NTuple', 'NewvarNode', 'NullException', 'Nullable',
        'Number', 'ObjectIdDict', 'OrdinalRange', 'OutOfMemoryError',
        'OverflowError', 'Pair', 'ParseError', 'PartialQuickSort',
        'Pipe', 'PollingFileWatcher', 'ProcessExitedException',
        'ProcessGroup', 'Ptr', 'QuoteNode', 'RandomDevice', 'Range',
        'Rational', 'RawFD', 'ReadOnlyMemoryError', 'Real',
        'ReentrantLock', 'Ref', 'Regex', 'RegexMatch',
        'RemoteException', 'RemoteRef', 'RepString', 'RevString',
        'RopeString', 'RoundingMode', 'SegmentationFault',
        'SerializationState', 'Set', 'SharedArray', 'SharedMatrix',
        'SharedVector', 'Signed', 'SimpleVector', 'SparseMatrixCSC',
        'StackOverflowError', 'StatStruct', 'StepRange', 'StridedArray',
        'StridedMatrix', 'StridedVecOrMat', 'StridedVector', 'SubArray',
        'SubString', 'SymTridiagonal', 'Symbol', 'SymbolNode',
        'Symmetric', 'SystemError', 'TCPSocket', 'Task', 'Text',
        'TextDisplay', 'Timer', 'TopNode', 'Tridiagonal', 'Tuple',
        'Type', 'TypeConstructor', 'TypeError', 'TypeName', 'TypeVar',
        'UDPSocket', 'UInt', 'UInt128', 'UInt16', 'UInt32', 'UInt64',
        'UInt8', 'UTF16String', 'UTF32String', 'UTF8String',
        'UndefRefError', 'UndefVarError', 'UnicodeError', 'UniformScaling',
        'Union', 'UnitRange', 'Unsigned', 'UpperTriangular', 'Val',
        'Vararg', 'VecOrMat', 'Vector', 'VersionNumber', 'Void', 'WString',
        'WeakKeyDict', 'WeakRef', 'WorkerConfig', 'Zip'],
         suffix='\\b'),
       Keyword.Type),
      (
       words([
        'ARGS', 'CPU_CORES', 'C_NULL', 'DevNull', 'ENDIAN_BOM',
        'ENV', 'I', 'Inf', 'Inf16', 'Inf32', 'Inf64',
        'InsertionSort', 'JULIA_HOME', 'LOAD_PATH', 'MergeSort',
        'NaN', 'NaN16', 'NaN32', 'NaN64', 'OS_NAME',
        'QuickSort', 'RoundDown', 'RoundFromZero', 'RoundNearest',
        'RoundNearestTiesAway', 'RoundNearestTiesUp',
        'RoundToZero', 'RoundUp', 'STDERR', 'STDIN', 'STDOUT',
        'VERSION', 'WORD_SIZE', 'catalan', 'e', 'eu',
        'eulergamma', 'golden', 'im', 'nothing', 'pi', 'γ',
        'π', 'φ'],
         suffix='\\b'), Name.Builtin),
      (
       words([
        '=', ':=', '+=', '-=', '*=', '/=', '//=', './/=', '.*=', './=',
        '\\=', '.\\=', '^=', '.^=', '÷=', '.÷=', '%=', '.%=', '|=', '&=',
        '$=', '=>', '<<=', '>>=', '>>>=', '~', '.+=', '.-=',
        '?',
        '--', '-->',
        '||',
        '&&',
        '>', '<', '>=', '≥', '<=', '≤', '==', '===', '≡', '!=', '≠',
        '!==', '≢', '.>', '.<', '.>=', '.≥', '.<=', '.≤', '.==', '.!=',
        '.≠', '.=', '.!', '<:', '>:', '∈', '∉', '∋', '∌', '⊆',
        '⊈', '⊂',
        '⊄', '⊊',
        '|>', '<|',
        ':',
        '+', '-', '.+', '.-', '|', '∪', '$',
        '<<', '>>', '>>>', '.<<', '.>>', '.>>>',
        '*', '/', './', '÷', '.÷', '%', '⋅', '.%', '.*', '\\', '.\\', '&', '∩',
        '//', './/',
        '^', '.^',
        '::',
        '.',
        '+', '-', '!', '√', '∛', '∜']),
       Operator),
      (
       "'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,3}|\\\\u[a-fA-F0-9]{1,4}|\\\\U[a-fA-F0-9]{1,6}|[^\\\\\\'\\n])'",
       String.Char),
      (
       "(?<=[.\\w)\\]])\\'+", Operator),
      (
       '"""', String, 'tqstring'),
      (
       '"', String, 'string'),
      (
       'r"""', String.Regex, 'tqregex'),
      (
       'r"', String.Regex, 'regex'),
      (
       '`', String.Backtick, 'command'),
      (
       allowed_variable, Name),
      (
       '@' + allowed_variable, Name.Decorator),
      (
       '(\\d+(_\\d+)+\\.\\d*|\\d*\\.\\d+(_\\d+)+)([eEf][+-]?[0-9]+)?', Number.Float),
      (
       '(\\d+\\.\\d*|\\d*\\.\\d+)([eEf][+-]?[0-9]+)?', Number.Float),
      (
       '\\d+(_\\d+)+[eEf][+-]?[0-9]+', Number.Float),
      (
       '\\d+[eEf][+-]?[0-9]+', Number.Float),
      (
       '0b[01]+(_[01]+)+', Number.Bin),
      (
       '0b[01]+', Number.Bin),
      (
       '0o[0-7]+(_[0-7]+)+', Number.Oct),
      (
       '0o[0-7]+', Number.Oct),
      (
       '0x[a-fA-F0-9]+(_[a-fA-F0-9]+)+', Number.Hex),
      (
       '0x[a-fA-F0-9]+', Number.Hex),
      (
       '\\d+(_\\d+)+', Number.Integer),
      (
       '\\d+', Number.Integer)], 
     'blockcomment':[
      (
       '[^=#]', Comment.Multiline),
      (
       '#=', Comment.Multiline, '#push'),
      (
       '=#', Comment.Multiline, '#pop'),
      (
       '[=#]', Comment.Multiline)], 
     'string':[
      (
       '"', String, '#pop'),
      (
       '\\\\([\\\\"\\\'$nrbtfav]|(x|u|U)[a-fA-F0-9]+|\\d+)', String.Escape),
      (
       '\\$' + allowed_variable, String.Interpol),
      (
       '(\\$)(\\()', bygroups(String.Interpol, Punctuation), 'in-intp'),
      (
       '%[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[E-GXc-giorsux%]',
       String.Interpol),
      (
       '.|\\s', String)], 
     'tqstring':[
      (
       '"""', String, '#pop'),
      (
       '\\\\([\\\\"\\\'$nrbtfav]|(x|u|U)[a-fA-F0-9]+|\\d+)', String.Escape),
      (
       '\\$' + allowed_variable, String.Interpol),
      (
       '(\\$)(\\()', bygroups(String.Interpol, Punctuation), 'in-intp'),
      (
       '.|\\s', String)], 
     'regex':[
      (
       '"', String.Regex, '#pop'),
      (
       '\\\\"', String.Regex),
      (
       '.|\\s', String.Regex)], 
     'tqregex':[
      (
       '"""', String.Regex, '#pop'),
      (
       '.|\\s', String.Regex)], 
     'command':[
      (
       '`', String.Backtick, '#pop'),
      (
       '\\$' + allowed_variable, String.Interpol),
      (
       '(\\$)(\\()', bygroups(String.Interpol, Punctuation), 'in-intp'),
      (
       '.|\\s', String.Backtick)], 
     'in-intp':[
      (
       '\\(', Punctuation, '#push'),
      (
       '\\)', Punctuation, '#pop'),
      include('root')]}

    def analyse_text(text):
        return shebang_matches(text, 'julia')


class JuliaConsoleLexer(Lexer):
    __doc__ = '\n    For Julia console sessions. Modeled after MatlabSessionLexer.\n\n    .. versionadded:: 1.6\n    '
    name = 'Julia console'
    aliases = ['jlcon']

    def get_tokens_unprocessed(self, text):
        jllexer = JuliaLexer(**self.options)
        start = 0
        curcode = ''
        insertions = []
        output = False
        error = False
        for line in text.splitlines(True):
            if line.startswith('julia>'):
                insertions.append((len(curcode), [(0, Generic.Prompt, line[:6])]))
                curcode += line[6:]
                output = False
                error = False
            else:
                if line.startswith('help?>') or line.startswith('shell>'):
                    yield (
                     start, Generic.Prompt, line[:6])
                    yield (start + 6, Text, line[6:])
                    output = False
                    error = False
                else:
                    if line.startswith('      ') and not output:
                        insertions.append((len(curcode), [(0, Text, line[:6])]))
                        curcode += line[6:]
                    else:
                        if curcode:
                            for item in do_insertions(insertions, jllexer.get_tokens_unprocessed(curcode)):
                                yield item

                            curcode = ''
                            insertions = []
                        else:
                            if line.startswith('ERROR: ') or error:
                                yield (
                                 start, Generic.Error, line)
                                error = True
                            else:
                                yield (
                                 start, Generic.Output, line)
                        output = True
            start += len(line)

        if curcode:
            for item in do_insertions(insertions, jllexer.get_tokens_unprocessed(curcode)):
                yield item