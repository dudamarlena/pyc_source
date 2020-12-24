# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hexagonit/form/interfaces.py
# Compiled at: 2006-10-07 14:17:38
from zope.formlib.interfaces import IFormFields

class IOrderableFormFields(IFormFields):
    """Orderable collection of form fields (IFormField).
    
    The moveField() method is modeled after the
    Archetypes.Schema.Schema.moveField() method.
    """
    __module__ = __name__

    def moveField(name, direction=None, position=None, after=None, before=None):
        """Moves a form field within the group of fields to a new position.

        The new position may be given as a relative position using parameters
        ``direction``, ``before`` or ``after`` or by using the absolute
        position parameter ``position``.
        
        The ``direction`` parameter accepts values ``up`` and ``down``. Both
        ``after`` and ``before`` parameters require a name of another field in
        the collection. The ``position`` parameter takes either an integer for
        the new position or the string ``top`` or ``bottom`` (alternatively
        ``first`` or ``last``).
        """
        pass