# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/ui/status_manager.py
# Compiled at: 2012-10-20 09:01:05
import os, sys, logging
from sqlalchemy.sql.expression import distinct, func
import oyProjectManager
from oyProjectManager import config, db, utils
from oyProjectManager.models.asset import Asset
from oyProjectManager.models.project import Project
from oyProjectManager.models.sequence import Sequence
from oyProjectManager.models.shot import Shot
from oyProjectManager.models.version import Version, VersionType
logger = logging.getLogger('beaker.container')
logger.setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
conf = config.Config()
qt_module_key = 'PREFERRED_QT_MODULE'
qt_module = 'PyQt4'
if os.environ.has_key(qt_module_key):
    qt_module = os.environ[qt_module_key]
if qt_module == 'PySide':
    from PySide import QtGui, QtCore
    from oyProjectManager.ui import status_manager_UI_pyside as status_manager_UI
elif qt_module == 'PyQt4':
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtGui, QtCore
    from oyProjectManager.ui import status_manager_UI_pyqt4 as status_manager_UI

def UI():
    """the UI to call the dialog by itself
    """
    global app
    global mainDialog
    self_quit = False
    if QtGui.QApplication.instance() is None:
        try:
            app = QtGui.QApplication(sys.argv)
        except AttributeError:
            app = QtGui.QApplication([])

        self_quit = True
    else:
        app = QtGui.QApplication.instance()
    mainDialog = MainDialog()
    mainDialog.show()
    app.exec_()
    if self_quit:
        app.connect(app, QtCore.SIGNAL('lastWindowClosed()'), app, QtCore.SLOT('quit()'))
    return mainDialog


