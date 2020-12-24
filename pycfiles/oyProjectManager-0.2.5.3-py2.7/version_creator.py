# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/ui/version_creator.py
# Compiled at: 2013-02-20 15:51:56
import os, re, sys, logging, datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import distinct
import oyProjectManager
from oyProjectManager import config, db, utils, Asset, User, EnvironmentBase, Project, Sequence, Shot, Version, VersionType, VersionTypeEnvironments
from oyProjectManager.ui import create_asset_dialog, version_updater, ui_utils
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
    from oyProjectManager.ui import version_creator_UI_pyside as version_creator_UI
elif qt_module == 'PyQt4':
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtGui, QtCore
    from oyProjectManager.ui import version_creator_UI_pyqt4 as version_creator_UI

def UI(environment=None, app_in=None, executor=None, mode=0):
    """the UI to call the dialog by itself
    
    :param environment: The
      :class:`~oyProjectManager.models.entity.EnvironmentBase` can be None to
      let the UI to work in "environmentless" mode in which it only creates
      data in database and copies the resultant version file path to clipboard.
    
    :param app_in: A Qt Application instance, which you can pass to let the UI
      be attached to the given applications event process.
    
    :param executor: Instead of calling app.exec_ the UI will call this given
      function. It also passes the created app instance to this executor.
    
    :param mode: Runs the UI either in Read-Write (0) mode or in Read-Only (1)
      mode.
    """
    global app
    global mainDialog
    self_quit = False
    if QtGui.QApplication.instance() is None:
        if not app_in:
            try:
                app = QtGui.QApplication(sys.argv)
            except AttributeError:
                app = QtGui.QApplication([])

        else:
            app = app_in
        self_quit = True
    else:
        app = QtGui.QApplication.instance()
    mainDialog = MainDialog(environment, mode=mode)
    mainDialog.show()
    if executor is None:
        app.exec_()
        if self_quit:
            app.connect(app, QtCore.SIGNAL('lastWindowClosed()'), app, QtCore.SLOT('quit()'))
    else:
        executor.exec_(app, mainDialog)
    return mainDialog


