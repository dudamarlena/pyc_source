# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\templ\teval.py
# Compiled at: 2013-07-26 11:14:51
"""
Copyright 2013 Brian Mearns

This file is part of templ.

templ is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

templ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with templ.  If not, see <http://www.gnu.org/licenses/>.

******************************************************************************

Functions and types of evaluating expressions.

Expressions, including lists, are *evaluated*. Symbols are self-evaluating. Empty lists eval to NULL.
For non empty lists, the first element is *resolved* to an executable. Executables are self-resolving,
Strings are resolved by looking them up in the stack. Finally, the resolved tag is *executed*.
"""
import ttypes, texec, tstreams, texceptions

def resolveExecutable(val, stack):
    """
    Given a TType value, gets an Executable object it represents, for intance, if the first
    value in a list-expression evaluated to the given val, what Executable would it be?
    Returns (name, exe).
    """
    if isinstance(val, ttypes.String):
        exe = stack.lookup(val)
        if exe is None:
            raise texceptions.NoSuchSymbolException(str(val), val.filepos)
        elif not isinstance(exe, texec.Executable):
            raise texceptions.TemplateTypeException('Invalid tag "%s".' % val, val.filepos, texec.Executable, exe)
        else:
            exe.filepos = val.filepos
            return (val, exe)
    else:
        if isinstance(val, texec.Executable):
            return (str(val), val)
        raise texceptions.TemplateTypeException('Invalid tag "%s". Must be a String or Executable.' % val, val.filepos, got=val)
    return


