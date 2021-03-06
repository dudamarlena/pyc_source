# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/lineedit.py
# Compiled at: 2020-05-03 00:26:03
# Size of source mod 2**32: 15588 bytes
"""
Module that contains classes to create different kind of line edits
"""
from __future__ import print_function, division, absolute_import
from functools import partial
from Qt.QtCore import *
from Qt.QtWidgets import *
from tpDcc.libs.qt.core import mixin, theme
from tpDcc.libs.qt.widgets import layouts, buttons, browser

@mixin.theme_mixin
class BaseLineEdit(QLineEdit, object):
    __doc__ = '\n     Basic line edit\n     '
    delayTextChanged = Signal(str)

    def __init__(self, text='', parent=None):
        super(BaseLineEdit, self).__init__(text, parent)
        self._prefix_widget = None
        self._suffix_widget = None
        self._size = self.theme_default_size()
        self._main_layout = layouts.HorizontalLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addStretch()
        self.setLayout(self._main_layout)
        self.setProperty('history', self.property('text'))
        self.setTextMargins(2, 0, 2, 0)
        self._delay_timer = QTimer()
        self._delay_timer.setInterval(500)
        self._delay_timer.setSingleShot(True)
        self._delay_timer.timeout.connect(self._on_delay_text_changed)

    def _get_size(self):
        """
        Returns the spin box height size
        :return: float
        """
        return self._size

    def _set_size(self, value):
        """
        Sets spin box height size
        :param value: float
        """
        self._size = value
        if hasattr(self._prefix_widget, 'theme_size'):
            self._prefix_widget.theme_size = self._size
        if hasattr(self._suffix_widget, 'theme_size'):
            self._suffix_widget.theme_size = self._size
        self.style().polish(self)

    theme_size = Property(int, _get_size, _set_size)

    def setText(self, text):
        self.setProperty('history', '{}\n{}'.format(self.property('history'), text))
        return super(BaseLineEdit, self).setText(text)

    def clear(self):
        self.setProperty('history', '')
        return super(BaseLineEdit, self).clear()

    def keyPressEvent(self, event):
        if event.key() not in [Qt.Key_Enter, Qt.Key_Tab]:
            if self._delay_timer.isActive():
                self._delay_timer.stop()
            self._delay_timer.start()
        super(BaseLineEdit, self).keyPressEvent(event)

    def set_delay_duration(self, ms):
        """
        Sets the delay timer duration
        :param ms: float
        """
        self._delay_timer.setInterval(ms)

    def get_prefix_widget(self):
        """
        Returns prefix widget for user to edit
        :return: QWidget
        """
        return self._prefix_widget

    def set_prefix_widget(self, widget):
        """
        Sets the edit line left start widget
        :param widget: QWidget
        :return: QWidget
        """
        if self._prefix_widget:
            index = self._main_layout.indexOf(self._prefix_widget)
            self._main_layout.takeAt(index)
            self._prefix_widget.setVisible(False)
            self._prefix_widget.deleteLater()
        widget.setProperty('combine', 'horizontal')
        widget.setProperty('position', 'left')
        if hasattr(widget, 'theme_size'):
            widget.them_size = self.theme_size
        margin = self.textMargins()
        margin.setLeft(margin.left() + widget.width())
        self.setTextMargins(margin)
        self._main_layout.insertWidget(0, widget)
        self._prefix_widget = widget
        return widget

    def get_suffix_widget(self):
        """
        Returns suffix widget for user to edit
        :return: QWidget
        """
        return self._suffix_widget

    def set_suffix_widget(self, widget):
        """
        Sets the edit line right start widget
        :param widget: QWidget
        :return: QWidget
        """
        if self._suffix_widget:
            index = self._main_layout.indexOf(self._suffix_widget)
            self._main_layout.takeAt(index)
            self._suffix_widget.setVisible(False)
            self._suffix_widget.deleteLater()
        widget.setProperty('combine', 'horizontal')
        widget.setProperty('position', 'right')
        if hasattr(widget, 'theme_size'):
            widget.them_size = self.theme_size
        margin = self.textMargins()
        margin.setRight(margin.right() + widget.width())
        self.setTextMargins(margin)
        self._main_layout.addWidget(widget)
        self._prefix_widget = widget
        return widget

    def search(self):
        """
        Adds a search icon button for line edit
        :return: self
        """
        prefix_btn = buttons.BaseToolButton().image('search').icon_only()
        suffix_btn = buttons.BaseToolButton().image('close').icon_only()
        suffix_btn.clicked.connect(self.clear)
        self.set_prefix_widget(prefix_btn)
        self.set_suffix_widget(suffix_btn)
        self.setPlaceholderText('Enter keyword to search ...')
        return self

    def search_engine(self, text='Search'):
        """
        Adds a search push button to line edit
        :param text: str
        :return: self
        """
        _suffix_btn = buttons.BaseButton(text).primary()
        _suffix_btn.clicked.connect(self.returnPressed)
        _suffix_btn.setFixedWidth(100)
        self.set_suffix_widget(_suffix_btn)
        self.setPlaceholderText('Enter keyword to search ...')
        return self

    def file(self, filters=None):
        """
        Adds a ClickBrowserFileToolButton to line edit
        :param filters:
        :return: self
        """
        _suffix_btn = browser.ClickBrowserFileToolButton()
        _suffix_btn.fileChanged.connect(self.setText)
        _suffix_btn.filters = filters
        self.textChanged.connect(_suffix_btn.set_path)
        self.set_suffix_widget(_suffix_btn)
        self.setPlaceholderText('Click button to browse files')
        return self

    def save_file(self, filters=None):
        """
        Adds a ClickSaveFileToolButton to line edit
        :param filters:
        :return: self
        """
        _suffix_button = browser.ClickSaveFileToolButton()
        _suffix_button.fileChanged.connect(self.setText)
        _suffix_button.filters = filters or list()
        self.textChanged.connect(_suffix_button.set_path)
        self.set_suffix_widget(_suffix_button)
        self.setPlaceholderText('Click button to set save file')
        return self

    def folder(self):
        """
        Adds a ClickBrowserFileToolButton to line edit
        :return: self
        """
        _suffix_btn = browser.ClickBrowserFolderToolButton()
        _suffix_btn.folderChanged.connect(self.setText)
        self.textChanged.connect(_suffix_btn.set_path)
        self.set_suffix_widget(_suffix_btn)
        self.setPlaceholderText('Click button to browse folder')
        return self

    def error(self):
        """
        Shows error in line edit with red style
        :return: self
        """

        def _on_show_detail(self):
            dlg = QTextEdit(self)
            dlg.setReadOnly(True)
            geo = QApplication.desktop().screenGeometry()
            dlg.setGeometry(geo.width() / 2, geo.height() / 2, geo.width() / 4, geo.height() / 4)
            dlg.setWindowTitle('Error Detail Information')
            dlg.setText(self.property('history'))
            dlg.setWindowFlags(Qt.Dialog)
            dlg.show()

        self.setProperty('theme_type', 'error')
        self.setReadOnly(True)
        _suffix_btn = buttons.BaseToolButton().image('delete_message').icon_only()
        _suffix_btn.clicked.connect(partial(_on_show_detail, self))
        self.set_suffix_widget(_suffix_btn)
        self.setPlaceholderText('Error information will be here ...')
        return self

    def tiny(self):
        """
        Sets line edit to tiny size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.tiny if widget_theme else theme.Theme.Sizes.TINY
        return self

    def small(self):
        """
        Sets line edit to small size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.small if widget_theme else theme.Theme.Sizes.SMALL
        return self

    def medium(self):
        """
        Sets line edit to medium size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.medium if widget_theme else theme.Theme.Sizes.MEDIUM
        return self

    def large(self):
        """
        Sets line edit to large size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.large if widget_theme else theme.Theme.Sizes.LARGE
        return self

    def huge(self):
        """
        Sets line edit to huge size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.huge if widget_theme else theme.Theme.Sizes.HUGE
        return self

    def password(self):
        """
        Sets line edit password mode
        """
        self.setEchoMode(QLineEdit.Password)
        return self

    def _on_delay_text_changed(self):
        """
        Internal callback function that is called when delay timer is completed
        """
        self.delayTextChanged.emit(self.text())


class StyledLineEdit(QLineEdit, object):
    __doc__ = "\n    Styled line edit that takes a different color if it's empty\n    "

    def __init__(self, default='', off_color=(125, 125, 125), on_color=(255, 255, 255), parent=None):
        super(StyledLineEdit, self).__init__(parent=parent)
        self._value = ''
        self._default = ''
        self._off_color = off_color
        self._on_color = on_color
        self.set_default(default)
        self.textChanged.connect(self._on_change)

    def get_value(self):
        if self.text() == self._default:
            return ''
        else:
            return self._value

    def set_value(self, value):
        self._value = value

    value = property(get_value, set_value)

    def focusInEvent(self, event):
        if self.text() == self._default:
            self.setText('')
            self.setStyleSheet(self._get_on_style())

    def focusOutEvent(self, event):
        if self.text() == '':
            self.setText(self._default)
            self.setStyleSheet(self._get_off_style())

    def set_default(self, text):
        self.setText(text)
        self._default = text
        self.setStyleSheet(self._get_off_style())

    def _get_on_style(self):
        return 'QLineEdit{color:rgb(%s, %s, %s);}' % (self._on_color[0], self._on_color[1], self._on_color[2])

    def _get_off_style(self):
        return 'QLineEdit{color:rgb(%s, %s, %s);}' % (self._off_color[0], self._off_color[1], self._off_color[2])

    def _on_change(self, text):
        if text != self._default:
            self.setStyleSheet(self._get_on_style())
            self._value = text
        else:
            self.setStyleSheet(self._get_off_style())


class ClickLineEdit(QLineEdit, object):
    __doc__ = '\n    Custom QLineEdit that becomes editable on click or double click\n    '

    def __init__(self, text, single=False, double=False, pass_through_click=True):
        super(ClickLineEdit, self).__init__(text)
        self.setReadOnly(True)
        self._editing_style = self.styleSheet()
        self._default_style = 'QLineEdit {border: 0;}'
        self.setStyleSheet(self._default_style)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        if single:
            self.mousePressEvent = self.editEvent
        else:
            if pass_through_click:
                self.mousePressEvent = self._mouse_click_pass_through
            if double:
                self.mouseDoubleClickEvent = self.editEvent
            elif pass_through_click:
                self.mousePressEvent = self._mouse_click_pass_through
        self.editingFinished.connect(self._on_edit_finished)

    def focusOutEvent(self, event):
        super(ClickLineEdit, self).focusOutEvent(event)
        self._on_edit_finished()

    def mousePressEvent(self, event):
        event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def editEvent(self, event):
        self.setStyleSheet(self._editing_style)
        self.selectAll()
        self.setReadOnly(False)
        self.setFocus()
        event.accept()

    def _mouse_click_pass_through(self, event):
        event.ignore()

    def _on_edit_finished(self):
        self.setReadOnly(True)
        self.setStyleSheet(self._default_style)
        self.deselect()


class BaseAttrLineEdit(QLineEdit, object):
    attr_type = None
    valueChanged = Signal()

    def __init__(self, parent=None):
        super(BaseAttrLineEdit, self).__init__(parent=parent)
        self.returnPressed.connect(self.update)
        self.editingFinished.connect(self.update)

    def get_value(self):
        pass

    value = property(get_value)


class FloatLineEdit(BaseAttrLineEdit, object):
    attr_type = 'float'
    valueChanged = Signal(float)

    def __init__(self, parent=None):
        super(FloatLineEdit, self).__init__(parent=parent)

    def get_value(self):
        if not self.text():
            return 0.0
        else:
            return float(self.text())

    value = property(get_value)

    def setText(self, text):
        super(FloatLineEdit, self).setText('%.2f' % float(text))

    def update(self):
        if self.text():
            self.setText(self.text())
        super(FloatLineEdit, self).update()
        self.valueChanged.emit(float(self.text()))


class IntLineEdit(QLineEdit, object):
    attr_type = 'int'
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super(IntLineEdit, self).__init__(parent=parent)

    def get_value(self):
        if not self.text():
            return 0
        else:
            return int(self.text())

    value = property(get_value)

    def setText(self, text):
        super(IntLineEdit, self).setText('%s' % int(text))

    def update(self):
        if self.text():
            self.setText(self.text())
        super(IntLineEdit, self).update()
        self.valueChanged.emit(int(self.text()))