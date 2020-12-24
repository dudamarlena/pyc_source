# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\an_example_pypi_project\useful_2.py
# Compiled at: 2009-11-11 21:35:44
__doc__ = 'A very useful module indeed. \n\n'

def public_fn_with_googley_docstring(name, state=None):
    """This function does something.
    
    Args:
       name (str):  The name to use. 
       
    Kwargs:
       state (bool): Current state to be in. 

    Returns: 
       int.  The return code::
       
          0 -- Success!
          1 -- No good. 
          2 -- Try again. 
    
    Raises:
       AttributeError, KeyError

    A really great idea.  A way you might use me is
    
    >>> print public_fn_with_googley_docstring(name='foo', state=None)
    0
    
    BTW, this always returns 0.  **NEVER** use with :class:`MyPublicClass`.
    
    """
    return 0


def public_fn_with_sphinxy_docstring(name, state=None):
    """This function does something.
    
    :param name: The name to use.
    :type name: str.
    :param state: Current state to be in.    
    :type state: bool.
    :returns:  int -- the return code.      
    :raises: AttributeError, KeyError

    """
    return 0


def public_fn_without_docstring():
    return True


def _private_fn_with_docstring(foo, bar='baz', foobarbas=None):
    """I have a docstring, but won't be imported if you just use ``:members:``.
    """
    return


class MyPublicClass(object):
    """We use this as a public class example class.

    You never call this class before calling :func:`public_fn_with_sphinxy_docstring`.
    
    .. note:: 
      
       An example of intersphinx is this: you **cannot** use :mod:`pickle` on this class. 
    
    """
    __module__ = __name__

    def __init__(self, foo, bar='baz'):
        """A really simple class.
        
        Args:
           foo (str): We all know what foo does. 
           
        Kwargs:
           bar (str): Really, same as foo.  
    
        """
        self._foo = foo
        self._bar = bar

    def get_foobar(self, foo, bar=True):
        """This gets the foobar
        
        This really should have a full function definition, but I am too lazy. 

        >>> print get_foobar(10, 20)
        30
        >>> print get_foobar('a', 'b')
        ab
        
        Isn't that what you want?
        
        """
        return foo + bar

    def _get_baz(self, baz=None):
        """A private function to get baz.
        
        This really should have a full function definition, but I am too lazy. 
        
        """
        return baz