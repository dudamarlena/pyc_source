# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/guimainsignaler.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2498 bytes
"""
Low-level :mod:`PySide2`-based application-wide signal classes.
"""
from PySide2.QtCore import QObject, Signal

class QBetseeSignaler(QObject):
    __doc__ = '\n    :class:`PySide2`-based collection of various application-wide signals.\n\n    These signals permit callers to trigger handling of events by corresponding\n    slots of interested objects and widgets distributed throughout the\n    application, including:\n\n    * Restoration and storage of application-wide settings to and from their\n      on-disk backing store (e.g., an application- and user-specific dotfile).\n\n    Design\n    ----------\n    This class has been intentionally isolated from all sibling classes (e.g.,\n    :class:`QBetseeSettings`) to circumvent circular chicken-and-the-egg issues\n    between this and the :class:`QBetseeMainWindow` class. Conjoining these\n    sibling classes into one monolithic class would introduce non-trivial (and\n    probably non-resolvable) complications, including the need for the\n    conjoined class to retain a weak reference to its\n    :class:`QBetseeMainWindow` parent, which could conceivably be prematurely\n    destroyed by Qt in another thread.\n    '
    restore_settings_signal = Signal()
    store_settings_signal = Signal()