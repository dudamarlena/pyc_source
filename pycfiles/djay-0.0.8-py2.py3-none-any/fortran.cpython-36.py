# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/fortran.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 9841 bytes
"""
    pygments.lexers.fortran
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Fortran languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, include, words, using, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic
__all__ = [
 'FortranLexer', 'FortranFixedLexer']

class FortranLexer(RegexLexer):
    __doc__ = '\n    Lexer for FORTRAN 90 code.\n\n    .. versionadded:: 0.10\n    '
    name = 'Fortran'
    aliases = ['fortran']
    filenames = ['*.f03', '*.f90', '*.F03', '*.F90']
    mimetypes = ['text/x-fortran']
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root':[
      (
       '^#.*\\n', Comment.Preproc),
      (
       '!.*\\n', Comment),
      include('strings'),
      include('core'),
      (
       '[a-z][\\w$]*', Name),
      include('nums'),
      (
       '[\\s]+', Text)], 
     'core':[
      (
       words(('ABSTRACT', 'ACCEPT', 'ALL', 'ALLSTOP', 'ALLOCATABLE', 'ALLOCATE', 'ARRAY',
       'ASSIGN', 'ASSOCIATE', 'ASYNCHRONOUS', 'BACKSPACE', 'BIND', 'BLOCK', 'BLOCKDATA',
       'BYTE', 'CALL', 'CASE', 'CLASS', 'CLOSE', 'CODIMENSION', 'COMMON', 'CONCURRRENT',
       'CONTIGUOUS', 'CONTAINS', 'CONTINUE', 'CRITICAL', 'CYCLE', 'DATA', 'DEALLOCATE',
       'DECODE', 'DEFERRED', 'DIMENSION', 'DO', 'ELEMENTAL', 'ELSE', 'ENCODE', 'END',
       'ENTRY', 'ENUM', 'ENUMERATOR', 'EQUIVALENCE', 'EXIT', 'EXTENDS', 'EXTERNAL',
       'EXTRINSIC', 'FILE', 'FINAL', 'FORALL', 'FORMAT', 'FUNCTION', 'GENERIC', 'GOTO',
       'IF', 'IMAGES', 'IMPLICIT', 'IMPORT', 'IMPURE', 'INCLUDE', 'INQUIRE', 'INTENT',
       'INTERFACE', 'INTRINSIC', 'IS', 'LOCK', 'MEMORY', 'MODULE', 'NAMELIST', 'NULLIFY',
       'NONE', 'NON_INTRINSIC', 'NON_OVERRIDABLE', 'NOPASS', 'OPEN', 'OPTIONAL',
       'OPTIONS', 'PARAMETER', 'PASS', 'PAUSE', 'POINTER', 'PRINT', 'PRIVATE', 'PROGRAM',
       'PROCEDURE', 'PROTECTED', 'PUBLIC', 'PURE', 'READ', 'RECURSIVE', 'RESULT',
       'RETURN', 'REWIND', 'SAVE', 'SELECT', 'SEQUENCE', 'STOP', 'SUBMODULE', 'SUBROUTINE',
       'SYNC', 'SYNCALL', 'SYNCIMAGES', 'SYNCMEMORY', 'TARGET', 'THEN', 'TYPE', 'UNLOCK',
       'USE', 'VALUE', 'VOLATILE', 'WHERE', 'WRITE', 'WHILE'),
         prefix='\\b', suffix='\\s*\\b'),
       Keyword),
      (
       words(('CHARACTER', 'COMPLEX', 'DOUBLE PRECISION', 'DOUBLE COMPLEX', 'INTEGER', 'LOGICAL',
       'REAL', 'C_INT', 'C_SHORT', 'C_LONG', 'C_LONG_LONG', 'C_SIGNED_CHAR', 'C_SIZE_T',
       'C_INT8_T', 'C_INT16_T', 'C_INT32_T', 'C_INT64_T', 'C_INT_LEAST8_T', 'C_INT_LEAST16_T',
       'C_INT_LEAST32_T', 'C_INT_LEAST64_T', 'C_INT_FAST8_T', 'C_INT_FAST16_T', 'C_INT_FAST32_T',
       'C_INT_FAST64_T', 'C_INTMAX_T', 'C_INTPTR_T', 'C_FLOAT', 'C_DOUBLE', 'C_LONG_DOUBLE',
       'C_FLOAT_COMPLEX', 'C_DOUBLE_COMPLEX', 'C_LONG_DOUBLE_COMPLEX', 'C_BOOL',
       'C_CHAR', 'C_PTR', 'C_FUNPTR'),
         prefix='\\b',
         suffix='\\s*\\b'),
       Keyword.Type),
      (
       '(\\*\\*|\\*|\\+|-|\\/|<|>|<=|>=|==|\\/=|=)', Operator),
      (
       '(::)', Keyword.Declaration),
      (
       '[()\\[\\],:&%;.]', Punctuation),
      (
       words(('Abort', 'Abs', 'Access', 'AChar', 'ACos', 'ACosH', 'AdjustL', 'AdjustR', 'AImag',
       'AInt', 'Alarm', 'All', 'Allocated', 'ALog', 'AMax', 'AMin', 'AMod', 'And',
       'ANInt', 'Any', 'ASin', 'ASinH', 'Associated', 'ATan', 'ATanH', 'Atomic_Define',
       'Atomic_Ref', 'BesJ', 'BesJN', 'Bessel_J0', 'Bessel_J1', 'Bessel_JN', 'Bessel_Y0',
       'Bessel_Y1', 'Bessel_YN', 'BesY', 'BesYN', 'BGE', 'BGT', 'BLE', 'BLT', 'Bit_Size',
       'BTest', 'CAbs', 'CCos', 'Ceiling', 'CExp', 'Char', 'ChDir', 'ChMod', 'CLog',
       'Cmplx', 'Command_Argument_Count', 'Complex', 'Conjg', 'Cos', 'CosH', 'Count',
       'CPU_Time', 'CShift', 'CSin', 'CSqRt', 'CTime', 'C_Loc', 'C_Associated', 'C_Null_Ptr',
       'C_Null_Funptr', 'C_F_Pointer', 'C_F_ProcPointer', 'C_Null_Char', 'C_Alert',
       'C_Backspace', 'C_Form_Feed', 'C_FunLoc', 'C_Sizeof', 'C_New_Line', 'C_Carriage_Return',
       'C_Horizontal_Tab', 'C_Vertical_Tab', 'DAbs', 'DACos', 'DASin', 'DATan', 'Date_and_Time',
       'DbesJ', 'DbesJN', 'DbesY', 'DbesYN', 'Dble', 'DCos', 'DCosH', 'DDiM', 'DErF',
       'DErFC', 'DExp', 'Digits', 'DiM', 'DInt', 'DLog', 'DMax', 'DMin', 'DMod',
       'DNInt', 'Dot_Product', 'DProd', 'DSign', 'DSinH', 'DShiftL', 'DShiftR', 'DSin',
       'DSqRt', 'DTanH', 'DTan', 'DTime', 'EOShift', 'Epsilon', 'ErF', 'ErFC', 'ErFC_Scaled',
       'ETime', 'Execute_Command_Line', 'Exit', 'Exp', 'Exponent', 'Extends_Type_Of',
       'FDate', 'FGet', 'FGetC', 'FindLoc', 'Float', 'Floor', 'Flush', 'FNum', 'FPutC',
       'FPut', 'Fraction', 'FSeek', 'FStat', 'FTell', 'Gamma', 'GError', 'GetArg',
       'Get_Command', 'Get_Command_Argument', 'Get_Environment_Variable', 'GetCWD',
       'GetEnv', 'GetGId', 'GetLog', 'GetPId', 'GetUId', 'GMTime', 'HostNm', 'Huge',
       'Hypot', 'IAbs', 'IAChar', 'IAll', 'IAnd', 'IAny', 'IArgC', 'IBClr', 'IBits',
       'IBSet', 'IChar', 'IDate', 'IDiM', 'IDInt', 'IDNInt', 'IEOr', 'IErrNo', 'IFix',
       'Imag', 'ImagPart', 'Image_Index', 'Index', 'Int', 'IOr', 'IParity', 'IRand',
       'IsaTty', 'IShft', 'IShftC', 'ISign', 'Iso_C_Binding', 'Is_Contiguous', 'Is_Iostat_End',
       'Is_Iostat_Eor', 'ITime', 'Kill', 'Kind', 'LBound', 'LCoBound', 'Len', 'Len_Trim',
       'LGe', 'LGt', 'Link', 'LLe', 'LLt', 'LnBlnk', 'Loc', 'Log', 'Log_Gamma', 'Logical',
       'Long', 'LShift', 'LStat', 'LTime', 'MaskL', 'MaskR', 'MatMul', 'Max', 'MaxExponent',
       'MaxLoc', 'MaxVal', 'MClock', 'Merge', 'Merge_Bits', 'Move_Alloc', 'Min',
       'MinExponent', 'MinLoc', 'MinVal', 'Mod', 'Modulo', 'MvBits', 'Nearest', 'New_Line',
       'NInt', 'Norm2', 'Not', 'Null', 'Num_Images', 'Or', 'Pack', 'Parity', 'PError',
       'Precision', 'Present', 'Product', 'Radix', 'Rand', 'Random_Number', 'Random_Seed',
       'Range', 'Real', 'RealPart', 'Rename', 'Repeat', 'Reshape', 'RRSpacing', 'RShift',
       'Same_Type_As', 'Scale', 'Scan', 'Second', 'Selected_Char_Kind', 'Selected_Int_Kind',
       'Selected_Real_Kind', 'Set_Exponent', 'Shape', 'ShiftA', 'ShiftL', 'ShiftR',
       'Short', 'Sign', 'Signal', 'SinH', 'Sin', 'Sleep', 'Sngl', 'Spacing', 'Spread',
       'SqRt', 'SRand', 'Stat', 'Storage_Size', 'Sum', 'SymLnk', 'System', 'System_Clock',
       'Tan', 'TanH', 'Time', 'This_Image', 'Tiny', 'TrailZ', 'Transfer', 'Transpose',
       'Trim', 'TtyNam', 'UBound', 'UCoBound', 'UMask', 'Unlink', 'Unpack', 'Verify',
       'XOr', 'ZAbs', 'ZCos', 'ZExp', 'ZLog', 'ZSin', 'ZSqRt'),
         prefix='\\b', suffix='\\s*\\b'),
       Name.Builtin),
      (
       '\\.(true|false)\\.', Name.Builtin),
      (
       '\\.(eq|ne|lt|le|gt|ge|not|and|or|eqv|neqv)\\.', Operator.Word)], 
     'strings':[
      (
       '(?s)"(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\])*"', String.Double),
      (
       "(?s)'(\\\\\\\\|\\\\[0-7]+|\\\\.|[^'\\\\])*'", String.Single)], 
     'nums':[
      (
       '\\d+(?![.e])(_[a-z]\\w+)?', Number.Integer),
      (
       '[+-]?\\d*\\.\\d+([ed][-+]?\\d+)?(_[a-z]\\w+)?', Number.Float),
      (
       '[+-]?\\d+\\.\\d*([ed][-+]?\\d+)?(_[a-z]\\w+)?', Number.Float),
      (
       '[+-]?\\d+(\\.\\d*)?[ed][-+]?\\d+(_[a-z]\\w+)?', Number.Float)]}


class FortranFixedLexer(RegexLexer):
    __doc__ = '\n    Lexer for fixed format Fortran.\n\n    .. versionadded:: 2.1\n    '
    name = 'FortranFixed'
    aliases = ['fortranfixed']
    filenames = ['*.f', '*.F']
    flags = re.IGNORECASE

    def _lex_fortran(self, match, ctx=None):
        """Lex a line just as free form fortran without line break."""
        lexer = FortranLexer()
        text = match.group(0) + '\n'
        for index, token, value in lexer.get_tokens_unprocessed(text):
            value = value.replace('\n', '')
            if value != '':
                yield (
                 index, token, value)

    tokens = {'root':[
      (
       '[C*].*\\n', Comment),
      (
       '#.*\\n', Comment.Preproc),
      (
       ' {0,4}!.*\\n', Comment),
      (
       '(.{5})', Name.Label, 'cont-char'),
      (
       '.*\\n', using(FortranLexer))], 
     'cont-char':[
      (
       ' ', Text, 'code'),
      (
       '0', Comment, 'code'),
      (
       '.', Generic.Strong, 'code')], 
     'code':[
      (
       '(.{66})(.*)(\\n)',
       bygroups(_lex_fortran, Comment, Text), 'root'),
      (
       '(.*)(\\n)', bygroups(_lex_fortran, Text), 'root'),
      default('root')]}