# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/help/assistant.py
# Compiled at: 2019-08-19 15:09:29
"""
This module allows an application to provide help through the Qt
assistant tool.
The :func:`Assistant` will create a subprocess displaying the
help system for the given QtHelp collection file (.qhc).
Example usage::

    from taurus.external.qt import Qt
    from taurus.qt.qtgui.help import Assistant

    app = Qt.QApplication([])
    qas = Assistant("my_app_help.qhc")
    qas.start()
    app.exec_()
"""
from builtins import object
from taurus.external.qt import Qt
__all__ = [
 'Assistant', 'Widgets']

class Widgets(object):
    contents = 'contents'
    index = 'index'
    bookmarks = 'bookmarks'
    search = 'search'


class _Assistant(Qt.QProcess):
    """The help assistant class"""

    def __init__(self, collection_file, parent=None):
        Qt.QProcess.__init__(self, parent)
        self.__collection_file = collection_file

    def start(self):
        if self.isRunning():
            return
        args = [
         '-enableRemoteControl',
         '-collectionFile', self.__collection_file]
        Qt.QProcess.start(self, 'assistant', args)

    def isRunning(self):
        return self.state() == Qt.QProcess.Running

    def __send(self, cmd):
        if not self.isRunning():
            raise Exception('Assistant is not running')
        self.write(cmd + '\n')

    def assistantShow(self, widget):
        self.__send('show ' + widget)

    def assistantHide(self, widget):
        self.__send('hide ' + widget)

    def assistantSetSource(self, url):
        self.__send('setSource ' + url)

    def assistantActivateKeyword(self, keyword):
        self.__send('activateKeyword ' + keyword)

    def assistantActivateIdentifier(self, id):
        self.__send('activateIdentifier ' + id)

    def assistantSyncContents(self):
        self.__send('syncContents')

    def assistantSetCurrentFilter(self, filter):
        self.__send('setCurrentFilter ' + filter)

    def assistantExpandToc(self, depth):
        self.__send('expandToc ' + str(depth))

    def assistantRegister(self, help_file):
        self.__send('register ' + help_file)

    def assistantUnregister(self, help_file):
        self.__send('unregister ' + help_file)


__ASSISTANTS = {}

def Assistant(collection_file, auto_create=True, parent=None):
    """
    The :func:`Assistant` will create a subprocess displaying the
    help system for the given QtHelp collection file (.qhc).
    Example usage::

        from taurus.external.qt import Qt
        from taurus.qt.qtgui.help import Assistant

        app = Qt.QApplication([])
        qas = Assistant("my_app_help.qhc")
        qas.start()
        app.exec_()
    """
    global __ASSISTANTS
    assistant = __ASSISTANTS.get(collection_file)
    if not auto_create:
        return assistant
    else:
        if assistant is None:

            def finished(*args):
                if __ASSISTANTS and collection_file in __ASSISTANTS:
                    del __ASSISTANTS[collection_file]

            assistant = _Assistant(collection_file, parent=parent)
            __ASSISTANTS[collection_file] = assistant
            assistant.finished.connect(finished)
        return assistant


def main():
    import sys
    app = Qt.QApplication([])
    window = Qt.QWidget()
    layout = Qt.QHBoxLayout(window)
    goButton = Qt.QPushButton('Activate help', window)
    terminateButton = Qt.QPushButton('Close help', window)
    textEdit = Qt.QLineEdit(window)
    layout.addWidget(textEdit)
    layout.addWidget(goButton)
    layout.addWidget(terminateButton)

    def go():
        assistant = Assistant(textEdit.text(), parent=window)
        assistant.start()
        assistant.waitForStarted()
        assistant.assistantShow(Widgets.bookmarks)

    def terminate():
        assistant = Assistant(textEdit.text(), auto_create=False, parent=window)
        if assistant:
            assistant.terminate()

    goButton.clicked.connect(go)
    terminateButton.clicked.connect(terminate)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()