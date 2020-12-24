# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/math.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.math
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for math languages.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, bygroups, include, do_insertions
from pygments.token import Comment, String, Punctuation, Keyword, Name, Operator, Number, Text, Generic
from pygments.lexers.agile import PythonLexer
__all__ = [
 'MuPADLexer', 'MatlabLexer', 'MatlabSessionLexer', 'NumPyLexer',
 'RConsoleLexer', 'SLexer']

class MuPADLexer(RegexLexer):
    """
    A `MuPAD <http://www.mupad.com>`_ lexer.
    Contributed by Christopher Creutzig <christopher@creutzig.de>.

    *New in Pygments 0.8.*
    """
    name = 'MuPAD'
    aliases = ['mupad']
    filenames = ['*.mu']
    tokens = {'root': [
              (
               '//.*?$', Comment.Single),
              (
               '/\\*', Comment.Multiline, 'comment'),
              (
               '"(?:[^"\\\\]|\\\\.)*"', String),
              (
               '\\(|\\)|\\[|\\]|\\{|\\}', Punctuation),
              (
               '(?x)\\b(?:\n            next|break|end|\n            axiom|end_axiom|category|end_category|domain|end_domain|inherits|\n            if|%if|then|elif|else|end_if|\n            case|of|do|otherwise|end_case|\n            while|end_while|\n            repeat|until|end_repeat|\n            for|from|to|downto|step|end_for|\n            proc|local|option|save|begin|end_proc|\n            delete|frame\n          )\\b', Keyword),
              (
               '(?x)\\b(?:\n            DOM_ARRAY|DOM_BOOL|DOM_COMPLEX|DOM_DOMAIN|DOM_EXEC|DOM_EXPR|\n            DOM_FAIL|DOM_FLOAT|DOM_FRAME|DOM_FUNC_ENV|DOM_HFARRAY|DOM_IDENT|\n            DOM_INT|DOM_INTERVAL|DOM_LIST|DOM_NIL|DOM_NULL|DOM_POLY|DOM_PROC|\n            DOM_PROC_ENV|DOM_RAT|DOM_SET|DOM_STRING|DOM_TABLE|DOM_VAR\n          )\\b', Name.Class),
              (
               '(?x)\\b(?:\n            PI|EULER|E|CATALAN|\n            NIL|FAIL|undefined|infinity|\n            TRUE|FALSE|UNKNOWN\n          )\\b',
               Name.Constant),
              (
               '\\b(?:dom|procname)\\b', Name.Builtin.Pseudo),
              (
               "\\.|,|:|;|=|\\+|-|\\*|/|\\^|@|>|<|\\$|\\||!|\\'|%|~=", Operator),
              (
               '(?x)\\b(?:\n            and|or|not|xor|\n            assuming|\n            div|mod|\n            union|minus|intersect|in|subset\n          )\\b',
               Operator.Word),
              (
               '\\b(?:I|RDN_INF|RD_NINF|RD_NAN)\\b', Number),
              (
               '(?x)\n          ((?:[a-zA-Z_#][a-zA-Z_#0-9]*|`[^`]*`)\n          (?:::[a-zA-Z_#][a-zA-Z_#0-9]*|`[^`]*`)*)\\s*([(])',
               bygroups(Name.Function, Punctuation)),
              (
               '(?x)\n          (?:[a-zA-Z_#][a-zA-Z_#0-9]*|`[^`]*`)\n          (?:::[a-zA-Z_#][a-zA-Z_#0-9]*|`[^`]*`)*', Name.Variable),
              (
               '[0-9]+(?:\\.[0-9]*)?(?:e[0-9]+)?', Number),
              (
               '\\.[0-9]+(?:e[0-9]+)?', Number),
              (
               '.', Text)], 
       'comment': [
                 (
                  '[^*/]', Comment.Multiline),
                 (
                  '/\\*', Comment.Multiline, '#push'),
                 (
                  '\\*/', Comment.Multiline, '#pop'),
                 (
                  '[*/]', Comment.Multiline)]}


