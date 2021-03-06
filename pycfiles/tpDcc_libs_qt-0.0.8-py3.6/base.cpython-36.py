# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/core/base.py
# Compiled at: 2020-04-15 12:12:43
# Size of source mod 2**32: 12327 bytes
"""
Module that contains base functionality for Qt widgets
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from tpDcc.libs.qt.core import consts, qtutils, mixin, theme

class HorizontalLayout(QHBoxLayout, object):
    __doc__ = '\n    Custom QHBoxLayout implementation with support for 4k resolution\n    '

    def __init__(self, *args, **kwargs):
        margins = kwargs.pop('margins', (0, 0, 0, 0))
        spacing = kwargs.pop('spacing', consts.DEFAULT_SUB_WIDGET_SPACING)
        (super(HorizontalLayout, self).__init__)(*args, **kwargs)
        (self.setContentsMargins)(*(qtutils.margins_dpi_scale)(*margins))
        self.setSpacing(qtutils.dpi_scale(spacing))


class VerticalLayout(QVBoxLayout, object):
    __doc__ = '\n    Custom QVBoxLayout implementation with support for 4k resolution\n    '

    def __init__(self, *args, **kwargs):
        margins = kwargs.pop('margins', (0, 0, 0, 0))
        spacing = kwargs.pop('spacing', consts.DEFAULT_SUB_WIDGET_SPACING)
        (super(VerticalLayout, self).__init__)(*args, **kwargs)
        (self.setContentsMargins)(*(qtutils.margins_dpi_scale)(*margins))
        self.setSpacing(qtutils.dpi_scale(spacing))


class FormLayout(QFormLayout, object):
    __doc__ = '\n    Custom QFormLayout implementation with support for 4k resolution\n    '

    def __init__(self, *args, **kwargs):
        margins = kwargs.pop('margins', (0, 0, 0, 0))
        spacing = kwargs.pop('spacing', consts.DEFAULT_SUB_WIDGET_SPACING)
        (super(FormLayout, self).__init__)(*args, **kwargs)
        (self.setContentsMargins)(*(qtutils.margins_dpi_scale)(*margins))
        self.setSpacing(qtutils.dpi_scale(spacing))


class GridLayout(QGridLayout, object):
    __doc__ = '\n    Custom QGridLayout implementation with support for 4k resolution\n    '

    def __init__(self, *args, **kwargs):
        margins = kwargs.pop('margins', (0, 0, 0, 0))
        spacing = kwargs.pop('spacing', consts.DEFAULT_SUB_WIDGET_SPACING)
        column_min_width = kwargs.pop('column_min_width', None)
        column_min_width_b = kwargs.pop('column_min_width_b', None)
        vertical_spacing = kwargs.pop('vertical_spacing', None)
        horizontal_spacing = kwargs.pop('horizontal_spacing', None)
        (super(GridLayout, self).__init__)(*args, **kwargs)
        (self.setContentsMargins)(*(qtutils.margins_dpi_scale)(*margins))
        if not vertical_spacing:
            if not horizontal_spacing:
                self.setHorizontalSpacing(qtutils.dpi_scale(spacing))
                self.setVerticalSpacing(qtutils.dpi_scale(spacing))
        elif vertical_spacing:
            if not horizontal_spacing:
                self.setHorizontalSpacing(qtutils.dpi_scale(horizontal_spacing))
                self.setVerticalSpacing(qtutils.dpi_scale(vertical_spacing))
        elif horizontal_spacing:
            if not vertical_spacing:
                self.setHorizontalSpacing(qtutils.dpi_scale(horizontal_spacing))
                self.setVerticalSpacing(qtutils.dpi_scale(spacing))
        else:
            self.setHorizontalSpacing(qtutils.dpi_scale(horizontal_spacing))
            self.setVerticalSpacing(qtutils.dpi_scale(vertical_spacing))
        if column_min_width:
            self.setColumnMinimumWidth(column_min_width[0], qtutils.dpi_scale(column_min_width[1]))
        if column_min_width_b:
            self.setColumnMinimumWidth(column_min_width_b[0], qtutils.dpi_scale(column_min_width_b[1]))


@mixin.theme_mixin
@mixin.cursor_mixin
class BaseWidget(QWidget, object):
    __doc__ = '\n    Base class for all QWidgets based items\n    '
    def_use_scrollbar = False

    def __init__(self, parent=None, **kwargs):
        super(BaseWidget, self).__init__(parent=parent)
        self._size = self.theme_default_size()
        self._use_scrollbar = kwargs.get('use_scrollbar', self.def_use_scrollbar)
        self.ui()
        self.setup_signals()

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
        self.style().polish(self)

    theme_size = Property(int, _get_size, _set_size)

    def keyPressEvent(self, event):
        pass

    def mousePressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.AltModifier:
            pos = self.mapToGlobal(self.rect().topLeft())
            QWhatsThis.showText(pos, self.whatsThis())
        else:
            super(BaseWidget, self).mousePressEvent(event)

    def get_main_layout(self):
        """
        Function that generates the main layout used by the widget
        Override if necessary on new widgets
        :return: QLayout
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignTop)
        return layout

    def ui(self):
        """
        Function that sets up the ui of the widget
        Override it on new widgets (but always call super)
        """
        self.main_layout = self.get_main_layout()
        if self._use_scrollbar:
            layout = QVBoxLayout()
            self.setLayout(layout)
            central_widget = QWidget()
            central_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            scroll = QScrollArea()
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setWidgetResizable(True)
            scroll.setFocusPolicy(Qt.NoFocus)
            layout.addWidget(scroll)
            scroll.setWidget(central_widget)
            central_widget.setLayout(self.main_layout)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        else:
            self.setLayout(self.main_layout)

    def setup_signals(self):
        """
        Function that set up signals of the widget
        """
        pass

    def set_spacing(self, value):
        """
        Set the spacing used by widget's main layout
        :param value: float
        """
        self.main_layout.setSpacing(value)

    def tiny(self):
        """
        Sets spin box to tiny size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.tiny if widget_theme else theme.Theme.Sizes.TINY
        return self

    def small(self):
        """
        Sets spin box to small size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.small if widget_theme else theme.Theme.Sizes.SMALL
        return self

    def medium(self):
        """
        Sets spin box to medium size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.medium if widget_theme else theme.Theme.Sizes.MEDIUM
        return self

    def large(self):
        """
        Sets spin box to large size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.large if widget_theme else theme.Theme.Sizes.LARGE
        return self

    def huge(self):
        """
        Sets spin box to huge size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.huge if widget_theme else theme.Theme.Sizes.HUGE
        return self


class BaseFrame(QFrame, object):
    mouseReleased = Signal(object)

    def __init__(self, *args, **kwargs):
        (super(BaseFrame, self).__init__)(*args, **kwargs)

    def mouseReleaseEvent(self, event):
        self.mouseReleased.emit(event)
        return super(BaseFrame, self).mouseReleaseEvent(event)


class ContainerWidget(QWidget, object):
    __doc__ = '\n    Basic widget used a\n    '

    def __init__(self, parent=None):
        super(ContainerWidget, self).__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.containedWidget = None

    def set_contained_widget(self, widget):
        """
        Sets the current contained widget for this container
        :param widget: QWidget
        """
        self.containedWidget = widget
        if widget:
            widget.setParent(self)
            self.layout().addWidget(widget)

    def clone_and_pass_contained_widget(self):
        """
        Returns a clone of this ContainerWidget
        :return: ContainerWidget
        """
        cloned = ContainerWidget(self.parent())
        cloned.set_contained_widget(self.containedWidget)
        self.set_contained_widget(None)
        return cloned


class BaseNumberWidget(BaseWidget, object):
    valueChanged = Signal(object)

    def __init__(self, name='', parent=None):
        self._name = name
        super(BaseNumberWidget, self).__init__(parent)

    def get_main_layout(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        return main_layout

    def ui(self):
        super(BaseNumberWidget, self).ui()
        self._number_widget = self.get_number_widget()
        self._number_label = QLabel((self._name), parent=self)
        if not self._name:
            self._number_label.hide()
        self._value_label = QLabel('value', parent=self)
        self._value_label.hide()
        self.main_layout.addWidget(self._number_label)
        self.main_layout.addSpacing(5)
        self.main_layout.addWidget((self._value_label), alignment=(Qt.AlignRight))
        self.main_layout.addWidget(self._number_widget)

    def get_number_widget(self):
        """
        Returns the widget used to edit numeric value
        :return: QWidget
        """
        spin_box = QSpinBox(parent=self)
        spin_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return spin_box

    def get_value(self):
        """
        Returns the number value of the numeric widget
        :return: variant, int || float
        """
        return self._number_widget.value()

    def set_value(self, new_value):
        """
        Sets the value of the numeric widget
        :param new_value: variant, int || float
        """
        if new_value:
            self._number_widget.setValue(new_value)

    def get_label_text(self):
        return self._number_label.text()

    def set_label_text(self, new_text):
        self._number_label.setText(new_text)

    def set_value_label(self, new_value):
        self._value_label.show()
        self._value_label.setText(str(new_value))

    def _on_value_changed(self):
        self.valueChanged.emit(self.get_value())


class DirectoryWidget(BaseWidget, object):
    __doc__ = '\n    Widget that contains variables to store current working directory\n    '

    def __init__(self, parent=None, **kwargs):
        self.directory = None
        self.last_directory = None
        (super(DirectoryWidget, self).__init__)(parent=parent, **kwargs)

    def set_directory(self, directory):
        """
        Set the directory used by this widget
        :param directory: str, new directory of the widget
        """
        self.last_directory = self.directory
        self.directory = directory


class PlaceholderWidget(QWidget, object):
    __doc__ = '\n    Basic widget that loads custom UI\n    '

    def __init__(self, *args):
        (super(PlaceholderWidget, self).__init__)(*args)
        qtutils.load_widget_ui(self)