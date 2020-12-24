# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\templ\texec.py
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

Base classes and utility functions for native executable objects: functions, macros, and operators
implemented in the evaluator, as oppose to user defined executable implemented in templ.

To define native executables, subclass one of `TOperator`, `TFunction`, or `TMacro`, apply the
appropriate decorator (`operator`, `function`, or `macro`) and imlement the functionality in 
the `execute` method. You also need to define the `__mnemonics__` class attribute to define the
canonical name (first element) and any aliases for the executable.
"""
import teval, ttypes, filepos as tFilepos, texceptions, stack as tStack, abc, collections, math, os

class ExeMeta(ttypes.MetaTType):
    """
    Quick summary of meta classes: Basically, they're just class factories. The class/type object
    itself will be an instance of this class if you put `__metaclass__ = MetaTType` in the class
    definition. That means the class object itself will have all of the functions defined in this
    class.
    """

    def __str__(cls):
        """
        Used for coercing instances of this Metaclass to a string. So for instance, if you
        have an instance object and you get it's type, and then print that type, it will
        use this to convert that type to a string.
        """
        return 'T_%s' % cls.__name__

    def __init__(cls, name, bases, dct):
        """
        This is called when the Class is created, so like when you use the class keyword 
        to define a class with this metaclass. We use it to replace the class's execute function
        with one that makes sure the result is a TType and has the filepos set.
        
        If your execute function returns None (or doesn't return anything), this returns a new Null
        object. It also asserts that the returned value is a TType instance.

        Finally, it replaces the filpos attribute of the returned value to the filepos of the
        executable object instance, unless the class has a __keep_filepos__ attribute and its
        set to True, in which case it leaves the returned value's filepos alone, and it's your
        responsibility to make sure it's set correctly.
        """
        super(ttypes.MetaTType, cls).__init__(name, bases, dct)
        orig_exe = getattr(cls, 'execute')

        def execute(self, name, args, ostream, stack):
            res = orig_exe(self, name, args, ostream, stack)
            if res is None:
                res = ttypes.Null(self.filepos)
            assert isinstance(res, ttypes.TType)
            if not hasattr(cls, '__keep_filepos__') or not getattr(cls, '__keep_filepos__'):
                res.filepos = self.filepos
            return res

        setattr(cls, 'execute', execute)


class Executable(ttypes.TType):
    """
    The base class for any executable object that can be used as the tag for a list expression.

    Don't subclass this directly, use one of the Function, Macro, or Operator types.

    This class has some useful utility functions that will be commonly used by executables.
    """
    __metaclass__ = ExeMeta

    def __init__(self):
        self.__aliases = tuple()
        self.__name = None
        return

    def __str__(self):
        return '<Exe:%s>' % type(self).__name__

    @classmethod
    def make_acceptable(cls, other, filepos=None):
        if isinstance(other, Executable):
            return other
        raise TypeError("Cannot make type '%s' acceptable for %s." % (type(other).__name__, cls))

    @property
    def doc(self):
        return type(self).__doc__

    @property
    def aliases(self):
        return self.__aliases

    def setAliases(self, aliases):
        self.__aliases = tuple(aliases)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __call__(self, *args, **kwargs):
        assert self.filepos is not None
        return self.execute(*args, **kwargs)

    def raw(self):
        return

    @abc.abstractmethod
    def execute(self, name, args, ostream, stack):
        pass

    __ordinals__ = ('first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh',
                    'eigth', 'ninth', 'tenth', 'eleventh', 'twelth')

    @classmethod
    def ordinal(cls, index):
        """
        Convert the number `index` into a string giving its ordinal in a pretty form.
        Ordinals are ranks, like "first", "second", "third", etc.
        """
        if index == 0:
            return '0th'
        else:
            if index > len(cls.__ordinals__):
                ones = index % 10
                if ones == 1:
                    suffix = 'st'
                elif ones == 2:
                    suffix = 'nd'
                elif ones == 3:
                    suffix = 'rd'
                else:
                    suffix = 'th'
                return str(index) + suffix
            return cls.__ordinals__[(index - 1)]

    def checkArgType(self, name, argc, args, cls):
        """
        Checks the type of a specific argument.
        
        Raises an appropriate exception if it's not the right type, otherwise just returns (None).

        Returns the argument value for convenience.

        Arguments:
            - `name` is the name with which it was invoked, as passed into the `execute` method.
            - `argc` is the index into the args list of the arg to check.
            - `args` is the array of arguments.
            - `cls` is the exected type.

        """
        argname = self.ordinal(argc + 1)
        return self.checkType('%s argument for "%s"' % (argname, name), args[argc], cls)

    def checkType(self, description, value, cls):
        """
        Checks the type of a value.
        
        Raises an appropriate exception if it's not the righ type, otherwise just returns (None).

        Returns `value` for convenience.

        Arguments:
            - `description` is a description of the value being checked. For instance "third element of second argument".
            - `value` is the value whose type is to be checked.
            - `cls` is the exected type.
        """
        if not isinstance(value, cls):
            filepos = value.filepos
            if filepos is None:
                filepos = tFilepos.NearFilepos.wrap(self.filepos)
            raise texceptions.TemplateTypeException('Incorrect type for %s.' % description, filepos, cls, value)
        return value

    def checkArgCount(self, name, args, exact=None, min=None, max=None):
        """
        Checks the number of arguments passed to the executable.

        You can specify the expected number of arguments either as a list of exact values, or
        as a max and/or minimum number. You can't supply both exact and a min/max. If the given
        number of arguments doesn't match, raise an appropriate exception, otherwise returns (None).

        Arguments:
            -   `name` is the name with which it was invoked, as passed into the `execute` method.
            -   `args` is the array of arguments.
            -   `exact` is an optional argument, a sequence of numbers, each number being a possible exact number of arguments
                that is acceptable.
            -   `min` is optional, it specifes the minimum number of acceptable args when specfying
                the allowed number of args as a min/max range.
            -   `max` is optional, it specifes the maximum number of acceptable args when specfying
                the allowed number of args as a min/max range.
        """
        count = len(args)
        if exact is not None:
            if min is not None or max is not None:
                raise Exception('Conflicting arguments.')
            elif not isinstance(exact, collections.Sequence):
                raise TypeError("Invalid type for 'exact'.")
            elif len(exact) == 0:
                raise ValueError("Invalid value for 'exact': require at least one value.")
            elif count not in exact:
                raise texceptions.WrongNumberArgsException('Incorrect number of arguments for "%s".' % name, self.filepos, got=count, exact=exact)
        elif min is None and max is None:
            raise Exception('Insufficient arguments.')
        elif min is not None and count < min:
            raise texceptions.WrongNumberArgsException('Insufficient number of arguments for "%s".' % name, self.filepos, got=count, min=min, max=max)
        elif max is not None and count > max:
            raise texceptions.WrongNumberArgsException('Too many arguments for "%s".' % name, self.filepos, got=count, min=min, max=max)
        return count


class TOperator(Executable):
    """
    The parent class for all Operator type executables.

    To create a new "native" operator, subclass this class and implement
    the `execute` method. Remember that for operators, the arguments are
    just raw expressions (LISTs and SYMBOLs), they are not evaluated before
    being passed it. Unlike Macros, you return the actual result value, not
    an expression to be further evaluated.
    """

    def __str__(self):
        return '<Oper:%s>' % type(self).__name__


class TFunction(Executable):
    """
    The parent class for all Function type executables.

    To create a new "native" function, subclass this class and implement
    the `execute` method. Remember that for functions, the arguments are
    all evaluated before they are passed in.
    """

    def __str__(self):
        return '<Func:%s>' % type(self).__name__


class TMacro(Executable):
    """
    The parent class for all Macro type executables.

    To create a new "native" macro, subclass this class and implement
    the `execute` method. Remember that for macros, the arguments are
    just raw expressions (LISTs and SYMBOLs), they are not evaluated before
    being passed it. Macros should then return an expression which the evaluator
    will then evaluate on its own.
    """

    def __str__(self):
        return '<Macro:%s>' % type(self).__name__


class UserFunc(TFunction):
    """
    The type for user defined functions.

    Don't override this to define new functions, just instantiate it.
    """

    def __init__--- This code section failed: ---

 L. 327         0  LOAD_GLOBAL           0  'super'
                3  LOAD_GLOBAL           1  'UserFunc'
                6  LOAD_FAST             0  'self'
                9  CALL_FUNCTION_2       2  None
               12  LOAD_ATTR             2  '__init__'
               15  CALL_FUNCTION_0       0  None
               18  POP_TOP          

 L. 328        19  LOAD_GLOBAL           3  'isinstance'
               22  LOAD_FAST             1  'filepos'
               25  LOAD_GLOBAL           4  'tFilepos'
               28  LOAD_ATTR             5  'Filepos'
               31  CALL_FUNCTION_2       2  None
               34  POP_JUMP_IF_TRUE     52  'to 52'
               37  LOAD_ASSERT              AssertionError
               40  LOAD_GLOBAL           7  'repr'
               43  LOAD_FAST             1  'filepos'
               46  CALL_FUNCTION_1       1  None
               49  RAISE_VARARGS_2       2  None

 L. 329        52  LOAD_GLOBAL           3  'isinstance'
               55  LOAD_FAST             2  'expr'
               58  LOAD_GLOBAL           8  'ttypes'
               61  LOAD_ATTR             9  'TType'
               64  CALL_FUNCTION_2       2  None
               67  POP_JUMP_IF_TRUE     76  'to 76'
               70  LOAD_ASSERT              AssertionError
               73  RAISE_VARARGS_1       1  None

 L. 330        76  LOAD_FAST             1  'filepos'
               79  LOAD_FAST             0  'self'
               82  STORE_ATTR           10  'definedAtFilepos'

 L. 331        85  LOAD_FAST             2  'expr'
               88  LOAD_FAST             0  'self'
               91  STORE_ATTR           11  '__expr'

 L. 333        94  LOAD_FAST             3  'argnames'
               97  LOAD_CONST               None
              100  COMPARE_OP            8  is
              103  POP_JUMP_IF_FALSE   121  'to 121'

 L. 334       106  LOAD_GLOBAL           8  'ttypes'
              109  LOAD_ATTR            13  'List'
              112  CALL_FUNCTION_0       0  None
              115  STORE_FAST            3  'argnames'
              118  JUMP_FORWARD          0  'to 121'
            121_0  COME_FROM           118  '118'

 L. 335       121  LOAD_GLOBAL           3  'isinstance'
              124  LOAD_FAST             3  'argnames'
              127  LOAD_GLOBAL           8  'ttypes'
              130  LOAD_ATTR            13  'List'
              133  CALL_FUNCTION_2       2  None
              136  POP_JUMP_IF_TRUE    145  'to 145'
              139  LOAD_ASSERT              AssertionError
              142  RAISE_VARARGS_1       1  None

 L. 336       145  LOAD_GLOBAL          14  'all'
              148  LOAD_GENEXPR             '<code_object <genexpr>>'
              151  MAKE_FUNCTION_0       0  None
              154  LOAD_FAST             3  'argnames'
              157  GET_ITER         
              158  CALL_FUNCTION_1       1  None
              161  CALL_FUNCTION_1       1  None
              164  POP_JUMP_IF_TRUE    173  'to 173'
              167  LOAD_ASSERT              AssertionError
              170  RAISE_VARARGS_1       1  None

 L. 337       173  LOAD_FAST             3  'argnames'
              176  LOAD_FAST             0  'self'
              179  STORE_ATTR           15  '__argnames'

 L. 339       182  LOAD_FAST             4  'doc'
              185  LOAD_CONST               None
              188  COMPARE_OP            8  is
              191  POP_JUMP_IF_FALSE   209  'to 209'

 L. 340       194  LOAD_GLOBAL           8  'ttypes'
              197  LOAD_ATTR            16  'String'
              200  CALL_FUNCTION_0       0  None
              203  STORE_FAST            4  'doc'
              206  JUMP_FORWARD          0  'to 209'
            209_0  COME_FROM           206  '206'

 L. 341       209  LOAD_GLOBAL           3  'isinstance'
              212  LOAD_FAST             4  'doc'
              215  LOAD_GLOBAL           8  'ttypes'
              218  LOAD_ATTR            16  'String'
              221  CALL_FUNCTION_2       2  None
              224  POP_JUMP_IF_TRUE    233  'to 233'
              227  LOAD_ASSERT              AssertionError
              230  RAISE_VARARGS_1       1  None

 L. 342       233  LOAD_FAST             4  'doc'
              236  LOAD_FAST             0  'self'
              239  STORE_ATTR           17  '__doc'
              242  LOAD_CONST               None
              245  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 242

    @property
    def doc(self):
        return self.__doc

    def __str__(self):
        return '<UFunc:%s>' % type(self).__name__

    def execute(self, name, args, ostream, stack):
        assert isinstance(args, ttypes.List)
        stack.push()
        stack.new(':argv', args)
        argc = len(args)
        namedc = len(self.__argnames)
        for i in xrange(argc):
            if i >= namedc:
                break
            else:
                stack.new(self.__argnames[i], args[i])

        try:
            res = teval.evalExpression(self.__expr, ostream, stack)
        except texceptions.TemplateException as e:
            stack.pop()
            raise texceptions.TemplateUserExecError(e, self.filepos, name, self.definedAtFilepos)
        except:
            stack.pop()
            raise

        stack.pop()
        return res


class UserMacro(TMacro):
    """
    The type for user defined macros.

    Don't override this to define new macros, just instantiate it.
    """

    def __init__--- This code section failed: ---

 L. 393         0  LOAD_GLOBAL           0  'super'
                3  LOAD_GLOBAL           1  'UserMacro'
                6  LOAD_FAST             0  'self'
                9  CALL_FUNCTION_2       2  None
               12  LOAD_ATTR             2  '__init__'
               15  CALL_FUNCTION_0       0  None
               18  POP_TOP          

 L. 394        19  LOAD_GLOBAL           3  'isinstance'
               22  LOAD_FAST             1  'filepos'
               25  LOAD_GLOBAL           4  'tFilepos'
               28  LOAD_ATTR             5  'Filepos'
               31  CALL_FUNCTION_2       2  None
               34  POP_JUMP_IF_TRUE     52  'to 52'
               37  LOAD_ASSERT              AssertionError
               40  LOAD_GLOBAL           7  'repr'
               43  LOAD_FAST             1  'filepos'
               46  CALL_FUNCTION_1       1  None
               49  RAISE_VARARGS_2       2  None

 L. 395        52  LOAD_GLOBAL           3  'isinstance'
               55  LOAD_FAST             2  'expr'
               58  LOAD_GLOBAL           8  'ttypes'
               61  LOAD_ATTR             9  'TType'
               64  CALL_FUNCTION_2       2  None
               67  POP_JUMP_IF_TRUE     76  'to 76'
               70  LOAD_ASSERT              AssertionError
               73  RAISE_VARARGS_1       1  None

 L. 396        76  LOAD_FAST             1  'filepos'
               79  LOAD_FAST             0  'self'
               82  STORE_ATTR           10  'definedAtFilepos'

 L. 397        85  LOAD_FAST             2  'expr'
               88  LOAD_FAST             0  'self'
               91  STORE_ATTR           11  '__expr'

 L. 399        94  LOAD_FAST             3  'argnames'
               97  LOAD_CONST               None
              100  COMPARE_OP            8  is
              103  POP_JUMP_IF_FALSE   121  'to 121'

 L. 400       106  LOAD_GLOBAL           8  'ttypes'
              109  LOAD_ATTR            13  'List'
              112  CALL_FUNCTION_0       0  None
              115  STORE_FAST            3  'argnames'
              118  JUMP_FORWARD          0  'to 121'
            121_0  COME_FROM           118  '118'

 L. 401       121  LOAD_GLOBAL           3  'isinstance'
              124  LOAD_FAST             3  'argnames'
              127  LOAD_GLOBAL           8  'ttypes'
              130  LOAD_ATTR            13  'List'
              133  CALL_FUNCTION_2       2  None
              136  POP_JUMP_IF_TRUE    145  'to 145'
              139  LOAD_ASSERT              AssertionError
              142  RAISE_VARARGS_1       1  None

 L. 402       145  LOAD_GLOBAL          14  'all'
              148  LOAD_GENEXPR             '<code_object <genexpr>>'
              151  MAKE_FUNCTION_0       0  None
              154  LOAD_FAST             3  'argnames'
              157  GET_ITER         
              158  CALL_FUNCTION_1       1  None
              161  CALL_FUNCTION_1       1  None
              164  POP_JUMP_IF_TRUE    173  'to 173'
              167  LOAD_ASSERT              AssertionError
              170  RAISE_VARARGS_1       1  None

 L. 403       173  LOAD_FAST             3  'argnames'
              176  LOAD_FAST             0  'self'
              179  STORE_ATTR           15  '__argnames'

 L. 405       182  LOAD_FAST             4  'doc'
              185  LOAD_CONST               None
              188  COMPARE_OP            8  is
              191  POP_JUMP_IF_FALSE   209  'to 209'

 L. 406       194  LOAD_GLOBAL           8  'ttypes'
              197  LOAD_ATTR            16  'String'
              200  CALL_FUNCTION_0       0  None
              203  STORE_FAST            4  'doc'
              206  JUMP_FORWARD          0  'to 209'
            209_0  COME_FROM           206  '206'

 L. 407       209  LOAD_GLOBAL           3  'isinstance'
              212  LOAD_FAST             4  'doc'
              215  LOAD_GLOBAL           8  'ttypes'
              218  LOAD_ATTR            16  'String'
              221  CALL_FUNCTION_2       2  None
              224  POP_JUMP_IF_TRUE    233  'to 233'
              227  LOAD_ASSERT              AssertionError
              230  RAISE_VARARGS_1       1  None

 L. 408       233  LOAD_FAST             4  'doc'
              236  LOAD_FAST             0  'self'
              239  STORE_ATTR           17  '__doc'
              242  LOAD_CONST               None
              245  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 242

    @property
    def doc(self):
        return self.__doc

    def __str__(self):
        return '<UMacro:%s>' % type(self).__name__

    def execute--- This code section failed: ---

 L. 418         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             2  'args'
                6  LOAD_GLOBAL           1  'ttypes'
                9  LOAD_ATTR             2  'List'
               12  CALL_FUNCTION_2       2  None
               15  POP_JUMP_IF_TRUE     33  'to 33'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_GLOBAL           4  'repr'
               24  LOAD_FAST             2  'args'
               27  CALL_FUNCTION_1       1  None
               30  RAISE_VARARGS_2       2  None

 L. 419        33  LOAD_FAST             4  'stack'
               36  LOAD_ATTR             5  'push'
               39  CALL_FUNCTION_0       0  None
               42  POP_TOP          

 L. 420        43  LOAD_FAST             4  'stack'
               46  LOAD_ATTR             6  'new'
               49  LOAD_CONST               ':argv'
               52  LOAD_FAST             2  'args'
               55  CALL_FUNCTION_2       2  None
               58  POP_TOP          

 L. 422        59  LOAD_GLOBAL           7  'len'
               62  LOAD_FAST             2  'args'
               65  CALL_FUNCTION_1       1  None
               68  STORE_FAST            5  'argc'

 L. 423        71  LOAD_GLOBAL           7  'len'
               74  LOAD_FAST             0  'self'
               77  LOAD_ATTR             8  '__argnames'
               80  CALL_FUNCTION_1       1  None
               83  STORE_FAST            6  'namedc'

 L. 424        86  SETUP_LOOP           63  'to 152'
               89  LOAD_GLOBAL           9  'xrange'
               92  LOAD_FAST             5  'argc'
               95  CALL_FUNCTION_1       1  None
               98  GET_ITER         
               99  FOR_ITER             49  'to 151'
              102  STORE_FAST            7  'i'

 L. 425       105  LOAD_FAST             7  'i'
              108  LOAD_FAST             6  'namedc'
              111  COMPARE_OP            5  >=
              114  POP_JUMP_IF_FALSE   121  'to 121'

 L. 426       117  BREAK_LOOP       
              118  JUMP_BACK            99  'to 99'

 L. 428       121  LOAD_FAST             4  'stack'
              124  LOAD_ATTR             6  'new'
              127  LOAD_FAST             0  'self'
              130  LOAD_ATTR             8  '__argnames'
              133  LOAD_FAST             7  'i'
              136  BINARY_SUBSCR    
              137  LOAD_FAST             2  'args'
              140  LOAD_FAST             7  'i'
              143  BINARY_SUBSCR    
              144  CALL_FUNCTION_2       2  None
              147  POP_TOP          
              148  JUMP_BACK            99  'to 99'
              151  POP_BLOCK        
            152_0  COME_FROM            86  '86'

 L. 430       152  SETUP_EXCEPT         28  'to 183'

 L. 431       155  LOAD_GLOBAL          10  'teval'
              158  LOAD_ATTR            11  'evalExpression'
              161  LOAD_FAST             0  'self'
              164  LOAD_ATTR            12  '__expr'
              167  LOAD_FAST             3  'ostream'
              170  LOAD_FAST             4  'stack'
              173  CALL_FUNCTION_3       3  None
              176  STORE_FAST            8  'res'
              179  POP_BLOCK        
              180  JUMP_FORWARD         81  'to 264'
            183_0  COME_FROM           152  '152'

 L. 432       183  DUP_TOP          
              184  LOAD_GLOBAL          13  'texceptions'
              187  LOAD_ATTR            14  'TemplateException'
              190  COMPARE_OP           10  exception-match
              193  POP_JUMP_IF_FALSE   244  'to 244'
              196  POP_TOP          
              197  STORE_FAST            9  'e'
              200  POP_TOP          

 L. 433       201  LOAD_FAST             4  'stack'
              204  LOAD_ATTR            15  'pop'
              207  CALL_FUNCTION_0       0  None
              210  POP_TOP          

 L. 434       211  LOAD_GLOBAL          13  'texceptions'
              214  LOAD_ATTR            16  'TemplateUserExecError'
              217  LOAD_FAST             9  'e'
              220  LOAD_FAST             0  'self'
              223  LOAD_ATTR            17  'filepos'
              226  LOAD_FAST             1  'name'
              229  LOAD_FAST             0  'self'
              232  LOAD_ATTR            18  'definedAtFilepos'
              235  CALL_FUNCTION_4       4  None
              238  RAISE_VARARGS_1       1  None
              241  JUMP_FORWARD         20  'to 264'

 L. 435       244  POP_TOP          
              245  POP_TOP          
              246  POP_TOP          

 L. 436       247  LOAD_FAST             4  'stack'
              250  LOAD_ATTR            15  'pop'
              253  CALL_FUNCTION_0       0  None
              256  POP_TOP          

 L. 437       257  RAISE_VARARGS_0       0  None
              260  JUMP_FORWARD          1  'to 264'
              263  END_FINALLY      
            264_0  COME_FROM           263  '263'
            264_1  COME_FROM           180  '180'

 L. 439       264  LOAD_FAST             4  'stack'
              267  LOAD_ATTR            15  'pop'
              270  CALL_FUNCTION_0       0  None
              273  POP_TOP          

 L. 440       274  LOAD_FAST             8  'res'
              277  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 277


class MathExec(Executable):
    """
    A helper mixin class for functions that have to parse numbers from strings.
    """

    def parseNumericArgs(self, name, args):
        """
        Like <parseNumericArg>, but parses a sequence of arguments, and returns a corresponding sequence of numeric values.
        """
        return tuple(self.parseNumericArg(name, i, args) for i in xrange(len(args)))

    def parseNumericArg--- This code section failed: ---

 L. 461         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             3  'args'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_FAST             2  'argc'
               12  COMPARE_OP            4  >
               15  POP_JUMP_IF_TRUE     43  'to 43'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               '%d > %d'
               24  LOAD_GLOBAL           0  'len'
               27  LOAD_FAST             3  'args'
               30  CALL_FUNCTION_1       1  None
               33  LOAD_FAST             2  'argc'
               36  BUILD_TUPLE_2         2 
               39  BINARY_MODULO    
               40  RAISE_VARARGS_2       2  None

 L. 463        43  LOAD_FAST             0  'self'
               46  LOAD_ATTR             2  'checkArgType'
               49  LOAD_FAST             1  'name'
               52  LOAD_FAST             2  'argc'
               55  LOAD_FAST             3  'args'
               58  LOAD_GLOBAL           3  'ttypes'
               61  LOAD_ATTR             4  'String'
               64  CALL_FUNCTION_4       4  None
               67  POP_TOP          

 L. 464        68  LOAD_FAST             3  'args'
               71  LOAD_FAST             2  'argc'
               74  BINARY_SUBSCR    
               75  STORE_FAST            4  'arg'

 L. 465        78  SETUP_EXCEPT         16  'to 97'

 L. 466        81  LOAD_GLOBAL           5  'int'
               84  LOAD_FAST             4  'arg'
               87  CALL_FUNCTION_1       1  None
               90  STORE_FAST            5  'v'
               93  POP_BLOCK        
               94  JUMP_FORWARD        100  'to 197'
             97_0  COME_FROM            78  '78'

 L. 467        97  DUP_TOP          
               98  LOAD_GLOBAL           6  'Exception'
              101  COMPARE_OP           10  exception-match
              104  POP_JUMP_IF_FALSE   196  'to 196'
              107  POP_TOP          
              108  POP_TOP          
              109  POP_TOP          

 L. 468       110  SETUP_EXCEPT         16  'to 129'

 L. 469       113  LOAD_GLOBAL           7  'float'
              116  LOAD_FAST             4  'arg'
              119  CALL_FUNCTION_1       1  None
              122  STORE_FAST            5  'v'
              125  POP_BLOCK        
              126  JUMP_ABSOLUTE       197  'to 197'
            129_0  COME_FROM           110  '110'

 L. 470       129  DUP_TOP          
              130  LOAD_GLOBAL           6  'Exception'
              133  COMPARE_OP           10  exception-match
              136  POP_JUMP_IF_FALSE   192  'to 192'
              139  POP_TOP          
              140  POP_TOP          
              141  POP_TOP          

 L. 471       142  LOAD_GLOBAL           8  'texceptions'
              145  LOAD_ATTR             9  'TemplateValueError'

 L. 472       148  LOAD_CONST               'Invalid %s argument for "%s": expected a numerical value.'
              151  LOAD_FAST             0  'self'
              154  LOAD_ATTR            10  'ordinal'
              157  LOAD_FAST             2  'argc'
              160  LOAD_CONST               1
              163  BINARY_ADD       
              164  CALL_FUNCTION_1       1  None
              167  LOAD_FAST             1  'name'
              170  BUILD_TUPLE_2         2 
              173  BINARY_MODULO    

 L. 473       174  LOAD_FAST             0  'self'
              177  LOAD_ATTR            11  'filepos'
              180  LOAD_FAST             4  'arg'
              183  CALL_FUNCTION_3       3  None
              186  RAISE_VARARGS_1       1  None
              189  JUMP_ABSOLUTE       197  'to 197'
              192  END_FINALLY      
            193_0  COME_FROM           192  '192'
              193  JUMP_FORWARD          1  'to 197'
              196  END_FINALLY      
            197_0  COME_FROM           196  '196'
            197_1  COME_FROM            94  '94'

 L. 475       197  LOAD_FAST             5  'v'
              200  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 200


class IndexExec(MathExec):
    """
    A helper mixin used for parsing indices. This is descended from `MathExec`. Primary purpose is to
    provide the `parseIndexArg` method.
    """

    def parseIndexArg(self, name, argc, args):
        """
        Parses an argument for a starting index value. A starting index value is a String representing
        an integer value. Returns the index, or raises an exception if it was invalid.
        """
        idx = self.parseNumericArg(name, argc, args)
        if not isinstance(idx, (int, long)):
            raise texceptions.TemplateValueError('Invalid %s argument for "%s": expected an integer value.' % (self.ordinal(argc + 1), name), self.filepos, idx)
        return idx

    def parseEndIndexArg--- This code section failed: ---

 L. 503         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             3  'args'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_FAST             2  'argc'
               12  COMPARE_OP            4  >
               15  POP_JUMP_IF_TRUE     43  'to 43'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               '%d > %d'
               24  LOAD_GLOBAL           0  'len'
               27  LOAD_FAST             3  'args'
               30  CALL_FUNCTION_1       1  None
               33  LOAD_FAST             2  'argc'
               36  BUILD_TUPLE_2         2 
               39  BINARY_MODULO    
               40  RAISE_VARARGS_2       2  None

 L. 505        43  LOAD_FAST             0  'self'
               46  LOAD_ATTR             2  'checkArgType'
               49  LOAD_FAST             1  'name'
               52  LOAD_FAST             2  'argc'
               55  LOAD_FAST             3  'args'
               58  LOAD_GLOBAL           3  'ttypes'
               61  LOAD_ATTR             4  'String'
               64  CALL_FUNCTION_4       4  None
               67  POP_TOP          

 L. 506        68  LOAD_FAST             3  'args'
               71  LOAD_FAST             2  'argc'
               74  BINARY_SUBSCR    
               75  STORE_FAST            4  'arg'

 L. 507        78  LOAD_FAST             4  'arg'
               81  LOAD_CONST               'END'
               84  COMPARE_OP            2  ==
               87  POP_JUMP_IF_FALSE    94  'to 94'

 L. 508        90  LOAD_CONST               None
               93  RETURN_END_IF    
             94_0  COME_FROM            87  '87'

 L. 510        94  LOAD_FAST             0  'self'
               97  LOAD_ATTR             6  'parseIndexArg'
              100  LOAD_FAST             1  'name'
              103  LOAD_FAST             2  'argc'
              106  LOAD_FAST             3  'args'
              109  CALL_FUNCTION_3       3  None
              112  RETURN_VALUE     
              113  LOAD_CONST               None
              116  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 113


class FindExec(IndexExec):
    """
    A utility class for functions similar to `find` and `str.find` (aka `strpos`).
    Overrides the execute method to do all the proper checking of arguments (other
    than checking types of `NEEDLE` and `HAYSTACK`), then passes them all to
    the `find` method, which you need to override.
    """

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[2, 3, 4])
        needle = args[0]
        startIdx = None
        endIdx = None
        end = None
        if count == 2:
            haystackIdx = 1
        else:
            startIdx = 1
            if count == 3:
                haystackIdx = 2
            else:
                endIdx = 2
                end = self.parseEndIndexArg(name, endIdx, args)
                haystackIdx = 3
        if startIdx is None:
            start = 0
        else:
            start = self.parseIndexArg(name, startIdx, args)
        haystack = args[haystackIdx]
        found = self.find(name, needle, start, end, haystack, args, 0, startIdx, endIdx, haystackIdx)
        if found is None:
            return ttypes.Null()
        else:
            if isinstance(found, (int, long)):
                if found >= 0:
                    return ttypes.String(found)
                else:
                    return Null()

            else:
                raise TypeError('Invalid type returned by find method: expected an integer, or None.')
            return

    @abc.abstractmethod
    def find(self, name, needle, start, end, haystack, args, needleIdx, startIdx, endIdx, haystackIdx):
        """
        This is where subclasses do their work to find the needle in the haystack. This is called by
        `execute` after processing all the args, your job is to find the index and return it as an 
        int, or return None if you can't find it. A negative integer return value is also acceptable
        when you can't find it, but execute will still return NULL for unfound objects.

        Arguments:
            - `name` is the name with which the function is invoked (e.g., for error messages).
            - `needle` is the object being sought.
            - `start` is the index to start looking at. This will always be an integer value: if the
              caller didn't specify a value, the default is 0.
            - `end` is the index to stop looking (i.e., *before* this index). This will either be
              an integer or None if the user didn't specify or specified "END". It's up to you to
              decide what the "END" is.
            - `haystack` is the object being searched.
            - `args` is the complete list of arguments that were passed in, for your reference and for
              error checking functions like `checkArgType`.
            - `needleIdx`, `startIdx`, `endIdx`, and `haystackIdx` are the indices into `args` of the
              respective arguments.  For needle and haystack, the indices are always set. For the start
              and end, they will either be set, or they will be None if the user didn't provide them.
        """
        pass


class IsTypeExec(Executable):

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        if isinstance(args[0], self.expectedType):
            string = '1'
        else:
            string = '0'
        return ttypes.String(string)

    @abc.abstractproperty
    def expectedType(self):
        pass


class ForLoopExec(Executable):
    """
    A utility class for operators that do for-loop operations.
    The execute method should yield values from `loop`, and just do
    what it needs to with each result.
    """

    def loop(self, name, args, ostream, stack):
        """
        Iterates over the loop and evaluates the expression(s), yielding results
        as they come. Pushes a new scope before any evaluation, and pops it before
        leaving. If you abort iterating for any reason (can't imagine why), you
        need to pop the scope. Exceptions are trapped so we can pop first, and
        then raised again. It's only if you stop iterating over this generator
        before it's done.
        """
        count = self.checkArgCount(name, args, exact=[3, 4])
        varname, seq = (teval.evalExpression(arg, ostream, stack) for arg in args[0:2])
        self.checkType('first argument for "%s"' % name, varname, ttypes.String)
        self.checkType('second argument for "%s"' % name, seq, ttypes.List)
        if count == 3:
            test = lambda : True
            expr = args[2]
        else:
            test = lambda : teval.evalExpression(args[2], ostream, stack) != '0'
            expr = args[3]
        scope = stack.push()
        try:
            for val in seq:
                scope[varname] = val
                cond = test()
                if cond:
                    res = teval.evalExpression(expr, ostream, stack)
                    if isinstance(res, ttypes.Return):
                        yield res.raw()
                        break
                    else:
                        yield res

        finally:
            stack.pop()


class WhileLoopExec(Executable):
    """
    A utility class for operators that do while-loop operations.
    The execute method should yield values from `loop`, and just do
    what it needs to with each result.

    {while TEST DO}
    """

    def loop(self, name, args, ostream, stack):
        """
        Iterates over the loop and evaluates the expression(s), yielding results
        as they come. Pushes a new scope before any evaluation, and pops it before
        leaving. If you abort iterating for any reason (can't imagine why), you
        need to pop the scope. Exceptions are trapped so we can pop first, and
        then raised again. It's only if you stop iterating over this generator
        before it's done.
        """
        self.checkArgCount(name, args, exact=[2])
        scope = stack.push()
        try:
            while True:
                cond = teval.evalExpression(args[0], ostream, stack)
                if cond == '0':
                    break
                else:
                    res = teval.evalExpression(args[1], ostream, stack)
                    if isinstance(res, ttypes.Return):
                        yield res.raw()
                        break
                    else:
                        yield res

        finally:
            stack.pop()


class LoopLoopExec(Executable):
    """
    A utility class for operators that do loop-loop operations.
    The execute method should yield values from `loop`, and just do
    what it needs to with each result.

    {loop [INIT] [TEST] [POST] DO}
    {loop [INIT] TEST [POST] DO}
    {loop [INIT] TEST POST DO}
    """

    def loop(self, name, args, ostream, stack):
        """
        Iterates over the loop and evaluates the expression(s), yielding results
        as they come. Pushes a new scope before any evaluation, and pops it before
        leaving. If you abort iterating for any reason (can't imagine why), you
        need to pop the scope. Exceptions are trapped so we can pop first, and
        then raised again. It's only if you stop iterating over this generator
        before it's done.

        Note that yielding is done *before* POST is evaled.
        """
        count = self.checkArgCount(name, args, exact=[1, 2, 3, 4])
        if count == 1:
            init = post = lambda : None
            test = lambda : True
            expr = args[0]
        elif count == 2:
            init = post = lambda : None
            test, expr = args
            test = lambda : teval.evalExpression(args[0], ostream, stack) != '0'
        elif count == 3:
            init = lambda : None
            test, post, expr = args
            test = lambda : teval.evalExpression(args[0], ostream, stack) != '0'
            post = lambda : teval.evalExpression(args[1], ostream, stack)
        else:
            init, test, post, expr = args
            init = lambda : teval.evalExpression(args[0], ostream, stack)
            test = lambda : teval.evalExpression(args[1], ostream, stack) != '0'
            post = lambda : teval.evalExpression(args[2], ostream, stack)
        stack.push()
        try:
            init()
            res = Null()
            while True:
                if test():
                    res = teval.evalExpression(expr, ostream, stack)
                    if isinstance(res, ttypes.Return):
                        yield res.raw()
                        break
                    else:
                        yield res
                    post()
                else:
                    break

        finally:
            stack.pop()


class PrecisionExec(MathExec, TFunction):
    """
    Helper function for things like floor, ceiling, and round.
    """

    @abc.abstractmethod
    def makeInt(self, value):
        """
        Does the actual conversion for the function, but always for precision 0. The base class implementation
        of execute will adjust the value appropriately before and after, to compensate for the specified precision.
        The job of this function is just to get rid of all the digits to the right of the radix point.
        """
        pass

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2])
        args = self.parseNumericArgs(name, args)
        if count == 1:
            res = int(self.makeInt(args[0]))
        else:
            val, prec = args
            if not isinstance(prec, (int, long)):
                raise texceptions.TemplateValueError('Invalid second argument for "%s": expected an integer value.' % name, self.filepos, prec)
            adj = pow(10.0, prec)
            res = self.makeInt(val * adj) / adj
            if prec < 1:
                res = int(res)
        return ttypes.String(res)


class BinaryCompareExec(MathExec, TFunction):
    """
    A helper class for functions that compare two values to result in a true or false value.
    Subclasses just need to implement `compare`.
    """

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        values = self.parseNumericArgs(name, args)
        if self.compare(values[0], values[1]):
            return ttypes.String('1')
        else:
            return ttypes.String('0')

    @abc.abstractmethod
    def compare(self, a, b):
        """
        Compare the two values a and b. Return a boolean true or false.
        """
        pass


def exe_class(cls):
    """
    A class decorator for all "native" executables.

    Create's a new instance of the executable class and adds that instance to the global
    `functions` list as a two-tuple with the class's `__mnemonics__` attribute as the list of
    aliases. Also sets the instance's name and aliases property from `__mnemonics__`.
    """
    if not issubclass(cls, Executable):
        raise TypeError('Only subclasses of Executable can be decorated with @exe_class.')
    elif not hasattr(cls, '__mnemonics__'):
        raise Exception('Executable class missing required __mnemonics__ attribute.')
    elif not isinstance(cls.__mnemonics__, collections.Iterable):
        raise TypeError("Incorrect type for executable's __mnemonics__ attributes: Expected iterable.")
    else:
        func = cls()
        func.name = cls.__mnemonics__[0]
        func.setAliases(cls.__mnemonics__[1:])
        functions.append((func, tuple(cls.__mnemonics__)))
    return cls


def operator(cls):
    """
    Decorator for Operator classes. Ensures it's a subclass of `TOperator`, then delegates to
    `exe_class`.
    """
    if not issubclass(cls, TOperator):
        raise TypeError('Only subclasses of TOperator can be decorated with @operator.')
    return exe_class(cls)


def function(cls):
    """
    Decorator for Function classes. Ensures it's a subclass of `TFunction`, then delegates to
    `exe_class`.
    """
    if not issubclass(cls, TFunction):
        raise TypeError('Only subclasses of TFunction can be decorated with @function.')
    return exe_class(cls)


def macro(cls):
    """
    Decorator for Macro classes. Ensures it's a subclass of `TMacro`, then delegates to
    `exe_class`.
    """
    if not issubclass(cls, TMacro):
        raise TypeError('Only subclasses of TMacro can be decorated with @macro.')
    return exe_class(cls)


functions = []

def getGlobalScope():
    """
    Returns a Scope pre-populated with all of the builtin functions, operators, and macros, from
    the functions list.
    """
    func_dict = {}
    for func, aliases in functions:
        if not isinstance(func, Executable):
            raise ValueError("Error in function definitions: not an Executable for class '%s'." % func)
        for alias in aliases:
            alias = ttypes.String(alias)
            if alias in func_dict:
                raise KeyError("Duplicate function alias '%s'." % alias)
            func_dict[alias] = func

    return tStack.Scope(func_dict)