class MatlabLexer(RegexLexer):
    """
    For Matlab (or GNU Octave) source code.
    Contributed by Ken Schutte <kschutte@csail.mit.edu>.

    *New in Pygments 0.10.*
    """
    name = 'Matlab'
    aliases = ['matlab', 'octave']
    filenames = ['*.m']
    mimetypes = ['text/matlab']
    elfun = [
     'sin', 'sind', 'sinh', 'asin', 'asind', 'asinh', 'cos', 'cosd', 'cosh',
     'acos', 'acosd', 'acosh', 'tan', 'tand', 'tanh', 'atan', 'atand', 'atan2',
     'atanh', 'sec', 'secd', 'sech', 'asec', 'asecd', 'asech', 'csc', 'cscd',
     'csch', 'acsc', 'acscd', 'acsch', 'cot', 'cotd', 'coth', 'acot', 'acotd',
     'acoth', 'hypot', 'exp', 'expm1', 'log', 'log1p', 'log10', 'log2', 'pow2',
     'realpow', 'reallog', 'realsqrt', 'sqrt', 'nthroot', 'nextpow2', 'abs',
     'angle', 'complex', 'conj', 'imag', 'real', 'unwrap', 'isreal', 'cplxpair',
     'fix', 'floor', 'ceil', 'round', 'mod', 'rem', 'sign']
    specfun = ['airy', 'besselj', 'bessely', 'besselh', 'besseli', 'besselk', 'beta',
     'betainc', 'betaln', 'ellipj', 'ellipke', 'erf', 'erfc', 'erfcx',
     'erfinv', 'expint', 'gamma', 'gammainc', 'gammaln', 'psi', 'legendre',
     'cross', 'dot', 'factor', 'isprime', 'primes', 'gcd', 'lcm', 'rat',
     'rats', 'perms', 'nchoosek', 'factorial', 'cart2sph', 'cart2pol',
     'pol2cart', 'sph2cart', 'hsv2rgb', 'rgb2hsv']
    elmat = ['zeros', 'ones', 'eye', 'repmat', 'rand', 'randn', 'linspace', 'logspace',
     'freqspace', 'meshgrid', 'accumarray', 'size', 'length', 'ndims', 'numel',
     'disp', 'isempty', 'isequal', 'isequalwithequalnans', 'cat', 'reshape',
     'diag', 'blkdiag', 'tril', 'triu', 'fliplr', 'flipud', 'flipdim', 'rot90',
     'find', 'end', 'sub2ind', 'ind2sub', 'bsxfun', 'ndgrid', 'permute',
     'ipermute', 'shiftdim', 'circshift', 'squeeze', 'isscalar', 'isvector',
     'ans', 'eps', 'realmax', 'realmin', 'pi', 'i', 'inf', 'nan', 'isnan',
     'isinf', 'isfinite', 'j', 'why', 'compan', 'gallery', 'hadamard', 'hankel',
     'hilb', 'invhilb', 'magic', 'pascal', 'rosser', 'toeplitz', 'vander',
     'wilkinson']
    tokens = {'root': [
              (
               '^!.*', String.Other),
              (
               '%.*$', Comment),
              (
               '^\\s*function', Keyword, 'deffunc'),
              (
               '(break|case|catch|classdef|continue|else|elseif|end|enumerated|events|for|function|global|if|methods|otherwise|parfor|persistent|properties|return|spmd|switch|try|while)\\b',
               Keyword),
              (
               '(' + ('|').join(elfun + specfun + elmat) + ')\\b', Name.Builtin),
              (
               '-|==|~=|<|>|<=|>=|&&|&|~|\\|\\|?', Operator),
              (
               '\\.\\*|\\*|\\+|\\.\\^|\\.\\\\|\\.\\/|\\/|\\\\', Operator),
              (
               '\\[|\\]|\\(|\\)|\\{|\\}|:|@|\\.|,', Punctuation),
              (
               '=|:|;', Punctuation),
              (
               "(?<=[\\w\\)\\]])\\'", Operator),
              (
               "(?<![\\w\\)\\]])\\'", String, 'string'),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Name),
              (
               '.', Text)], 
       'string': [
                (
                 "[^\\']*\\'", String, '#pop')], 
       'deffunc': [
                 (
                  '(\\s*)(?:(.+)(\\s*)(=)(\\s*))?(.+)(\\()(.*)(\\))(\\s*)',
                  bygroups(Text.Whitespace, Text, Text.Whitespace, Punctuation, Text.Whitespace, Name.Function, Punctuation, Text, Punctuation, Text.Whitespace), '#pop')]}

    def analyse_text(text):
        if re.match('^\\s*%', text, re.M):
            return 0.9
        if re.match('^!\\w+', text, re.M):
            return 0.9
        return 0.1


