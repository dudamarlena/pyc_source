# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/languagedelegate.py
# Compiled at: 2013-04-11 17:47:52
from plaintextdelegate import PlainTextDelegate
from camelot.view.controls.editors import LanguageEditor

class LanguageDelegate(PlainTextDelegate):
    """Delegate for :class:`camelot.types.Language` columns.  Expects string
    values.
    """
    editor = LanguageEditor