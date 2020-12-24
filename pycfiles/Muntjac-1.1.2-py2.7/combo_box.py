# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/combo_box.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a filtering drop-down single-select."""
from muntjac.ui.select import Select
from muntjac.data.container import IContainer
from muntjac.terminal.gwt.client.ui.v_filter_select import VFilterSelect

class ComboBox(Select):
    """A filtering dropdown single-select. Suitable for newItemsAllowed, but
    it's turned of by default to avoid mistakes. Items are filtered based on
    user input, and loaded dynamically ("lazy-loading") from the server. You
    can turn on newItemsAllowed and change filtering mode (and also turn it
    off), but you can not turn on multi-select mode.
    """
    CLIENT_WIDGET = None

    def __init__(self, *args):
        self._inputPrompt = None
        self._textInputAllowed = True
        nargs = len(args)
        if nargs == 0:
            super(ComboBox, self).__init__()
            self.setMultiSelect(False)
            self.setNewItemsAllowed(False)
        elif nargs == 1:
            caption, = args
            super(ComboBox, self).__init__(caption)
            self.setMultiSelect(False)
            self.setNewItemsAllowed(False)
        elif nargs == 2:
            if isinstance(args[1], IContainer):
                caption, dataSource = args
                super(ComboBox, self).__init__(caption, dataSource)
                self.setMultiSelect(False)
                self.setNewItemsAllowed(False)
            else:
                caption, options = args
                super(ComboBox, self).__init__(caption, options)
                self.setMultiSelect(False)
                self.setNewItemsAllowed(False)
        else:
            raise ValueError, 'too many arguments'
        return

    def setMultiSelect(self, multiSelect):
        if multiSelect and not self.isMultiSelect():
            raise NotImplementedError, 'Multiselect not supported'
        super(ComboBox, self).setMultiSelect(multiSelect)

    def getInputPrompt(self):
        """Gets the current input prompt.

        @see: L{setInputPrompt}
        @return: the current input prompt, or null if not enabled
        """
        return self._inputPrompt

    def setInputPrompt(self, inputPrompt):
        """Sets the input prompt - a textual prompt that is displayed when
        the select would otherwise be empty, to prompt the user for input.

        @param inputPrompt:
                   the desired input prompt, or null to disable
        """
        self._inputPrompt = inputPrompt
        self.requestRepaint()

    def paintContent(self, target):
        if self._inputPrompt is not None:
            target.addAttribute('prompt', self._inputPrompt)
        super(ComboBox, self).paintContent(target)
        if not self._textInputAllowed:
            target.addAttribute(VFilterSelect.ATTR_NO_TEXT_INPUT, True)
        return

    def setTextInputAllowed(self, textInputAllowed):
        """Sets whether it is possible to input text into the field or whether
        the field area of the component is just used to show what is selected.
        By disabling text input, the comboBox will work in the same way as a
        L{NativeSelect}

        @see L{isTextInputAllowed}

        @param textInputAllowed:
                 true to allow entering text, false to just show the current
                 selection
        """
        self._textInputAllowed = textInputAllowed
        self.requestRepaint()

    def isTextInputAllowed(self):
        """Returns true if the user can enter text into the field to either
        filter the selections or enter a new value if :{isNewItemsAllowed}
        returns true. If text input is disabled, the comboBox will work in the
        same way as a L{NativeSelect}.
        """
        return self._textInputAllowed