class MainDialog(QtGui.QDialog, version_creator_UI.Ui_Dialog):
    """The main version creation dialog for the system.
    
    This is the main interface that the users of the oyProjectManager will use
    to create a new Version.
    
    .. versionadded:: 0.2.5.2
       
       Now it is possible to run the version_creator UI in read-only mode where
       the UI is only for choosing previous versions. There will only be one
       button called "Choose" which returns the chosen Version instance.
    
    :param environment: It is an object which supplies **methods** like
      ``open``, ``save``, ``export``,  ``import`` or ``reference``. The most
      basic way to do this is to pass an instance of a class which is derived
      from the :class:`~oyProjectManager.models.entity.EnvironmentBase` which
      has all this methods but produces ``NotImplemented`` errors if the child
      class has not implemented these actions.
      
      The main duty of the Environment object is to introduce the host
      application (Maya, Houdini, Nuke, etc.) to oyProjectManager and let it to
      open, save, export, import or reference a file.
      
      .. versionadded:: 0.2.5
         No Environment Interaction
         
         From and after version 0.2.5 the UI is now able to handle the
         situation of not being bounded to an Environment. So if there is no
         Environment instance is given then the UI generates new Version
         instance and will allow the user to "copy" the full path of the newly
         generated Version. So environments which are not able to run Python
         code (Photoshop etc.) will also be able to contribute to projects.
    
    :param parent: The parent ``PySide.QtCore.QObject`` of this interface. It
      is mainly useful if this interface is going to be attached to a parent
      UI, like the Maya or Nuke.
    
    :param mode: Sets the UI in to Read-Write (mode=0) and Read-Only (mode=1)
      mode. Where in Read-Write there are all the buttons you would normally
      have (Export As, Save As, Open, Reference, Import), and in Read-Only mode
      it has only one button called "Choose" which lets you choose one Version.
    """

    def __init__(self, environment=None, parent=None, mode=0):
        logger.debug('initializing the interface')
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.mode = mode
        self.chosen_version = None
        window_title = 'Version Creator | ' + 'oyProjectManager v' + oyProjectManager.__version__
        if environment:
            window_title += ' | ' + environment.name
        else:
            window_title += ' | No Environment'
        if self.mode:
            window_title += ' | Read-Only Mode'
        else:
            window_title += ' | Normal Mode'
        self.setWindowTitle(window_title)
        if db.session is None:
            db.setup()
        self.environment = environment
        self.users_comboBox.users = []
        self.projects_comboBox.projects = []
        self.sequences_comboBox.sequences = []
        self.assets_tableWidget.assets = []
        self.shots_listWidget.shots = []
        self.input_dialog = None
        self.previous_versions_tableWidget.versions = []
        self.assets_tableWidget.labels = [
         'Type', 'Name']
        self.previous_versions_tableWidget.labels = [
         'Version',
         'User',
         'Status',
         'File Size',
         'Date',
         'Note']
        self._setup_signals()
        self._set_defaults()
        self._center_window()
        logger.debug('finished initializing the interface')
        return

    def _setup_signals(self):
        """sets up the signals
        """
        logger.debug('start setting up interface signals')
        QtCore.QObject.connect(self.close_pushButton, QtCore.SIGNAL('clicked()'), self.close)
        QtCore.QObject.connect(self.projects_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.project_changed)
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL('currentChanged(int)'), self.tabWidget_changed)
        QtCore.QObject.connect(self.sequences_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.sequences_comboBox_changed)
        QtCore.QObject.connect(self.assets_tableWidget, QtCore.SIGNAL('currentItemChanged(QTableWidgetItem*,QTableWidgetItem*)'), self.asset_changed)
        QtCore.QObject.connect(self.shots_listWidget, QtCore.SIGNAL('currentTextChanged(QString)'), self.shot_changed)
        QtCore.QObject.connect(self.version_types_listWidget, QtCore.SIGNAL('currentTextChanged(QString)'), self.version_types_listWidget_changed)
        QtCore.QObject.connect(self.takes_listWidget, QtCore.SIGNAL('currentTextChanged(QString)'), self.takes_listWidget_changed)
        QtCore.QObject.connect(self.add_type_toolButton, QtCore.SIGNAL('clicked()'), self.add_type_toolButton_clicked)
        self.assets_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self.assets_tableWidget, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self._show_assets_tableWidget_context_menu)
        self.previous_versions_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self.previous_versions_tableWidget, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self._show_previous_versions_tableWidget_context_menu)
        QtCore.QObject.connect(self.create_asset_pushButton, QtCore.SIGNAL('clicked()'), self.create_asset_pushButton_clicked)
        QtCore.QObject.connect(self.add_take_toolButton, QtCore.SIGNAL('clicked()'), self.add_take_toolButton_clicked)
        QtCore.QObject.connect(self.export_as_pushButton, QtCore.SIGNAL('clicked()'), self.export_as_pushButton_clicked)
        QtCore.QObject.connect(self.save_as_pushButton, QtCore.SIGNAL('clicked()'), self.save_as_pushButton_clicked)
        QtCore.QObject.connect(self.open_pushButton, QtCore.SIGNAL('clicked()'), self.open_pushButton_clicked)
        QtCore.QObject.connect(self.chose_pushButton, QtCore.SIGNAL('cliched()'), self.chose_pushButton_clicked)
        if self.mode:
            QtCore.QObject.connect(self.previous_versions_tableWidget, QtCore.SIGNAL('cellDoubleClicked(int,int)'), self.chose_pushButton_clicked)
        else:
            QtCore.QObject.connect(self.previous_versions_tableWidget, QtCore.SIGNAL('cellDoubleClicked(int,int)'), self.open_pushButton_clicked)
        QtCore.QObject.connect(self.reference_pushButton, QtCore.SIGNAL('clicked()'), self.reference_pushButton_clicked)
        QtCore.QObject.connect(self.import_pushButton, QtCore.SIGNAL('clicked()'), self.import_pushButton_clicked)
        QtCore.QObject.connect(self.show_published_only_checkBox, QtCore.SIGNAL('stateChanged(int)'), self.update_previous_versions_tableWidget)
        QtCore.QObject.connect(self.version_count_spinBox, QtCore.SIGNAL('valueChanged(int)'), self.update_previous_versions_tableWidget)
        QtCore.QObject.connect(self.shot_info_update_pushButton, QtCore.SIGNAL('clicked()'), self.shot_info_update_pushButton_clicked)
        QtCore.QObject.connect(self.upload_thumbnail_pushButton, QtCore.SIGNAL('clicked()'), self.upload_thumbnail_pushButton_clicked)
        logger.debug('finished setting up interface signals')

    def _show_assets_tableWidget_context_menu(self, position):
        """the custom context menu for the assets_tableWidget
        """
        if self.mode:
            return
        global_position = self.assets_tableWidget.mapToGlobal(position)
        menu = QtGui.QMenu()
        menu.addAction('Rename Asset')
        selected_item = menu.exec_(global_position)
        if selected_item:
            if selected_item.text() == 'Rename Asset':
                asset = self.get_versionable()
                self.input_dialog = QtGui.QInputDialog(self)
                new_asset_name, ok = self.input_dialog.getText(self, 'Rename Asset', 'New Asset Name', QtGui.QLineEdit.Normal, asset.name)
                if ok:
                    if new_asset_name != '':
                        asset.name = new_asset_name
                        asset.code = new_asset_name
                        asset.save()
                        self.tabWidget_changed(0)

    def _show_previous_versions_tableWidget_context_menu(self, position):
        """the custom context menu for the pervious_versions_tableWidget
        """
        global_position = self.previous_versions_tableWidget.mapToGlobal(position)
        item = self.previous_versions_tableWidget.itemAt(position)
        if not item:
            return
        index = item.row()
        version = self.previous_versions_tableWidget.versions[index]
        menu = QtGui.QMenu()
        if not self.mode:
            for status in conf.status_list_long_names:
                action = QtGui.QAction(status, menu)
                action.setCheckable(True)
                if version.status == status:
                    action.setChecked(True)
                menu.addAction(action)

            menu.addSeparator()
        menu.addAction('Browse Output Path...')
        menu.addSeparator()
        if not self.mode:
            menu.addAction('Change Note...')
            menu.addSeparator()
        menu.addAction('Copy Path')
        menu.addAction('Copy Output Path')
        selected_item = menu.exec_(global_position)
        if selected_item:
            choice = selected_item.text()
            if choice in conf.status_list_long_names:
                if version:
                    version.status = selected_item.text()
                    version.save()
                    self.update_previous_versions_tableWidget()
                    return
            elif choice == 'Browse Output Path...':
                path = os.path.expandvars(version.output_path)
                try:
                    utils.open_browser_in_location(path)
                except IOError:
                    QtGui.QMessageBox.critical(self, 'Error', "Path doesn't exists:\n" + path)

            elif choice == 'Change Note...':
                if version:
                    self.input_dialog = QtGui.QInputDialog(self)
                    new_note, ok = self.input_dialog.getText(self, 'Enter the new note', 'Please enter the new note:', QtGui.QLineEdit.Normal, version.note)
                    if ok:
                        version.note = new_note
                        version.save()
                        self.update_previous_versions_tableWidget()
            elif choice == 'Copy Path':
                clipboard = QtGui.QApplication.clipboard()
                clipboard.setText(os.path.normpath(version.full_path))
            elif choice == 'Copy Output Path':
                clipboard = QtGui.QApplication.clipboard()
                clipboard.setText(os.path.normpath(version.output_path))

    def rename_asset(self, asset, new_name):
        """Renames the asset with the given new name
        
        :param asset: The :class:`~oyProjectManager.models.asset.Asset` instance
          to be renamed.
        
        :param new_name: The desired new name for the asset.
        """
        pass

    def _center_window(self):
        """centers the window to the screen
        """
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) * 0.5, (screen.height() - size.height()) * 0.5)

    def _set_defaults(self):
        """sets up the defaults for the interface
        """
        logger.debug('started setting up interface defaults')
        self.clear_thumbnail()
        self.statuses_comboBox.clear()
        self.statuses_comboBox.addItems(conf.status_list_long_names)
        projects = Project.query().filter(Project.active == True).order_by(Project.name).all()
        self.projects_comboBox.addItems(map(lambda x: x.name, projects))
        self.projects_comboBox.projects = projects
        users = User.query().filter(User.active == True).order_by(User.name).all()
        self.users_comboBox.users = users
        self.users_comboBox.addItems(map(lambda x: x.name, users))
        last_user_id = conf.last_user_id
        if last_user_id:
            logger.debug('last_user_id: %i' % last_user_id)
        else:
            logger.debug('no last user is set before')
        last_user = None
        if last_user_id is not None:
            last_user = User.query().filter(User.id == last_user_id).first()
        logger.debug('last_user: %s' % last_user)
        if last_user is not None:
            index = self.users_comboBox.findText(last_user.name)
            logger.debug('last_user index in users_comboBox: %i' % index)
            if index != -1:
                self.users_comboBox.setCurrentIndex(index)
        self.takes_listWidget.addItem(conf.default_take_name)
        item = self.takes_listWidget.item(0)
        self.takes_listWidget.setCurrentItem(item)
        self.project_changed()
        if self.environment and isinstance(self.environment, EnvironmentBase):
            logger.debug('restoring the ui with the version from environment')
            version_from_env = self.environment.get_last_version()
            logger.debug('version_from_env: %s' % version_from_env)
            self.restore_ui(version_from_env)
        else:
            self.export_as_pushButton.setVisible(False)
            self.reference_pushButton.setVisible(False)
            self.import_pushButton.setVisible(False)
        if self.mode:
            self.create_asset_pushButton.setVisible(False)
            self.add_type_toolButton.setVisible(False)
            self.add_take_toolButton.setVisible(False)
            self.note_label.setVisible(False)
            self.note_textEdit.setVisible(False)
            self.status_label.setVisible(False)
            self.statuses_comboBox.setVisible(False)
            self.publish_checkBox.setVisible(False)
            self.update_paths_checkBox.setVisible(False)
            self.export_as_pushButton.setVisible(False)
            self.save_as_pushButton.setVisible(False)
            self.open_pushButton.setVisible(False)
            self.reference_pushButton.setVisible(False)
            self.import_pushButton.setVisible(False)
            self.upload_thumbnail_pushButton.setVisible(False)
            self.user_label.setVisible(False)
            self.users_comboBox.setVisible(False)
            self.shot_info_update_pushButton.setVisible(False)
            self.frame_range_label.setVisible(False)
            self.handles_label.setVisible(False)
            self.start_frame_spinBox.setVisible(False)
            self.end_frame_spinBox.setVisible(False)
            self.handle_at_end_spinBox.setVisible(False)
            self.handle_at_start_spinBox.setVisible(False)
        else:
            self.chose_pushButton.setVisible(False)
        self.note_textEdit.setText('')
        logger.debug('finished setting up interface defaults')
        return

    def restore_ui(self, version):
        """Restores the UI with the given Version instance
        
        :param version: :class:`~oyProjectManager.models.version.Version`
          instance
        """
        logger.debug('restoring ui with the given version: %s', version)
        if version is None or not version.project.active:
            return
        index = self.projects_comboBox.findText(version.project.name)
        if index != -1:
            self.projects_comboBox.setCurrentIndex(index)
        else:
            return
        versionable = version.version_of
        if isinstance(versionable, Asset):
            self.tabWidget.setCurrentIndex(0)
            items = self.assets_tableWidget.findItems(versionable.name, QtCore.Qt.MatchExactly)
            item = None
            if items:
                item = items[0]
            else:
                return
            logger.debug('*******************************')
            logger.debug('item: %s' % item)
            self.assets_tableWidget.setCurrentItem(item)
        else:
            self.tabWidget.setCurrentIndex(1)
            index = self.sequences_comboBox.findText(versionable.sequence.name)
            if index != -1:
                self.sequences_comboBox.setCurrentIndex(index)
            else:
                return
            items = self.shots_listWidget.findItems(versionable.code, QtCore.Qt.MatchExactly)
            item = None
            if items:
                item = items[0]
            else:
                return
            self.shots_listWidget.setCurrentItem(item)
        type_name = version.type.name
        logger.debug('finding type with name: %s' % type_name)
        items = self.version_types_listWidget.findItems(type_name, QtCore.Qt.MatchExactly)
        if not items:
            logger.debug('no items found with: %s' % type_name)
            return
        else:
            self.version_types_listWidget.setCurrentItem(items[0])
            take_name = version.take_name
            logger.debug('finding take with name: %s' % take_name)
            items = self.takes_listWidget.findItems(take_name, QtCore.Qt.MatchExactly)
            self.takes_listWidget.setCurrentItem(items[0])
            return

    def project_changed(self):
        """updates the assets list_widget and sequences_comboBox for the 
        """
        logger.debug('project_comboBox has changed in the UI')
        project = self.get_current_project()
        if project:
            self.client_name_label.setText(project.client.name if project.client else 'N/A')
        curr_tab_index = self.tabWidget.currentIndex()
        self.tabWidget_changed(curr_tab_index)

    def tabWidget_changed(self, index):
        """called when the tab widget is changed
        """
        proj = self.get_current_project()
        self.clear_thumbnail()
        self.clear_previous_versions_tableWidget()
        if index == 0:
            logger.debug('tabWidget index changed to asset')
            assets = Asset.query().filter(Asset.project == proj).order_by(Asset.type).order_by(Asset.name).all()
            self.assets_tableWidget.assets = assets
            self.assets_tableWidget.clear()
            self.assets_tableWidget.setRowCount(len(assets))
            self.assets_tableWidget.setHorizontalHeaderLabels(self.assets_tableWidget.labels)
            for i, asset in enumerate(assets):
                item = QtGui.QTableWidgetItem(asset.type)
                item.setTextAlignment(129)
                self.assets_tableWidget.setItem(i, 0, item)
                item = QtGui.QTableWidgetItem(asset.name)
                item.setTextAlignment(129)
                self.assets_tableWidget.setItem(i, 1, item)

            self.assets_tableWidget.resizeColumnsToContents()
            table_item = self.assets_tableWidget.item(0, 0)
            if table_item is not None:
                self.assets_tableWidget.selectRow(0)
                self.asset_changed()
            else:
                self.version_types_listWidget.clear()
                self.takes_listWidget.clear()
                self.takes_listWidget.addItem(conf.default_take_name)
                item = self.takes_listWidget.item(0)
                self.takes_listWidget.setCurrentItem(item)
        elif self.tabWidget.currentIndex() == 1:
            logger.debug('tabWidget index changed to shots')
            seqs = Sequence.query().filter(Sequence.project == proj).all()
            self.sequences_comboBox.clear()
            self.sequences_comboBox.addItems([ seq.name for seq in seqs ])
            self.sequences_comboBox.sequences = seqs
            if self.sequences_comboBox.count():
                self.sequences_comboBox.setCurrentIndex(0)
                self.sequences_comboBox_changed(0)
            else:
                self.shots_listWidget.clear()
                self.version_types_listWidget.clear()
                self.takes_listWidget.clear()
                self.takes_listWidget.addItem(conf.default_take_name)
                item = self.takes_listWidget.item(0)
                self.takes_listWidget.setCurrentItem(item)
        return

    def sequences_comboBox_changed(self, index):
        """called when the sequences_comboBox index has changed
        """
        logger.debug('sequences_comboBox changed')
        try:
            seq = self.sequences_comboBox.sequences[index]
        except IndexError:
            logger.debug('there is no sequences cached in sequence_comboBox')
            return

        shots = Shot.query().filter(Shot.sequence == seq).all()
        shots.sort(key=lambda x: utils.embedded_numbers(x.number))
        self.shots_listWidget.clear()
        self.shots_listWidget.addItems([ shot.code for shot in shots ])
        self.shots_listWidget.shots = shots
        list_item = self.shots_listWidget.item(0)
        self.clear_thumbnail()
        if list_item is not None:
            self.shots_listWidget.setCurrentItem(list_item)
        return

    def asset_changed(self):
        """updates the asset related fields with the current asset information
        """
        proj = self.get_current_project()
        asset = self.get_versionable()
        if asset is None:
            return
        else:
            if self.environment is None:
                types = map(lambda x: x[0], db.query(distinct(VersionType.name)).join(Version).filter(Version.version_of == asset).all())
            else:
                types = map(lambda x: x[0], db.query(distinct(VersionType.name)).join(VersionTypeEnvironments).join(Version).filter(VersionTypeEnvironments.environment_name == self.environment.name).filter(Version.version_of == asset).all())
            self.version_types_listWidget.clear()
            self.version_types_listWidget.addItems(types)
            item = self.version_types_listWidget.item(0)
            self.version_types_listWidget.setCurrentItem(item)
            self.update_thumbnail()
            return

    def get_current_shot(self):
        """returns the current selected shot in the interface
        """
        index = self.shots_listWidget.currentIndex().row()
        shot = self.shots_listWidget.shots[index]
        return shot

    def shot_changed(self, shot_name):
        """updates the shot related fields with the current shot information
        """
        proj = self.get_current_project()
        shot = self.get_current_shot()
        self.start_frame_spinBox.setValue(shot.start_frame)
        self.end_frame_spinBox.setValue(shot.end_frame)
        self.handle_at_start_spinBox.setValue(shot.handle_at_start)
        self.handle_at_end_spinBox.setValue(shot.handle_at_end)
        if self.environment is None:
            types = map(lambda x: x[0], db.query(distinct(VersionType.name)).join(Version).filter(Version.version_of == shot).all())
        else:
            types = map(lambda x: x[0], db.query(distinct(VersionType.name)).join(VersionTypeEnvironments).join(Version).filter(VersionTypeEnvironments.environment_name == self.environment.name).filter(Version.version_of == shot).all())
        self.clear_previous_versions_tableWidget()
        self.version_types_listWidget.clear()
        self.version_types_listWidget.addItems(types)
        item = self.version_types_listWidget.item(0)
        self.version_types_listWidget.setCurrentItem(item)
        self.update_thumbnail()
        return

    def shot_info_update_pushButton_clicked(self):
        """runs when the shot_info_update_pushButton is clicked
        """
        shot = self.get_current_shot()
        start_frame = self.start_frame_spinBox.value()
        end_frame = self.end_frame_spinBox.value()
        handle_at_start = self.handle_at_start_spinBox.value()
        handle_at_end = self.handle_at_end_spinBox.value()
        shot.start_frame = start_frame
        shot.end_frame = end_frame
        shot.handle_at_start = handle_at_start
        shot.handle_at_end = handle_at_end

    def version_types_listWidget_changed(self, index):
        """runs when the asset version types comboBox has changed
        """
        versionable = self.get_versionable()
        version_type_name = ''
        item = self.version_types_listWidget.currentItem()
        if item:
            version_type_name = item.text()
        self.takes_listWidget.clear()
        self.clear_previous_versions_tableWidget()
        if version_type_name != '':
            logger.debug('version_type_name: %s' % version_type_name)
        else:
            return
        takes = map(lambda x: x[0], db.query(distinct(Version.take_name)).join(VersionType).filter(VersionType.name == version_type_name).filter(Version.version_of == versionable).all())
        logger.debug('len(takes) from db: %s' % len(takes))
        if len(takes) == 0:
            logger.debug('appending the default take name')
            self.takes_listWidget.addItem(conf.default_take_name)
        else:
            logger.debug('adding the takes from db')
            self.takes_listWidget.addItems(takes)
        logger.debug('setting the first element selected')
        item = self.takes_listWidget.item(0)
        self.takes_listWidget.setCurrentItem(item)

    def takes_listWidget_changed(self, index):
        """runs when the takes_listWidget has changed
        """
        self.update_previous_versions_tableWidget()
        versionable = self.get_versionable()
        version_type_name = ''
        item = self.version_types_listWidget.currentItem()
        if item:
            version_type_name = item.text()
        take_name = ''
        item = self.takes_listWidget.currentItem()
        if item:
            take_name = item.text()
        query = Version.query().join(VersionType).filter(VersionType.name == version_type_name).filter(Version.version_of == versionable).filter(Version.take_name == take_name)
        version = query.order_by(Version.version_number.desc()).first()
        if version:
            status_index = conf.status_list.index(version.status)
            status_long_name = conf.status_list_long_names[status_index]
            index = self.statuses_comboBox.findText(status_long_name)
            if index != -1:
                self.statuses_comboBox.setCurrentIndex(index)

    def clear_previous_versions_tableWidget(self):
        """clears the previous_versions_tableWidget properly
        """
        self.previous_versions_tableWidget.clear()
        self.previous_versions_tableWidget.versions = []
        self.previous_versions_tableWidget.setHorizontalHeaderLabels(self.previous_versions_tableWidget.labels)

    def update_previous_versions_tableWidget(self):
        """updates the previous_versions_tableWidget
        """
        versionable = self.get_versionable()
        version_type_name = ''
        item = self.version_types_listWidget.currentItem()
        if item:
            version_type_name = item.text()
        self.clear_previous_versions_tableWidget()
        if version_type_name != '':
            logger.debug('version_type_name: %s' % version_type_name)
        else:
            self.previous_versions_tableWidget.versions = []
            return
        take_name = ''
        item = self.takes_listWidget.currentItem()
        if item:
            take_name = item.text()
        if take_name != '':
            logger.debug('take_name: %s' % take_name)
        else:
            return
        query = Version.query().join(VersionType).filter(VersionType.name == version_type_name).filter(Version.version_of == versionable).filter(Version.take_name == take_name)
        if self.show_published_only_checkBox.isChecked():
            query = query.filter(Version.is_published == True)
        count = self.version_count_spinBox.value()
        versions = query.order_by(Version.version_number.desc()).limit(count).all()
        versions.reverse()
        self.previous_versions_tableWidget.versions = versions
        self.previous_versions_tableWidget.setRowCount(len(versions))

        def set_font(item):
            """sets the font for the given item
            
            :param item: the a QTableWidgetItem
            """
            my_font = item.font()
            my_font.setBold(True)
            item.setFont(my_font)
            foreground = item.foreground()
            foreground.setColor(QtGui.QColor(0, 192, 0))
            item.setForeground(foreground)

        for i, vers in enumerate(versions):
            is_published = vers.is_published
            item = QtGui.QTableWidgetItem(str(vers.version_number))
            item.setTextAlignment(132)
            if is_published:
                set_font(item)
            self.previous_versions_tableWidget.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem(vers.created_by.name)
            item.setTextAlignment(129)
            if is_published:
                set_font(item)
            self.previous_versions_tableWidget.setItem(i, 1, item)
            item = QtGui.QTableWidgetItem(vers.status)
            item.setTextAlignment(132)
            index = conf.status_list.index(vers.status)
            bgcolor = conf.status_bg_colors[index]
            fgcolor = conf.status_fg_colors[index]
            bg = item.background()
            bg.setColor(QtGui.QColor(*bgcolor))
            item.setBackground(bg)
            fg = item.foreground()
            fg.setColor(QtGui.QColor(*fgcolor))
            try:
                item.setBackgroundColor(QtGui.QColor(*bgcolor))
            except AttributeError:
                pass

            self.previous_versions_tableWidget.setItem(i, 2, item)
            file_size = -1
            if os.path.exists(vers.full_path):
                file_size = float(os.path.getsize(vers.full_path)) / 1024 / 1024
            item = QtGui.QTableWidgetItem(conf.file_size_format % file_size)
            item.setTextAlignment(129)
            if is_published:
                set_font(item)
            self.previous_versions_tableWidget.setItem(i, 3, item)
            file_date = datetime.datetime.today()
            if os.path.exists(vers.full_path):
                file_date = datetime.datetime.fromtimestamp(os.path.getmtime(vers.full_path))
            item = QtGui.QTableWidgetItem(file_date.strftime(conf.time_format))
            item.setTextAlignment(129)
            if is_published:
                set_font(item)
            self.previous_versions_tableWidget.setItem(i, 4, item)
            item = QtGui.QTableWidgetItem(vers.note)
            item.setTextAlignment(129)
            if is_published:
                set_font(item)
            self.previous_versions_tableWidget.setItem(i, 5, item)

        self.previous_versions_tableWidget.resizeRowsToContents()
        self.previous_versions_tableWidget.resizeColumnsToContents()
        self.previous_versions_tableWidget.resizeRowsToContents()

    def create_asset_pushButton_clicked(self):
        """displays an input dialog and creates a new asset if everything is ok
        """
        dialog = create_asset_dialog.create_asset_dialog(parent=self)
        dialog.exec_()
        ok = dialog.ok
        asset_name = dialog.asset_name_lineEdit.text()
        asset_type_name = dialog.asset_types_comboBox.currentText()
        logger.debug('new asset_name: %s' % asset_name)
        logger.debug('new asset_type_name: %s' % asset_type_name)
        if not ok:
            return
        if asset_name == '' or asset_type_name == '':
            error_message = 'The given Asset.name or Asset.type is empty!!!\n\nNot creating any new asset!'
            QtGui.QMessageBox.critical(self, 'Error', error_message)
            return
        proj = self.get_current_project()
        try:
            new_asset = Asset(proj, asset_name, type=asset_type_name)
            new_asset.save()
            proj.create()
            self.project_changed()
        except (TypeError, ValueError, IntegrityError) as e:
            error_message = str(e)
            if isinstance(e, IntegrityError):
                db.session.rollback()
                error_message = 'Asset.name or Asset.code is not unique'
            QtGui.QMessageBox.critical(self, 'Error', error_message)
            return

    def get_versionable(self):
        """returns the versionable from the UI, it is an asset or a shot
        depending on to the current tab
        """
        proj = self.get_current_project()
        versionable = None
        if self.tabWidget.currentIndex() == 0:
            index = self.assets_tableWidget.currentRow()
            if index != -1:
                versionable = self.assets_tableWidget.assets[index]
        else:
            index = self.shots_listWidget.currentIndex().row()
            if index != -1:
                versionable = self.shots_listWidget.shots[index]
        logger.debug('versionable: %s' % versionable)
        return versionable

    def get_version_type(self):
        """returns the VersionType instance by looking at the UI elements. It
        will return the correct VersionType by looking at if it is an Asset or
        a Shot and picking the name of the VersionType from the comboBox
        
        :returns: :class:`~oyProjectManager.models.version.VersionType`
        """
        project = self.get_current_project()
        if project is None:
            return
        else:
            versionable = self.get_versionable()
            type_for = versionable.__class__.__name__
            version_type_name = ''
            item = self.version_types_listWidget.currentItem()
            if item:
                version_type_name = item.text()
            return VersionType.query().filter(VersionType.type_for == type_for).filter(VersionType.name == version_type_name).first()

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

    def add_type(self, version_type):
        """adds new types to the version_types_listWidget
        """
        if not isinstance(version_type, VersionType):
            raise TypeError('please supply a oyProjectManager.models.version.VersionType for the type to be added to the version_types_listWidget')
        versionable = self.get_versionable()
        if versionable.__class__.__name__ != version_type.type_for:
            raise TypeError('The given version_type is not suitable for %s' % self.tabWidget.tabText(self.tabWidget.currentIndex()))
        items = self.version_types_listWidget.findItems(version_type.name, QtCore.Qt.MatchExactly)
        if not len(items):
            self.version_types_listWidget.addItem(version_type.name)
            index = self.version_types_listWidget.count() - 1
            item = self.version_types_listWidget.item(index)
            self.version_types_listWidget.setCurrentItem(item)

    def add_type_toolButton_clicked(self):
        """adds a new type for the currently selected Asset or Shot
        """
        proj = self.get_current_project()
        versionable = self.get_versionable()
        current_types = []
        for index in range(self.version_types_listWidget.count()):
            current_types.append(self.version_types_listWidget.item(index).text())

        if self.environment:
            available_types = map(lambda x: x[0], db.query(distinct(VersionType.name)).join(VersionTypeEnvironments).filter(VersionType.type_for == versionable.__class__.__name__).filter(VersionTypeEnvironments.environment_name == self.environment.name).filter(~VersionType.name.in_(current_types)).all())
        else:
            available_types = map(lambda x: x[0], db.query(distinct(VersionType.name)).filter(VersionType.type_for == versionable.__class__.__name__).filter(~VersionType.name.in_(current_types)).all())
        self.input_dialog = QtGui.QInputDialog(self)
        if self.environment:
            type_name, ok = self.input_dialog.getItem(self, 'Choose a VersionType', 'Available Version Types for %ss in %s' % (
             versionable.__class__.__name__, self.environment.name), available_types, 0, False)
        else:
            type_name, ok = self.input_dialog.getItem(self, 'Choose a VersionType', 'Available Version Types for %ss' % versionable.__class__.__name__, available_types, 0, False)
        if ok:
            vers_type = VersionType.query().filter_by(name=type_name).first()
            try:
                self.add_type(vers_type)
            except TypeError:
                return

    def add_take_toolButton_clicked(self):
        """runs when the add_take_toolButton clicked
        """
        self.input_dialog = QtGui.QInputDialog(self)
        current_take_name = self.takes_listWidget.currentItem().text()
        take_name, ok = self.input_dialog.getText(self, 'Add Take Name', 'New Take Name', QtGui.QLineEdit.Normal, current_take_name)
        if ok:
            if take_name != '':
                take_name = take_name.title()
                take_name = re.sub('[\\s\\-]+', '_', take_name)
                take_name = re.sub('[^a-zA-Z0-9_]+', '', take_name)
                take_name = re.sub('[_]+', '_', take_name)
                take_name = re.sub('[_]+$', '', take_name)
                in_list = False
                for i in range(self.takes_listWidget.count()):
                    item = self.takes_listWidget.item(i)
                    if item.text() == take_name:
                        in_list = True

                if not in_list:
                    self.takes_listWidget.addItem(take_name)
                    self.takes_listWidget.sortItems()
                    items = self.takes_listWidget.findItems(take_name, QtCore.Qt.MatchExactly)
                    if items:
                        item = items[0]
                        self.takes_listWidget.setCurrentItem(item)

    def get_new_version(self):
        """returns a :class:`~oyProjectManager.models.version.Version` instance
        from the UI by looking at the input fields
        
        :returns: :class:`~oyProjectManager.models.version.Version` instance
        """
        versionable = self.get_versionable()
        version_type = self.get_version_type()
        take_name = self.takes_listWidget.currentItem().text()
        user = self.get_user()
        note = self.note_textEdit.toPlainText()
        published = self.publish_checkBox.isChecked()
        status = self.statuses_comboBox.currentText()
        version = Version(versionable, versionable.code, version_type, user, take_name=take_name, note=note, is_published=published, status=status)
        return version

    def get_previous_version(self):
        """returns the :class:`~oyProjectManager.models.version.Version`
        instance from the UI by looking at the previous_versions_tableWidget
        """
        index = self.previous_versions_tableWidget.currentRow()
        try:
            version = self.previous_versions_tableWidget.versions[index]
            return version
        except IndexError:
            return

        return

    def get_user(self):
        """returns the current User instance from the interface by looking at
        the name of the user from the users comboBox
        
        :return: :class:`~oyProjectManager.models.auth.User` instance
        """
        index = self.users_comboBox.currentIndex()
        return self.users_comboBox.users[index]

    def export_as_pushButton_clicked(self):
        """runs when the export_as_pushButton clicked
        """
        logger.debug('exporting the data as a new version')
        new_version = self.get_new_version()
        if self.environment is not None:
            self.environment.export_as(new_version)
            if logger.level != logging.DEBUG:
                QtGui.QMessageBox.information(self, 'Export', new_version.filename + '\n\n has been exported correctly!', QtGui.QMessageBox.Ok)
        return

    def save_as_pushButton_clicked(self):
        """runs when the save_as_pushButton clicked
        """
        logger.debug('saving the data as a new version')
        try:
            new_version = self.get_new_version()
        except (TypeError, ValueError) as e:
            QtGui.QMessageBox.critical(self, 'Error', e)
            return

        if self.environment and isinstance(self.environment, EnvironmentBase):
            try:
                self.environment.save_as(new_version)
            except RuntimeError as e:
                QtGui.QMessageBox.critical(self, 'Error', str(e))
                return

        else:
            logger.debug('No environment given, just generating paths')
            clipboard = QtGui.QApplication.clipboard()
            v_path = os.path.normpath(new_version.full_path)
            clipboard.setText(v_path)
            try:
                logger.debug('creating path for new version')
                os.makedirs(new_version.path)
            except OSError:
                pass

            try:
                logger.debug('creating output_path for new version')
                os.makedirs(new_version.output_path)
            except OSError:
                pass

            QtGui.QMessageBox.warning(self, 'Path Generated', 'A new Version is created at:\n\n' + v_path + '\n\n' + 'And the path is copied to your clipboard!!!', QtGui.QMessageBox.Ok)
        db.session.add(new_version)
        db.session.commit()
        conf.last_user_id = new_version.created_by.id
        if self.environment:
            self.close()
        else:
            self.project_changed()
        return

    def chose_pushButton_clicked(self):
        """runs when the chose_pushButton clicked
        """
        self.chosen_version = self.get_previous_version()
        if self.chosen_version:
            logger.debug(self.chosen_version)
            self.close()

    def open_pushButton_clicked(self):
        """runs when the open_pushButton clicked
        """
        old_version = self.get_previous_version()
        logger.debug('opening version %s' % old_version)
        if self.environment is not None:
            to_update_list = []
            try:
                envStatus, to_update_list = self.environment.open_(old_version)
            except RuntimeError as e:
                answer = QtGui.QMessageBox.question(self, 'RuntimeError', 'There are <b>unsaved changes</b> in the current scene<br><br>Do you really want to open the file?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                envStatus = False
                if answer == QtGui.QMessageBox.Yes:
                    envStatus, to_update_list = self.environment.open_(old_version, True)
                else:
                    return

            if len(to_update_list):
                version_updater_mainDialog = version_updater.MainDialog(self.environment, self)
                version_updater_mainDialog.exec_()
            self.environment.post_open(old_version)
        self.close()
        return

    def reference_pushButton_clicked(self):
        """runs when the reference_pushButton clicked
        """
        previous_version = self.get_previous_version()
        if not previous_version.is_published:
            QtGui.QMessageBox.critical(self, 'Critical Error', 'Referencing <b>un-published versions</b> are not allowed!\nPlease reference a published version of the same Asset/Shot', QtGui.QMessageBox.Ok)
            return
        else:
            logger.debug('referencing version %s' % previous_version)
            if self.environment is not None:
                self.environment.reference(previous_version)
                if logger.level != logging.DEBUG:
                    QtGui.QMessageBox.information(self, 'Reference', previous_version.filename + '\n\n has been referenced correctly!', QtGui.QMessageBox.Ok)
            return

    def import_pushButton_clicked(self):
        """runs when the import_pushButton clicked
        """
        previous_version = self.get_previous_version()
        logger.debug('importing version %s' % previous_version)
        if self.environment is not None:
            self.environment.import_(previous_version)
            if logger.level != logging.DEBUG:
                QtGui.QMessageBox.information(self, 'Import', previous_version.filename + '\n\n has been imported correctly!', QtGui.QMessageBox.Ok)
        return

    def clear_thumbnail(self):
        """clears the thumbnail_graphicsView
        """
        ui_utils.clear_thumbnail(self.thumbnail_graphicsView)

    def update_thumbnail(self):
        """updates the thumbnail for the selected versionable
        """
        versionable = self.get_versionable()
        ui_utils.update_gview_with_versionable_thumbnail(versionable, self.thumbnail_graphicsView)

    def upload_thumbnail_pushButton_clicked(self):
        """runs when the upload_thumbnail_pushButton is clicked
        """
        thumbnail_full_path = ui_utils.choose_thumbnail(self)
        if thumbnail_full_path == '':
            return
        versionable = self.get_versionable()
        ui_utils.upload_thumbnail(versionable, thumbnail_full_path)
        self.update_thumbnail()