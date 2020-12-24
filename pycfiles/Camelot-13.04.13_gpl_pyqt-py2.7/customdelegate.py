# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/customdelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QItemDelegate
from camelot.core.utils import variant_to_pyobject
from camelot.core.utils import create_constant_function
from camelot.view.proxy import ValueLoading
not_editable_background = QtGui.QColor(235, 233, 237)
not_editable_foreground = QtGui.QColor(Qt.darkGray)

def DocumentationMetaclass(name, bases, dct):
    dct['__doc__'] = dct.get('__doc__', '') + '\n\n.. _delegate-%s:\n\n.. image:: /_static/delegates/%s_unselected_disabled.png\n.. image:: /_static/delegates/%s_unselected_editable.png\n\n.. image:: /_static/delegates/%s_selected_disabled.png\n.. image:: /_static/delegates/%s_selected_editable.png\n\n' % (name, name, name, name, name)
    import inspect

    def add_field_attribute_item(a):
        """Add the name of a field attribute and a reference to its documentation
        to the docstring"""
        dct['__doc__'] = dct['__doc__'] + '\n * :ref:`%s <field-attribute-%s>`' % (arg, arg)

    if '__init__' in dct:
        dct['__doc__'] = dct['__doc__'] + 'Field attributes supported by the delegate : \n'
        args, _varargs, _varkw, _defaults = inspect.getargspec(dct['__init__'])
        for arg in args:
            if arg not in ('self', 'parent'):
                add_field_attribute_item(arg)

    if 'editor' in dct:
        row_separator = '+' + '-' * 40 + '+' + '-' * 90 + '+'
        row_format = '| %-38s | %-88s |'
        states = {'editable': ['editable=True'], 'disabled': [
                      'editable=False'], 
           'editable_tooltip': [
                              'editable=True', "tooltip='tooltip'"], 
           'disabled_tooltip': [
                              'editable=False', "tooltip='tooltip'"], 
           'editable_background_color': [
                                       'editable=True', 'background_color=ColorScheme.green'], 
           'disabled_background_color': [
                                       'editable=False', 'background_color=ColorScheme.green']}
        dct['__doc__'] = dct['__doc__'] + '\n\nBy default, creates a %s as its editor.\n\n' % dct['editor'].__name__
        dct['__doc__'] = dct['__doc__'] + row_separator + '\n'
        dct['__doc__'] = dct['__doc__'] + row_format % ('**Field Attributes**', '**Editor**') + '\n'
        dct['__doc__'] = dct['__doc__'] + row_separator + '\n'
        for state, attrs in states.items():
            for i, attr in enumerate(attrs):
                if i == 0:
                    image = '.. image:: /_static/editors/%s_%s.png' % (dct['editor'].__name__, state)
                else:
                    image = ''
                dct['__doc__'] = dct['__doc__'] + row_format % (attr, image) + '\n'

            dct['__doc__'] = dct['__doc__'] + row_separator + '\n'

        dct['__doc__'] = dct['__doc__'] + '\nStatic attributes supported by this editor : \n'
        args, _varargs, _varkw, _defaults = inspect.getargspec(dct['editor'].__init__)
        for arg in args:
            if arg not in ('self', 'parent'):
                add_field_attribute_item(arg)

        if hasattr(dct['editor'], 'set_field_attributes'):
            dct['__doc__'] = dct['__doc__'] + '\n\nDynamic field attributes supported by the editor : \n'
            args, _varargs, _varkw, _defaults = inspect.getargspec(dct['editor'].set_field_attributes)
            for arg in args:
                if arg not in ('self', 'parent'):
                    add_field_attribute_item(arg)

        dct['__doc__'] = dct['__doc__'] + '\n\n'
    return type(name, bases, dct)


