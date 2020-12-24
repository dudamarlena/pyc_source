# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/labeldelegate.py
# Compiled at: 2013-04-11 17:47:52
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors

class LabelDelegate(CustomDelegate):
    """Delegate to display an attribute as a label
    """
    __metaclass__ = DocumentationMetaclass
    editor = editors.LabelEditor