line_re = re.compile('.*?\n')

class MatlabSessionLexer(Lexer):
    """
    For Matlab (or GNU Octave) sessions.  Modeled after PythonConsoleLexer.
    Contributed by Ken Schutte <kschutte@csail.mit.edu>.

    *New in Pygments 0.10.*
    """
    name = 'Matlab session'
    aliases = ['matlabsession']

    def get_tokens_unprocessed(self, text):
        mlexer = MatlabLexer(**self.options)
        curcode = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            if line.startswith('>>'):
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, line[:3])]))
                curcode += line[3:]
            elif line.startswith('???'):
                idx = len(curcode)
                line = '\n' + line
                token = (0, Generic.Traceback, line)
                insertions.append((idx, [token]))
            else:
                if curcode:
                    for item in do_insertions(insertions, mlexer.get_tokens_unprocessed(curcode)):
                        yield item

                    curcode = ''
                    insertions = []
                yield (match.start(), Generic.Output, line)

        if curcode:
            for item in do_insertions(insertions, mlexer.get_tokens_unprocessed(curcode)):
                yield item


class NumPyLexer(PythonLexer):
    """
    A Python lexer recognizing Numerical Python builtins.

    *New in Pygments 0.10.*
    """
    name = 'NumPy'
    aliases = ['numpy']
    mimetypes = []
    filenames = []
    EXTRA_KEYWORDS = set([
     'abs', 'absolute', 'accumulate', 'add', 'alen', 'all', 'allclose',
     'alltrue', 'alterdot', 'amax', 'amin', 'angle', 'any', 'append',
     'apply_along_axis', 'apply_over_axes', 'arange', 'arccos', 'arccosh',
     'arcsin', 'arcsinh', 'arctan', 'arctan2', 'arctanh', 'argmax', 'argmin',
     'argsort', 'argwhere', 'around', 'array', 'array2string', 'array_equal',
     'array_equiv', 'array_repr', 'array_split', 'array_str', 'arrayrange',
     'asanyarray', 'asarray', 'asarray_chkfinite', 'ascontiguousarray',
     'asfarray', 'asfortranarray', 'asmatrix', 'asscalar', 'astype',
     'atleast_1d', 'atleast_2d', 'atleast_3d', 'average', 'bartlett',
     'base_repr', 'beta', 'binary_repr', 'bincount', 'binomial',
     'bitwise_and', 'bitwise_not', 'bitwise_or', 'bitwise_xor', 'blackman',
     'bmat', 'broadcast', 'byte_bounds', 'bytes', 'byteswap', 'c_',
     'can_cast', 'ceil', 'choose', 'clip', 'column_stack', 'common_type',
     'compare_chararrays', 'compress', 'concatenate', 'conj', 'conjugate',
     'convolve', 'copy', 'corrcoef', 'correlate', 'cos', 'cosh', 'cov',
     'cross', 'cumprod', 'cumproduct', 'cumsum', 'delete', 'deprecate',
     'diag', 'diagflat', 'diagonal', 'diff', 'digitize', 'disp', 'divide',
     'dot', 'dsplit', 'dstack', 'dtype', 'dump', 'dumps', 'ediff1d', 'empty',
     'empty_like', 'equal', 'exp', 'expand_dims', 'expm1', 'extract', 'eye',
     'fabs', 'fastCopyAndTranspose', 'fft', 'fftfreq', 'fftshift', 'fill',
     'finfo', 'fix', 'flat', 'flatnonzero', 'flatten', 'fliplr', 'flipud',
     'floor', 'floor_divide', 'fmod', 'frexp', 'fromarrays', 'frombuffer',
     'fromfile', 'fromfunction', 'fromiter', 'frompyfunc', 'fromstring',
     'generic', 'get_array_wrap', 'get_include', 'get_numarray_include',
     'get_numpy_include', 'get_printoptions', 'getbuffer', 'getbufsize',
     'geterr', 'geterrcall', 'geterrobj', 'getfield', 'gradient', 'greater',
     'greater_equal', 'gumbel', 'hamming', 'hanning', 'histogram',
     'histogram2d', 'histogramdd', 'hsplit', 'hstack', 'hypot', 'i0',
     'identity', 'ifft', 'imag', 'index_exp', 'indices', 'inf', 'info',
     'inner', 'insert', 'int_asbuffer', 'interp', 'intersect1d',
     'intersect1d_nu', 'inv', 'invert', 'iscomplex', 'iscomplexobj',
     'isfinite', 'isfortran', 'isinf', 'isnan', 'isneginf', 'isposinf',
     'isreal', 'isrealobj', 'isscalar', 'issctype', 'issubclass_',
     'issubdtype', 'issubsctype', 'item', 'itemset', 'iterable', 'ix_',
     'kaiser', 'kron', 'ldexp', 'left_shift', 'less', 'less_equal', 'lexsort',
     'linspace', 'load', 'loads', 'loadtxt', 'log', 'log10', 'log1p', 'log2',
     'logical_and', 'logical_not', 'logical_or', 'logical_xor', 'logspace',
     'lstsq', 'mat', 'matrix', 'max', 'maximum', 'maximum_sctype',
     'may_share_memory', 'mean', 'median', 'meshgrid', 'mgrid', 'min',
     'minimum', 'mintypecode', 'mod', 'modf', 'msort', 'multiply', 'nan',
     'nan_to_num', 'nanargmax', 'nanargmin', 'nanmax', 'nanmin', 'nansum',
     'ndenumerate', 'ndim', 'ndindex', 'negative', 'newaxis', 'newbuffer',
     'newbyteorder', 'nonzero', 'not_equal', 'obj2sctype', 'ogrid', 'ones',
     'ones_like', 'outer', 'permutation', 'piecewise', 'pinv', 'pkgload',
     'place', 'poisson', 'poly', 'poly1d', 'polyadd', 'polyder', 'polydiv',
     'polyfit', 'polyint', 'polymul', 'polysub', 'polyval', 'power', 'prod',
     'product', 'ptp', 'put', 'putmask', 'r_', 'randint', 'random_integers',
     'random_sample', 'ranf', 'rank', 'ravel', 'real', 'real_if_close',
     'recarray', 'reciprocal', 'reduce', 'remainder', 'repeat', 'require',
     'reshape', 'resize', 'restoredot', 'right_shift', 'rint', 'roll',
     'rollaxis', 'roots', 'rot90', 'round', 'round_', 'row_stack', 's_',
     'sample', 'savetxt', 'sctype2char', 'searchsorted', 'seed', 'select',
     'set_numeric_ops', 'set_printoptions', 'set_string_function',
     'setbufsize', 'setdiff1d', 'seterr', 'seterrcall', 'seterrobj',
     'setfield', 'setflags', 'setmember1d', 'setxor1d', 'shape',
     'show_config', 'shuffle', 'sign', 'signbit', 'sin', 'sinc', 'sinh',
     'size', 'slice', 'solve', 'sometrue', 'sort', 'sort_complex', 'source',
     'split', 'sqrt', 'square', 'squeeze', 'standard_normal', 'std',
     'subtract', 'sum', 'svd', 'swapaxes', 'take', 'tan', 'tanh', 'tensordot',
     'test', 'tile', 'tofile', 'tolist', 'tostring', 'trace', 'transpose',
     'trapz', 'tri', 'tril', 'trim_zeros', 'triu', 'true_divide', 'typeDict',
     'typename', 'uniform', 'union1d', 'unique', 'unique1d', 'unravel_index',
     'unwrap', 'vander', 'var', 'vdot', 'vectorize', 'view', 'vonmises',
     'vsplit', 'vstack', 'weibull', 'where', 'who', 'zeros', 'zeros_like'])

    def get_tokens_unprocessed(self, text):
        for (index, token, value) in PythonLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield (
                 index, Keyword.Pseudo, value)
            else:
                yield (
                 index, token, value)