class CustomDelegate(QItemDelegate):
    """Base class for implementing custom delegates.

    .. attribute:: editor

    class attribute specifies the editor class that should be used

    """
    editor = None

    def __init__(self, parent=None, editable=True, **kwargs):
        """:param parent: the parent object for the delegate
        :param editable: a boolean indicating if the field associated to the delegate
        is editable

        """
        QItemDelegate.__init__(self, parent)
        self.editable = editable
        self.kwargs = kwargs
        self._font_metrics = QtGui.QFontMetrics(QtGui.QApplication.font())
        self._height = self._font_metrics.lineSpacing() + 10
        self._width = self._font_metrics.averageCharWidth() * 20

    def createEditor(self, parent, option, index):
        """
        :param option: use an option with version 5 to indicate the widget
        will be put onto a form
        """
        editor = self.editor(parent, editable=self.editable, option=option, **self.kwargs)
        assert editor != None
        assert isinstance(editor, (QtGui.QWidget,))
        if option.version != 5:
            editor.setAutoFillBackground(True)
        editor.editingFinished.connect(self.commitAndCloseEditor)
        return editor

    def sizeHint(self, option, index):
        return QtCore.QSize(self._width, self._height)

    def commitAndCloseEditor(self):
        editor = self.sender()
        assert editor != None
        assert isinstance(editor, (QtGui.QWidget,))
        self.commitData.emit(editor)
        return

    def setEditorData(self, editor, index):
        if not index.model():
            return
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        field_attributes = variant_to_pyobject(index.data(Qt.UserRole)) or dict()
        if field_attributes.get('tooltip'):
            editor.setToolTip(unicode(field_attributes.get('tooltip', '')))
        editor.set_field_attributes(**field_attributes)
        editor.set_value(value)

    def setModelData(self, editor, model, index):
        if isinstance(model, QtGui.QStandardItemModel):
            val = QtCore.QVariant(editor.get_value())
        else:
            val = create_constant_function(editor.get_value())
        model.setData(index, val)

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.DisplayRole))
        if value in (None, ValueLoading):
            value_str = ''
        else:
            value_str = unicode(value)
        self.paint_text(painter, option, index, value_str)
        painter.restore()
        return

    def paint_text(self, painter, option, index, text, margin_left=0, margin_right=0, horizontal_align=Qt.AlignLeft, vertical_align=Qt.AlignVCenter):
        """Paint unicode text into the given rect defined by option, and fill the rect with
        the background color
        :arg margin_left: additional margin to the left, to be used for icons or others
        :arg margin_right: additional margin to the right, to be used for icons or others"""
        rect = option.rect
        if rect.height() > 2 * self._height:
            vertical_align = Qt.AlignTop
        field_attributes = variant_to_pyobject(index.model().data(index, Qt.UserRole))
        tooltip = None
        if field_attributes != ValueLoading:
            editable = field_attributes.get('editable', True)
            background_color = field_attributes.get('background_color', None)
            prefix = field_attributes.get('prefix', None)
            suffix = field_attributes.get('suffix', None)
            tooltip = field_attributes.get('tooltip', None)
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            fontColor = option.palette.highlightedText().color()
        elif editable:
            painter.fillRect(rect, background_color or option.palette.base())
            fontColor = option.palette.windowText().color()
        else:
            painter.fillRect(rect, background_color or option.palette.window())
            fontColor = QtGui.QColor()
            fontColor.setRgb(130, 130, 130)
        if tooltip:
            painter.drawPixmap(rect.x(), rect.y(), QtGui.QPixmap(':/tooltip_visualization_7x7_glow.png'))
        if prefix:
            text = '%s %s' % (unicode(prefix).strip(), unicode(text).strip())
        if suffix:
            text = '%s %s' % (unicode(text).strip(), unicode(suffix).strip())
        painter.setPen(fontColor.toRgb())
        painter.drawText(rect.x() + 2 + margin_left, rect.y() + 2, rect.width() - 4 - (margin_left + margin_right), rect.height() - 4, vertical_align | horizontal_align, text)
        return