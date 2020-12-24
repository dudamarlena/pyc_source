# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zc/shortcut/i18n.py
# Compiled at: 2006-12-07 13:02:03
"""I18N support for shortcuts.

This defines a `MessageFactory` for the I18N domain for the shortcut
package.  This is normally used with this import::

  from i18n import MessageFactory as _

The factory is then used normally.  Two examples::

  text = _('some internationalized text')
  text = _('helpful-descriptive-message-id', 'default text')
"""
__docformat__ = 'reStructuredText'
from zope import i18nmessageid
MessageFactory = _ = i18nmessageid.MessageFactory('zc.shortcut')