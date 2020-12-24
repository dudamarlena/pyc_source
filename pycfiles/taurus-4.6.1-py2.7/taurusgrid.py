# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/table/taurusgrid.py
# Compiled at: 2019-08-19 15:09:30
"""
taurusgrid.py: module containing the Taurus Widget: TaurusGrid
original idea and development by gcuni
integrated with taurus and regular expressions by srubio
alba, 2009
"""
from __future__ import print_function
from future.utils import string_types
from future import standard_library
standard_library.install_aliases()
from builtins import str
__all__ = [
 'TaurusGrid']
__docformat__ = 'restructuredtext'
import re
from queue import Queue
from taurus.external.qt import Qt, QtGui, QtCore
import taurus
from taurus.qt.qtcore.util.emitter import modelSetter, SingletonWorker, MethodModel
from taurus.core.taurusmanager import TaurusManager
from taurus.qt.qtgui.base import TaurusBaseWidget
from taurus.qt.qtgui.panel import TaurusValue
metachars = re.compile('([.][*])|([.][^*])|([$^+\\-?{}\\[\\]|()])')

def re_search_low(regexp, target):
    return re.search(regexp.lower(), target.lower())


def re_match_low(regexp, target):
    return re.match(regexp.lower(), target.lower())


def get_all_models(expressions, limit=1000):
    """
    All devices matching expressions must be obtained.
    For each device only the good attributes are read.

    It practically equals to fandango.get_matching_attributes; check which is better!
    Move this method to taurus.core.tango.search
    """
    if isinstance(expressions, string_types):
        expressions = expressions.split(',')
    else:
        if isinstance(expressions, (list, tuple, dict)):
            expressions = list(str(e) for e in expressions)
        taurus_db = taurus.Authority()
        if 'SimulationAuthority' in str(type(taurus_db)):
            models = expressions
        else:
            all_devs = taurus_db.get_device_exported('*')
            models = []
            for exp in expressions:
                exp = str(exp)
                devs = []
                targets = []
                if exp.count('/') == 3:
                    device, attribute = exp.rsplit('/', 1)
                else:
                    device, attribute = exp, 'State'
                if any(c in device for c in '.*[]()+?'):
                    if '*' in device and '.*' not in device:
                        device = device.replace('*', '.*')
                    devs = [ s for s in all_devs if re_match_low(device, s) ]
                else:
                    devs = [
                     device]
                for dev in devs:
                    if any(c in attribute for c in '.*[]()+?'):
                        if '*' in attribute and '.*' not in attribute:
                            attribute = attribute.replace('*', '.*')
                        try:
                            taurus_dp = taurus.core.taurusmanager.TaurusManager().getFactory()().getDevice(dev)
                            attrs = [ att.name for att in taurus_dp.attribute_list_query() if re_match_low(attribute, att.name)
                                    ]
                            targets.extend(dev + '/' + att for att in attrs)
                        except Exception as e:
                            pass

                    else:
                        targets.append(dev + '/' + attribute)

                models.extend(targets)

    models = models[:limit]
    return models


def get_readwrite_models(expressions, limit=1000):
    """
    All devices matching expressions must be obtained.
    For each device only the good attributes are read.
    """
    if isinstance(expressions, string_types):
        if any(re.match(s, expressions) for s in ('\\{.*\\}', '\\(.*\\)', '\\[.*\\]')):
            expressions = list(eval(expressions))
        else:
            expressions = expressions.split(',')
    else:
        if isinstance(expressions, (list, tuple, dict)):
            expressions = list(str(e) for e in expressions)
        taurus_db = taurus.Authority()
        if 'SimulationAuthority' in str(type(taurus_db)):
            models = expressions
        else:
            all_devs = taurus_db.get_device_exported('*')
            models = []
            for exp in expressions:
                exp = str(exp)
                devs = []
                targets = []
                if exp.count('/') == 3:
                    device, attribute = exp.rsplit('/', 1)
                else:
                    device, attribute = exp, 'State'
                if any(c in device for c in '.*[]()+?'):
                    if '*' in device and '.*' not in device:
                        device = device.replace('*', '.*')
                    devs = [ s for s in all_devs if re_match_low(device, s) ]
                else:
                    devs = [
                     device]
                for dev in devs:
                    if any(c in attribute for c in '.*[]()+?'):
                        if '*' in attribute and '.*' not in attribute:
                            attribute = attribute.replace('*', '.*')
                        try:
                            taurus_dp = taurus.core.taurusmanager.TaurusManager().getFactory()().getDevice(dev)
                            attrs = [ att.name for att in taurus_dp.attribute_list_query() if re_match_low(attribute, att.name) and att.isReadOnly()
                                    ]
                            targets.extend(dev + '/' + att for att in attrs)
                        except Exception as e:
                            pass

                    else:
                        targets.append(dev + '/' + attribute)

                models.extend(targets)

    models = models[:limit]
    return models


