# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/baseskin/schema.py
# Compiled at: 2014-04-02 09:41:12
from z3c.form.interfaces import IButton
from z3c.form.button import Button
from zope.interface import implements

class IResetButton(IButton):
    """Reset button interface"""
    pass


class ResetButton(Button):
    """Reset button"""
    implements(IResetButton)


class ICloseButton(IButton):
    """Close button interface"""
    pass


class CloseButton(Button):
    """Close button"""
    implements(ICloseButton)