# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/Calc.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Application, Button, GridLayout, Label, Window
from muntjac.ui.button import IClickListener

class Calc(Application, IClickListener):
    """A simple calculator using Muntjac."""

    def __init__(self):
        super(Calc, self).__init__()
        self._current = 0.0
        self._stored = 0.0
        self._lastOperationRequested = 'C'
        self._display = Label('0.0')

    def init(self):
        layout = GridLayout(4, 5)
        self.setMainWindow(Window('Calculator Application', layout))
        layout.addComponent(self._display, 0, 0, 3, 0)
        operations = [
         '7', '8', '9', '/', '4', '5', '6',
         '*', '1', '2', '3', '-', '0', '=', 'C', '+']
        for caption in operations:
            button = Button(caption)
            button.addListener(self)
            layout.addComponent(button)

    def buttonClick(self, event):
        button = event.getButton()
        requestedOperation = button.getCaption()[0]
        newValue = self.calculate(requestedOperation)
        self._display.setValue(newValue)

    def calculate(self, requestedOperation):
        if '0' <= requestedOperation and requestedOperation <= '9':
            self._current = self._current * 10 + float('' + requestedOperation)
            return self._current
        last = self._lastOperationRequested
        if last == '+':
            self._stored += self._current
        elif last == '-':
            self._stored -= self._current
        elif last == '/':
            try:
                self._stored /= self._current
            except ZeroDivisionError:
                pass

        elif last == '*':
            self._stored *= self._current
        elif last == 'C':
            self._stored = self._current
        self._lastOperationRequested = requestedOperation
        self._current = 0.0
        if requestedOperation == 'C':
            self._stored = 0.0
        return self._stored


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(Calc, nogui=True, forever=True, debug=True)