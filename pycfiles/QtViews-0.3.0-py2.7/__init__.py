# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtviews/__init__.py
# Compiled at: 2015-01-16 13:00:43
qt_bindings = 'PySide'
if qt_bindings == 'PyQt4':
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
from .dockers import *
from .calendar import CalendarView, CalendarTopNav
__version_info__ = [
 '0', '3', '0']
__version__ = ('.').join(__version_info__)