class MainDialog(QtGui.QDialog, status_manager_UI.Ui_Dialog):
    """Lets the users to view the status of the assets and shots in one place
    """

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        if db.session is None:
            db.setup()
        self.setWindowTitle('Status Manager | ' + 'oyProjectManager v' + oyProjectManager.__version__)
        self.projects_comboBox.projects = []
        self.setup_signals()
        self.setup_defaults()
        return

    def setup_signals(self):
        """sets the signals up
        """
        QtCore.QObject.connect(self.close_pushButton, QtCore.SIGNAL('clicked()'), self.close)
        QtCore.QObject.connect(self.projects_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.project_changed)
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL('currentChanged(int)'), self.tabWidget_changed)
        self.assets_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self.assets_tableWidget, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self._show_assets_tableWidget_context_menu)
        self.shots_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self.shots_tableWidget, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self._show_shots_tableWidget_context_menu)

    def setup_defaults(self):
        """sets the defaults
        """
        projects = Project.query().filter(Project.active == True).order_by(Project.name).all()
        self.projects_comboBox.addItems(map(lambda x: x.name, projects))
        self.projects_comboBox.projects = projects
        self.projects_comboBox.setCurrentIndex(0)
        self.project_changed()
        self.fill_assets_tableWidget()

    def get_current_project(self):
        """Returns the currently selected project instance in the
        projects_comboBox
        :return: :class:`~oyProjectManager.models.project.Project` instance
        """
        index = self.projects_comboBox.currentIndex()
        try:
            return self.projects_comboBox.projects[index]
        except IndexError:
            return

        return

    def project_changed(self):
        """runs when selection in projects_comboBox changed
        """
        project = self.get_current_project()
        if project:
            self.client_name_label.setText(project.client.name if project.client else 'N/A')
        self.tabWidget_changed()

    def tabWidget_changed(self):
        if self.tabWidget.currentIndex():
            self.fill_shots_tableWidget()
        else:
            self.fill_assets_tableWidget()

    def fill_assets_tableWidget(self):
        """fills the asset_tableWidget
        """
        self.assets_tableWidget.clear()
        asset_vtypes = VersionType.query().filter(VersionType.type_for == 'Asset').order_by(VersionType.name).all()
        asset_vtype_codes = map(lambda x: x.code, asset_vtypes)
        labels = [
         'Thumbnail', 'Type', 'Name', 'Take']
        labels.extend(map(lambda x: x.code, asset_vtypes))
        logger.debug('asset_tableWidget.labels: %s' % labels)
        self.assets_tableWidget.setColumnCount(len(labels))
        self.assets_tableWidget.setHorizontalHeaderLabels(labels)
        project = self.get_current_project()
        if project is None:
            return
        else:
            assets = Asset.query().filter(Asset.project == project).order_by(Asset.type).all()
            items = []
            row = 0
            column = 0
            for asset in assets:
                take_names = map(lambda x: x[0], db.query(distinct(Version.take_name)).filter(Version.version_of == asset).all())
                if not len(take_names):
                    take_names = [
                     '-']
                for take_name in take_names:
                    column = 0
                    item = QtGui.QTableWidgetItem()
                    item.setTextAlignment(132)
                    if os.path.exists(asset.thumbnail_full_path):
                        thumbnail_full_path = asset.thumbnail_full_path
                        pixmap = QtGui.QPixmap(thumbnail_full_path)
                        pixmap = pixmap.scaled(conf.thumbnail_size[0] / 2, conf.thumbnail_size[1] / 2, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                        brush = QtGui.QBrush(pixmap)
                        item.has_thumbnail = True
                        item.setBackground(brush)
                    else:
                        item.has_thumbnail = False
                    items.append(item)
                    column = 1
                    item = QtGui.QTableWidgetItem(asset.type)
                    item.setTextAlignment(132)
                    items.append(item)
                    column = 2
                    item = QtGui.QTableWidgetItem(asset.name)
                    item.setTextAlignment(132)
                    items.append(item)
                    column = 3
                    item = QtGui.QTableWidgetItem(take_name)
                    item.setTextAlignment(132)
                    items.append(item)
                    for type_code in asset_vtype_codes:
                        column += 1
                        version = Version.query().join(VersionType).filter(Version.version_of == asset).filter(Version.type_id == VersionType.id).filter(VersionType.code == type_code).filter(Version.take_name == take_name).order_by(Version.version_number.desc()).first()
                        if version:
                            item = QtGui.QTableWidgetItem(version.status + '\n' + version.created_by.name)
                            item.setTextAlignment(132)
                            index = conf.status_list.index(version.status)
                            bgcolor = conf.status_bg_colors[index]
                            fgcolor = conf.status_fg_colors[index]
                            bg = item.background()
                            bg.setColor(QtGui.QColor(*bgcolor))
                            item.setBackground(bg)
                            fg = item.foreground()
                            fg.setColor(QtGui.QColor(*fgcolor))
                            item.setForeground(fg)
                            try:
                                item.setBackgroundColor(QtGui.QColor(*bgcolor))
                            except AttributeError:
                                pass

                            item.version = version
                        else:
                            item = QtGui.QTableWidgetItem('-')
                            item.setTextAlignment(132)
                            bg = item.background()
                            bg.setColor(QtGui.QColor(0, 0, 0))
                            item.setBackground(bg)
                            try:
                                item.setBackgroundColor(QtGui.QColor(0, 0, 0))
                            except AttributeError:
                                pass

                            item.version = None
                        items.append(item)

                    row += 1

            self.assets_tableWidget.setRowCount(row)
            item_index = 0
            for r in range(row):
                for c in range(column + 1):
                    item = items[item_index]
                    self.assets_tableWidget.setItem(r, c, item)
                    item_index += 1

            self.assets_tableWidget.resizeRowsToContents()
            for r in range(row):
                item_index = r * (column + 1)
                item = items[item_index]
                if item.has_thumbnail:
                    self.assets_tableWidget.setRowHeight(r, conf.thumbnail_size[1] / 2)

            self.assets_tableWidget.resizeColumnsToContents()
            self.assets_tableWidget.setColumnWidth(0, conf.thumbnail_size[0] / 2)
            return

    def fill_shots_tableWidget(self):
        """fills the shots_tableWidget
        """
        self.shots_tableWidget.clear()
        shot_vtypes = VersionType.query().filter(VersionType.type_for == 'Shot').order_by(VersionType.name).all()
        shot_vtype_codes = map(lambda x: x.code, shot_vtypes)
        labels = [
         'Thumbnail', 'Sequence', 'Number', 'Take']
        labels.extend(map(lambda x: x.code, shot_vtypes))
        self.shots_tableWidget.setColumnCount(len(labels))
        self.shots_tableWidget.setHorizontalHeaderLabels(labels)
        project = self.get_current_project()
        if project is None:
            return
        else:
            sequences = Sequence.query().filter(Sequence.project == project).order_by(Sequence.name).all()
            shot_count = db.query(func.count(Shot.id)).join(Sequence).filter(Sequence.id == Shot.sequence_id).filter(Sequence.project == project).all()[0][0]
            self.shots_tableWidget.setRowCount(shot_count)
            items = []
            row = 0
            column = 0
            for sequence in sequences:
                shots = Shot.query().filter(Shot.sequence == sequence).order_by(Shot.number).all()
                shots.sort(key=lambda x: utils.embedded_numbers(x.number))
                previous_shot = None
                for shot in shots:
                    take_names = map(lambda x: x[0], db.query(distinct(Version.take_name)).filter(Version.version_of == shot).all())
                    if not len(take_names):
                        take_names = [
                         '-']
                    for take_name in take_names:
                        column = 0
                        item = QtGui.QTableWidgetItem()
                        item.setTextAlignment(132)
                        if os.path.exists(shot.thumbnail_full_path):
                            thumbnail_full_path = shot.thumbnail_full_path
                            pixmap = QtGui.QPixmap(thumbnail_full_path)
                            pixmap = pixmap.scaled(conf.thumbnail_size[0] / 2, conf.thumbnail_size[1] / 2, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                            brush = QtGui.QBrush(pixmap)
                            item.has_thumbnail = True
                            item.setBackground(brush)
                        else:
                            item.has_thumbnail = False
                        items.append(item)
                        column = 1
                        item = QtGui.QTableWidgetItem(sequence.name)
                        item.setTextAlignment(132)
                        items.append(item)
                        column = 2
                        item = QtGui.QTableWidgetItem(shot.code)
                        item.setTextAlignment(132)
                        items.append(item)
                        column = 3
                        item = QtGui.QTableWidgetItem(take_name)
                        item.setTextAlignment(132)
                        items.append(item)
                        for type_code in shot_vtype_codes:
                            column += 1
                            version = Version.query().join(VersionType).filter(Version.version_of == shot).filter(Version.type_id == VersionType.id).filter(VersionType.code == type_code).filter(Version.take_name == take_name).order_by(Version.version_number.desc()).first()
                            if version:
                                item = QtGui.QTableWidgetItem(version.status + '\n' + version.created_by.name)
                                item.setTextAlignment(132)
                                index = conf.status_list.index(version.status)
                                bgcolor = conf.status_bg_colors[index]
                                fgcolor = conf.status_fg_colors[index]
                                bg = item.background()
                                bg.setColor(QtGui.QColor(*bgcolor))
                                item.setBackground(bg)
                                fg = item.foreground()
                                fg.setColor(QtGui.QColor(*fgcolor))
                                item.setForeground(fg)
                                try:
                                    item.setBackgroundColor(QtGui.QColor(*bgcolor))
                                except AttributeError:
                                    pass

                                item.version = version
                            else:
                                item = QtGui.QTableWidgetItem('-')
                                item.setTextAlignment(132)
                                bg = item.background()
                                bg.setColor(QtGui.QColor(0, 0, 0))
                                item.setBackground(bg)
                                try:
                                    item.setBackgroundColor(QtGui.QColor(0, 0, 0))
                                except AttributeError:
                                    pass

                                item.version = None
                            items.append(item)

                        row += 1

            self.shots_tableWidget.setRowCount(row)
            item_index = 0
            for r in range(row):
                for c in range(column + 1):
                    item = items[item_index]
                    self.shots_tableWidget.setItem(r, c, item)
                    item_index += 1

            self.shots_tableWidget.resizeRowsToContents()
            for r in range(row):
                item_index = r * (column + 1)
                item = items[item_index]
                if item.has_thumbnail:
                    self.shots_tableWidget.setRowHeight(r, conf.thumbnail_size[1] / 2)

            self.shots_tableWidget.resizeColumnsToContents()
            self.shots_tableWidget.setColumnWidth(0, conf.thumbnail_size[0] / 2)
            return

    def _show_assets_tableWidget_context_menu(self, position):
        """the custom context menu for the assets_tableWidget
        """
        self._add_custom_context_menu_to_table_widget(self.assets_tableWidget, position)

    def _show_shots_tableWidget_context_menu(self, position):
        """the custom context menu for the shots_tableWidget
        """
        self._add_custom_context_menu_to_table_widget(self.shots_tableWidget, position)

    def _add_custom_context_menu_to_table_widget(self, tableWidget, position):
        """Adds a custom context menu to the given table_widget, which is
        a Shot or Asset table
        :param tableWidget: The QTableWidget instance
        :param position: QPosition that the right click is occurred
        """
        global_position = tableWidget.mapToGlobal(position)
        menu = QtGui.QMenu()
        item = tableWidget.itemAt(position)
        version = None
        if hasattr(item, 'version'):
            version = item.version
        if not version:
            return
        else:
            for status in conf.status_list_long_names:
                action = QtGui.QAction(status, menu)
                action.setCheckable(True)
                if version.status == status:
                    action.setChecked(True)
                menu.addAction(action)

            menu.addSeparator()
            action = QtGui.QAction('Browse Outputs', menu)
            menu.addAction(action)
            selected_item = menu.exec_(global_position)
            if selected_item:
                choice = selected_item.text()
                if choice in conf.status_list_long_names:
                    version.status = choice
                    version.save()
                    assert isinstance(item, QtGui.QTableWidgetItem)
                    item.setText(version.status + '\n' + version.created_by.name)
                    index = conf.status_list.index(version.status)
                    bgcolor = conf.status_bg_colors[index]
                    fgcolor = conf.status_fg_colors[index]
                    bg = item.background()
                    bg.setColor(QtGui.QColor(*bgcolor))
                    item.setBackground(bg)
                    fg = item.foreground()
                    fg.setColor(QtGui.QColor(*fgcolor))
                    item.setForeground(fg)
                    item.setBackgroundColor(QtGui.QColor(*bgcolor))
                elif choice == 'Browse Outputs':
                    path = os.path.expandvars(version.output_path)
                    try:
                        utils.open_browser_in_location(path)
                    except IOError:
                        QtGui.QMessageBox.critical(self, 'Error', "Path doesn't exists:\n" + path)

            return