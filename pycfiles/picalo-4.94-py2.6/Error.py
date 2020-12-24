# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/Error.py
# Compiled at: 2008-03-17 12:58:02
import sys
__all__ = [
 'error']

class error:

    def __init__(self, exc=None, msg=None, previous=None):
        """An error type that signifies that an error occurred when
       calculating the value for some cell.  Don't create this
       directly.  Picalo creates them when errors
       are encountered during analyses so the analysis doesn't 
       get stopped by small errors.
       
       The error object is useful in that it encodes information
       about what went wrong.  Although it only prints as <err>
       in table listings, it can be inspected as shown in the 
       set_type method example.
       
       @param exc:         The exception object.
       @type  exc:         Exception
       @param msg:         Allows you to provide a specific error message.  Defaults to str(exception).
       @type  msg:         str
       @param previous:    The previous value of the cell, so we don't lose it.
       @type  previous:    object
    """
        self.msg = msg
        self.exc = None
        self.previous = previous
        if exc:
            if msg == None:
                self.msg = str(exc)
            if isinstance(exc, Exception):
                self.exc = exc
        if self.msg == None:
            self.msg = 'Unspecified Error'
        return

    def __repr__(self):
        return '<err: ' + str(self.msg) + '>'

    def __str__(self):
        return '<err: ' + str(self.msg) + '>'

    def get_message(self):
        """Returns the actual error message.  This allows the object
       to be interrogated for what really went wrong.
     
       @return:  The error message.
       @rtype:   str
    """
        return self.msg

    def get_exception(self):
        """Returns the exception object associated with this error.
       This might be None if no object was created.
       
       @return:   The exception object that caused this error.
       @rtype:    Exception
    """
        return self.exc

    def get_previous(self):
        """Returns the previous value of the cell before the error
       was placed in the table.  This might be none if the 
       error didn't replace a cell value.
       
       @return:   The previous value of the cell where this error occurred.
       @rtype:    object
    """
        return self.previous

    def __lt__(self, other):
        return id(self) < id(other)

    def __le__(self, other):
        return id(self) <= id(other)

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return id(self) != id(other)

    def __gt__(self, other):
        return id(self) > id(other)

    def __ge__(self, other):
        return id(self) >= id(other)

    def __cmp__(self, *args, **kargs):
        return cmp(id(self, *args, **kargs), id(other))

    def __nonzero__(self, *args, **kargs):
        return True

    def __len__(self, *args, **kargs):
        return 0

    def __getitem__(self, key):
        return self

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __iter__(self, *args, **kargs):
        return iter([])

    def __contains__(self, item):
        return False

    def __add__(self, *args, **kargs):
        return self

    def __sub__(self, *args, **kargs):
        return self

    def __mul__(self, *args, **kargs):
        return self

    def __floordiv__(self, *args, **kargs):
        return self

    def __mod__(self, *args, **kargs):
        return self

    def __divmod__(self, *args, **kargs):
        return self

    def __pow__(self, *args, **kargs):
        return self

    def __lshift__(self, *args, **kargs):
        return self

    def __rshift__(self, *args, **kargs):
        return self

    def __and__(self, *args, **kargs):
        return self

    def __xor__(self, *args, **kargs):
        return self

    def __or__(self, *args, **kargs):
        return self

    def __div__(self, *args, **kargs):
        return self

    def __truediv__(self, *args, **kargs):
        return self

    def __radd__(self, *args, **kargs):
        return self

    def __rsub__(self, *args, **kargs):
        return self

    def __rmul__(self, *args, **kargs):
        return self

    def __rdiv__(self, *args, **kargs):
        return self

    def __rtruediv__(self, *args, **kargs):
        return self

    def __rfloordiv__(self, *args, **kargs):
        return self

    def __rmod__(self, *args, **kargs):
        return self

    def __rdivmod__(self, *args, **kargs):
        return self

    def __rpow__(self, *args, **kargs):
        return self

    def __rlshift__(self, *args, **kargs):
        return self

    def __rrshift__(self, *args, **kargs):
        return self

    def __rand__(self, *args, **kargs):
        return self

    def __rxor__(self, *args, **kargs):
        return self

    def __ror__(self, *args, **kargs):
        return self

    def __iadd__(self, *args, **kargs):
        return self

    def __isub__(self, *args, **kargs):
        return self

    def __imul__(self, *args, **kargs):
        return self

    def __idiv__(self, *args, **kargs):
        return self

    def __itruediv__(self, *args, **kargs):
        return self

    def __ifloordiv__(self, *args, **kargs):
        return self

    def __imod__(self, *args, **kargs):
        return self

    def __ipow__(self, *args, **kargs):
        return self

    def __ilshift__(self, *args, **kargs):
        return self

    def __irshift__(self, *args, **kargs):
        return self

    def __iand__(self, *args, **kargs):
        return self

    def __ixor__(self, *args, **kargs):
        return self

    def __ior__(self, *args, **kargs):
        return self

    def __neg__(self, *args, **kargs):
        return self

    def __pos__(self, *args, **kargs):
        return self

    def __abs__(self, *args, **kargs):
        return self

    def __invert__(self, *args, **kargs):
        return self

    def __complex__(self, *args, **kargs):
        return complex(0)

    def __int__(self, *args, **kargs):
        return 0

    def __long__(self, *args, **kargs):
        return 0

    def __float__(self, *args, **kargs):
        return 0.0

    def __oct__(self, *args, **kargs):
        return str(self, *args, **kargs)

    def __hex__(self, *args, **kargs):
        return str(self, *args, **kargs)

    def __coerce(self, other):
        return (
         self, other)