def evalExpression--- This code section failed: ---

 L.  58         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             1  'ostream'
                6  LOAD_GLOBAL           1  'tstreams'
                9  LOAD_ATTR             2  'TemplateOutputStream'
               12  CALL_FUNCTION_2       2  None
               15  POP_JUMP_IF_TRUE     43  'to 43'

 L.  59        18  LOAD_GLOBAL           3  'TypeError'
               21  LOAD_CONST               'Invalid output stream in use: must use a TemplateOutputStream, not a %s'
               24  LOAD_GLOBAL           4  'type'
               27  LOAD_FAST             1  'ostream'
               30  CALL_FUNCTION_1       1  None
               33  BINARY_MODULO    
               34  CALL_FUNCTION_1       1  None
               37  RAISE_VARARGS_1       1  None
               40  JUMP_FORWARD          0  'to 43'
             43_0  COME_FROM            40  '40'

 L.  62        43  LOAD_GLOBAL           0  'isinstance'
               46  LOAD_FAST             0  'expr'
               49  LOAD_GLOBAL           5  'ttypes'
               52  LOAD_ATTR             6  'String'
               55  CALL_FUNCTION_2       2  None
               58  POP_JUMP_IF_FALSE    65  'to 65'

 L.  63        61  LOAD_FAST             0  'expr'
               64  RETURN_END_IF    
             65_0  COME_FROM            58  '58'

 L.  66        65  LOAD_GLOBAL           0  'isinstance'
               68  LOAD_FAST             0  'expr'
               71  LOAD_GLOBAL           5  'ttypes'
               74  LOAD_ATTR             7  'List'
               77  CALL_FUNCTION_2       2  None
               80  POP_JUMP_IF_FALSE   307  'to 307'

 L.  68        83  LOAD_GLOBAL           8  'len'
               86  LOAD_FAST             0  'expr'
               89  CALL_FUNCTION_1       1  None
               92  LOAD_CONST               0
               95  COMPARE_OP            2  ==
               98  POP_JUMP_IF_FALSE   123  'to 123'

 L.  69       101  LOAD_GLOBAL           5  'ttypes'
              104  LOAD_ATTR             6  'String'
              107  LOAD_CONST               ''
              110  LOAD_CONST               'filepos'
              113  LOAD_FAST             0  'expr'
              116  LOAD_ATTR             9  'filepos'
              119  CALL_FUNCTION_257   257  None
              122  RETURN_END_IF    
            123_0  COME_FROM            98  '98'

 L.  71       123  LOAD_GLOBAL          10  'evalExpression'
              126  LOAD_FAST             0  'expr'
              129  LOAD_CONST               0
              132  BINARY_SUBSCR    
              133  LOAD_FAST             1  'ostream'
              136  LOAD_FAST             2  'stack'
              139  CALL_FUNCTION_3       3  None
              142  STORE_FAST            3  'name'

 L.  72       145  LOAD_GLOBAL          11  'resolveExecutable'
              148  LOAD_FAST             3  'name'
              151  LOAD_FAST             2  'stack'
              154  CALL_FUNCTION_2       2  None
              157  UNPACK_SEQUENCE_2     2 
              160  STORE_FAST            3  'name'
              163  STORE_FAST            4  'exe'

 L.  74       166  LOAD_FAST             0  'expr'
              169  LOAD_ATTR             9  'filepos'
              172  LOAD_CONST               None
              175  COMPARE_OP            9  is-not
              178  POP_JUMP_IF_TRUE    187  'to 187'
              181  LOAD_ASSERT              AssertionError
              184  RAISE_VARARGS_1       1  None

 L.  75       187  LOAD_GLOBAL           8  'len'
              190  LOAD_FAST             0  'expr'
              193  CALL_FUNCTION_1       1  None
              196  LOAD_CONST               1
              199  COMPARE_OP            2  ==
              202  POP_JUMP_IF_TRUE    230  'to 230'
              205  LOAD_FAST             0  'expr'
              208  LOAD_CONST               1
              211  BINARY_SUBSCR    
              212  LOAD_ATTR             9  'filepos'
              215  LOAD_CONST               None
              218  COMPARE_OP            9  is-not
              221  POP_JUMP_IF_TRUE    230  'to 230'
              224  LOAD_ASSERT              AssertionError
              227  RAISE_VARARGS_1       1  None

 L.  76       230  LOAD_FAST             0  'expr'
              233  LOAD_ATTR             9  'filepos'
              236  LOAD_FAST             4  'exe'
              239  STORE_ATTR            9  'filepos'

 L.  77       242  LOAD_GLOBAL          14  'callExecutable'
              245  LOAD_FAST             3  'name'
              248  LOAD_FAST             4  'exe'
              251  LOAD_FAST             0  'expr'
              254  LOAD_CONST               1
              257  SLICE+1          
              258  LOAD_FAST             1  'ostream'
              261  LOAD_FAST             2  'stack'
              264  CALL_FUNCTION_5       5  None
              267  STORE_FAST            5  'res'

 L.  78       270  LOAD_GLOBAL           0  'isinstance'
              273  LOAD_FAST             5  'res'
              276  LOAD_GLOBAL           5  'ttypes'
              279  LOAD_ATTR            15  'TType'
              282  CALL_FUNCTION_2       2  None
              285  POP_JUMP_IF_TRUE    303  'to 303'
              288  LOAD_ASSERT              AssertionError
              291  LOAD_GLOBAL          16  'repr'
              294  LOAD_FAST             5  'res'
              297  CALL_FUNCTION_1       1  None
              300  RAISE_VARARGS_2       2  None

 L.  79       303  LOAD_FAST             5  'res'
              306  RETURN_END_IF    
            307_0  COME_FROM            80  '80'

 L.  81       307  LOAD_GLOBAL           0  'isinstance'
              310  LOAD_FAST             0  'expr'
              313  LOAD_GLOBAL          17  'texec'
              316  LOAD_ATTR            18  'Executable'
              319  CALL_FUNCTION_2       2  None
              322  POP_JUMP_IF_FALSE   349  'to 349'

 L.  83       325  LOAD_GLOBAL          19  'texceptions'
              328  LOAD_ATTR            20  'InternalError'
              331  LOAD_CONST               'Sorry, not implemented yet.'
              334  LOAD_FAST             0  'expr'
              337  LOAD_ATTR             9  'filepos'
              340  CALL_FUNCTION_2       2  None
              343  RAISE_VARARGS_1       1  None
              346  JUMP_FORWARD         64  'to 413'

 L.  86       349  LOAD_GLOBAL           0  'isinstance'
              352  LOAD_FAST             0  'expr'
              355  LOAD_GLOBAL           5  'ttypes'
              358  LOAD_ATTR            15  'TType'
              361  CALL_FUNCTION_2       2  None
              364  POP_JUMP_IF_FALSE   379  'to 379'

 L.  87       367  LOAD_FAST             0  'expr'
              370  LOAD_ATTR             9  'filepos'
              373  STORE_FAST            6  'fp'
              376  JUMP_FORWARD          6  'to 385'

 L.  89       379  LOAD_CONST               None
              382  STORE_FAST            6  'fp'
            385_0  COME_FROM           376  '376'

 L.  90       385  LOAD_GLOBAL          19  'texceptions'
              388  LOAD_ATTR            21  'TemplateTypeException'

 L.  91       391  LOAD_CONST               'Invalid expression for evaluation: %r. Must be a String, List, or Executable.'
              394  LOAD_FAST             0  'expr'
              397  BINARY_MODULO    

 L.  92       398  LOAD_FAST             6  'fp'
              401  LOAD_CONST               'got'
              404  LOAD_FAST             0  'expr'
              407  CALL_FUNCTION_258   258  None
              410  RAISE_VARARGS_1       1  None
            413_0  COME_FROM           346  '346'
              413  LOAD_CONST               None
              416  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 413


def callExecutable(name, exe, args, ostream, stack):
    stackDepth = stack.depth()
    if isinstance(exe, texec.TOperator):
        res = exe(str(name), args, ostream, stack)
    elif isinstance(exe, texec.TFunction):
        xargs = []
        for e in args:
            arg = evalExpression(e, ostream, stack)
            assert isinstance(arg, ttypes.TType)
            xargs.append(arg)

        xargs = ttypes.List(xargs)
        res = exe(str(name), xargs, ostream, stack)
    elif isinstance(exe, texec.TMacro):
        subst = exe(str(name), ttypes.List(args), ostream, stack)
        assert isinstance(subst, ttypes.TType)
        subst.fillInFilepos(exe.filepos)
        try:
            res = evalExpression(subst, ostream, stack)
        except texceptions.TemplateException as e:
            if stack.depth() != stackDepth:
                raise texceptions.InternalError('Macro did not restore stack: "%s".' % name, exe.filepos)
            raise texceptions.TemplateMacroError(e, exe.filepos, name)

    else:
        raise texceptions.InternalError('Unhandled Executable class %s' % type(exe), exe.filepos)
    if stack.depth() != stackDepth:
        raise texec.InternalError('Executable did not restore stack (%d, %d): "%s".' % (stackDepth, stack.depth(), name), exe.filepos)
    return res