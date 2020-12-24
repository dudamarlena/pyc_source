# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jquery/widget/resteditor/interfaces.py
# Compiled at: 2007-05-24 08:27:53
"""
$Id: layer.py 197 2007-04-13 05:03:32Z rineichen $
"""
__docformat__ = 'reStructuredText'
from z3c.form import interfaces

class IRESTEditorWidget(interfaces.ITextAreaWidget):
    """RESTEditor widget interface."""
    __module__ = __name__