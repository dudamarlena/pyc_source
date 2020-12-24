# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/sigdispatch/__init__.py
# Compiled at: 2015-01-13 11:07:57
"""
sigdispatch
~~~~~~~~~~~

Sigdispatch is a simple events library.

>>> import sigdispatch
>>> def on_foo(payload):
...     print 'Received %s' % payload
...
>>> sigdispatch.observe('foo', on_foo)
>>> sigdispatch.emit('foo', 'bar')
Received bar

.. data:: default_dispatcher

   An instance of :py:class:`SignalDispatcher`. Calls to
   :py:func:`sigdispatch.observe`, :py:func:`emit` and
   :py:func:`on_exceptions` are method invocations of this object.

.. automodule:: sigdispatch.SignalDispatcher
   :members:
"""
__version__ = '0.0.1'
from .SignalDispatcher import SignalDispatcher
default_dispatcher = SignalDispatcher()

def observe(*args, **kwargs):
    """
    Calls ``default_dispatcher.observe``.
    See :py:meth:`.SignalDispatcher.observe`.
    """
    default_dispatcher.observe(*args, **kwargs)


def emit(*args, **kwargs):
    """
    Calls ``default_dispatcher.emit``.
    See :py:meth:`.SignalDispatcher.emit`.
    """
    default_dispatcher.emit(*args, **kwargs)


def on_exceptions(*args, **kwargs):
    """
    Calls ``default_dispatcher.observe``.
    See :py:meth:`.SignalDispatcher.on_exceptions`.
    """
    default_dispatcher.on_exceptions(*args, **kwargs)