# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/languagedelegate.py
# Compiled at: 2013-04-11 17:47:52
from plaintextdelegate import PlainTextDelegate
from camelot.view.controls.editors import LanguageEditor

class LanguageDelegate(PlainTextDelegate):
    """Delegate for :class:`camelot.types.Language` columns.  Expects string
    values.
    """
    editor = LanguageEditor