class RConsoleLexer(Lexer):
    """
    For R console transcripts or R CMD BATCH output files.
    """
    name = 'RConsole'
    aliases = ['rconsole', 'rout']
    filenames = ['*.Rout']

    def get_tokens_unprocessed(self, text):
        slexer = SLexer(**self.options)
        current_code_block = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            if line.startswith('>') or line.startswith('+'):
                insertions.append((len(current_code_block),
                 [
                  (
                   0, Generic.Prompt, line[:2])]))
                current_code_block += line[2:]
            else:
                if current_code_block:
                    for item in do_insertions(insertions, slexer.get_tokens_unprocessed(current_code_block)):
                        yield item

                    current_code_block = ''
                    insertions = []
                yield (match.start(), Generic.Output, line)

        if current_code_block:
            for item in do_insertions(insertions, slexer.get_tokens_unprocessed(current_code_block)):
                yield item


class SLexer(RegexLexer):
    """
    For S, S-plus, and R source code.

    *New in Pygments 0.10.*
    """
    name = 'S'
    aliases = ['splus', 's', 'r']
    filenames = ['*.S', '*.R']
    mimetypes = ['text/S-plus', 'text/S', 'text/R']
    tokens = {'comments': [
                  (
                   '#.*$', Comment.Single)], 
       'valid_name': [
                    (
                     '[a-zA-Z][0-9a-zA-Z\\._]+', Text),
                    (
                     '`.+`', String.Backtick)], 
       'punctuation': [
                     (
                      '\\[|\\]|\\[\\[|\\]\\]|\\$|\\(|\\)|@|:::?|;|,', Punctuation)], 
       'keywords': [
                  (
                   'for(?=\\s*\\()|while(?=\\s*\\()|if(?=\\s*\\()|(?<=\\s)else|(?<=\\s)break(?=;|$)|return(?=\\s*\\()|function(?=\\s*\\()',
                   Keyword.Reserved)], 
       'operators': [
                   (
                    '<-|-|==|<=|>=|<|>|&&|&|!=|\\|\\|?', Operator),
                   (
                    '\\*|\\+|\\^|/|%%|%/%|=', Operator),
                   (
                    '%in%|%*%', Operator)], 
       'builtin_symbols': [
                         (
                          '(NULL|NA|TRUE|FALSE|NaN)\\b', Keyword.Constant),
                         (
                          '(T|F)\\b', Keyword.Variable)], 
       'numbers': [
                 (
                  '(?<![0-9a-zA-Z\\)\\}\\]`\\"])(?=\\s*)[-\\+]?[0-9]+(\\.[0-9]*)?(E[0-9][-\\+]?(\\.[0-9]*)?)?',
                  Number),
                 (
                  '\\.[0-9]*(E[0-9][-\\+]?(\\.[0-9]*)?)?', Number)], 
       'statements': [
                    include('comments'),
                    (
                     '\\s+', Text),
                    (
                     "\\'", String, 'string_squote'),
                    (
                     '\\"', String, 'string_dquote'),
                    include('builtin_symbols'),
                    include('numbers'),
                    include('keywords'),
                    include('punctuation'),
                    include('operators'),
                    include('valid_name')], 
       'root': [
              include('statements'),
              (
               '\\{|\\}', Punctuation),
              (
               '.', Text)], 
       'string_squote': [
                       (
                        "[^\\']*\\'", String, '#pop')], 
       'string_dquote': [
                       (
                        '[^\\"]*\\"', String, '#pop')]}

    def analyse_text(text):
        return '<-' in text