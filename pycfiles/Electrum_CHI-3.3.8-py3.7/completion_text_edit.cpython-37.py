# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/gui/qt/completion_text_edit.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 4448 bytes
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCompleter, QPlainTextEdit, QApplication
from .util import ButtonsTextEdit

class CompletionTextEdit(ButtonsTextEdit):

    def __init__(self, parent=None):
        super(CompletionTextEdit, self).__init__(parent)
        self.completer = None
        self.moveCursor(QTextCursor.End)
        self.disable_suggestions()

    def set_completer(self, completer):
        self.completer = completer
        self.initialize_completer()

    def initialize_completer(self):
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.activated.connect(self.insert_completion)
        self.enable_suggestions()

    def insert_completion(self, completion):
        if self.completer.widget() != self:
            return
        else:
            text_cursor = self.textCursor()
            extra = len(completion) - len(self.completer.completionPrefix())
            text_cursor.movePosition(QTextCursor.Left)
            text_cursor.movePosition(QTextCursor.EndOfWord)
            if extra == 0:
                text_cursor.insertText(' ')
            else:
                text_cursor.insertText(completion[-extra:] + ' ')
        self.setTextCursor(text_cursor)

    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def enable_suggestions(self):
        self.suggestions_enabled = True

    def disable_suggestions(self):
        self.suggestions_enabled = False

    def keyPressEvent--- This code section failed: ---

 L.  76         0  LOAD_FAST                'self'
                2  LOAD_METHOD              isReadOnly
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  77         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  79        12  LOAD_FAST                'self'
               14  LOAD_METHOD              is_special_key
               16  LOAD_FAST                'e'
               18  CALL_METHOD_1         1  '1 positional argument'
               20  POP_JUMP_IF_FALSE    34  'to 34'

 L.  80        22  LOAD_FAST                'e'
               24  LOAD_METHOD              ignore
               26  CALL_METHOD_0         0  '0 positional arguments'
               28  POP_TOP          

 L.  81        30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'

 L.  83        34  LOAD_GLOBAL              QPlainTextEdit
               36  LOAD_METHOD              keyPressEvent
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'e'
               42  CALL_METHOD_2         2  '2 positional arguments'
               44  POP_TOP          

 L.  85        46  LOAD_FAST                'e'
               48  LOAD_METHOD              modifiers
               50  CALL_METHOD_0         0  '0 positional arguments'
               52  JUMP_IF_FALSE_OR_POP    64  'to 64'
               54  LOAD_GLOBAL              Qt
               56  LOAD_ATTR                ControlModifier
               58  JUMP_IF_TRUE_OR_POP    64  'to 64'
               60  LOAD_GLOBAL              Qt
               62  LOAD_ATTR                ShiftModifier
             64_0  COME_FROM            58  '58'
             64_1  COME_FROM            52  '52'
               64  STORE_FAST               'ctrlOrShift'

 L.  86        66  LOAD_FAST                'self'
               68  LOAD_ATTR                completer
               70  LOAD_CONST               None
               72  COMPARE_OP               is
               74  POP_JUMP_IF_TRUE     88  'to 88'
               76  LOAD_FAST                'ctrlOrShift'
               78  POP_JUMP_IF_FALSE    92  'to 92'
               80  LOAD_FAST                'e'
               82  LOAD_METHOD              text
               84  CALL_METHOD_0         0  '0 positional arguments'
               86  POP_JUMP_IF_TRUE     92  'to 92'
             88_0  COME_FROM            74  '74'

 L.  87        88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            86  '86'
             92_1  COME_FROM            78  '78'

 L.  89        92  LOAD_FAST                'self'
               94  LOAD_ATTR                suggestions_enabled
               96  POP_JUMP_IF_TRUE    102  'to 102'

 L.  90        98  LOAD_CONST               None
              100  RETURN_VALUE     
            102_0  COME_FROM            96  '96'

 L.  92       102  LOAD_STR                 '~!@#$%^&*()_+{}|:"<>?,./;\'[]\\-='
              104  STORE_FAST               'eow'

 L.  93       106  LOAD_FAST                'e'
              108  LOAD_METHOD              modifiers
              110  CALL_METHOD_0         0  '0 positional arguments'
              112  LOAD_GLOBAL              Qt
              114  LOAD_ATTR                NoModifier
              116  COMPARE_OP               !=
              118  JUMP_IF_FALSE_OR_POP   124  'to 124'
              120  LOAD_FAST                'ctrlOrShift'
              122  UNARY_NOT        
            124_0  COME_FROM           118  '118'
              124  STORE_FAST               'hasModifier'

 L.  94       126  LOAD_FAST                'self'
              128  LOAD_METHOD              text_under_cursor
              130  CALL_METHOD_0         0  '0 positional arguments'
              132  STORE_FAST               'completionPrefix'

 L.  96       134  LOAD_FAST                'hasModifier'
              136  POP_JUMP_IF_TRUE    180  'to 180'
              138  LOAD_FAST                'e'
              140  LOAD_METHOD              text
              142  CALL_METHOD_0         0  '0 positional arguments'
              144  POP_JUMP_IF_FALSE   180  'to 180'
              146  LOAD_GLOBAL              len
              148  LOAD_FAST                'completionPrefix'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  LOAD_CONST               1
              154  COMPARE_OP               <
              156  POP_JUMP_IF_TRUE    180  'to 180'
              158  LOAD_FAST                'eow'
              160  LOAD_METHOD              find
              162  LOAD_FAST                'e'
              164  LOAD_METHOD              text
              166  CALL_METHOD_0         0  '0 positional arguments'
              168  LOAD_CONST               -1
              170  BINARY_SUBSCR    
              172  CALL_METHOD_1         1  '1 positional argument'
              174  LOAD_CONST               0
              176  COMPARE_OP               >=
              178  POP_JUMP_IF_FALSE   198  'to 198'
            180_0  COME_FROM           156  '156'
            180_1  COME_FROM           144  '144'
            180_2  COME_FROM           136  '136'

 L.  97       180  LOAD_FAST                'self'
              182  LOAD_ATTR                completer
              184  LOAD_METHOD              popup
              186  CALL_METHOD_0         0  '0 positional arguments'
              188  LOAD_METHOD              hide
              190  CALL_METHOD_0         0  '0 positional arguments'
              192  POP_TOP          

 L.  98       194  LOAD_CONST               None
              196  RETURN_VALUE     
            198_0  COME_FROM           178  '178'

 L. 100       198  LOAD_FAST                'completionPrefix'
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                completer
              204  LOAD_METHOD              completionPrefix
              206  CALL_METHOD_0         0  '0 positional arguments'
              208  COMPARE_OP               !=
              210  POP_JUMP_IF_FALSE   254  'to 254'

 L. 101       212  LOAD_FAST                'self'
              214  LOAD_ATTR                completer
              216  LOAD_METHOD              setCompletionPrefix
              218  LOAD_FAST                'completionPrefix'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  POP_TOP          

 L. 102       224  LOAD_FAST                'self'
              226  LOAD_ATTR                completer
              228  LOAD_METHOD              popup
              230  CALL_METHOD_0         0  '0 positional arguments'
              232  LOAD_METHOD              setCurrentIndex
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                completer
              238  LOAD_METHOD              completionModel
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  LOAD_METHOD              index
              244  LOAD_CONST               0
              246  LOAD_CONST               0
              248  CALL_METHOD_2         2  '2 positional arguments'
              250  CALL_METHOD_1         1  '1 positional argument'
              252  POP_TOP          
            254_0  COME_FROM           210  '210'

 L. 104       254  LOAD_FAST                'self'
              256  LOAD_METHOD              cursorRect
              258  CALL_METHOD_0         0  '0 positional arguments'
              260  STORE_FAST               'cr'

 L. 105       262  LOAD_FAST                'cr'
              264  LOAD_METHOD              setWidth
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                completer
              270  LOAD_METHOD              popup
              272  CALL_METHOD_0         0  '0 positional arguments'
              274  LOAD_METHOD              sizeHintForColumn
              276  LOAD_CONST               0
              278  CALL_METHOD_1         1  '1 positional argument'
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                completer
              284  LOAD_METHOD              popup
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  LOAD_METHOD              verticalScrollBar
              290  CALL_METHOD_0         0  '0 positional arguments'
              292  LOAD_METHOD              sizeHint
              294  CALL_METHOD_0         0  '0 positional arguments'
              296  LOAD_METHOD              width
              298  CALL_METHOD_0         0  '0 positional arguments'
              300  BINARY_ADD       
              302  CALL_METHOD_1         1  '1 positional argument'
              304  POP_TOP          

 L. 106       306  LOAD_FAST                'self'
              308  LOAD_ATTR                completer
              310  LOAD_METHOD              complete
              312  LOAD_FAST                'cr'
              314  CALL_METHOD_1         1  '1 positional argument'
              316  POP_TOP          

Parse error at or near `CALL_METHOD_1' instruction at offset 314

    def is_special_key(self, e):
        if self.completer:
            if self.completer.popup().isVisible():
                if e.key() in (Qt.Key_Enter, Qt.Key_Return):
                    return True
        if e.key() == Qt.Key_Tab:
            return True
        return False


if __name__ == '__main__':
    app = QApplication([])
    completer = QCompleter(['alabama', 'arkansas', 'avocado', 'breakfast', 'sausage'])
    te = CompletionTextEdit()
    te.set_completer(completer)
    te.show()
    app.exec_()