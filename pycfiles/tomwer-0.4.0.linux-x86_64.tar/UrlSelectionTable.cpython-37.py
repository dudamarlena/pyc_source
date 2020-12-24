# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/UrlSelectionTable.py
# Compiled at: 2020-02-10 09:12:42
# Size of source mod 2**32: 10381 bytes
"""Some widget construction to check if a sample moved"""
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '19/03/2018'
from silx.gui import qt
from collections import OrderedDict
import silx.gui.widgets.TableWidget as TableWidget
from silx.io.url import DataUrl
import enum, functools, logging, os
from collections import OrderedDict
logger = logging.getLogger(__file__)

class ColumnMode(enum.Enum):
    SINGLE = ('single', )
    SINGLE_OR_NONE = ('single_or_none', )
    MULTIPLE = ('multiple', )
    MULTIPLE_OR_NONE = ('multiple_or_none', )


_DEFAULT_COLUMNS = OrderedDict({
 (
  'img B', ColumnMode.SINGLE),
 (
  'img A', ColumnMode.SINGLE)})

class UrlSelectionTable(TableWidget):
    __doc__ = 'Table used to select the color channel to be displayed for each'
    sigSelectionChanged = qt.Signal(dict)

    def __init__(self, parent=None, columns=_DEFAULT_COLUMNS):
        TableWidget.__init__(self, parent)
        self.selection_columns = columns
        self.clear()

    def clear(self):
        qt.QTableWidget.clear(self)
        self.setRowCount(0)
        self._column_index = OrderedDict({'url': 0})
        for i, column in enumerate(self.selection_columns):
            self._column_index[column] = i + 1

        self.setColumnCount(len(self._column_index))
        self.setHorizontalHeaderLabels(list(self._column_index.keys()))
        self.verticalHeader().hide()
        if hasattr(self.horizontalHeader(), 'setSectionResizeMode'):
            self.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        else:
            self.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)
        self.setSortingEnabled(True)
        self._checkBoxes = {}
        self._url_path_to_url = {}

    def setUrls(self, urls):
        self.clear()
        self.setRowCount(len(urls))
        for iUrl, url in enumerate(urls):
            self.addUrl(url=url, row=iUrl, resize=False)

        self.sortItems(0)
        self.resizeColumnsToContents()

    def addUrl(self, url, row=None, resize=False, **kwargs):
        """

        :param url: 
        :param args: 
        :return: index of the created items row
        :rtype int
        """
        assert isinstance(url, DataUrl)
        if row is None:
            row = self.rowCount()
            self.setRowCount(row + 1)
        _item = qt.QTableWidgetItem()
        _item.setText(os.path.basename(url.path()))
        _item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        self.setItem(row, self._column_index['url'], _item)
        self._checkBoxes[url.path()] = {}
        self._url_path_to_url[url.path()] = url
        for column_name in self.selection_columns:
            widgetImg = qt.QRadioButton(parent=self)
            widgetImg.setAutoExclusive(False)
            self.setCellWidget(row, self._column_index[column_name], widgetImg)
            callbackImg = functools.partial(self._selection_changed, column_name, url)
            widgetImg.toggled.connect(callbackImg)
            self._checkBoxes[url.path()][column_name] = widgetImg

        if resize is True:
            self.resizeColumnsToContents()
        return row

    def _selection_changed(self, column_name, url, toggle):
        column_mode = self.selection_columns[column_name]
        if toggle is True:
            if column_mode in (
             ColumnMode.SINGLE, ColumnMode.SINGLE_OR_NONE):
                for tmp_url in self._checkBoxes:
                    for tmp_column in self._checkBoxes[tmp_url]:
                        self._checkBoxes[tmp_url][tmp_column].blockSignals(True)

                self._set_column_selection(column=column_name, selection=[url])
                for tmp_url in self._checkBoxes:
                    for tmp_column in self._checkBoxes[tmp_url]:
                        self._checkBoxes[tmp_url][tmp_column].blockSignals(False)

        if toggle is False:
            if column_mode in (ColumnMode.SINGLE, ColumnMode.MULTIPLE):
                if self._has_no_element(column_name):
                    for tmp_url in self._checkBoxes:
                        for tmp_column in self._checkBoxes[tmp_url]:
                            self._checkBoxes[tmp_url][tmp_column].blockSignals(True)

                    selection = [
                     url]
                    self._set_column_selection(column=column_name, selection=selection)
                    for tmp_url in self._checkBoxes:
                        for tmp_column in self._checkBoxes[tmp_url]:
                            self._checkBoxes[tmp_url][tmp_column].blockSignals(False)

    def _has_no_element(self, column):
        for url_path in self._checkBoxes:
            if self._checkBoxes[url_path][column].isChecked():
                return False

        return True

    def _updatecheckBoxes(self, whichImg, name):
        old = self.blockSignals(True)
        assert name in self._checkBoxes
        assert whichImg in self._checkBoxes[name]
        if self._checkBoxes[name][whichImg].isChecked():
            for radioUrl in self._checkBoxes:
                if radioUrl != name:
                    self._checkBoxes[radioUrl.path()][whichImg].setChecked(False)

        self.blockSignals(old)

    def getSelectedUrls(self, name=None):
        """

        :return: url selected for the requested name. Or full selection if no
                 name selected.
        """
        selection = {}
        for _name in self.selection_columns:
            selection[_name] = None

        for radioUrl in self._checkBoxes:
            for _name in self.selection_columns:
                if self._checkBoxes[radioUrl][_name].isChecked():
                    if selection[_name] is None:
                        selection[_name] = []
                    selection[_name].append(self._url_path_to_url[radioUrl])

        if name is None:
            return selection
        return selection[name]

    def setSelectedUrls(self, selection):
        """

        :param ddict: key: image url, values: list of active channels
        """
        assert isinstance(selection, dict)
        for name, sel in selection.items():
            assert isinstance(sel, (type(None), list, tuple))
            self._set_column_selection(column=name, selection=sel)

        self._signal_selection_changed()

    def _clear_column(self, column):
        """

        :param str column: 
        """
        old = self.blockSignals(True)
        for radioUrl in self._checkBoxes:
            self._checkBoxes[radioUrl][column].setChecked(False)

        self.blockSignals(old)

    def _set_column_selection(self, column, selection):
        """

        :param str column: id of the column
        :param Union[None, list]: None or list of DataUrl
        """
        self._clear_column(column=column)
        old = self.blockSignals(True)
        if selection is not None:
            assert isinstance(selection, (list, tuple))
            for sel in selection:
                if sel is not None:
                    assert isinstance(sel, DataUrl)
                    self._checkBoxes[sel.path()][column].setChecked(True)

        self.blockSignals(old)

    def _signal_selection_changed(self):
        self.sigSelectionChanged.emit(self.getSelectedUrls())

    def removeUrl(self, url):
        raise NotImplementedError('')


class UrlSelectionDialog(qt.QDialog):
    __doc__ = 'Embed the UrlSelectionWidget into a QDialog'
    _sizeHint = qt.QSize(500, 500)

    def __init__(self, columns, parent=None):
        qt.QDialog.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self.widget = UrlSelectionTable(columns=columns, parent=self)
        self.layout().addWidget(self.widget)
        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._buttons.button(qt.QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.setUrls = self.widget.setUrls
        self.addUrl = self.widget.addUrl
        self.setSelection = self.widget.setSelectedUrls
        self.getSelection = self.widget.getSelectedUrls

    def sizeHint(self):
        """Return a reasonable default size for usage in :class:`PlotWindow`"""
        return self._sizeHint