class TaurusGrid(QtGui.QFrame, TaurusBaseWidget):
    """ TaurusGrid is a Taurus widget designed to represent a set of attributes distributed in columns and rows.
    The Model will be a list with attributes or device names (for devices the State attribute will be shown).
    Each setModel(*) execution will be able to modify the attribute list.
    An example of execution:<pre>
    /usr/bin/python taurusgrid.py "model=lt.*/VC.*/.*/((C*)|(P*)|(I*))" cols=IP,CCG,PNV rows=LT01,LT02
    </pre>
    @author originally developed by gcuni, extended by srubio and sblanch
    @todo Future releases should allow a list of filters as argument
    @todo names/widgets should be accessible as a caselessdict dictionary (e.g. for adding custom context menus)
    @todo refactoring to have methods that add/remove new widgets one by one, not only the whole dictionary
    @todo _TAGS property should allow to change row/columns meaning and also add new Custom tags based on regexp
    """
    itemSelected = Qt.pyqtSignal('QString')
    itemClicked = Qt.pyqtSignal('QString')
    _TAGS = [
     'DOMAIN', 'FAMILY', 'HOST',
     'LEVEL', 'CLASS', 'ATTRIBUTE', 'DEVICE']

    class _TaurusGridCell(Qt.QFrame):
        itemClicked = Qt.pyqtSignal('QString')

        def mousePressEvent(self, event):
            targets = set(str(child.getModelName()) for child in self.children() if hasattr(child, 'underMouse') and child.underMouse() and hasattr(child, 'getModelName'))
            for t in targets:
                self.itemClicked.emit(t)

    def __init__(self, parent=None, designMode=False):
        name = self.__class__.__name__
        self.call__init__wo_kw(QtGui.QFrame, parent)
        if isinstance(parent, TaurusBaseWidget):
            self.call__init__(TaurusBaseWidget, name, parent, designMode=designMode)
        else:
            self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        self.title = ''
        self.showLabels = True
        self.filter = ''
        self._modelNames = []
        self.row_labels = []
        self.column_labels = []
        self._widgets_list = []
        self._last_selected = None
        self._show_frames = True
        self._show_row_frame = True
        self._show_column_frame = True
        self._show_others = False
        self._show_attr_labels = True
        self._show_attr_units = True
        self.hideLabels = False
        self.defineStyle()
        self.modelsQueue = Queue()
        self.__modelsThread = None
        if not designMode:
            self.modelsThread
        return

    @property
    def modelsThread(self):
        modelsThread = self.__modelsThread
        if modelsThread is None:
            modelsThread = SingletonWorker(parent=self, name='TaurusGrid', queue=self.modelsQueue, method=modelSetter, cursor=True)
            self.__modelsThread = modelsThread
        return modelsThread

    def save(self, filename):
        import pickle
        d = {'model': self.filter, 
           'row_labels': self.row_labels, 
           'column_labels': self.column_labels, 'frames': self._show_row_frame or self._show_column_frame, 
           'labels': self._show_attr_labels, 
           'units': self._show_attr_units, 
           'others': self._show_others}
        f = open(filename, 'wb')
        pickle.dump(d, f)
        f.close()

    def load(self, filename, delayed=False):
        self.trace('In TauGrid.load(%s,%s)' % (filename, delayed))
        if not isinstance(filename, dict):
            manual = False
            import pickle
            f = open(filename, 'rb')
            d = pickle.load(f)
            f.close()
        else:
            manual = True
            d = filename
        self.setRowLabels(d['row_labels'])
        self.setColumnLabels(d['column_labels'])
        self.showAttributeLabels(d.get('labels', True))
        self.showAttributeUnits(d.get('units', True))
        self.showOthers(d.get('others', True))
        self.showRowFrame(d.get('frames', True))
        if manual:
            self.showColumnFrame(d.get('frames', True))
        self.setModel(d['model'], delayed=d.get('delayed', delayed))
        return self._modelNames

    def defineStyle(self):
        """ Defines the initial style for the widget """
        self.setLayout(QtGui.QGridLayout())
        self.updateStyle()

    def sizeHint(self):
        return QtGui.QFrame.sizeHint(self)

    def minimumSizeHint(self):
        return QtGui.QFrame.minimumSizeHint(self)

    def getModelClass(self):
        raise RuntimeError('Forgot to overwrite %s.getModelClass' % str(self))
        return list

    def attach(self):
        """Attaches the widget to the model"""
        if self.isAttached():
            return True
        ret = TaurusBaseWidget.attach(self)
        self.setEnabled(ret)
        return ret

    def detach(self):
        """Detaches the widget from the model"""
        TaurusBaseWidget.detach(self)
        self.setEnabled(False)

    def updateStyle(self):
        self.trace('@' * 80)
        self.trace('In TaurusGrid.updateStyle() ....... It seems never called!!!!')
        self.trace('@' * 80)
        self.setToolTip(self.getFormatedToolTip())
        if hasattr(self, 'title_widget'):
            if self.title:
                self.title_widget.show()
            else:
                self.title_widget.hide()
        self.update()

    def setModel(self, model, devsInRows=False, delayed=False, append=False, load=True):
        """The model can be initialized as a list of devices or hosts or dictionary or ..."""
        if isinstance(model, dict):
            self.load(model)
        else:
            model = isinstance(model, string_types) and [model] or list(model)
            self.trace('#' * 80)
            self.trace('In TaurusGrid.setModel(%s)' % str(model)[:100])
            self.delayed = delayed
            self.filter = model
            if any('*' in m for m in model):
                model = get_all_models(model)
                self.debug('model was a RegExp, done the query and converted to an attr list')
            if not self._modelNames == []:
                for widget in self._widgets_list:
                    del widget

            if append:
                self._modelNames = self._modelNames + model
            else:
                self._modelNames = model
            self.debug(('In TaurusGrid.setModel(...): modelNames are %s' % self._modelNames)[:100] + '...')
            if load:
                self.trace('In TaurusGrid.setModel(%s,load=True): modelNames are %d' % (
                 str(model)[:100] + '...',
                 len(self._modelNames)))
                if devsInRows:
                    self.setRowLabels((',').join(set(d.rsplit('/', 1)[0] for d in self._modelNames)))
                self.create_widgets_table(self._modelNames)
                self.modelsQueue.put((
                 MethodModel(self.showRowFrame), self._show_row_frame))
                self.modelsQueue.put((
                 MethodModel(self.showColumnFrame), self._show_column_frame))
                self.modelsQueue.put((
                 MethodModel(self.showOthers), self._show_others))
                self.modelsQueue.put((
                 MethodModel(self.showAttributeLabels),
                 self._show_attr_labels))
                self.modelsQueue.put((
                 MethodModel(self.showAttributeUnits),
                 self._show_attr_units))
                self.updateStyle()
                if not self.delayed:
                    self.trace('In setModel(): not delayed loading of models')
                    if not self.modelsThread.isRunning():
                        self.trace('<' * 80)
                        self.modelsThread.start()
                    else:
                        self.modelsThread.next()
                else:
                    self.trace('In setModel(): models loading delayed!')
            self.trace('Out of TaurusGrid.setModel(%s)' % str(model)[:100])
            self.updateStyle()

    def getModel(self):
        return self._modelNames

    def resetModel(self):
        self._modelNames = []
        self.updateFromList(self._modelNames)

    def setTitle(self, title):
        self.title = str(title)
        if hasattr(self, 'title_widget'):
            if title:
                self.title_widget.setText(self.title)
                self.title_widget.show()
            else:
                self.title_widget.hide()

    def parse_labels(self, text):
        if any(text.startswith(c[0]) and text.endswith(c[1]) for c in [
         ('{', '}'), ('(', ')'), ('[', ']')]):
            try:
                labels = eval(text)
                return labels
            except Exception as e:
                self.warning('ERROR! Unable to parse labels property: %s' % str(e))
                return []

        else:
            exprs = [ t.strip() for t in text.split(',') ]
            labels = [ ':' in e and (e.split(':', 1)[0].strip(), e.split(':', 1)[(-1)].strip()) or (e, e) for e in exprs
                     ]
            return labels

    def setRowLabels(self, rows):
        """The model can be initialized as a list of devices or hosts or ..."""
        self.row_labels = self.parse_labels(str(rows))
        try:
            self.rows = [ r[0] for r in self.row_labels ]
            for i in range(len(self.rows)):
                section = self.rows[i]
                self.table.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(section))

        except Exception as e:
            self.debug('setRowLabels(): Exception! %s' % e)

    def getRowLabels(self):
        return (',').join((':').join(c) for c in self.row_labels)

    def resetRowLabels(self):
        self.row_labels = []

    def setColumnLabels(self, columns):
        """The model can be initialized as a list of devices or hosts or ..."""
        self.column_labels = self.parse_labels(str(columns))
        try:
            self.columns = [ c[0] for c in self.column_labels ]
            for i in range(len(self.columns)):
                equipment = self.columns[i]
                self.table.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(equipment))

        except Exception as e:
            self.debug('setColumnLabels(): Exception! %s' % e)

    def getColumnLabels(self):
        return (',').join((':').join(c) for c in self.column_labels)

    def resetColumnLabels(self):
        self.column_labels = []

    def showRowFrame(self, boolean):
        self._show_row_frame = boolean
        if hasattr(self, 'rows_frame'):
            if boolean:
                self.rows_frame.show()
            else:
                self.rows_frame.hide()

    def showColumnFrame(self, boolean):
        self._show_column_frame = boolean
        if hasattr(self, 'columns_frame'):
            if boolean:
                self.columns_frame.show()
            else:
                self.columns_frame.hide()

    def showAttributeLabels(self, boolean):
        self.trace('In showAttributeLabels(%s)' % boolean)
        self._show_attr_labels = boolean
        for tv in self._widgets_list:
            try:
                if tv and tv.labelWidget:
                    if boolean:
                        tv.labelWidget().show()
                    else:
                        tv.labelWidget().hide()
            except:
                pass

        return self._show_attr_labels

    def showAttributeUnits(self, boolean):
        self.trace('In showAttributeUnits(%s)' % boolean)
        self._show_attr_units = boolean
        for tv in self._widgets_list:
            try:
                if tv and tv.unitsWidget:
                    if boolean:
                        tv.unitsWidget().show()
                    else:
                        tv.unitsWidget().hide()
            except:
                pass

        return self._show_attr_units

    model = QtCore.pyqtProperty('QStringList', getModel, setModel, resetModel)
    rowlabels = QtCore.pyqtProperty('QString', getRowLabels, setRowLabels, resetRowLabels)
    columnlabels = QtCore.pyqtProperty('QString', getColumnLabels, setColumnLabels, resetColumnLabels)
    useParentModel = QtCore.pyqtProperty('bool', TaurusBaseWidget.getUseParentModel, TaurusBaseWidget.setUseParentModel, TaurusBaseWidget.resetUseParentModel)

    def create_widgets_dict(self, models):
        from collections import defaultdict
        values = defaultdict(lambda : defaultdict(list))
        if not self.row_labels:
            self.row_labels = sorted(list(set(m.split('/')[0].upper() for m in models if m.count('/') >= 2)))
            self.row_labels = list(zip(self.row_labels, self.row_labels))
        if not self.column_labels:
            self.column_labels = sorted(list(set(m.split('/')[1].upper() for m in models if m.count('/') >= 2)))
            self.column_labels = list(zip(self.column_labels, self.column_labels))
        row_not_found, col_not_found = False, False
        for m in models:
            row, column = ('Others', 'Others')
            for label, rexp in self.row_labels:
                if '*' in rexp and '.*' not in rexp:
                    rexp = rexp.replace('*', '.*')
                if re_search_low(rexp, m):
                    row = label
                    break

            for label, rexp in self.column_labels:
                if '*' in rexp and '.*' not in rexp:
                    rexp = rexp.replace('*', '.*')
                if re_search_low(rexp, m):
                    column = label
                    break

            if 'Others' == row:
                row_not_found = True
            if 'Others' == column:
                col_not_found = True
            self.debug('Model %s added to row %s , column %s' % (
             m, row, column))
            values[row][column].append(m)

        if row_not_found:
            self.row_labels.append(('Others', '.*'))
        if col_not_found:
            self.column_labels.append(('Others', '.*'))
        return values

    def create_frame_with_gridlayout(self):
        """ Just a 'macro' to create the layouts that seem to fit better. """
        frame = TaurusGrid._TaurusGridCell()
        frame.setLayout(QtGui.QGridLayout())
        frame.layout().setContentsMargins(2, 2, 2, 2)
        frame.layout().setSpacing(0)
        frame.layout().setSpacing(0)
        return frame

    def create_widgets_table(self, models):
        self.title_widget = QtGui.QLabel()
        self.layout().addWidget(self.title_widget, 0, 0)
        self.setTitle(self.title)
        dct = self.create_widgets_dict(models)
        self.rows = [ r[0] for r in self.row_labels ]
        self.columns = [ c[0] for c in self.column_labels ]
        values = []
        for row in self.rows:
            line = []
            for col in self.columns:
                if col in dct[row]:
                    line.append(dct[row][col])
                else:
                    line.append([])

            values.append(line)

        self.table = self.build_table(values)
        for i in range(len(self.columns)):
            equipment = self.columns[i]
            self.table.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(equipment))

        for i in range(len(self.rows)):
            section = self.rows[i]
            self.table.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(section))

        use_scroll = False
        if use_scroll:
            scrollable = QtGui.QScrollArea(self)
            scrollable.setWidget(self.table)
            self.layout().addWidget(scrollable, 1, 0)
        else:
            self.layout().addWidget(self.table, 1, 0)
        self.checkboxes_frame = self.create_frame_with_gridlayout()
        self.rows_frame = self.create_frame_with_gridlayout()
        self.rows_frame.setFrameStyle(QtGui.QFrame.Box)
        if not self._show_row_frame:
            self.rows_frame.hide()
        self.checkboxes_frame.layout().addWidget(self.rows_frame, 0, 0)
        self.columns_frame = self.create_frame_with_gridlayout()
        self.columns_frame.setFrameStyle(QtGui.QFrame.Box)
        if not self._show_column_frame:
            self.columns_frame.hide()
        self.checkboxes_frame.layout().addWidget(self.columns_frame, 0, 1)
        layout_row = 0
        layout_col = 0
        for i in range(len(self.rows)):
            section = self.rows[i]
            checkbox = QtGui.QCheckBox(section)
            checkbox._id = section
            if section == 'Others':
                checkbox.setChecked(False)
                if not self._show_others:
                    checkbox.hide()
            else:
                checkbox.setChecked(True)
            self.rows_frame.layout().addWidget(checkbox, layout_row, layout_col)
            layout_col += 1
            if layout_col == 3:
                layout_col = 0
                layout_row += 1
            checkbox.toggled.connect(self.show_hide_rows)

        self.show_hide_rows()
        layout_row = 0
        layout_col = 0
        for i in range(len(self.columns)):
            column = self.columns[i]
            checkbox = QtGui.QCheckBox(column)
            checkbox._id = column
            if column == 'Others':
                checkbox.setChecked(False)
                if not self._show_others:
                    checkbox.hide()
            else:
                checkbox.setChecked(True)
            self.columns_frame.layout().addWidget(checkbox, layout_row, layout_col)
            layout_col += 1
            if layout_col == 3:
                layout_col = 0
                layout_row += 1
            checkbox.toggled.connect(self.show_hide_columns)

        self.show_hide_columns()
        self.layout().addWidget(self.checkboxes_frame, 2, 0)

    def show_hide_rows(self):
        """
        This needs refactoring to be together with the show_hide_columns method
        """
        for checkbox in self.rows_frame.children():
            if isinstance(checkbox, QtGui.QCheckBox):
                table_row = self.rows.index(checkbox._id)
                if checkbox.isChecked():
                    self.table.showRow(table_row)
                else:
                    self.table.hideRow(table_row)

    def show_hide_columns(self):
        """
        This needs refactoring to be together with the show_hide_rows method
        """
        for checkbox in self.columns_frame.children():
            if isinstance(checkbox, QtGui.QCheckBox):
                table_col = self.columns.index(checkbox._id)
                if checkbox.isChecked():
                    self.table.showColumn(table_col)
                else:
                    self.table.hideColumn(table_col)

    def showOthers(self, boolean):
        self._show_others = boolean
        if hasattr(self, 'rows_frame'):
            for checkbox in self.rows_frame.children():
                if isinstance(checkbox, QtGui.QCheckBox) and checkbox._id == 'Others':
                    if self._show_others:
                        checkbox.show()
                    else:
                        checkbox.hide()

        if hasattr(self, 'columns_frame'):
            for checkbox in self.columns_frame.children():
                if isinstance(checkbox, QtGui.QCheckBox) and checkbox._id == 'Others':
                    if self._show_others:
                        checkbox.show()
                    else:
                        checkbox.hide()

    def build_table(self, values):
        """
        This is a builder. For all the elements in widgets matrix,
        just set the corresponding cells of the QTableWidget.
        """
        self.trace('In TaurusGrid.build_table(%s)' % values)
        widgets_matrix = self.build_widgets(values, self.showLabels)
        rows = len(widgets_matrix)
        cols = rows and len(widgets_matrix[0]) or 0
        table = QtGui.QTableWidget()
        table.setItemDelegate(Delegate(table))
        palette = Qt.QPalette()
        palette.setBrush(palette.Active, palette.Highlight, Qt.QBrush(Qt.Qt.white))
        table.setPalette(palette)
        table.setRowCount(rows)
        table.setColumnCount(cols)
        for row in range(len(widgets_matrix)):
            for col in range(len(widgets_matrix[row])):
                table.setCellWidget(row, col, widgets_matrix[row][col])

        hh = table.horizontalHeader()
        if hh.length() > 0:
            try:
                hh.setSectionResizeMode(hh.Stretch)
            except AttributeError:
                hh.setResizeMode(hh.Stretch)

        vh = table.verticalHeader()
        if vh.length() > 0:
            try:
                vh.setSectionResizeMode(vh.ResizeToContents)
            except AttributeError:
                hh.setResizeMode(vh.ResizeToContents)

        return table

    def build_widgets(self, values, show_labels=False, width=240, height=20, value_width=120):
        widgets_matrix = []
        for row in values:
            widgets_row = []
            for cell in row:
                cell_frame = self.create_frame_with_gridlayout()
                cell_frame.itemClicked.connect(self.onItemClicked)
                count = 0
                for synoptic in sorted(cell):
                    self.debug('processing synoptic %s' % synoptic)
                    name = model = synoptic
                    self.debug('Creating TaurusValue with model =  %s' % model)
                    synoptic_value = TaurusValue(cell_frame)
                    self.modelsQueue.put((synoptic_value, model))
                    if self.hideLabels:
                        synoptic_value.setLabelWidgetClass(None)
                    else:
                        synoptic_value.setLabelConfig('label')
                    cell_frame.layout().addWidget(synoptic_value, count, 0)
                    self._widgets_list.append(synoptic_value)
                    count += 1

                widgets_row.append(cell_frame)

            widgets_matrix.append(widgets_row)

        return widgets_matrix

    def onItemClicked(self, item_name):
        self.trace('In TaurusGrid.itemClicked(%s)' % item_name)
        self.setItemSelected(item_name)
        self.itemClicked.emit(str(item_name))

    def setItemSelected(self, item_name='', selected=True):
        """ it adds a blue frame around a clicked item. """
        if isinstance(item_name, TaurusValue):
            self.trace('In TaurusGrid.setItemSelected(%s,%s)' % (
             str(item_name.getModel()), selected))
            item = item_name
        else:
            self.trace('In TaurusGrid.setItemSelected(%s,%s)' % (
             str(item_name), selected))
            if item_name:
                item = self.getItemByModel(item_name)
            else:
                item = self._last_selected
        if item:
            if selected:
                item._labelWidget.setStyleSheet('border-style: solid ; border-width: 1px; border-color: blue; color: blue; border-radius:4px;')
                if self._last_selected and self._last_selected != item:
                    self.setItemSelected(self._last_selected, False)
                self._last_selected = item
            else:
                item._labelWidget.setStyleSheet('border-style: solid; border-width: 1px; border-color: transparent; color: black;  border-radius:4px;')
                self._last_selected = None
        else:
            return
        return

    def getItemByModel(self, model, index=0):
        model = str(model).lower()
        for widget in self._widgets_list:
            if str(widget.getModel()).lower() == model:
                if index <= 0:
                    return widget
                index -= 1

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.table'
        ret['group'] = 'Taurus Views'
        ret['icon'] = 'designer:grid.png'
        return ret


