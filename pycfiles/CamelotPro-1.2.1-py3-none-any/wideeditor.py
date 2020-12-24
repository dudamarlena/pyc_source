# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/wideeditor.py
# Compiled at: 2013-04-11 17:47:52


class WideEditor(object):
    """Class signaling that an editor, is a wide editor, so it's label should be displayed
  on top of the editor and the editor itself should take two columns::

    class WideTextLineEditor(TextLineEditor, WideEditor):
      pass

  will generate a test line editor where the text line takes the whole with of the
  form"""