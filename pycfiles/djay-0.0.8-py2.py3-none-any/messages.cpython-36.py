# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/messages.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 7575 bytes
"""
Provide the class Message and its subclasses.
"""

class Message(object):
    message = ''
    message_args = ()

    def __init__(self, filename, loc):
        self.filename = filename
        self.lineno = loc.lineno
        self.col = getattr(loc, 'col_offset', 0)

    def __str__(self):
        return '%s:%s: %s' % (self.filename, self.lineno,
         self.message % self.message_args)


class UnusedImport(Message):
    message = '%r imported but unused'

    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class RedefinedWhileUnused(Message):
    message = 'redefinition of unused %r from line %r'

    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class RedefinedInListComp(Message):
    message = 'list comprehension redefines %r from line %r'

    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class ImportShadowedByLoopVar(Message):
    message = 'import %r from line %r shadowed by loop variable'

    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class ImportStarNotPermitted(Message):
    message = "'from %s import *' only allowed at module level"

    def __init__(self, filename, loc, modname):
        Message.__init__(self, filename, loc)
        self.message_args = (modname,)


class ImportStarUsed(Message):
    message = "'from %s import *' used; unable to detect undefined names"

    def __init__(self, filename, loc, modname):
        Message.__init__(self, filename, loc)
        self.message_args = (modname,)


class ImportStarUsage(Message):
    message = '%r may be undefined, or defined from star imports: %s'

    def __init__(self, filename, loc, name, from_list):
        Message.__init__(self, filename, loc)
        self.message_args = (name, from_list)


class UndefinedName(Message):
    message = 'undefined name %r'

    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class DoctestSyntaxError(Message):
    message = 'syntax error in doctest'

    def __init__(self, filename, loc, position=None):
        Message.__init__(self, filename, loc)
        if position:
            self.lineno, self.col = position
        self.message_args = ()


class UndefinedExport(Message):
    message = 'undefined name %r in __all__'

    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class UndefinedLocal(Message):
    message = 'local variable %r {0} referenced before assignment'
    default = 'defined in enclosing scope on line %r'
    builtin = 'defined as a builtin'

    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        if orig_loc is None:
            self.message = self.message.format(self.builtin)
            self.message_args = name
        else:
            self.message = self.message.format(self.default)
            self.message_args = (name, orig_loc.lineno)


class DuplicateArgument(Message):
    message = 'duplicate argument %r in function definition'

    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class MultiValueRepeatedKeyLiteral(Message):
    message = 'dictionary key %r repeated with different values'

    def __init__(self, filename, loc, key):
        Message.__init__(self, filename, loc)
        self.message_args = (key,)


class MultiValueRepeatedKeyVariable(Message):
    message = 'dictionary key variable %s repeated with different values'

    def __init__(self, filename, loc, key):
        Message.__init__(self, filename, loc)
        self.message_args = (key,)


class LateFutureImport(Message):
    message = 'from __future__ imports must occur at the beginning of the file'

    def __init__(self, filename, loc, names):
        Message.__init__(self, filename, loc)
        self.message_args = ()


class FutureFeatureNotDefined(Message):
    __doc__ = 'An undefined __future__ feature name was imported.'
    message = 'future feature %s is not defined'

    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class UnusedVariable(Message):
    __doc__ = '\n    Indicates that a variable has been explicitly assigned to but not actually\n    used.\n    '
    message = 'local variable %r is assigned to but never used'

    def __init__(self, filename, loc, names):
        Message.__init__(self, filename, loc)
        self.message_args = (names,)


class ReturnWithArgsInsideGenerator(Message):
    __doc__ = '\n    Indicates a return statement with arguments inside a generator.\n    '
    message = "'return' with argument inside generator"


class ReturnOutsideFunction(Message):
    __doc__ = '\n    Indicates a return statement outside of a function/method.\n    '
    message = "'return' outside function"


class YieldOutsideFunction(Message):
    __doc__ = '\n    Indicates a yield or yield from statement outside of a function/method.\n    '
    message = "'yield' outside function"


class ContinueOutsideLoop(Message):
    __doc__ = '\n    Indicates a continue statement outside of a while or for loop.\n    '
    message = "'continue' not properly in loop"


class BreakOutsideLoop(Message):
    __doc__ = '\n    Indicates a break statement outside of a while or for loop.\n    '
    message = "'break' outside loop"


class ContinueInFinally(Message):
    __doc__ = '\n    Indicates a continue statement in a finally block in a while or for loop.\n    '
    message = "'continue' not supported inside 'finally' clause"


class DefaultExceptNotLast(Message):
    __doc__ = '\n    Indicates an except: block as not the last exception handler.\n    '
    message = "default 'except:' must be last"


class TwoStarredExpressions(Message):
    __doc__ = '\n    Two or more starred expressions in an assignment (a, *b, *c = d).\n    '
    message = 'two starred expressions in assignment'


class TooManyExpressionsInStarredAssignment(Message):
    __doc__ = '\n    Too many expressions in an assignment with star-unpacking\n    '
    message = 'too many expressions in star-unpacking assignment'


class AssertTuple(Message):
    __doc__ = '\n    Assertion test is a tuple, which are always True.\n    '
    message = 'assertion is always true, perhaps remove parentheses?'


class ForwardAnnotationSyntaxError(Message):
    message = 'syntax error in forward annotation %r'

    def __init__(self, filename, loc, annotation):
        Message.__init__(self, filename, loc)
        self.message_args = (annotation,)


class CommentAnnotationSyntaxError(Message):
    message = 'syntax error in type comment %r'

    def __init__(self, filename, loc, annotation):
        Message.__init__(self, filename, loc)
        self.message_args = (annotation,)


class RaiseNotImplemented(Message):
    message = "'raise NotImplemented' should be 'raise NotImplementedError'"


class InvalidPrintSyntax(Message):
    message = 'use of >> is invalid with print function'


class IsLiteral(Message):
    message = 'use ==/!= to compare str, bytes, and int literals'