class Delegate(QtGui.QItemDelegate):

    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)

    def sizeHint(self, option, index):
        table = self.parent()
        widget = table.cellWidget(index.row(), index.column())
        size = widget.sizeHint()
        return size


def sysargs_to_dict(defaults=[]):
    import sys
    i, result = 0, {}
    for a in sys.argv[1:]:
        if '=' in a:
            bar = a.split('=')
            if bar[1] in ('True', 'False'):
                bar[1] = eval(bar[1])
            result[bar[0].replace('--', '')] = bar[1]
        else:
            result[defaults[i]] = a
            i += 1

    return result


if __name__ == '__main__':
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    if len(sys.argv) < 2:
        print('The format of the call is something like:')
        print('\t/usr/bin/python taurusgrid.py grid.pickle.file')
        print('\t/usr/bin/python taurusgrid.py "model=lt.*/VC.*/.*/((C*)|(P*)|(I*))" cols=IP,CCG,PNV rows=LT01,LT02 others=False rowframe=True colframe=False')
        exit()
    app = TaurusApplication(sys.argv[0:1], cmd_line_parser=None)
    gui = TaurusGrid()
    try:
        filename = sys.argv[1]
        open(filename, 'r')
        gui.load(filename)
    except:
        args = sysargs_to_dict([
         'model', 'rows', 'cols', 'others', 'rowframe', 'colframe'])
        print('args = %s' % args)
        if args.get('rows'):
            gui.setRowLabels(args['rows'])
        if args.get('cols'):
            gui.setColumnLabels(args['cols'])
        if args.get('model'):
            gui.setModel(args['model'])
        gui.showRowFrame('rowframe' in args and args['rowframe'] and True)
        gui.showColumnFrame('colframe' in args and args['colframe'] and True)
        gui.showOthers('others' in args and args['others'] or True)

    print('current TaurusGrid model= %s' % gui.getModel())
    gui.show()
    sys.exit(app.exec_())